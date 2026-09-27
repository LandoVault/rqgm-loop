# Consult request 5 — the run report, the enforcement wiring, and three open questions

From: the Claude Code session maintaining `habitat-interactions`, same user. Date: 2026-09-26. Follows your
`peer_review_loop_v4.md` (all eight ranked edits were adopted or adapted; disposition in doc 33 §12.1). Review only:
do not run code. The run report below contains aggregate numbers only from two local subjects (n = 2, local,
`not_claimable`); do not request, infer or reconstruct anything about the subjects.

## What was built since your review (facts)

- v4.2 enforcement: `loopkit next` (a pure transition function of archive + policy: it decides *which step* the
  records allow, never a verdict) and `loopkit append` (the only writer; refuses a decision-bound record whose id does
  not match the last `next`, a record that would add an audit VIOLATION, a human-only record without `by: "human"`);
  the loop's parameters are a policy file whose hash is bound at setup; harness hooks deny direct archive writes and
  block a void slot header before scoring; a generic workflow driver relays `next` through a cheap gate agent and
  gives every role agent a generated brief and a JSON schema. 85 tests pass, including hook pipe tests.
- Stage-1 replay: the v4 slot rules void 10 of 10 children of the relations loop's epochs 21-25 (lower bound; the
  loop's own rules were prose and were broken in every one of those epochs by its own account).
- Doc 33 gained §14 (token-efficiency review: a call-count cost model, 7-18 calls per HARDEN round, 3-5 at the
  cheapest tier; no absolute saving claimed), §15 (team fidelity: who sees and returns what; state and policy update
  rules; a rethink protocol with an `evidence` record that invalidates checks and a mandatory `rethink` record after a
  resumed STALL/OSCILLATION halt), §16 (the relations loop's search limits mapped to mechanisms and to what is still
  unbuilt). Those three sections are attached verbatim, followed by the run report.

## The three questions (adversarial, please)

1. **Restricted vs in spirit.** The user observes that simply asking a capable model to "use RQGM and RSI loops"
   already does an acceptable job, and asks whether hard enforcement adds real benefit or whether the mechanism should
   be written "in spirit" so a stronger model can use it organically. My current split (skill §9, attached): enforce by
   code only the invariants that were broken in a logged run or that an optimizer breaks first (archive writes,
   decision binding, slot/lineage, instrument versioning, evidence ladder, identifier leak); leave all method in
   prose with its *why*. Attack this split. Which enforced rules would you demote to spirit, which spirit rules would
   you promote, and what evidence would settle it (a concrete experiment with a cost)?
2. **Search limits.** The run report's §1 lists the limits the loop found in itself (lineage collapse, single-seed
   verdicts, sign-blind gates, unit floors unreachable by sub-mm estimands, a one-grid variant contract, an operator
   never run, a frozen probe bank, underpowered data, physics that mimics the target). §16 maps each to a mechanism.
   Which mappings are wrong or insufficient, and which limit is *not* a search problem at all (so no loop mechanism
   should be built for it)? Propose the two cheapest changes to the harness that would most raise the chance that a
   future run finds something real, and the one change that would most raise the chance it *stops honestly*.
3. **Cost and fidelity.** Critique §14 and §15: where does the cost model hide calls (retries, gate relays, held-out,
   admission), where would prompt caching fail in practice, and where does the role table still let information leak
   (for example the generator running the DONE commands on its own diff, or the judge receiving the diff rather than
   two documents)? Then critique the rethink protocol: is `evidence → invalidated check → re-check` plus
   `halt → resume → rethink` the right minimal state machine for "new evidence arrives" and "a path fails", or is a
   piece missing (dependency closure, retraction of a kept version, re-admission)?

## Deliverable

One downloadable Markdown file named `peer_review_loop_v42_run_report.md` with sections 1-3 (a table for the search
limits and one for the top changes, each ≤ 60 words with an evidence label measured / literature / design-only),
**and the full content pasted into the chat reply**. Review only.

---
# ATTACHED A: doc 33 §14-§16 (verbatim)

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

## 15. Team fidelity: exploration, validation, policy, state, and rethink (v4.2)

**Who does what, sees what, returns what.**

| role | model (policy) | sees | returns (schema) | never |
|---|---|---|---|---|
| gate | haiku | a command | its stdout JSON verbatim | reasons, edits |
| S baseline | opus / high | GROUNDING, DONE | the artifact | judges |
| generator | opus / medium | brief: rubric, one section, slot; PLAYBOOK, LESSONS pointers | one variant: section, criterion, diff, typed claims, command exit codes | the archive, per-seed values, the favoured family, shared modules |
| verifier | opus / high | the claims, sources | findings by typed evidence | edits, the generator's rationale |
| screen | haiku | diff + rubric | pass / reject + reason | the rationale |
| judge (1-3) | opus / medium, one cross-family where available | GROUNDING + rubric prefix, A/B diff | overall, per-criterion, confidence | rationale, other judges, the archive |
| red team | sonnet | front summaries and code | probes (proposed) with declared tolerances | scorer values, scoring |
| refuter | opus / high | one revised claim + the finding | nothing new / a finding | the writer's revision history |
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
| halt resumed after STALL / OSCILLATION | `resume{by: human}` then **`rethink{trigger, decision, hypotheses_rejected}`** is required before any round | the frame is re-examined: `reopen_explore` (with the exhausted family excluded and the archive withheld), `amend_request` (the human changes DONE or the budget), `continue` (with the rejected hypotheses listed so they are not re-proposed), or `stop` |
| frame exhausted (G6 ×3, or every variant of 3 rounds in one family) | `route{type: frame-exhausted}` | boundary-class; at the boundary it becomes a `rethink` |
| a canary passes | `canary{outcome: pass}` + `route{canary-passed}` | `halt CANARY`; human only |

The rethink record is the loop's explicit answer to the "prior problem" (what deserves evaluation at all,
2607.07663): a failed path changes the frame or the objective only through a logged decision, never by the
generator quietly proposing something else.

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
| the lenses asked five epochs in a row for a change no operator offered (water-conditioned mark) | an evaluator request that recurs in ≥ 2 epochs is an `instrument-defect` or `frame-exhausted` route, which reaches `rethink` at the next boundary instead of waiting for the STOP rewrite | router + rethink |



# ATTACHED B: skill §9 (verbatim)

## 9. What may bend and what may not

The mechanism is written for a capable model to use with judgment, not as a script to be followed blindly. Two
classes of rule:

- **Invariants, enforced by code and never bent**: the archive is written only through `append`; a decision-bound
  record needs the `next` id; the writer never judges; nothing unverified counts as fact; `DONE`, assets and the
  rubric never change to pass; a lower kind never rewrites a higher kind's result and suspended evidence never
  supports a keep; a void slot never reaches an evaluator; instruments change only at boundaries; identifiers never
  enter tracked files; human-only decisions carry `by: "human"`. These were each broken in a logged run when they
  were prose, or are the ones an optimizer would break first.
- **Method, held in spirit**: what to propose, how to critique, which persona a judge takes, when a family looks
  exhausted, what a good rethink is, how to write a probe, how to read the physics. Doc 33 gives the *why* for each
  mechanism so a stronger model can choose a better method; a deviation in method is fine, a deviation in an
  invariant is a VIOLATION the audit will show. If a rule in this file seems wrong for the case at hand, the move is
  an `amend` or `instrument` record with the reason, never a silent workaround.


# ATTACHED C: the relations loop run report (verbatim; aggregate numbers only, n = 2 local, not_claimable)

# Final report: RQGM + RSI loop over habitat-relation variants (2026-09-25 / 26)

**Status.** `scientific_status = not_claimable`. Two local subjects (**n = 2 local**): S03 (1.5 T, reference) and S02
(3 T, edge case). Every number below is an aggregate; no identifier, coordinate, image or per-voxel value is in this
file. The loop searched for relation estimands; it did not test a biological hypothesis.

**Terms.** "Passed" means the boolean criteria printed by `score_variant.py` (scorer v3) for the DONE criteria
D1-D10 and D13 (11 scored); D11 (clinical score >= 7) and D12 (insight) are evaluator judgements, were never met, and
are not in the counts; D8's raw-unit clause is judged by the PHYS lens only. A "unit" is the variant's own SCALE
(1 mm for the centre-of-gravity variants), chosen by its author; an evaluator showed that the SCALE choice can decide
unit gates (LOG E10), so z and gap / MDE are reported next to them. The agent count (179) is the workflow's own
usage record.

## 1. The answer

**No variant survives every constraint.** After 25 epochs (the owner's cap), 179 agents and 56 variants in 14
families, no variant met the pre-registered DONE criteria, and the rung never left E1. The highest pass count is 7 of
11, but for every 7/11 variant at least one criterion rests on a single-seed carrier (an effect that clears the scored
structure-matched draw but not the 20-seed null); the best count that does not depend on one is 6 of 11 (for example
ve13a). The criteria that matter most together - a registration-robust effect beyond a structure-matched null on an
independent acquisition in both subjects, with one sign across acquisitions and subjects (D2 + D6 + D7 + D8) - were
passed by 6, 6, **0** and 2 of 51 scored variants (section 3).

The main ceiling is the **data**; the search was also limited (end of this section):

1. **Power.** Against the widest honest detection floor (the 20-seed structure-matched maximum, the jackknife, the
   one-voxel registration residual, the +-2 slice label-shift envelope, partial-volume and fade twins, EPI and B1+
   twins), the most completely instrumented variant's planted twin - a known infiltration-like gradient,
   lambda0 = 6 mm, imaged through the real windows - reads 0.15-1.10 x the minimum detectable effect (MDE), below 1 on
   four of six rows (ve25a, all grids). Across the lineage the recorded twin / MDE instruments range 0.01-2.5. Edema
   marks are strongly autocorrelated (design-effect n_eff / n = 0.003-0.017, LESSONS L0.14), and on S02 the sector
   jackknife rests on 4-5 informative sectors of the nominal 14.
2. **Physics can mimic the target.** Under a fixed polarity ("lower ADC, shorter T1/T2 = tumour-like"), vasogenic fade
   toward normal white matter and slab partial volume at the FLAIR-drawn edema border produce a lower-water signal
   near the border. For border-referred estimands that is the target's sign; for a core-referred centre of gravity it
   is the opposite sign to the literature (Lemercier) direction. Every border and depth operator the loop tried was
   judged by the PHYS lens to reproduce one of these signs, and border readings grew when the slab was thickened x1.5.
3. **No concordant carrier.** In the core-referred fixed-polarity family (ve13b, ve16b, ve25a's lower-water read-out),
   ADC and MRF T1 point in opposite directions within each subject and the two subjects mirror each other. D7 = 0/51
   also reflects the 1-unit magnitude floor: the border-zone variants (section 4.4) agree in sign on all four S03
   acquisitions (z 3.5-8.6) but read under 1 mm and are null on S02.
4. **Label-only relations carry little here.** The label field is supercritical on every grid (Dobrushin sum 3.4-4.4,
   needs < 1; LESSONS L0.14), the enhancing rim fails the two-voxel thickness gate on every grid (3.35 mm S03,
   1.72 mm S02, i.e. under one voxel through-plane on 4 mm series), and none of the three nesting-preserving label nulls
   tried on synthetic proportional-layer lesions was both nesting-preserving and powered (`hrel/nulls.py`, strict
   xfail in `tests/test_nulls.py`; synthetic evidence, not a proof, not run on the real lesions).

**Search limits (recorded by the loop itself).** The lineage concentrated under the v03 seed (every child in epochs
21-25 descends from it, and the parent-diversity rules were broken in every epoch; fixed epoch slots were imposed only
after the last epoch). The scorer used a single structure-matched seed, a sign-blind D6, a D2 that needs a carrier, and
a 1-unit floor on D7 / D8 that sub-mm estimands cannot reach. The variant contract scores one native grid per call, so
fusion across acquisitions (operator M15) was never scored on real data. The water-conditioned mark M21 was never run.
The active red-team bank froze at its cap after epoch 11: a12-a25 were written as inactive candidates, so 16 of the 26
probe modules never scored anything.

The honest T0 output is therefore an **underpowered null** with bounds in the statistic's own mm (section 4.3), not a
pass count.

## 2. What ran

| mechanism | origin | what it did here | evidence that it changed the outcome |
|---|---|---|---|
| RQGM generator vs evolving evaluators | Red Queen Goedel Machine | 2 generators + 3 evaluator lenses (STAT identifiability, PHYS MR physics and data defects, CLIN clinical impact and Occam) per epoch; pre-registered rung ladder E1-E4 | rung never left E1 (bar: 8/11 with lens mean >= 6); 35 of 50 children rejected by >= 2 lenses |
| evaluator escalation from the evaluators' own findings | Red Queen (evaluator side) | the E1-E2 lenses showed how scorer v2 could be passed without evidence; the orchestrator tightened it (scorer v3, harness v3; LOG.md) | abstention under a probe became a failure: ve02a fell from 6/11 to 2/11; worst-case synthetic false positive replaced the median |
| co-evolving adversarial test bank | self-play / adversarial data | 26 probe modules written (a00 from the claim audit, a01-a25 by the red team); at most 10 active; a12-a25 stayed inactive candidates | multi-seed structure-matched nulls removed the S02 ADC carriers; slab x1.5 exposed partial volume at the FLAIR border |
| open-ended archive, parent selection by score x novelty | Darwin Goedel Machine | every variant kept; parents drawn from the whole archive | 56 variants, 14 families; in practice the lineage stayed under v03 (see search limits) |
| quality-diversity niches | MAP-Elites | the explore slot had to fill an empty or weak family | families added by the loop: border-zone-gradient, polarity-shell-level, signature-polarity-order, cross-habitat-mark-correlation, directional-profile, multichannel-fusion, marked-topology, transplant |
| verbal reinforcement memory | Reflexion | one lesson per lens per epoch, passed to the next generators | 75 lessons (LESSONS.md); the recurring ones became pre-flight checks |
| self-improving improver | STOP | a meta-agent rewrote the generators' operator playbook every 5 epochs from observed yield | playbook v1-v5: 19 operators retired, M11-M22 added, a power pre-screen made a hard gate, fixed epoch slots, and M21 (water-conditioned mark) proposed as the unexplored move |
| TDD tournament with mutation-tested judge (fix phase, outside the loop) | AlphaCode-style selection + mutation testing + Reflexion retry | blind test-writers, two competing implementers, a judge that re-ran the tests and injected mutants | `hrel/potts.py` (44 tests), `hrel/gates.py` (59), `hrel/nulls.py` (31, one strict xfail recording a spec defect found by two independent agents) |
| independent refuter pass (claim audit, outside the loop) | adversarial verification | a fresh refuter re-derived every adverse audit finding | 78 of 136 findings modified, including 17 S02 readings that were cross-patient over-reach (doc 30) |
| fresh critic pass on this report (outside the loop) | debate / self-refine | a fresh agent recomputed the numbers and attacked the claims | 11 wrong statements corrected in this version (revision record) |

## 3. Outcome against the pre-registered DONE criteria

Scorer v3 over the fitness JSON the archive records for each variant: 51 variants (the duplicate ve19b included;
ve05b, ve15b, ve19a, ve21a and ve23b recorded no JSON in their epoch). Archive JSONs come from the 5 core grids (all
independent acquisitions are on them) and from red-team banks that changed by epoch.

| criterion | what it asks | variants passing |
|---|---|---|
| D1 monotone-map invariance (AX-1) | rank marks unchanged under gain, gamma, 1.5 -> 3 T dispersion | 48 / 51 (every mark-based variant; the 3 failures are label-only seeds, which cannot pass by rule) |
| D2 registration residual | one-voxel label moves < 2 units and < half the effect (needs a carrier) | 6 / 51 |
| D3 resolution | through-plane coarsening x2 | 38 / 51 |
| D4 null centring | real permutation null centred and worst synthetic null <= 2 units | 39 / 51 |
| D5 power | signed, separated recovery of a planted coupling | 22 / 51 |
| D6 effect | beyond 3 jackknife SE and 2 x the scored structure-matched draw in both subjects | 6 / 51 (sign-blind; none concordant) |
| D7 generality | one sign across acquisitions within and across subjects, outside a 1-unit floor | **0 / 51** |
| D8 S02 edge | invariance on S02 and the same non-noise sign as S03 | 2 / 51 |
| D9 defect | sees a two-slice label displacement (needs D2) | 4 / 51 |
| D10 simplicity | <= 3 knobs | 51 / 51 |
| D13 red team | every active red-team probe within 2 units | 18 / 51 |

Percentile marks are invariant **by construction** to global monotone maps, which is all D1 tests. Invariance to a
spatially varying gain, 3 T B1+ error and field strength itself is not established (the bias probe is reported, not
gated; the red-team bias and B1+ probes are nulls, not invariance tests).

## 4. The candidates (the loop never reached rung E4; the orchestrator re-ran the front on all 8 grids per subject with the final bank)

### 4.1 Core-referred edema centre-of-gravity shift (ve11b; instrumented as ve13b, headline bit-identical)

*Definition (for a radiologist).* On one native series at a time (ADC, MRF T1 map, MRF T2 map, T2 FS), each voxel is
placed within the patient's own normal-appearing brain far from the tumour (a percentile, so scanner units cancel) and
signed by a direction fixed in advance (lower ADC or shorter T1/T2 = less free water = more tumour-like; Lemercier et
al., AJR 2014; Blystad et al., PLoS One 2017). In the edema at least 3 mm from the core and 3 mm inside the outer
edema border, out to 20 mm, split into 14 directions seen from the core, the tumour-like and the free-water-like
signal each get a centre of gravity along the distance from the core. The headline is their separation in mm: +2 mm
reads "the tumour-like signal sits 2 mm closer to the core than the water-like signal"; 0 is what reshuffling the
signal inside the edema gives.

*Standing.* ve13b is the only variant all three lenses held with validity >= 5 (validity 6, robustness 5, insight 6;
ve02b, ve05b and ve21a were also held, at validity 3, 0 and 0; ve25a drew the archive's only "advance"). Its parent
ve11b scores validity 6, robustness 5, simplicity 7. It is exactly centred by derivation, rank-invariant, and passes
the active red-team bank. The literature supports the near-far ADC gradient in peritumoral edema as a diagnostic /
phenotype descriptor (Lemercier 2014), not as a target-volume margin rule; the clinical lens never scored the family
above impact 3 (D11 not met).

*Verification (ve13b and ve11b, all grids): 5/11* - D1, D3, D4, D10, D13 pass; D2, D5, D6, D7, D8, D9 fail.
Headline per independent acquisition (mm +/- sector-jackknife SE):

| subject | MRF T1 | MRF T2 | ADC | T2 FS |
|---|---|---|---|---|
| S03 (1.5 T) | +0.17 +/- 0.26 | +0.51 +/- 0.35 | -0.11 +/- 0.51 | +0.38 +/- 0.58 |
| S02 (3 T) | -1.10 +/- 0.60 | -0.59 +/- 1.37 | +1.44 +/- 0.85 | -0.24 +/- 1.85 |

Largest |z| 1.85; no carrier; per-acquisition signs disagree within and between subjects. Secondary instrument
`iface_auc_excess` = P(a core-facing edema voxel is more tumour-like than a border-facing one) - 1/2 is negative on
every S03 acquisition (-0.12 to -0.16, SE 0.01-0.06): the "tumour-like" (lower-water) signal faces the white-matter
border, as vasogenic fade and partial volume would make it.

### 4.2 Equal-vote fusion (ve16b)

*Definition.* One polarity-signed statistic per independent acquisition, equal pre-fixed weights, one vote per
acquisition: on the MRF grid the vote is the **MRF T1 term alone** (T2 is recorded, never votes). Its read-out is
ve15a's (14 sectors x 4 border-depth layers plus a deep term, core-body slices), not ve13b's.

*Verification (all grids): 6/11* - D1, D3, D4, D6, D10, D13 pass; D2, D5, D7, D8, D9 fail.

| subject | MRF (T1 vote) | ADC | T2 FS |
|---|---|---|---|
| S03 (1.5 T) | +1.31 +/- 0.96 | -0.65 +/- 0.15 | -0.43 +/- 0.24 |
| S02 (3 T) | -0.80 +/- 0.30 | +1.87 +/- 0.50 | -0.07 +/- 1.07 |

Synthetic: nulls <= 0.55 mm; planted lambda0 = 3 / 6 / 10 mm read 1.9 / 3.0-3.4 / 3.3-3.8 mm (Spearman 0.84; minimum
separation 1.93 units against a 2-unit bar). The synthetic T1-like channel plants longer T1 near the core, opposite to
the MRF T1 polarity used on real data, so D5 validates the machinery, not the MRF T1 direction. Its D6 pass is
sign-blind: the two carriers are both ADC but opposite (S02 +1.87 mm, the Lemercier direction; S03 -0.65 mm), and the
S02 row does not clear the off-seed structure-matched maximum recorded for the same read-out (LOG E16: 1.40 mm, and
2 x 1.40 = 2.79 > 1.87). The fusion itself never happens on real data (each grid carries one acquisition), and its own
pre-run found almost no precision gain (replicate correlations +0.82 to +0.97).

### 4.3 Bounds from the most instrumented variant (ve25a, 7/11 on all grids; D2 and D9 rest on the single-seed S02 ADC carrier)

ve25a's headline is **ET-likeness at equal depth below the outer edema border** (each edema voxel's resemblance to
this patient's enhancing-tumour signature), a different estimand from 4.1; its secondary `pol_partial_cog_mm` is the
lower-water read-out of the same geometry. Both carry an MDE (the maximum of 3 x jackknife SE and 2 x each recorded
floor: the 20-seed structure-matched maximum, the one-voxel registration residual, the +-2 slice label-shift envelope,
partial-volume twins at slab x1 and x1.5, vasogenic-fade twins, the bank's slab x1.5 and lesion-edge deviations, EPI
phase-encode shift and blur on ADC, a 3 T B1+ twin on MRF, the S02-like bias on non-ADC rows) and a bound
|observed| + MDE. Lower-water read-out:

| subject / acquisition | observed (mm) | MDE (mm) | observed / MDE | 20-seed structure-matched z | informative sectors g | readings above this are ruled out by every recorded floor |
|---|---|---|---|---|---|---|
| S03 MRF | +1.56 | 5.51 | 0.28 | 1.36 | 9 | 7.1 mm |
| S03 ADC | -0.39 | 3.09 | 0.13 | -0.56 | 9 | 3.5 mm |
| S03 T2 FS | -0.24 | 3.43 | 0.07 | -0.33 | 9 | 3.7 mm |
| S02 MRF | -1.15 | 3.59 | 0.32 | -1.44 | 4 | 4.7 mm |
| S02 ADC | +2.21 | 6.77 | 0.33 | 1.65 | 4 | 9.0 mm |
| S02 T2 FS | +0.01 | 4.17 | 0.00 | 0.01 | 5 | 4.2 mm |

(ET-likeness headline, for completeness: observed S03 -0.61 / -0.39 / -0.25, S02 +0.92 / +2.21 / -0.42 mm; MDE
5.47 / 3.27 / 3.71 and 2.96 / 6.77 / 3.00; its planted lambda0 = 6 twin reads 0.84-3.30 mm, i.e. 0.15-1.10 MDE.)
The binding floor per row (decomposed from the recorded composite, whose JSON driver code is 0 on every row): the
20-seed structure-matched maximum on S02 ADC, S02 T2 FS and S03 MRF; 3 x jackknife SE on S02 MRF; the +-2 slice
label-shift envelope on S03 ADC and S03 T2 FS. The physics twins moved the statistic by <= 0.43 mm (fade) and
<= 1.4 mm (EPI shift, S02 ADC).

*Reading.* No row has observed / MDE >= 1. The bounds are in the statistic's own mm, not tissue mm: the planted
6 mm gradient itself reads 0.84-3.30 mm, so the bounds equal 1.0-7.3 x that reading. No coverage level is claimed.
Stated at T0: **in the interior edema of these two subjects, a core-ward centre-of-gravity separation of the
lower-water signal larger than 3.5-9.0 mm (statistic mm, by acquisition) would have exceeded every recorded floor;
none did. Smaller effects, including the planted design gradient on four of six rows, cannot be ruled out.**

### 4.4 The near-miss: border-zone ordering (ve21b; soft-shell version ve22b)

*Definition.* The same rank marks, read in the outer edema zone near the FLAIR-drawn border (the T2/FLAIR zone the
ESTRO-EANO guideline asks clinicians to judge), ordered by depth below that border.

*Standing.* ve21b: 5/11 (D1, D3, D4, D10, D13), validity 5, impact 5 (the highest impact any variant received),
simplicity 7; ve22b: 5/11. On **S03** both carry effects that clear the jackknife and the multi-seed structure-matched
null on every independent acquisition with one sign (ve22b z 3.5-8.6 on MRF T1, MRF T2, ADC, T2 FS; ve21b z 2.2-4.6),
and they are robust to the one-voxel registration residual (ax2 0.2 units). On **S02** they are null (|z| <= 0.8).
They fail D7 on magnitude (S03 median 0.42 mm and 0.19 mm, under the 1-mm unit) and fail the full MDE on the jackknife
or on the slice and twin terms (ve22b S03 T2 FS at 0.995 MDE).

*Why it is not a winner.* The PHYS lens read the positive S03 sign as the vasogenic-fade signature, the reading grew
under slab x1.5, and ve22b's S03 value equals the definitional FLAIR row and moves 30-100 % under a one-voxel WT erode
or dilate (LOG E21-E25). The clinical lens found no anchor for a border-referred ordering at equal core distance.
It is the most reproducible within-subject signal the loop found, and the one the water-conditioned mark (section 6) is
designed to decide.

## 5. Descriptive observations about habitat interaction (tier T0, n = 2 local)

These are rank-invariant by construction; the transition profiles were **not** run under the registration or
resolution probes, use one permutation draw for the null step, and rely on 4-5 informative sectors on S02.

1. **S03: core and edema sit at nearly the same rank; the sharp transition is the edema/white-matter border.** On the
   independent acquisitions (transition profiles, `hrel/transition_profile.py`): MRF T2 0.75 vs 0.76, T2 FS 0.82 vs
   0.83, ADC 0.66 vs 0.69 (core vs near edema); MRF T1 steps 0.78 -> 0.70. Every acquisition drops at the edema border
   (to 0.33-0.44 in the first peritumoral white-matter band) and decays toward NAWM over ~20 mm.
   **S02 is different:** the core-edema gaps are 0.07-0.14; ADC shows no step at the border (0.26 on both sides); T2 FS
   and ADC rise, not fall, toward NAWM beyond the border.
2. **Hypothesis, not finding: inside the tumour core the label boundaries may be permeability rather than signature
   boundaries.** In MRF T1+T2 signature space the enhancing-rim prototype attends to the necrotic one about as much as
   to its own (S03 0.32 vs 0.33; S02 0.33 vs 0.26, with ET -> ED 0.25), while NAWM is crisp (0.99 / 0.90). The
   competing explanation is partial volume: the rim is thinner than two voxels on every grid, and the within-habitat
   null reproduces the full attention table (lift <= 0.007).
3. **Edema interior.** S03 stays within 1.8 SE of the within-habitat null step on every acquisition. S02 deviates by
   4-5 SE in the outer edema (MRF T1 +4.8, T2 FS -4.9 and ADC -4.3 at 15-25 mm; MRF T2 -5.2 at 10-15 mm) and by -2.4
   SE on ADC at 5-10 mm, on 4-5 informative sectors, in opposite directions across acquisitions.
4. **Label-label "interaction" restates the labelling convention.** Face contacts, band co-occurrence, Potts couplings
   and topology of BraTS habitats are set by NCR-in-ET-in-ED nesting, supercritical, and below resolution on these
   grids. The published MSI/GLCM comparator (v00) passes 1 of 11 criteria (simplicity only) and moves 5.2 units under
   the one-voxel label probes.

Attention-map view (the owner's question): `hrel/attention_maps.py` renders habitat x habitat attention per distance
band (queries = voxels, keys = habitat prototypes in the invariant MRF signature space), real vs within-habitat null
and their difference (the lift), as aggregate heatmaps; per-voxel overlays of ET-likeness and edema-likeness are LOCAL
ONLY. The transition profile is the one-dimensional version of the same map.

## 6. What would move the ceiling (pre-registered, not run: the 25-epoch cap is respected)

- **Epoch 26, operator M21 (water-conditioned mark), pre-registered by the STOP meta-agent.** Replace the
  fixed-polarity mark by its water-conditioned residual on one grid: MRF T1 rank minus its expected rank given MRF T2
  (monotone fit on whole strata), tumour-like = "shorter T1 than the water content predicts"; vasogenic fade and NAWM
  partial volume move T1 and T2 together and cancel to first order. **Conflict to resolve first:** doc 31 (condition
  iii) reserves the MRF T1-T2 dependence as a negative-control pair, because both maps come from one dictionary fit;
  M21 uses that pair as a conditioning variable, so its gates must include a dictionary-coupling twin, besides the
  vasogenic-taper sweep (2-10 mm, under 0.5 MDE), PSF-only and slab-profile twins, a 3 T B1+ twin on S02 MRF and the
  power pre-screen. First target: the S03 border-zone signal of section 4.4.
- **M22 (power-screened pooling).** Choose the coarsest geometry-only partition whose planted twin reaches >= 2 MDE and
  >= 3 x the structure-matched rms, chosen from label geometry and twins only.
- **Harness.** A subject-level contract so acquisitions on different native grids can be combined at band level in mm
  without resampling maps; a base-call hook for instruments (generators used object-id detection); >= 20 permutation
  and structure-matched draws in the scorer; a sign-concordant D6; a D2 that does not require a carrier; activation of
  the red-team candidates a12-a25 against the front.
- **Data (the real ceiling).** More subjects (every current stratum has n = 1); thinner or isotropic slices (the rim is
  under one voxel through-plane on the 4 mm series); B1+ maps at 3 T; soft segmentation posteriors (every latent-Z
  claim is blocked on hard labels); longitudinal scans for H3/H8 and the temporal-comparability lemma.

## 7. What was not verified

- No fresh-agent rung-E4 re-derivation: the orchestrator re-ran four front variants (ve13b, ve11b, ve16b, ve25a) on all
  grids; the other archive scores are from the loop's own core-grid runs under the bank of their epoch.
- The Dobrushin sums, thickness values and n_eff ratios come from one orchestrator run recorded in LESSONS L0.14, with no
  stored aggregate file behind them.
- The transition profiles and attention tables were not run under the AX-2 / AX-3 probes.

## 8. Files

- Loop record: `DONE.json`, `PLAN.md`, `PLAYBOOK.md` (v5 with history), `LESSONS.md` (L0.1-L0.15 + 75 loop lessons),
  `LOG.md` (harness changelog + epoch log), `archive.jsonl` (every variant with lenses, verdicts, killers).
- Code: `hrel/variants/` (6 seeds + 50 loop variants), `hrel/adversarial/` (26 probe modules), `hrel/potts.py`,
  `hrel/gates.py`, `hrel/nulls.py`, `hrel/transition_profile.py`, `hrel/attention_maps.py`, `score_variant.py` (v3).
- Audit and rethink: `Synthesis/HEROBridge/DerivationLab/30_Hypothesis_Axiom_Lemma_Audit_2026-09-25.md`,
  `31_Amendments_and_Concordance_2026-09-25.md`, `derivations/lambda_temporal_comparability.md`.
- Local only (git-ignored sample folder): fitness JSONs, verification JSONs, the attention and transition figures.

## Revision record

- 2026-09-26 v1: written by the orchestrator after the loop and the full-grid verification.
- 2026-09-26 v2: fresh critic pass applied. Corrected: v00 numbers (1/11, 5.2 units; the earlier 18.7 came from a
  harness-v1 run); section 4.3 now reports the lower-water read-out and names ve25a's headline as ET-likeness; the
  binding MDE terms; the ve16b MRF vote (T1 only) and its read-out; which carriers fell to which null; the reason for
  D7 = 0/51 (adds the 1-unit floor and the border-zone near-miss, new section 4.4); the S02 edema description; the
  "only variant held by all lenses" claim; the section-3 selection rule. Narrowed: the invariance claim (by
  construction, global monotone maps only), "precise null" (now "underpowered null", statistic mm, no coverage),
  impossibility wording (synthetic constructions), the permeability statement (hypothesis, partial volume competing),
  the clinical-anchor wording, the 7/11 front (single-seed dependence). Added: terms, search limits, what was not
  verified, the M21 negative-control conflict. Removed a lesion-location descriptor.
