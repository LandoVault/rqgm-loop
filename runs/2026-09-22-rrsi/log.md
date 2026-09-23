# RQGM run 2026-09-22 — strengthen the RQGM loop with RRSI (arXiv:2609.24972)

**Outcome: HALT(STALL) at iteration 10 / 20, rung E1.** Current (accepted) version = v10 (`bded944`).

## Score trajectory (panel mean `overall`, 3 judges, 0–10)
| iter | version | S | decision |
|---|---|---|---|
| 1 | v1 | 5.33 (×2 calibration) | δ = 0.3 (floor), S* = 5.33 |
| 2 | v2 | 6.00 | accept, gain → S* 6.0 |
| 3 | v3 | 6.00 | accept (noise band, shrank) |
| 4 | v4 | 6.50 | accept, gain → S* 6.5 |
| 5 | v5 | 6.67 | accept (noise band, shrank) |
| 6 | v6 | 6.00 | **G1 reject** → restore v5, retry |
| 7 | v7 | 6.50 | G6 reject (noise band but grew) |
| 8 | v8 | 6.33 (2 runs avg) | G6 reject (ΔS < −δ) |
| 9 | v9 | 6.33 | G6 reject (ΔS < −δ) |
| 10 | v10 | 6.50 | accept (noise band, −1.3% size) → **HALT(STALL)** |

Leakage screen rejected 11 edits across the run (each restored before scoring), e.g. dropping
rubric-echo screening, dropping `[OPEN]` prune exemptions, S* allowed to decrease, a run-specific
"steps 0–7" exemption the generator itself wrote, and a lowered held-out bar.

## What RRSI contributed to the loop (now in SKILL.md / INITIATOR.md / README.md)
Annealed edit budget `bₙ` (cosine, rounded so it actually reaches 1) · one-component, hypothesis-tagged
edits + edit ledger · stall exploration of never-edited components · pre-scoring leakage screen ·
3× fresh-context noise calibration δ = clip(2·SD, 1/panel, 1.5) · G1 vs best-so-far − δ · G6 "gain pays
for growth" with a noise band (ΔC ≤ 0) · pruning of loop-added text (DONE/`[OPEN]` exempt) · HALT(STALL) ·
human-supplied, sealed, single-use held-out judge with `heldout{attempt}` log · score→pass rule (≥7,
strict majority) · schema records calib/screen/citation/halt/heldout · adaptations labeled vs RRSI.

## Open (surfaced, not fixed — criteria c5, c7, c12 still fail by majority at E1)
1. Scalar `overall` gate hides per-criterion progress (methods-expert) — the cause of this stall.
   v9's criterion-pass gain event was tried; needs a numeric ΔS rule (operator/methods).
2. Held-out noise tolerance: critics want it, the screen rejects any lowered bar → **human decision**.
3. Bundle attribution: RRSI-faithful shared dS (free-rider risk) vs `dS=null` (prunes real gains) —
   evaluators split; candidate fix: leave-one-out re-score.
4. Unaccepted but screen-clean improvements in v7–v9 (G3 `[OPEN]`-removal guard, G4 on accepted states,
   anti-sawtooth G6 vs S*, symmetric re-score, dissent definition, E3 dominance rule) — see those commits.
5. The 1000/1300/1150-word caps bind every iteration (E3 compactness-vs-rigor Pareto, never reached).
6. Parent reference for iters 6–10 was v5's single draw 6.67 (winner's curse the critics describe).
