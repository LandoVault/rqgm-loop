# Derivation workspace addendum (2026-09-26, v2): recursion, red team and exploration

> v2 (same day) applies peer review 6 (`loops/peer/peer_review_derivation_rsi_gm.md`); disposition in doc 33 §12.3.
> Changed items are marked *(v2)*.

Additive to `CONSTRAINTS_AND_MOVES_pin_2026-09-08.md` (the pin), which stays in force unchanged; this file
narrows it and adds habitat-local process (never widens upstream). Upstream `F:\git\first-principles-derivation-lab`
is still pinned at `0db9639` (verified 2026-09-26: `main` HEAD unchanged; MOVE_SCHEMA v2, `linter/lint.py` v2,
template unchanged). Everything adopted below from upstream `staging/` is adopted **as habitat-local posture with a
habitat rule**, exactly as the pin did for M-D and instrument versioning; nothing upstream has moved out of staging.

Loop context: doc 33 (`33_Loop_Architecture_v4_Harden_Explore_Derive.md`) makes DERIVE one of three loop kinds; this
addendum is the DERIVE contract the pin did not have. The peer review (`loops/peer/peer_review_loop_v4.md` §1, §3)
is incorporated where marked *(peer)*.

## A. Recursion: claim-grain micro-loops instead of whole-document epochs

Source: upstream `staging/process-upgrades/LOOPGRAPH_V2.md` (finding-typed router). Habitat rule:

- **A-1 Scope = dependency slice** *(v2)*. A finding names one anchor (`[S<n>]`, a Basis item `B<k>`, a trace row, or a
  `## Checks` cell). The repair unit is the anchor **plus its premises, definitions and affected downstream uses**
  (the dependency slice, listed in the micro-loop record). Whole-trace re-verification is required when a revision
  changes the statement, quantifiers, the conditioning sigma-algebra, the exchangeability class, the null
  transformation, a coordinate or measure convention, or a shared definition, or when dependencies are cyclic or
  unknown. Trace-table cells stay immutable (pin R-A1): a repair appends a dated correction overlay or a versioned
  replacement trace, and the effective trace is built deterministically from those records.
- **A-2 Fresh refuter.** Each micro-loop round is one writer revision plus one fresh-context refuter who sees the
  revised slice **with its premises, definitions and dependencies** and the original finding, and is blind only to the
  writer's self-assessment and to prior verdicts *(v2)* (the `writer ↛ verifier` edge at claim grain).
- **A-3 Stopping heuristic, then the Check** *(v2)*. Stop proposing repairs after two consecutive "nothing new" rounds or
  three rounds; that is a heuristic, not a fixed-point certificate. The reserved independent Check over the
  effective trace and affected companions decides; a third round ending without a valid Check stays `unresolved`,
  never a pass; "nothing new twice" neither promotes the file nor overrides an open defeater. The anchor's debt cell
  carries `OPEN` mirrored as a Pauli question (CHECK2).
- **A-4 Every adjudicated-VALID defeater blocks.** A required claim with any unresolved adjudicated-valid defeater is
  not `footprint-checked`, whatever its rank; rank orders repair only *(peer §1, §8 rank 4)*. Statuses are kept apart
  *(v2)*: `proposed` → `substantiated` (exact claim, premise set, violated obligation, witness or reasoning chain) →
  `adjudicated-valid` | `rejected` | `unresolved`. While the panel is uncalibrated (§D) its outputs are **proposals**
  that may suspend applicability pending adjudication; they never manufacture VALID labels. An empty accepted set is
  a legitimate outcome; a disputed block has an appeal path over the full dependency slice with evidence and a cost
  bound.
- **A-5 Fold-back and sweep.** The accepted revision lands with a dated `## Revision record` line naming the finding
  id and the round record; then a propagation sweep visits every companion file sharing the anchor (the doc 28 /
  `rs_*` / oracle triplets are the standing case). A sweep never copies a status; it re-verifies.
- **A-6 Budget.** Micro-loops charge the parent loop's budget; `budget.reserved` for the final VERIFY is untouchable.

## B. Red team: prediction sheets, defeater panel, replay forks, canaries

- **B-1 Prediction-registered VERIFY** (upstream `EVAL_V2.md` §A) is **optional instrument-calibration work** *(v2)*,
  sampled on ambiguous or newly introduced rules, never required on every derivation and never affecting the
  derivation's grade: it measures the verifier first. Protocol: a finite set of load-bearing binary questions is
  frozen independently of the predictor ("does row R discharge a universal obligation by a numeric match?"), each
  gets a probability locked before downstream inspection, and the sheet is scored against separately adjudicated
  outcomes by mean Brier loss with the unadjudicated fraction and abstention coverage reported. Template:
  `templates/VERIFY_template_v2.md` (Check 0, optional).
- **B-2 Defeater panel** (upstream RQGM-002 `LOOP_GRAPH.md` IL3, habitat form). Two blind generators attack the same
  trace with the same segmentation; a judge who wrote its key first grades validity under the pin's criteria, unions
  the findings, and ranks them for repair order only (a forced ranking never decides validity; an empty accepted
  set is allowed) *(v2)*. Types: `MISATTRIBUTION`, `UNSUPPORTED` (support never produced for inspection; adopted here
  as a habitat type, upstream M-A still staged), `scope-unresolved` and `evidence-unavailable` (replacing
  `boundary-UNDECIDABLE`, which is reserved for a stated undecidability theorem *(v2)*), `false-debt-freeness`,
  `vacuous-hypothesis` (C-P2), `values-for-logic` (C-P4). Two blind attackers can share a blind spot: "no VALID
  defeater" is a bounded search result, not completeness. Output feeds A-4.
- **B-3 Replay forks as a transfer diagnostic** *(v2)* (upstream `PREREG_REPLAY.md`, with its own PR-1/PR-2 fixes). A
  fork tests whether a model can **recover** a move from the pre-step context, not whether the move is valid or who
  originated it. Use it only for a decisive move that repeatedly fails to transfer between agents (recognizing the
  transformation group, conditioning away a nuisance while keeping a testable target, detecting a singleton null
  orbit): one preselected step, two cheap fresh-context forks, one adjudication if no mechanical check exists (≤ 3
  calls), exclusive outcome classes fixed in advance, logical equivalence scored rather than wording, a factual check
  that the package holds the needed definitions and premises. Provenance axes are kept separate: recorded
  proposer/executor; precursor present/absent/uncertain; fork outcome. No recursive retries.
- **B-4 Derivation canary suite** *(v2, peer 6 A5)*. Four frozen valid/defective pairs, identical except for the
  targeted fault, run through the same acceptance path: (1) vacuous hypothesis: a null-validity certificate stating
  exchangeability under a fixed group with a way to fail, vs "assume the test is valid" (reject as circular); (2)
  values-for-logic: an enumerated finite null with its preservation argument, vs the same numbers with the argument
  deleted (obligation unresolved despite matching values); (3) EXEC doing typed work: a value row plus a separate
  certifying row, vs the discharge moved into EXEC (structural failure regardless of value); (4) promotion without
  event: a promotion pointing at a VERIFY event for the exact version, vs a changed `State:` alone (refuse). Payloads
  are frozen, verdicts checked independently, and superficial representation varied in occasional held-out controls.
  A valid-pair rejection means an over-blocking evaluator, an invalid-pair acceptance an under-blocking one: an
  instrument problem, never a defect of the target derivation. Promotion is a separate controller event after
  VERIFY; a `State:` string is not the event.
- **B-5 Oracle authority is claim-scoped** *(peer 4 §3; v2 per peer 6 A6)*. Three outcomes are kept apart: a value
  outside the pre-registered tolerance is a **failed numerical obligation** (investigate); a unit, domain, input-version
  or assumption mismatch makes the result **inapplicable** (suspend its use for that criterion, output preserved); an
  execution error or missing input is **unchecked/error**. A `MATCH` supports only the declared value at the declared
  scope; a validated counterexample can refute a universal claim, agreement cannot establish one. The oracle contract
  (stated in `## Checks / Oracle`, else the row is `gloss-only`) records: contract and implementation version; target
  claim and row ids; input references and schema; quantity, unit, coordinate/measure convention, domain, conditioning
  assumptions; preprocessing; deterministic or seeded mode; tolerance and comparison rule; expected coverage;
  permitted conclusion; prohibited extrapolations; execution receipt. Declared-field mismatches are decidable;
  semantic applicability still needs the claim-to-manifest mapping. K-oracle is optional only when no required claim
  and no requested promotion depends on it; a failed optional oracle that contradicts a required claim is examined.

## C. Exploration: territory map, incubation ledger, F6 slot

- **C-1 Territory map per ticket.** Every `tickets/ND*.md` that admits more than one derivation route carries a
  `## Territory` table: families F1…F5 from doc 19's pentad plus an **F6 row: a bounded outside-pentad search attempt
  when route uncertainty matters** *(v2)*; "none found within budget" is a coverage result, not a failure, and F6 never
  blocks an otherwise valid single-route proof unless outside-family exploration is the task's objective. A family
  must differ in assumption, representation, transformation or proof strategy, not in name. A route that hits a wall
  is recorded `blocked` with `wall` and `resume_requires` (doc 26 §4 schema), distinguishable from `not attempted`.
- **C-2 Incubation ledger.** `derivations/INCUBATION_LEDGER.md` (new): parked derivation ideas with a return
  condition and a return count; every DERIVE run re-reads it first (upstream ANTI_DISTORTION #3). A return counts
  only on **substantive reactivation** (changed prerequisites or a new discriminating argument, with the trigger and
  its evidence stored), never on re-reading *(v2)*; priority reflects expected unblock value, relevance and cost; an
  item rediscovered three times without a new test is a blocker to diagnose, not an automatic promotion.
- **C-3 Corroboration, obligation by obligation** *(v2)*. Two routes corroborate only the obligation both support: a
  Lean object and a numeric oracle do not establish the same proposition (the oracle checks values); two blind writers
  can share a false premise. A `corroborated-by: <file>` relationship records which obligation each route supports,
  their shared dependencies and the distinct failure modes tested; it never ranks two shallow routes above one
  complete proof and never confers the pin's `attestation: corroborated`.
- **C-4 Surprise log feeds exploration.** `## Surprise & by-product log (miracles)` entries are candidate F6 routes;
  the STOP meta-agent reads them at boundaries and may open an incubation entry, never a derivation.

## D. Instrument registry (habitat, per upstream `instrument-versioning.md` rules 1-4)

| instrument | version | status | calibration anchor | changes |
|---|---|---|---|---|
| `linter/lint.py` (upstream) | v2 @ 0db9639 | ACTIVE | its fixtures | pin bump only |
| Judge key | `JUDGE_KEY_2026-09-08.md` | FROZEN (single use, spent) | — | a new key per round, written before arms |
| Habitat VERIFY template | v2 (this addendum) | ACTIVE | the four D1 lab-template files | boundary only |
| Defeater criteria | v1 (B-2 types) | UNCALIBRATED: outputs are proposals until calibrated on known-valid traces **and** independently seeded defects; K-defeaters becomes a required gate only then *(v2)* | `nv3_fiber_exactness.md` + seeded-defect twins | boundary only |
| Derivation canary pair | v1 (B-4) | ACTIVE | — | pair changes need a new id |
| `score_variant.py` (relations) | v3 (sibling branch) | ACTIVE there | seeds v00-v05 | re-baseline on the anchor set at every change |

A decision-gating instrument changes only at an epoch boundary, with a changelog line here and an `instrument`
record in the loop archive; an uncalibrated instrument runs as secondary and gates nothing.

## E. Not adopted (and why)

- Upstream M15+ / schema-v3 prototypes: still forbidden (lint regex; pin §4).
- Upstream M-B attestation ladder: still the three-valued field.
- A fourth "calibration loop": calibration is a **state** with a named owner (this file's §D), not a search loop
  *(peer §1, §10)*.
- Parallel-tempering vocabulary for exploration: the lanes in doc 33 are exploration/exploitation heuristics
  *(peer §5a)*; the derivation workspace uses the territory map instead.

## F. Revision record

- 2026-09-26 — created beside the 2026-09-08 pin after the loop-v4 redesign (doc 33) and the peer review of it.
  No derivation file was edited; the VERIFY template v2 and the incubation ledger are new files.
- 2026-09-26 (v2) — peer review 6 applied: dependency-slice repair unit, refuter sees premises, stopping heuristic
  then Check, defeater statuses and calibration gate, prediction sheets optional and Brier-scored, transfer-diagnostic
  forks, four-pair canary suite, three-way oracle outcomes and contract fields, bounded F6, substantive-return
  counting, obligation-scoped corroboration. Template corrections for the DERIVE initiator: stable rubric per
  cohort, mechanical K-items by command, ACCEPT-WITH-DEBT never substitutes for the requested state, promotion is a
  controller event, budget in calls not rounds.
