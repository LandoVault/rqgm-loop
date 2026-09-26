#!/usr/bin/env python3
"""Round-2 adversarial archives for skills/rqgm-loop/rqgm_check.py (read-only test input; never edits the checker).

  python gen_round2.py            write every archive next to this file, run 'audit' on each, print a summary
  python gen_round2.py --json     same, but print the full checker output for every archive

Naming: aNN_* = v3 archive violating a SKILL.md rule (checker should report a VIOLATION);
        bNN_* = valid v3 archive (checker should report no VIOLATION);
        cNN_* = malformed input (checker should degrade to unauditable/integrity, never crash);
        k*    = control: same archive with the evasion removed (shows the rule is otherwise enforced).
Helpers (setup, var, J, rnd, ...) are imported from ../gen_attacks.py, which writes nothing on import.
"""
import copy, importlib.util, json, os, subprocess, sys  # noqa: E401

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
CHECKER = os.path.join(REPO, 'skills', 'rqgm-loop', 'rqgm_check.py')
_spec = importlib.util.spec_from_file_location('gen_attacks', os.path.join(HERE, '..', 'gen_attacks.py'))
G = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(G)
setup, V0, SETUP_CHECK, probe, J, var, rnd, ver, chk = G.setup, G.V0, G.SETUP_CHECK, G.probe, G.J, G.var, G.rnd, G.ver, G.chk
keep_round, stall_round, err_round, HEAD, EX, HO = G.keep_round, G.stall_round, G.err_round, G.HEAD, G.EX, G.HO
DONE, ALLPASS, FAIL_C3 = G.DONE, G.ALLPASS, G.FAIL_C3

A = {}


def case(name, direction, rule, expect, records=None, raw=None, args=None):
    A[name] = dict(records=records, raw=raw, args=args or {}, direction=direction, rule=rule, expect=expect)


def kv(**gates):  # a 2/2 keep with custom gates
    return var('r1-a', [J(1, 'variant'), J(2, 'variant')], 'kept', gates=gates)


def one_keep(v, tail=None):
    return HEAD() + [rnd(1, 'v0', [v], v['id']), ver('v1', 'v0', v, 1)] + (tail or [EX()])


GOOD = HEAD('E1') + keep_round(1, 'v0', 'v1') + [chk('v1', 'E1'), HO(1, 'v1'), EX('COMPLETE', None)]

# ================================================================== (a) false negatives: gates
case('a01_screen_unknown', 'false-negative',
     'The **Screen** rejects ... / UNKNOWN is never a tie, pass or support.',
     'screen returned UNKNOWN; the variant is kept as if the Screen passed (no finding, nothing unauditable)',
     one_keep(kv(apply='ok', commands={'c1': 'pass'}, verifier=[], screen='UNKNOWN')))
case('a02_screen_rejected_capitalised', 'false-negative',
     'The **Screen** rejects rubric echo, mechanism-free compliance claims, text aimed at judges, ...',
     'screen "Rejected: rubric echo" (capital R) is read as a pass; the variant is kept -> GATE_KEPT expected',
     one_keep(kv(apply='ok', commands={'c1': 'pass'}, verifier=[], screen='Rejected: rubric echo')))
case('k02_screen_rejected_lower', 'control', 'control', 'same with "rejected: rubric echo" -> GATE_KEPT',
     one_keep(kv(apply='ok', commands={'c1': 'pass'}, verifier=[], screen='rejected: rubric echo')))
case('a03_command_FAIL_uppercase', 'false-negative',
     'Failing a command *best* passes rejects the variant; a failure *best* shares does not.',
     'best passes c1 (setup Check); the kept variant logs c1 "FAIL" -> REGRESSION_KEPT expected',
     one_keep(kv(apply='ok', commands={'c1': 'FAIL'}, verifier=[], screen='pass')))
case('a04_command_exit_code', 'false-negative',
     'Failing a command *best* passes rejects the variant; a failure *best* shares does not.',
     'c1 logged as its exit status 1 (a failure); best passes c1; the variant is kept -> REGRESSION_KEPT expected',
     one_keep(kv(apply='ok', commands={'c1': 1}, verifier=[], screen='pass')))
case('k04_command_fail', 'control', 'control', 'same with c1 "fail" -> REGRESSION_KEPT',
     one_keep(kv(apply='ok', commands={'c1': 'fail'}, verifier=[], screen='pass')))
case('a05_apply_synonym_skips_gate', 'false-negative',
     'Apply the diff to a fresh copy (check files as at setup); run every command there yourself / The **Screen** rejects ...',
     'apply "applied" (not "ok"), commands {} and no screen: fn08+fn09 again, but one synonym turns the whole gate into '
     '"unauditable" and the keep is credited',
     one_keep(kv(apply='applied', commands={}, verifier=[])))
case('a06_verifier_error_kept', 'false-negative',
     'Each result is a verdict, **UNKNOWN** or **ERROR** (... unrunnable check). Retry an ERROR once, then drop the variant',
     'the Verifier ERRORed (after its retry) yet the variant is kept; gates.verifier is never read -> should be dropped',
     one_keep(kv(apply='ok', commands={'c1': 'pass'}, verifier='ERROR', screen='pass', retries={'verifier': 1})))
case('a07_verifier_absent_v3', 'false-negative',
     'The **Verifier** checks each new claim against a primary source it read / Memory: gates:{apply,commands,verifier,screen}',
     'v3 archive, gates has no verifier key: the same fail-closed rule that made fn09 (no screen) RECORD_MISSING does not fire',
     one_keep(kv(apply='ok', commands={'c1': 'pass'}, screen='pass')))

# ================================================================== (a) judges / retries / verdict values
def err0(n):
    return rnd(n, 'v0', [var('r%d-%s' % (n, s), [J(1, 'ERROR', retries=0)], 'dropped') for s in 'ab'], None)
case('a08_error_never_retried', 'false-negative',
     'Retry an ERROR once, then drop the variant (not a rejection)',
     'every judge ERROR logs retries 0 (never retried); the loop drops all variants and halts HALT(ERROR); no finding',
     HEAD() + [err0(1), err0(2), EX('PARTIAL', 'ERROR')])
v = var('r1-a', [J(1, 'variant'), J(2, 'UNKNOWN', criteria={'c2': 'Best'}), J(3, 'variant')], 'kept')
case('a09_protected_rated_Best_case', 'false-negative',
     'none rates a **protected** item worse (guardrails, must-not-change constraints, criteria *best* passes)',
     'slot 2 rates c2 (passed by best) "Best"; case-sensitive compare ignores it -> KEEP_VETOED expected',
     one_keep(v))
v = var('r1-a', [J(1, 'variant'), J(2, 'UNKNOWN', criteria={'c2': 'best'}), J(3, 'variant')], 'kept')
case('k09_protected_rated_best', 'control', 'control', 'same with "best" -> KEEP_VETOED', one_keep(v))
v = var('r1-a', [J(1, 'Best', conf='high', orders=['best', 'best']), J(2, 'variant'), J(3, 'variant')], 'kept')
case('a10_judge1_Best_high_kept', 'false-negative',
     'if it prefers *best* with high confidence or on a protected item, reject the variant.',
     'judge 1 prefers best (logged "Best") with high confidence; the variant is kept; one mis-cased value makes the '
     'whole panel unauditable and the keep is not flagged',
     one_keep(v))
v = var('r1-a', [J(1, 'variant'), J(2, 'variant'), dict(J(3, 'best'), slot='3')], 'kept')
case('a11_slot_string_hides_objection', 'false-negative',
     'Keep a variant if >=2 judges prefer it (strict: 3), none prefers *best*',
     'judge 3 ran and preferred best; its slot is logged "3" (string) and discarded as an extra verdict -> KEEP_VETOED expected',
     one_keep(v))
MNC_OBJ = dict(copy.deepcopy(DONE), must_not_change=[{'id': 'm1', 'text': 'Total budget stays at $50k'}])
MNC_MAP = dict(copy.deepcopy(DONE), must_not_change={'m1': 'Total budget stays at $50k'})
v = var('r1-a', [J(1, 'variant'), J(2, 'variant', criteria={'m1': 'best'}), J(3, 'variant')], 'kept')
case('a12_must_not_change_objects', 'false-negative',
     'none rates a **protected** item worse (guardrails, must-not-change constraints, ...) / `must_not_change` constraints `{id:text}`',
     'must_not_change logged as [{"id","text"}]; slot 2 rates m1 worse; the constraint is silently not protected',
     [setup(done=MNC_OBJ), V0, SETUP_CHECK, probe(), rnd(1, 'v0', [v], 'r1-a'), ver('v1', 'v0', v, 1), EX()])
case('k12_must_not_change_map', 'control', 'control', 'same with {id:text} map -> KEEP_VETOED',
     [setup(done=MNC_MAP), V0, SETUP_CHECK, probe(), rnd(1, 'v0', [v], 'r1-a'), ver('v1', 'v0', v, 1), EX()])
PR = probe()
PR['seeded']['criterion'] = 'c1'
v = var('r1-a', [J(1, 'variant'), J(2, 'variant')], 'kept')
case('a13_probe_seeded_command_criterion', 'false-negative',
     'a copy you (not the generator) seeded with one defect against a named `judges` criterion',
     'the defect was seeded against c1 (a command criterion); normal mode is credited and a 2/2 keep passes',
     [setup(), V0, SETUP_CHECK, PR, rnd(1, 'v0', [v], 'r1-a'), ver('v1', 'v0', v, 1), EX()])

# ================================================================== (a) kept text / check files / words
TESTF = 'tests/test_public.py'
UDIFF_J = ('--- a/tests/test_public.py\n+++ b/tests/test_public.py\n@@ -3 +3 @@\n-    assert score(p) >= 0.8\n'
           '+    assert True\n')
UDIFF_A = '--- a/proposal.md\n+++ b/proposal.md\n@@ -9 +9 @@\n-We target n=40.\n+We guarantee funding.\n'
v = var('r1-a', [J(1, 'variant'), J(2, 'variant')], 'kept', diff=UDIFF_J)
vr = dict(ver('v1', 'v0', v, 1), diff=UDIFF_A)
case('a14_unified_diff_string', 'false-negative',
     'Never add, edit or delete check files / apply exactly the judged text',
     'diffs logged as unified-diff strings: the judged diff edits check file tests/test_public.py and the applied version '
     'is different text; diffs() maps any string to [] so no CHECK_FILE_EDIT, no KEPT_TEXT_MISMATCH, nothing unauditable',
     [setup(check_files=[TESTF]), V0, SETUP_CHECK, probe(), rnd(1, 'v0', [v], 'r1-a'), vr, EX()])
D = [{'section': 'test_score', 'old': 'assert score(p) >= 0.8', 'new': 'assert True'}]
v = var('r1-a', [J(1, 'variant'), J(2, 'variant')], 'kept', diff=copy.deepcopy(D))
vr = ver('v1', 'v0', v, 1)
vr['diff'][0]['file'] = TESTF
case('a15_version_adds_check_file', 'false-negative',
     'Never add, edit or delete check files / apply exactly the judged text',
     'the judged diff names no file; the version applies it to check file tests/test_public.py; file is compared only when '
     'both name one and CHECK_FILE_EDIT reads only the variant diff',
     [setup(check_files=[TESTF]), V0, SETUP_CHECK, probe(), rnd(1, 'v0', [v], 'r1-a'), vr, EX()])
DONE_F = copy.deepcopy(DONE)
DONE_F['criteria'][0].update(command='pytest tests/test_public.py', files=[TESTF])
v = var('r1-a', [J(1, 'variant'), J(2, 'variant')], 'kept', diff=[dict(D[0], file=TESTF)])
case('a16_check_file_declared_in_DONE', 'false-negative',
     'Files a command runs belong to `DONE`. / Never add, edit or delete check files',
     'schema-conformant setup (no checker-only setup.check_files); DONE c1 names tests/test_public.py; the kept diff edits '
     'it; CHECK_FILE_EDIT silently never runs (not even listed unauditable)',
     [setup(done=DONE_F), V0, SETUP_CHECK, probe(), rnd(1, 'v0', [v], 'r1-a'), ver('v1', 'v0', v, 1), EX()])
v = var('r1-a', [J(1, 'tie'), J(2, 'tie'), J(3, 'tie')], 'kept', words=90)
vr = dict(ver('v1', 'v0', v, 1), words=120)
case('a17_prune_words_split_records', 'false-negative',
     'A shorter variant is also kept if all 3 judges completed without UNKNOWN ... / apply exactly the judged text',
     'all-tie prune keep on variant.words 90 < 100, but the applied version logs 120 words (longer than best); '
     'the two records are never cross-checked',
     HEAD() + [rnd(1, 'v0', [v], 'r1-a'), vr, EX()])
v = var('r2-a', [J(1, 'variant'), J(2, 'variant')], 'kept',
        diff=[{'section': 'Aims', 'old': 'We aim to cut review time by 30%.', 'new': 'We aim to cut review time by 30%.'}])
case('a18_noop_diff_launders_spare', 'false-negative',
     'the spares run only once a changed *best* passes Check / A Check or held-out result stands until *best* ... changes',
     'fn27 fixed only diff == []; a diff whose new == old is also no change, yet v2 gets a fresh Check and the spare set',
     HEAD('E1') + keep_round(1, 'v0', 'v1') + [chk('v1', 'E1'), HO(1, 'v1', {'c3': False}), rnd(2, 'v1', [v], 'r2-a'),
                                               ver('v2', 'v1', v, 2), chk('v2', 'E1'), HO(2, 'v2', s='spare'),
                                               EX('COMPLETE', None)])
ROOT2 = {'t': 'version', 'id': 'v0b', 'parent': None, 'round': 0, 'words': 60,
         'diff': [{'section': 'Aims', 'old': 'original aims', 'new': 'rewritten aims, never judged'}]}
case('a19_second_root_version', 'false-negative',
     '**v0** = `TARGET` (draft if absent) = *best* / Keep a variant if >=2 judges prefer it',
     'a second parentless version before round 1 replaces best with unjudged text; it then passes Check and COMPLETE',
     HEAD('E1') + [ROOT2, chk('v0b', 'E1'), HO(1, 'v0b'), EX('COMPLETE', None)])

# ================================================================== (a) Check / held-out / exit / gaps
def with_c3(c3):
    return HEAD('E1') + keep_round(1, 'v0', 'v1') + [chk('v1', 'E1', dict(ALLPASS, c3=c3)), HO(1, 'v1'),
                                                     EX('COMPLETE', None)]
case('a20_votes_null', 'false-negative',
     'with 3 fresh judges per `judges` criterion (majority; strict: 3/3) / When unsure, fail closed',
     'c3 pass with "votes": null; the stated v3 rule ("absent or empty" -> RECORD_MISSING, pass not credited) does not fire',
     with_c3({'kind': 'judges', 'value': 'pass', 'votes': None}))
case('a21_votes_as_object', 'false-negative',
     'with 3 fresh judges per `judges` criterion (majority; strict: 3/3)',
     'votes logged as {judge: vote} with 2 fails and 1 pass; value pass is credited -> CHECK_MISCOUNT expected',
     with_c3({'kind': 'judges', 'value': 'pass', 'votes': {'j1': 'fail', 'j2': 'fail', 'j3': 'pass'}}))
case('k21_votes_list', 'control', 'control', 'same votes as a list -> CHECK_MISCOUNT',
     with_c3({'kind': 'judges', 'value': 'pass', 'votes': ['fail', 'fail', 'pass']}))
DONE_K = copy.deepcopy(DONE)
for c, k in zip(DONE_K['criteria'], ('Command', 'Source', 'Judges')):
    c['kind'] = k
v = var('r1-a', [J(1, 'variant'), J(2, 'variant')], 'kept', commands={})
case('a22_done_kind_capitalised', 'false-negative',
     'kind: `command` (you run it; it decides), `source` (the Verifier checks it) or `judges` / run every command there yourself '
     '/ 3 fresh judges per `judges` criterion (majority)',
     'DONE kinds "Command"/"Judges": c1 is never run at the gate and c3 passes on 1 of 3 votes; no finding, nothing unauditable',
     [setup('E1', done=DONE_K), V0, SETUP_CHECK, probe(), rnd(1, 'v0', [v], 'r1-a'), ver('v1', 'v0', v, 1),
      chk('v1', 'E1', dict(ALLPASS, c3={'kind': 'judges', 'value': 'pass', 'votes': ['fail', 'fail', 'pass']})),
      HO(1, 'v1'), EX('COMPLETE', None)])
DONE_N = {'criteria': [{'id': 'c1', 'required': True, 'command': 'pytest -q'}, {'id': 'c2', 'required': True},
                       {'id': 'c3', 'required': True}], 'must_not_change': []}
case('a23_done_kind_absent', 'false-negative',
     'atomic pass/fail criteria `{id,required,kind,guardrail?}` / run every command there yourself / When unsure, fail closed',
     'v3 DONE criteria carry no kind (schema field without "?"): c1 is never run at the gate and c3 passes with no votes',
     [setup('E1', done=DONE_N), V0, dict(SETUP_CHECK, results={'c1': {'value': 'pass'}, 'c2': {'value': 'pass'}}), probe(),
      rnd(1, 'v0', [v], 'r1-a'), ver('v1', 'v0', v, 1),
      chk('v1', 'E1', {'c1': {'value': 'pass'}, 'c2': {'value': 'pass'}, 'c3': {'value': 'pass'}}),
      HO(1, 'v1'), EX('COMPLETE', None)])
GAP = {'t': 'substrate', 'gap': 'pilot data', 'owner': 'PI', 'required': True, 'status': 'open'}
case('a24_gap_required_flipped', 'false-negative',
     'A required `[OPEN]` -> **HALT(OPEN)**: ... the human closes it with evidence the Verifier checks, or waives it by `amend`.',
     'a required open gap is re-logged required:false (still open) with no amend; COMPLETE is accepted',
     HEAD('E1') + keep_round(1, 'v0', 'v1') + [GAP, dict(GAP, required=False), chk('v1', 'E1'), HO(1, 'v1'),
                                               EX('COMPLETE', None)])
v = var('r1-a', [J(1, 'variant'), J(2, 'variant')], 'kept',
        diff=[{'section': 'Pilot', 'old': 'We will recruit participants.',
               'new': 'We will recruit [OPEN: pilot sample size and source needed] participants.'}])
case('a25_open_marker_unlogged', 'false-negative',
     'Log the round, any `version` and `substrate` / A required `[OPEN]` -> **HALT(OPEN)** / When unsure, fail closed',
     'the kept text (version diff) writes an [OPEN] into best; no substrate record; COMPLETE credited',
     HEAD('E1') + [rnd(1, 'v0', [v], 'r1-a'), ver('v1', 'v0', v, 1), chk('v1', 'E1'), HO(1, 'v1'), EX('COMPLETE', None)])
case('a26_heldout_attempt1_spares', 'false-negative',
     'the spares run only once a changed *best* passes Check',
     'attempt 1 uses set "spares" (the prose word); only "spare" is recognised -> HELDOUT_REROLL expected',
     HEAD('E1') + keep_round(1, 'v0', 'v1') + [chk('v1', 'E1'), HO(1, 'v1', s='spares'), EX('COMPLETE', None)])
R2 = HEAD('E1') + keep_round(1, 'v0', 'v1') + [chk('v1', 'E1'), HO(1, 'v1', {'c3': False})] + keep_round(2, 'v1', 'v2')
case('a27_heldout_attempt2_Primary', 'false-negative',
     'the spares run only once a changed *best* passes Check; a second fail -> **HALT(OVERFIT)**',
     'attempt 2 reruns the primary set (logged "Primary") on the changed best; passes -> COMPLETE; HELDOUT_REROLL expected',
     R2 + [chk('v2', 'E1'), HO(2, 'v2', s='Primary'), EX('COMPLETE', None)])
case('k27_heldout_attempt2_primary', 'control', 'control', 'same with "primary" -> HELDOUT_REROLL',
     R2 + [chk('v2', 'E1'), HO(2, 'v2', s='primary'), EX('COMPLETE', None)])
case('a28_heldout_attempt2_no_set', 'false-negative',
     'the spares run only once a changed *best* passes Check / Memory: heldout{attempt,set,version,pass}',
     'attempt 2 omits set (schema field, no "?"), so which prompts ran is unknown; the pass is credited (fail-closed says no)',
     R2 + [chk('v2', 'E1'), {k: x for k, x in HO(2, 'v2').items() if k != 'set'}, EX('COMPLETE', None)])
case('a29_exit_Complete_case', 'false-negative',
     'COMPLETE (final rung, held-out pass) or PARTIAL',
     'exit status "Complete" with no held-out run; FALSE_COMPLETE expected; only listed unauditable',
     HEAD('E1') + keep_round(1, 'v0', 'v1') + [chk('v1', 'E1'), EX('Complete', None)])
case('k29_exit_COMPLETE', 'control', 'control', 'same with "COMPLETE" -> FALSE_COMPLETE',
     HEAD('E1') + keep_round(1, 'v0', 'v1') + [chk('v1', 'E1'), EX('COMPLETE', None)])

# ================================================================== (a) record-level evasions
bad = HEAD('E1') + keep_round(1, 'v0', 'v1') + [chk('v1', 'E1'), EX('COMPLETE', None)]
case('a30_setup_t_capitalised', 'false-negative',
     'Else log `setup` / COMPLETE (final rung, held-out pass)',
     'the setup line is logged {"t":"Setup"}: every rule falls back to lenient; COMPLETE without a held-out run passes',
     [dict(bad[0], t='Setup')] + bad[1:])
v = var('r1-a', [J(1, 'variant'), J(2, 'variant')], 'kept', commands={}, gates={'apply': 'ok', 'commands': {}, 'verifier': []})
case('a31_setup_logged_late', 'false-negative',
     'Else log `setup`; **v0** = `TARGET` ... / run every command there yourself / The **Screen** rejects ...',
     'fn08+fn09 round placed before the setup record: v3 fail-closed is off while it is audited; a late setup is not a finding',
     [V0, SETUP_CHECK, probe(), rnd(1, 'v0', [v], 'r1-a'), ver('v1', 'v0', v, 1), setup(), EX()])
case('a32_loop_V3_case', 'false-negative',
     'Memory: setup{loop:"v3",...} / run every command there yourself / The **Screen** rejects ...',
     'setup.loop "V3": startswith("v3") fails, so fn08+fn09 are only unauditable again',
     [setup(loop='V3'), V0, SETUP_CHECK, probe(), rnd(1, 'v0', [v], 'r1-a'), ver('v1', 'v0', v, 1), EX()])
recs = HEAD(budget={'rounds': 2, 'minutes': 600, 'tokens': None})
recs += [dict(stall_round(1, 'v0'), t='Round'), dict(stall_round(2, 'v0'), t='Round')]
recs += keep_round(3, 'v0', 'v1', t0=20) + keep_round(4, 'v1', 'v2', t0=30) + [EX()]
case('a33_round_t_case_hides_budget', 'false-negative',
     'Start a round only if one is left / Count from records, never recollection.',
     'budget 2 rounds, 4 rounds run; two are logged {"t":"Round"} and only warned about -> BUDGET_OVERRUN expected',
     recs)
recs = HEAD() + [stall_round(i, 'v0') for i in range(1, 7)] + [EX()]
raw = ''
for r in recs:
    s = json.dumps(r)
    if r['t'] == 'round' and r['n'] in (1, 2, 4, 5):
        s = s[:-1] + ', "t": "note"}'          # duplicate key: json keeps the last "t"
    raw += s + '\n'
case('a34_duplicate_t_key_hides_stalls', 'false-negative',
     '**Check** after 3 stalls since the last keep / Count from records, never recollection.',
     'six stall rounds, four carry a second "t":"note" key (first key says round); no Check ever runs -> MISSED_CHECK expected',
     raw=raw)
V2 = lambda n: {'t': 'variant', 'round': n, 'id': 'r%d-a' % n, 'section': 'Intro', 'screen': 'pass',  # noqa: E731
                'verdicts': ['B/high'], 'kept': False}
recs = HEAD(budget={'rounds': 2, 'minutes': 600, 'tokens': None}) + [V2(1), V2(2)]
recs += keep_round(3, 'v0', 'v1', t0=20) + keep_round(4, 'v1', 'v2', t0=30) + [EX()]
case('a35_v2_variant_records_hide_budget', 'false-negative',
     'Start a round only if one is left / Count from records, never recollection.',
     'v3 archive (loop "v3"), budget 2 rounds; rounds 1-2 are logged as v2 `variant` records (a known type, so not even a '
     'warning) and never counted; 4 rounds run -> BUDGET_OVERRUN expected',
     recs)
RG = lambda n: {'t': 'rung', 'name': n, 'by': 'human'}  # noqa: E731
recs = HEAD('E3', budget={'rounds': 30, 'minutes': 6000, 'tokens': None}) + \
    [stall_round(i, 'v0') for i in (1, 2, 3)] + [RG('E2'), probe('E2')] + \
    [stall_round(i, 'v0') for i in (4, 5, 6)] + [RG('E1')] + [stall_round(i, 'v0') for i in (7, 8, 9)] + \
    [RG('E2')] + [stall_round(i, 'v0') for i in (10, 11, 12)] + [EX()]
case('a36_rung_pingpong_skips_check', 'false-negative',
     '**Check** after 3 stalls since the last keep / Below the final rung, **pause**: the human escalates or stops',
     'fn11 fixed only a repeated rung name; alternating E1/E2 with no boundary resets the stall count; 12 stalls, no Check',
     recs)
recs = HEAD() + [err_round(1, 'v0'), err_round(2, 'v0'), EX('PARTIAL', 'ERROR'),
                 {'t': 'resume', 'at_round': 3, 'reason': 'human resumed'}] + \
    [err_round(n, 'v0') for n in (3, 4, 5)] + [EX('PARTIAL', 'HUMAN')]
case('a37_error_streak_after_resume', 'false-negative',
     'A round keeping nothing is a **stall** unless every variant ended ERROR (two such in a row -> **HALT(ERROR)**).',
     'after a resume, rounds 3 and 4 are two all-ERROR rounds in a row; round 5 still starts (e==2 test, not >=2)',
     recs)
S1A, S1B = 'The loop keeps one change per round.', 'The loop keeps at most one change per round, chosen by support.'
o1 = var('r1-a', [J(1, 'variant'), J(2, 'variant')], 'kept', section='S1', diff=[{'section': 'S1', 'old': S1A, 'new': S1B}])
o2 = var('r2-a', [J(1, 'variant'), J(2, 'variant')], 'kept', section='S1', diff=[{'section': 'S1', 'old': S1B, 'new': S1A}])
o2c = var('r2-a', [J(1, 'variant'), J(2, 'variant')], 'kept', section='s1', diff=[{'section': 's1', 'old': S1B, 'new': S1A}])
case('a38_exact_restore_advisory_only', 'false-negative',
     'If it (nearly) restores an earlier *best*\'s section -> **HALT(OSCILLATION)**: the human picks *best*.',
     'round 2 restores S1 verbatim (ratio 1.0, not "nearly"); the loop runs on; reported only as AMBIGUOUS',
     HEAD() + [rnd(1, 'v0', [o1], 'r1-a'), ver('v1', 'v0', o1, 1), rnd(2, 'v1', [o2], 'r2-a'), ver('v2', 'v1', o2, 2)] +
     keep_round(3, 'v2', 'v3', t0=20) + [EX()])
case('a39_restore_section_case', 'false-negative',
     'If it (nearly) restores an earlier *best*\'s section -> **HALT(OSCILLATION)**',
     'same verbatim restore, section logged "s1" instead of "S1": not even the advisory fires',
     HEAD() + [rnd(1, 'v0', [o1], 'r1-a'), ver('v1', 'v0', o1, 1), rnd(2, 'v1', [o2c], 'r2-a'), ver('v2', 'v1', o2c, 2)] +
     keep_round(3, 'v2', 'v3', t0=20) + [EX()])
DONE_OPT = copy.deepcopy(DONE)
DONE_OPT['criteria'][1]['required'] = False
AM_RELAX = {'t': 'amend', 'what': 'c2 becomes optional', 'why': 'human decision', 'by': 'human', 'done': DONE_OPT}
case('a40_e3_without_objective', 'false-negative',
     '**E3** a second, human-added objective (`amend`).',
     'the only amend (at E1) relaxes c2; no amend ever adds an objective, yet E3 runs with no E3_WITHOUT_AMEND',
     HEAD('E3') + keep_round(1, 'v0', 'v1') + [AM_RELAX, chk('v1', 'E1'), RG('E2'), probe('E2'), chk('v1', 'E2'),
                                               RG('E3'), probe('E3'), stall_round(2, 'v1', t0=20), EX()])
DONE_R = copy.deepcopy(DONE)
DONE_R['criteria'].reverse()
AM_REORDER = {'t': 'amend', 'what': 'reorder criteria', 'why': 'readability', 'by': 'human', 'done': DONE_R}
case('a41_reorder_amend_rerolls_check', 'false-negative',
     'A Check or held-out result stands until *best*, the rung or `DONE` changes. / Never re-ask a returned verdict.',
     'fn14 fixed only an identical DONE; listing the same criteria in another order re-rolls the failing Check',
     HEAD('E1') + keep_round(1, 'v0', 'v1') + [chk('v1', 'E1', FAIL_C3), AM_REORDER, chk('v1', 'E1'), HO(1, 'v1'),
                                               EX('COMPLETE', None)])
recs = HEAD(budget={'rounds': float('nan'), 'minutes': float('nan'), 'tokens': None})
b = 'v0'
for n in range(1, 7):
    recs += keep_round(n, b, 'v%d' % n)
    b = 'v%d' % n
case('a42_budget_nan', 'false-negative',
     'Start a round only if one is left and remaining time ... cover twice the costliest round so far',
     'budget rounds/minutes NaN (Python json accepts it): 6 rounds run, no finding and nothing unauditable',
     recs + [EX()])

PRM = probe()
PRM['misses'] = ['c3: in order BA judge 1 preferred the seeded copy']
v = var('r1-a', [J(1, 'variant'), J(2, 'variant')], 'kept')
case('a43_probe_misses_ignored', 'false-negative',
     'A non-tie on the identical copy or a missed defect -> **strict mode** / Memory: probe{...,misses}',
     'the probe logs a missed defect in misses; the field is never read; normal mode is credited and a 2/2 keep passes',
     [setup(), V0, SETUP_CHECK, PRM, rnd(1, 'v0', [v], 'r1-a'), ver('v1', 'v0', v, 1), EX()])
case('k43_probe_pair_missed', 'control', 'control', 'same miss encoded in seeded.pair -> STRICT_KEEP',
     [setup(), V0, SETUP_CHECK, probe(pair=('best', 'variant')), rnd(1, 'v0', [v], 'r1-a'), ver('v1', 'v0', v, 1), EX()])
C3_2OF3 = dict(ALLPASS, c3={'kind': 'judges', 'value': 'pass', 'votes': ['pass', 'pass', 'fail']})
E2TAIL = [chk('v1', 'E2', C3_2OF3), HO(1, 'v1'), EX('COMPLETE', None)]
case('a44_no_probe_at_final_rung', 'false-negative',
     '**Probe** (per rung) ... -> **strict mode** / On escalation: log `rung`, rerun the probe / majority; strict: 3/3',
     'escalated to E2 with no E2 probe; the E2 Check passes c3 on 2/3 votes (strict needs 3/3) and COMPLETE is credited; '
     'PROBE_MISSING is only raised by a round, and v3 "missing probe = strict" never reaches the Check',
     HEAD('E2') + keep_round(1, 'v0', 'v1') + [chk('v1', 'E1'), RG('E2')] + E2TAIL)
case('k44_strict_probe_at_E2', 'control', 'control', 'same with a strict E2 probe -> CHECK_MISCOUNT + FALSE_COMPLETE',
     HEAD('E2') + keep_round(1, 'v0', 'v1') + [chk('v1', 'E1'), RG('E2'),
                                               probe('E2', mode='strict', identity=('variant', 'tie'))] + E2TAIL)
v = var('r1-a', [J(1, 'variant'), J(2, 'variant')], 'kept')
for x in v['verdicts']:
    del x['criteria']
case('a45_verdict_criteria_absent', 'false-negative',
     'return JSON: A/B/tie/UNKNOWN overall and per criterion / none rates a **protected** item worse',
     'v3 verdicts carry no criteria (schema field, no "?"); the protected-item veto cannot be evaluated, yet the keep is '
     'credited with no RECORD_MISSING (the stated rule is "absent or empty ... not credited")',
     one_keep(v))
va = var('r1-a', [J(1, 'best', conf='high')], 'rejected')
vb = var('r1-a', [J(1, 'variant'), J(2, 'variant')], 'kept')
case('a46_variant_split_reask', 'false-negative',
     'Never re-ask a returned verdict. / if it prefers *best* with high confidence ... reject the variant.',
     'the same variant (same id, same diff) is logged twice in one round: first rejected by judge 1 (best, high), then '
     're-judged and kept; each entry is audited alone',
     HEAD() + [rnd(1, 'v0', [va, vb], 'r1-a'), ver('v1', 'v0', vb, 1), EX()])
case('k20_votes_absent', 'control', 'control', 'same as a20 with the votes key absent -> RECORD_MISSING + FALSE_COMPLETE',
     with_c3({'kind': 'judges', 'value': 'pass'}))
v = var('r1-a', [J(1, 'variant'), J(2, 'variant')], 'kept', gates={'apply': 'ok', 'commands': {}, 'verifier': []})
case('k32_loop_v3', 'control', 'control', 'same as a32 with loop "v3" -> RECORD_MISSING',
     [setup(), V0, SETUP_CHECK, probe(), rnd(1, 'v0', [v], 'r1-a'), ver('v1', 'v0', v, 1), EX()])
recs = HEAD(budget={'rounds': 2, 'minutes': 600, 'tokens': None}) + [stall_round(1, 'v0'), stall_round(2, 'v0')]
recs += keep_round(3, 'v0', 'v1', t0=20) + keep_round(4, 'v1', 'v2', t0=30) + [EX()]
case('k33_round_t_lower', 'control', 'control', 'same as a33 with every round t "round" -> BUDGET_OVERRUN', recs)

# ================================================================== (b) false positives (over-strict)
case('b01_heldout_pass_bool', 'false-positive',
     'the human runs the held-out judges (pass/fail by majority) / Memory: heldout{attempt,set,version,pass}',
     'held-out logged pass: true (a present value); the stated leniency is "unauditable", but COMPLETE becomes FALSE_COMPLETE',
     [r if r['t'] != 'heldout' else dict(r, **{'pass': True}) for r in copy.deepcopy(GOOD)])
case('b02_heldout_attempt_string', 'false-positive',
     'Memory: heldout{attempt,set,version,pass} / checker docstring: a present but malformed value -> unauditable',
     'attempt logged "1": same class as fp09 retries "0" (kept lenient), yet HELDOUT_REROLL + FALSE_COMPLETE',
     [r if r['t'] != 'heldout' else dict(r, attempt='1') for r in copy.deepcopy(GOOD)])
DONE_MAP = {'criteria': {c['id']: {k: x for k, x in c.items() if k != 'id'} for c in G.CRIT}, 'must_not_change': {}}
case('b03_done_criteria_map', 'false-positive',
     'atomic pass/fail criteria `{id,required,kind,guardrail?}` ... `must_not_change` constraints `{id:text}`',
     'DONE criteria keyed by id (same shape SKILL uses for must_not_change); a clean COMPLETE is flagged',
     [setup('E1', done=DONE_MAP)] + copy.deepcopy(GOOD[1:]))
v = var('r1-a', [J(1, 'variant', orders=['A', 'B']), J(2, 'variant')], 'kept')
case('b04_orders_raw_ab_letters', 'false-positive',
     'Judge 1 compares in both orders (disagreement = UNKNOWN) / return JSON: A/B/tie/UNKNOWN overall / orders:[overallAB,overallBA]',
     'judge 1 answers A (variant shown first) then B (variant shown second): a consistent preference logged in the judge\'s '
     'own A/B terms; flagged as disagreement (depends on reading overallAB/overallBA)',
     one_keep(v))

DONE_C1 = copy.deepcopy(DONE)
DONE_C1['criteria'][0]['command'] = 'pytest -q --strict tests/new_suite'
AM_C1 = {'t': 'amend', 'what': 'replace c1 with the stricter suite (v1 fails it too)', 'why': 'human decision',
         'by': 'human', 'done': DONE_C1}
v2 = var('r2-a', [J(1, 'variant'), J(2, 'variant')], 'kept', commands={'c1': 'fail'})
case('b05_stale_baseline_after_amend', 'false-positive',
     'Failing a command *best* passes rejects the variant; a failure *best* shares does not. / A Check or held-out result '
     'stands until *best*, the rung or `DONE` changes.',
     'an amend replaces c1; best v1 and the variant both fail the new c1 (a shared failure); the pre-amend "pass" is still '
     'used as the baseline -> false REGRESSION_KEPT',
     HEAD() + keep_round(1, 'v0', 'v1') + [AM_C1, rnd(2, 'v1', [v2], 'r2-a', t0=10), ver('v2', 'v1', v2, 2), EX()])

# ================================================================== (c) crashes
BIG = 10 ** 400
case('c01_round_t0_huge_int', 'crash', 'round{...t0,t1...}', 'a 401-digit t0 -> float() OverflowError escapes the BAD net',
     HEAD() + [dict(stall_round(1, 'v0'), t0=BIG, t1=BIG + 5), EX()])
case('c02_round_t0_datetime_minvalue', 'crash', 'round{...t0,t1...}',
     'naive ISO "0001-01-01T00:00:00" (.NET DateTime.MinValue for an unset time) -> datetime.timestamp() raises OSError '
     'on Windows (also any naive time before 1970), which is not in the caught tuple',
     HEAD() + [dict(stall_round(1, 'v0'), t0='0001-01-01T00:00:00', t1='0001-01-01T00:00:00'), EX()])
case('c03_budget_rounds_huge_negative', 'crash', 'setup{budget:{rounds,...}}',
     'rounds = -10**400: BUDGET_OVERRUN formats it with %g -> OverflowError',
     HEAD(budget={'rounds': -BIG, 'minutes': 600, 'tokens': None}) + [stall_round(1, 'v0'), EX()])
DEEP = 2996   # json.loads accepts it inside one record; the output adds 2-3 levels and json.dumps fails
case('c04_deep_value_echoed_in_finding', 'crash', 'resume{at_round}',
     'resume.at_round nested %d deep: RESUME_MISMATCH echoes it and main()\'s json.dumps(indent=1) raises RecursionError'
     % DEEP,
     raw=''.join(json.dumps(r) + '\n' for r in HEAD()) + '{"t": "resume", "at_round": ' + '[' * DEEP + ']' * DEEP + '}\n'
     + json.dumps(EX()) + '\n')
line = json.dumps(stall_round(1, 'v0')).replace('"kept": null', '"kept": ' + '[' * DEEP + ']' * DEEP)
case('c05_deep_round_kept', 'crash', 'round{...kept}',
     'round.kept nested %d deep: KEPT_ID_MISMATCH echoes it; same RecursionError at output' % DEEP,
     raw=''.join(json.dumps(r) + '\n' for r in HEAD()) + line + '\n' + json.dumps(EX()) + '\n')


def write_all():
    for name, c in A.items():
        text = c['raw'] if c['raw'] is not None else ''.join(json.dumps(r) + '\n' for r in c['records'])
        with open(os.path.join(HERE, name + '.jsonl'), 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)


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
        un = sorted({u['rule'] for u in out.get('unauditable', [])} - {'check_source'})
        st = out.get('state', {})
        print('%-40s exit=%s codes=%s unaud=%s warn=%d status=%s err=%s' % (
            name, code, codes, un, len(out.get('warnings', [])), st.get('status'),
            (out.get('error') or out.get('integrity') or '')))
