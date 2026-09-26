# Peer-input redesign of the RQGM loop — run report (2026-09-25 → 26)

**Bottom line.** The peer agent's Scientific Loop materials were turned into RQGM **v3.1**: a prose-first, fail-closed
protocol (`skills/rqgm-loop/SKILL.md`, `INITIATOR.md`) with a read-only auditor (`skills/rqgm-loop/rqgm_check.py`).
As a *design*, every reviewer prefers it to v2. As a *release*, it is **PARTIAL**: its own adversarial E2 Check and
the sealed held-out judges still fail two criteria (executability, auditability), and the cross-family GPT review
fails five. On two small known-answer tasks (sealed oracles, n=1 per cell, one model family), **a single strong
agent matched or beat every loop arm at about 1/40 of the tokens**; v2 and best-of-24 also produced correct
artifacts, while v3/v3.1 ran out of their 49-call budget on the report task. **No arm ever claimed DONE on a failing
artifact.** Nothing here shows that the loop improves task outcomes; it shows where it costs too much and where
its honesty rules work. Every figure below is in this folder's records.

## 1. Inputs
- Peer (ChatGPT, "Codex"/GPT-6 Astra) materials in `reference materials/`: an agent-organization study design, a
  Yang–Mills reconstruction pilot, and a Scientific Loop async repo starter (20 invariants, verifier levels, state
  machine, contracts, orchestration). Reproduced locally: 18/18 contract tests, 5/5 import hashes (`peer-inputs.sha256`).
- Three consults with the peer, by uploaded Markdown (saved verbatim in `reference materials/` and here):
  `peer_review_rqgm_v2.md` (evidence-and-acceptance contract, 8 replacement blocks, a 198-call pilot plan),
  `peer_review_rqgm_infra.md` (after the user widened scope: an offline single-writer controller, C01–C17),
  `peer_review_rqgm_v3.md` (cross-family review of v3.1, received after local scoring, given no outcomes).
- User scope: infrastructure is in bounds; the paste-and-go prompt must still work alone.

## 2. Process (each step is a committed record)
| Step | What happened | Record |
|---|---|---|
| Intake | 46 peer constraints triaged against v2 (3 readers, conflict finder, 2 literature verifiers → 18 verified papers), adversarially re-ranked | `register.json` |
| Design panel | 3 architects (prose-first / controller-first / evaluation-first), 3 lens judges: prose-first won 3/3 (39/42/39 vs 28–36); an *owning* controller vetoed; read-only auditor + pre-registered promotion rule instead | `blueprint.json` |
| Build | v3 prose installed; DESIGN/README relabelled evidence; auditor built test-first | commit 0f1a0e5 |
| Auditor hardening | 2 adversarial rounds: 54 then 56 breaks found; all evasions now flagged; 181 selftest cases | `checker-attack/`, 1c93f61, 8666433 |
| Recursive meta-run | v3's own procedure (frozen, executed by workflow code) improved its text for 10 rounds: 9 keeps, 4 gate ERRORs, **16/16 judged variants preferred pairwise**; seeded-defect probe caught; fresh E2 Check failed 5/6 → HALT(BUDGET), PARTIAL. Its archive audits clean except null clock fields | `archive-meta.v3.jsonl`, `meta-check-failing.json` |
| Restructure (human-proxy approved) | attempt 1 rejected by the Verifier (DESIGN cited sources that did not support it); attempt 2 dropped by an orchestrator parse bug, fixed and resumed; 2 kept → **v3.1 = 8332bed570f1**; Check failures 5 → 2 | `restructure-*.json`, e99b778, 17d91ec |
| Validation | sealed held-out judges; cross-family peer review; Stage 1 decision scenarios; 10-run pilot with sealed oracles | below |

## 3. Validation results
**Design review (same family unless noted).**
| Criterion | meta-run end | v3.1 in-loop Check | v3.1 sealed held-out (3 judges) | v3.1 GPT review |
|---|---|---|---|---|
| d1 guardrails | fail | pass | pass (3/3) | **fail** |
| d2 executable | fail | fail | fail (3/3) | fail |
| d3 SKILL/paste parity | fail | pass | pass (3/3) | **fail** |
| d4 auditable | fail | fail | fail (2/3) | fail |
| d5 honest | fail | pass | pass (3/3) | **fail (narrowly)** |
| d6 cost | pass | pass | pass (3/3) | UNKNOWN (undefined) |
Pairwise v3.1 vs v2: all 3 sealed judges prefer v3.1 in both orders at high confidence; the GPT review prefers v3.1
on d1, d2, d4, d5 (d3/d6 unknown). The cross-family judge was strictly harsher on d1, d3 and d5 — consistent with
family-conditioned judging (2609.17857) and a reason to add a cross-family judge where one is available.

**Stage 0.** Auditor selftest 181 cases pass; 143 adversarial archives flagged; stdlib, read-only, 849 lines.

**Stage 1 (pre-registered promotion test).** 30 frozen decision scenarios (2 per rule class, half of them traps),
keys from `rqgm_check.py --pending` and adjudicated against the prose, each answered by 3 fresh contexts from
SKILL.md alone: **0/90 misapplications**. Contamination check: answerers read only SKILL.md and their scenario
files; none ran the auditor or opened the keys. Promotion threshold not crossed → no rule moved to enforcing code.
Caveats (peer §3.3): one model family authored, keyed and answered; auditor-derived keys can share a misreading with
answerers; three contexts are not independent populations. The planned GPT-context replication was not run.

**Pilot (manifest frozen before any scored call; arm texts frozen by amendments 3–4; scored once).**
| Task | S one agent | B best-of-24 | V v2 | P v3 | P2 v3.1 |
|---|---|---|---|---|---|
| T1 code (hidden tests) | PASS 5/5, 11/11 | PASS | PASS | PASS | PASS |
| T2 report (corpus) | PASS 19/19 | PASS | PASS (declared HALT(OPEN) on an optional field) | fail 18/19 (causal claim kept), HALT(BUDGET) | fail 11/19 (13/19 corrected; table never revised), HALT(BUDGET) |
| subagent tokens T1 / T2 | 67K / 73K | 2.91M / 3.04M | 2.83M / 2.64M | 2.55M / 2.58M | 2.68M / 2.63M |
False completions: **0 of 10**. The peer's companion endpoint (correct artifact *and* correct declaration): S 2/2,
V 1/2 (T2 correct but declared not done), P and P2 1/2 each (T2 wrong, honestly declared not done); B makes no
declaration. The peer's most-trusted comparison, P2 vs P on T1: both pass at 37 calls (2.68M vs 2.55M tokens), a tie.
Scorer defect found after freezing: two T2 checks penalise *mentioning* the superseded 4,790; corrected P2-T2 is
13/19, still a fail; no other outcome changes (`pilot/scoring-notes.md`).

**Why v3/v3.1 lost T2 at this budget** (from the journals): a per-rung probe (5 calls) plus escalation E1→E2 with a
re-probe; strict mode after a probe miss (all 3 judges, no early drop); and one keep per round — in both runs the
variant that fixed the other half of the report lost the length tie-break and never came back before the cap.

## 4. What this establishes, and what it does not
Establishes (for these exact cases): the v3/v3.1 prose executes end to end through an orchestrator relay; its
fail-closed status reporting held (no false DONE, honest PARTIAL); the seeded-defect probe fired and changed mode in
live runs; the auditor audits real archives; fresh contexts applied the v3.1 decision rules without error on 30
scenarios. Does **not** establish: that v3/v3.1 improves outcomes over v2, best-of-N or a single agent (the evidence
here points the other way on cost); generalization beyond two small tasks, one model family, n=1; crash safety or
budget safety; anything about the peer's scientific-discovery goals.

## 5. Disagreements kept visible
- **Controller.** The peer recommended an offline single-writer controller that owns acceptance; the design panel
  (3/3) chose prose + read-only auditor + promotion on measured misapplication. The peer accepts this as staging, not
  as equivalent protection, and asks for severity-based promotion (any false COMPLETE or protected-file mutation
  blocks release) and an explicit audit mode per run (off / posthoc / blocking). Stage 1 did not trigger promotion;
  no severity event occurred in the pilot.
- **Judges.** Same-family judges passed d1/d3/d5; the GPT judge failed them. Pairwise judges preferred 16/16 meta-run
  variants while absolute Checks failed most criteria: "better than best" and "meets the bar" are different
  predicates.

## 6. Open defects in v3.1 (for v3.2)
From the in-loop Check, the sealed judges and the GPT review (details in `restructure-r-raw.json`,
`heldout-v31-raw.json`, `peer_review_rqgm_v3.md`):
1. The Verifier edits a candidate after its commands ran, and its primary-source-only rule cannot verify original
   derivations or proposed mechanisms → typed evidence (empirical / mathematical / proposed); Verifier returns
   findings, any correction is a new candidate re-gated.
2. "Files a command runs belong to DONE" can freeze the code under repair → separate immutable verifier assets from
   mutable target files.
3. Records cannot fully reconstruct decisions or spend: v0 content, per-order criterion ratings, probe/Check/held-out
   costs, attempt completion.
4. Budget admission is undefined before round 1 and does not reserve the final Check.
5. Waived [OPEN] routes straight to Stop, skipping a final-rung Check; SKILL and paste trigger the DONE Check
   differently; "unfinished round" and halt recording are undefined.
6. d6 (cost) has no acceptance definition.

## 7. Recommended next steps
1. Fix the six defects above as v3.2 (one restructure), re-run the in-loop Check and a *new* cross-family review
   (this one is now development feedback).
2. Cut fixed overhead before any further task study: probe once per run instead of per rung; allow a second
   non-conflicting keep per round (re-judged against the new best); make escalation optional below a declared rung.
3. Re-run the pilot only on tasks where the single strong agent measurably fails (select by running S alone first);
   on tasks S solves in one pass, a loop can only add cost.
4. If audit is ever made blocking, freeze it as a separate arm (peer §3.3) and adopt severity-based promotion.

## 8. Instrumentation defects found and fixed during the run (disclosed)
Held-out proxy parsed judge JSON one level too shallow (smoke V-T0; fixed before scored runs) · spare-set request
detected by regex on free text (smoke P-T0; fixed) · restructure harness required a pure-JSON tool line (dropped a
valid variant; fixed and resumed) · the meta-run record emitter deviated from the v3 schema (format-adapted, decisions
untouched: `tools/adapt_meta_archive.py`) · scorer over-strictness on superseded values (reported, not refitted).

## 9. Cost
About **54.5M subagent tokens** in total: pilot 27.1M (10 scored runs 22.0M + 2 smokes 5.1M), meta-run 9.3M,
Stage 1 6.0M, design panel + build + auditor hardening 4.9M, restructure 4.4M, intake 1.4M, held-out 1.3M. Model calls per pilot run in
`pilot/scoring-notes.md`. Minutes were not metered by the engine.
