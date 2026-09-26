#!/usr/bin/env python3
"""rqgm_check.py - optional, read-only auditor for an RQGM v3 MEMORY (archive.jsonl).

  audit MEMORY [--done DONE.json] [--target DIR] [--pending ROUND.json] [--first]
  selftest [DIR]        (DIR holds expected.json and fixtures/; default <repo>/tests/checker)
  hash FILE... [--lf]   (the only source of setup.check_hashes)

It recomputes the keeps, drops, Check values, halts and exits its records allow and reports findings
{code, class, record_index (file line), expected, actual}; it never decides. Classes: VIOLATION (a
decision differs), RECORD (inconsistent, no decision changed), AMBIGUOUS (advisory). Record types and
enumerated values match case-insensitively; a decision value outside its vocabulary is never a pass,
support or keep. Fail closed on a v3 archive (its first setup record, wherever logged, has loop
"v3..."): a field SKILL.md's Memory schema lists (no "?") that a decision needs, when absent or empty
(budget.rounds: not a finite number; budget.minutes: neither that nor null, unreported; round t0/t1
only while minutes is a number), is RECORD_MISSING (a VIOLATION) and the decision is not credited (a
rung with no probe is strict; with no judges criterion in DONE no probe is due and every rung is
strict; a prune whose length cannot be compared, as with no version v0, is not kept). check.models
(absent, or empty beside a judges result) and a command criterion's files are RECORD_MISSING too.
Otherwise (v2 or partial archives, a malformed label the checker recounts itself such as retries or
attempt, a link the prose never logs) a rule whose inputs are missing is listed as unauditable.
Unauditable from any record: held-out secrecy, role separation, relay authenticity, the
cosmetic-differences judgment (a restore at difflib ratio >= 0.9 is advisory; an exact undo is a
VIOLATION), section boundaries, judge 1's logged confidence, a check editing files, and a Screen or
Verifier verdict relabelled ERROR. A closed gap stays required until a kept diff removes an [OPEN]
(advisory: markers are counted in aggregate). Rounds are counted from round records, never logged
numbers; loop time excludes waits for the human (rung, amend, approve, held-out, exit, resume);
naive ISO times are UTC. Python >= 3.9 stdlib only; no network, model calls or clock; never writes
a file. Exit: 0 no VIOLATION, 1 violations, 2 integrity (an interior line unparsable or repeating a
key, or no line whose "t" names a record) or usage error.
"""
import copy, difflib, hashlib, json, os, sys  # noqa: E401
from datetime import datetime, timezone

RECORD = {'ORDER_MISMAP', 'KEPT_ID_MISMATCH', 'VERSION_MISSING', 'ROUND_SEQUENCE', 'MISLABEL', 'JUDGED_AFTER_GATE',
          'RESUME_MISMATCH', 'AFTER_EXIT', 'EXTRA_VERDICT', 'PROBE_REROLL', 'RUNG_REPEATED', 'SETUP_CHECK_LATE',
          'SETUP_REPEATED', 'VERSION_ID_REUSED', 'FINAL_RUNG_CONFLICT', 'SETUP_LATE'}
AMBIGUOUS = {'OSCILLATION_MISSED', 'OSCILLATION_UNSUPPORTED', 'REJECTED_IDEA'}
DONE_VALS = ('variant', 'best', 'tie')          # "completed" judge values
VALUES = DONE_VALS + ('UNKNOWN', 'ERROR')
RUNGS = {'E1': 1, 'E2': 2, 'E3': 3}             # a rung record is an escalation only to a later rung
CANON = dict({w.casefold(): w for w in VALUES + tuple(RUNGS) + tuple(
    'pass fail unchecked ok low med high primary spare COMPLETE PARTIAL command source judges open closed waived '
    'kept rejected dropped strict normal setup STALL OVERFIT BUDGET OSCILLATION HUMAN restructure pick verified'
    .split())}, spares='spare')
BAD = (TypeError, AttributeError, ValueError, KeyError, OverflowError, RecursionError)  # malformed: unauditable
EPOCH = datetime(1970, 1, 1, tzinfo=timezone.utc)
hid = lambda x: x if isinstance(x, (str, int, float, type(None))) else json.dumps(x)  # noqa: E731 (ids as keys)
num = lambda x: type(x) in (int, float) and abs(x) < 1e300  # noqa: E731 (finite: never bool, NaN or a huge int)
canon = lambda x: CANON.get(x.strip().casefold(), x) if isinstance(x, str) else x  # noqa: E731
nf = lambda f: os.path.normpath(str(f).replace('\\', '/')).casefold()  # noqa: E731 (paths, case-insensitive FS)
worse = lambda x: x is not None and x not in ('variant', 'tie')  # noqa: E731 (best, UNKNOWN or unreadable: a veto)

class Stop(Exception):  """--first: raised at the first VIOLATION, so nothing later is evaluated."""

def rtype(r):  # a record's type, case-insensitive ({"t":"Round"} is a round)
    t = r.get('t') or r.get('type')
    return t.casefold() if isinstance(t, str) else None
def minutes(x):  # a number, or an ISO time (naive = UTC, never the local clock) -> minutes; else None
    if num(x): return float(x)
    try:
        d = datetime.fromisoformat(x.replace('Z', '+00:00'))
        return ((d if d.tzinfo else d.replace(tzinfo=timezone.utc)) - EPOCH).total_seconds() / 60.0
    except (AttributeError, TypeError, ValueError, OverflowError): return None

def clip(x, d=48):  # echoed values are cut to a finite depth, so the report always serializes
    if isinstance(x, dict): return {str(k): clip(v, d - 1) for k, v in x.items()} if d else '{...}'
    return ([clip(v, d - 1) for v in x] if d else '[...]') if isinstance(x, (list, tuple)) else x
def cres(x):  # a gate result, case-insensitive: 'ok' or exit status 0 passes, another exit status fails
    x = canon(x)
    return ('fail' if x else 'pass') if type(x) is int else 'pass' if x == 'ok' else x
def diffs(var):  # a list of edits, one edit, or a unified-diff string (one opaque edit)
    d = (var or {}).get('diff')
    return d if isinstance(d, list) else [d] if isinstance(d, dict) or (isinstance(d, str) and d) else []

def same_text(a, b):  # the judged text is section, old and new (and file when both name one)
    ks = lambda x, y: ('section', 'old', 'new') + (('file',) if 'file' in x and 'file' in y else ())  # noqa: E731
    return len(a) == len(b) and all(all(x.get(k) == y.get(k) for k in ks(x, y)) if isinstance(x, dict) and
                                    isinstance(y, dict) else x == y for x, y in zip(a, b))

def dfiles(ds):  # the files edits name: a `file` key, or a unified diff's ---/+++ headers
    out = {nf(d['file']) for d in ds if isinstance(d, dict) and d.get('file')}
    for ln in (ln for d in ds if isinstance(d, str) for ln in d.splitlines() if ln[:4] in ('--- ', '+++ ')):
        p = ln[4:].split('\t')[0].strip()
        if p and p != '/dev/null': out.add(nf(p[2:] if p[:2] in ('a/', 'b/') else p))
    return out
def opens(d):  # [OPEN] markers an edit adds (negative: removes)
    if isinstance(d, dict): return str(d.get('new') or '').count('[OPEN') - str(d.get('old') or '').count('[OPEN')
    return sum((ln[:1] == '+') - (ln[:1] == '-') for ln in str(d).splitlines() if '[OPEN' in ln and ln[:3] not in
               ('+++', '---'))

def crits(done):  # DONE.criteria, a list of {id,...} or a map {id: {...}} -> {id: criterion}
    cr = done.get('criteria') if isinstance(done, dict) else None
    if isinstance(cr, dict): return {hid(k): dict(v, id=k) for k, v in cr.items() if isinstance(v, dict)}
    return {hid(c['id']): c for c in cr if isinstance(c, dict) and 'id' in c} if isinstance(cr, list) else {}
def dkey(d):  # DONE up to criteria order: the same criteria listed in another order change nothing
    return json.dumps(dict(d, criteria=crits(d)), sort_keys=True) if isinstance(d, dict) else d

def sha(path, lf=False):
    with open(path, 'rb') as f: b = f.read()
    return hashlib.sha256(b.replace(b'\r\n', b'\n') if lf else b).hexdigest()

def _obj(pairs):  # a repeated key makes a line ambiguous: which value counts depends on the parser
    if len({k for k, _ in pairs}) < len(pairs): raise ValueError('duplicate key')
    return dict(pairs)
def parse(s):
    try: r = json.loads(s, object_pairs_hook=_obj)
    except (ValueError, RecursionError): return None   # RecursionError: deeply nested garbage
    return r if isinstance(r, dict) else None

def load(path, text=None):
    """-> (records [(line, dict)], torn_line, set_aside_lines, integrity_line)."""
    if text is None:
        with open(path, 'rb') as f: text = f.read().decode('utf-8', 'replace')
    lines = (text[1:] if text[:1] == '\ufeff' else text).split('\n')   # a UTF-8 BOM is not content
    full = [i for i, s in enumerate(lines, 1) if s.strip()]
    recs, aside = [], []
    for k, i in enumerate(full):
        rec = parse(lines[i - 1])
        if k == len(full) - 1 and (rec is None or i == len(lines)):
            return recs, i, aside, None          # torn tail (unparsable or newline-less): excluded
        if rec is None:
            if (nxt := parse(lines[full[k + 1] - 1])) and rtype(nxt) == 'resume':
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
        # Round-derived state; restored from a snapshot when an unfinished round is rerun on resume. appr: unused
        self.rs = dict(s=0, e=0, n=0, cnt=0, maxdur=None, tok=0.0, tok_all=True, maxtok=None, latest={},  # restructure
                       hist={}, ratio=0.0, any_round=False, marks=0, appr=[], rm=0)   # approvals; rm: [OPEN]s removed
        self.snap = self.due = self.pend = self.osc = self.start = self.now = self.last_eval = self.e3 = None
        self.epoch, self.amends, self.standing, self.hofail, self.heldout = 0, [], {}, {}, []
        self.subs, self.opened, self.cites, self.exited, self.exit_status, self.why = {}, {}, [], False, None, None
        self.vers, self.ideas, self.done_known, self.pick, self.paused, self.waive = {}, {}, True, False, False, None
        self.v3, self.obj, self.nrec, self.ended, self.budg = False, False, 0, False, None   # v3: fail closed; obj:
        # an amend added a criterion; ended: an exit OVERFIT ended the archive; budg: the live BUDGET (bud());
        # waive: after exit OPEN and a resume, the gaps waived since ("OPEN with all gaps waived -> Stop")

    def add(self, code, exp=None, act=None, cls=None, idx=None):
        cls = cls or ('RECORD' if code in RECORD else 'AMBIGUOUS' if code in AMBIGUOUS else 'VIOLATION')
        self.findings.append({'code': code, 'class': cls, 'record_index': idx or self.idx,
                              'expected': exp, 'actual': act})
        if self.first and cls == 'VIOLATION': raise Stop

    def na(self, rule, field):
        self.unaud += [u for u in [{'rule': rule, 'missing_field': field}] if u not in self.unaud]
    def miss(self, rule, field, act=None, absent=True):  # v3 and absent: RECORD_MISSING; else unauditable
        return self.add('RECORD_MISSING', field, act) if self.v3 and absent else self.na(rule, field)
    def kind(self, c, r=None):  # a criterion's kind (DONE's, else the result's); None when unknown
        k = canon(self.crit.get(c, {}).get('kind') or (r or {}).get('kind'))
        return k if k in ('command', 'source', 'judges') else None

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
    def open_required(self, hard=False):  # "A required [OPEN] (in best, unwaived, criterion not optional)"
        req = lambda c: self.crit.get(c, {}).get('required', True) is not False  # noqa: E731  (none named: required)
        return [g for g, (c, st) in self.subs.items() if req(c) and st in ('open',) + ('closed',) * (not hard)] + \
            ['[OPEN] in best, no substrate record'] * (self.rs['marks'] > len(self.subs))   # an [OPEN] kept, unlogged
    def ocls(self):  # only a closed gap not yet written in (no kept diff removed an [OPEN] since): advisory
        return None if self.open_required(True) else 'AMBIGUOUS'
    def spent(self):  # held-out attempt 1 failed on best: "Spares run only on a changed best passing Check"
        return len(self.heldout) == 1 and not self.heldout[0]['passed'] and self.heldout[0]['version'] == self.best

    # "A veto: a protected item ... rated worse, UNKNOWN or not at all"; not at all: a completed v3 verdict leaves it
    # unrated (judges rate "each criterion and must_not_change id")
    def veto(self, ov, cr, prot):
        return any(worse(x := cr.get(c)) or x is None and self.v3 and ov in DONE_VALS for c in prot)
    def protected(self):
        mnc = [x.get('id') if isinstance(x, dict) else x for x in (self.done or {}).get('must_not_change') or []]
        ids = {c for c, v in self.crit.items() if v.get('guardrail') or v.get('must_not_change')}
        return ids | {x for x in mnc if isinstance(x, str)} | {c for c, v in self.rs['latest'].items() if v == 'pass'}

    def complete_conds(self):
        if self.setup is None: return self.na('status', 'setup')
        why, ap = [] if self.rung == self.final else ['rung %s != final %s' % (self.rung, self.final)], \
            self.all_pass(self.best, self.final)
        if ap is False or (ap is None and self.v3):   # v3: an unknown DONE is not credited
            why.append('no all-pass Check on best at the final rung')
        if not any(h['version'] == self.best and h['passed'] and h['epoch'] == self.epoch for h in self.heldout):
            why.append('no held-out pass')           # a held-out result stands only until DONE changes
        return not why, not self.open_required(), '; '.join(why)

    def bud(self):  # the live budget ("only amend{budget} changes it"); one logged as prose text is unauditable
        return b if isinstance(b := self.budg, dict) else {}
    def bcheck(self, b, where):  # rounds: a finite number; minutes: one, or null when the host reports none
        if not (type(b) is dict and num(b.get('rounds')) and (num(b.get('minutes')) or b.get('minutes', 0) is None)):
            self.miss('budget', where + '.budget{rounds,minutes} (finite numbers; minutes null if unreported)', b)
        return b
    def budget_out(self):
        b, rs = self.bud(), self.rs
        out = num(b.get('rounds')) and rs['cnt'] >= b['rounds']
        if num(b.get('minutes')) and rs['maxdur'] is not None and None not in (self.now, self.start):
            out = out or b['minutes'] - (self.now - self.start) < 2 * rs['maxdur']
        return out

    # ---- obligations: what the previous decision made due for the next decision record
    def pre(self, kind, rec):
        why = canon(rec.get('reason')) if kind == 'exit' else None
        if self.osc and why != 'OSCILLATION':        # an exact undo needs no judgment: a VIOLATION
            self.add('OSCILLATION_MISSED', 'exit PARTIAL OSCILLATION', kind, self.osc[2] and 'VIOLATION', self.osc[0])
        self.osc = None                              # "HALT(OSCILLATION) after its version": no exemption for it
        if self.pick and kind != 'exit':             # "after HALT(OSCILLATION), pick best among logged versions"
            self.pick = self.miss('pick', 'approve{what:pick,version} after HALT(OSCILLATION)', kind)
        if self.waive and not self.open_required() and kind not in ('heldout', 'exit', 'check'):
            self.add('STOP_MISSED', 'Stop (heldout or exit): "OPEN with all gaps waived -> Stop"', kind)
        self.waive = self.waive if kind == 'check' else None   # else "the next round"
        k = self.due[0] if self.due else None
        if k is None or (kind == 'check' and k not in ('check', 'version')):
            return                                  # nothing due; a Check never settles a boundary or halt
        if k == 'version':
            self.add('VERSION_MISSING', 'version for round %s' % self.pend['n'], kind)
            self.best, self.best_words = hid(self.pend['var'].get('id')), self.pend['var'].get('words')
        elif k == 'check':
            if kind == 'round': self.add('MISSED_CHECK', 'check (stall count %d)' % self.rs['s'], kind)
        elif k == 'boundary':                        # after a failed attempt 1 on best: rounds (a heldout: REROLL)
            want = 'rung' if self.rung != self.final else 'round' if self.spent() else 'heldout'
            if kind not in ('exit', want, 'heldout' if want == 'round' else want):
                self.add('BOUNDARY_MISSED', want + ' or exit', kind)
        elif not (kind == 'exit' and (why == k[5:] or (why == 'BUDGET' and self.budget_out()))):
            self.add(k[5:] + '_HALT_MISSED', 'exit PARTIAL ' + k[5:], '%s %s' % (kind, why or ''))
        self.due = self.pend = None

    def post_check(self):  # a required criterion that is not 'pass' (fail or unchecked) fails closed
        st, req = self.result(self.best, self.rung), self.required()
        if None not in (st, req) and all(st.get(c) == 'pass' for c in req): self.due = ('boundary', self.idx)
        elif st and req and self.rs['s'] >= 3: self.due = ('halt:STALL', self.idx)
    def e3_due(self):  # rung E3 needs an amend adding a criterion (the second objective) before its probe or round
        e, self.e3 = self.e3, None
        if e: self.add('E3_WITHOUT_AMEND', 'an amend adding an objective before the E3 probe or round', 'none', idx=e)

    # ---- records
    def feed(self, rec, idx):
        self.idx, t, self.nrec = idx, rtype(rec), self.nrec + 1
        if self.ended: self.add('AFTER_OVERFIT', 'no record: "OVERFIT ends the archive"', t)
        elif self.exited and t != 'resume': self.exited = self.add('AFTER_EXIT', 'resume', t) or False
        fn = getattr(self, 'r_' + t, None) if t else None
        try:
            return fn(rec) if fn else self.warnings.append('line %d: unknown record type %r' % (self.idx, t))
        except BAD as e:
            self.na('record', 'line %d: %r' % (idx, e))

    def set_done(self, done):
        self.done = done if isinstance(done, dict) else None
        self.crit, self.final = crits(self.done), canon(hid((self.done or {}).get('final_rung') or self.final))
        unk = [c for c in self.crit if self.kind(c) is None]   # which check decides these criteria is unknown
        if unk: self.miss('kind', 'DONE.criteria[].kind (command|source|judges)', unk,
                          any(not self.crit[c].get('kind') for c in unk))
        nof = [c for c, v in self.crit.items() if self.kind(c) == 'command' and type(v.get('files') or 0) is not list]
        if nof: self.miss('check_files', 'DONE.criteria[].files ("listing every file it runs")', nof)

    def r_setup(self, s):
        if self.setup is not None:                   # a resume logs `resume`: a second setup is ignored
            return self.add('SETUP_REPEATED' if dkey(s.get('done')) == dkey(self.setup.get('done')) else
                            'UNRECORDED_AMEND', 'resume (or an amend)', 'setup')
        if self.nrec > 1: self.add('SETUP_LATE', 'setup as the first record', 'record %d' % self.nrec)
        self.setup, self.setup_idx, self.start = s, self.idx, minutes(s.get('t0'))
        self.set_done(s.get('done'))
        top, dn = canon(s.get('final_rung')), canon((self.done or {}).get('final_rung'))
        if None not in (top, dn) and top != dn: self.add('FINAL_RUNG_CONFLICT', dn, top)   # DONE's rung applies
        elif top is not None: self.final = hid(top)
        if not self.crit: self.miss('setup', 'setup.done.criteria', absent=not (self.done or {}).get('criteria'))
        self.budg = self.bcheck(s.get('budget'), 'setup')   # "minutes and tokens only as the host reports them"

    def r_citation(self, c): self.cites.append(c)
    def r_substrate(self, s):  # required from DONE by criterion; waived needs a later amend; not closed or waived: open
        g, st, n, ev = s.get('gap'), canon(s.get('status')), len(self.amends), s.get('evidence')
        if st == 'open': self.opened[g] = n
        if st == 'closed' and not (ev and any(canon(x.get('status')) == 'verified' and x.get('locator') == ev
                                              for x in self.cites)):   # "Verifier-checked evidence"
            if self.v3: st = self.add('CLOSED_UNVERIFIED', 'evidence = a verified citation locator', ev)   # stays open
            else: self.na('substrate', 'substrate.evidence (closure unverified)')
        ok = st == 'closed' or (st == 'waived' and n > self.opened.get(g, 0))   # closed: required until written in
        w = st == 'closed' and self.rs['rm'] > 0     # written in by the round just logged (markers in aggregate)
        self.rs['rm'] -= w
        self.subs[g] = (hid(s.get('criterion')), 'closed' if st == 'closed' and not w else 'resolved' if ok else 'open')
        self.waive = self.waive + (st == 'waived' and ok) if self.waive is not None else None

    def r_amend(self, a):
        d, self.amends, self.paused = a.get('done'), self.amends + [a], True
        if a.get('budget') is not None: self.budg = self.bcheck(a['budget'], 'amend')   # the live budget from here
        if not isinstance(d, dict): self.miss('required', 'amend.done (DONE after the amend)', a.get('what'), d is None)
        elif set(crits(d)) - set(self.crit): self.e3, self.obj = None, True   # a new criterion: an objective
        if isinstance(d, dict) and dkey(d) == dkey(self.done): return   # DONE unchanged: every result stands
        self.epoch, self.done_known, old = self.epoch + 1, isinstance(d, dict), self.crit   # no `done`: unauditable
        if isinstance(d, dict): self.set_done(d)
        self.rs['latest'] = {c: x for c, x in self.rs['latest'].items() if self.crit.get(c) == old.get(c)}
        if self.due and self.due[0] in ('boundary', 'halt:STALL', 'halt:OVERFIT'): self.due = None

    def r_probe(self, p):
        rung, mode, idn, sd = canon(hid(p.get('rung'))), canon(p.get('mode')), p.get('identity'), p.get('seeded')
        if rung is None: return self.miss('probe', 'probe.rung')
        self.e3_due()
        pair = sd.get('pair') if isinstance(sd, dict) else None
        if isinstance(idn, list) and isinstance(pair, list) and len(idn) == len(pair) == 2:   # both orders
            miss = any(canon(x) != 'best' for x in pair) or canon(sd.get('check')) != 'fail' or bool(
                p.get('misses')) or bool(self.crit) and self.kind(hid(sd.get('criterion'))) != 'judges'
            exp = 'strict' if miss or any(canon(x) != 'tie' for x in idn) else 'normal'   # seeded: a judges criterion
            if mode not in (exp, 'strict'): self.add('PROBE_MODE_WRONG', exp, mode)   # strict by choice fails closed
            mode = 'strict' if 'strict' in (exp, mode) else exp
        else:                                        # v3: normal mode is unproven, so the rung is strict
            self.miss('probe_mode', 'probe.identity/seeded.pair (two orders each)', [idn, pair], not idn or not pair)
            mode = 'strict' if self.v3 else mode
        if self.probes.get(rung) is not None:       # a re-probe never relaxes the first: strict stays strict
            self.add('PROBE_REROLL', 'one probe per rung', rung)
            mode = 'strict' if 'strict' in (mode, self.probes[rung]) else mode
        self.probes[rung] = mode

    def r_rung(self, r):
        nm = canon(hid(r.get('name')))
        if RUNGS.get(nm, 0) <= RUNGS.get(self.rung, 0):   # not an escalation: no reset, and nothing due is settled
            return self.add('RUNG_REPEATED', 'a rung above ' + str(self.rung), nm)
        self.pre('rung', r)
        if nm == 'E3' and not self.obj: self.e3 = self.idx
        self.rung, self.rs['s'], self.paused = nm, 0, True

    def r_resume(self, r):
        exp = self.rs['n'] + 1
        if self.due and self.due[0] == 'version':  # unfinished round: rerun, never applied
            exp, self.rs, self.due, self.pend, self.osc = self.pend.get('n'), self.snap or self.rs, None, None, None
        if r.get('at_round') not in (None, exp): self.add('RESUME_MISMATCH', exp, r.get('at_round'))
        self.waive, self.why = 0 if self.why == canon('OPEN') else None, None   # "OPEN with all gaps waived -> Stop"
        self.exited, self.paused = self.ended, True   # after OVERFIT the archive stays ended

    def r_variant(self, v):                          # v2 format: keep rules are unauditable (v3: RECORD_MISSING)
        self.miss('keep', 'round record (a v2 variant record hides a round)')
        if v.get('kept') is True:                    # its version record is still audited for lineage
            self.pend, self.due = dict(n=v.get('round'), best=self.best, var={'id': v.get('id')}), ('version', self.idx)
    def r_halt(self, h): self.miss('exit', 'exit.status (v2 halt record)')   # v2 format

    def r_approve(self, a):  # the human approves a restructure (sections?: else any) or an OSCILLATION pick
        w, vid, self.paused = canon(a.get('what')), hid(a.get('version')), True
        if w == 'restructure': return self.rs['appr'].append(a.get('sections'))   # one approval: one kept restructure
        if w != 'pick' or vid not in self.vers:
            return self.miss('approve', 'approve{what:restructure|pick,version (a logged version)}', [w, vid],
                             w is None or (w == 'pick' and vid is None))
        if not self.pick: self.add('PICK_WITHOUT_HALT', 'a pick only after HALT(OSCILLATION)', vid)   # still applied
        self.best, (self.best_words, lt), self.pick = vid, self.vers[vid], False
        self.rs['latest'] = dict(lt)

    def r_version(self, v):
        words, vid = v.get('words'), hid(v.get('id'))
        if self.due and self.due[0] == 'version':   # a keep: its version precedes any halt
            p, pw = self.pend, self.pend['var'].get('words')
            if v.get('parent') != p['best']: self.add('STALE_PARENT', p['best'], v.get('parent'))
            if 'diff' not in v or 'diff' not in p['var']: self.miss('kept_text', 'version.diff / variant.diff', vid)
            elif not same_text(diffs(v), diffs(p['var'])): self.add('KEPT_TEXT_MISMATCH', diffs(p['var']), diffs(v))
            elif num(words) and num(pw) and words != pw: self.add('KEPT_TEXT_MISMATCH', 'words %s' % pw, words)
            self.cfe(dfiles(diffs(v)) - dfiles(diffs(p['var'])))   # the applied text names a check file
            words, self.due, self.pend = pw if words is None else words, None, None
        elif v.get('parent') is not None or self.rs['any_round'] or self.vers:   # one root: v0 (at setup)
            self.add('VERSION_WITHOUT_KEEP', 'a kept round before a version', v.get('id'))
        if vid in self.vers:                         # new text under an old id: nothing recorded before stands
            self.epoch = self.add('VERSION_ID_REUSED', 'a new version id', vid) or self.epoch + 1
        self.best, self.best_words, self.vers[vid] = vid, words, (words, dict(self.rs['latest']))

    # ---- rounds: gates, panel, eligibility, selection, stall
    def verdict(self, v, s):
        if v.get('overall') is None: return self.miss('keep', 'verdicts[].overall', v)
        ov, o, cr = canon(v['overall']), v.get('orders'), {k: canon(x) for k, x in (v.get('criteria') or {}).items()}
        ov = ov if ov in VALUES else 'UNKNOWN'       # an unreadable verdict is never support
        if ov in DONE_VALS and 'criteria' not in v: self.miss('keep', 'verdicts[].criteria', s)
        if s == 1 and isinstance(o, list) and len(o) >= 2:
            o = o[:2] if len(o) == 2 else self.add('EXTRA_VERDICT', 'two orders (the first two stand)', len(o)) or o[:2]
            vals = [canon(x.get('overall') if isinstance(x, dict) else x) for x in o]
            rov, rcr = 'ERROR' if 'ERROR' in vals else vals[0] if vals[0] == vals[1] in VALUES else 'UNKNOWN', cr
            if all(isinstance(x, dict) and isinstance(x.get('criteria'), dict) for x in o):
                a, b = ({k: canon(y) for k, y in x['criteria'].items()} for x in o)
                rcr = {k: a.get(k) if a.get(k) == b.get(k) else 'UNKNOWN' for k in set(a) | set(b)}
            if (rov, rcr) != (ov, cr): self.add('ORDER_MISMAP', [rov, rcr], [ov, cr])
            ov, cr = rov, rcr
        elif s == 1:                                 # an ERROR needs no orders: it is dropped either way
            self.miss('order', 'verdicts[slot=1].orders', o, (not o or isinstance(o, list)) and ov != 'ERROR')
        rt = v.get('retries')
        if not num(rt): self.miss('retry', 'verdicts[].retries', rt, rt is None)   # "0" is malformed: unauditable
        elif rt > 1: ov = self.add('RETRY_EXCEEDED', '<= 1', rt) or 'ERROR'
        elif ov == 'ERROR' and rt < 1: self.add('RETRY_MISSING', 'one retry before an ERROR stands', rt)
        return ov, cr, canon(v.get('confidence'))

    def gate(self, var):
        """-> 'ok' | 'dropped' | 'rejected' | 'regression' | None (unauditable; v3: RECORD_MISSING)."""
        g, vid = var.get('gates'), var.get('id')
        if not isinstance(g, dict): return self.miss('gates', 'round.variants[].gates', vid, g is None)
        gr = g.get('retries')                        # gates{...,retries}: "Retry an ERROR once (retries)"
        rts = [x for x in (gr.values() if isinstance(gr, dict) else [gr]) if num(x)]
        if not rts: self.miss('gates', 'gates.retries', vid, gr is None)   # malformed ("0"): unauditable
        if any(x > 1 for x in rts): return self.add('RETRY_EXCEEDED', '<= 1', gr) or 'dropped'
        (ap, scr, vf), cm = (cres(g.get(k)) for k in ('apply', 'screen', 'verifier')), g.get('commands')
        cmds = {c: cres(x) for c, x in cm.items()} if isinstance(cm, dict) else {}
        if 'ERROR' in (ap, scr, vf) or 'ERROR' in cmds.values():
            if rts and sum(rts) < 1: self.add('RETRY_MISSING', 'one retry before an ERROR stands', gr)
            return 'dropped'
        if ap != 'pass': return self.miss('gates', 'gates.apply', vid) if ap is None else 'dropped'  # not applied
        for c, x in cmds.items():                    # any result but pass is a failure (UNKNOWN is never a pass)
            if x != 'pass' and self.kind(c) in ('command', None):
                if self.rs['latest'].get(c) == 'pass': return 'regression'
                if c not in self.rs['latest']: self.na('regression', 'check{trigger:setup}.' + c)
        if scr not in (None, 'pass'): return 'rejected'   # reject..., UNKNOWN or unreadable: never a pass
        need = ['gates.commands.%s' % c for c in self.crit if self.kind(c) == 'command' and c not in cmds]
        need += ['gates.' + k for k in ('verifier', 'screen') if g.get(k) is None]   # every command, Verifier, Screen
        return self.miss('gates', ' / '.join(need), vid) if need else None if gr is None else 'ok'

    def panel(self, var, strict, prot):
        """Recompute the judged outcome: exp = dropped | rejected | eligible | None (unauditable)."""
        vs, vid = var.get('verdicts'), var.get('id')
        if not isinstance(vs, list): return self.miss('keep', 'round.variants[].verdicts', vid, vs is None)
        slots, xobj = {}, False
        for v in vs:
            s = v.get('slot') if isinstance(v, dict) else None
            s = int(s) if isinstance(s, str) and s.strip().isdigit() else s   # slot "3" is slot 3
            if s is None: return self.miss('keep', 'verdicts[].slot', vid, isinstance(v, dict))
            if s in slots or s not in (1, 2, 3):     # the first stands; an extra never supports, but still objects
                self.add('EXTRA_VERDICT', 'one verdict per slot 1-3', s)
                cr = v.get('criteria') if isinstance(v.get('criteria'), dict) else {}
                ov = canon(v.get('overall'))
                xobj = xobj or ov == 'best' or self.veto(ov, {k: canon(x) for k, x in cr.items()}, prot)
            elif (r := self.verdict(v, s)) is None: return None
            else: slots[s] = r
        val = lambda s: slots[s][0] if s in slots else None  # noqa: E731
        comp = [s for s in slots if slots[s][0] in DONE_VALS]
        pbest = xobj or any(self.veto(*slots[s][:2], prot) for s in slots)   # a veto, whatever the overall;
        objection = pbest or any(slots[s][0] == 'best' for s in comp)   # judge 1's rejects early (below)
        early = not strict and val(1) not in (None, 'ERROR') and (
            (val(1) == 'best' and slots[1][2] == 'high') or self.veto(*slots[1][:2], prot))
        same = not strict and val(1) in ('variant', 'best') and val(1) == val(2)
        req = [1] if early else [1, 2] + ([] if same else [3])
        w, bw, ds = var.get('words'), self.best_words, diffs(var)   # an edit whose new text is its old: no change
        nochange = 'diff' in var and all(isinstance(d, dict) and 'new' in d and d['new'] == d.get('old') for d in ds)
        p = dict(missing=[s for s in req if s not in slots], objection=objection or early,
                 nvar=sum(slots[s][0] == 'variant' for s in comp), nbest=sum(slots[s][0] == 'best' for s in comp),
                 shorter=False if nochange else w < bw if all(num(x) for x in (w, bw)) else None)
        if early: p['exp'] = 'rejected'
        elif any(x[0] == 'ERROR' for x in slots.values()): p['exp'] = 'dropped'   # after one retry: not a rejection
        else:
            improve = p['nvar'] >= (3 if strict else 2) and p['nbest'] == 0 and not pbest and not nochange
            shape = not pbest and all(val(s) in ('variant', 'tie') for s in (1, 2, 3)) and not any(
                x not in ('variant', 'tie') for s in (1, 2, 3) for x in slots[s][1].values())
            if shape and not improve and p['shorter'] is None:   # no length for best or the variant: v3, not kept
                self.miss('prune', 'version.words / variant.words', vid, w is None)
            elig = True if improve else None if shape and p['shorter'] is None and not self.v3 else bool(
                shape and p['shorter'])
            p['exp'] = {True: 'eligible', False: 'rejected', None: None}[elig]
        return p

    def budget(self, r):
        b, rs = self.bud(), self.rs
        if not b: self.na('budget', 'setup.budget')
        if num(b.get('rounds')) and rs['cnt'] > b['rounds']:
            self.add('BUDGET_OVERRUN', '<= %g rounds' % b['rounds'], rs['cnt'])   # a non-number: listed at setup
        t0, t1, m = minutes(r.get('t0')), minutes(r.get('t1')), b.get('minutes')
        if t0 is None or t1 is None:                 # minutes null (unreported): no round clock is needed
            if num(m): self.miss('budget_time', 'round.t0/t1', None, None in (r.get('t0'), r.get('t1')))
        else:
            if self.now is not None and (self.paused or t0 < self.now):
                self.start += t0 - self.now          # a human wait or a restarted clock is not loop time
            self.start, self.paused = t0 if self.start is None else self.start, False
            md = rs['maxdur']
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
        n0, g, out = len(self.findings), self.gate(var), var.get('outcome')
        if g not in ('ok', None):
            exp = 'dropped' if g == 'dropped' else 'rejected'
            if out == 'kept': self.add('REGRESSION_KEPT' if g == 'regression' else 'GATE_KEPT', exp, out)
            elif out != exp: self.add('ERROR_AS_REJECTION' if exp == 'dropped' else 'REJECTION_AS_ERROR', exp, out)
            elif var.get('verdicts'): self.add('JUDGED_AFTER_GATE', 'no verdicts after a failed gate', out)
            return exp, None
        p = self.panel(var, strict, prot)
        exp, code = (p or {}).get('exp'), None
        if exp == 'eligible' and any(f['code'] == 'RECORD_MISSING' for f in self.findings[n0:]): exp = None   # closed
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
        try: return self.judge_variant(v, strict, prot)
        except BAD as e: return self.na('record', 'line %d: %r' % (self.idx, e)), None

    def ledger(self, res):  # an idea rejected by >=2 judges or twice by the screen needs new evidence (advisory)
        for v, e, p in res:
            k, g = json.dumps(diffs(v), sort_keys=True), v.get('gates')
            sc, ban = self.ideas.get(k, (0, None))
            if diffs(v) and ban == len(self.cites): self.add('REJECTED_IDEA', 'a new citation first', v.get('id'))
            sc += isinstance(g, dict) and str(g.get('screen')).casefold().startswith('reject')
            self.ideas[k] = (sc, len(self.cites) if sc >= 2 or (p or {}).get('nbest', 0) >= 2 else ban)

    def r_round(self, r):
        self.e3_due()
        self.pre('round', r)
        n, rs = r.get('n'), self.rs
        if n != rs['n'] + 1: self.add('ROUND_SEQUENCE', rs['n'] + 1, n)
        if not self.vers and not rs['any_round']: self.miss('version', 'version v0 (logged at setup)', r.get('best'))
        self.snap = copy.deepcopy(rs)
        if self.rung not in self.probes:             # "or no judges criterion (no probe) -> strict mode"; else a
            nj = self.crit and all(self.kind(c) in ('command', 'source') for c in self.crit)   # missing probe is
            self.probes[self.rung] = 'strict' if nj else self.add(   # reported once (normal; v3: strict, fail closed)
                'PROBE_MISSING', 'probe{rung}', self.rung) or self.v3 and 'strict' or None
        if r.get('best') != self.best: self.add('STALE_PARENT', self.best, r.get('best'))
        rs['cnt'], rs['rm'] = rs['cnt'] + 1, 0       # the budget counts round records, never the logged n
        self.budget(r)
        strict, prot, seen = self.probes.get(self.rung) == 'strict', self.protected(), set()
        vs = [dict(v, outcome=canon(v.get('outcome'))) for v in r['variants'] if isinstance(v, dict)] \
            if isinstance(r.get('variants'), list) else []
        if len(vs) > 2:                              # proposals beyond 2: keeping one of them is a VIOLATION
            self.add('VARIANT_COUNT', '<= 2 variants', len(vs), 'VIOLATION' if any(
                v.get('outcome') == 'kept' for v in vs[2:]) else 'RECORD')
        for v in vs:                                 # one variant logged twice (same id or edits): a re-ask
            ks = {('i', hid(v.get('id'))), ('d', json.dumps(diffs(v), sort_keys=True))} - {('i', None), ('d', '[]')}
            if ks & seen: self.add('VARIANT_REPEATED', 'one entry per variant (the first stands)', v.get('id'),
                                   'VIOLATION' if v['outcome'] == 'kept' else 'RECORD')
            seen |= ks
        res = [(v,) + self.judge(v, strict, prot) for v in vs]
        self.ledger(res)
        elig = [(i, v, p) for i, (v, e, p) in enumerate(res) if e == 'eligible']
        top = [x for x in elig if x[2]['nvar'] == max(y[2]['nvar'] for y in elig)]
        if len(top) > 1 and not all(num(x[1].get('words')) for x in top):   # "then shorter" needs words
            sel = self.miss('selection', 'variants[].words', None, any(x[1].get('words') is None for x in top))
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
            rs['latest'] = {c: x for c, x in rs['latest'].items() if self.kind(c) != 'command'}
            rs['latest'].update({c: cres(x) for c, x in cm.items() if cres(x) in ('pass', 'fail')})
            self.pend, self.due = {'n': n, 'best': r.get('best'), 'var': k}, ('version', self.idx)
            self.keep_checks(k)
        elif vs and all((e or v.get('outcome')) == 'dropped' for v, e, _ in res):
            rs['e'] += 1                             # all-ERROR round: not a stall; two or more in a row halt
            self.due = ('halt:ERROR', self.idx) if rs['e'] >= 2 else self.due
        else:
            rs['s'], rs['e'] = rs['s'] + 1, 0
            if rs['s'] >= 3 and self.result(self.best, self.rung) is None: self.due = ('check', self.idx)
            elif rs['s'] >= 3: self.post_check()     # the standing Check is reused, never re-rolled

    def cfe(self, fs):  # edits to check files: setup.check_files, or a command criterion's `files` in DONE
        cf = [(self.setup or {}).get('check_files')] + [v.get('files') for v in self.crit.values()]
        cf = {nf(f) for x in cf if isinstance(x, list) for f in x if isinstance(f, str)}   # none: set_done lists it
        for f in sorted(fs):
            if any(f == c or f.startswith(c + os.sep) for c in cf): self.add('CHECK_FILE_EDIT', 'no edit', f)

    def keep_checks(self, k):
        hist, ratio, exact, ds = self.rs['hist'], 0.0, False, [d for d in diffs(k) if isinstance(d, dict)]
        key = lambda x: ' '.join(str(x).split()).casefold()  # noqa: E731 (a section, whatever its case or spacing)
        secs, ap = {key(d.get('section')) for d in ds}, self.rs['appr']   # "one change to one section ... of best,
        if len(secs) > 1:                            # or one human-approved restructure": an approve covering them
            i = next((i for i, a in enumerate(ap) if a is None or isinstance(a, list) and secs <= set(map(key, a))), -1)
            if i < 0: self.add('MULTI_SECTION', 'one section, or a prior approve{what:restructure}', sorted(secs))
            else: del ap[i]                          # spent by this keep
        self.cfe(dfiles(diffs(k)))
        self.rs['marks'] = max(0, self.rs['marks'] + sum(opens(d) for d in diffs(k)))   # [OPEN] now in best
        rm = -sum(min(0, opens(d)) for d in diffs(k))   # "closes it (substrate.evidence) and a round writes it in"
        cl = [g for g, (_, st) in self.subs.items() if st == 'closed']
        for g in cl[:rm]: self.subs[g] = (self.subs[g][0], 'resolved')
        self.rs['rm'] = max(0, rm - len(cl))           # left for a closure this round logs after it
        for d in ds:
            sec, new, cur = key(d.get('section')), *(' '.join(str(d.get(x) or '').split()) for x in ('new', 'old'))
            for old in hist.get(sec, []):            # a restore moves the text back toward an earlier best's
                r = difflib.SequenceMatcher(None, new, old).ratio()
                if old != cur and r > difflib.SequenceMatcher(None, cur, old).ratio():
                    ratio, exact = max(ratio, r), exact or (r == 1.0 and cur in hist[sec])   # an exact undo
            hist.setdefault(sec, []).extend(x for x in (cur, new) if x not in hist.get(sec, []))
        self.rs['ratio'] = ratio
        if ratio >= 0.9: self.osc = (self.idx, ratio, exact)   # advisory unless exact: "(nearly)" is a judgment

    # ---- Check, held-out, exit
    def r_check(self, c):
        self.pre('check', c)
        if not isinstance(c.get('results'), dict) or 'version' not in c:
            return self.miss('check', 'check.version/results', None, c.get('results') is None or 'version' not in c)
        ver, rung = c['version'], canon(hid(c.get('rung', self.rung)))
        base = not self.rs['any_round'] and ver == self.best          # v0's baseline run, before any round
        setup = canon(c.get('trigger', 'setup' if base else None)) == 'setup' and base
        if canon(c.get('trigger')) == 'setup' and not base: self.add('SETUP_CHECK_LATE', 'v0 before round 1', ver)
        key = (ver, rung, self.epoch)
        if not setup and (ver != self.best or rung != self.rung):
            return self.add('CHECK_NOT_BEST', [self.best, self.rung], [ver, rung])
        if not setup and key in self.standing:
            return self.add('RECHECK_UNCHANGED', 'the first Check on %s/%s stands' % (ver, rung), 'another Check')
        strict, vals, jr = self.probes.get(rung, self.v3 and 'strict') == 'strict', {}, False   # v3: no probe: strict
        for cid, r in c['results'].items():
            r = r if isinstance(r, dict) else {'value': r}
            kind, val = self.kind(cid, r), canon(r.get('value'))
            jr = jr or kind == 'judges'
            if kind == 'judges': val = self.tally('check', cid, r, strict, val == 'pass')
            elif kind == 'source' and val == 'pass':   # "pass only if all its claims verify": that version's
                cs = [x for x in self.cites if x.get('criterion', cid) == cid]   # citations (none: not a pass)
                mine = [canon(x.get('status')) for x in cs if x.get('version') == ver]
                if any('version' not in x or 'criterion' not in x for x in cs) or not (cs or self.v3):
                    val = self.miss('check_source', 'citation.criterion/version', cid) or self.v3 and 'unchecked' or val
                elif not mine or any(s != 'verified' for s in mine):
                    val = self.add('CHECK_MISCOUNT', 'all %s citations on %s verified' % (cid, ver), mine) or 'fail'
            elif kind is None and self.v3 and val == 'pass': val = 'unchecked'   # unknown kind: nothing decided it
            vals[cid] = val
        if self.v3 and not c.get('models') and ('models' not in c or jr):   # check{...,models,...}: "one source per
            self.add('RECORD_MISSING', 'check.models', c.get('models'))       # named model family" (null: no judges)
        self.rs['latest'].update({k: v for k, v in vals.items() if v in ('pass', 'fail')})
        if not setup:                                # the setup Check is v0's baseline, not a Check
            self.standing[key] = vals
            self.post_check()

    def tally(self, where, cid, r, strict, need):  # {value, votes} by the Check rule -> the value it credits
        val, vt = canon(r.get('value')), r.get('votes')
        vt = list(vt.values()) if isinstance(vt, dict) else vt   # {judge: vote}: its votes
        if not (isinstance(vt, list) and vt):      # v3: a pass without readable votes is not credited
            self.miss(where + '_votes', '%s.results[%s].votes' % (where, cid), val, not vt and need)
            return 'unchecked' if self.v3 and val == 'pass' else val
        vt = [canon(x) for x in vt]                # 3 judges; any extra vote counts against a pass
        if len(vt) > 3: self.add('EXTRA_VERDICT', '3 votes', len(vt))
        ok = sum(x == 'pass' for x in vt) >= (max(3, len(vt)) if strict else max(2, len(vt) // 2 + 1))
        exp = 'unchecked' if 'ERROR' in vt else 'pass' if ok else 'fail'   # an ERROR vote: never a pass
        if (val == 'pass') != (exp == 'pass'): self.add('CHECK_MISCOUNT', 'recounted ' + exp, val)
        return 'pass' if exp == 'pass' else val if val in ('fail', 'unchecked') else exp

    def r_heldout(self, h):
        self.pre('heldout', h)
        res, att, st, self.paused = h.get('results'), h.get('attempt'), canon(h.get('set')), True   # the human runs it
        if 'version' not in h or not isinstance(res, dict):   # "the human reports only the marks"
            return self.miss('heldout', 'heldout.version/results', h.get('pass'), 'version' not in h or res is None)
        if (o := self.open_required()): self.add('OPEN_AT_HELDOUT', 'exit PARTIAL OPEN first', o, self.ocls())
        n, ver, prev, req = len(self.heldout) + 1, h['version'], self.heldout, self.required()
        strict = self.probes.get(self.rung, self.v3 and 'strict') == 'strict'   # "(heldout.results; Check rule)"
        fails = {c for c in (list(res) if req is None else req) if c not in res or self.tally(   # "Each non-pass is
            'heldout', c, res[c] if isinstance(res[c], dict) else {'value': res[c]}, strict, True) != 'pass'}
        passed = not fails                           # non-pass in best's Check": fail, unchecked or unreported
        if not num(att): self.miss('heldout', 'heldout.attempt', att, att is None)   # a label: attempts are counted
        if st is None or (n == 2 and st != 'spare'): self.miss('heldout', 'heldout.set (2: spare)', st, st is None)
        reroll = n > 2 or (num(att) and att != n) or (n == 1 and st == 'spare') or (n == 2 and (
            prev[0]['passed'] or ver == prev[0]['version'] or st == 'primary'))
        if reroll: self.add('HELDOUT_REROLL', 'attempt %d: not the spares first; then spares on a changed best' % n,
                            [att, ver])              # a rerolled pass never counts
        elif ver != self.best or self.rung != self.final or self.all_pass(ver, self.final) is False:
            self.add('HELDOUT_UNCHECKED', 'best with an all-pass Check at ' + self.final, [ver, self.rung])
        self.heldout.append({'attempt': att, 'version': ver, 'epoch': self.epoch,   # attempt 2 runs the spares
                             'passed': passed and not reroll and st is not None and (n == 1 or st == 'spare')})
        self.hofail.setdefault((ver, self.epoch), set()).update(fails)
        if ver == self.best: self.rs['latest'].update({c: 'fail' for c in fails})
        if n == 2 and not passed: self.due = ('halt:OVERFIT', self.idx)

    def r_exit(self, x):
        self.pre('exit', x)
        st, why, rs, conds = canon(x.get('status')), canon(x.get('reason')), self.rs, self.complete_conds()
        if st == 'COMPLETE' and conds:
            if not conds[0]: self.add('FALSE_COMPLETE', 'PARTIAL', conds[2])
            if not conds[1]: self.add('OPEN_AT_COMPLETE', 'exit PARTIAL OPEN', self.open_required(), self.ocls())
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
        elif st != 'COMPLETE': self.miss('exit', 'exit.status', st, st is None)
        self.exited, self.exit_status, self.why, self.pick, self.paused = True, st, why, why == 'OSCILLATION', True
        self.ended = self.ended or why == 'OVERFIT'   # "OVERFIT ends the archive": nothing may follow, not even resume

    # ---- options and summary
    def check_done(self, path):
        cur = (self.setup or {}).get('done')
        for a in self.amends:
            if not isinstance(a.get('done'), dict): return self.na('done_drift', 'amend.done')
            cur = a['done']
        with open(path, encoding='utf-8') as f: new = json.load(f)
        if dkey(new) != dkey(cur): self.add('UNRECORDED_AMEND', 'DONE = setup.done + amends', path, idx=self.setup_idx)
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
        if self.waive and not self.open_required():   # Stop: held-out needs best's all-pass Check at the final rung
            return 'heldout' if self.rung == self.final and self.all_pass(self.best, self.final) else 'halt:OPEN'
        if k not in (None, 'version'):   # Stop; after a failed attempt 1 on best: rounds until a changed best passes
            return k if k != 'boundary' or self.rung != self.final else 'halt:OPEN' if self.open_required() else \
                'heldout' if not self.spent() else 'halt:BUDGET' if self.budget_out() else 'round'
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
    a.v3 = next((isinstance(r.get('loop'), str) and r['loop'].strip().casefold().startswith('v3')
                 for _, r in recs if rtype(r) == 'setup'), False)   # a v3 archive is v3 from its first line
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
    integ = integ and {'line': integ, 'error': 'unparsable interior line (or a repeated key)'}
    if not integ and not any(rtype(r) and hasattr(a, 'r_' + rtype(r)) for _, r in recs):
        integ = {'line': None, 'error': 'no RQGM records: no line {"t":name,...} names a record'}  # never ok
    ok = not integ and not any(f['class'] == 'VIOLATION' for f in a.findings)
    out = {'ok': ok, 'state': a.state(), 'violations': a.findings, 'unauditable': a.unaud,
           'warnings': a.warnings, 'torn_tail': torn is not None, 'torn_line': torn, 'set_aside': aside,
           'integrity': integ}
    if not pending: return out, 2 if integ else 0 if ok else 1
    with open(pending, encoding='utf-8') as f: pr = json.load(f)
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
    with open(os.path.join(d, 'expected.json'), encoding='utf-8') as f: cases = json.load(f)['cases']
    fx, named = os.path.join(d, 'fixtures'), {c['fixture'] for c in cases}
    fails = [{'fixture': n, 'error': 'no expected case'} for n in sorted(os.listdir(fx))
             if n.endswith('.jsonl') and n not in named]
    for c in cases:
        a = c.get('args', {})
        opt = lambda k: os.path.join(fx, a[k]) if a.get(k) else None  # noqa: E731
        path, text = os.path.join(fx, c['fixture']), None
        try:
            if c.get('strip_final_newline'):         # a torn-before-newline variant, derived in memory
                with open(path, encoding='utf-8') as f: text = f.read().rstrip('\r\n')
            out, code = audit(path, opt('done'), opt('target'), bool(a.get('first')),
                              os.path.join(fx, c['pending']) if c.get('pending') else None, text)
        except Exception as e:                       # a crash is a failed case, never a pass
            fails.append({'fixture': c['fixture'], 'error': repr(e)})
            continue
        if c.get('pending'):
            want = dict({k: c.get(k) for k in ('required_keep', 'outcomes', 'next_due')}, exit=c.get('exit', 0))
            got = dict({k: out.get(k) for k in want if k != 'exit'}, exit=code)
        else:
            want = {'codes': sorted(c['codes']), 'exit': c.get('exit', int(any('VIOLATION' in x for x in c['codes']))),
                    'state': c.get('state', {}), 'unaud': sorted(c.get('unauditable_includes', []))}
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
            print(json.dumps(clip(res), indent=1))
            return 0 if res['ok'] else 1
        if op == 'audit' and len(pos) == 1 and None not in opts.values():
            out, code = audit(pos[0], opts.get('done'), opts.get('target'), '--first' in rest, opts.get('pending'))
            print(json.dumps(clip(out), indent=1))
            return code
    except Exception as e:                           # never exit 1 on a crash: 1 means violations
        print(json.dumps({'ok': False, 'error': repr(e)}))
        return 2
    print(__doc__, file=sys.stderr)
    return 2

if __name__ == '__main__': sys.exit(main(sys.argv[1:]))
