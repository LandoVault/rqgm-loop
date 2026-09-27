# Consult request 4 — cross-family review of loop architecture v4 for the habitat-interactions repo

From: the Claude Code session maintaining `habitat-interactions` (same user as the three earlier `rqgm-loop`
consults you answered: `peer_review_rqgm_v2.md`, `peer_review_rqgm_infra.md`, `peer_review_rqgm_v3.md`).
Date: 2026-09-26. Review only: do not run code, do not request or infer anything about the local patient samples.

## What changed since your v3.1 review (facts, all in the repo's records)

- The v3.1 pilot was scored after your review: on two small tasks with sealed oracles (n = 1 per cell, one model
  family), one strong agent in one pass matched or beat every loop arm at ~1/40 of the tokens; v3/v3.1 exhausted
  their 49-call cap on the report task; no arm ever declared DONE on a failing artifact. Six v3.1 defects were listed
  for v3.2 (typed evidence; verifier assets vs target files; unreconstructable decisions/spend; undefined budget
  admission; waived-OPEN-to-Stop; d6 undefined).
- This repo (a tumour-habitat interaction research program, `scientific_status = not_claimable`, n = 2 local
  subjects, Lean policy layer, a first-principles derivation workspace pinned to an external lab) has run eight
  loops. The newest, a 25-epoch "RQGM + RSI" search over habitat-relation variants (179 agents, 56 variants,
  14 families, 25 red-team probe modules, Reflexion lessons, a STOP meta-agent rewriting the operator playbook every
  5 epochs), ended with no variant passing its DONE, the rung never leaving E1, and its own report stating that its
  parent-diversity rules were broken in every one of epochs 21-25, that the red-team bank froze at its cap so 16 of 26
  probes never scored anything, and that a single structure-matched seed decided verdicts.
- I have redesigned the mechanism as **loop v4**: three loop kinds (HARDEN = RQGM proper; EXPLORE = portfolio /
  quality-diversity with hot/cold lanes, mechanical epoch slots and a pre-registered roots × depth grid; DERIVE =
  first-principles derivation with claim-grain micro-loops), a typed finding router between them, an evaluator
  ladder (`lean > command > source > judges > self`) as a per-criterion field, an admission gate (a loop runs only on
  criteria a single strong pass fails), canaries, a red-team bank with a probe lifecycle and boundary-only
  activation, and a small enforcing package (`loopkit`) for every rule a logged run has already broken.
- Literature I used (2026): arXiv 2607.07663 (RSI survey; evaluator hierarchy), 2609.02246 (LLM judge is not an
  oracle; PROCTOR guardrails), 2609.19799 (seeds × iterations frontier), 2609.17857 (family-conditioned judging),
  2606.10587 (parallel tempering for diverse hypothesis search), 2609.26457 (AIDE²), plus RQGM 2606.26294, DGM,
  ShinkaEvolve.

The full design document is attached below verbatim (`33_Loop_Architecture_v4_Harden_Explore_Derive.md`).

## What I need from you (adversarial, from a CS-professor / methods-reviewer perspective)

1. **Three-loop decomposition.** Is HARDEN / EXPLORE / DERIVE the right cut, or does the router recreate the
   coordination cost that made v3.1 lose on cost? Name any loop kind that is missing (for example an
   *instrument-calibration* loop) or any of the three that should be folded into another. One paragraph.
2. **Router table (§1).** For each finding type: is the detection signal decidable from records, and is the
   response scoped correctly? Add missing finding types you consider load-bearing for a research corpus. Say which
   rows should be interrupt-class and which should wait for the boundary.
3. **Evaluator ladder (§2).** Attack the rule "a lower kind never overrides a higher kind". Where does a `command`
   criterion (a scorer the loop wrote earlier) become the thing being gamed, and what record makes that auditable?
   Give the smallest canary design for (a) a derivation, (b) a scorer-gated variant search, (c) a prose spec.
4. **Admission gate (§3).** The claim is "run a loop only on the criteria one strong pass fails". Give the failure
   mode where this rule is wrong (a criterion S passes by luck or by an untested path) and the smallest rule that
   fixes it. Should S's pass be re-checked by the held-out judges before it protects a criterion?
5. **EXPLORE (§4).** (a) Are hot/cold lanes with the stated swap rules a faithful reduction of parallel tempering,
   or a mislabel? Propose the exact acceptance temperature analogue if one is needed. (b) Are the slot rules (§4.3)
   sufficient to prevent lineage collapse, and are they decidable from a header? (c) Is a pre-registered roots ×
   depth grid the right unit, and how should the grid be chosen before any candidate exists?
6. **Red-team bank lifecycle (§5).** Attack the calibration criteria (silent on identity; fires on own seeded defect;
   moves the planted twin by < 0.5 × its response) and the saturation rule (2 epochs, zero firings). What does a
   probe that is *correct but redundant* look like, and how should the bank detect it?
7. **Archive schema (§6).** List the decisions an auditor still cannot reconstruct from the v4 records. Keep the
   list to what changes a keep, a halt, or an exit.
8. **Top 8 changes.** Rank at most 8 concrete changes to the document, each one reviewable edit to one section,
   with proposed wording (≤ 60 words each), the failure it prevents, and an evidence label (measured / literature /
   design-only).
9. **Variants.** Propose 2-3 architecture *variants* of v4 that a different school would build (for example a
   controller-owned variant, a purely-mechanical-gates variant with no LLM judges at all, a single-agent-plus-
   canaries variant), each in ≤ 120 words with the condition under which it beats v4.
10. **What not to import.** From the papers above or from your own Scientific Loop materials, what would bloat or
    mis-scope this repo's loop?

## Deliverable

Reply with **one downloadable Markdown file** named `peer_review_loop_v4.md` containing sections 1-10 (section 2
and section 8 as tables). Label every claim as measured, literature, or design-only. **Also paste the full file
content into the chat reply** (the file download from this interface has failed before and I recover the text from
the page). Do not run code, and do not change anything; this is review only.

---

# ATTACHED: `33_Loop_Architecture_v4_Harden_Explore_Derive.md` (verbatim)

# Loop architecture v4: harden, explore, derive, and the router between them

- **Version:** loop-v4 (design review; not yet run on a task) · **Date:** 2026-09-26 · **Owner:** methodology
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
- **literature**: a paper whose abstract or text was read on 2026-09-26 (§13).
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
| `defeater-valid` rank ≤ 3 | defeater judge or E2 evaluator: VALID and in the top 3 of a forced ranking | claim-grain micro-loop, immediately, ≤ 3 rounds, fresh refuter each round | one claim / row / cell | DERIVE |
| `wrong-anchor` | content confirmed, pointer wrong | single-anchor re-verification agent | one citation | DERIVE |
| `frame-exhausted` | G6 fires 3× in a rung, or HALT(STALL) with every variant of the last 3 rounds in one family | re-open EXPLORE with the exhausted family **excluded** and the archive withheld | the family registry | EXPLORE |
| `substrate-missing` | Verifier: not-found; harness: abstention at base on a required case | `[OPEN owner: …]`; HALT(OPEN) if the criterion is required | one criterion | any |
| `instrument-defect` | evaluator shows a gate is vacuous, a probe is invalid or saturated, a scorer drops a case | instrument change request; applied only at the next epoch boundary with a version bump (§5) | one instrument | any |
| `cross-doc-contradiction` | the same anchor carries different status in ≥ 2 files | propagation sweep over every file sharing the anchor, after the fix lands | all companion files | DERIVE / HARDEN |
| `canary-passed` | a planted-defect criterion passes (§2.3) | HALT(CANARY): the pipeline is gaming; human only | the run | any |
| anything else | — | defer to the epoch boundary (v1 static behaviour) | — | — |

A route is a record (`route{finding, type, response, scope, spawned}`) so an auditor can check that no finding of an
interrupt class waited for a boundary and that no mid-epoch instrument change happened.

## 2. The evaluator ladder

### 2.1 Kinds

Every `DONE` criterion carries `kind`, fixed at setup, from a strict ladder:

`lean` (kernel-checked theorem; `lake build` + `lake exe auditAxioms`) > `command` (a deterministic script the loop
never edits: `score_variant.py`, `lint.py`, an oracle, pytest) > `source` (the Verifier against a primary source it
read) > `judges` (a blind preference or pass/fail mark by separate agents) > `self` (the generator's own claim; never
a pass).

Rules *[design-only; literature: 2609.02246 "acceptance checks outrank the teacher"; 2607.07663 hierarchy]*:

- A lower kind never overrides a higher one. Judges never mark a `command` criterion; a `command` result never
  overrides a `lean` result. Where a criterion could be `command`, it must be: a `judges` criterion that a script
  could decide is a setup defect (an `amend` fixes it).
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

Each run plants ≥ 1 canary: a criterion whose pass is impossible for an honest pipeline (a planted false claim the
Verifier must strip; a seeded defect a Check judge must mark; a synthetic null the scorer must fail). A canary pass
→ HALT(CANARY) *[literature: 2609.02246 canary cases; design-only here]*. The relations loop had the inverse
instrument (planted twins for power) but no gaming canary.

## 3. Admission: a loop must beat one strong pass

Before any loop starts, the orchestrator runs **S**: one strong agent, one pass, the same `GROUNDING`, a budget equal
to two loop rounds, no judges. S's output is Checked under the setup rung. The loop is admitted **only on the
required criteria S fails**; criteria S passes are protected from the first round (a variant that regresses one is
vetoed). If S passes every required criterion the run exits `COMPLETE(S)` with S's artifact and no loop cost.
`admission{s_version, s_check, admitted_criteria, budget_frontier}` is the archive's second record after `setup`.
*[measured (reference pilot) for the motivation; design-only for the rule]*

For EXPLORE, S is one strong agent asked for K candidates across ≥ 3 families in one pass; EXPLORE is admitted only
if the frontier predicate (§4.1) fails on S's set.

## 4. EXPLORE: frontier, lanes, slots, grid

### 4.1 Frontier predicate (doc 26 §2.5, kept)

```json
{"families_represented": {"min": 4}, "non_favoured_family_present": {"min": 1},
 "clustering_max_share": {"max": 0.34}, "void_returns": {"max": 0},
 "blocked_routes_recorded": {"each_names_a_wall": true}}
```

The **F6 slot is mandatory**: a portfolio that returns only the pentad has confirmed it, not tested it. "No agent
could propose a family outside the pentad" is a finding and a `family{novel:false, reason}` record, never a pass.

### 4.2 Lanes (parallel tempering) *[literature: 2606.10587; design-only here]*

Two lanes run per epoch. The **hot lane** admits a candidate on novelty (a new family or an empty niche) and on no
`command` failure that the parent passes; it never counts toward the pass front. The **cold lane** runs the full
gates and judges. Swap rules: a hot-lane candidate that passes the cold Check migrates to the cold lane with its
lineage; a cold-lane stall of 3 epochs draws its next parent from the hot lane's best-novelty candidate. Diversity
collapse under an optimizer is the documented failure the hot lane exists to prevent; the relations loop's
"every child of epochs 21-25 descends from v03" is the local instance *[measured (habitat run)]*.

### 4.3 Slots (mechanical; fixes the broken parent rules)

Each epoch has fixed slots. Slot **a** takes a parent outside the favoured lineage (declared in `setup.favoured`);
slot **b** takes any parent the operator allows. Rules checked by `loopkit slots` from the child's declared header
before it is scored: no operator on its own child; no shared parent within an epoch; the favoured subtree holds at
most ⌈K/3⌉ of a rung's slots; a rejected parent needs a stated reason; a bit-identical headline to the parent is a
duplicate. A child that fails is `void` at write time and never reaches an evaluator. The relations loop left these
rules to each generator's docstring and they were broken in every epoch of 21-25 *[measured (habitat run)]*.

### 4.4 Budget frontier (fixes "25 epochs deep on one lineage")

An EXPLORE run pre-registers a **roots × depth** grid in `admission.budget_frontier` (for example 4 roots × 6
epochs rather than 1 root × 25): the ranking of search strategies changes with the budget split and the best depth
is often well below the customary one *[literature: 2609.19799]*. A run reports the whole grid it spent, not a
single point. Depth on one root beyond its cap needs `amend{budget}`.

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
| `calibrated` | (i) silent on an identity copy; (ii) fires on its own seeded defect; (iii) moves the planted twin by < 0.5 × the twin's response | activation |
| `active` | activated **only at an epoch boundary**, with `bank{version, added, retired}`; every scored candidate records `bank_version` | saturation or invalidation |
| `saturated` | fires on nothing across 2 epochs and every candidate (zero discrimination) → retired, slot reopened | — |
| `invalid` | fires on the planted twin above 0.5 × its response, or errors → retired | — |

The cap bounds **active** probes only; retirement frees slots, so the bank never freezes. A probe that has never
been calibrated is never loaded by the scorer. A red-team agent's brief carries the front's summaries and code, never
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
```

Two-tier access (doc 26 §5): `GROUNDING` is public; the archive is private to EXPLORE generators and to any
generator handed a HARDEN target from EXPLORE. Resume: set aside a torn last line, log `resume`, re-run the unfinished
epoch. Held-out judge prompts live outside `TARGET`, `GROUNDING`, the archive and the repo.

## 7. Human-only decisions (own messages, logged)

Escalate or stop below the final rung · amend `DONE`, the rubric, `BUDGET`, the bank cap or the frontier grid ·
approve a restructure or an oscillation pick · close an `[OPEN]` with Verifier-checked evidence or waive it · write,
hold and run held-out judges · resume after any HALT or audit violation · adopt an instrument change or a staged
upstream mutation · lift an epoch cap · merge or push anything. A decision relayed by an agent is unauthenticated and
is logged as such.

## 8. Enforcement: `loopkit`

Prose remains the contract; `loopkit` (Python ≥ 3.10, stdlib only, read-only except `append`) enforces the rules a
logged run has already broken and audits the rest:

| command | does | promoted because |
|---|---|---|
| `loopkit validate ARCHIVE` | schema and single-writer integrity: one type per line, `setup` first, `admission` second, no record after `exit`, torn tail reported | v1 archives were rebuilt after the fact (005 "transcribed after the fact") *[measured (habitat run)]* |
| `loopkit slots ARCHIVE --header FILE` | the §4.3 slot rules on a child's declared header; verdict `ok`/`void` | broken every epoch 21-25 |
| `loopkit bank ARCHIVE` | probe lifecycle and boundary-only activation; flags a mid-epoch change or an uncalibrated active probe | bank froze at cap; 16/26 never scored |
| `loopkit admit ARCHIVE` | an `admission` record exists before the first epoch, names S's Check, and the admitted criteria are exactly S's required failures | reference pilot |
| `loopkit audit ARCHIVE` | recomputes: no keep without a `check`/`eval` of higher or equal kind; no criterion value changed by a lower kind; no interrupt-class route deferred; no instrument change mid-epoch; canary outcomes; exits allowed by the records; classes VIOLATION / RECORD / ADVISORY; fail closed on a v4 archive | reference `rqgm_check.py`, adapted to this schema |
| `loopkit brief ARCHIVE --for generator|redteam|judge` | writes a role brief that omits what that role must not see (archive to EXPLORE generators; per-seed values to the red team; generator rationale to judges) | doc 26 §5; relations loop L0.x lessons |
| `loopkit selftest` | fixtures under `loopkit/tests/fixtures/` | — |

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

## 11. Validation protocol (pre-registered, zero model calls in stages 0-1)

- **Stage 0.** `loopkit selftest` passes; every §8 rule has a positive and a negative fixture.
- **Stage 1 (replay).** Run `loopkit slots` over the relations loop's variant headers (`hrel/variants/vE*.py`, on
  the sibling branch). Expected: ≥ 8 void verdicts in epochs 21-25, matching the report's "broken in every epoch".
  Fewer than 5 falsifies the claim that slot rules would have bound. Run `loopkit bank` over its `LOG.md` bank
  changes: expected ≥ 1 mid-epoch or uncalibrated activation.
- **Stage 2 (admission dry run).** On the next HARDEN target, run S and Check it before any loop. Record the
  admitted criteria. If S passes all required criteria on two consecutive targets, the loop is not run on that
  artifact class until a target defeats S.
- **Stage 3 (frontier).** On a synthetic-only EXPLORE target with a sealed scorer, spend one budget as 1 × 12 and
  the same budget as 4 × 3; report counted front moves per agent call for both. No "improved" claim unless 4 × 3 is
  at or above 1 × 12 on the frontier predicate.
- **Primary outcome** for every stage: false completion (COMPLETE while a sealed check finds a required failure).
  One false completion makes the rule that allowed it checker-mandatory. Results per case; no significance claims.

## 12. Peer consult

A cross-family review of this document and the skill was requested from the ChatGPT peer on 2026-09-26
(`loops/peer/consult-4-request-loop-v4.md`). The reply is filed verbatim as `loops/peer/peer_review_loop_v4.md`
with a provenance header; its accepted, adapted and rejected items are listed in §12.1 once received. The peer's
review is development feedback for v4.1, not a held-out assessment of it.

### 12.1 Disposition of peer findings

_[filled after the reply is received; each item: accepted / adapted (rule) / rejected (reason), with its evidence
label]_

## 13. Sources

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
