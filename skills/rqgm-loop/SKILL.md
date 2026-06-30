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

## When invoked

1. **Collect the six slots** from the request and context (ask only for what's missing):
   - `TARGET` — the artifact to optimize · `GROUNDING` — sources of truth the agents may read ·
     `DONE` — a machine-verifiable success spec (pass/fail criteria as JSON + constraints that must not
     change + a hard stop) · `EVALUATORS` — 2–5 critic personas, each run as a **separate subagent** ·
     `MEMORY` — a file for the append-only `archive.jsonl` · `BUDGET` — MAX_EPOCHS + token/wall-clock caps.
   - If the user hasn't defined `DONE`, propose a concrete checkable spec and confirm it before starting.
2. **Run THE LOOP** below, spawning the evaluators (and any verification/research help) as subagents so
   the checker is never the writer. *Requires a host that can spawn subagents (e.g. a Task/Agent tool);
   if none is available, run each evaluator as a separate, fresh-context pass.*
3. **Persist** state to `MEMORY` after every epoch; mirror a human-readable log.
4. **Stop** at `DONE` (under the escalated utility, no open substrates) or on any HALT, and report.

## THE LOOP

- **0 · Setup.** Read `MEMORY`; resume if state exists (torn last record → discard, use prior), else
  read `GROUNDING` first, draft **v0**, write `DONE` as JSON criteria (each `pass:false`), set rung **E1**.
- **1 · Generate.** Revise **vₙ** for the single highest-leverage open critique; smallest reviewable
  diff; version it. Never edit `DONE`/the rubric to pass; never fabricate a substrate (real data,
  people, results, agreements) — mark gaps `[OPEN]`.
- **2 · Evaluate.** Each evaluator subagent (≠ generator) scores vₙ on the current rung's rubric
  (excluding formatting/length/tone) and returns scores + ranked killers + required fixes, tagged to claims.
- **3 · Verify.** Any new number/claim lacking a citation event → BLOCK and verify against primary
  sources before trusting the score (assume the generator will exploit any gap the rubric leaves).
- **4 · Gates.** `G1` reject + restore on a score regression (2nd fail → HALT REGRESSION) · `G2` discard
  purely-presentational wins · `G3` revert any score gained on an unevidenced substrate → `[OPEN]` ·
  `G4` HALT on oscillation (vₙ≈vₙ₋₂) · `G5` HALT on `BUDGET` exceed, emit best-so-far.
- **5 · Record & repeat** 1–4 until the rung saturates (score plateau or all rung criteria pass).
- **6 · Boundary.** Advance a rung only if the bar is met **and** ≥1 evaluator still dissents;
  **pause for human confirmation** (escalating the judge changes the definition of success). Rungs:
  E1 fair-critical → E2 adversarial/equal-stringency (reject polish, demand derivations) →
  E3 add a 2nd objective (Pareto) → E4 red-team re-verifies every cited number.
- **7 · Stop & output** the version, provenanced critiques, the updated archive + log, and one next
  action — or, on HALT, the reason and exactly what the human must supply.

## Stance
Keep the generator on a tight leash (small verifiable diffs). Make verification fast and visual; the
checker is a separate, dissenting agent. Engineer the context, don't wordsmith. Expect the march of
nines — a 90%-good draft is not done.

## Memory schema (`archive.jsonl`, append-only, single-writer)
`{"t":"version"}` · `{"t":"utility","rung"}` · `{"t":"eval","version","evaluator","scores","critiques"}`
· `{"t":"decision"}` · `{"t":"substrate","gap","owner","status"}`. Resume = last version + last utility +
open substrates + Pareto front.

## Notes
- The two highest-value moves are **evolving the evaluator** (so it can't be gamed) and the **substrate
  firewall** (the loop optimizes *features*; it must surface, never fake, *substrates*).
- Guardrails follow validated practice: maker–checker separation and structured `DONE`
  (Anthropic, *Effective harnesses for long-running agents*); audit-before-trust against reward-hacking
  (Cursor); bounded autonomy with budgets, rollback, and a human checkpoint at each escalation.
