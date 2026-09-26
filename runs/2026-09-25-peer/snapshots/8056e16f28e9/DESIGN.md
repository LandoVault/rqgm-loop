# RQGM Loop — design from first principles

Any loop that improves an artifact by asking LLMs "is this better?" has to solve the same ten
problems. For each one the loop keeps **one mechanism**, chosen because there is evidence it helps.
A mechanism with no evidence, or one that made things worse in our own runs, is left out.

Evidence comes in two kinds:
- **[own]** — observed in this repo's own runs (`runs/`). Each is one run, so it is observational, not
  proof.
- **[paper]** — a verified abstract (`runs/2026-09-22-meta/research.json`), or the primary PDF read
  during the runs (RQGM, RRSI: `runs/2026-09-22-rrsi/grounding.md`). Industry write-ups are named.

## The ten problems → the mechanism kept

| # | Problem | Mechanism | Evidence |
|---|---|---|---|
| 1 | **Objective.** "Better" drifts unless it is written down, and some criteria can be tested exactly. | `DONE`: atomic, non-overlapping pass/fail criteria, each naming its **check**. A command or test when it can be checked mechanically; its result overrides judges. Otherwise judges. Plus must-not-change constraints and the final rung. The loop never edits `DONE` or the rubric. | Anthropic *Effective harnesses*: a structured success spec, and don't edit the tests. [paper] 2602.05125: decomposing and de-duplicating rubrics raises judge accuracy. 2606.09498: validating edits with regression tests. |
| 2 | **Independence.** A reviewer is lenient toward work like its own. | Separate roles: generator, screen, verifier, judges, held-out judges. The writer never judges. Judges come from a different model family where available. | [paper] RQGM 2606.26294: a baseline reviewer over-accepts AI-generated papers at up to 1.91× the human rate. 2603.00077: verdicts differ across judge families. |
| 3 | **Signal quality.** One absolute LLM score is noisy and hides per-criterion progress, and pairwise judges have an order bias. | **Pairwise** blind comparison with the current best, verdicts per criterion, cosmetic = tie. The first judge compares in both orders, and verdicts that disagree count as a tie. A one-time bias probe (identity + meaning-preserving rewording) switches on strict mode if judges don't tie. | [own] Run 1, absolute 0–10 scores: re-scoring one version shifted the panel mean by 0.33, and single judges moved 1 point. The scalar gate stalled at iteration 10. [own] Meta-run, pairwise: identity controls tied 4/4 and the placebo tied 2/2. [paper] 2506.03785 pairwise knockout; 2602.13110 bidirectional pairwise with abstention; 2509.20293 aggregate scores hide per-criterion signal; 2609.02942 rubric artifacts call for probes. |
| 4 | **Goodhart.** The generator optimizes whatever the judge rewards. | A **screen** that sees the rubric reads every diff *before* judging. It rejects rubric echo, compliance claims with no mechanism, judge-targeting, inert text, and guardrail weakening. Judges never see the generator's rationale. | [own] The screen rejected 11 edits in run 1 and 15 of 47 variants in the meta-run, including an exemption the generator wrote for its own run. [paper] RRSI 2609.24972: a pre-evaluation leakage critic, and acceptance regularizers matter most (Table 2). 2605.21384: reward hacking in coding agents. |
| 5 | **Truth.** The generator can invent facts. | The **Verifier** checks v0's claims and every new number or claim against a primary source, or strips it, or marks it `[OPEN]`. No fabricated substrates. Removing an `[OPEN]` needs evidence, and any open gap blocks Stop. | [own] Critics' readings of RRSI Table 5 conflicted, and several were wrong when checked against the PDF. Verification kept every unverified reading out of the artifact. Cursor: audit before trusting a score. |
| 6 | **Search.** Bundled edits can't be credited, and failures repeat. | 2 single-change variants per round, each one change to one section, with a hypothesis naming its criterion. A **ledger** blocks ideas rejected by ≥2 judges. After 2 empty rounds, target the least-recently-changed section. `GROUNDING` may carry 1–2 exemplars. | [paper] RRSI §3.2 proposal regularizers: an edit budget and evidence-aware credit assignment; removing them lowered OOD (Table 2). 2507.19457 GEPA: complementary variants; 2604.25850: revertible, prediction-tagged edits; 2605.24539: exemplars help under sparse feedback. [own] Meta-run: 26 of 32 judged single-change variants won and 16 were applied. |
| 7 | **Selection.** Keep only real, non-regressing gains, without bloat. | Keep a variant if ≥2 judges prefer it, none prefers the best, and nothing **protected** is rated worse. Protected: guardrails, must-not-change constraints, criteria already passing. A shorter variant no judge rates worse is also kept, so neutral deletions prune for free. More judges run only when earlier ones are unsure. A kept version that (nearly) restores an earlier best halts for the human to pick (HALT(OSCILLATION)). | [paper] RRSI: non-compensatory, complexity-aware acceptance (the unregularized run cost 3.80M vs 2.42M tokens per trial, Table 2). 2604.13717 and 2602.13110: escalate only uncertain judgments. |
| 8 | **Generalization.** The loop overfits its own judges. | The bar rises through cumulative rungs (E1 fair → E2 adversarial → E3 a human-written second criterion), only with the human. A final **held-out check** by 3 human-written judges the loop never saw, using the same pass/fail check decided by majority. | [paper] RQGM: evolving evaluators. RRSI: held-out/OOD evaluation. 2607.12227: evolved gains often don't generalize and must be compared at matched budget. [own] Meta-run: 3/3 held-out judges preferred the result in a *pairwise* comparison. The majority pass/fail check specified here has not yet been run. |
| 9 | **Stopping and ownership.** Loops burn budget on plateaus, and only a human can supply real data or change the goal. | Check on a stall (3 rounds with nothing kept) or on a claim of done. Each HALT (STALL, OPEN, OSCILLATION, OVERFIT, BUDGET) names what only the human can supply. The human decides every escalation and closes every `[OPEN]`. A global budget. | [paper] 2606.27009: early stopping on a plateau cut loop tokens by 38%. [own] Run 1 and the meta-run both ended cleanly on a stall, with the remaining gaps listed. |
| 10 | **State and cost.** Long runs crash, and context is the main cost. | Append-only `MEMORY`, every version revertible, resume from the last kept version and probe mode. Each role sees only what it needs; judges get `GROUNDING` and the rubric as a cached prefix; one judge first, more only if needed. | [own] Lean meta-run: about 6.8 agents per round vs about 11. [own] Resuming the parallel meta-run replayed agents out of order and re-ran finished ones (5 wasted, `runs/2026-09-22-meta/log.md`), so running one agent at a time in a fixed order is recommended when CPU or resume matters. |

## What was removed, and why

| Removed | Why |
|---|---|
| Absolute 0–10 scalar gate, δ calibration, `S*`, noise band | Noise as large as the gains, and it stalled run 1 (problem 3). Pairwise comparison against the best replaces all four. |
| β₀/β₁ growth formula, prune windows, `dS` attribution | "A tie goes to the shorter version" plus single-change variants keep the intent with no parameters. |
| Cosine edit budget, bundles | Bundles made credit impossible, and critics fought over it for four iterations. One change per variant is the edit-budget regularizer at its most restrictive. |
| Gates G1–G6 as a list | G1 (no regression) follows from comparing against the best: every kept version beat the previous best, so no separate regression counter is needed. G2 became "cosmetic = tie". G3 and G5 are invariants. G6 is the tie-to-shorter rule. G4 is kept as HALT(OSCILLATION) when a kept version (nearly) restores an earlier best. |
| Dissent thresholds, "killers" as the escalation trigger, E3 as a vague "Pareto" | Lenient judges produce no dissent, so a dissent trigger would stop at the weakest rung. Escalation is now the human's decision at every rung below the final one (the human checkpoint is kept; only the dissent precondition goes), and E3 is a written criterion. |
| E4 "red team re-verifies every number" | Every claim, including v0's, is verified when it enters. |
| Re-offering losing winners | The ledger already lets the generator re-propose anything not rejected. |

## Invariants (never traded for score)

The writer never judges. Nothing unverified counts as fact. `DONE` and the rubric are never edited to
pass. A change is kept only if independent judges prefer it and nothing protected gets worse.
Mechanical checks beat opinions. The bar only rises, and only with the human. The final check uses
judges the loop never saw.

## Not yet proven

- The meta-run showed the *redesign process* works. It did not compare this loop with a
  matched-budget baseline, such as the same token spend on plain best-of-N rewriting (2607.12227).
  That is the test to run before claiming the loop beats simpler alternatives on a given artifact.
- The held-out majority check, bias probe and mechanical-check override are specified from evidence
  but have not yet been exercised end-to-end in a logged run.
