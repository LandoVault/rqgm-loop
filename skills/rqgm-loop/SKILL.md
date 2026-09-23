---
name: rqgm-loop
description: >-
  Co-evolve an artifact against separate, adversarial, evolving evaluators to a defined bar (Red
  Queen Gödel Machine loop). Use to "run the RQGM loop", red-team and iterate,
  or harden / pressure-test a proposal, paper, spec, design, or codebase until it's fundable,
  defensible, correct, or publishable.
---

# RQGM Loop

Run a Red Queen Gödel Machine loop (Iacob et al., arXiv:2606.26294): co-evolve a **generator** against
**separate, adversarial, evolving** evaluators. Static reviewers — and a model grading its own output —
over-accept polished work, so a *different* agent judges, *stricter every epoch*, surfacing real
weaknesses and **the gaps only the human can close**. Re-facing one panel invites overfitting,
noise-chasing and bloat, so the loop is **regularized** after RRSI (Xia et al., arXiv:2609.24972).

## When invoked

1. **Collect the six slots** (ask only for what's missing): `TARGET` — the artifact · `GROUNDING` —
   sources of truth · `DONE` — machine-verifiable pass/fail criteria as JSON + must-not-change
   constraints + a hard stop (propose + confirm if missing) · `EVALUATORS` — 2–5 critic personas,
   each a **separate subagent**, plus **1 held-out judge** held by the human, unseen by the
   generator · `MEMORY` — append-only `archive.jsonl` · `BUDGET` — `MAX_ITERS` (= N) + token/time caps.
2. **Run THE LOOP**, persisting to `MEMORY` (+ a readable log) each iteration; evaluators and
   verifiers are subagents (else fresh-context passes), never the writer.

**Units.** Scores: 0–10 per criterion plus `overall`; `S(v)` = panel mean `overall`; a judge
passes a criterion at ≥7, the panel on a strict majority (ties fail). `C(v)` = word count of `TARGET`
(tokens for code). A **component** = a top-level section or file, fixed at setup (checker-approved). Epoch = rung;
iteration = generate→gate cycle. Defaults: `b_max=3`, `w=3`, `β₀=2%`, `β₁=5%`/point, `δ_min` = 1/panel size, `δ_max=1.5`.

## THE LOOP

- **0 · Setup.** Read `MEMORY`; resume if any (drop a torn last record), else
  read `GROUNDING` first, draft **v0**, write `DONE` (each `pass:false`), list components, set rung
  **E1**. **Calibrate:** the panel scores the unchanged version 3× in fresh contexts;
  `δ = clip(2·SD, δ_min, δ_max)`, `S*` = mean; redo per rung.
- **1 · Generate.** Revise **vₙ** (n = 1…N, not reset per rung) with at most
  `bₙ = 1 + round_half_up((b_max−1)·½(1+cos(π·n/N)))` edits — bundled early, single late (attributable). One edit = one component + a one-line falsifiable hypothesis; smallest reviewable
  diff; version it. Skip hypotheses the ledger rejected on single-edit iterations absent new
  evidence. **Stalled** (no gain) → one of the `bₙ` edits goes to a never-edited (else
  least-recently-edited) component.
  Never edit `DONE`/the rubric to pass; never fabricate a substrate (data, people, results,
  agreements) — mark gaps `[OPEN]`.
- **2 · Evaluate.** A **leakage screen** (checker ≠ generator) reads the diff *before* scoring and
  rejects edits that echo rubric wording, assert compliance without adding mechanism, or target a
  named evaluator.
  Then each evaluator scores vₙ on the rung's rubric (not format/length/tone): scores + ranked
  killers + required fixes tagged to claims.
- **3 · Verify.** Any new number/claim lacking a `citation` record → BLOCK until verified against
  primary sources.
- **4 · Gates.** Scores that would raise `S*` or trip G1 get one averaged re-score. With
  `ΔS = S(vₙ) − S(parent)`, `ΔC` = relative change in `C`:
  `G1` reject, restore best, retry once if `S(vₙ) < S* − δ` (2nd fail → HALT REGRESSION) · `G2` discard
  purely-presentational wins · `G3` revert score gained on an unevidenced substrate → `[OPEN]`, or any
  `[OPEN]` dropped without an evidenced `substrate` close · `G4` HALT if accepted vₙ ≈ vₙ₋₂ · `G5` HALT past `BUDGET`, emit best-so-far ·
  `G6` if `ΔS > δ` require `ΔC ≤ β₀ + β₁·ΔS`; if `|ΔS| ≤ δ` (noise) require `ΔC ≤ 0` (or `ΔC ≤ β₀`,
  once per component, for a single edit on a never-edited one); else reject, restore parent.
  On accept, `S* = max(S*, S(vₙ))`. **Gain** = `S*` up > δ over the last `w` iterations.
- **5 · Record & repeat.** Log each edit (bundles share the version's `dS`). **Prune** only text the loop added: if a component's accepted edits in the
  last `2w` iterations all had `dS ≤ δ`, their text is deleted (a gated edit) unless the checker upholds
  keeping it; `DONE` must-not-change items and `[OPEN]` markers are exempt.
  The rung **saturates** when all rung criteria pass; `S*` flat (no gain) over `2w` iterations → HALT(STALL).
- **6 · Boundary.** Advance a rung only if the bar is met **and** ≥1 evaluator still dissents;
  **pause for human confirmation** (escalation redefines success). Rungs:
  E1 fair-critical → E2 adversarial/equal-stringency (reject polish, demand derivations) →
  E3 2nd objective (Pareto) → E4 red-team re-verifies every cited number.
- **7 · Stop.** STOP only when `DONE` passes under the escalated utility, no `[OPEN]` substrate
  remains, and the **held-out judge** — run by the human or a subagent on a prompt the generator never
  reads, once, on the final rung — passes every criterion. A fail (panel overfit) →
  record it in a sealed file outside `MEMORY`, reopen only that criterion ID (no critique text) with a
  fresh held-out judge; a 2nd fail → HALT(OVERFIT). Or STOP on any HALT. Output: version, provenanced critiques, archive/log, one next action (on HALT: reason + what the
  human must add).

## Stance
Tight leash, small verifiable diffs; a separate, dissenting checker; engineer context, don't wordsmith; ties go to
the simpler version; a 90%-good draft is not done.

## Memory schema (`archive.jsonl`, append-only, single-writer)
`version` · `utility{rung,delta,s_star,s_star_version}` · `calib{runs,sd}` ·
`eval{version,evaluator,scores,critiques}` · `edit{version,component,hypothesis,dS,dC,accepted,rejected_by}`
· `screen{edit,verdict,reason}` · `citation{claim,source,status}` · `decision` · `halt{reason}` ·
`substrate{gap,owner,status}`. Resume = last version, utility, ledger, open substrates, Pareto front.

## Notes
- Highest-value: **evolving the evaluator**; the **substrate firewall** (surface, never fake).
- From RRSI: step 1's budget/ledger/stall, step 2's screen, G1, G6, pruning. **Adapted**: panel =
  evolve set; held-out judge ≈ OOD test (a judge shift); checker ≠ generator; screen targets;
  falsifiable hypotheses; stall fallback; per-rung δ; re-scoring; noise band (ν → never-edited
  allowance); `C` = size; `bₙ` rounding; prune scope/window; numeric defaults.
- Also: maker–checker, structured `DONE` (Anthropic); audit-before-trust (Cursor).
