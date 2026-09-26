#!/usr/bin/env python3
"""Adversarial archives for skills/rqgm-loop/rqgm_check.py (read-only test input; never edits the checker).

  python gen_attacks.py            write every archive next to this file, run 'audit' on each, print a summary
  python gen_attacks.py --json     same, but print the full checker output for every archive

Naming: fnNN_* = violates a SKILL.md rule (checker should report a VIOLATION);
        fpNN_* = legitimate under SKILL.md (checker should report no VIOLATION);
        crNN_* = malformed input (checker should degrade to unauditable, never crash).
"""
import copy, json, os, subprocess, sys  # noqa: E401

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
CHECKER = os.path.join(REPO, 'skills', 'rqgm-loop', 'rqgm_check.py')

CRIT = [{"id": "c1", "required": True, "kind": "command", "command": "pytest -q"},
        {"id": "c2", "required": True, "kind": "source"},
        {"id": "c3", "required": True, "kind": "judges"}]
DONE = {"criteria": CRIT, "must_not_change": []}
ALLPASS = {"c1": {"kind": "command", "value": "pass"}, "c2": {"kind": "source", "value": "pass"},
           "c3": {"kind": "judges", "value": "pass", "votes": ["pass", "pass", "pass"]}}


def setup(final='E2', budget=None, done=None, **kw):
    r = {"t": "setup", "loop": "v3", "done": copy.deepcopy(done or DONE),
         "models": {"generator": "m-gen", "judges": ["m-j", "m-j", "m-j"]},
         "budget": budget or {"rounds": 10, "minutes": 600, "tokens": None}, "final_rung": final}
    r.update(kw)
    return r


V0 = {"t": "version", "id": "v0", "parent": None, "round": 0, "diff": [], "words": 100}
SETUP_CHECK = {"t": "check", "version": "v0", "rung": "E1", "trigger": "setup",
               "results": {"c1": {"kind": "command", "value": "pass"}, "c2": {"kind": "source", "value": "pass"}}}


def probe(rung='E1', mode='normal', identity=('tie', 'tie'), pair=('best', 'best'), check='fail'):
    return {"t": "probe", "rung": rung, "mode": mode, "identity": list(identity),
            "seeded": {"criterion": "c3", "pair": list(pair), "check": check}, "misses": []}


def J(slot, overall, conf='med', criteria=None, orders=None, retries=0):
    v = {"slot": slot, "model": "m-j"}
    if slot == 1:
        v["orders"] = orders if orders is not None else [overall, overall]
    v.update({"overall": overall, "criteria": criteria or {}, "confidence": conf, "retries": retries})
    return v


def var(vid, verdicts, outcome, words=100, commands=None, screen='pass', section=None, diff=None, apply='ok',
        gates=None):
    sec = section or 'S-' + vid
    d = diff if diff is not None else [{"section": sec, "old": "old text of " + vid, "new": "new text of " + vid}]
    g = gates if gates is not None else {"apply": apply, "commands": {"c1": "pass"} if commands is None else commands,
                                         "verifier": [], "screen": screen}
    return {"id": vid, "section": sec, "words": words, "diff": d, "gates": g, "verdicts": verdicts,
            "outcome": outcome}


def rnd(n, best, variants, kept, t0=None, t1=None, tokens=None):
    t0 = (n - 1) * 10 if t0 is None else t0
    return {"t": "round", "n": n, "best": best, "t0": t0, "t1": t0 + 5 if t1 is None else t1, "tokens": tokens,
            "variants": variants, "kept": kept}


def ver(vid, parent, variant, n):
    return {"t": "version", "id": vid, "parent": parent, "round": n, "diff": copy.deepcopy(variant["diff"]),
            "words": variant["words"]}


def chk(v, rung, results=None, trigger='claim'):
    return {"t": "check", "version": v, "rung": rung, "trigger": trigger,
            "results": copy.deepcopy(ALLPASS if results is None else results)}


def keep_round(n, best, vid_new, section=None, words=100, t0=None, t1=None, variant=None):
    """A clean round keeping one variant on 2/2 support, plus its version record."""
    v = variant or var('r%d-a' % n, [J(1, 'variant'), J(2, 'variant')], 'kept', words=words, section=section)
    return [rnd(n, best, [v], v["id"], t0=t0, t1=t1), ver(vid_new, best, v, n)]


def stall_round(n, best, t0=None, t1=None):
    v = var('r%d-a' % n, [J(1, 'best', conf='high')], 'rejected')
    return rnd(n, best, [v], None, t0=t0, t1=t1)


def err_round(n, best):
    vs = [var('r%d-%s' % (n, s), [], 'dropped', apply='ERROR', commands={}) for s in 'ab']
    return rnd(n, best, vs, None)


HEAD = lambda final='E2', **kw: [setup(final, **kw), V0, SETUP_CHECK, probe()]  # noqa: E731
EX = lambda st='PARTIAL', why='HUMAN': {"t": "exit", "status": st, "reason": why}  # noqa: E731
HO = lambda att, v, p=None, s='primary': {"t": "heldout", "attempt": att, "set": s, "version": v,  # noqa: E731
                                           "pass": p or {}}
FAIL_C3 = dict(ALLPASS, c3={"kind": "judges", "value": "fail", "votes": ["pass", "fail", "fail"]})

A = {}  # name -> dict(records | raw, args, direction, rule, expect)


def case(name, direction, rule, expect, records=None, raw=None, args=None):
    A[name] = dict(records=records, raw=raw, args=args or {}, direction=direction, rule=rule, expect=expect)


# ------------------------------------------------------------------ false negatives
v = var('r1-a', [J(1, 'variant'), J(2, 'best'), J(2, 'variant')], 'kept')
case('fn01_duplicate_slot_reask', 'false-negative',
     'Never re-ask a returned verdict. / Keep a variant if >=2 judges prefer it (strict: 3), none prefers *best*',
     'slot 2 returned best and was re-asked; KEEP_VETOED (or a re-ask finding)',
     HEAD() + [rnd(1, 'v0', [v], 'r1-a'), ver('v1', 'v0', v, 1), EX()])

v = var('r1-a', [J(1, 'UNKNOWN', orders=['variant', 'best']), J(2, 'variant'), J(3, 'tie'), J(4, 'variant')], 'kept')
case('fn02_fourth_judge_support', 'false-negative',
     'EVALUATORS: 3 judge personas. / Keep a variant if >=2 judges prefer it / UNKNOWN is never a tie, pass or support.',
     'of the 3 panel slots only slot 2 prefers the variant; a 4th slot must not add support -> KEEP_WITHOUT_SUPPORT',
     HEAD() + [rnd(1, 'v0', [v], 'r1-a'), ver('v1', 'v0', v, 1), EX()])

v = var('r1-a', [J(1, 'variant'), J(2, 'variant'), J(3, 'tie'), J(4, 'variant')], 'kept')
case('fn03_strict_fourth_judge', 'false-negative',
     'Strict mode: all 3, no early drop. / Keep a variant if >=2 judges prefer it (strict: 3)',
     'strict: slots 1-3 give 2 variant + 1 tie -> STRICT_KEEP; a 4th slot must not supply the 3rd vote',
     [setup(), V0, SETUP_CHECK, probe(mode='strict', identity=('variant', 'tie')),
      rnd(1, 'v0', [v], 'r1-a'), ver('v1', 'v0', v, 1), EX()])

v = var('r1-a', [J(1, 'variant'), J(2, 'variant')], 'kept')
case('fn04_probe_reroll', 'false-negative',
     'Probe (per rung) ... A non-tie on the identical copy or a missed defect -> **strict mode** / Never re-ask a returned verdict.',
     'the E1 probe returned a non-tie (strict); re-running it until normal is a re-ask -> strict stands -> STRICT_KEEP + JUDGE_MISSING',
     [setup(), V0, SETUP_CHECK, probe(mode='strict', identity=('variant', 'tie')), probe(),
      rnd(1, 'v0', [v], 'r1-a'), ver('v1', 'v0', v, 1), EX()])

case('fn05_probe_empty', 'false-negative',
     'judge 1 compares *best*, in both orders, with an identical copy and with a copy ... seeded with one defect / When unsure, fail closed',
     'a probe with no comparisons cannot establish normal mode -> strict (or probe unauditable); here 2/2 keep passes silently',
     [setup(), V0, SETUP_CHECK, probe(identity=(), pair=()),
      rnd(1, 'v0', [v], 'r1-a'), ver('v1', 'v0', v, 1), EX()])

v2 = var('r2-a', [J(1, 'variant'), J(2, 'variant')], 'kept', commands={"c1": "fail"})
case('fn06_setup_check_launders_regression', 'false-negative',
     'Failing a command *best* passes rejects the variant; a failure *best* shares does not.',
     'best v1 passed c1 at its gate; a mid-run check{trigger:setup} on old v0 marks c1 fail; r2-a fails c1 and is kept -> REGRESSION_KEPT',
     HEAD() + keep_round(1, 'v0', 'v1') + [
         {"t": "check", "version": "v0", "rung": "E1", "trigger": "setup", "results": {"c1": {"kind": "command", "value": "fail"}}},
         rnd(2, 'v1', [v2], 'r2-a'), ver('v2', 'v1', v2, 2), EX()])

SETUP_FAILCHECK = {"t": "check", "version": "v0", "rung": "E1", "trigger": "setup",
                   "results": {"c1": {"kind": "command", "value": "pass"}, "c2": {"kind": "source", "value": "fail"}}}
case('fn07_setup_check_evades_stall', 'false-negative',
     'Check after 3 stall rounds since the last keep ... Failing while stalled -> **HALT(STALL)**',
     'after 3 stalls the Check on best v0 fails required c2; logged with trigger setup it never stands, round 4 runs -> STALL_HALT_MISSED',
     HEAD() + [stall_round(i, 'v0') for i in (1, 2, 3)] + [SETUP_FAILCHECK] + keep_round(4, 'v0', 'v1') + [EX()])

v = var('r1-a', [J(1, 'variant'), J(2, 'variant')], 'kept', commands={})
case('fn08_command_not_run', 'false-negative',
     'Apply the diff to a fresh copy ...; run every command there yourself',
     'c1 (a command best passes) was never run on the kept variant; the checker lists nothing as unauditable',
     HEAD() + [rnd(1, 'v0', [v], 'r1-a'), ver('v1', 'v0', v, 1), EX()])

v = var('r1-a', [J(1, 'variant'), J(2, 'variant')], 'kept',
        gates={"apply": "ok", "commands": {"c1": "pass"}, "verifier": []})
case('fn09_screen_missing', 'false-negative',
     '**Gate**, in order. ... The **Screen** rejects rubric echo, ... / A rule whose inputs are missing is listed as unauditable (checker docstring)',
     'no screen result: the variant passed an unrun gate; checker treats a missing screen as pass and lists nothing unauditable',
     HEAD() + [rnd(1, 'v0', [v], 'r1-a'), ver('v1', 'v0', v, 1), EX()])

v = var('r1-a', [J(1, 'variant'), J(2, 'UNKNOWN', criteria={"c2": "best"}), J(3, 'variant')], 'kept')
case('fn10_unknown_slot_rates_protected_worse', 'false-negative',
     'Keep a variant if >=2 judges prefer it, none prefers *best*, and none rates a **protected** item worse (... criteria *best* passes)',
     'slot 2 rates c2 (passed by best at setup) worse; its overall is UNKNOWN so the checker ignores its criteria -> KEEP_VETOED',
     HEAD() + [rnd(1, 'v0', [v], 'r1-a'), ver('v1', 'v0', v, 1), EX()])

RUNG_E1 = {"t": "rung", "name": "E1", "by": "human"}
case('fn11_same_rung_resets_stall', 'false-negative',
     'On escalation: log the rung, rerun the probe, reset the stall count. / **Check** after 3 stall rounds since the last keep',
     're-logging the current rung is not an escalation; 9 stall rounds with no Check -> MISSED_CHECK',
     HEAD() + [stall_round(i, 'v0') for i in (1, 2, 3)] + [RUNG_E1] + [stall_round(i, 'v0') for i in (4, 5, 6)] +
     [RUNG_E1] + [stall_round(i, 'v0') for i in (7, 8, 9)] + [EX()])

c5 = dict(ALLPASS, c3={"kind": "judges", "value": "pass", "votes": ["fail", "fail", "fail", "pass", "pass"]})
case('fn12_check_extra_votes', 'false-negative',
     'with 3 fresh judges per `judges` criterion (majority; strict: 3/3)',
     'c3 has 3 fails and 2 passes; 2 passes are not a majority -> CHECK_MISCOUNT; COMPLETE rests on it',
     HEAD('E1') + keep_round(1, 'v0', 'v1') + [chk('v1', 'E1', c5), HO(1, 'v1'), EX('COMPLETE', None)])

v = var('r1-a', [J(1, 'variant'), J(2, 'variant'), J(3, 'variant')], 'kept')
c4 = dict(ALLPASS, c3={"kind": "judges", "value": "pass", "votes": ["pass", "pass", "pass", "fail"]})
case('fn13_strict_check_extra_votes', 'false-negative',
     'with 3 fresh judges per `judges` criterion (majority; strict: 3/3)',
     'strict mode; c3 votes 3 pass + 1 fail = not 3/3 of the judges asked -> CHECK_MISCOUNT',
     [setup('E1'), V0, SETUP_CHECK, probe(mode='strict', identity=('variant', 'tie')),
      rnd(1, 'v0', [v], 'r1-a'), ver('v1', 'v0', v, 1), chk('v1', 'E1', c4), HO(1, 'v1'), EX('COMPLETE', None)])

NOOP_AMEND = {"t": "amend", "what": "reword the E1 stance line", "why": "clarity", "by": "human", "done": copy.deepcopy(DONE)}
case('fn14_noop_amend_rerolls_check', 'false-negative',
     'A Check or held-out result stands until *best*, the rung or `DONE` changes.',
     'DONE is identical after the amend; the failing Check on v1/E1 stands -> RECHECK_UNCHANGED, COMPLETE false',
     HEAD('E1') + keep_round(1, 'v0', 'v1') + [chk('v1', 'E1', FAIL_C3), NOOP_AMEND, chk('v1', 'E1'), HO(1, 'v1'),
                                               EX('COMPLETE', None)])

case('fn15_noop_amend_cancels_halt_error', 'false-negative',
     'A round keeping nothing is a **stall** unless every variant ended ERROR (two such in a row -> **HALT(ERROR)**).',
     'two all-ERROR rounds; a DONE-identical amend clears the due HALT(ERROR) and round 3 runs -> ERROR_HALT_MISSED',
     HEAD() + [err_round(1, 'v0'), err_round(2, 'v0'), NOOP_AMEND] + keep_round(3, 'v0', 'v1') + [EX()])

DONE4 = copy.deepcopy(DONE)
DONE4["criteria"].append({"id": "c4", "required": True, "kind": "command", "command": "ruff check"})
AMEND4 = {"t": "amend", "what": "add required c4", "why": "human wants lint", "by": "human", "done": DONE4}
ALL4 = dict(ALLPASS, c4={"kind": "command", "value": "pass"})
case('fn16_heldout_survives_done_change', 'false-negative',
     'A Check or held-out result stands until *best*, the rung or `DONE` changes. / COMPLETE (final rung, held-out pass)',
     'the only held-out pass predates the amend that changed DONE; it no longer stands -> FALSE_COMPLETE',
     HEAD('E2') + keep_round(1, 'v0', 'v1') + [chk('v1', 'E1'), {"t": "rung", "name": "E2", "by": "human"},
                                               probe('E2'), chk('v1', 'E2'), HO(1, 'v1'), AMEND4,
                                               chk('v1', 'E2', ALL4), EX('COMPLETE', None)])

v = var('r2-a', [J(1, 'variant'), J(2, 'variant')], 'kept')
case('fn17_version_id_reuse', 'false-negative',
     '`version{id,parent,diff}` / Count from records, never recollection. / COMPLETE (final rung, held-out pass)',
     'round 2 changes the text but the new version reuses id v1 (parent v1); the old Check and held-out pass are credited -> FALSE_COMPLETE',
     HEAD('E1') + keep_round(1, 'v0', 'v1') + [chk('v1', 'E1'), HO(1, 'v1'), rnd(2, 'v1', [v], 'r2-a'),
                                               ver('v1', 'v1', v, 2), EX('COMPLETE', None)])

recs = HEAD(budget={"rounds": 3, "minutes": 6000, "tokens": None})
best = 'v0'
for i, n in enumerate([1, 2, 3, 1, 2, 3], 1):
    recs += keep_round(n, best, 'v%d' % i, t0=(i - 1) * 10,
                       variant=var('x%d' % i, [J(1, 'variant'), J(2, 'variant')], 'kept'))
    best = 'v%d' % i
case('fn18_round_number_reuse_hides_budget', 'false-negative',
     'Start a round only if one is left / Count from records, never recollection.',
     '6 round records under budget.rounds=3 -> BUDGET_OVERRUN (checker trusts the logged n; only ROUND_SEQUENCE RECORD)',
     recs + [EX()])

recs = HEAD() + keep_round(1, 'v0', 'v1') + keep_round(2, 'v1', 'v2')
v = var('r2-b', [J(1, 'variant'), J(2, 'variant')], 'kept')
recs += [rnd(2, 'v2', [v], 'r2-b', t0=20), ver('v3', 'v2', v, 2), EX()]
case('fn19_second_keep_in_round_2', 'false-negative',
     'Keep at most one (most support, then shorter, then first)',
     'round 2 is logged twice, each with a keep, and no resume between -> MULTI_KEEP (only RECORD ROUND_SEQUENCE)',
     recs)

recs = HEAD(budget={"rounds": 10, "minutes": 60, "tokens": None})
best = 'v0'
for n in (1, 2, 3, 4):
    recs += keep_round(n, best, 'v%d' % n, t0=(n - 1) * 10, t1=n * 10)
    best = 'v%d' % n
recs += [EX(), {"t": "resume", "at_round": 5, "reason": "human resumed"}]
for n, t in ((5, 0), (6, 10), (7, 20)):
    recs += keep_round(n, best, 'v%d' % n, t0=t, t1=t + 10)
    best = 'v%d' % n
case('fn20_clock_restart_hides_time_budget', 'false-negative',
     'Start a round only if one is left and remaining time ... cover twice the costliest round so far',
     'round times restart at 0 after a resume (t0 goes backwards); real elapsed >= 70 of 60 minutes -> BUDGET_START',
     recs + [EX()])

case('fn21_heldout_nonbool_counts_as_pass', 'false-negative',
     'the human runs the held-out judges (same pass/fail check, majority) ... / When unsure, fail closed',
     'heldout pass {"c3": "fail"} is counted as a pass -> COMPLETE; should be a failure or unauditable',
     HEAD('E1') + keep_round(1, 'v0', 'v1') + [chk('v1', 'E1'), HO(1, 'v1', {"c3": "fail"}), EX('COMPLETE', None)])

case('fn22_gap_waived_without_amend', 'false-negative',
     'A required `[OPEN]` -> **HALT(OPEN)** ... the human closes it with evidence the Verifier checks, or waives it by `amend`.',
     'a required gap flips to waived with no amend -> OPEN_AT_HELDOUT / OPEN_AT_COMPLETE',
     HEAD('E1') + keep_round(1, 'v0', 'v1') + [
         {"t": "substrate", "gap": "pilot data", "owner": "PI", "required": True, "status": "open"},
         {"t": "substrate", "gap": "pilot data", "owner": "PI", "required": True, "status": "waived"},
         chk('v1', 'E1'), HO(1, 'v1'), EX('COMPLETE', None)])

case('fn23_gap_status_case', 'false-negative',
     'A required `[OPEN]` -> **HALT(OPEN)** / When unsure, fail closed',
     'required gap with status "OPEN" is treated as closed -> COMPLETE accepted',
     HEAD('E1') + keep_round(1, 'v0', 'v1') + [
         {"t": "substrate", "gap": "pilot data", "owner": "PI", "required": True, "status": "OPEN"},
         chk('v1', 'E1'), HO(1, 'v1'), EX('COMPLETE', None)])

D3 = dict(copy.deepcopy(DONE), final_rung='E3')
case('fn24_final_rung_conflict', 'false-negative',
     '`DONE` ...: atomic pass/fail criteria ...; the final rung (default **E2**). / COMPLETE (final rung, held-out pass)',
     'DONE says final rung E3; a top-level setup.final_rung E1 silently overrides it -> COMPLETE at E1 accepted',
     [setup('E1', done=D3), V0, SETUP_CHECK, probe()] + keep_round(1, 'v0', 'v1') +
     [chk('v1', 'E1'), HO(1, 'v1'), EX('COMPLETE', None)])

case('fn25_escalation_without_boundary', 'false-negative',
     'All required pass -> Boundary. ... Below the final rung, **pause**: the human escalates or stops',
     'E1 Check fails c3 (no boundary reached) yet rung E2 is logged and the run completes at E2',
     HEAD('E2') + keep_round(1, 'v0', 'v1') + [chk('v1', 'E1', FAIL_C3), {"t": "rung", "name": "E2", "by": "human"},
                                               probe('E2'), chk('v1', 'E2'), HO(1, 'v1'), EX('COMPLETE', None)])

case('fn26_spare_set_first', 'false-negative',
     'the spares run only once a changed *best* passes Check',
     'held-out attempt 1 uses the spare set -> HELDOUT_REROLL (primary set never run)',
     HEAD('E1') + keep_round(1, 'v0', 'v1') + [chk('v1', 'E1'), HO(1, 'v1', s='spare'), EX('COMPLETE', None)])

v = var('r2-a', [J(1, 'tie'), J(2, 'tie'), J(3, 'tie')], 'kept', words=99, diff=[])
case('fn27_empty_diff_prune_launders_spare', 'false-negative',
     'each **one change to one section** / the spares run only once a changed *best* passes Check',
     'the "change" has an empty diff yet claims 99 < 100 words; v2 is v1 verbatim, so the spare runs on unchanged text',
     HEAD('E1') + keep_round(1, 'v0', 'v1') + [chk('v1', 'E1'), HO(1, 'v1', {"c3": False}),
                                               rnd(2, 'v1', [v], 'r2-a'), ver('v2', 'v1', v, 2), chk('v2', 'E1'),
                                               HO(2, 'v2', s='spare'), EX('COMPLETE', None)])

case('fn28_check_file_path_case', 'false-negative',
     'Never add, edit or delete check files',
     'kept diff edits "Tests/Test_Public.py" = setup check file tests/test_public.py on a case-insensitive FS -> CHECK_FILE_EDIT',
     [setup(check_files=["tests/test_public.py"]), V0, SETUP_CHECK, probe()] + keep_round(
         1, 'v0', 'v1', variant=var('r1-a', [J(1, 'variant'), J(2, 'variant')], 'kept',
                                    diff=[{"file": "Tests/Test_Public.py", "section": "test_a", "old": "assert x == 1",
                                           "new": "assert True"}])) + [EX()])

vs = [var('r1-%s' % s, [J(1, 'best', conf='high')], 'rejected') for s in 'abcde']
vk = var('r1-f', [J(1, 'variant'), J(2, 'variant')], 'kept',
         diff=[{"section": "Intro", "old": "a", "new": "b"}, {"section": "Method", "old": "c", "new": "d"}])
case('fn29_six_variants_two_sections', 'false-negative',
     '**Propose** 2 variants, each **one change to one section** of *best*',
     'six variants in one round and the kept one edits two sections; no finding, nothing unauditable',
     HEAD() + [rnd(1, 'v0', vs + [vk], 'r1-f'), ver('v1', 'v0', vk, 1), EX()])

IDEA = [{"section": "Aims", "old": "old aims", "new": "bold new aims"}]
r1 = var('r1-a', [J(1, 'best'), J(2, 'best')], 'rejected', diff=copy.deepcopy(IDEA))
r2 = var('r2-a', [J(1, 'variant'), J(2, 'variant')], 'kept', diff=copy.deepcopy(IDEA))
case('fn30_rejected_idea_reproposed', 'false-negative',
     'Skip ideas the ledger shows rejected by >=2 judges or twice by the screen, absent new evidence.',
     'round 2 re-proposes round 1\'s exact diff (rejected by 2 judges) with no new evidence and keeps it',
     HEAD() + [rnd(1, 'v0', [r1], None), rnd(2, 'v0', [r2], 'r2-a'), ver('v1', 'v0', r2, 2), EX()])

v = var('r1-a', [J(1, 'variant', orders=['best', 'variant', 'variant']), J(2, 'variant')], 'kept')
case('fn31_slot1_three_orders', 'false-negative',
     'Judge 1 compares in both orders (disagreement = UNKNOWN) / Never re-ask a returned verdict.',
     'slot 1 logs 3 orders whose first two disagree (UNKNOWN); the 3rd order is a re-ask; its "variant" is counted as support',
     HEAD() + [rnd(1, 'v0', [v], 'r1-a'), ver('v1', 'v0', v, 1), EX()])

recs = HEAD(budget={"rounds": 3.0, "minutes": 6000, "tokens": None})
best = 'v0'
for n in range(1, 6):
    recs += keep_round(n, best, 'v%d' % n)
    best = 'v%d' % n
case('fn32_budget_rounds_float', 'false-negative',
     'Start a round only if one is left',
     'budget.rounds = 3.0; 5 rounds run; no BUDGET_OVERRUN and the budget rule is not listed unauditable',
     recs + [EX()])

recs = HEAD() + [stall_round(i, 'v0') for i in (1, 2, 3)]
UNCHK = dict(ALLPASS, c3={"kind": "judges", "value": "unchecked", "votes": ["pass", "ERROR", "ERROR"]})
recs += [chk('v0', 'E1', UNCHK, 'stall')] + [stall_round(i, 'v0') for i in range(4, 10)] + [EX()]
case('fn33_stall_with_unchecked_runs_on', 'false-negative',
     'All required pass -> Boundary. Failing while stalled -> **HALT(STALL)**',
     'the stall Check leaves required c3 unchecked (not pass); rounds 4-9 run with no halt and no finding',
     recs)

case('fn34_gap_closed_without_evidence', 'false-negative',
     'the human closes it with evidence the Verifier checks, or waives it by `amend`.',
     'a required gap is marked closed with no evidence and no Verifier citation -> OPEN_AT_HELDOUT / OPEN_AT_COMPLETE',
     HEAD('E1') + keep_round(1, 'v0', 'v1') + [
         {"t": "substrate", "gap": "pilot data", "owner": "PI", "required": True, "status": "open"},
         {"t": "substrate", "gap": "pilot data", "owner": "PI", "required": True, "status": "closed"},
         chk('v1', 'E1'), HO(1, 'v1'), EX('COMPLETE', None)])

# ------------------------------------------------------------------ false positives
recs = HEAD() + [stall_round(i, 'v0') for i in (1, 2, 3)] + [chk('v0', 'E1', UNCHK, 'stall'), EX('PARTIAL', 'STALL')]
case('fp01_halt_stall_on_unchecked', 'false-positive',
     'Retry an ERROR once, then ... leave its criterion unchecked. / Failing while stalled -> **HALT(STALL)**, naming what each failing criterion needs',
     'honest HALT(STALL): 3 stalls, the Check leaves required c3 unchecked after judge ERRORs; no violation expected',
     recs)

va = var('r1-a', [J(1, 'best', conf='high')], 'dropped')
vb = var('r1-b', [J(1, 'variant'), J(2, 'variant')], 'kept')
case('fp02_early_drop_logged_dropped', 'false-positive',
     'if it prefers *best* with high confidence or on a protected item, drop the variant.',
     'judge 1 prefers best with high confidence; the loop "drops" it as step 3 says; no violation expected',
     HEAD() + [rnd(1, 'v0', [va, vb], 'r1-b'), ver('v1', 'v0', vb, 1), EX()])

def objection_error(n):
    return rnd(n, 'v0', [var('r%d-%s' % (n, s), [J(1, 'best'), J(2, 'ERROR', retries=1)], 'dropped') for s in 'ab'], None)
case('fp03_error_after_objection_halt_error', 'false-positive',
     'Retry an ERROR once, then drop the variant (not a rejection) ... / unless every variant ended ERROR (two such in a row -> **HALT(ERROR)**)',
     'every variant ends with judge 2 ERROR after one retry -> dropped; two such rounds -> HALT(ERROR); no violation expected',
     HEAD() + [objection_error(1), objection_error(2), EX('PARTIAL', 'ERROR')])

C3OPT_FAIL = dict(ALLPASS, c3={"kind": "judges", "value": "fail", "votes": ["pass", "fail", "fail"]})
case('fp04_skill_schema_amend', 'false-positive',
     'only a human-approved `amend{what,why}` changes either. / Memory: `amend{what,why}`',
     'a SKILL-schema amend (what/why, no machine DONE) makes c3 optional; c3 then fails, required c1/c2 pass, held-out passes, COMPLETE',
     HEAD('E1') + keep_round(1, 'v0', 'v1') + [chk('v1', 'E1', FAIL_C3),
                                               {"t": "amend", "what": "c3 becomes optional (required: false)",
                                                "why": "human decision: judges criterion is advisory", "by": "human"},
                                               chk('v1', 'E1', C3OPT_FAIL), HO(1, 'v1'), EX('COMPLETE', None)])

good = HEAD('E1') + keep_round(1, 'v0', 'v1') + [chk('v1', 'E1'), HO(1, 'v1'), EX('COMPLETE', None)]
case('fp05_utf8_bom', 'false-positive',
     'MEMORY: append-only `archive.jsonl`.',
     'a valid COMPLETE archive saved with a UTF-8 BOM (Windows PowerShell 5.1 Out-File -Encoding utf8); expected ok, exit 0',
     raw='﻿' + ''.join(json.dumps(r) + '\n' for r in good))
case('fp05b_same_without_bom', 'control', 'control', 'same records as fp05 without the BOM', good)

v = var('r1-a', [J(1, 'variant'), J(2, 'variant'), J(3, 'tie')], 'rejected')
case('fp06_voluntary_strict', 'false-positive',
     '**When unsure, fail closed**: don\'t keep, don\'t pass / Strict mode: all 3, no early drop.',
     'the loop (fail-closed, or at the human\'s request) runs E1 in strict mode though the probe was clean and declines a 2/3 keep',
     [setup(), V0, SETUP_CHECK, probe(mode='strict'), rnd(1, 'v0', [v], None), EX()])

case('fp07_human_pause_counts_as_budget', 'false-positive',
     'Below the final rung, **pause**: the human escalates or stops / BUDGET: max rounds and time',
     'the human takes 12 hours to escalate at the E1 boundary; loop work so far is 5 of 600 minutes; the next round is flagged',
     HEAD() + keep_round(1, 'v0', 'v1') + [chk('v1', 'E1'), {"t": "rung", "name": "E2", "by": "human"}, probe('E2')] +
     keep_round(2, 'v1', 'v2', t0=725, t1=730) + [EX()])

case('fp08_citation_mixed_criterion_field', 'false-positive',
     'contradicted -> strip / Memory: `citation{claim,locator,status}`',
     'a contradicted claim for c2 was stripped (its citation carries an extra criterion field); c2 passes on the verified claims logged per the SKILL schema',
     HEAD() + [{"t": "citation", "claim": "rate is 12%", "locator": "report.pdf p4", "status": "contradicted", "criterion": "c2"}] +
     keep_round(1, 'v0', 'v1') + [{"t": "citation", "claim": "n=40", "locator": "grounding.md s2", "status": "verified"},
                                  chk('v1', 'E1'), EX()])

v = var('r1-a', [J(1, 'variant'), J(2, 'variant', retries="0")], 'kept')
case('fp09_malformed_retries_string', 'false-positive',
     'Missing fields make a rule unauditable, never violated (blueprint P22) / checker docstring: a malformed field: that record is unauditable',
     'retries logged as the string "0": the round should be unauditable; instead its version becomes a VIOLATION',
     HEAD() + [rnd(1, 'v0', [v], 'r1-a'), ver('v1', 'v0', v, 1)] + keep_round(2, 'v1', 'v2') + [EX()])

va = var('r1-a', [J(1, 'variant'), J(2, 'variant')], 'rejected')
del va['words']
vb = var('r1-b', [J(1, 'variant'), J(2, 'variant')], 'kept', words=80)
case('fp10_selection_missing_words', 'false-positive',
     'Keep at most one (most support, then shorter, then first) / a rule whose inputs are missing is unauditable',
     'r1-a has no words; which variant is shorter is unknown, yet keeping r1-b is a WRONG_SELECTION VIOLATION',
     HEAD() + [rnd(1, 'v0', [va, vb], 'r1-b'), ver('v1', 'v0', vb, 1), EX()])

S1A, S1B = "The loop keeps one change per round.", "The loop keeps at most one change per round, chosen by support."
o1 = var('r1-a', [J(1, 'variant'), J(2, 'variant')], 'kept', section='S1', diff=[{"section": "S1", "old": S1A, "new": S1B}])
o2 = var('r2-a', [J(1, 'variant'), J(2, 'variant')], 'kept', section='S1', diff=[{"section": "S1", "old": S1B, "new": S1A}])
case('fp11a_oscillation_human_picks_old_best', 'false-positive',
     'If it (nearly) restores an earlier *best*\'s section -> **HALT(OSCILLATION)**: the human picks.',
     'after HALT(OSCILLATION) the human picks v1 over v2; the next round starts from v1 -> STALE_PARENT',
     HEAD() + [rnd(1, 'v0', [o1], 'r1-a'), ver('v1', 'v0', o1, 1), rnd(2, 'v1', [o2], 'r2-a'), ver('v2', 'v1', o2, 2),
               EX('PARTIAL', 'OSCILLATION'), {"t": "resume", "at_round": 3, "reason": "human picked v1"}] +
     keep_round(3, 'v1', 'v3') + [EX()])
case('fp11b_oscillation_human_picks_variant', 'false-positive',
     'If it (nearly) restores an earlier *best*\'s section -> **HALT(OSCILLATION)**: the human picks.',
     'HALT(OSCILLATION) before the version is written; the human picks the variant, so its version is logged after resume -> VERSION_WITHOUT_KEEP',
     HEAD() + [rnd(1, 'v0', [o1], 'r1-a'), ver('v1', 'v0', o1, 1), rnd(2, 'v1', [o2], 'r2-a'),
               EX('PARTIAL', 'OSCILLATION'), {"t": "resume", "at_round": 3, "reason": "human picked r2-a"},
               ver('v2', 'v1', o2, 2)] + keep_round(3, 'v2', 'v3') + [EX()])

case('fp12_e3_amend_after_rung', 'false-positive',
     '**E3** a second objective the human adds by `amend`. On escalation: log the rung, rerun the probe, reset the stall count.',
     'rung E3 is logged first, then the amend adding the objective, then the probe; E3_WITHOUT_AMEND expected absent',
     HEAD('E3') + keep_round(1, 'v0', 'v1') + [chk('v1', 'E1'), {"t": "rung", "name": "E2", "by": "human"}, probe('E2'),
                                               chk('v1', 'E2'), {"t": "rung", "name": "E3", "by": "human"}, AMEND4,
                                               probe('E3'), EX()])

G0 = ("Aim: test whether the loop improves grant proposals under adversarial review. It keeps at most one change "
      "per round, logs every verdict with its model family, and stops when the held-out judges pass or the budget "
      "of ten rounds is spent. Results are reported per criterion with how each was decided.")
G1 = G0.replace("grant proposals", "research proposals")
G2 = G1.replace("ten rounds", "twelve rounds")
g1 = var('r1-a', [J(1, 'variant'), J(2, 'variant')], 'kept', section='Aims', diff=[{"section": "Aims", "old": G0, "new": G1}])
g2 = var('r2-a', [J(1, 'variant'), J(2, 'variant')], 'kept', section='Aims', diff=[{"section": "Aims", "old": G1, "new": G2}])
case('fp13_two_small_edits_as_oscillation', 'false-positive',
     'If it (nearly) restores an earlier *best*\'s section -> **HALT(OSCILLATION)**',
     'two keeps each change a different phrase of Aims (grant->research, ten->twelve); nothing is restored; expected no oscillation advisory, next_due round',
     HEAD() + [rnd(1, 'v0', [g1], 'r1-a'), ver('v1', 'v0', g1, 1), rnd(2, 'v1', [g2], 'r2-a'), ver('v2', 'v1', g2, 2),
               EX()])

v = var('r1-a', [J(1, 'variant'), J(2, 'variant')], 'kept')
vr = ver('v1', 'v0', v, 1)
vr['diff'][0]['file'] = 'proposal.md'
case('fp14_version_diff_adds_file_key', 'false-positive',
     'apply exactly the judged text / Memory: `version{id,parent,diff}`',
     'the version diff carries the same section/old/new text plus a file name; the text applied is exactly the judged text',
     HEAD() + [rnd(1, 'v0', [v], 'r1-a'), vr, EX()])

# ------------------------------------------------------------------ malformed input (crashes)
case('cr01_v2_resume_unfinished', 'crash',
     'P22: v2 records ... rules are unauditable, never violated, never a crash',
     'v2 archive: a kept variant with no version, then a resume (a round unfinished at a crash)',
     [{"t": "version", "id": "v0", "parent": None, "change": "initial draft"},
      {"t": "variant", "round": 1, "id": "r1-a", "section": "Intro", "screen": "pass", "verdicts": ["B/high", "B/med"], "kept": True},
      {"t": "resume", "at_round": 1, "reason": "crash"}])
case('cr02_second_setup_record', 'crash',
     'Resume from MEMORY if present: ... log `resume`',
     'a (wrong) second setup record without t0 after a timed round; expected a finding or unauditable, not a crash',
     HEAD() + keep_round(1, 'v0', 'v1') + [setup()])
case('cr03_target_nonstring_check_file', 'crash',
     'checker docstring: --target DIR hashes setup.check_files',
     'check_files holds a list; audit --target should list it unauditable, not crash',
     [setup(check_files=[["tests", "t.py"]], check_hashes={"tests/t.py": "0" * 64}), V0, SETUP_CHECK, probe(), EX()],
     args={"target": "."})
case('cr04_deep_nesting_torn_tail', 'crash',
     'set aside a torn last line',
     'last line is unparsable garbage (deeply nested brackets, never closed); expected torn_tail, not a crash',
     raw=''.join(json.dumps(r) + '\n' for r in HEAD()) + '[' * 200000)
case('cr05_pending_not_object', 'crash',
     'checker docstring: --pending audits a not-yet-logged round',
     '--pending file is a JSON list; expected a usage error message, got a caught exception',
     HEAD() + keep_round(1, 'v0', 'v1'), args={"pending": "cr05_pending.json"})


# ------------------------------------------------------------------ controls: the same violation without the evasion
def first(recs, t, **kw):
    return next(r for r in recs if r.get('t') == t and all(r.get(k) == x for k, x in kw.items()))


def ctl(src, fn, want):
    recs = copy.deepcopy(A[src]['records'])
    recs = fn(recs) or recs
    case('ctl_' + src, 'control', A[src]['rule'], 'control for %s; checker should report %s' % (src, want), recs,
         args=A[src]['args'])


def pop_verdict(slot_idx):
    def f(recs):
        first(recs, 'round', n=1)['variants'][0]['verdicts'].pop(slot_idx)
    return f


ctl('fn01_duplicate_slot_reask', pop_verdict(2), 'KEEP_VETOED')
ctl('fn02_fourth_judge_support', pop_verdict(3), 'KEEP_WITHOUT_SUPPORT')
ctl('fn03_strict_fourth_judge', pop_verdict(3), 'STRICT_KEEP')
ctl('fn04_probe_reroll', lambda r: [x for x in r if not (x['t'] == 'probe' and x['mode'] == 'normal')], 'STRICT_KEEP')
ctl('fn06_setup_check_launders_regression',
    lambda r: [x for x in r if not (x['t'] == 'check' and x['results'].get('c1', {}).get('value') == 'fail')],
    'REGRESSION_KEPT')
ctl('fn07_setup_check_evades_stall',
    lambda r: [dict(x, trigger='stall') if x['t'] == 'check' and 'c2' in x['results'] and
               x['results']['c2']['value'] == 'fail' else x for x in r], 'STALL_HALT_MISSED')
ctl('fn10_unknown_slot_rates_protected_worse',
    lambda r: first(r, 'round', n=1)['variants'][0]['verdicts'][1].update(overall='tie'), 'KEEP_VETOED')
ctl('fn11_same_rung_resets_stall', lambda r: [x for x in r if x['t'] != 'rung'], 'MISSED_CHECK')
ctl('fn12_check_extra_votes',
    lambda r: first(r, 'check', version='v1')['results']['c3'].update(votes=['fail', 'fail', 'pass']), 'CHECK_MISCOUNT')
ctl('fn14_noop_amend_rerolls_check', lambda r: [x for x in r if x['t'] != 'amend'], 'RECHECK_UNCHANGED')
ctl('fn15_noop_amend_cancels_halt_error', lambda r: [x for x in r if x['t'] != 'amend'], 'ERROR_HALT_MISSED')
ctl('fn17_version_id_reuse',
    lambda r: [dict(x, id='v2') if x['t'] == 'version' and x.get('round') == 2 else x for x in r], 'FALSE_COMPLETE')


def renumber(recs):
    k = 0
    for x in recs:
        if x['t'] == 'round':
            k += 1
            x['n'] = k
ctl('fn18_round_number_reuse_hides_budget', renumber, 'BUDGET_OVERRUN')


def monotone(recs):
    k = 0
    for x in recs:
        if x['t'] == 'round':
            x['t0'], x['t1'], k = k * 10, k * 10 + 10, k + 1
ctl('fn20_clock_restart_hides_time_budget', monotone, 'BUDGET_START')
ctl('fn21_heldout_nonbool_counts_as_pass', lambda r: first(r, 'heldout').update({'pass': {"c3": False}}),
    'FALSE_COMPLETE')
ctl('fn22_gap_waived_without_amend', lambda r: [x for x in r if x.get('status') != 'waived'],
    'OPEN_AT_HELDOUT + OPEN_AT_COMPLETE')
ctl('fn23_gap_status_case', lambda r: first(r, 'substrate').update(status='open'), 'OPEN_AT_HELDOUT + OPEN_AT_COMPLETE')
ctl('fn24_final_rung_conflict', lambda r: first(r, 'setup').pop('final_rung') and None, 'FALSE_COMPLETE')
ctl('fn28_check_file_path_case',
    lambda r: first(r, 'round', n=1)['variants'][0]['diff'][0].update(file='tests/test_public.py') or
    first(r, 'version', id='v1')['diff'][0].update(file='tests/test_public.py'), 'CHECK_FILE_EDIT')
ctl('fn32_budget_rounds_float', lambda r: first(r, 'setup')['budget'].update(rounds=3), 'BUDGET_OVERRUN')


def write_all():
    for name, c in A.items():
        path = os.path.join(HERE, name + '.jsonl')
        text = c['raw'] if c['raw'] is not None else ''.join(json.dumps(r) + '\n' for r in c['records'])
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)
    with open(os.path.join(HERE, 'cr05_pending.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump([{"t": "round"}], f)


def run(name):
    c, path = A[name], os.path.join(HERE, name + '.jsonl')
    cmd = [sys.executable, CHECKER, 'audit', path]
    for k, val in c['args'].items():
        cmd += ['--' + k, os.path.join(HERE, val) if k != 'target' else HERE]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    try:
        out = json.loads(p.stdout)
    except ValueError:
        out = {'raw_stdout': p.stdout[-400:], 'stderr': p.stderr[-800:]}
    return p.returncode, out


if __name__ == '__main__':
    write_all()
    full = '--json' in sys.argv
    for name in A:
        code, out = run(name)
        if full:
            print(json.dumps({'archive': name, 'exit': code, 'out': out}, ensure_ascii=True))
            continue
        codes = [(f['code'], f['class'][0], f['record_index']) for f in out.get('violations', [])]
        un = sorted({u['rule'] for u in out.get('unauditable', [])})
        st = out.get('state', {})
        print('%-44s exit=%s ok=%s codes=%s unaud=%s status=%s next=%s err=%s' % (
            name, code, out.get('ok'), codes, un, st.get('status'), st.get('next_due'),
            (out.get('error') or out.get('integrity') or '')))
