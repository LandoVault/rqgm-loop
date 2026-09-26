# RQGM Loop — design from first principles

Any loop that improves an artifact by asking LLMs "is this better?" has to solve the same problems.
The table names eleven and the one mechanism v3 keeps for each. The evidence shows the problems are
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
| 1 | **Objective.** "Better" drifts unless written down; tests can be gamed. | `DONE`: atomic criteria, required or optional, each checked by `command` (it decides), `source` (the Verifier) or `judges` (a preference, never proof). Files a command runs belong to `DONE`; they, `DONE` and the rubric change only by human `amend`. Commands run on a fresh copy with setup-time check files; one that edits files is ERROR. Failing a command *best* passes rejects the variant before judging; a failure *best* shares does not. | Hazard, literature: SpecBench 2605.21384; Anthropic *Effective harnesses* (don't edit the tests); 2503.05061 (judge competence bounds reliability). |
| 2 | **Independence.** Reviewers favor work like their own; judges' errors correlate. | Separate roles; the writer never judges. Judges come from another model family where available; same-family judges count as one source. Without subagents the human relays judges in fresh chats, else HALT(OPEN). | Literature: RQGM 2606.26294, its strongest baseline reviewer over-accepts AI-generated papers at up to 1.91× the human rate (`grounding.md`); 2506.07962, errors correlate most within a provider; 2603.00077. |
| 3 | **Signal.** Absolute scores are noisy; pairwise judges show order bias and leniency. | Blind pairwise comparison with *best*, per criterion; cosmetic = tie. A result is a verdict, UNKNOWN or ERROR (retried once, then dropped, not rejected). Judge 1's two orders disagreeing is UNKNOWN, not a tie. Per rung, a 5-call probe: judge 1 on identity and seeded-defect pairs in both orders, plus one Check judge; the orchestrator, never the generator, writes the seed. A non-tie or miss → strict mode (all 3 judges, no early rejection, 3/3 for keeps and Check passes); tell the human. | Measured (v1 run): the absolute-score gate stalled run 1 (`rrsi/log.md`). Literature: 2609.17857 (open-weight preprint), 55.4% of AB/BA pairs reverse; 2510.11822, validator true-negative rate under 25%; FLAWS 2511.21843 bears on the Check; 2607.23002, a silent output cap faked an effect; 2506.03785. |
| 4 | **Goodhart.** The generator optimizes whatever the judge rewards. | A Screen seeing the diff and rubric reads every variant before judging. It rejects rubric echo, mechanism-free compliance claims, judge-targeting, inert text, weakened guardrails and unevidenced `[OPEN]` removals. Judges never see the generator's rationale. The ledger blocks ideas rejected by ≥2 judges or twice by the Screen. | Measured (v1 run): run 1's screen rejected 11 edits (`rrsi/log.md`; 12 until c3eebb2 edited it). Meta-run: 13 substantive screen rejections + 2 apply errors (e5-A, e18-B), now ERROR, of 47 variants (`ledger-e1-9.json`, `result-e9-19.json`); one idea was screened out 3 times (`meta/log.md`). Literature: RRSI 2609.24972, a pre-evaluation leakage critic (`grounding.md`). |
| 5 | **Truth.** The generator can invent facts. | The Verifier checks every claim, v0's included, against a primary source it read, never loop-written text, logging a locator: verified, contradicted (strip) or not-found (`[OPEN]`). No fabricated substrates. Only a required `[OPEN]` blocks Stop; the human closes it with Verifier-checked evidence or waives it by `amend` (Output: "waived"). | Measured (v1 run): `grounding.md` marks RRSI's truncated Table 5 values UNVERIFIED, never to be cited. Cursor's reward-hacking write-up: audit before trusting a score. |
| 6 | **Search.** Bundled edits can't be credited; failures repeat. | 2 variants per round, each one change to one section of *best*, naming its criterion; failing command checks first. Non-`pass` required criteria after 3 stalls → HALT(STALL), naming a source, an approved restructure or human input. `GROUNDING` may carry exemplars. | Measured (v1 run): judged variants won 16 of 17 in meta e1–e9 (`ledger-e1-9.json`, rebuilt in c237491) and 10 of 15 in lean e10–e19 (`result-e9-19.json`). Run 1's stall was structural (the scalar gate, `rrsi/log.md`); v2 removed it outside any round (ff9eab2). Literature: RRSI §3.2 (`grounding.md`); 2507.19457; 2604.25850; 2605.24539. |
| 7 | **Selection.** Keep only real, non-regressing gains, without bloat. | Keep if ≥2 judges prefer it (strict: 3), none prefers *best*, and no protected item (guardrails, must-not-change constraints, criteria *best* passes) is rated worse. Judge 3 runs unless judges 1 and 2 prefer the same version. Pruning a shorter variant needs all 3 judges completed without UNKNOWN. Keep one (most support, then shorter, then first); apply exactly the judged text. (Nearly) restoring an earlier *best* → HALT(OSCILLATION). Preference is not transitive: the command gate, protected veto and each Check's full re-marking catch regressions. | Literature: RRSI complexity-aware acceptance (low-gain rule, `grounding.md`); 2604.13717; 2602.13110. The two-tie prune gap: design-only, found by a policy prototype. |
| 8 | **Generalization.** The loop overfits its own judges. | Rungs E1 fair → E2 adversarial → E3 a human-added objective, only with the human. Final check: 3 human-written held-out judges, stored outside `TARGET`, `GROUNDING`, `MEMORY` and the repo (unauditable), spent per `TARGET`; majority-failed criteria fail *best*'s Check (`rqgm_check.py` `result()`). The first result is reported; spares run only on a changed *best* passing Check; a second fail → HALT(OVERFIT). | Literature: RQGM 2606.26294 uses no majority vote, so ours is an uncited design choice; 2510.11822's minority veto awaits Stage-6 data. Measured (v1 run): 3/3 held-out judges preferred the meta-run result pairwise (`meta/log.md`); the pass/fail check never ran. Held-out rationales sit in the repo (`result-e9-19.json`). |
| 9 | **Stopping.** Loops burn budget on plateaus; only a human supplies real data. | Stalls count merit outcomes only: a round keeping nothing is a stall unless every variant ended ERROR; two all-ERROR rounds → HALT(ERROR). Check after 3 stalls or a `DONE` claim; a result stands until *best*, the rung or `DONE` changes. Budget: rounds and time from records, tokens `null` unless reported. Start every round only if remaining time covers twice the costliest round; else Check, then Boundary or HALT(BUDGET). | Measured (v1 run): e18, one of the 3 empty epochs before the meta-run's HALT(STALL), had one variant judged (`result-e9-19.json`); token totals are missing for run 1 and meta e1–e9. About 60K subagent tokens per agent call (4.52M/75, `meta/log.md`). Literature: 2604.22750, models cannot predict their own usage; 2606.27009. |
| 10 | **State and cost.** Long runs crash; context is the main cost. | Append-only `MEMORY`, one writer. Round-atomic resume: set aside a torn last line, log `resume`, rerun an unfinished round; log before writing `TARGET`. Caching judges' prefix is a cost note, not a rule. | Measured (v1 run): 5 wasted re-runs "on the broken resume" (`meta/log.md` at 3dd6700; the "out of order" cause, added in c3eebb2, is not relied on). About 6.8 vs 11 agents per epoch, lean vs earlier (`meta/log.md`): calls per round, not cost per verified outcome. |
| 11 | **Enforcement.** Where no code runs, an orchestrator can misapply its rules. | The prose is the contract. Every rule is local, fails closed and can be recomputed from verbatim, un-blinded verdict records. The optional read-only `rqgm_check.py` recomputes every keep, drop, Check, halt and exit from `MEMORY`; it never decides or writes. Where it runs, a violation pauses for the human; Output says whether it audited. | Motivation, measured (text dry-run): the two v2 dry-runs flagged 10, then 8, ambiguities (`meta/v2-validation.json`, `meta/v2-revalidation.json`). Remedy: design-only; promotion to code is pre-registered (Deferred). |

## Non-guarantees

- Prose runs make no claim of atomic saves, a hard budget or crash-safe resume.
- Held-out secrecy is only as good as where the human stores the prompts.
- No judge PASS establishes truth.
- Human decisions relayed by an agent are unauthenticated.
- The audit checks internal consistency, not whether records are honest: the orchestrator writes `MEMORY`.

## What was removed, and why

| Removed | Why |
|---|---|
| Absolute 0–10 gate, δ, `S*`, β formula, prune windows; bundles | Noise as large as the gains stalled run 1; bundles made credit impossible. |
| Gates G1–G6 as a list | Each became a rule above; G1's regression duty moved to the command gate, protected veto and Check. |
| Dissent-triggered escalation, E4, re-offering losers | Lenient judges produce no dissent; claims are verified on entry. |
| Paraphrase probe control; judge replacement on a miss | Paraphrases legitimately change clarity; replacement selects judges on one noisy trial. |
| Least-recently-changed fallback | Section age is not evidence. |
| Stance slogans, the strongest-model line, "2–5 personas" | Repeated rules, unexecutable, or conflicting (held-out judges on the generator's model; 3 slots). |
| "A stable order makes resume deterministic" | Ordering does not prevent re-execution. |
| v2's out-of-paste schema; "a plan worded as a result → reword" | The paste now carries the records; not-found → `[OPEN]` covers plans. |
| Per-call keys, per-call usage, model-written hashes | Without a shell an LLM writes plausible hex; chat hosts cannot see subagent tokens. |
| Exact-text oscillation test | It almost never fires on regenerated text. |
| An owning controller; sidecar rule files | Code-free hosts would become second-class; SKILL.md and the paste must each stand alone. |

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
