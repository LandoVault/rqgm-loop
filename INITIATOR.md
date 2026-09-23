# RQGM Loop — Initiator (paste-and-go)

Fill the six slots, then paste **THE LOOP** into any capable LLM/agent session. The block is
self-contained — it runs without the rest of this file.

## Fill first

| slot | meaning |
|---|---|
| `{{TARGET}}` | the artifact to optimize (file / doc / repo / design) |
| `{{GROUNDING}}` | source-of-truth docs/links the agents may read |
| `{{DONE}}` | **machine-verifiable** success spec: a list of pass/fail criteria (write as JSON, each `pass:false`), the constraints (what must NOT change), and the hard stop |
| `{{EVALUATORS}}` | 2–5 adversarial judges, **each a separate agent from the generator** (archetypes below), plus **1 held-out judge** the generator never sees before Stop |
| `{{MEMORY}}` | path to the append-only `archive.jsonl` (state + resume) |
| `{{BUDGET}}` | caps: MAX_ITERS (= N), token/cost ceiling, wall-clock; optional overrides of the defaults in **Units** |

**Evaluator archetypes** (pick `{{EVALUATORS}}`): domain-expert (correct / feasible?) · rigor-&-methods
skeptic (derived, reproducible, powered?) · strategy / defensibility critic (unique? moat? competitive
threat?) · end-user (solves a real problem?) · red-team fact-checker (re-verify every number).

---

## ── THE LOOP ── (paste this block)

**Replace every `{{SLOT}}` before pasting** — a paste still containing `{{…}}` will not run.

> **Role.** You orchestrate a Red Queen Gödel Machine loop (Iacob et al., arXiv:2606.26294): co-evolve a
> *generator* against *separate, adversarial, evolving* evaluators to drive `{{TARGET}}` to `{{DONE}}`.
> Static evaluators over-accept polished/AI work — that paper measures up to **1.91× the human rate** for
> AI-generated work — so the checker must be a **different agent** from the writer and must get
> **stricter** as the writer improves. Re-facing one panel also lets the writer overfit it, chase score
> noise, and bloat the artifact, so the loop is **regularized** after RRSI (Xia et al., arXiv:2609.24972;
> the panel/held-out mapping, per-rung δ, noise-band rule and all defaults are this loop's adaptations).
>
> **Units.** Judges score each criterion and `overall` on 0–10; `S(v)` = panel mean `overall`; a
> criterion passes on a panel majority. `C(v)` = word count of `{{TARGET}}` (tokens for code). A
> **component** is a top-level section or file, listed at setup. Epoch = one rung; iteration = one
> generate→gate cycle. Defaults: `b_max=3`, `w=3`, `β₀=2%`, `β₁=5%`/point, `δ_min=0.3`.
>
> **0 · Setup (load or bootstrap).** Read `{{MEMORY}}`. If it holds prior state → resume (see schema);
> if its last record is torn, discard it and use the prior. If empty → bootstrap: read `{{GROUNDING}}` **first**, draft **v0** of
> `{{TARGET}}`, write `{{DONE}}` as a checkable JSON criteria-list (every item `pass:false`), list the
> components, set rung **E1**. Exactly one writer to the archive at a time. **Calibrate noise:** the panel
> scores the unchanged version twice; `δ = max(δ_min, |S₁ − S₂|)`, best-so-far `S*` = their mean. Redo
> at every rung change.
>
> **1 · Generator step.** Revise **vₙ** (n = 1…N, N = MAX_ITERS, not reset per rung) with at most
> `bₙ = 1 + round_half_up((b_max − 1)·½(1 + cos(π·n/N)))` edits, highest-leverage critiques first —
> bundled early for coordinated fixes, single late so gains are attributable. One edit = one component +
> a one-line falsifiable hypothesis; smallest reviewable diff; version each vₙ so any state is
> revertable. Skip hypotheses the ledger shows rejected on a single-edit iteration unless there is new
> evidence. If **stalled** (no gain > δ for `w` iterations), spend ≥1 edit on a never-edited component.
> **Never edit `{{DONE}}` or the rubric to pass. Never fabricate a substrate** (real data, people,
> results, agreements) — mark gaps `[OPEN]`.
>
> **2 · Evaluator step.** First a **leakage screen**: a checker (≠ the generator) reads the diff *before*
> scoring and rejects edits that assert compliance without adding mechanism, or that target a named
> judge. Then each `{{EVALUATORS}}` agent (≠ the generator) scores vₙ under the **current** rung's rubric
> (not formatting / length / tone), returning scores + **ranked killers** + required fixes tagged to
> claims.
>
> **3 · Verify before trust.** Any number or claim newly entering vₙ without a citation event in the
> archive → BLOCK; dispatch a verification agent on primary sources before trusting any score (assume
> the generator takes any shortcut the rubric leaves open).
>
> **4 · Gates (every iteration — `assert … else <action>`),** with `ΔS = S(vₙ) − S(parent)` and `ΔC` =
> relative change in `C`:
> - **G1 noise-aware monotonicity** — on the *fixed* rung utility, if `S(vₙ) < S* − δ` → reject vₙ,
>   restore the best version, retry once with the critique appended; on a 2nd failure →
>   **HALT(REGRESSION)**.
> - **G2 no-polish-reward** — a purely presentational top change → discard, re-revise on substance.
> - **G3 substrate firewall** — if a score rose on an asserted-but-unevidenced substrate → revert, mark
>   `[OPEN]`; a version with open substrates can never be "done".
> - **G4 oscillation** — if vₙ ≈ vₙ₋₂ (thrash) → **HALT(OSCILLATION)**, surface both.
> - **G5 budget** — if iterations / tokens / wall-clock exceed `{{BUDGET}}` → **HALT(BUDGET)**, emit best-so-far.
> - **G6 gain pays for growth** — if `ΔS > δ`, require `ΔC ≤ β₀ + β₁·ΔS`; if `|ΔS| ≤ δ` (noise), accept
>   only if `ΔC ≤ 0`. On accept, `S* = max(S*, S(vₙ))`.
>
> **5 · Record & repeat.** Append version, scores, critiques, decisions and each edit (component,
> hypothesis, `dS`, `dC`, accepted; bundled edits share the version's `dS`) to `{{MEMORY}}`. **Prune:** a
> component whose best accepted `dS` over the last `w` iterations is ≤ 0 goes on a deletion list; the
> checker rules on any keep-justification; gates, `{{DONE}}` items and `[OPEN]` markers are exempt. The
> rung **saturates** when every rung criterion passes, or when no gain > δ for `2w` iterations (i.e.
> exploration also failed).
>
> **6 · Boundary (evolve the utility).** Advance one rung **only if** the current bar is met **and** ≥1
> evaluator still dissents (else done, or stuck → HALT). Escalation *redefines success*, so **pause for
> a human checkpoint here**. Record the utility event; scores
> across a boundary are not comparable. Rungs: **E1** fair-but-critical → **E2** adversarial /
> equal-stringency (reject polish; demand every number derived) → **E3** add a 2nd objective as a Pareto
> axis (e.g. defensibility / moat) → **E4** red-team that re-verifies every cited number.
>
> **7 · Stop & output.** Before claiming done, the **held-out judge** scores the final candidate
> **once**; a criterion it fails that the panel passed means the loop overfit the panel → reopen it and
> do not claim done. STOP when `{{DONE}}` passes under the escalated utility, the held-out check passes,
> **and** no `[OPEN]` substrates remain — or when any HALT fires. Output: the current version, the
> provenanced critiques, the updated archive + log, and **one** next action (or, on HALT, the reason +
> what a human must supply).
>
> **Stance (hold throughout).** **Tight leash** — small, verifiable steps. Verification **fast and
> visual**; a model grading itself is too generous, so the checker is a separate, *dissenting* agent.
> Engineer the **context**, don't wordsmith. Ties go to the simpler version. Expect the **march of nines**: each reliability nine costs
> as much as all the prior ones combined — don't mistake a 90%-good draft for a finished one.

---

## Memory schema (`archive.jsonl`, append-only, single-writer)

```jsonc
{"t":"version","id":"vN","parent":"vN-1","summary":"…"}
{"t":"utility","rung":"E2","rule":"adversarial-equal-stringency","delta":0.4,"s_star":6.1,"s_star_version":"vN"}
{"t":"eval","version":"vN","evaluator":"…","scores":{"…":N,"overall":N},"critiques":[{"target","severity","text"}]}
{"t":"edit","version":"vN","component":"…","hypothesis":"…","dS":0.6,"dC":0.03,"accepted":true,"rejected_by":null}
{"t":"decision","critique":"…","action":"accept|reject","why":"…"}
{"t":"substrate","gap":"…","owner":"human-role","status":"open|closed"}
```
Resume = last `version` + last `utility` (δ, `S*`) + edit ledger + open substrates + recomputed Pareto front.
`rejected_by` ∈ `screen | G1 | G2 | G3 | G6`.

## Retarget
Refill the six slots, reset the archive, start at **E1**; THE LOOP is domain-agnostic.
