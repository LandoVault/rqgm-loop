# Consult request 6 — the derivation workspace, and when to use an RSI loop vs a Gödel-machine loop on a task

From: the Claude Code session maintaining `habitat-interactions`, same user. Date: 2026-09-26. Follows consult 5.
Review only; do not run code; nothing about the local subjects.

The user's emphasis for this round: **(A) the first-principles derivation workspace** (how a derivation is written,
verified, attacked and promoted here) and **(B) the use of recursive-self-improvement (RSI) loops and
Gödel-machine (GM) loops on concrete tasks** in this repo. Attached verbatim: the derivation-workspace addendum
(2026-09-26), the DERIVE initiator template, and the pin's judge key (what a GOLD-READY derivation must show).

## Vocabulary as used here (so we argue about the same thing)

- **GM-style loop** (Red Queen Gödel Machine lineage): one artifact, a written `DONE`, separate adversarial
  evaluators whose bar rises at boundaries; a change is kept only on evidence it improves the artifact under the
  current utility; the utility itself changes only at epoch boundaries with a human. In this repo: HARDEN.
- **RSI-style mechanisms** (as the relations loop used them): an open archive with parent sampling (Darwin GM),
  quality-diversity niches (MAP-Elites), an evaluator that evolves through data (a co-evolving red-team bank),
  verbal reinforcement memory (Reflexion lessons), a self-improving improver (a STOP meta-agent rewriting the
  operator playbook), final debate/refutation. In this repo: EXPLORE plus the bank and the meta agent.
- **DERIVE**: the derivation lab's protocol (extract → classify → trace basis → re-derive → check → file; states
  sketch → footprint-checked → oracle-checked → settled; lint v2 with seven checks; a fresh-context VERIFY; oracle
  values only, never logic; move trace M1-M14; Pauli question; §0 invariance declaration), plus this addendum's
  additions: claim-grain micro-loops, prediction-registered VERIFY, a defeater panel, replay forks, canary pairs,
  oracle contracts, a territory map with a mandatory F6 slot, an incubation ledger, an instrument registry.

## Questions (adversarial, constructive; label every claim measured / literature / design-only)

### A. The derivation workspace

1. Attack the DERIVE contract as a *loop*: is claim-grain micro-looping (one anchor, fresh refuter, ≤ 3 rounds,
   exhaustion = unresolved) the right unit, or does it fragment a derivation whose steps are entangled? When must the
   unit be the whole trace?
2. Prediction-registered VERIFY (the verifier files predictions before reading the writer's self-assessment): does
   it measure the verifier or the derivation? What would make a prediction sheet gameable, and what is the smallest
   scoring rule that is not?
3. The defeater panel (two blind generators, one judge with a key written before reading, forced ranking, every
   VALID defeater blocks): give the failure mode where this produces confident wrong blocks, and the one where it
   produces confident wrong passes. Which of the six defeater types is least decidable?
4. Replay forks as a derivation red team (fork a cheap model at a decisive step with the pre-step context only;
   exclusive outcome classes fixed in advance): is this evidence about the *derivation* or about the *model*? When is
   it worth its cost on this repo's derivations (statistics and spatial nulls, not physics)?
5. Canary pairs for derivations (a valid identity vs the same with an essential hypothesis dropped, same acceptance
   path): what pair would actually catch the failure modes this repo has recorded (vacuous hypotheses, values
   standing in for logic, an EXEC row doing typed work, a `State:` promotion without an event)?
6. Oracle contracts (an oracle MATCH supports only the value under the assumptions it encodes; a mismatch suspends,
   never rewrites): is "suspend" the right semantics for a numeric oracle, and how should the contract be written so
   that a `contract-or-assumption-mismatch` is decidable from records?
7. The territory map with a mandatory F6 ("a family outside the pentad must be proposed; 'none could' is a finding,
   not a pass") and the incubation ledger with return counts: do these produce exploration or ritual? What record
   would show the difference after three runs?

### B. RSI vs GM loops on tasks

8. Give a decision rule, as a table, for **which loop kind for which task in this repo**: (i) a claim-bearing
   document with attached derivations (doc 28 shape); (ii) an executable null layer with tests and Lean policy
   (nullkit shape); (iii) a search over estimands/variants against a scorer (relations shape); (iv) a single
   derivation file; (v) a proposal or spec for a peer; (vi) the loop mechanism itself (recursive self-application).
   For each: HARDEN / EXPLORE / DERIVE / a single strong pass / none, the admission test, the evaluator kinds that
   should dominate, the stopping rule, and the one failure to watch.
9. Where does an RSI mechanism add value over a GM loop, and where does it only add cost? Be specific about the six
   mechanisms the relations loop used (archive + parent sampling; niches; co-evolving bank; Reflexion lessons; STOP
   playbook rewrite; final debate). For each: keep / drop / gate behind a trigger, with the trigger.
10. Recursive self-application (the loop improving its own spec, as the reference repo did): under what conditions
    is this evidence of anything, and what is the minimal held-out design that would make a "the mechanism improved"
    claim honest? What must never be self-modified?
11. The user observes that asking a capable model to "use RQGM and RSI loops" already does an acceptable job. From
    your side of the fence (a different model family): which parts of this design would *you* need spelled out to
    execute it faithfully, and which would you rather have as principles? Answer for a derivation task specifically.

## Deliverable

One downloadable Markdown file named `peer_review_derivation_rsi_gm.md` with sections A1-A7 and B8-B11 (B8 as a
table), **and the full content pasted into the chat**. Review only.

---

# ATTACHED A: derivation-workspace addendum (verbatim)

# Derivation workspace addendum (2026-09-26): recursion, red team and exploration

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

- **A-1 Scope lock.** A finding against a derivation names one anchor (`[S<n>]`, a Basis item `B<k>`, a trace row, or
  a `## Checks` cell). The writer revises **only that anchor's text** and the cells that cite it. A revision that
  touches another `[S]` is a new finding, not a repair.
- **A-2 Fresh refuter.** Each micro-loop round is one writer revision plus one fresh-context refuter who sees the
  revised anchor and the original finding only (the `writer ↛ verifier` edge at claim grain).
- **A-3 Fixed point.** Stop after two consecutive "nothing new" rounds or three rounds. Exhaustion yields
  `unresolved`, never a pass *(peer §2)*; the anchor's debt cell carries `OPEN` mirrored as a Pauli question (CHECK2).
- **A-4 Every VALID defeater blocks.** A required claim with any unresolved VALID defeater is not `footprint-checked`,
  whatever its rank; rank orders repair only *(peer §1, §8 rank 4)*.
- **A-5 Fold-back and sweep.** The accepted revision lands with a dated `## Revision record` line naming the finding
  id and the round record; then a propagation sweep visits every companion file sharing the anchor (the doc 28 /
  `rs_*` / oracle triplets are the standing case). A sweep never copies a status; it re-verifies.
- **A-6 Budget.** Micro-loops charge the parent loop's budget; `budget.reserved` for the final VERIFY is untouchable.

## B. Red team: prediction sheets, defeater panel, replay forks, canaries

- **B-1 Prediction-registered VERIFY** (upstream `EVAL_V2.md` §A). The verifier files a prediction sheet **before**
  reading the writer's self-assessment or `## Tier-1 lint (self-run)`: (i) which rows will draw which defeater type;
  (ii) which anchor will move under a better substrate; (iii) which load-bearing claims survive unchanged. Scored
  after the layers run as CONFIRMED / MISS / UNFALSIFIABLE-AS-WRITTEN; the last bucket is an instrument defect,
  routed to tighten the template, never counted against the derivation. Template: `templates/VERIFY_template_v2.md`.
- **B-2 Defeater panel** (upstream RQGM-002 `LOOP_GRAPH.md` IL3, habitat form). Two blind generators attack the same
  trace with the same segmentation; a judge who wrote its key first grades validity under the pin's criteria, unions
  the findings, and produces a forced ranking. Types: `MISATTRIBUTION`, `UNSUPPORTED` (support never produced for
  inspection; adopted here as a habitat type, upstream M-A still staged), `boundary-UNDECIDABLE`,
  `false-debt-freeness`, `vacuous-hypothesis` (C-P2), `values-for-logic` (C-P4). Output feeds A-4.
- **B-3 Replay forks as a derivation red team** (upstream `PREREG_REPLAY.md`, with its own PR-1/PR-2 fixes). For a
  derivation whose decisive step is a human or orchestrator move, fork a cheap model at the step with the
  pre-step context only, under **exclusive** outcome classes fixed in advance, a proposes/executes axis separated
  from the route axis, and a one-line factual check of the package before any fork runs. The verdict vocabulary
  gains `crystallized` (a diffuse idea the trajectory already held, committed by the human) beside human / model /
  joint / unrecorded (M-G).
- **B-4 Derivation canaries** *(peer §3)*. Each DERIVE run plants a matched pair: a valid elementary identity with an
  explicit domain, and the same identity with an essential hypothesis dropped (a nonzero denominator, a finiteness
  assumption). The pipeline must accept the first and reject or leave `unresolved` the second, through the same
  path as the real derivation, and must show that the checked statement is the submitted one. A pass on the
  defective control → HALT(CANARY). Canary outcomes are logged (`canary` record), never mixed into the derivation's
  grade.
- **B-5 Oracle authority is claim-scoped** *(peer §3)*. An oracle `MATCH` supports the value it computes under the
  assumptions it encodes; a `contract-or-assumption-mismatch` finding (units, grid, band, side) **suspends** that
  support for the criterion without rewriting the oracle's output. The `## Checks / Oracle` subsection states the
  oracle's contract (inputs, assumptions, what a mismatch would look like) or the row is `gloss-only`.

## C. Exploration: territory map, incubation ledger, F6 slot

- **C-1 Territory map per ticket.** Every `tickets/ND*.md` that admits more than one derivation route carries a
  `## Territory` table: families F1…F5 from doc 19's pentad plus a mandatory **F6 (must be proposed)** row (doc 26
  §2.1 kept). A route that hits a wall is recorded `blocked` with `wall` and `resume_requires` (doc 26 §4 schema),
  distinguishable from `not attempted`.
- **C-2 Incubation ledger.** `derivations/INCUBATION_LEDGER.md` (new): parked derivation ideas with a return
  condition and a return count; every DERIVE run re-reads it first (upstream ANTI_DISTORTION #3). Return count is
  priority; an item returned three times without a route is escalated to a ticket.
- **C-3 Corroboration tier.** Two independent routes to one result (Lean object + oracle; two blind writers; physics
  reading + statistics reading) outrank one deep route (upstream BEYOND_AXIOMS §5). A derivation may record
  `corroborated-by: <other file>` only when the other route was produced blind (`writer ↛ writer`).
- **C-4 Surprise log feeds exploration.** `## Surprise & by-product log (miracles)` entries are candidate F6 routes;
  the STOP meta-agent reads them at boundaries and may open an incubation entry, never a derivation.

## D. Instrument registry (habitat, per upstream `instrument-versioning.md` rules 1-4)

| instrument | version | status | calibration anchor | changes |
|---|---|---|---|---|
| `linter/lint.py` (upstream) | v2 @ 0db9639 | ACTIVE | its fixtures | pin bump only |
| Judge key | `JUDGE_KEY_2026-09-08.md` | FROZEN (single use, spent) | — | a new key per round, written before arms |
| Habitat VERIFY template | v2 (this addendum) | ACTIVE | the four D1 lab-template files | boundary only |
| Defeater criteria | v1 (B-2 types) | UNCALIBRATED: advisory until piloted on a gold trace | `nv3_fiber_exactness.md` | boundary only |
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


# ATTACHED B: DERIVE initiator template (verbatim)

## D — DERIVE: one derivation to footprint-checked (the rs_* shape)

```text
kind: derive
TARGET: derivations/{{rs_<name>.md}} (+ its VERIFY_ file, written by a non-writer)
GROUNDING: the pin + 2026-09-26 addendum; the ticket's ## Territory table; INCUBATION_LEDGER.md (read first);
  the named _derived/ records the derivation may cite (by file name only)
ASSETS: lint.py; the derivation's oracle (with its contract stated, addendum §B-5); the canary pair
DONE:
  K1 lint          required  command  "lint exits 0, verifier-run"
  K2–K20           required  judges   (the JUDGE_KEY items, one fresh key per round)
  K-defeaters      required  judges   "no unresolved VALID defeater of a required claim (any rank)"
  K-oracle         optional  command  "oracle MATCH for every value row; contract stated"
  must_not_change: State (promotes only by the pin's rules R-A2); trace-table cells; band; envelope
  final_rung: E2
CANARIES: the addendum §B-4 pair (valid identity with domain / same identity with a hypothesis dropped)
ROLES: writer (one derivation, TOC-grade brief); verifier (fresh; prediction sheet BEFORE reading; re-runs lint);
  defeater panel (2 blind generators + 1 judge with key-before-arms, forced ranking); refuter (fresh per micro-loop
  round)
ROUTER: defeater-valid → claim-grain micro-loop (≤ 3 rounds; exhaustion = unresolved); wrong-anchor → single-anchor
  re-verify; contract-or-assumption-mismatch → suspend the oracle's support for that criterion; cross-doc →
  propagation sweep over doc 28 / rs_* / oracle triplets
MEMORY: loops/rqgm-derive-{{name}}/archive.jsonl ; BUDGET: rounds 6; reserved {rounds: 1}
ADMISSION: S = one strong writer producing the derivation in one pass; Check K1 by lint, K2–K20 by three fresh
  judges against a key written before reading; admit only the required failures.
```


# ATTACHED C: judge key 2026-09-08 (verbatim; what a GOLD-READY derivation must show)

# Judge key — what a GOLD-READY real-datum derivation must show (2026-09-08)

Written **before** reading any `rs_*` derivation, any `VERIFY_*` file, or the Codex native-sampling
variant, per the blindness edge *judge: key-before-arms* (pin §7). Source: `CONSTRAINTS_AND_MOVES_pin_2026-09-08.md`
§1 (constraints), §3 (document shape), §5 (habitat retrofit checklist), §6 (habitat-local narrowings).
Nothing below is derived from a writer's self-assessment.

## A. Grade definitions (fixed here, before evidence)

| grade | meaning |
|---|---|
| **GOLD-READY** | every K-item below is satisfied; lint exit 0 run by me; a fresh-context `VERIFY_` exists with its own exit-0 lint; the single load-bearing result is inside the T0 claim envelope and every real-datum number is traceable to a named `_derived/` file. Open debt may exist but is *declared*, owned, and non-load-bearing. |
| **ACCEPT-WITH-DEBT** | all FAIL-class mechanical items pass (lint 0, shape, provenance vocabulary, envelope), but ≥1 K-item is met only in substance, not in form, or load-bearing debt is declared and correctly quarantined so the stated result survives its worst case. |
| **REWORK** | any of: lint ≠ 0; a claim outside the T0 envelope; an invented substrate; a real-datum number not traceable to a named file; an M15+ or unrecognized move id; an EXEC row doing typed work; a `State:` promotion unsupported by an actual event; a factual falsity about the repository left uncorrected. |

Any single REWORK trigger dominates; grade is not an average.

## B. K-items (the checklist, mechanical first)

**K1 — Lint, judge-run.** `python F:\git\first-principles-derivation-lab\linter\lint.py <file>` exits `0`.
INFO lines are permitted and must be recorded. Exit `2` (parse error) is as fatal as `1`. §1.3.

**K2 — Document shape, in order.** Frontmatter bullets `Source` · `Label in source` · `Classification` ·
`State`; then `## Statement` · `## Basis` · `## Search program` · `**§0 invariance declaration**` ·
`## Derivation` · `## Move trace` · `## Checks` (Footprint; Oracle) · `## Pauli question` ·
`## Surprise & by-product log (miracles)` · `## Known limitations` · `## Open questions / debt` ·
`## Tier-1 lint (self-run)` · `## Revision record`. §3.

**K3 — Search program is FENCED** under that exact heading, fields verbatim: `hard core:` (parameterized
schemas, not prose) · `scope σ:` · `pass π:` · `exhaustion:` · `attestation:`. A prose hard core silently
disables CHECK5/6 and is a Gap-A regression → REWORK. `exhaustion:` **must be empty** unless a graded
boundary-spectrum table exists (§5 Gap A). §1.2.

**K4 — Attestation honesty.** `attestation:` ∈ {`pre-registered`, `corroborated`, `gloss-only`}; `corroborated`
only if an oracle script **in this repo** under `derivations/oracles/` backs a row, and that oracle reads only
`_derived/`. Otherwise `gloss-only`. Do not pre-adopt the M-B ladder. §5 Gap B, §1.2, §6.

**K5 — `provenance:` in the trace header**, habitat vocabulary only:
`synthetic-oracle | fixture | executed | real-datum-local`. Any row carrying local-sample numbers ⇒
`real-datum-local`. §6.

**K6 — Claim envelope (T0, RII-v1).** A `real-datum-local` row may support **descriptive, gate, feasibility**
statements only — plus, per the task framing, NV-1 negative-control and fiber-degeneracy statements.
**Zero** population, cohort, cross-patient, biological, or latent-Z statements, anywhere, including in
prose, Pauli question, or surprise log. `scientific_status: not_claimable` must be visible and not hedged
into a claim. §6. *This is the sharpest REWORK trigger.*

**K7 — Traceability + no leakage.** Every real-datum number names the `_derived/` file it came from
(pin §7 barrier discipline: "never re-typed from memory"). **No** voxel coordinates, per-voxel rows, image
crops, or file hashes in the document; aggregate numbers only, labelled n = 1 local. §6.

**K8 — Basis roles (C-B1).** Every `## Basis` item tagged `axiom | theorem | hypothesis-checked-in-this-regime
| principle`. CSV priors (`_derived/*.csv`, `habitat_summary_*.csv`, `extra_summary.csv`) enter **only** as
`hypothesis-checked-in-this-regime` — they may parameterize, never certify; a CSV-only derivation must say so.
Statements about adjacency, bands, strata, fiber cardinality, join counts, or level control require the 3D
field channel (`_derived/t0/*.npz` + `*_qc.json` / `*_fiber_*.json` / `*_nv1_*.json`), with band/pair/side
pre-registered in `t0_delivery_index.json`. §6, §1.1.

**K9 — Move-trace legality.** Six columns `| step | move ID | holds/frees | from→to (anchors) | debt |
discharged-at |`; move ids **M1–M14 only** (M15 is a CHECK3 hard failure); every row class-annotated
`(constructive)` / `(certifying)` / `EXEC`; **no EXEC row** carrying π, a discharge, a surprise token, or a
cross-step `[S<n>]` reference. §1.2, §1.3 CHECK7, §2, §5 Gap C.

**K10 — Anchors both directions (CHECK1).** Every trace row's from→to resolves to a real `[S<n>]`; every
`[S<n>]` narrated in `## Derivation` has a trace row. Equations over prose in the derivation body. §1.3, §3.

**K11 — Debt bookkeeping (CHECK2).** Every `debt` entry has a `discharged-at` anchor **or** the literal `OPEN`
mirrored as a Pauli question. A missing substrate is `[OPEN owner: …]` — **never invented** (§6 substrate
firewall). A stale `discharged-at` cell is corrected by a dated note beside the table, never by editing the
cell (R-A1).

**K12 — Hard-core integrity (CHECK6).** Every `;`-separated hard-core clause's symbols appear
word-boundary-matched in some row's `holds/frees` and resolve unchanged in the final state. Clauses with no
extractable symbols are human-held and the Tier-1 section must say so. §1.3, §5 Gap A.

**K13 — §0 invariance declaration** present as `**§0 invariance declaration**` with the three partition cells
`HELD | HELD-UP-TO-GENERALIZATION | FREED`; the guarantee-label demotion rule belongs in
`HELD-UP-TO-GENERALIZATION`. §1.2, §5 Gap D.

**K14 — Pauli question is the strongest open objection, unsmoothed** (C-D3, C-A1..7); `## Known limitations`
carries honest **NEAREST-FIT** declarations (zero declarations on a statistics/spatial substrate is
implausible → suspicious, §5 Gap E); `## Surprise & by-product log (miracles)` present, and **no** shared
distinctive math token with an EXEC row (CHECK7).

**K15 — Values-vs-logic firewall (C-P4).** Oracle numerics confirm **values only**. A `## Checks / Oracle`
subsection that lets a numeric agreement discharge a logical step → REWORK. M14 rows must be certifying and
value-scoped.

**K16 — Vacuous-hypothesis hardening (C-P2).** Any assumption that could absorb any outcome must be tightened
until it can fail, or carried as declared debt. Gate readings in particular must state what a *fail* would
have looked like.

**K17 — State discipline.** `State:` ∈ {sketch, footprint-checked, oracle-checked, settled}. No file is
`footprint-checked` until its `VERIFY_` exists with a fresh exit-0 lint (§7 barrier). `oracle-checked`
requires a fresh-context verifier to have **re-run** the oracle (R-A2); a corrected attestation alone does
not promote. Peer/agent output enters as OPEN until footprint-checked by a fresh context (C-P3).

**K18 — Companion `VERIFY_<name>.md`** exists, written by a non-writer, with sections `## Overall verdict` /
`## Check 1 — Fresh lint` / `## Check 2 — Anchor spot-check` / `## Check 3 — v2 purity grep` /
`## Check 4 — Debt consistency` / `## Check 5 — Honesty flags` / `## Verdict`. §3, §5 Gap G.

**K19 — No carry-forward without basis (C-D1); axiom-hood is regime-scoped (C-D2).** No verification inherited
across regimes (e.g. a synthetic-fixture result reused as certified on the real datum without re-derivation).

**K20 — Staged mutations not pre-adopted.** No `M15`, no M-B attestation ladder values, no upstream
`provenance:` vocabulary (`fetch | pdf-text | eq-verified`) in place of the habitat one. §4.

## C. Judge-specific additions for this round (Codex variant cross-grading)

**X1 — Failure-class consistency.** Each derivation's asserted failure modes must be consistent with the
native-sampling variant's failure-class table; a derivation that treats a variant-listed failure class as
impossible, or silently outside its σ, is at best ACCEPT-WITH-DEBT.

**X2 — Coordinate contract.** Statements about adjacency, bands, margins, or registration must be stated in a
coordinate frame the variant's contract admits (native vs resampled), and must say which.

**X3 — Better carried in Lean.** If a statement is a finite, checkable structural fact now realized as a
`DataChecks.lean` object (e.g. `crossPairs`, `WithinStratumMoves`, scalar-order transport, positive-weight
statements), the judge names that object; the derivation keeping it as prose is debt, not error.

**X4 — Dated snapshot.** A derivation citing **626 audited theorems** predates the PR #3 merge (now 658).
This is a dated snapshot, **not** an error — record it, never grade down for it. Grade down only if the
derivation asserts 626 is the *current* count or leans on the count's stability.

## D. Cross-derivation contradiction sweep (what I will look for)

1. **Registration error (1.0 mm)** — is it *given* in one file and `[OPEN]` in another? Same margin arithmetic
   must not be both premise and open substrate across the set.
2. **Gate verdicts** — one file calling a gate *passed* that another calls *outside_scope* / *not run*.
3. **Band/pair/side pre-registration** — inconsistent claims about what was pre-registered in
   `t0_delivery_index.json` before testing (RQGM 015/016).
4. **n_eff / spacing / censuses** — the same aggregate quoted with different values or different source files.
5. **Provenance divergence** — the same number carried as `executed` in one trace and `fixture` /
   `synthetic-oracle` in another.
6. **Attestation divergence** — one file `corroborated` on an oracle another file calls absent.
7. **Envelope divergence** — one file treating a statement as descriptive that another treats as inferential.

## E. Ranking rule for open items (fixed before evidence)

Open items are ranked by **how soon resolving them would move the T0 claim envelope**, i.e. by
(i) whether the item currently blocks a gate from being *readable at all*, then
(ii) whether it is the sole reason a statement is descriptive-only rather than feasibility-grade, then
(iii) whether it is mechanically dischargeable in-repo (an oracle or a Lean object) versus requiring new data,
then (iv) breadth — how many derivations it unblocks at once.
Items requiring n > 1 rank last by construction: no amount of work on them can move a T0 envelope that
forbids cross-patient statements.

## F. Revision record

- 2026-09-09 — created by the judge before reading any `rs_*` derivation, any `VERIFY_*` file, or the Codex
  native-sampling variant. No later edits: the key is frozen at the moment of writing.
