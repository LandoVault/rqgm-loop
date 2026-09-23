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
2. **Run THE LOOP**, persisting to `MEMORY` (+ a log) each iteration; evaluators and
   verifiers are subagents (else fresh-context passes), never the writer.

**Units.** Scores: 0–10 per criterion plus `overall`; `S(v)` = panel mean `overall`; a judge
passes a criterion at ≥7, the panel on a strict majority (ties fail). `C(v)` = word count of `TARGET`
(tokens for code). A **component** = a top-level section or file, fixed at setup (checker-approved). Epoch = rung;
iteration = generate→gate cycle. Defaults: `b_max=3`, `w=3`, `β₀=2%`, `β₁=5%`/point, `δ_min` = 1/panel size, `δ_max=1.5`.

## THE LOOP

- **0 · Setup.** Read `MEMORY`; resume if any (drop a torn last record), else
  read `GROUNDING` first, draft **v0**, write `DONE` (each `pass:false`), list components, set rung
  **E1**. **Calibrate** once per rung (resume keeps it): the panel scores the unchanged version 3× in fresh contexts;
  `δ = clip(2·SD, δ_min, δ_max)`, `S*` = mean.
- **1 · Generate.** Revise **vₙ** (n = 1…N across rungs), seeing only parent, `GROUNDING`, `DONE`, ledger, latest killers/fixes, with at most
  `bₙ = 1 + round_half_up((b_max−1)·½(1+cos(π·n/N)))` edits. One edit = one component + one-line falsifiable hypothesis; smallest reviewable
  diff; version it. Skip hypotheses the ledger rejected on single-edit iterations absent new
  evidence. **Stalled** (`w` iterations without Progress, step 5) → ≥1 edit on the least-recently-edited component.
  Never edit `DONE`/the rubric to pass; never fabricate a substrate (data, people, results,
  agreements) — mark gaps `[OPEN]`.
- **2 · Evaluate.** A **leakage screen** (checker ≠ generator) reads the diff *before* scoring and
  rejects edits that echo rubric wording, assert compliance without mechanism, or target
  named evaluators (none survive → reject unscored).
  Each evaluator, seeing only vₙ, `GROUNDING` and the rung's rubric, scores it (not format/length/tone): scores, ranked
  killers (≤`b_max`), claim-tagged fixes.
- **3 · Verify.** Any new number/claim lacking a `citation` record → BLOCK until verified against
  primary sources.
- **4 · Gates.** `ΔS = S(vₙ) − S(parent)`; `ΔC` = relative `C` change:
  `G1` reject, restore best, retry once if `S(vₙ) < S* − δ` (2nd fail → HALT REGRESSION) · `G2` discard
  presentational wins · `G3` revert unevidenced substrate score gains and unevidenced `[OPEN]` removals → `[OPEN]` ·
  `G4` HALT on oscillation (accepted vₙ's text ≈ accepted grandparent's, not scores) · `G5` HALT past `BUDGET`, emit best-so-far ·
  `G6` if `ΔS > δ` require `ΔC ≤ β₀ + β₁·ΔS`; if `|ΔS| ≤ δ` (noise) require `ΔC ≤ 0` (or `ΔC ≤ β₀`,
  once per component, for a single edit on a never-edited one); else reject, restore parent.
  Only on an accept with `ΔS > δ`: `S* = max(S*, mean(S(vₙ), fresh re-score))`.
- **5 · Record & repeat.** Log each edit (bundles share `dS`). **Progress**: an accept with `dS > δ` or a
  newly passing criterion (step 4's re-score confirms; else re-score that criterion alone), none lost (adapted from arXiv:2509.20293, 2602.15481).
  **Prune** loop-added text only: a component whose last-`2w` accepted edits all lacked Progress loses
  it (gated) unless checker-upheld; `DONE` constraints and `[OPEN]` markers exempt.
  The rung **saturates** when all rung criteria pass; `2w` iterations without Progress → HALT(STALL).
- **6 · Boundary.** A judge **dissents** if it scores any criterion < 7. Advance a rung only if it
  saturates (step 5) **and** ≥1 judge dissents (none → the human may skip rungs); **pause for human
  confirmation** (escalation redefines success). Rungs (cumulative):
  E1 fair-critical → E2 adversarial/equal-stringency (reject polish, demand derivations) →
  E3 2nd objective (Pareto) → E4 red-team re-verifies every cited number.
- **7 · Stop.** STOP only when `DONE` passes under the escalated utility, no `[OPEN]` substrate
  remains, and the **held-out judge** — a prompt file the human supplies and the generator never
  opens, run once on the final rung — passes every criterion. A fail (panel overfit) →
  seal its critique outside `MEMORY` (log only `heldout{attempt}`), reopen only that criterion ID with
  a fresh human-written judge; a 2nd fail → HALT(OVERFIT). Or STOP on any HALT. Output: version,
  provenanced critiques, archive/log, one next action (on HALT: reason + what the human must supply).

## Stance
Tight leash, small verifiable diffs; a separate, dissenting checker; engineer context, don't wordsmith; ties go to
the simpler version; a 90%-good draft is not done.

## Memory schema (`archive.jsonl`, append-only, single-writer)
`version` · `utility{rung,delta,s_star,s_star_version}` · `calib{runs,sd}` ·
`eval{version,evaluator,scores,critiques}` · `edit{version,component,hypothesis,dS,dC,accepted,rejected_by}`
· `screen{edit,verdict,reason}` · `citation{claim,source,status}` · `decision` · `halt{reason}` ·
`heldout{attempt}` · `substrate{gap,owner,status}`. Resume = last version, utility, ledger, open substrates, Pareto front.

## Notes
- Highest-value moves: **evolving the evaluator**; the **substrate firewall** (surface, never fake).
- From RRSI: step 1's budget/ledger/stall, step 2's screen, G1, G6, pruning. **Adapted**: panel =
  evolve set; held-out judge ≈ held-out split (a judge shift); checker ≠ generator;
  screen targets; per-rung δ; `S*` re-score; noise band (ν → never-edited allowance); `C` = size;
  `bₙ` rounding; prune threshold/window; numeric defaults.
- Also: maker–checker, structured `DONE` (Anthropic, *Effective harnesses*); audit-before-trust
  (Cursor).
