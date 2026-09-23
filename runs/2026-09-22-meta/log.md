# RQGM meta-loop — the loop improves its own design + token efficiency

**Outcome: HALT(STALL) at epoch 19/20** (epochs 17–19 produced no winner). 16 variants applied
(`092f8ad` … `885ea01`). Held-out check: **3/3 fresh-persona judges prefer the final spec over v10
(`bded944`)** — 2 high, 1 medium confidence; all three rate v10 more compact (d6), the final wins d1–d4.

## Method (dynamic workflow)
- Research sweep: 4 lab/angle searchers + 1 arXiv verifier → 23 verified papers (`research.json`), 0 fabricated ids.
- Per epoch: 1 proposer → diff-only variants → leakage screen → 2 blind pairwise judges, order swapped
  (+ tiebreak on split) → apply winner only if majority prefers it, no d2 (guardrail) veto, caps hold.
- Controls: identity (baseline vs baseline) at e1, e6 → clean ties; placebo (meaning-preserving
  rewording) at e10 → tie/high ×2, so no change-favoritism was detected and strict mode stayed off.
- From e10 ("lean"): 2 variants/epoch, one agent at a time, early exit after a confident first judge,
  judges no longer shown the generator's rationale. Peak concurrency ~6 → 1.

## Applied changes (what the loop now does differently)
| e | change | criterion |
|---|---|---|
| 1 | G4 checks the accepted lineage; G3 also reverts unevidenced `[OPEN]` removals | d1 d2 |
| 2 | **Progress** = dS > δ *or* a confirmed newly passing criterion; stall/prune key on it | d4 (fixes last run's stall cause) |
| 3 | reuse step 4's re-score to confirm Progress | d3 |
| 4 | "Stalled" keyed on Progress | d1 d4 |
| 5 | ranked killers capped at `b_max` | d3 |
| 6 | calibrate once per rung; resume keeps it | d3 d1 |
| 7 | "bar is met" → "saturates" (defined term) | d1 |
| 8 | evaluators see only GROUNDING + rubric + vₙ | d3 d2 |
| 9 | generator sees only parent, GROUNDING, DONE, ledger, latest killers/fixes | d3 |
| 10 | a criterion-only Progress re-scores that criterion alone (not the full panel) | d3 |
| 11 | G4 compares version text, not scores | d4 d1 |
| 12 | stall exploration falls back to the least-recently-edited component (no deadlock) | d1 |
| 13 | screen rejects every edit → version rejected unscored | d3 |
| 14 | generator receives a ledger slice, not the whole ledger | d3 |
| 15 | evaluators get GROUNDING + rubric as a cached prefix | d3 |
| 16 | S* re-score only when S(vₙ) > S* | d3 d4 |

## Rejected / never passed (selected)
Relaxing dissent-gated escalation (screen: weakens human checkpoint, ×3) · dropping `> δ` from stall ·
literal-undo G4 (narrows coverage) · verify only screen-flagged claims (×3) · pre-score G6 · killer cap
tied to bₙ · E3 Pareto definition (screen) · scripted prune revert.

## Cost
Research 5 agents / 0.32M subagent tokens. Epochs 1–9: ~83 agents (plus 5 wasted re-runs: resuming the parallel run replayed agents out of
order, so finished epochs re-ran live; stopped and restarted sequentially). Lean epochs 9–19: 75 agents / 4.52M subagent tokens / 73 min. ~6.8 agents per lean epoch vs
~11 before.

## Open (for the human)
1. Held-out caveat: Progress's "newly passing criterion" branch is not explicitly limited to *accepted* versions.
2. SKILL.md is at 1000/1000 words — every further rule needs a cut (E3 compactness Pareto still undefined).
3. Pruning wording ("loses it (gated)") is vaguer than before; who produces the pruned version is implicit.
4. Held-out noise tolerance and the E3 objective remain human decisions (screen blocks any lowered bar).
