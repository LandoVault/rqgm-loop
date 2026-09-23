# RQGM Loop — design from first principles

Any loop that improves an artifact by asking LLMs "is this better?" has to solve the same ten
problems. For each one the loop keeps exactly **one mechanism**, chosen because there is evidence it
helps. A mechanism that has no evidence, or that made things worse in our own runs, is left out.

Evidence comes in two kinds. **[own]** means observed in this repo's own runs (`runs/`): one run each,
so treat it as observational. **[paper]** means verified arXiv abstracts (`runs/2026-09-22-meta/research.json`).

## The ten problems → the mechanism kept

| # | Problem | Mechanism | Evidence |
|---|---|---|---|
| 1 | **Objective.** "Better" drifts unless it is written down. | `DONE`: atomic, non-overlapping pass/fail criteria, plus must-not-change constraints, plus a hard stop. The loop may never edit `DONE` or the rubric to pass. | Anthropic *Effective harnesses* (structured success spec). [paper] 2602.05125: decomposing and de-duplicating rubrics improves judge accuracy. |
| 2 | **Independence.** A writer grading itself is too lenient. | Separate roles: generator, screen, verifier, judges, held-out judges. The writer never judges. | [paper] RQGM 2606.26294: a baseline reviewer over-accepts AI-generated papers at up to 1.91× the human rate. |
| 3 | **Signal quality.** One absolute LLM score is noisy and hides per-criterion progress. | **Pairwise** blind comparison against the current best: order swapped, per-criterion verdicts, cosmetic changes count as a tie. A bias probe (identity + placebo) runs once. | [own] Run 1, absolute 0–10 scoring: re-scoring the same version shifted the panel mean by 0.33, and single judges moved 1 point. The scalar gate stalled at iteration 10 while criteria kept flipping. [own] Meta-run, pairwise: identity controls tied 4/4 and the placebo tied 2/2. [paper] 2506.03785 pairwise knockout; 2509.20293 aggregate scores hide per-criterion signal; 2609.02942 rubric artifacts need probes. |
| 4 | **Goodhart.** The generator optimizes whatever the judge rewards. | A **screen** reads every diff *before* judging. It rejects rubric echo, compliance claims with no mechanism, judge-targeting, inert text, and guardrail weakening. Judges never see the generator's rationale. | [own] The screen rejected 11 edits in run 1 and 15 of 47 variants in the meta-run, including an exemption the generator wrote for its own run. [paper] RRSI 2609.24972: a pre-evaluation leakage critic, and acceptance regularizers matter most (Table 2). 2605.21384: reward hacking. |
| 5 | **Truth.** The generator can invent facts. | **Verify** every new number or claim against a primary source, or strip it, or mark it `[OPEN]`. Never fabricate a substrate. Removing an `[OPEN]` marker needs evidence. | [own] Critics' readings of RRSI Table 5 conflicted, and several were wrong when checked against the PDF. Verification kept every unverified reading out of the artifact. Cursor: audit before trusting a score. |
| 6 | **Search.** Big bundled edits can't be credited, and failures repeat. | Each round proposes K single-change variants, each one change to one section, with a one-line hypothesis naming a `DONE` criterion. A **ledger** blocks re-proposing rejected ideas. On a stall, target the least-recently-changed section. | [paper] RRSI proposal regularizers (edit budget, evidence-aware credit; removing them costs OOD); 2507.19457 GEPA: complementary variants, reflection; 2604.25850: revertible, prediction-tagged edits. [own] Meta-run: 26 of 32 judged single-change variants won and 16 were applied. |
| 7 | **Selection.** Keep only real, non-regressing gains, without bloat. | Keep a variant if a majority of judges prefer it and no judge rates a **protected** item worse. Protected items are guardrails, must-not-change constraints, and criteria already passing. Ties go to the shorter version, so a neutral deletion is kept, which means pruning comes free. Reverting a kept change needs all judges. | [paper] RRSI: non-compensatory, complexity-aware acceptance (the unregularized run cost 3.80M tokens per trial vs 2.42M). 2602.13110 / 2604.13717: escalate to more judges only when uncertain. |
| 8 | **Generalization.** The loop overfits its own judges. | The **bar rises**: rungs E1→E4, changed only with the human. At the end, a **held-out** check by human-written judges the loop never saw, deciding each criterion by majority. | [paper] RQGM: evolving evaluators. RRSI: held-out/OOD evaluation. 2607.12227: evolved gains often fail to generalize. [own] Held-out judges preferred the meta-run result 3/3. |
| 9 | **Stopping and ownership.** Loops burn budget on plateaus, and only a human can supply real data or change the goal. | Stop on DONE (plus held-out), **stall** (w rounds with nothing kept), or budget. The human confirms every escalation, names the E3 objective, and supplies every `[OPEN]` substrate. | [paper] 2606.27009: early stopping on plateau cut loop tokens by 38%. 2606.23075: bound per-step evaluator change. [own] Run 1 and the meta-run both ended cleanly on a stall. |
| 10 | **State and cost.** Long runs crash, and context is the main cost. | Append-only `MEMORY`, every version revertible, resume from the last kept version. Each role sees only what it needs; judges get `GROUNDING` and the rubric as a cached prefix; one judge first, more only if needed. | [own] Lean meta-run: about 6.8 agents per round vs about 11. Order-stable sequential runs resume deterministically, while a parallel replay broke. [paper] 2604.23472: reuse existing scores. |

## What was removed, and why

| Removed | Why |
|---|---|
| Absolute 0–10 scalar gate, δ calibration, `S*`, noise band | Noise of the same size as the gains, and it stalled run 1 (problem 3). Pairwise comparison against the best replaces all four. |
| β₀/β₁ growth formula, prune windows, `dS` attribution | Replaced by "ties → shorter" and single-change variants: same intent, no parameters to tune. |
| Cosine edit budget, bundles | Bundles made credit impossible and the critics fought over it for four iterations. Single-change variants are the edit-budget regularizer at its most restrictive. |
| Gates G1–G6 as a list | G1 and G4 follow from "compare against best" plus the ledger. G2 became "cosmetic = tie". G3, G5 and G6 became invariants and the selection rule. |
| Dissent thresholds, "E3 Pareto" | Escalation is a human decision at the checkpoint. The E3 objective, once named, becomes a protected criterion. |

## Invariants (never traded for score)

The writer never judges. Nothing unverified counts as fact. `DONE` and the rubric are never edited to
pass. A change is kept only if independent judges prefer it and nothing protected gets worse. The bar
only rises, and only with the human. The final check uses judges the loop never saw.
