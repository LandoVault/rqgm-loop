#!/usr/bin/env python3
"""rqgm_check.py - optional, read-only auditor for an RQGM v3 MEMORY (archive.jsonl).

  audit MEMORY [--done DONE.json] [--target DIR] [--pending ROUND.json] [--first]
  selftest [DIR]        (DIR holds expected.json and fixtures/; default <repo>/tests/checker)
  hash FILE... [--lf]   (the only source of setup.check_hashes)

It recomputes every keep, drop, Check value, halt and exit from the records and reports findings
{code, class, record_index (file line), expected, actual}; it never decides. Classes: VIOLATION (a
decision differs), RECORD (inconsistent, no decision changed), AMBIGUOUS (advisory). A rule whose
inputs are missing is listed as unauditable, never violated. Rounds are counted from round records,
never from logged numbers; loop time excludes waits for the human (rung, amend, held-out, exit, resume).
Python >= 3.9 stdlib only; no network, no model calls, no clock; never writes a file.
Exit: 0 no VIOLATION, 1 violations, 2 integrity or usage error.
"""
import copy, difflib, hashlib, json, os, sys  # noqa: E401
from datetime import datetime

RECORD = {'ORDER_MISMAP', 'KEPT_ID_MISMATCH', 'VERSION_MISSING', 'ROUND_SEQUENCE', 'MISLABEL', 'JUDGED_AFTER_GATE',
          'RESUME_MISMATCH', 'AFTER_EXIT', 'EXTRA_VERDICT', 'PROBE_REROLL', 'RUNG_REPEATED', 'SETUP_CHECK_LATE',
          'SETUP_REPEATED', 'VERSION_ID_REUSED', 'FINAL_RUNG_CONFLICT'}
AMBIGUOUS = {'OSCILLATION_MISSED', 'OSCILLATION_UNSUPPORTED', 'MULTI_SECTION', 'REJECTED_IDEA'}
DONE_VALS = ('variant', 'best', 'tie')          # "completed" judge values
VALUES = DONE_VALS + ('UNKNOWN', 'ERROR')
BAD = (TypeError, AttributeError, ValueError, KeyError)   # a malformed field: that record is unauditable
hid = lambda x: x if isinstance(x, (str, int, float, type(None))) else json.dumps(x)  # noqa: E731 (ids as keys)
num = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)  # noqa: E731

class Stop(Exception):  """--first: raised at the first VIOLATION, so nothing later is evaluated."""

def minutes(x):
    if num(x): return float(x)
    try:
        return datetime.fromisoformat(x.replace('Z', '+00:00')).timestamp() / 60.0
    except (AttributeError, TypeError, ValueError):
        return None

def diffs(var):
    d = (var or {}).get('diff')
    return d if isinstance(d, list) else [d] if isinstance(d, dict) else []

def same_text(a, b):  # the judged text is section, old and new (and file when both name one)
    ks = lambda x, y: ('section', 'old', 'new') + (('file',) if 'file' in x and 'file' in y else ())  # noqa: E731
    return len(a) == len(b) and all(all(x.get(k) == y.get(k) for k in ks(x, y)) if isinstance(x, dict) and
                                    isinstance(y, dict) else x == y for x, y in zip(a, b))

def sha(path, lf=False):
    with open(path, 'rb') as f:
        b = f.read()
    return hashlib.sha256(b.replace(b'\r\n', b'\n') if lf else b).hexdigest()

def parse(s):
    try:
        r = json.loads(s)
    except (ValueError, RecursionError):             # RecursionError: deeply nested garbage
        return None
    return r if isinstance(r, dict) else None

def load(path, text=None):
    """-> (records [(line, dict)], torn_line, set_aside_lines, integrity_line)."""
    if text is None:
        with open(path, 'rb') as f:
            text = f.read().decode('utf-8', 'replace')
    lines = (text[1:] if text[:1] == '\ufeff' else text).split('\n')   # a UTF-8 BOM is not content
    full = [i for i, s in enumerate(lines, 1) if s.strip()]
    recs, aside = [], []
    for k, i in enumerate(full):
        rec = parse(lines[i - 1])
        if k == len(full) - 1 and (rec is None or i == len(lines)):
            return recs, i, aside, None          # torn tail (unparsable or newline-less): excluded
        if rec is None:
            nxt = parse(lines[full[k + 1] - 1])
            if nxt and (nxt.get('t') or nxt.get('type')) == 'resume':
                aside.append(i)                  # a torn line that a resume set aside
                continue
            return recs, None, aside, i          # interior corruption: nothing after it is audited
        recs.append((i, rec))
    return recs, None, aside, None

class Audit:
    def __init__(self, first=False):
        self.first, self.idx, self.findings, self.unaud, self.warnings = first, 0, [], [], []
        self.setup, self.setup_idx, self.crit, self.done, self.final = None, 0, {}, None, 'E2'
        self.best, self.best_words, self.rung, self.probes = 'v0', None, 'E1', {}   # probes: rung -> mode
        # Round-derived state; restored from a snapshot when an unfinished round is rerun on resume.
        self.rs = dict(s=0, e=0, n=0, cnt=0, maxdur=None, tok=0.0, tok_all=True, maxtok=None, latest={},
                       hist={}, ratio=0.0, any_round=False)
        self.snap = self.due = self.pend = self.osc = self.start = self.now = self.last_eval = self.e3 = None
        self.epoch, self.amends, self.standing, self.hofail, self.heldout = 0, [], {}, {}, []
        self.subs, self.opened, self.cites, self.exited, self.exit_status = {}, {}, [], False, None
        self.vers, self.ideas, self.done_known, self.pick, self.paused = {}, {}, True, False, False

    def add(self, code, exp=None, act=None, cls=None, idx=None):
        cls = cls or ('RECORD' if code in RECORD else 'AMBIGUOUS' if code in AMBIGUOUS else 'VIOLATION')
        self.findings.append({'code': code, 'class': cls, 'record_index': idx or self.idx,
                              'expected': exp, 'actual': act})
        if self.first and cls == 'VIOLATION': raise Stop

    def na(self, rule, field):
        self.unaud += [u for u in [{'rule': rule, 'missing_field': field}] if u not in self.unaud]

    def required(self):
        if not self.done_known: return self.na('required', 'amend.done (DONE after an amend)')
        if not self.crit: return self.na('required', 'setup.done.criteria')
        return [c for c, v in self.crit.items() if v.get('required', True) is not False]

    def result(self, ver, rung):  # the standing Check for (ver, rung, epoch), held-out failures applied
        st = self.standing.get((ver, rung, self.epoch))
        return None if st is None else dict(st, **{c: 'fail' for c in self.hofail.get((ver, self.epoch), ())})

    def all_pass(self, ver, rung):  # None: DONE is unknown, so unauditable
        st, req = self.result(ver, rung), self.required()
        if st is not None and req is None: return None
        return st is not None and req is not None and all(st.get(c) == 'pass' for c in req)

    def open_required(self):
        return [g for g, (req, status) in self.subs.items() if req and status == 'open']

    def protected(self):
        mnc = (self.done or {}).get('must_not_change') or []
        ids = {c for c, v in self.crit.items() if v.get('guardrail') or v.get('must_not_change')}
        return ids | {x for x in mnc if isinstance(x, str)} | {c for c, v in self.rs['latest'].items() if v == 'pass'}

    def complete_conds(self):
        if self.setup is None: return self.na('status', 'setup')
        why, ap = [] if self.rung == self.final else ['rung %s != final %s' % (self.rung, self.final)], \
            self.all_pass(self.best, self.final)
        if ap is False: why.append('no all-pass Check on best at the final rung')
        if not any(h['version'] == self.best and h['passed'] and h['epoch'] == self.epoch for h in self.heldout):
            why.append('no held-out pass')           # a held-out result stands only until DONE changes
        return not why, not self.open_required(), '; '.join(why)

    def bud(self):
        b = (self.setup or {}).get('budget')
        return b if isinstance(b, dict) else {}           # a budget logged as prose text is unauditable

    def budget_out(self):
        b, rs = self.bud(), self.rs
        out = num(b.get('rounds')) and rs['cnt'] >= b['rounds']
        if num(b.get('minutes')) and rs['maxdur'] is not None and None not in (self.now, self.start):
            out = out or b['minutes'] - (self.now - self.start) < 2 * rs['maxdur']
        return out

    # ---- obligations: what the previous decision made due for the next decision record
    def pre(self, kind, rec):
        why = rec.get('reason') if kind == 'exit' else None
        if self.osc and why != 'OSCILLATION':
            self.add('OSCILLATION_MISSED', 'exit PARTIAL OSCILLATION', kind, idx=self.osc[0])
        self.osc = None
        k = self.due[0] if self.due else None
        if k is None or (k, why) == ('version', 'OSCILLATION') or (kind == 'check' and k not in ('check', 'version')):
            return                                  # nothing due; a Check never settles a boundary or halt
        if k == 'version':
            self.add('VERSION_MISSING', 'version for round %s' % self.pend['n'], kind)
            self.best, self.best_words = hid(self.pend['var'].get('id')), self.pend['var'].get('words')
        elif k == 'check':
            if kind == 'round': self.add('MISSED_CHECK', 'check (stall count %d)' % self.rs['s'], kind)
        elif k == 'boundary':
            want = 'heldout' if self.rung == self.final else 'rung'
            if kind not in ('exit', want): self.add('BOUNDARY_MISSED', want + ' or exit', kind)
        elif not (kind == 'exit' and (why == k[5:] or (why == 'BUDGET' and self.budget_out()))):
            self.add(k[5:] + '_HALT_MISSED', 'exit PARTIAL ' + k[5:], '%s %s' % (kind, why or ''))
        self.due = self.pend = None

    def post_check(self):  # a required criterion that is not 'pass' (fail or unchecked) fails closed
        st, req = self.result(self.best, self.rung), self.required()
        if None not in (st, req) and all(st.get(c) == 'pass' for c in req): self.due = ('boundary', self.idx)
        elif st and req and self.rs['s'] >= 3: self.due = ('halt:STALL', self.idx)

    def e3_due(self):  # rung E3 needs an amend before its probe or first round
        e, self.e3 = self.e3, None
        if e: self.add('E3_WITHOUT_AMEND', 'an amend before the E3 probe or round', 'none', idx=e)

    # ---- records
    def feed(self, rec, idx):
        self.idx, t = idx, rec.get('t') or rec.get('type')
        if self.exited and t != 'resume':
            self.add('AFTER_EXIT', 'resume', t)
            self.exited = False
        fn = getattr(self, 'r_' + str(t), None)
        try:
            return fn(rec) if fn else self.warnings.append('line %d: unknown record type %r' % (self.idx, t))
        except BAD as e:
            self.na('record', 'line %d: %r' % (idx, e))

    def set_done(self, done):
        self.done = done if isinstance(done, dict) else None
        crit = (self.done or {}).get('criteria')
        self.crit = {c['id']: c for c in crit if isinstance(c, dict) and 'id' in c} if isinstance(crit, list) else {}
        self.final = hid((self.done or {}).get('final_rung') or self.final)   # an amend may move it

    def r_setup(self, s):
        if self.setup is not None:                   # a resume logs `resume`: a second setup is ignored
            return self.add('SETUP_REPEATED' if s.get('done') == self.setup.get('done') else 'UNRECORDED_AMEND',
                            'resume (or an amend)', 'setup')
        self.setup, self.setup_idx, self.start = s, self.idx, minutes(s.get('t0'))
        self.set_done(s.get('done'))
        top, dn = s.get('final_rung'), (self.done or {}).get('final_rung')
        if None not in (top, dn) and top != dn: self.add('FINAL_RUNG_CONFLICT', dn, top)   # DONE's rung applies
        elif top is not None: self.final = hid(top)
        if not self.crit: self.na('setup', 'setup.done.criteria')

    def r_citation(self, c):
        self.cites.append(c)

    def r_substrate(self, s):  # waived needs a later amend; anything but closed or waived is open
        g, st, n = s.get('gap'), s.get('status'), len(self.amends)
        if st == 'open': self.opened[g] = n
        if st == 'closed' and not s.get('evidence'): self.na('substrate', 'substrate.evidence (closure unverified)')
        ok = st == 'closed' or (st == 'waived' and n > self.opened.get(g, 0))
        self.subs[g] = (s.get('required', True) is not False, 'resolved' if ok else 'open')

    def r_amend(self, a):
        d, self.amends, self.e3, self.paused = a.get('done'), self.amends + [a], None, True
        if isinstance(d, dict) and d == self.done: return   # DONE unchanged: every result stands
        self.epoch, self.done_known = self.epoch + 1, isinstance(d, dict)   # no `done`: DONE unknown, unauditable
        if isinstance(d, dict): self.set_done(d)
        if self.due and self.due[0] in ('boundary', 'halt:STALL', 'halt:OVERFIT'): self.due = None

    def r_probe(self, p):
        rung, mode, idn, sd = p.get('rung'), p.get('mode'), p.get('identity'), p.get('seeded')
        if rung is None: return self.na('probe', 'probe.rung')
        self.e3_due()
        pair = sd.get('pair') if isinstance(sd, dict) else None
        if isinstance(idn, list) and isinstance(pair, list) and len(idn) == len(pair) == 2:   # both orders
            miss = any(x != 'best' for x in pair) or sd.get('check') != 'fail'
            exp = 'strict' if miss or any(x != 'tie' for x in idn) else 'normal'
            if mode not in (exp, 'strict'): self.add('PROBE_MODE_WRONG', exp, mode)   # strict by choice fails closed
            mode = 'strict' if 'strict' in (exp, mode) else exp
        else: self.na('probe_mode', 'probe.identity/seeded.pair (two orders each)')
        if self.probes.get(rung) is not None:       # a re-probe never relaxes the first: strict stays strict
            self.add('PROBE_REROLL', 'one probe per rung', rung)
            mode = 'strict' if 'strict' in (mode, self.probes[rung]) else mode
        self.probes[rung] = mode

    def r_rung(self, r):
        if r.get('name') == self.rung: return self.add('RUNG_REPEATED', 'a new rung', self.rung)  # no escalation
        self.pre('rung', r)
        if r.get('name') == 'E3' and not self.amends: self.e3 = self.idx
        self.rung, self.rs['s'], self.paused = hid(r.get('name')), 0, True

    def r_resume(self, r):
        exp = self.rs['n'] + 1
        if self.due and self.due[0] == 'version' and not self.pick:   # unfinished round: rerun, never applied
            exp, self.rs, self.due, self.pend, self.osc = self.pend.get('n'), self.snap or self.rs, None, None, None
        if r.get('at_round') not in (None, exp): self.add('RESUME_MISMATCH', exp, r.get('at_round'))
        self.exited, self.paused = False, True

    def r_variant(self, v):                          # v2 format: keep rules are unauditable
        self.na('keep', 'round.variants[].verdicts (v2 variant record)')
        if v.get('kept') is True:                    # its version record is still audited for lineage
            self.pend, self.due = dict(n=v.get('round'), best=self.best, var={'id': v.get('id')}), ('version', self.idx)

    def r_halt(self, h):                             # v2 format
        self.na('exit', 'exit.status (v2 halt record)')

    def r_version(self, v):
        words, vid = v.get('words'), hid(v.get('id'))
        if self.due and self.due[0] == 'version':
            p = self.pend
            if v.get('parent') != p['best']: self.add('STALE_PARENT', p['best'], v.get('parent'))
            if 'diff' not in v or 'diff' not in p['var']: self.na('kept_text', 'version.diff / variant.diff')
            elif not same_text(diffs(v), diffs(p['var'])): self.add('KEPT_TEXT_MISMATCH', diffs(p['var']), diffs(v))
            words, self.due, self.pend = p['var'].get('words') if words is None else words, None, None
        elif v.get('parent') is not None or self.rs['any_round']:
            self.add('VERSION_WITHOUT_KEEP', 'a kept round before a version', v.get('id'))
        if vid in self.vers:                         # new text under an old id: nothing recorded before stands
            self.epoch = self.add('VERSION_ID_REUSED', 'a new version id', vid) or self.epoch + 1
        self.best, self.best_words, self.pick, self.vers[vid] = vid, words, False, (words, dict(self.rs['latest']))

    # ---- rounds: gates, panel, eligibility, selection, stall
    def verdict(self, v):
        if not isinstance(v, dict) or v.get('overall') not in VALUES: return self.na('keep', 'verdicts[].overall')
        ov, cr, o = v['overall'], dict(v.get('criteria') or {}), v.get('orders')
        if v.get('slot') == 1 and isinstance(o, list) and len(o) >= 2:
            if len(o) > 2: self.add('EXTRA_VERDICT', 'two orders (the first two stand)', len(o))
            o = o[:2]
            vals = [x.get('overall') if isinstance(x, dict) else x for x in o]
            rov, rcr = 'ERROR' if 'ERROR' in vals else vals[0] if vals[0] == vals[1] else 'UNKNOWN', cr
            if all(isinstance(x, dict) and isinstance(x.get('criteria'), dict) for x in o):
                a, b = o[0]['criteria'], o[1]['criteria']
                rcr = {k: a.get(k) if a.get(k) == b.get(k) else 'UNKNOWN' for k in set(a) | set(b)}
            if (rov, rcr) != (ov, cr): self.add('ORDER_MISMAP', [rov, rcr], [ov, cr])
            ov, cr = rov, rcr
        elif v.get('slot') == 1: self.na('order', 'verdicts[slot=1].orders')
        rt = v.get('retries')
        if not num(rt): self.na('retry', 'verdicts[].retries')
        elif rt > 1: ov = self.add('RETRY_EXCEEDED', '<= 1', rt) or 'ERROR'
        return ov, cr, v.get('confidence')

    def gate(self, var):
        """-> 'ok' | 'dropped' | 'rejected' | 'regression' | None (unauditable)."""
        g = var.get('gates')
        if not isinstance(g, dict): return self.na('gates', 'round.variants[].gates')
        gr = g.get('retries') or {}
        if any(num(x) and x > 1 for x in (gr.values() if isinstance(gr, dict) else [gr])):
            return self.add('RETRY_EXCEEDED', '<= 1', gr) or 'dropped'
        if g.get('apply') != 'ok': return 'dropped' if g.get('apply') == 'ERROR' else self.na('gates', 'gates.apply')
        cmds = g.get('commands') if isinstance(g.get('commands'), dict) else {}
        if 'ERROR' in cmds.values(): return 'dropped'
        for c, val in cmds.items():
            if val == 'fail' and self.rs['latest'].get(c) == 'pass': return 'regression'
            if val == 'fail' and c not in self.rs['latest']: self.na('regression', 'check{trigger:setup}.' + c)
        scr = g.get('screen')
        if scr == 'ERROR' or str(scr).startswith('reject'): return 'dropped' if scr == 'ERROR' else 'rejected'
        miss = [c for c, x in self.crit.items() if x.get('kind') == 'command' and cmds.get(c) not in ('pass', 'fail')]
        return self.na('gates', 'gates.screen / gates.commands %s' % miss) if miss or scr is None else 'ok'

    def panel(self, var, strict, prot):
        """Recompute the judged outcome: exp = dropped | rejected | eligible | None (unauditable)."""
        if not isinstance(var.get('verdicts'), list): return self.na('keep', 'round.variants[].verdicts')
        slots = {}
        for v in var['verdicts']:
            s = v.get('slot') if isinstance(v, dict) else None
            if s is None: return self.na('keep', 'verdicts[].slot')
            if s in slots or s not in (1, 2, 3): self.add('EXTRA_VERDICT', 'one verdict per slot 1-3', s)  # 1st stands
            elif (r := self.verdict(v)) is None: return None
            else: slots[s] = r
        val = lambda s: slots[s][0] if s in slots else None  # noqa: E731
        comp = [s for s in slots if slots[s][0] in DONE_VALS]
        pbest = any(slots[s][1].get(c) == 'best' for s in slots for c in prot)   # an UNKNOWN overall still vetoes
        objection = pbest or any(slots[s][0] == 'best' for s in comp)
        early = not strict and val(1) not in (None, 'ERROR') and (
            (val(1) == 'best' and slots[1][2] == 'high') or any(slots[1][1].get(c) == 'best' for c in prot))
        same = not strict and val(1) in ('variant', 'best') and val(1) == val(2)
        req = [1] if early else [1, 2] + ([] if same else [3])
        w, bw, nochange = var.get('words'), self.best_words, var.get('diff') == []   # an empty diff changes nothing
        p = dict(missing=[s for s in req if s not in slots], objection=objection or early,
                 nvar=sum(slots[s][0] == 'variant' for s in comp), nbest=sum(slots[s][0] == 'best' for s in comp),
                 shorter=False if nochange else w < bw if all(num(x) for x in (w, bw)) else None)
        if early: p['exp'] = 'rejected'
        elif any(x[0] == 'ERROR' for x in slots.values()): p['exp'] = 'dropped'   # after one retry: not a rejection
        else:
            improve = p['nvar'] >= (3 if strict else 2) and p['nbest'] == 0 and not pbest and not nochange
            shape = all(val(s) in ('variant', 'tie') for s in (1, 2, 3)) and not any(
                x in ('best', 'UNKNOWN') for s in (1, 2, 3) for x in slots[s][1].values())
            if shape and not improve and p['shorter'] is None: self.na('prune', 'version.words / variant.words')
            elig = True if improve else None if shape and p['shorter'] is None else bool(shape and p['shorter'])
            p['exp'] = {True: 'eligible', False: 'rejected', None: None}[elig]
        return p

    def budget(self, r):
        b, rs = self.bud(), self.rs
        if not b: self.na('budget', 'setup.budget')
        if num(b.get('rounds')) and rs['cnt'] > b['rounds']:
            self.add('BUDGET_OVERRUN', '<= %g rounds' % b['rounds'], rs['cnt'])
        elif 'rounds' in b and not num(b['rounds']): self.na('budget', 'setup.budget.rounds')
        t0, t1 = minutes(r.get('t0')), minutes(r.get('t1'))
        if t0 is None or t1 is None: self.na('budget_time', 'round.t0/t1')
        else:
            if self.now is not None and (self.paused or t0 < self.now):
                self.start += t0 - self.now          # a human wait or a restarted clock is not loop time
            self.start, self.paused = t0 if self.start is None else self.start, False
            m, md = b.get('minutes'), rs['maxdur']
            if num(m) and md is not None and m - (t0 - self.start) < 2 * md:
                self.add('BUDGET_START', '>= %g minutes left' % (2 * md), m - (t0 - self.start))
            rs['maxdur'], self.now = max(md or 0, t1 - t0), t1
        tk, bt = r.get('tokens'), b.get('tokens')
        if num(tk) and rs['tok_all']:
            if num(bt) and rs['maxtok'] is not None and bt - rs['tok'] < 2 * rs['maxtok']:
                self.add('BUDGET_START', '>= %g tokens left' % (2 * rs['maxtok']), bt - rs['tok'])
            rs['tok'], rs['maxtok'] = rs['tok'] + tk, max(rs['maxtok'] or 0, tk)
        else:
            rs['tok_all'] = False
            if bt is not None: self.na('budget_tokens', 'round.tokens')

    def judge_variant(self, var, strict, prot):
        """Recompute one variant's outcome and report differences -> (expected outcome, panel)."""
        g, out = self.gate(var), var.get('outcome')
        if g not in ('ok', None):
            exp = 'dropped' if g == 'dropped' else 'rejected'
            if out == 'kept': self.add('REGRESSION_KEPT' if g == 'regression' else 'GATE_KEPT', exp, out)
            elif out != exp: self.add('ERROR_AS_REJECTION' if exp == 'dropped' else 'REJECTION_AS_ERROR', exp, out)
            elif var.get('verdicts'): self.add('JUDGED_AFTER_GATE', 'no verdicts after a failed gate', out)
            return exp, None
        p = self.panel(var, strict, prot)
        exp, code = (p or {}).get('exp'), None
        if exp and out == 'kept' and exp != 'eligible':
            code = ('KEEP_WITHOUT_SUPPORT' if exp == 'dropped' else 'KEEP_VETOED' if p['objection'] else
                    'STRICT_KEEP' if strict and p['nvar'] >= 2 and p['nbest'] == 0 else
                    'PRUNE_INCOMPLETE' if p['shorter'] else 'KEEP_WITHOUT_SUPPORT')
            self.add(code, exp, out)
        elif exp and out not in ('kept', exp) and (exp != 'eligible' or out == 'dropped'):
            self.add('ERROR_AS_REJECTION' if exp == 'dropped' else 'REJECTION_AS_ERROR',
                     'rejected' if exp == 'eligible' else exp, out)
        if p and p['missing'] and exp != 'dropped' and code != 'PRUNE_INCOMPLETE':
            cls = 'VIOLATION' if out == 'kept' or not p['objection'] else 'RECORD'
            self.add('JUDGE_MISSING', 'slots %s' % p['missing'], 'absent', cls)
        return exp, p

    def judge(self, v, strict, prot):               # a malformed variant is unauditable; the round goes on
        try:
            return self.judge_variant(v, strict, prot)
        except BAD as e:
            return self.na('record', 'line %d: %r' % (self.idx, e)), None

    def ledger(self, res):  # an idea rejected by >=2 judges or twice by the screen needs new evidence (advisory)
        for v, e, p in res:
            k, g = json.dumps(diffs(v), sort_keys=True), v.get('gates')
            sc, ban = self.ideas.get(k, (0, None))
            if diffs(v) and ban == len(self.cites): self.add('REJECTED_IDEA', 'a new citation first', v.get('id'))
            sc += isinstance(g, dict) and str(g.get('screen')).startswith('reject')
            self.ideas[k] = (sc, len(self.cites) if sc >= 2 or (p or {}).get('nbest', 0) >= 2 else ban)

    def r_round(self, r):
        self.e3_due()
        if self.pick and r.get('best') in self.vers:  # after HALT(OSCILLATION) the human picked best
            self.best, (self.best_words, lt), self.due, self.pend = r['best'], self.vers[r['best']], None, None
            self.rs['latest'] = dict(lt)
        self.pre('round', r)
        n, rs, self.pick = r.get('n'), self.rs, False
        if n != rs['n'] + 1: self.add('ROUND_SEQUENCE', rs['n'] + 1, n)
        self.snap = copy.deepcopy(rs)
        if self.rung not in self.probes:             # reported once; the mode stays null (normal)
            self.probes[self.rung] = self.add('PROBE_MISSING', 'probe{rung:%s} before this round' % self.rung, 'none')
        if r.get('best') != self.best: self.add('STALE_PARENT', self.best, r.get('best'))
        rs['cnt'] += 1                               # the budget counts round records, never the logged n
        self.budget(r)
        strict, prot = self.probes.get(self.rung) == 'strict', self.protected()
        vs = [v for v in r['variants'] if isinstance(v, dict)] if isinstance(r.get('variants'), list) else []
        if len(vs) > 2:                              # proposals beyond 2: keeping one of them is a VIOLATION
            self.add('VARIANT_COUNT', '<= 2 variants', len(vs), 'VIOLATION' if any(
                v.get('outcome') == 'kept' for v in vs[2:]) else 'RECORD')
        res = [(v,) + self.judge(v, strict, prot) for v in vs]
        self.ledger(res)
        elig = [(i, v, p) for i, (v, e, p) in enumerate(res) if e == 'eligible']
        top = [x for x in elig if x[2]['nvar'] == max(y[2]['nvar'] for y in elig)]
        if len(top) > 1 and not all(num(x[1].get('words')) for x in top): sel = self.na('selection', 'variants[].words')
        else: sel = min(top, key=lambda x: (x[1]['words'] if len(top) > 1 else 0, x[0]))[1] if top else None
        kept = [v for v in vs if v.get('outcome') == 'kept']
        if len(kept) > 1: self.add('MULTI_KEEP', '<= 1 kept', [v.get('id') for v in kept])
        elif kept and sel is not None and kept[0] is not sel and any(v is kept[0] and e == 'eligible'
                                                                     for v, e, _ in res):
            self.add('WRONG_SELECTION', sel.get('id'), kept[0].get('id'))
        elif not kept and elig: self.add('MISSED_KEEP', sel.get('id') if sel else 'an eligible variant', None)
        ids = [v.get('id') for v in kept]
        if (r.get('kept') is None) != (not ids) or (ids and r.get('kept') not in ids):
            self.add('KEPT_ID_MISMATCH', ids, r.get('kept'))
        self.last_eval = {'required_keep': None if sel is None else sel.get('id'), 'outcomes': {
            v.get('id'): 'kept' if v is sel else e if e in ('dropped', 'rejected') else e and 'rejected'
            for v, e, _ in res}}
        k = next((v for v in kept if v.get('id') == r.get('kept')), kept[0] if kept else None)
        rs['n'], rs['any_round'] = n if isinstance(n, int) else rs['n'] + 1, True
        if k is not None:                            # the log's keep is followed, violation or not
            g = k.get('gates') if isinstance(k.get('gates'), dict) else {}
            cm = g.get('commands') if isinstance(g.get('commands'), dict) else {}
            rs['s'] = rs['e'] = 0                    # a command not rerun on the new best is no longer known
            rs['latest'] = {c: x for c, x in rs['latest'].items() if self.crit.get(c, {}).get('kind') != 'command'}
            rs['latest'].update({c: x for c, x in cm.items() if x in ('pass', 'fail')})
            self.pend, self.due = {'n': n, 'best': r.get('best'), 'var': k}, ('version', self.idx)
            self.keep_checks(k)
        elif vs and all((e or v.get('outcome')) == 'dropped' for v, e, _ in res):
            rs['e'] += 1                             # all-ERROR round: not a stall
            self.due = ('halt:ERROR', self.idx) if rs['e'] == 2 else self.due
        else:
            rs['s'], rs['e'] = rs['s'] + 1, 0
            if rs['s'] >= 3 and self.result(self.best, self.rung) is None: self.due = ('check', self.idx)
            elif rs['s'] >= 3: self.post_check()     # the standing Check is reused, never re-rolled

    def keep_checks(self, k):
        nf = lambda f: os.path.normpath(str(f).replace('\\', '/')).casefold()  # noqa: E731 (case-insensitive FS)
        cf, hist, ratio = (self.setup or {}).get('check_files'), self.rs['hist'], 0.0
        cf, ds = {nf(f) for f in cf} if isinstance(cf, list) else set(), [d for d in diffs(k) if isinstance(d, dict)]
        if len({hid(d.get('section')) for d in ds}) > 1:   # advisory: an approved restructure is not recorded
            self.add('MULTI_SECTION', 'one section', sorted(str(d.get('section')) for d in ds))
        for d in ds:
            if d.get('file') and nf(d['file']) in cf: self.add('CHECK_FILE_EDIT', 'no edit', d['file'])
            sec, new, cur = hid(d.get('section')), *(' '.join(str(d.get(x) or '').split()) for x in ('new', 'old'))
            for old in hist.get(sec, []):            # a restore moves the text back toward an earlier best's
                r = difflib.SequenceMatcher(None, new, old).ratio()
                if old != cur and r > difflib.SequenceMatcher(None, cur, old).ratio(): ratio = max(ratio, r)
            hist.setdefault(sec, []).extend(x for x in (cur, new) if x not in hist.get(sec, []))
        self.rs['ratio'] = ratio
        if ratio >= 0.9: self.osc = (self.idx, ratio)  # advisory: the prose's "(nearly)" is a judgment

    # ---- Check, held-out, exit
    def r_check(self, c):
        self.pre('check', c)
        if not isinstance(c.get('results'), dict) or 'version' not in c: return self.na('check', 'check.results')
        ver, rung = c['version'], c.get('rung', self.rung)
        base = not self.rs['any_round'] and ver == self.best          # v0's baseline run, before any round
        setup = c.get('trigger', 'setup' if base else None) == 'setup' and base
        if c.get('trigger') == 'setup' and not base: self.add('SETUP_CHECK_LATE', 'v0 before round 1', ver)
        key = (ver, rung, self.epoch)
        if not setup and (ver != self.best or rung != self.rung):
            return self.add('CHECK_NOT_BEST', [self.best, self.rung], [ver, rung])
        if not setup and key in self.standing:
            return self.add('RECHECK_UNCHANGED', 'the first Check on %s/%s stands' % (ver, rung), 'another Check')
        strict, vals, cited = self.probes.get(rung) == 'strict', {}, any('criterion' in x for x in self.cites)
        vc = [x for x in self.cites if x.get('status') == 'verified']
        for cid, r in c['results'].items():
            r = r if isinstance(r, dict) else {'value': r}
            kind, val = self.crit.get(cid, {}).get('kind') or r.get('kind'), r.get('value')
            if kind == 'judges' and isinstance(r.get('votes'), list):
                vt = r['votes']                      # 3 judges; any extra vote counts against a pass
                if len(vt) > 3: self.add('EXTRA_VERDICT', '3 votes', len(vt))
                ok = sum(x == 'pass' for x in vt) >= (max(3, len(vt)) if strict else max(2, len(vt) // 2 + 1))
                if (val == 'pass') != ok: self.add('CHECK_MISCOUNT', 'pass' if ok else 'not pass', val)
                val = 'pass' if ok else val if val in ('fail', 'unchecked') else 'fail'
            elif kind == 'judges': self.na('check_judges', 'check.results[].votes')
            elif kind == 'source' and val == 'pass' and not any(x.get('criterion') == cid for x in vc):
                if not cited or any('criterion' not in x for x in vc): self.na('check_source', 'citation.criterion')
                else: val = self.add('CHECK_MISCOUNT', 'a verified citation for ' + cid, 'none') or 'fail'
            vals[cid] = val
        self.rs['latest'].update({k: v for k, v in vals.items() if v in ('pass', 'fail')})
        if not setup:                                # the setup Check is v0's baseline, not a Check
            self.standing[key] = vals
            self.post_check()

    def r_heldout(self, h):
        self.pre('heldout', h)
        self.paused = True                           # the human runs the held-out judges
        if 'version' not in h or not isinstance(h.get('pass'), dict): return self.na('heldout', 'heldout.version')
        if self.open_required(): self.add('OPEN_AT_HELDOUT', 'exit PARTIAL OPEN first', self.open_required())
        n, ver, prev = len(self.heldout) + 1, h['version'], self.heldout
        passed = all(h['pass'].get(c, True) is True for c in (self.required() or list(h['pass'])))  # non-bool fails
        reroll = n > 2 or h.get('attempt') != n or (n == 1 and h.get('set') == 'spare') or (n == 2 and (
            prev[0]['passed'] or ver == prev[0]['version'] or h.get('set') == 'primary'))
        if reroll: self.add('HELDOUT_REROLL', 'attempt %d, primary first, spares on a changed best after a failed '
                            'attempt 1' % n, [h.get('attempt'), ver])      # a rerolled pass never counts
        elif ver != self.best or self.rung != self.final or self.all_pass(ver, self.final) is False:
            self.add('HELDOUT_UNCHECKED', 'best with an all-pass Check at ' + self.final, [ver, self.rung])
        self.heldout.append({'attempt': h.get('attempt'), 'version': ver, 'passed': passed and not reroll,
                             'epoch': self.epoch})
        fails = {c for c, ok in h['pass'].items() if ok is not True}
        self.hofail.setdefault((ver, self.epoch), set()).update(fails)
        if ver == self.best: self.rs['latest'].update({c: 'fail' for c in fails})
        if n == 2 and not passed: self.due = ('halt:OVERFIT', self.idx)

    def r_exit(self, x):
        self.pre('exit', x)
        st, why, rs, conds = x.get('status'), x.get('reason'), self.rs, self.complete_conds()
        if st == 'COMPLETE' and conds:
            if not conds[0]: self.add('FALSE_COMPLETE', 'PARTIAL', conds[2])
            if not conds[1]: self.add('OPEN_AT_COMPLETE', 'exit PARTIAL OPEN', self.open_required())
        elif st == 'PARTIAL':
            if conds and conds[0] and conds[1]: self.add('MISLABEL', 'COMPLETE', 'PARTIAL')
            res, req = self.result(self.best, self.rung), self.required()
            if why == 'STALL' and req is not None and not (
                    rs['s'] >= 3 and res and any(res.get(c) != 'pass' for c in req)):
                self.add('STALL_MISCOUNT', 's >= 3 and a required non-pass in the standing Check', 's=%d' % rs['s'])
            elif why == 'ERROR' and rs['e'] < 2: self.add('EXIT_UNSUPPORTED', 'two all-ERROR rounds', 'e=%d' % rs['e'])
            elif why == 'OVERFIT' and not (len(self.heldout) == 2 and not self.heldout[1]['passed']):
                self.add('EXIT_UNSUPPORTED', 'a failed held-out attempt 2', len(self.heldout))
            elif why == 'BUDGET' and res is None:
                self.add('UNCHECKED_BUDGET_EXIT', 'a standing Check on %s/%s' % (self.best, self.rung), 'none')
            elif why == 'OSCILLATION' and rs['ratio'] < 0.5: self.add('OSCILLATION_UNSUPPORTED', 0.5, rs['ratio'])
        elif st != 'COMPLETE': self.na('exit', 'exit.status')
        self.exited, self.exit_status, self.pick, self.paused = True, st, why == 'OSCILLATION', True

    # ---- options and summary
    def check_done(self, path):
        cur = (self.setup or {}).get('done')
        for a in self.amends:
            if not isinstance(a.get('done'), dict): return self.na('done_drift', 'amend.done')
            cur = a['done']
        with open(path, encoding='utf-8') as f:
            if json.load(f) != cur:
                self.add('UNRECORDED_AMEND', 'DONE = setup.done + amends', path, idx=self.setup_idx)

    def check_target(self, d):
        files, hs = (self.setup or {}).get('check_files'), (self.setup or {}).get('check_hashes')
        if not isinstance(files, list) or not files or not isinstance(hs, dict):
            return self.na('check_hashes', 'setup.check_hashes')
        for f in (x for x in files if isinstance(x, str) or self.na('check_hashes', 'setup.check_files[] (a path)')):
            p = os.path.join(d, f)
            got = (sha(p), sha(p, True)) if os.path.isfile(p) else ()
            if not hs.get(f): self.na('check_hashes', 'setup.check_hashes.' + f)
            elif hs[f] not in got:                   # raw or LF-normalized digest (CRLF checkouts)
                self.add('CHECK_FILE_DRIFT', hs[f], got[0] if got else 'missing', idx=self.setup_idx)

    def next_due(self):
        k = self.due[0] if self.due else None
        if self.exited: return None
        if k not in (None, 'version'):
            return k if k != 'boundary' else 'boundary' if self.rung != self.final else \
                'halt:OPEN' if self.open_required() else 'heldout'
        c = None if self.osc or not self.setup else self.complete_conds()
        if self.osc or (c and c[0] and c[1]): return 'halt:OSCILLATION' if self.osc else 'exit'
        if self.budget_out(): return 'halt:BUDGET' if self.result(self.best, self.rung) is not None else 'check'
        return 'round'

    def state(self):
        rs, c = self.rs, (self.complete_conds() if self.exited and self.setup else None)
        status = 'ACTIVE' if not self.exited else 'COMPLETE' if c and c[0] and c[1] else \
            'PARTIAL' if c or self.exit_status == 'PARTIAL' else 'UNKNOWN'
        return {'best': self.best, 'rung': self.rung, 'final_rung': self.final, 'probe_modes': self.probes,
                'stall': rs['s'], 'error_streak': rs['e'], 'rounds': rs['cnt'],
                'minutes': None if self.now is None or self.start is None else self.now - self.start,
                'tokens': rs['tok'] if rs['tok_all'] and rs['any_round'] else None,
                'standing_checks': [{'version': k[0], 'rung': k[1], 'epoch': k[2]} for k in self.standing],
                'open_required_gaps': self.open_required(), 'heldout': self.heldout,
                'amends': len(self.amends), 'next_due': self.next_due(), 'status': status}

def audit(path, done=None, target=None, first=False, pending=None, text=None):
    """-> (output dict, exit code). With pending: the Stage-1 answer key for a not-yet-logged round."""
    (recs, torn, aside, integ), a = load(path, text), Audit(first)
    try:
        for i, rec in recs: a.feed(rec, i)
        for fn, arg in ((a.check_done, done), (a.check_target, target)):
            try:
                if arg: fn(arg)
            except BAD as e:                         # a malformed option input is unauditable, not a crash
                a.na('option', repr(e))
    except Stop:
        pass
    if a.setup is None: a.na('setup', 'setup record (v2 or partial archive)')
    ok = integ is None and not any(f['class'] == 'VIOLATION' for f in a.findings)
    out = {'ok': ok, 'state': a.state(), 'violations': a.findings, 'unauditable': a.unaud,
           'warnings': a.warnings, 'torn_tail': torn is not None, 'torn_line': torn, 'set_aside': aside,
           'integrity': None if integ is None else {'line': integ, 'error': 'unparsable interior line'}}
    if not pending: return out, 2 if integ is not None else 0 if ok else 1
    with open(pending, encoding='utf-8') as f:
        pr = json.load(f)
    if not isinstance(pr, dict): return {'ok': False, 'error': 'usage: --pending holds one round object'}, 2
    def replay(rnd):  # noqa: E306                                 # appended to a copy; its findings are discarded
        b = copy.deepcopy(a)
        b.first, b.findings, b.exited, b.last_eval = False, [], False, None
        b.feed(dict(rnd, t='round'), (recs[-1][0] if recs else 0) + 1)
        return b
    ev, fixed = replay(pr).last_eval, copy.deepcopy(pr)
    if ev is None: return {'ok': False, 'error': 'usage: the --pending round is unauditable'}, 2
    for v in fixed.get('variants') if isinstance(fixed.get('variants'), list) else []:
        if isinstance(v, dict): v['outcome'] = ev['outcomes'].get(hid(v.get('id')))
    fixed['kept'] = ev['required_keep']
    return dict(ev, next_due=replay(fixed).next_due(), archive_ok=ok), 0

def selftest(d):
    """Every fixture must match expected.json exactly (codes and classes, no extras)."""
    with open(os.path.join(d, 'expected.json'), encoding='utf-8') as f:
        cases = json.load(f)['cases']
    fx, named = os.path.join(d, 'fixtures'), {c['fixture'] for c in cases}
    fails = [{'fixture': n, 'error': 'no expected case'} for n in sorted(os.listdir(fx))
             if n.endswith('.jsonl') and n not in named]
    for c in cases:
        a = c.get('args', {})
        opt = lambda k: os.path.join(fx, a[k]) if a.get(k) else None  # noqa: E731
        path, text = os.path.join(fx, c['fixture']), None
        try:
            if c.get('strip_final_newline'):         # a torn-before-newline variant, derived in memory
                with open(path, encoding='utf-8') as f:
                    text = f.read().rstrip('\r\n')
            out, code = audit(path, opt('done'), opt('target'), bool(a.get('first')),
                              os.path.join(fx, c['pending']) if c.get('pending') else None, text)
        except Exception as e:                       # a crash is a failed case, never a pass
            fails.append({'fixture': c['fixture'], 'error': repr(e)})
            continue
        if c.get('pending'):
            want = {k: c.get(k) for k in ('required_keep', 'outcomes', 'next_due')}
            got = dict({k: out.get(k) for k in want}, exit=code)
            want['exit'] = c.get('exit', 0)
        else:
            bad = int(any(x[1] == 'VIOLATION' for x in c['codes']))
            want = {'codes': sorted(c['codes']), 'exit': c.get('exit', bad), 'state': c.get('state', {}),
                    'unaud': sorted(c.get('unauditable_includes', []))}
            got = {'codes': sorted([f['code'], f['class']] for f in out['violations']), 'exit': code,
                   'state': {k: out['state'].get(k) for k in want['state']},
                   'unaud': sorted({u['rule'] for u in out['unauditable']} & set(want['unaud']))}
            for k in ('ok', 'torn_tail', 'set_aside', 'integrity', 'record_indexes'):
                if k in c:
                    want[k], got[k] = c[k], (out['integrity'] or {}).get('line') if k == 'integrity' else \
                        sorted(f['record_index'] for f in out['violations']) if k == 'record_indexes' else out[k]
        if want != got:
            fails.append({'fixture': c['fixture'], 'invariant': c.get('invariant'), 'want': want, 'got': got})
    return {'ok': not fails, 'cases': len(cases), 'failed': fails}

def main(argv):
    op, rest = (argv[0], argv[1:]) if argv else (None, [])
    files, opts, pos, it = [x for x in rest if x != '--lf'], {}, [], iter(rest)
    for x in it:
        if x in ('--done', '--target', '--pending'): opts[x[2:]] = next(it, None)
        elif x != '--first': pos.append(x)
    try:
        if op == 'hash' and files:
            for p in files: print('%s  %s' % (sha(p, '--lf' in rest), p))
            return 0
        if op == 'selftest':
            root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            res = selftest(rest[0] if rest else os.path.join(root, 'tests', 'checker'))
            print(json.dumps(res, indent=1))
            return 0 if res['ok'] else 1
        if op == 'audit' and len(pos) == 1 and None not in opts.values():
            out, code = audit(pos[0], opts.get('done'), opts.get('target'), '--first' in rest, opts.get('pending'))
            print(json.dumps(out, indent=1))
            return code
    except Exception as e:                           # never exit 1 on a crash: 1 means violations
        print(json.dumps({'ok': False, 'error': repr(e)}))
        return 2
    print(__doc__, file=sys.stderr)
    return 2

if __name__ == '__main__': sys.exit(main(sys.argv[1:]))
