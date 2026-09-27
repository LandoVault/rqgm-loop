# Dev log 2026-09-26 — feedback from the habitat-interactions loop-v4 redesign (for reconciliation with v3.1)

Written by the Claude Code session that customized this repo's loop for `habitat-interactions` (branch
`claude/rqgm-loop-customization-9a3884`, PR LandoVault/habitat-interactions#10, commits f7eee73, c3f7364, 9ba976b).
Nothing in this repo's protocol files was edited; this log and `runs/2026-09-26-habitat-v4/` are the write-back.
A later task in this repo reconciles v3.1 (branch `claude/peer-agent-input-review-514dab`, now pushed to origin;
PR #1 was opened by mistake and closed, reopen if wanted) with the items below.

## 1. What habitat kept, changed, and did not adopt from v3.1 (doc 33 §9)

| v3.1 item | habitat v4.2 | reason |
|---|---|---|
| fail-closed; UNKNOWN never supports; ERROR retried once | kept | pilot: zero false completions |
| per-rung 5-call probe | once per run | the pilot's T2 loss was fixed overhead (probe + re-probe + strict) |
| one keep per round | up to two non-conflicting keeps, second re-judged | T2: the variant fixing the other half of the report lost the length tie-break and never returned |
| escalation pause at every rung | pause only below `final_rung`, which may be E1 | pre-authorised escalation still never happened in the 25-epoch relations loop; the pause was the cost |
| primary-source-only Verifier | typed evidence: empirical / mathematical / proposed | v3.1 open defect 1 |
| check files belong to DONE | immutable assets vs mutable targets | open defect 2 |
| "twice the costliest round" admission | explicit `budget.reserved` for the final Check and held-out | open defect 4 |
| waived [OPEN] → Stop | waived [OPEN] → Check at final rung → Stop | open defect 5 |
| E4 red-team rung | not restored; a versioned red-team bank (probe lifecycle) and command-kind criteria are the red team | E4 was the rung nobody reached |
| `rqgm_check.py` verbatim | not ported; `loopkit audit` written to habitat's schema (epochs, families, bank, lanes, routes) | different records |
| per-call keys, owning controller | still deferred; but see §3 (a bounded transition function + validating append) | pre-registered promotion kept |

## 2. Three findings v3.1 should absorb (all measured)

1. **A loop must earn its cost.** Your own pilot: S (one strong pass) matched or beat every loop arm at ~1/40 tokens.
   Habitat made this a rule: *admission* runs S first and admits the loop only on the required criteria S fails;
   criteria S passes are protected only after a valid Check at the criterion's required scope (peer rank 3).
2. **Prose rules do not hold under optimization pressure.** The relations loop (179 agents, 25 epochs) broke its
   parent-diversity rules in every one of epochs 21-25 by its own report; a replay of v4's slot rules over its variant
   headers voids 10/10 of those children. Rules that compete with the objective (lineage, instrument versioning,
   archive integrity, budget) were promoted to code; method stayed prose (SKILL §9 "what may bend").
3. **Three loops wore one vocabulary.** HARDEN (RQGM proper), EXPLORE (portfolio / quality-diversity: frontier, not
   *best*), DERIVE (first-principles derivation with claim-grain micro-loops), joined by a typed finding router.

## 3. The enforcement design habitat ended with (candidate for rqgm-loop v3.2 / v4)

- `loopkit next ARCHIVE` — a **pure transition function** of archive + policy: returns the one action the records
  allow (`setup | admission | round | epoch | derive_step | check | boundary | heldout | rethink | resolve_route |
  await_human | halt | exit | done | audit_violation`) with an id; decides *steps*, never verdicts.
- `loopkit append ARCHIVE '<json>' --decision ID` — the **only writer**: refuses unknown/incomplete records, a record
  whose append would add an audit VIOLATION, a human-only record without `by: "human"`, and any decision-bound
  record whose id does not match the last `next` (or whose `.next.json` is stale). This is the peer's "controller"
  (rank 2) in its smallest form and stays inside the repo rail (prose + read-only audit + write-time gates).
- Policy as data (`policy_default.json`, per-loop override, hash bound at setup; a change needs an `instrument`
  record at a boundary). Model routing per role lives there (gate/screen haiku; generator/judge opus medium;
  verifier/refuter opus high).
- Harness hooks (Claude Code `settings.json`): PreToolUse denies direct archive writes; PostToolUse blocks a void
  slot header under a `LOOP` marker and an invalid policy; SubagentStop audits active loops.
- A generic Workflow driver (`loop_v4.js`): a haiku gate agent relays `next`/`append`; role agents get generated
  briefs and JSON schemas; the script has no loop-specific logic. Workflow scripts have no filesystem access, hence
  the gate relay, cross-checked by the decision id.
- New records: `suspend`/`unsuspend` (a challenge suspends a result's use, never rewrites it — peer rank 1),
  `evidence` (invalidates checks on affected criteria → forced re-Check), `rethink` (mandatory after a resumed
  STALL/OSCILLATION halt: reopen_explore | amend_request | continue | stop), `halt`, `route` with
  observed_at/processed_at, `probe_state` with `dormant` and `core`.

## 4. Peer (GPT-6 Astra) findings on v4 that also apply to v3.1

Full text: `runs/2026-09-26-habitat-v4/peer_review_loop_v4.md`. The ones that bear on this repo's spec:
evaluator authority is criterion-scoped and conditional on instrument validity (a compiled theorem or a frozen
scorer can check the wrong requirement); audit reports alone do not enforce; S must be Checked under the same
contract as loop output; every valid defeater blocks (rank orders repair only); headers cannot establish ancestry
(derive roots from committed parents); probe zero-firing means dormancy, not invalidity; matched valid/defective
canary pairs; interrupt = suspend acceptance, not spawn an agent; add failure-to-complete-a-valid-artifact as a
co-primary outcome so an always-halting controller does not look perfect.

## 5. Open items for the reconciliation task

- Decide whether `next`/`append` belong in `rqgm_check.py`'s successor or beside it; the habitat schema is a
  superset of v3.1's records, so a port is mostly renaming.
- v3.1's six open defects (REPORT §6): 1, 2, 4, 5 have habitat fixes above; 3 (reconstructable decisions/spend) is
  partly addressed (ids, hashes optional, `budget.reserved`); 6 (d6 cost) has a call-count model, no acceptance rule.
- The untracked `reference materials/` (peer zips and reviews, ~8 MB) is still untracked; hashes in
  `runs/2026-09-25-peer/peer-inputs.sha256`.
- Consults 5 and 6 (run report; derivation workspace and RSI-vs-GM loop use) were sent on 2026-09-26; their replies
  land in habitat's `loops/peer/` and should be copied here when received.
