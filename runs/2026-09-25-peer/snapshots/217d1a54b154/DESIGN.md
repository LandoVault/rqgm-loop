# RQGM Loop — design from first principles

Any loop that improves an artifact by asking LLMs "is this better?" must solve the eleven problems
below; the table names the one mechanism v3 keeps for each. The evidence shows the problems are
real; no mechanism has yet been shown to improve outcomes in a logged task run.

## Evidence labels

- **measured (v1 run)**: seen in `runs/2026-09-22-rrsi/` (run 1) or `runs/2026-09-22-meta/`: one run
  each (n = 1) under v1-era procedures (scalar gate, bundles, winner carry-over, a parallel Workflow
  harness). Tallies are correlated judge calls from one model family, not trials; each names its record
  file, plus the commit where a record was later edited or rebuilt.
- **measured (text dry-run)**: agents walked the spec's branches; no loop ran.
- **literature**: verified in `runs/2026-09-22-meta/research.json`, `runs/2026-09-25-peer/register.json`
  (literature) or `runs/2026-09-22-rrsi/grounding.md`. Industry write-ups are named.
- **design-only**: reasoning. Every mechanism cell is design-only until a v3 task run measures it.

Labels are never upgraded; no v1-run or dry-run failure is presented as a v2 or v3 defect.

## The problems → the mechanism kept

| # | Problem | Mechanism (design-only) | Evidence |
|---|---|---|---|
| 1 | **Objective.** "Better" drifts unless written down; tests can be gamed. | `DONE`: atomic criteria, required or optional, checked by `command` (it decides; its `files` are check files), `source` (the Verifier) or `judges` (a preference, never proof). Check files, `DONE`, the rubric and `BUDGET` change only by human `amend`. Commands run on a fresh copy; failing one *best* passes rejects the variant before judging. | Hazard, literature: SpecBench 2605.21384; Anthropic *Effective harnesses* (don't edit the tests); 2503.05061 (judge competence bounds reliability). |
| 2 | **Independence.** Reviewers favor work like their own; judges' errors correlate. | Separate roles; the writer never judges. Judges from another model family where available; one family = one source (`verdicts[].model`, `check.models`). Without subagents the human runs every other role in fresh chats, else HALT(OPEN). | Literature: RQGM 2606.26294, its strongest baseline reviewer over-accepts AI-generated papers at up to 1.91× the human rate (`grounding.md`); 2506.07962, errors correlate most within a provider; 2603.00077. |
| 3 | **Signal.** Absolute scores are noisy; pairwise judges show order bias and leniency. | Blind pairwise comparison with *best*, per criterion; cosmetic = tie; judge 1's two orders disagreeing is UNKNOWN. UNKNOWN and ERROR (retried once, then dropped, not rejected) never support. Per rung, a 5-call probe (judge 1 on identity and seeded pairs, both orders; one Check judge), never seeded by the generator; a non-tie, miss or ERROR, or no `judges` criterion (no probe) → strict mode. A Check is 3 calls, each judge marking every `judges` criterion. | Measured (v1 run): run 1 stalled at its absolute-score gate (`rrsi/log.md`). Literature: 2609.17857 (open-weight preprint), 55.4% of AB/BA pairs reverse; 2510.11822, validator true-negative rate under 25%; FLAWS 2511.21843 bears on the Check; 2607.23002, a silent output cap faked an effect; 2506.03785. |
| 4 | **Goodhart.** The generator optimizes whatever the judge rewards. | A Screen (diff and rubric only) reads every variant before judging and rejects gaming; an LLM pass, it can miss. Judges never see the generator's rationale. The ledger blocks ideas rejected by ≥2 judges or twice by the Screen. | Measured (v1 run): run 1's screen rejected 11 edits (`rrsi/log.md`; 12 until c3eebb2 edited it). Meta-run: 13 substantive screen rejections + 2 apply errors (e5-A, e18-B), now ERROR, of 47 variants (`ledger-e1-9.json`, `result-e9-19.json`); one idea was screened out 3 times (`meta/log.md`). Literature: RRSI 2609.24972, a pre-evaluation leakage critic (`grounding.md`). |
| 5 | **Truth.** The generator can invent facts. | The Verifier checks every claim against a primary source it read (a `citation` each); in a variant, contradicted → strip, not-found → `[OPEN]` on a criterion; v0's failures stand until a round fixes them; a `source` criterion passes only if all its claims verify. No fabricated substrates. An `[OPEN]` in *best*, unless waived or its criterion optional, → HALT(OPEN) until the human waives (`amend`) or closes it (`substrate.evidence`) and a round writes it in. | Measured (v1 run): `grounding.md` marks RRSI's truncated Table 5 values UNVERIFIED, never to be cited. Cursor's reward-hacking write-up: audit before trusting a score. |
| 6 | **Search.** Bundled edits can't be credited; failures repeat. | 2 variants per round, one change to one section each, naming a criterion; a multi-section restructure needs the human's `approve`. Required criteria still non-pass after 3 stalls → HALT(STALL). `GROUNDING` may carry exemplars. | Measured (v1 run): judged variants won 16 of 17 in meta e1–e9 (`ledger-e1-9.json`, rebuilt in c237491) and 10 of 15 in lean e10–e19 (`result-e9-19.json`). v2 removed run 1's scalar gate outside any round (ff9eab2). Literature: RRSI §3.2 (`grounding.md`); 2507.19457; 2604.25850; 2605.24539. |
| 7 | **Selection.** Keep only real, non-regressing gains, without bloat. | Keep on ≥2 preferences (strict: 3), none for *best*, no protected item rated worse, UNKNOWN or not at all (fail closed; costs some keeps); a shorter variant needs 3 completed judges without UNKNOWN. Keep one, exactly as judged. Restoring an earlier *best*'s section up to cosmetic differences → HALT(OSCILLATION) after its `version`; the human picks a logged version (`approve`). Preference is not transitive: the command gate, protected veto and each Check's full re-marking catch regressions. | Literature: RRSI complexity-aware acceptance (low-gain rule, `grounding.md`); 2604.13717; 2602.13110. The two-tie prune gap: design-only, found by a policy prototype. |
| 8 | **Generalization.** The loop overfits its own judges. | Rungs (human-only): E1 fair → E2 adversarial → E3 a human-added objective. Final check: 3 human-written held-out judges only the human sees or runs, stored outside `TARGET`, `GROUNDING`, `MEMORY` and the repo, single-use per `TARGET`. The human reports the marks and votes (`heldout.results`; Check rule), so UNKNOWN or ERROR never passes; each non-pass is non-pass in *best*'s Check. The first result is reported; spares run only on a changed *best* passing Check; a second non-pass → HALT(OVERFIT). | Literature: RQGM 2606.26294 uses no majority vote; ours is design-only; 2510.11822's minority veto awaits Stage-6 data. Measured (v1 run): 3/3 held-out judges preferred the meta-run result pairwise (`meta/log.md`); no pass/fail check ran. Held-out rationales sit in the repo (`result-e9-19.json`). |
| 9 | **Stopping.** Loops burn budget on plateaus; only a human supplies real data. | Stalls count merit only; two all-ERROR rounds → HALT(ERROR). Check after 3 stalls or a `DONE` claim; results stand until *best*, the rung or `DONE` changes. Budget: rounds, plus host-reported minutes and tokens (else `null`, never estimated); a round starts only if each holds twice the costliest round; only `amend{budget}` changes it. | Measured (v1 run): e18, one of the 3 empty epochs before the meta-run's HALT(STALL), had one variant judged (`result-e9-19.json`); token totals are missing for run 1 and meta e1–e9. About 60K subagent tokens per agent call (4.52M/75, `meta/log.md`). Literature: 2604.22750, models cannot predict their own usage; 2606.27009. |
| 10 | **State and cost.** Long runs crash; context is the main cost. | Append-only `MEMORY`, one writer (print mode: the human keeps and pastes back records). Round-atomic resume: set aside a torn last line, log `resume`, rerun an unfinished round; log before writing `TARGET`. After a halt or audit violation, only the human resumes (logged). | Measured (v1 run): 5 wasted re-runs "on the broken resume" (`meta/log.md` at 3dd6700; the "out of order" cause, added in c3eebb2, is not relied on). About 6.8 vs 11 agents per epoch, lean vs earlier (`meta/log.md`): calls per round, not cost per verified outcome. |
| 11 | **Enforcement.** Where no code runs, an orchestrator can misapply its rules. | The prose is the contract; rules are local and fail closed. The optional read-only `rqgm_check.py` recomputes the keeps, drops, Checks, halts and exits its records allow, and never decides or writes; rules it cannot or does not yet check are listed below. Where it runs, a violation pauses for the human; Output says whether it audited. | Motivation, measured (text dry-run): the two v2 dry-runs flagged 10, then 8, ambiguities (`meta/v2-validation.json`, `meta/v2-revalidation.json`). Remedy: design-only; promotion to code is pre-registered (Deferred). |

## Non-guarantees

- Prose runs make no claim of atomic saves, a hard budget or crash-safe resume.
- Held-out secrecy is only as good as where the human stores the prompts.
- No judge PASS establishes truth; the Screen, Verifier and judges are LLM passes and can miss.
- Human decisions relayed by an agent are unauthenticated.
- The audit checks internal consistency, not whether records are honest: the orchestrator writes `MEMORY`.

## What was removed

Removed from earlier versions: the absolute 0–10 gate and its parameters (row 3); bundles (row 6);
dissent-triggered escalation, E4 and re-offering losers
(lenient judges produce no dissent). Rejected, with reasons in `runs/2026-09-25-peer/blueprint.json`
`rejected`: the paraphrase probe control and judge replacement on a miss; the
least-recently-changed fallback; model-written hashes, per-call usage and keys; the exact-text
oscillation test; an owning controller; sidecar rule files.

## Pending `rqgm_check.py` changes

Each change adds a fixture.

| Rule (record) | `rqgm_check.py` change |
|---|---|
| Unrated protected id (`verdicts[].criteria`) | `panel()`: a veto (p23_complete_spare gains ratings) |
| v0 length (`version` v0) | v3: RECORD_MISSING; a prune is not credited |
| Check files (`criteria[].files`) | v3: RECORD_MISSING on a `command` criterion |
| Gate retries (`gates.retries`) | v3: RECORD_MISSING |
| `source` Check (`citation.version`) | `r_check`: all that version's citations for it verified |
| Held-out marks (`heldout.results{id:{value,votes}}`) | `r_heldout`: recount by the Check rule |
| Waiver (`amend.gap`, `substrate`) | `next_due`, `pre()`: all required gaps waived after a halt → Stop |
| Closed gap (`substrate`) | `open_required`: required until a later keep removes an `[OPEN]` |
| Spares (`heldout`) | `next_due`: rounds until a changed *best* passes Check |
| Stop below the final rung (`exit`) | none |

Unauditable: held-out secrecy, role separation, relay authenticity, the cosmetic-differences judgment,
section boundaries, judge 1's logged confidence, a check editing files, and a Screen or Verifier
verdict relabelled ERROR.

## Deferred

| Item | Promotion trigger |
|---|---|
| Live enforcing controller | Stage-1 threshold crossed, or a pilot decision-changing VIOLATION or journal mismatch |
| Per-call keys | A logged v3 resume re-runs completed calls |
| Full per-judge probe | Stage-6 per-slot miss rates differ |
| Minority-veto Check | Stage-6 false-pass above 50%, tested prospectively |
| "A command newly passing counts as support" | A T1 stall with command-fixing variants rejected |
| P+audit arm | After the first pilot |
| Rung-scoped ledger lapse | E2 derivations blocked by E1 rejections in a logged run |
| Substrate export | A consumer exists |

## Validation status

- **Design review.** v3 was designed outside any run (`runs/2026-09-25-peer/blueprint.json`). It stays
  "design review" until a logged run on a task other than its own spec; a recursive meta-run on the
  spec is design review only.
- The v1 meta-run: judges preferred the result; the loop was not run on a task.
- No matched-budget baseline has been run (2607.12227).

## Validation protocol (pre-registered summary)

- **Stage 0** (no model calls): caps; `rqgm_check.py selftest` P01–P23, positive fixtures included;
  each rule mapped to a checker rule or marked unauditable; harness tests; scorer sanity.
- **Stage 1** (~90 short calls): 30 frozen archive states; answer key `audit --pending`, adjudicated
  by the human; 3 fresh Claude contexts answer from SKILL.md, one GPT upload from the paste. ≥3/30
  errors in any context, or a class wrong in 2 of 3 contexts, makes that rule checker-mandatory where a
  shell exists (v3.1).
- **Stage 2** (≤20 toy-target calls): cap C = 1.25 × the larger minimal complete path; human-approved
  spend; `manifest.json` frozen before any scored call.
- **Stage 3**: T1, T2 (T3 if written blind after the freeze) × arms S (one strong agent), B (best-of-N,
  fixed verification), V (v2), P (v3 prose, no `rqgm_check.py`); one run per cell, one model family
  (disclosed); S and B also at 0.5×C; a sealed deterministic scorer.
- **Stage 4**: V and P under identical injected faults, including a real mid-round kill.
- **Stage 5** (zero calls): `audit --first` on P archives; `compare.py` checks records against the raw
  journal; contamination voids a run.
- **Stage 6**: judges score human-seeded defects (miss, false-pass, order reversal).

Primary outcome: false completion (COMPLETE while the scorer finds a required failure). Decision rules:
a P false completion, decision-changing VIOLATION or journal mismatch makes that rule checker-mandatory
where a shell exists. P below S or B on any task: no "improved" claim. S or B at or above P everywhere:
"no advantage observed over simpler methods on these cases". Stage-6 false-pass above 50%: that task
type's Check passes are unreliable. Results per case, no significance claims. T2's optional field was
co-designed with P's optional-`[OPEN]` rule, so V failing T2 is not evidence.

## Maintainer process rules

- Run records are never edited; corrections are appended as `correction{record,why}`.
- Evidence-run archives are committed (`.gitignore` exception `!runs/**/archive*.jsonl`) or their
  SHA-256 is logged in `log.md`.
- A spec change outside a run is a new version labelled design review; it invalidates the Stage-1
  answer key until the human re-adjudicates it.
- A rule change names its record fields and checker rule, or declares itself unauditable.
- Word counts use `str.split`, markdown tokens included; formatting savings are disclosed separately.
