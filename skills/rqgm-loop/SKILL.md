---
name: rqgm-loop
description: >-
  Co-evolve an artifact against separate, adversarial, evolving evaluators to drive it to a defined
  bar — a generator-vs-critics improvement loop with guardrails (Red Queen Gödel Machine). Use when
  the user wants to "run the RQGM loop", red-team and iterate, or "harden / pressure-test this
  proposal, paper, spec, design, or codebase until it's fundable, defensible, correct, or
  publishable" — i.e. when the work needs honest, escalating critique and real gaps surfaced rather
  than polished prose.
---

# RQGM Loop

Run a Red Queen Gödel Machine loop (Iacob et al., arXiv:2606.26294): co-evolve a **generator** against
**separate, adversarial, evolving** evaluators. Static reviewers — and a model grading its own output —
over-accept polished work; this skill uses a *different* agent to judge, and makes that judge *stricter
every epoch*, so it drives out real weaknesses and **surfaces the gaps only the human can close**.
Because the generator re-faces the same panel every iteration, it can also *overfit that panel*, chase
score noise, and bloat the artifact; the generator and gates are therefore **regularized** following
RRSI (Xia et al., arXiv:2609.24972), adapted here from harness benchmarks to evaluator panels.

## When invoked

1. **Collect the six slots** from the request and context (ask only for what's missing):
   - `TARGET` — the artifact to optimize · `GROUNDING` — sources of truth the agents may read ·
     `DONE` — a machine-verifiable success spec (pass/fail criteria as JSON + constraints that must not
     change + a hard stop) · `EVALUATORS` — 2–5 critic personas, each run as a **separate subagent**,
     plus **1 held-out evaluator** whose persona and output the generator never sees before Stop ·
     `MEMORY` — a file for the append-only `archive.jsonl` · `BUDGET` — MAX_EPOCHS (= N, total
     iterations) + token/wall-clock caps.
   - If the user hasn't defined `DONE`, propose a concrete checkable spec and confirm it before starting.
2. **Run THE LOOP** below, spawning the evaluators (and any verification/research help) as subagents so
   the checker is never the writer. *Requires a host that can spawn subagents (e.g. a Task/Agent tool);
   if none is available, run each evaluator as a separate, fresh-context pass.*
3. **Persist** state to `MEMORY` after every iteration; mirror a human-readable log.
4. **Stop** at `DONE` (under the escalated utility, no open substrates, held-out check passed) or on any
   HALT, and report.

**Score scale.** Every evaluator scores each criterion and `overall` on 0–10; `S(v)` = panel mean
`overall`. Defaults (override in `BUDGET`): `b_max=3`, `w=3`, `β₀=2%`, `β₁=5%` per point, `δ_min=0.3`.

## THE LOOP

- **0 · Setup.** Read `MEMORY`; resume if state exists (torn last record → discard, use prior), else
  read `GROUNDING` first, draft **v0**, write `DONE` as JSON criteria (each `pass:false`), set rung
  **E1**. **Calibrate noise:** score the unchanged current version twice with the panel;
  `δ = max(δ_min, |S₁ − S₂|)`; `S*` = their mean. Recalibrate δ and reset `S*` at every rung change.
- **1 · Generate.** Revise **vₙ** with at most `bₙ = ⌈1 + (b_max − 1)·½(1 + cos(π·n/N))⌉` edits —
  bundled early for coordinated fixes, one at a time late so gains are attributable. Each edit names
  its component and a one-line falsifiable hypothesis ("fixes critique X"). Read the edit ledger first:
  don't retry a hypothesis already rejected on that component without new evidence. **Stalled** (no
  gain > δ over the last `w` iterations) → spend ≥1 edit on a never-edited component. Never edit
  `DONE`/the rubric to pass; never fabricate a substrate (real data, people, results, agreements) —
  mark gaps `[OPEN]`.
- **2 · Evaluate.** First a **leakage screen**: a checker (≠ generator) reads the diff *before*
  scoring and rejects edits that echo an evaluator's rubric wording, target a named evaluator, or add
  inert text (claims compliance without doing it). Then each evaluator subagent (≠ generator) scores
  vₙ on the current rung's rubric (excluding formatting/length/tone) and returns scores + ranked
  killers + required fixes, tagged to claims.
- **3 · Verify.** Any new number/claim lacking a citation event → BLOCK and verify against primary
  sources before trusting the score (assume the generator will exploit any gap the rubric leaves).
- **4 · Gates.** `G1` noise-aware monotonicity: reject + restore best if `S(vₙ) < S* − δ` (2nd
  consecutive fail → HALT REGRESSION); a change within ±δ is noise — keep it only if it doesn't grow the
  artifact · `G2` discard purely-presentational wins · `G3` revert any score gained on an unevidenced
  substrate → `[OPEN]` · `G4` HALT on oscillation (vₙ≈vₙ₋₂) · `G5` HALT on `BUDGET` exceed, emit
  best-so-far · `G6` gain must pay for growth: if size/cost rose by `ΔC%`, require
  `ΔC% ≤ β₀ + β₁·ΔS`, else reject. On accept with `S(vₙ) > S*`, set `S* = S(vₙ)`.
- **5 · Record & repeat.** Log each edit (`dS`, `dC`, accepted). **Prune:** any component edited in the
  last `w` iterations with net gain ≤ 0 goes on a deletion list the generator must delete or justify
  next. Repeat 1–4 until the rung saturates (no gain > δ over `w` iterations, or all rung criteria pass).
- **6 · Boundary.** Advance a rung only if the bar is met **and** ≥1 evaluator still dissents;
  **pause for human confirmation** (escalating the judge changes the definition of success). Rungs:
  E1 fair-critical → E2 adversarial/equal-stringency (reject polish, demand derivations) →
  E3 add a 2nd objective (Pareto) → E4 red-team re-verifies every cited number.
- **7 · Stop & output.** Before claiming `DONE`, the **held-out evaluator** scores the final candidate
  **once**; any criterion it fails that the panel passed means the loop overfit the panel → reopen it,
  record it, and do not claim `DONE` (never reuse the same held-out persona). Output the version,
  provenanced critiques, the updated archive + log, and one next action — or, on HALT, the reason and
  exactly what the human must supply.

## Stance
Keep the generator on a tight leash (small verifiable diffs). Make verification fast and visual; the
checker is a separate, dissenting agent. Engineer the context, don't wordsmith. Prefer the simpler
version on ties. Expect the march of nines — a 90%-good draft is not done.

## Memory schema (`archive.jsonl`, append-only, single-writer)
`{"t":"version"}` · `{"t":"utility","rung","delta","s_star"}` ·
`{"t":"eval","version","evaluator","scores","critiques"}` ·
`{"t":"edit","version","component","hypothesis","dS","dC","accepted"}` · `{"t":"decision"}` ·
`{"t":"substrate","gap","owner","status"}`. Resume = last version + last utility (δ, `S*`) + edit ledger
+ open substrates + Pareto front.

## Notes
- The two highest-value moves are **evolving the evaluator** (so it can't be gamed) and the **substrate
  firewall** (the loop optimizes *features*; it must surface, never fake, *substrates*).
- Regularizers from RRSI: annealed edit budget, edit ledger, stall-triggered exploration (proposer);
  pre-scoring leakage screen, noise-calibrated best-so-far acceptance, gain-must-pay-for-growth, and
  pruning (selector). The held-out evaluator is this skill's adaptation of RRSI's out-of-distribution
  test, not an RRSI component.
- Guardrails follow validated practice: maker–checker separation and structured `DONE`
  (Anthropic, *Effective harnesses for long-running agents*); audit-before-trust against reward-hacking
  (Cursor); bounded autonomy with budgets, rollback, and a human checkpoint at each escalation.
