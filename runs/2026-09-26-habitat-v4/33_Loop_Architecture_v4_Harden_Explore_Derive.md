# Loop architecture v4: harden, explore, derive, and the router between them

- **Version:** loop-v4.3 (design review; not yet run on a task; v4.1 = v4 plus peer review 4, §12.1; v4.2 = enforcement wiring, cost model, rethink, §8, §14-§16; v4.3 = peer reviews 5 and 6 applied, §12.2-§12.3, §14-§16 amended) · **Date:** 2026-09-26 · **Owner:** methodology
- **Formal status:** `verified_conditional` (unchanged). **Scientific status:** `not_claimable` (unchanged). Nothing
  here upgrades any claim about habitats, nulls, or the local samples.
- **Supersedes, for the loop mechanism only:** `26_Territory_Hardening_Loop_Protocol.md` (thl-v1) and the v1-era
  slot/gate vocabulary used by `loops/rqgm-*-001..007`. Doc 26's G6/G7, family registry and two-tier memory are
  carried into v4 (§4, §6); its filled T2 initiator is re-expressed in `loops/INITIATOR_habitat.md`.
- **Reference implementation read:** `F:\git\rqgm-loop` at `main` 471b786 (v1), branch
  `claude/rqlm-loop-epoch-strengthen-8c32b8` 24663bd (v2), branch `claude/peer-agent-input-review-514dab` 99d3910
  (v3.1: `skills/rqgm-loop/SKILL.md`, `DESIGN.md`, `rqgm_check.py`, `runs/2026-09-25-peer/REPORT.md`).
- **Doc number:** 29 is taken on `claude/lean-refinement-2026-09-14`; 30-32 are taken or reserved on
  `claude/hypothesis-lemma-validation-9e44e3`. 33 is the first free number across all branches on 2026-09-26.
- **Enforcement:** `loopkit/` (this directory) implements §8; `loopkit/tests/` are its behavioural spec.
- **Operational contract:** `.claude/skills/rqgm-habitat/SKILL.md` (repo root) is the paste-ready form of §1-§7.

## Evidence labels

Every mechanism row below carries one of:

- **measured (habitat run)**: seen in a logged run in this repo. Named: `rqgm-null-001` … `rqgm-realsample-007`
  (`loops/`), `rqgm-thl-006`, and `rqgm-relations-2026-09-25` (on branch `claude/hypothesis-lemma-validation-9e44e3`,
  `substrates/habitat_relations/loops/`; not on master as of this date). Each is n = 1, one model family.
- **measured (reference pilot)**: the `rqgm-loop` v3.1 study, `runs/2026-09-25-peer/REPORT.md`: 10 scored runs,
  two tasks, one model family, sealed oracles, n = 1 per cell.
- **literature**: a paper whose abstract or text was read on 2026-09-26 (§17).
- **design-only**: reasoning. Every v4 mechanism is design-only until a v4 run logs it.

Labels are never upgraded in place; a later run appends a `correction` record and a dated note here.

## 0. Why redesign (three findings, each measured)

1. **A loop must earn its cost.** In the reference pilot, one strong agent in one pass matched or beat every loop
   arm on both tasks at about 1/40 of the subagent tokens, and the v3/v3.1 arms exhausted their call cap on the
   report task while a single agent finished it. No arm ever declared DONE on a failing artifact. *[measured
   (reference pilot)]* Consequence: a loop is admitted only on criteria a single strong pass demonstrably fails (§3).
2. **Prose rules do not hold under 179 agents.** The relations loop's own final report records that its
   parent-diversity rules were broken in every one of epochs 21-25, that every child of those epochs descended from
   one seed, that the red-team bank froze at its cap after epoch 11 so 16 of 26 probe modules never scored anything,
   that a single structure-matched seed decided verdicts, and that the rung never left E1 in 25 epochs. *[measured
   (habitat run)]* Consequence: any rule that was broken in a logged run is promoted to code where a shell exists,
   and a candidate that breaks it is void at write time, not at review time (§4, §5, §8).
3. **Three loops were wearing one vocabulary.** The seven DerivationLab runs harden one artifact; doc 26 proposed a
   portfolio search that never ran; the relations loop searched a frontier but kept a single "best" and a
   single-artifact rung ladder, so its exploration mechanisms (archive, niches, two generators) fought its
   selection rule (one incumbent). *[measured (habitat run); design-only for the diagnosis]* Consequence: three
   loop kinds with distinct objects and success predicates, joined by a typed router (§1).

The evaluator is the bottleneck in every self-improvement loop, and improvement quality tracks the strength of the
signal it uses, from formal verifiers down to self-assessment *[literature: 2607.07663]*. v4 therefore makes the
evaluator's kind a first-class field of every criterion (§2) rather than a property of the loop.

## 1. The three loops and the router

| loop | object | success predicate | selection | memory | admitted when |
|---|---|---|---|---|---|
| **HARDEN** (RQGM proper) | one artifact (a document, a module, a derivation set, a spec) | `DONE` holds under the final rung, no required `[OPEN]`, held-out judges pass | blind pairwise vs *best*; keep only real, non-regressing gains; fail closed | `archive.jsonl`, single writer | a single strong pass fails ≥ 1 required criterion (§3) |
| **EXPLORE** (portfolio / quality-diversity) | a *set* of candidates over declared families | a frontier predicate (§4.1) **and** at least one candidate passing an admission predicate for HARDEN | archive with niches (family × simplicity); two lanes (hot / cold); pre-registered roots × depth grid | `archive.jsonl` private to generators; `GROUNDING` public | the frame is in doubt: no candidate family is favoured by evidence, or HARDEN halted on STALL/OSCILLATION with every variant in one family |
| **DERIVE** (first-principles derivation) | one derivation file and its companions | `State` reaches `footprint-checked` or `oracle-checked` by the pin's rules; lint exit 0; VERIFY exists; defeater panel finds no VALID rank ≤ 3 | claim-grain micro-loops (writer ↛ refuter); oracle values only | the derivation's own `## Revision record` + a `derive` record in the loop archive | a claim-bearing artifact rests on a derivation that is `sketch` or has an unclassified basis item |

**The router** sits between "a critic produced a finding" and "the next epoch starts". Findings are typed at the
moment they are logged, and the type fixes the response and its blast radius *[literature-adjacent: upstream
`staging/process-upgrades/LOOPGRAPH_V2.md`, staged, not adopted upstream; adopted here as habitat-local]*:

| finding type | detected by | response | scope | loop |
|---|---|---|---|---|
| `defeater-valid` | defeater judge or E2 evaluator: VALID against a required claim, any rank | **every** valid defeater blocks acceptance of the claim and its dependents; rank orders repair only *(v4.1, peer rank 4)*; claim-grain micro-loop, ≤ 3 rounds, fresh refuter each round; exhaustion = `unresolved`, never pass | one claim / row / cell | DERIVE |
| `unsupported-required-claim` | Verifier or Check: required evidence absent | mark unchecked/unsupported; suspend dependent acceptance; mathematical gaps → DERIVE, empirical gaps → evidence repair | one criterion | any |
| `contract-or-assumption-mismatch` | a `lean`/`command` result whose statement, units, grid, band or side does not match the criterion | `suspend` the result for that criterion (result preserved); repair the mapping or request an `amend` | one criterion | any |
| `stale-or-contaminated-evidence` | version mismatch, or documented exposure of a held-out prompt | invalidate affected evaluations; replace held-out prompts by human setup; recheck dependents | affected checks | any |
| `budget-or-provenance-violation` | reservation exceeded, or a record that cannot be tied to a version | refuse dispatch/keep; HALT(BUDGET) or reconcile; never reconstruct an audit trail silently | the run | any |
| `measurement-inconclusive` | typed ERROR/timeout/out-of-scope | keep distinct from failure; one pre-registered retry, then `unresolved` | one evaluation | any |
| `wrong-anchor` | content confirmed, pointer wrong | single-anchor re-verification agent | one citation | DERIVE |
| `frame-exhausted` | G6 fires 3× in a rung, or HALT(STALL) with every variant of the last 3 rounds in one family | re-open EXPLORE with the exhausted family **excluded** and the archive withheld | the family registry | EXPLORE |
| `substrate-missing` | Verifier: not-found; harness: abstention at base on a required case | `[OPEN owner: …]`; HALT(OPEN) if the criterion is required | one criterion | any |
| `instrument-defect` | evaluator shows a gate is vacuous, a probe is invalid or saturated, a scorer drops a case | instrument change request; applied only at the next epoch boundary with a version bump (§5) | one instrument | any |
| `cross-doc-contradiction` | the same anchor carries different status in ≥ 2 files | propagation sweep over every file sharing the anchor, after the fix lands | all companion files | DERIVE / HARDEN |
| `canary-passed` | a planted-defect criterion passes (§2.3) | HALT(CANARY): the pipeline is gaming; human only | the run | any |
| anything else | — | defer to the epoch boundary (v1 static behaviour) | — | — |

A route is a record (`route{finding, type, response, scope, spawned, observed_at, processed_at}`) so an auditor can
check that no finding of an interrupt class waited for a boundary and that no mid-epoch instrument change happened.
**Interrupt** means "suspend affected acceptance and dependent work now"; it does not mean "spawn a repair agent
now" *(v4.1, peer §2)*: schema errors route mechanically, citation and propagation fixes batch at boundaries, repeated
findings are deduplicated, and nested repairs charge the parent run's budget. "Anything else" is an explicit
`unresolved` category that blocks affected acceptance until classified; it is never permission to exit.

## 2. The evaluator ladder

### 2.1 Kinds

Every `DONE` criterion carries `kind`, fixed at setup, from a strict ladder:

`lean` (kernel-checked theorem; `lake build` + `lake exe auditAxioms`) > `command` (a deterministic script the loop
never edits: `score_variant.py`, `lint.py`, an oracle, pytest) > `source` (the Verifier against a primary source it
read) > `judges` (a blind preference or pass/fail mark by separate agents) > `self` (the generator's own claim; never
a pass).

Rules *[design-only; literature: 2609.02246 "acceptance checks outrank the teacher"; 2607.07663 hierarchy]*:

- A lower kind never **rewrites** a higher kind's result. Judges never mark a `command` criterion; a `command` result
  never overrides a `lean` result. Where a criterion could be `command`, it must be: a `judges` criterion that a script
  could decide is a setup defect (an `amend` fixes it).
- **Authority is criterion-scoped and conditional on instrument validity and assumption applicability** *(v4.1, peer
  rank 1)*. A Lean theorem establishes its proposition under its formal assumptions, not that the proposition encodes
  the criterion; a scorer establishes its programmed checks, not that they measure the right thing. Any supported
  challenge from any kind (a `contract-or-assumption-mismatch`, `stale-or-contaminated-evidence` or
  `instrument-defect` route) **suspends** the result's use in acceptance for that criterion (`suspend{criterion,
  result, challenge}`); the original result is preserved, never turned from pass to fail. No keep or completion may use
  suspended evidence until an `unsuspend` with evidence. A `command` criterion therefore names its contract: the
  cases it covers, its aggregation rule, the scorer and case-manifest identities, and the calibration it passed; a
  scorer change starts a new evaluation cohort and incumbents are re-scored before any comparison.
- "Preferred" is not "passes". Pairwise wins move *best*; only a Check under the criterion's own kind changes a
  criterion's value. The relations loop's 16/16 pairwise wins beside a failed absolute Check (reference meta-run) and
  its 7/11 front that never met DONE are the same distinction *[measured (reference pilot); measured (habitat run)]*.
- Every Check reports each criterion's value **and kind**; Output lists pass/fail/unchecked/waived by kind.
- Cross-family judges where available: same-family panels favour same-family candidates by 3.4-8.4 points and
  55.4 % of AB/BA pairs reverse *[literature: 2609.17857]*. In this repo the second family is the ChatGPT peer
  (§12), used for design review and held-out marks, never as a generator.

### 2.2 Typed evidence for the Verifier (fixes reference defect 1)

A new claim is `empirical` (needs a primary source or an executed record under `_derived/`), `mathematical` (needs a
derivation file or a Lean object; a citation is not enough), or `proposed` (a mechanism or design; needs a
`design-only` label and its assumptions, never a source). The Verifier returns **findings**; it never edits a
candidate. A correction is a new candidate that is re-gated. Verifier assets (check files, oracles, judge keys,
held-out prompts) are listed in `setup.assets` and are immutable; target files under repair are not assets even when
a command reads them (fixes reference defect 2).

### 2.3 Canaries

Each run plants ≥ 1 canary as a **matched valid/defective pair** evaluated through the same acceptance path *(v4.1,
peer §3)*: a valid control the pipeline must accept and a defective twin it must reject or leave unresolved (a
derivation identity with and without an essential hypothesis; a complete synthetic fixture and one that omits the
hardest case yet scores higher; two specs differing by one contradictory required transition). One known-bad case
alone cannot tell a working evaluator from an always-rejecting one. Canary outcomes are logged separately from the
target's quality and are never optimization targets. A pass on the defective control → HALT(CANARY): an integrity or
calibration failure, not proof of intent *[literature: 2609.02246 canary cases; design-only here]*. The relations loop
had the inverse instrument (planted twins for power) but no gaming canary.

## 3. Admission: a loop must beat one strong pass

Before any loop starts, the orchestrator runs **S**: one strong agent, one pass, the same `GROUNDING`, a budget equal
to two loop rounds, no deliberative judges during generation. S's output is then Checked under **the same acceptance
contract as loop output** *(v4.1, peer rank 3)*: each required criterion by its own kind at its required scope
(`judges` criteria by three fresh judges against a key written before reading; stochastic `command` criteria by a
pre-registered replication plan, never by re-sampling until a pass). The loop is admitted **only on the required
criteria S fails**. A criterion is **protected** only after S receives a valid Check at that criterion's required
acceptance scope; protection covers required final behaviour and declared invariants, not every intermediate feature
of S, and is re-checked after changes to its dependency closure. Unchecked or uncertain required criteria never permit
completion and stay eligible for repair. If S passes every required criterion the run exits `COMPLETE(S)` under the
same final contract (held-out marks for `judges` criteria included). `admission{s_version, s_check, admitted_criteria,
budget_frontier}` is the archive's second record after `setup`. *[measured (reference pilot) for the motivation;
design-only for the rule]*

For EXPLORE, S is one strong agent asked for K candidates covering **every mandatory family** in one pass; EXPLORE is
admitted only if the frontier predicate (§4.1) fails on S's set **or** no S candidate is `eligible_for_harden`.
Two predicates are distinct *(peer §4)*: `eligible_for_harden(c)` = c passes every hard invariant and at least one
required criterion by a `command` or `lean` kind; `needs_harden(c)` = c fails ≥ 1 required criterion. A candidate that
passes all required criteria bypasses HARDEN; a diverse frontier with no eligible candidate has not met EXPLORE's
success predicate.

## 4. EXPLORE: frontier, lanes, slots, grid

### 4.1 Frontier predicate (doc 26 §2.5, kept)

```json
{"families_represented": {"min": 4}, "non_favoured_family_present": {"min": 1},
 "clustering_max_share": {"max": 0.34}, "void_returns": {"max": 0},
 "blocked_routes_recorded": {"each_names_a_wall": true}}
```

The **F6 slot is mandatory**: a portfolio that returns only the pentad has confirmed it, not tested it. "No agent
could propose a family outside the pentad" is a finding and a `family{novel:false, reason}` record, never a pass.

### 4.2 Exploration / exploitation lanes (a heuristic, not parallel tempering) *[design-only]*

Two lanes run per epoch. Both obey the **hard invariants** (no identifier leak, no shared-module edit, finite base
values on every required case, no `must_not_change` breach). The **hot lane** admits a candidate on novelty (a new
family or an empty niche) and may temporarily fail optimizable quality gates, so it can cross a proxy-quality valley;
it never enters the accepted frontier. The **cold lane** runs the full gates and judges. Transfers: a hot-lane
candidate that passes a full cold Check migrates with its ancestry and evaluation versions; a cold-lane stall of 3
epochs draws its next parent from the hot lane's best-novelty candidate. The name "parallel tempering" is not used
*(v4.1, peer rank 8)*: no energy, temperature or swap kernel is specified, and free-form proposals supply no proposal
probabilities; 2606.10587 is the motivation for keeping an exploration lane, not a claim of equivalence. Diversity
collapse under an optimizer is the documented failure the hot lane exists to prevent; the relations loop's "every
child of epochs 21-25 descends from v03" is the local instance *[measured (habitat run)]*.

### 4.3 Slots (mechanical; fixes the broken parent rules)

Each epoch has fixed slots. Slot **a** takes a parent outside the favoured lineage (declared in `setup.favoured`);
slot **b** takes any parent the operator allows. Rules checked by `loopkit slots` from the child's declared header
before it is scored: no operator on its own child; no shared parent within an epoch; the favoured subtree holds at
most ⌈K/3⌉ of a rung's slots; a rejected parent needs a stated reason; a bit-identical headline to the parent is a
duplicate. A child that fails is `void` at write time and never reaches an evaluator. The relations loop left these
rules to each generator's docstring and they were broken in every epoch of 21-25 *[measured (habitat run)]*.

A header **asserts** a parent and a root; it cannot establish them *(v4.1, peer rank 7)*. `loopkit audit` re-derives
every root transitively from committed `version{id, parent}` records and voids a slot whose declared root or parent
differs (`ROOT_MISMATCH`, `PARENT_MISMATCH`). Root diversity and semantic family diversity are enforced separately:
families come from a versioned registry (`family` records) with adjudicated assignments, never from the header alone.
Quota populations are named: the ⌈K/3⌉ cap applies to a rung's **slots**; the frontier's 0.34 share applies to the
**evaluated population** as ⌊0.34 × N⌋. An infeasible allocation returns `blocked`, never a silent relaxation. "No
operator on its own child" forbids consecutive application of the same operator id along a lineage.

### 4.4 Budget frontier (fixes "25 epochs deep on one lineage")

An EXPLORE run pre-registers a **roots × depth** allocation in `admission.budget_frontier` (for example 4 roots × 6
epochs rather than 1 root × 25): the ranking of search strategies changes with the budget split and the best depth
is often well below the customary one *[literature: 2609.19799]*. The allocation is chosen **before any candidate
exists** from a total cost ceiling, the reserve for the final Check and held-out, and the mandatory family coverage
(roots ≥ mandatory families) *(v4.1, peer §5c)*. Epochs are unequal units when evaluation or DERIVE costs differ, so
the record carries the priced allowance per root, not only counts. A run reports the whole allocation it spent and
its coverage, valid front additions, false completions and total cost, never front moves alone (which reward churn).
Depth on one root beyond its cap needs `amend{budget}`; any adaptive reallocation is a pre-registered policy.

### 4.5 Rungs for EXPLORE escalate diversity as well as stringency (doc 26 §6, kept)

E1 ≥ 3 families · E2 ≥ 4 families and no family above ⌈K/3⌉ · E3 ≥ 1 family outside the pentad · every
surviving candidate traced to a family and a seed. Escalation is human-only below the final rung, as in HARDEN.

### 4.6 Hand-off

A cold-lane candidate that passes HARDEN's admission predicate (§3) becomes a HARDEN `TARGET` with the EXPLORE
archive **withheld** from its generators (doc 26 §5 two-tier memory): `loopkit brief` writes the generator brief from
`GROUNDING` and the candidate alone.

## 5. The red-team bank as a versioned instrument

The relations loop evolved the evaluator through data (probe modules), which is the right mechanism, and then froze
it at a cap *[measured (habitat run)]*. v4 gives probes a lifecycle and a version *[design-only; rails from upstream
`staging/instrument-versioning.md`]*:

| state | entry condition | exit |
|---|---|---|
| `proposed` | written by the red-team agent, who never scores | calibration |
| `calibrated` | passes its **probe-specific acceptance intervals, declared before activation** *(v4.1, peer §6)*: (i) no false alarm on a valid negative control; (ii) fires on an **independently constructed** defect of the same class, not only the author's seeded one; (iii) its influence on unrelated measurements (the planted twin among them) stays inside a declared, unit-bearing tolerance; stochastic controls state repetitions and uncertainty | activation |
| `active` | activated **only at an epoch boundary**, with `bank{version, added, retired}`; every scored candidate records `bank_version`; eligible incumbents are re-scored under the new cohort before any comparison | dormancy, saturation or invalidation |
| `dormant` | zero firings across 2 epochs on the candidate distribution → dormant **with a reactivation condition**, never silently deleted; a probe marked `core` (it guards a required failure class) is never dormant | reactivation |
| `saturated` | retired only after an independent challenge case shows zero discrimination and another active probe covers its defect class | — |
| `invalid` | fails calibration, or errors → never loaded; a probe that fires on the planted twin first challenges the twin's validity | — |

The cap bounds **active** probes only; dormancy and retirement free slots, so the bank never freezes. A probe that has
never been calibrated is never loaded by the scorer. Redundancy is measured on the calibration matrix (per-probe
detection vectors): identical columns keep the cheaper representative active and the other dormant. A harness
execution error is `ERROR`, never a calibration failure. A red-team agent's brief carries the front's summaries and code, never
the scorer's per-seed values (else it aims at seed luck). Scorer changes obey the same rule: versioned, boundary-only,
re-baselined on a fixed anchor set (the seeds v00-v05 and the six T2 synthetic geometries).

## 6. Memory: one archive schema for three loops

`archive.jsonl`, append-only, one writer (the orchestrator), one JSON object per line `{"t": <type>, …}`; unreported
values are `null`, never estimated. v4 is a superset of the project's existing records (`version`, `utility`,
`epoch`, `decision`, `substrate`, `eval`, `finding`) and of v3.1's (`setup`, `round`, `citation`, `probe`, `check`,
`amend`, `approve`, `rung`, `heldout`, `exit`, `resume`). New in v4:

```
setup{loop:"v4", kind:harden|explore|derive, target, grounding, done{criteria[{id,required,kind,test,command?,files?}],
      must_not_change, final_rung}, assets[], favoured?, budget{epochs,rounds,tokens|null,minutes|null}, canaries[]}
admission{s_version, s_check{id:value}, admitted_criteria[], budget_frontier{roots,depth}|null}
slot{epoch, slot:a|b, child, parent, root, operator, parent_operator, in_favoured, verdict:ok|void, reason?}
lane{epoch, child, lane:hot|cold, event:admit|migrate|draw}
family{agent|child, family, novel, redirected_from?, reason?}
bank{version, epoch, added[], retired[]}   probe_state{probe, state, evidence}
route{finding, type, response, scope, spawned[]}   canary{id, planted, outcome}
instrument{name, version, changed_at_epoch, why, anchor_rebaseline}
derive{file, state_before, state_after, lint_exit, verify_file, defeaters{valid, rank1}}
correction{record, why}
suspend{criterion, result, challenge, by}   unsuspend{criterion, result, evidence}
```

Every keep, halt and exit must be reconstructable *(v4.1, peer §7, rank 5)*: a `check` names the artifact identity it
checked (`version` id, and a content hash where a shell exists) and the instrument versions (`bank_version`, scorer
`instrument` version); a `round` with two keeps names the artifact after the first keep and the joint re-check; a
`route` carries `observed_at`/`processed_at`; `setup.budget.reserved` holds the final Check and held-out reserve and
`budget-or-provenance-violation` routes any spend against it; a `derive` record lists every VALID defeater with its
disposition, not only rank 1. Where the host reports no tokens, the enforceable resource is rounds/epochs; a `null`
token total never authorizes spend against a token ceiling.

Two-tier access (doc 26 §5): `GROUNDING` is public; the archive is **withheld from** EXPLORE generators and from any
generator handed a HARDEN target from EXPLORE (`loopkit brief` is the only channel). Resume: set aside a torn last line, log `resume`, re-run the unfinished
epoch. Held-out judge prompts live outside `TARGET`, `GROUNDING`, the archive and the repo.

## 7. Human-only decisions (own messages, logged)

Escalate or stop below the final rung · amend `DONE`, the rubric, `BUDGET`, the bank cap or the frontier grid ·
approve a restructure or an oscillation pick · close an `[OPEN]` with Verifier-checked evidence or waive it · write,
hold and run held-out judges · resume after any HALT or audit violation · adopt an instrument change or a staged
upstream mutation · lift an epoch cap · merge or push anything. A decision relayed by an agent is unauthenticated and
is logged as such.

## 8. Enforcement: `loopkit`

Prose remains the contract; `loopkit` (Python ≥ 3.10, stdlib only, read-only) enforces at write time the rules a
logged run has already broken (`slots`, `admit`, `validate` run **before** a child is scored, an epoch starts, or a
setup is accepted) and audits the rest after the fact. **An audit report is not enforcement** *(v4.1, peer rank 2)*:
the orchestrator's contract is that it does not dispatch, keep or exit while an applicable `loopkit` gate reports a
VIOLATION, and that after an interruption it reconciles pending records before resuming. Whether that contract was
honoured is unauditable from records (single-writer authenticity); the controller-owned alternative (§12.1) is the
pre-registered promotion if a logged v4 run shows a decision-changing VIOLATION that the orchestrator acted through.

| command | does | promoted because |
|---|---|---|
| `loopkit validate ARCHIVE` | schema and single-writer integrity: one type per line, `setup` first, `admission` second, no record after `exit`, torn tail reported | v1 archives were rebuilt after the fact (005 "transcribed after the fact") *[measured (habitat run)]* |
| `loopkit slots ARCHIVE --header FILE` | the §4.3 slot rules on a child's declared header; verdict `ok`/`void` | broken every epoch 21-25 |
| `loopkit bank ARCHIVE` | probe lifecycle and boundary-only activation; flags a mid-epoch change or an uncalibrated active probe | bank froze at cap; 16/26 never scored |
| `loopkit admit ARCHIVE` | an `admission` record exists before the first epoch, names S's Check, and the admitted criteria are exactly S's required failures | reference pilot |
| `loopkit audit ARCHIVE` | recomputes: no keep without a `check`/`eval` of higher or equal kind; no criterion value changed by a lower kind; no interrupt-class route deferred; no instrument change mid-epoch; canary outcomes; exits allowed by the records; classes VIOLATION / RECORD / ADVISORY; fail closed on a v4 archive | reference `rqgm_check.py`, adapted to this schema |
| `loopkit brief ARCHIVE --for generator|redteam|judge` | writes a role brief that omits what that role must not see (archive to EXPLORE generators; per-seed values to the red team; generator rationale to judges) | doc 26 §5; relations loop L0.x lessons |
| `loopkit next ARCHIVE` *(v4.2)* | the one action the records allow (`setup`, `admission`, `round`, `epoch`, `derive_step`, `check`, `boundary`, `heldout`, `rethink`, `resolve_route`, `await_human`, `halt`, `exit`, `done`, `audit_violation`, `policy_invalid`); a pure function of archive + policy that decides **transitions, never verdicts**; writes `<loop>/.next.json` with an id | peer rank 2, bounded form: the orchestrator cannot invent a step |
| `loopkit append ARCHIVE '<json>' --decision ID` *(v4.2)* | the **only writer**: refuses an unknown or incomplete record, a record whose append would add a VIOLATION, a human-only record without `by: "human"`, and any decision-bound record (round, epoch, check, heldout, exit, halt, rung, slot, bank, admission, rethink) whose `--decision` id does not equal the last `next` id or whose `.next.json` is stale; atomic append with fsync | peer rank 2 and §7: single-writer integrity at write time |
| `loopkit policy [LOOP_DIR]` *(v4.2)* | the loop's parameters as data: `loopkit/policy_default.json` merged with `<loop>/policy.json`; validated; its hash is bound in `setup.policy_hash` and `next` refuses a changed policy without an `instrument` record at a boundary | peer §10: no rewriting of objectives or operators inside a cohort |
| hooks (`loopkit/hooks/gate.py`, wired in `.claude/settings.json` with `$CLAUDE_PROJECT_DIR`) *(v4.2)* | PreToolUse denies any direct Write/Edit of `loops/**/archive.jsonl`; PostToolUse checks a variant's slot header under a `LOOP` marker and blocks a void child, validates `policy.json`; SubagentStop audits active loops and surfaces VIOLATIONs | the harness calls the gate, not the model; works in every worktree |
| `loops/loop_v4.js` *(v4.2)* | a generic Workflow driver with no loop-specific logic: a cheap gate agent relays `next`, role agents receive `loopkit brief` and return schema-typed JSON, results go through `append --decision`; stops on `await_human`, `boundary`, `rethink`, `resolve_route`, `heldout`, `audit_violation` | scripts have no filesystem; loopkit cross-checks the relay, so a mis-relay cannot advance the loop |
| `loopkit selftest` | fixtures under `loopkit/tests/fixtures/` (85 tests incl. hook pipe tests) | — |

What is still discretionary after v4.2: the orchestrator may run steps by hand from a session instead of the driver,
and a role agent may ignore its brief. Both leave records (`next` ids, briefs are regenerable), so the audit can
show a step that no `next` allowed; it cannot show a brief that was not read. Promotion to a controller that owns
the agents stays the pre-registered next step (§12.1).

Unauditable from records: held-out secrecy, role separation, relay authenticity, whether a "fresh context" was fresh,
section boundaries, and whether a human really wrote a human-only message. `loopkit` never decides and never writes
anything but an audit report.

## 9. Kept, changed and not adopted from the reference v3.1

| item | v4 | why |
|---|---|---|
| fail-closed, UNKNOWN never supports, ERROR retried once | kept | reference pilot: zero false completions |
| per-rung 5-call probe | **once per run**, at setup | the pilot's T2 loss was fixed overhead (probe + re-probe + strict mode) |
| one keep per round | **up to two non-conflicting keeps**, the second re-judged against the new *best* | the pilot's T2: the variant fixing the other half of the report lost the length tie-break and never returned |
| escalation pauses at every rung | pause only below `final_rung`; `final_rung` may be E1 for a run the human declares so | escalation was pre-authorised in the relations loop and still never happened; the pause, not the rung, was the cost |
| primary-source-only Verifier | typed evidence (§2.2) | reference defect 1; this repo's claims are mostly mathematical or proposed |
| check files belong to DONE | assets vs targets (§2.2) | reference defect 2 |
| budget "twice the costliest round" | admission reserves the final Check and the held-out run explicitly (`budget.reserved`) | reference defect 4 |
| waived [OPEN] → Stop | waived [OPEN] → Check at the final rung, then Stop | reference defect 5 |
| E4 "red-team re-verifies every number" | not restored as a rung; the bank (§5) and `command`-kind criteria are the red team | E4 was the rung nobody reached |
| per-call keys, owning controller | deferred | no logged v4 resume has re-run completed calls; no shell-less host here |
| `rqgm_check.py` verbatim | not ported; `loopkit audit` is written to this schema | the project's records differ (epochs, families, bank, lanes) |

## 10. Where the existing runs land

| run | v4 kind | what v4 would have changed |
|---|---|---|
| rqgm-null-001, -marked-002, -relational-003, -mrpfm-004 | HARDEN (Lean-kind criteria) | admission: a single strong pass would have caught several of the 20 epoch-1..20 findings first; canary absent |
| rqgm-nullkit-005 | HARDEN (command-kind) | archive transcribed after the fact → `validate` would flag; personas not recoverable → RECORD |
| rqgm-thl-006 | EXPLORE (aborted after epoch 8) | frontier predicate; F6 slot; the self-adjudicated distinctness verdict (epoch 5) becomes an `instrument-defect` route |
| rqgm-realsample-007 | HARDEN + DERIVE (five `rs_*` derivations) | claim-grain micro-loops for the `[S11]`/`[S4]` findings instead of whole-document epochs |
| rqgm-relations-2026-09-25 | EXPLORE with a cold-lane HARDEN hand-off that never triggered | slots, lanes, roots × depth grid, bank lifecycle; the 7/11 front would have been reported as an EXPLORE frontier, not as a failed HARDEN |

## 10a. Which loop for which task (v4.3, adopted from peer 6 B8)

| task | default | admitted to a loop when | evaluators that dominate | stop | watch for |
|---|---|---|---|---|---|
| claim-bearing document with derivations (doc 28 shape) | one strong pass; HARDEN with bounded DERIVE dependency repairs | an independent Check finds a required unsupported claim, contradiction or invalid dependency | derivation/formal checks for logic; sources for empirical claims; commands for structure; judges for claim-to-evidence correspondence | required claims supported at the stated scope, companion sweep complete; else scoped unresolved/budget exit | polished prose outrunning the derivation's assumptions |
| executable null layer with tests and Lean policy (nullkit shape) | one pass for a bounded edit; HARDEN for observed failures; DERIVE for validity lemmas | an independent invariant/null calibration or integration check fails | executable controls and formal policy checks, plus review that the implementation realizes the formal contract | frozen synthetic acceptance suite and linkage obligations pass; unresolved calibration blocks | tests certify behaviour while the null's validity stays unproved |
| estimand/variant search (relations shape) | EXPLORE only after scorer calibration; HARDEN an eligible candidate | S fails a pre-registered portfolio objective and distinguishable feasible routes exist | synthetic scorer, nuisance controls, uncertainty and coverage rules; semantic review of the estimand | validated objective met or information limit reached; ranking alone never upgrades inference | adaptive search overfitting its evaluator |
| single derivation file | one strong pass plus independent VERIFY; DERIVE if obligations fail | a named required logical, provenance or trace obligation stays unresolved | proof or finite exhaustive check; typed oracle for values; independent semantic review | requested state has all required evidence and a promotion event | an anchor repair breaking another dependency |
| proposal or spec for a peer | one strong pass and focused review; HARDEN only for substantive contract defects | an important ambiguity, inconsistency or infeasible requirement survives review | schema and examples where possible; an independent reader | scope and assumptions explicit; unresolved choices labelled | process rewarding stylistic consensus |
| the loop mechanism itself | one pass on a scoped defect; HARDEN spec/implementation; EXPLORE only over bounded alternative policies | an external frozen failure case exists and improvement is measurable without changing the test | controller tests, fault injection, held-out tasks scored outside the modified loop | pre-registered improvement without regression under equal accounting; else keep the baseline | the candidate changing its own judge, budget or success definition |
| no viable contract | none beyond diagnosis or a separately scoped calibration | required support unavailable, instrument invalid, or target out of scope | evidence-availability and applicability checks | explicit blocked/unresolved result with a return condition | more iterations mistaken for missing evidence |

RSI mechanisms are gated, not default *(peer 6 B9)*: archive parent-sampling only once distinct viable routes exist;
niches only on premature convergence or an explicit alternatives task; the red-team bank keeps calibrated core
controls and grows only after a new failure class; lessons are short, evidence-linked and expire on premise or
instrument change; the playbook rewrite needs a documented plateau and a policy hypothesis, tested against a frozen
baseline; one focused refutation per load-bearing unresolved step. Self-application (task vi) never modifies the
external acceptance standard, sealed cases or keys, the approval root, the audit history, the resource meter, the
budget ceiling or its own permissions.

## 11. Validation protocol (pre-registered, zero model calls in stages 0-1)

- **Stage 0.** `loopkit selftest` passes; every §8 rule has a positive and a negative fixture.
- **Stage 1 (replay).** Run `loopkit slots` over the relations loop's variant headers (`hrel/variants/vE*.py`, on
  the sibling branch). Expected: ≥ 8 void verdicts in epochs 21-25, matching the report's "broken in every epoch".
  Fewer than 5 falsifies the claim that slot rules would have bound. Run `loopkit bank` over its `LOG.md` bank
  changes: expected ≥ 1 mid-epoch or uncalibrated activation.
  **Stage 1 outcome (2026-09-26, measured (habitat run), zero model calls):** `python -m loopkit.tools.replay_relations
  <hrel/variants> --favoured v03 --epochs 21-25` synthesised v4 headers from the variants' docstrings (operator, parent;
  root by parent chain; unknown fields filled conservatively) and returned **void 10 of 10** children in epochs 21-25
  (every epoch: slot a inside the favoured lineage; both slots on root v03; ve24a = M13 on an M13 child; ve25a/ve25b
  sharing parent ve24a), above the pre-registered threshold of 8. Over epochs 1-25 the rules void 48 of 50, but v4's
  slot-a rule did not exist before playbook v5, so only the 21-25 figure bears on the claim. This shows the rules would
  have voided those children at write time; it does not show whether the loop's own rules were applied (peer §10).
- **Stage 2 (admission dry run).** On the next HARDEN target, run S and Check it before any loop. Record the
  admitted criteria. If S passes all required criteria on two consecutive targets, the loop is not run on that
  artifact class until a target defeats S.
- **Stage 3 (frontier).** On a synthetic-only EXPLORE target with a sealed scorer, spend one budget as 1 × 12 and
  the same budget as 4 × 3; report counted front moves per agent call for both. No "improved" claim unless 4 × 3 is
  at or above 1 × 12 on the frontier predicate.
- **Stage 4 (spirit / kernel / full, v4.3, peer 5 §1.2).** Four synthetic tasks (a module with sealed tests; a
  prose contract with a planted cross-section contradiction; a portfolio search with an attractive single-seed
  shortcut; a workflow receiving a scorer correction after a keep) × three arms (concise "use RQGM/RSI" guidance
  plus the acceptance contract; the same plus the enforced acceptance/provenance kernel; full v4.3) × two
  repetitions = 24 runs, ≤ 18 model calls each including admission, relays, screens, retries and final assessment
  (≤ 432 calls; a 12-run first stage ≤ 216), one pre-registered token ceiling per run, final assessment reserved
  inside the cap. Outcomes: sealed correctness, false completion, successful completion, honest unresolved exits,
  denied invalid transitions, human interventions, elapsed time, billed usage; quality against total cost.
  Mechanical fault injections (stale approvals, omitted cases, forged exit codes, late evidence) cost no model
  calls. Decision rule: if the kernel prevents invalid acceptance at comparable completion and lower cost than full
  v4.3, the kernel stays and the method simplifies; if quotas only raise rejection counts, their benefit is unshown.
- **Primary outcomes** for every stage *(v4.1, peer §10)*: false completion (COMPLETE while a sealed check finds a
  required failure) **and** failure to complete a valid artifact (PARTIAL or HALT on an artifact the sealed check
  passes), so an always-halting controller does not look perfect; secondary: unresolved required claims, coverage,
  total cost. One false completion makes the rule that allowed it checker-mandatory. Results per case; no significance
  claims. Stage 1 shows only that the slot rules **would have voided** those children; it cannot show the original
  rules were or were not enforced, and absent calibration records are not proof of invalid activation. Stage 3
  describes one realization; it establishes no general winning allocation.

## 12. Peer consult

A cross-family review of this document and the skill was requested from the ChatGPT peer on 2026-09-26
(`loops/peer/consult-4-request-loop-v4.md`). The reply is filed verbatim as `loops/peer/peer_review_loop_v4.md`
with a provenance header; its accepted, adapted and rejected items are listed in §12.1 once received. The peer's
review is development feedback for v4.1, not a held-out assessment of it.

### 12.1 Disposition of peer findings

Received 2026-09-26 (`loops/peer/peer_review_loop_v4.md`, GPT-6 Astra, design document only, no code or archives seen;
every item design-only unless marked). Verdict quoted: retain the three modes; revise the acceptance and execution
contract before treating v4 as enforceable.

| peer item | disposition | where |
|---|---|---|
| Rank 1: authority is criterion-scoped and conditional on instrument validity; a challenge suspends, never rewrites | **accepted** | §2.1; `suspend`/`unsuspend` records; `loopkit` `COMPLETE_WITH_SUSPENDED`, `KEEP_ON_SUSPENDED` |
| Rank 2: audit reports alone do not enforce; refuse dispatch/keep/exit on failing gates; reconcile after interruption | **accepted as contract; controller deferred** | §8; the controller-owned variant is the pre-registered promotion (repo rail: prose + read-only auditor, as the reference repo's design panel chose 3/3) |
| Rank 3: S under the same acceptance contract; protect only Checked required behaviour; unchecked never completes | **accepted** | §3; `ADMISSION_UNCHECKED`, `PROTECTED_REGRESSED` |
| Rank 4: every valid defeater blocks; instrument invalidity interrupts; routes record detection and resolution | **accepted** | §1 router; addendum §A-4; `derive.defeaters` lists all |
| Rank 5: hashes, complete results, stable ids, attempt states, ancestry from committed parents | **adapted**: version ids plus optional content hashes; ancestry from `version.parent` (`ROOT_MISMATCH`); per-call attempt ids stay deferred until a logged resume re-runs a completed call | §6; `ancestry_audit` |
| Rank 6: probe-specific tolerances; zero firings → dormancy; core coverage retained; re-score incumbents | **accepted** | §5; `dormant`, `core`, `CORE_PROBE_RETIRED` |
| Rank 7: ancestry from the controller's graph; explicit quota denominators; family registry separate from roots | **accepted** | §4.3 |
| Rank 8: rename lanes; hard invariants vs quality gates; hot lane may cross valleys | **accepted** | §4.2 |
| New router rows (unsupported-required-claim, contract-or-assumption-mismatch, stale-or-contaminated-evidence, budget-or-provenance-violation, measurement-inconclusive); interrupt = suspend, not spawn | **accepted** | §1; `schema.INTERRUPT_ROUTES` |
| Matched valid/defective canary pairs | **accepted** | §2.3; addendum §B-4 |
| `eligible_for_harden` vs `needs_harden`; EXPLORE success needs an eligible candidate | **accepted** | §3 |
| Roots × depth chosen from a cost ceiling and mandatory families; report coverage and cost, not front moves | **accepted** | §4.4 |
| One controller with three modes rather than three loops; DERIVE as a bounded HARDEN subroutine | **adapted**: the three kinds stay as *modes of one contract* (one archive schema, one router, one auditor); DERIVE has standalone entry only for an independently scoped derivation | §1 |
| Instrument calibration is a state with an owner, not a fourth loop | **accepted** | addendum §D |
| Parallel-tempering swap kernel | **rejected** (not needed; the heuristic name is the smaller claim) | §4.2 |
| Held-out judges check S | **adapted**: yes for required `judges` criteria under the final rubric; no as a layer over valid mechanical checks | §3 |
| Do not import: autonomous rubric/playbook rewriting inside a cohort; replica-exchange machinery; a calibration swarm; every upstream stage; per-route human approval; a judge panel everywhere; RSI claims; distributed infrastructure | **accepted**; the STOP meta-agent rewrites the playbook only at a boundary, under a new cohort | §7, §9, addendum §E |
| Stage 1/3 validation claims overstated; add failure-to-complete as a co-primary outcome | **accepted** | §11 |

Disagreement kept visible: the peer prefers a controller that owns transitions; this repo keeps prose + write-time
gates + a read-only auditor until a logged run shows a decision-changing violation the orchestrator acted through
(the same rail as the reference repo's v3 decision and its severity-based promotion rule).

### 12.2 Disposition of peer review 5 (run report, enforcement, cost, rethink; `loops/peer/peer_review_loop_v42_run_report.md`)

| peer item | disposition | where |
|---|---|---|
| Split by consequence and observability, not by "broken last time": enforce what corrupts acceptance, provenance, permissions, budgets; make allocation rules configurable | **accepted**: slot fractions, slot-a novelty, stall thresholds and family exclusion are *policy* (versioned, per-run), enforced only as the run pre-registered them; ancestry truth stays invariant | SKILL §9; `policy_default.json` |
| Narrow five "invariants" (writer may self-check; typed evidence not "truth"; `by: human` is a label until authenticated; identifier scan is defense in depth; assets freeze per cohort, replaceable with rebaseline) | **accepted** as wording; authentication of human approvals **deferred** (no trusted channel exists in this harness; logged as unauditable) | SKILL §9; §7 |
| Promote: independent command-result capture; complete case coverage; dependency-closure invalidation; withdrawal of unsupported keeps; final-assessment reserve | **accepted**: the driver (or a gate agent, never the generator) runs acceptance commands and binds receipts to the candidate hash; `evidence` follows the six-step sequence; `budget.reserved` is required | §15; `loop_v4.js`; `schema` |
| The 24-run spirit / kernel / full experiment (≤ 432 calls) | **accepted as the pre-registered Stage 4** replacing the §11 admission dry run as the primary comparison | §11 |
| §16 mapping corrections (lineage, single seed, sign/robustness split, unit floor, fusion, M21, bank, power, physics, recurring request) | **accepted**; the recurring request becomes `capability-gap`, physics-sign is an identification obligation, power is not repairable by search | §16 |
| Report language: "MDE" is an operational detection envelope; no exclusion bounds; separate pass-at-time from final-cohort pass; Dobrushin and nesting-null inference forms | **accepted**; applied to §16 here and queued for the sibling branch's report by strike-and-quote | §16 |
| HALT(UNINFORMATIVE_FOR_CONTRACT) | **accepted** | §15; `schema.HALTS` |
| Run-level cost formula; count host events; caching is not a budget line | **accepted** | §14 |
| Generator-run commands are not receipts; verifier bypass via "no new claims"; A/B diff is not blind; LESSONS/PLAYBOOK leak; refuter needs premises | **accepted** | §15 role table; `loop_v4.js` |
| Six-step evidence sequence; suspended criteria may receive authorized remediation; post-exit evidence links a supersession | **accepted** | §15 |
| Resume enters review-only; rethink needs rejected assumption + evidence + changed action + discriminating result + cost ceiling + stop condition; no automatic family exclusion; typed `hypotheses_rejected`; stop is the default when information is missing | **accepted** | §15; `schema` (rethink required fields) |
| Replace gate-agent relays with direct driver calls where supported | **adapted**: the Workflow runtime has no filesystem access, so the relay stays; the id cross-check bounds its damage; direct calls are used when the loop runs from a session | §8 |

### 12.3 Disposition of peer review 6 (derivation workspace; RSI vs GM on tasks; `loops/peer/peer_review_derivation_rsi_gm.md`)

| peer item | disposition | where |
|---|---|---|
| Repair unit = dependency slice (anchor + premises + downstream uses); whole-trace re-verification when statement, quantifiers, conditioning, exchangeability class, null transformation, convention or shared definition changes | **accepted** | addendum §A-1 |
| Refuter sees premises and the dependency slice; blind only to self-assessment and verdict history | **accepted** | addendum §A-2 |
| "Nothing new twice" is a heuristic, not a fixed point: the reserved independent Check decides; a third round without a valid Check stays unresolved | **accepted** | addendum §A-3 |
| Trace-cell immutability vs A-1/A-5: versioned replacement trace or correction overlay; effective trace built from records | **accepted** (pin R-A1 already prescribes dated notes beside the table; the overlay is that rule made explicit) | addendum §A-1 |
| Prediction sheets measure the verifier; make them optional calibration work, Brier-scored on frozen binary questions, with abstention coverage; never affect the derivation's grade | **accepted** | addendum §B-1; VERIFY template Check 0 optional |
| Defeater panel: proposed vs substantiated vs adjudicated-valid vs rejected vs unresolved; uncalibrated panel outputs are proposals; empty accepted set allowed; appeal path; `boundary-UNDECIDABLE` renamed `scope-unresolved` / `evidence-unavailable` | **accepted**; resolves the §D-vs-K-defeaters conflict: K-defeaters is required only once the panel is calibrated on known-valid traces plus independently seeded defects | addendum §B-2, §D |
| Replay forks test recoverability by a model, not validity; separate provenance axes; ≤ 3 calls per fork; only for moves that repeatedly fail to transfer | **accepted** | addendum §B-3 |
| Canary suite of four pairs (vacuous hypothesis; values-for-logic; EXEC doing typed work; promotion without event); frozen payloads; instrument problem, not derivation defect | **accepted** | addendum §B-4 |
| Oracle semantics: contradiction (out of tolerance) vs inapplicable (unit/domain/version mismatch → suspend) vs error; minimum oracle contract fields; K-oracle conditional | **accepted** | addendum §B-5; INITIATOR D |
| F6 as a bounded attempt when route uncertainty matters, not a blocker; return counts only on substantive reactivation; C-3 corroboration corrected (which obligation each route supports) | **accepted** | addendum §C |
| B8 loop-selection table; B9 RSI mechanisms keep/gate; B10 self-application needs an external evaluator and must never self-modify the standard, keys, approval root, audit, meter, budget or permissions | **accepted**; B8 is adopted as §10a below | §10a |
| B11 template corrections: stable rubric per cohort ("fresh key" = fresh private items, not a new standard); mechanical K-items by command; ACCEPT-WITH-DEBT ≠ DONE unless the requested state allows it; promotion as a controller event; real budget units | **accepted** | INITIATOR D; addendum §A, §D |

## 14. Token-efficiency review (critical, v4.2)

**Measured baselines.** Reference meta-run: about 60K subagent tokens per agent call (4.52M over 75 calls) and
6.8 vs 11 agent calls per round lean vs full *[measured (reference pilot)]*. Reference pilot: single strong pass 67-73K
tokens per task vs 2.5-3.0M for every loop arm at a 49-call cap *[measured (reference pilot)]*. Relations loop: 179
agents over 25 epochs, about 7 per epoch, one model family, no per-call token record *[measured (habitat run)]*.

**Cost model per HARDEN round under v4.2 (design-only, counts of model calls).**

| step | calls | model / effort (policy `routing`) | tokens driver |
|---|---|---|---|
| gate (`next`, appends) | 2-4 | haiku / low | tiny; relays JSON only |
| generators | 2 | opus / medium | brief + one section; the archive is withheld |
| commands | 0 | code | run by the generator on a scratch copy; a failure rejects with **no** further model call |
| verifier | 0-2 | opus / high | only when a variant declares new claims |
| screen | 1-2 | haiku / low | diff + rubric |
| judge 1 (both orders) | 2-4 | opus / medium | one section diff, cached GROUNDING + rubric prefix |
| judge 2, judge 3 | 0-4 | opus / medium | judge 2 only if judge 1 did not prefer *best*; judge 3 only on disagreement |
| **total** | **7-18** | | typical 9-11, of which 3-5 at haiku |

Where the tokens actually go and what v4.2 does about each *[design-only unless marked]*:

1. **Whole-document context in every call** was the largest cost in the reference runs. v4.2 briefs carry the rubric
   and one section; judges see a diff, never two full documents. Expected effect: the per-call cost falls from
   ~60K toward the size of the section plus rubric. Unmeasured.
2. **Fixed overhead per rung** (probe, re-probe, strict mode) lost the reference pilot's T2. v4 probes once per run;
   strict mode is a policy switch, default off.
3. **Judges when commands already decided.** A variant failing a `command` gate never reaches a judge; a variant with
   no new claims never reaches the verifier. The generator reports command exit codes in its schema so the decision is
   made in the script, not by another agent.
4. **Rounds that cannot be attributed.** Two single-section variants per round and up to two keeps (the second
   re-judged) keep credit assignment without doubling judge calls.
5. **The loop itself as overhead.** Admission runs S first; on an artifact S completes, the loop costs zero. The
   pilot found S sufficient on both of its tasks *[measured (reference pilot)]*; the rule that S must fail a criterion
   before the loop runs is the single largest expected saving and the only one with measured motivation.
6. **Exploration depth on one lineage.** Roots × depth allocation plus slots stop the 25-epochs-on-v03 pattern; the
   relations loop's last 10 trials produced zero counted moves *[measured (habitat run)]*.
7. **Scorer and lint are code.** Every `command`- and `lean`-kind criterion costs no tokens; the design pushes every
   criterion that a script can decide into those kinds (§2.1).
8. **Prompt caching.** Judge calls share an identical GROUNDING + rubric prefix (the brief is generated the same way
   every time), which is what the cache keys on. The session's subagent cache TTL applies; nothing here can be
   measured without host-reported tokens, which the archive records as `null` when absent.
9. **Gate agent cost is real but bounded**: `policy.budget.gate_calls_per_round_max` caps relays; a run that needs
   more is a design defect, not a budget line.

What this review cannot claim: any absolute saving. Every number above is a call count; tokens per call depend on
the artifact. The validation protocol (§11) reports tokens per verified keep against the S baseline, per case.

**Run-level accounting (v4.3, peer 5 §3.1-§3.2).** The round table is not a dispatch tree. A run is costed as
`C_run = C_setup + C_admission + Σ(C_round + C_retry + C_repair + C_rebaseline) + C_final + C_closure`, and the
archive records per model attempt: model/version, uncached input, cache-read input, cache-write input where
billed, output as the host exposes it, and the charge; deterministic compute and human effort as separate
quantities; critical-path time separately from summed worker time. "S costs zero" reads "no subsequent search
rounds are needed": S, its Check, setup and closure still cost. Tokens per verified keep is a secondary measure
only; a run with no keeps reports total cost and outcome. Caching is an optimization, never a budget line: the
budget assumes the worst permitted cache behaviour and reports observed savings from host receipts. The
gate-relay cap bounds a category; calls above it are still incurred and counted.

## 15. Team fidelity: exploration, validation, policy, state, and rethink (v4.2)

**Who does what, sees what, returns what.**

| role | model (policy) | sees | returns (schema) | never |
|---|---|---|---|---|
| gate | haiku | a command | its stdout JSON verbatim | reasons, edits |
| S baseline | opus / high | GROUNDING, DONE | the artifact | judges |
| generator | opus / medium | brief: rubric, one section, slot; sanitized LESSONS view (no per-case outcomes, no held-out feedback) | one variant: section, criterion, diff, typed claims, a claim/dependency manifest of what the diff touches; command exit codes as **development feedback only** | the archive, per-seed values, the favoured family, shared modules |
| command runner (driver or gate agent, not the generator) *(v4.3)* | code (haiku relay where a shell is not reachable) | the diff, the immutable acceptance commands | exit codes and outputs bound to the candidate's hash: the **acceptance receipt** | the generator's rationale |
| verifier | opus / high | the claims and the claim/dependency manifest, sources | findings by typed evidence; runs whenever the diff touches claim-bearing material (a manifest hit), not only when the writer declares a claim *(v4.3)* | edits, the generator's rationale |
| screen | haiku | diff + rubric | pass / reject + reason | the rationale |
| judge (1-3) | opus / medium, one cross-family where available | GROUNDING + rubric prefix; the affected section in two randomly labelled versions with the shared context they need and a dependency summary (a neutral diff may be supplemental) *(v4.3)* | overall, per-criterion, confidence | rationale, other judges, the archive; ancestry cues that a raw diff would disclose |
| red team | sonnet | front summaries and code | probes (proposed) with declared tolerances | scorer values, scoring |
| refuter | opus / high | the revised claim **with its premises, definitions and dependency slice** + the finding *(v4.3)* | nothing new / a finding | the writer's self-assessment and verdict history |
| meta (STOP) | opus | the archive (yields) | a **policy proposal** | a live policy change |
| human | — | everything | `by: "human"` records | — |

**State update.** Only `loopkit append` writes; only decision-bound records advance the loop; every other record
(version, citation, substrate, evidence, suspend, family, probe_state, route) is context that `next` reads. The
state is therefore the archive, and the archive is recomputable into a state by `next._state` (rounds, stalls,
invalidated criteria, suspended criteria, open gaps, halts, rung, admission, protected set).

**Policy update.** The meta agent never edits `policy.json`; it appends a proposal the human can adopt with an
`instrument` record at a boundary and a re-baseline on the anchor set. `next` refuses to run under a policy whose
hash differs from `setup.policy_hash` without that record. A playbook rewrite (operators, yields) is the same kind
of event: a boundary instrument change under a new cohort, never a mid-epoch change *(peer §10)*.

**Rethink protocol (when evidence arrives or a path fails).**

| event | record | what `next` does |
|---|---|---|
| new evidence (a source, a datum, an instrument result, an external review, a human ruling) | `evidence{kind, affects, invalidates}` | invalidates the last Check on the affected required criteria → the next action is a `check` with trigger `evidence` before any keep or exit |
| a result's applicability is challenged | `suspend{criterion, result, challenge}` | the criterion is excluded from targets and from any exit until `unsuspend` with evidence |
| an interrupt-class route | `route{type ∈ interrupt}` | `resolve_route` until it carries `resolved` |
| ERROR | variant `dropped` after one retry; two all-ERROR rounds → `halt ERROR` | |
| stall | 3 empty rounds → `check`; still failing → `halt STALL` | |
| halt resumed after STALL / OSCILLATION | `resume{by: human}` enters a **review-only state** (no generation authority); a **`rethink`** record is required before any round *(v4.3, peer 5 §3.5)*: `trigger`, `decision ∈ reopen_explore | amend_request | continue | stop`, `hypotheses_rejected[{id, status ∈ falsified | instrument-invalid | inconclusive | untested, evidence}]`, `changed_action`, `expected_discriminating_result`, `cost_ceiling`, `stop_condition` | the frame is re-examined: `reopen_explore` **down-weights** the exhausted family rather than excluding it (an unsuccessful allocation rejects neither a family nor its hypotheses) with the archive withheld; `amend_request` (a weaker DONE defines a new task and never certifies the failed one); `continue` only with a genuinely changed action whose result would distinguish explanations; `stop` (the recommended default when the contract cannot be resolved with the information available: a scoped, synthetic-only instrument or estimand study may be authorized separately) |
| frame exhausted (G6 ×3, or every variant of 3 rounds in one family) | `route{type: frame-exhausted}` | boundary-class; at the boundary it becomes a `rethink`; it is a within-budget search failure, never evidence against the family |
| an evaluator asks for a capability no operator offers, twice or more | `route{type: capability-gap}` *(v4.3)* | boundary-class: an unmet-capability or unresolved-hypothesis record naming the executable contract change and an independent feasibility test; repetition is scheduling evidence, not scientific justification; never auto-classified as instrument-defect |
| the contract cannot be resolved with the available information (identification or sensitivity obligations unmet) | `halt{reason: UNINFORMATIVE_FOR_CONTRACT}` *(v4.3, peer 5 §2.3)* | completion is blocked; the report states the tested scope and uses no exclusion language without a validated bound; exhausted budget, inadequate instruments and unmet information needs are reported as three different things |
| a canary passes | `canary{outcome: pass}` + `route{canary-passed}` | `halt CANARY`; human only |

The rethink record is the loop's explicit answer to the "prior problem" (what deserves evaluation at all,
2607.07663): a failed path changes the frame or the objective only through a logged decision, never by the
generator quietly proposing something else.

**Evidence intake is a six-step sequence, not a re-check (v4.3, peer 5 §3.4).** (1) Intake: stable id,
provenance, affected claims and instruments, triage status; a credible applicability challenge suspends dependent
acceptance before adjudication. (2) Dependency closure: affected claims, Checks, kept versions, frontier
membership, descendants, admission protections; unresolved scope suspends conservatively. (3) Withdraw current
authority: affected keeps and COMPLETE status become `superseded` while the historical records stay. (4) Resolve:
rejected challenge | artifact repair | instrument recalibration | contract amendment | information gap, each with
evidence, never a self-authored `resolved: true`. (5) Re-evaluate under a valid cohort; re-admit if S's protected
criteria, scope, budget or contract changed. (6) Recommit or halt. A suspended criterion is excluded from
acceptance and from score optimization, but explicitly authorized remediation work targeting the suspension is
allowed, else the controller forbids the repair that would lift it. Evidence arriving after `exit` creates a linked
supersession event; an exit never implies permanent validity.

## 16. The relations loop's search limits, and the v4 response

Its final report listed the limits itself *[measured (habitat run)]*. Each is mapped to a mechanism and to what is
still open.

| limit (FINAL_REPORT §1, "search limits") | v4 mechanism | status |
|---|---|---|
| every child of epochs 21-25 descended from v03; parent rules broken every epoch | slots checked at write time (hook), roots × depth allocation, hot lane, ancestry from version records | built; Stage 1 replay: 10/10 void |
| a single structure-matched seed decided verdicts; 3-draw permutation null understated the SD 2-9× | the scorer is an `instrument` with a version; a change (20-seed null, `sm20` as SCALE) lands at a boundary with a re-baseline; a "single-seed carrier" is a discounted gate in policy, and the `command` criterion names its case manifest and aggregation | to build on the sibling branch's harness (scorer v4); the archive side is built |
| sign-blind D6; D2 needs a carrier | criteria are atomic and typed: D6 gains a sign clause; robustness (D2) is split from effect (D6) so a null-effect variant can still earn robustness | INITIATOR X template; scorer change to build |
| 1-unit floor on D7/D8 that sub-mm estimands cannot reach | SCALE fixed before the run from physics (playbook check 14) as a `must_not_change`; a unit gate whose SCALE is far above the effect is an `instrument-defect` route | policy + template; scorer change to build |
| the variant contract scores one grid per call, so fusion (M15) was never scored on real data | a multi-grid variant contract is an `instrument` change; until it exists, fusion operators are `blocked` routes with a named wall, not retired operators | incubation ledger INC-4; harness change to build |
| M21 was never run (cap reached) | exploration operators reserve slot **a** first; an untried operator is never retired; the cap is lifted only by `amend{budget}` | policy `explore.slots`; INITIATOR X |
| the red-team bank froze at its cap; 16 of 26 probes never scored anything | probe lifecycle with dormancy and core coverage; the cap bounds active probes only | built |
| power: planted twins at 0.15-1.10 MDE; n_eff/n 0.003-0.017 | the power pre-screen (playbook check 6) becomes a `command`-kind admission criterion for a candidate: a variant that cannot detect its own planted twin at ≥ 2 MDE on one independent row per subject is not scored on real data; the honest deliverable is the exclusion report | template; no loop can fix the data; synthetic-only frontier work and explicit bounds are the route |
| physics mimics the target (vasogenic fade, slab partial volume) | fade and partial-volume nulls are pre-registered `core` probes; a sign that the null reproduces is not a carrier | policy `bank`; probes exist on the sibling branch |
| the lenses asked five epochs in a row for a change no operator offered (water-conditioned mark) | a recurring evaluator request is a `capability-gap` route (v4.3): it names the executable contract change and an independent feasibility test and reaches `rethink` at the boundary; it is not auto-classified as an instrument defect and it does not by itself justify the operator | router + rethink |

**Corrections to the run report's own language (v4.3, peer 5 §2.2; to be applied on the sibling branch when it is
next edited, by strike-and-quote per pin R-A1).** The quantity the report calls "MDE" is an *operational detection
envelope* (a maximum over a scaled jackknife error, sampled-null extremes and selected perturbation responses),
not a calibrated minimum detectable effect; adding null draws raises its maximum without any scientific change.
`|observed| + envelope` is not an exclusion bound or an upper confidence limit; "ruled out" and "underpowered null
with bounds" overstate the result. Replacement wording: "No candidate met the specified acceptance criteria. The
reported sensitivity envelopes summarize the tested controls and perturbations; they do not exclude an underlying
effect or establish a confidence bound." Pass counts scored under different bank versions are not one
leaderboard: report "passed at evaluation time" and "passes the final frozen cohort" separately, and per-criterion
vectors rather than counts. "The data are the main ceiling" is a working diagnosis, not identified by the run: scorer
defects, incomplete operator coverage, changing banks and lineage concentration are co-causes. Two inference-form
corrections: failing a sufficient condition (a Dobrushin contraction certificate) does not establish the opposite
property ("supercritical"); failed constructions of a nesting-preserving powered null do not show that none exists.
Both become "the certificate was not obtained" and "the attempted constructions failed".

## 17. Sources

Reference repo: `F:\git\rqgm-loop` (README, INITIATOR, SKILL v3.1, DESIGN.md, REPORT.md, open-issues.md,
`rqgm_check.py`). Upstream derivation lab: `F:\git\first-principles-derivation-lab` @ 0db9639 (`methodology/*`,
`staging/process-upgrades/{LOOPGRAPH_V2,EVAL_V2,PREREG_REPLAY,MMOP_SYNTHESIS}.md`, `staging/instrument-versioning.md`,
`staging/arxiv-2606-eval/LOOP_GRAPH.md`). This repo: docs 19, 21, 25, 26, 27, 28; `loops/*/archive.jsonl`;
`derivations/CONSTRAINTS_AND_MOVES_pin_2026-09-08.md`; `derivations/JUDGE_KEY_2026-09-08.md`; the relations loop's
`PLAN.md`, `DONE.json`, `PLAYBOOK.md` v5, `FINAL_REPORT.md`.

Literature (read 2026-09-26): Iacob et al., *The Red Queen Gödel Machine*, arXiv:2606.26294 · *Recursive
Self-Improvement in AI: From Bounded Self-Refinement to Autonomous Research Loops*, arXiv:2607.07663 (evaluator
hierarchy; the "prior problem") · *LLM-as-a-Judge Is Not an Oracle*, arXiv:2609.02246 (PROCTOR: hermetic sandboxes,
capability-disjoint roles, acceptance checks outrank the teacher, frozen holdouts, canaries) · *Evolution or
Illusion? Rethinking Evaluation in LLM Evolutionary Search*, arXiv:2609.19799 (seeds × iterations frontier) ·
*Who Judges Matters*, arXiv:2609.17857 (family-conditioned preference, 55.4 % AB/BA reversal) · *Towards Diverse
Scientific Hypothesis Search with LLMs*, arXiv:2606.10587 (parallel tempering against diversity collapse) ·
Zhang et al., *Darwin Gödel Machine*, arXiv:2505.22954 (open archive, parent sampling) · Sakana, *ShinkaEvolve*,
arXiv:2509.19349 (novelty rejection sampling, bandit ensemble) · Srikanth et al., *Recursive self-improvement of AI
research agents*, arXiv:2609.26457 (keep on hidden evaluations) · SpecBench, arXiv:2605.21384 · Anthropic,
*Effective harnesses for long-running agents* (2025) · Cursor, reward hacking in coding benchmarks (2026).
