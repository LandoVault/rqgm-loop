# Grounding for this run

Primary sources (evaluators may fetch and must verify against these):
- RRSI — Xia, Han, Wang, ... Pfister, Lee. "RRSI: Regularized Recursive Self-Improvement of Agent Harnesses", arXiv:2609.24972 (submitted 2026-09-21). https://arxiv.org/abs/2609.24972 · HTML: https://arxiv.org/html/2609.24972
- RQGM — Iacob et al., "The Red Queen Gödel Machine: Co-Evolving Agents and Their Evaluators", arXiv:2606.26294. https://arxiv.org/abs/2606.26294

## RRSI extraction (generator's notes; verify, do not trust)
Failure modes of unregularized RSI (Sec. 1): benchmark-specific fitting; noise chasing; complexity accumulation — caused by adaptive reuse of a finite evolve set.
Proposer (Sec. 3.2):
- Annealed edit budget (L0-style), Eq. 4: b_t = ceil(b_min + (b_max - b_min) * 1/2 (1 + cos(pi t / T))); ||z_t||_0 <= b_t (Eq. 9) — bounds # independently attributable edits bundled per candidate.
- Evidence-aware credit assignment: edit history L_t = {(round, component, hypothesis, diff, dS, dC, accepted)} (Eq. 10) — avoid retesting falsified hypotheses.
- Structured exploration: stall indicator sigma_t = 1[S_t - S_{t-w} <= delta]; U_t = unexplored components; part of proposal budget reserved for U_t; does not restrict which components may eventually be modified.
Selector (Sec. 3.3):
- Leakage screening: critic reads diffs BEFORE evaluation; rejects edits encoding task names, entity names, task-specific values, answers, benchmark-specific logic, or inert machinery.
- Stability-aware acceptance, Eq. 5: S(H') >= S* - delta, S* = best so far, delta calibrated from repeated evals of the unchanged base harness.
- Complexity-aware (ridge/L2) acceptance, Eq. 7: for dS > delta, require dC <= beta0 + beta1 * dS (dC = relative policy-token cost change).
- Lasso/L1 structural pruning: components exercised with gain <= 0 over a pruning window -> deletion list handed to proposer.
- No held-out split used during evolution; frozen final harness evaluated on ID held-out + OOD; hyperparameters chosen on evolve env only.
Results: Table 2 ablation (agentic workspace): unregularized 92.8 evolve / 40.3 OOD / 3.80M tok; RRSI 90.5 / 43.6 / 2.42M; acceptance regularizers matter most. Abstract: up to +14.1 ID, +4.7 OOD, ~30% fewer tokens.
Limitations: frozen backbones; finite evolve set; hyperparameter sensitivity; broader validation needed.

## Mapping to RQGM loop (generator's hypotheses)
evolve set <-> the fixed evaluator panel (the generator adaptively reuses the same judges every iteration, so it can overfit them); OOD <-> a held-out evaluator. This mapping is an ADAPTATION, not a claim of the RRSI paper.
