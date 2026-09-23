# RQGM Loop — Initiator (paste-and-go)

Fill the six slots, then paste **THE LOOP** (self-contained) into any capable LLM/agent session.

## Fill first

| slot | meaning |
|---|---|
| `{{TARGET}}` | the artifact to optimize (file / doc / repo / design) |
| `{{GROUNDING}}` | source-of-truth docs/links the agents may read |
| `{{DONE}}` | **machine-verifiable** success spec: JSON pass/fail criteria (each `pass:false`), must-NOT-change constraints, and the hard stop |
| `{{EVALUATORS}}` | 2–5 adversarial judges, **each a separate agent from the generator** (archetypes below); write the **held-out judge** separately — never paste it |
| `{{MEMORY}}` | path to the append-only `archive.jsonl` (state + resume) |
| `{{BUDGET}}` | caps: MAX_ITERS (= N), token/cost ceiling, wall-clock; optional overrides of the defaults in **Units** |

**Evaluator archetypes:** domain-expert (correct? feasible?) · methods skeptic (derived, reproducible,
powered?) · defensibility critic (unique? moat?) · end-user (real problem?) · red-team fact-checker
(re-verify every number).

---

## ── THE LOOP ── (paste this block)

**Replace every `{{SLOT}}` before pasting** — leftover `{{…}}` will not run.

> **Role.** You orchestrate a Red Queen Gödel Machine loop (Iacob et al., arXiv:2606.26294): co-evolve a
> *generator* against *separate, adversarial, evolving* evaluators to drive `{{TARGET}}` to `{{DONE}}`.
> Static evaluators over-accept polished/AI work — that paper measures up to **1.91× the human rate** for
> AI-generated work — so the checker must be a **different agent** from the writer and must get
> **stricter** as the writer improves. Re-facing one panel also lets the writer overfit it, chase score
> noise, and bloat the artifact, so the loop is **regularized** after RRSI (Xia et al., arXiv:2609.24972;
> the panel/held-out mapping, human-held held-out judge, checker ≠ generator, screen targets,
> per-rung δ, noise band, `bₙ` rounding, prune threshold/window, `S*` re-score and all defaults are
> adaptations).
>
> **Units.** Judges score each criterion and `overall` on 0–10; `S(v)` = panel mean `overall`; a judge
> passes a criterion at ≥7, the panel on a strict majority (ties fail). `C(v)` = word count of
> `{{TARGET}}` (tokens for code). A **component** is a top-level section or file, fixed at setup
> (checker-approved). Epoch = rung; iteration = generate→gate cycle. Defaults: `b_max=3`, `w=3`,
> `β₀=2%`, `β₁=5%`/point, `δ_min` = 1/panel size, `δ_max=1.5`.
>
> **0 · Setup (load or bootstrap).** Read `{{MEMORY}}`. If it holds prior state → resume (see schema);
> discard a torn last record. If empty → bootstrap: read `{{GROUNDING}}` **first**, draft **v0** of
> `{{TARGET}}`, write `{{DONE}}` as a checkable JSON criteria-list (every item `pass:false`), list the
> components, set rung **E1**. **Calibrate noise:** the panel
> scores the unchanged version 3× in fresh contexts; `δ = clip(2·SD, δ_min, δ_max)`, best-so-far `S*` =
> the mean. Redo at every rung change.
>
> **1 · Generator step.** Revise **vₙ** (n = 1…N, N = MAX_ITERS, not reset per rung) with at most
> `bₙ = 1 + round_half_up((b_max − 1)·½(1 + cos(π·n/N)))` edits, highest-leverage critiques first —
> bundled early for coordinated fixes, single late (attributable). One edit = one component +
> a one-line falsifiable hypothesis; smallest reviewable diff; version each vₙ so any state is
> revertable. Skip hypotheses the ledger rejected on single-edit iterations absent new evidence. If
> **stalled** (no gain > δ for `w` iterations), spend ≥1 edit on a never-edited component.
> **Never edit `{{DONE}}` or the rubric to pass. Never fabricate a substrate** (real data, people,
> results, agreements) — mark gaps `[OPEN]`.
>
> **2 · Evaluator step.** First a **leakage screen**: a checker (≠ the generator) reads the diff *before*
> scoring and rejects edits that echo rubric wording, assert compliance without adding mechanism, or
> target a named judge. Then each `{{EVALUATORS}}` agent (≠ the generator) scores vₙ under the
> **current** rung's rubric (not format/length/tone): scores + **ranked killers** + required
> fixes tagged to claims.
>
> **3 · Verify before trust.** Any number or claim newly entering vₙ without a `citation` record → BLOCK;
> a verification agent checks primary sources before any score is trusted.
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
> - **G6 gain pays for growth** — if `ΔS > δ`, require `ΔC ≤ β₀ + β₁·ΔS`; if `|ΔS| ≤ δ` (noise), require
>   `ΔC ≤ 0` (or `ΔC ≤ β₀`, once per component, for a single edit on a never-edited one); else reject,
>   restore the parent. Only on an accept with `ΔS > δ`: `S* = max(S*, mean(S(vₙ), fresh re-score))`.
>
> **5 · Record & repeat.** Append every record (schema below; bundles share the version's `dS`)
> to `{{MEMORY}}`. **Prune** only text the loop added: if a component's accepted edits in the last `2w`
> iterations all had `dS ≤ δ`, their text is deleted (a gated edit) unless the checker upholds keeping
> it; `{{DONE}}` must-not-change items and `[OPEN]` markers are exempt. The
> rung **saturates** when every rung criterion passes; no gain > δ for `2w` iterations →
> **HALT(STALL)**.
>
> **6 · Boundary (evolve the utility).** A judge **dissents** if it scores any criterion < 7. Advance
> one rung **only if** the current bar is met **and** ≥1 judge dissents (none → the human may skip
> rungs). Escalation *redefines success*, so **pause for a human checkpoint here**. Record the utility event; scores across a boundary are not comparable. Rungs (cumulative): **E1** fair-but-critical → **E2** adversarial /
> equal-stringency (reject polish; demand every number derived) → **E3** add a 2nd objective as a Pareto
> axis (e.g. defensibility / moat) → **E4** red-team that re-verifies every cited number.
>
> **7 · Stop & output.** STOP only when `{{DONE}}` passes under the escalated utility, no `[OPEN]`
> substrate remains, **and** the **held-out judge** — written by the human, kept out of this paste, run
> once on the final rung in a fresh context — passes every criterion. A fail (panel overfit)
> → the human seals its critique outside `{{MEMORY}}` (log only `heldout{attempt}`) and reopens only that
> criterion ID with a fresh human-written judge; a 2nd fail → **HALT(OVERFIT)**. Or STOP on any HALT.
> Output: the current version, provenanced critiques, archive/log, and **one** next action (on HALT: the
> reason + what a human must supply).
>
> **Stance (hold throughout).** **Tight leash** — small, verifiable steps. Verification **fast and
> visual**; a model grading itself is too generous, so the checker is a separate, *dissenting* agent.
> Engineer the **context**, don't wordsmith. Ties go to the simpler version. **March of nines** — a
> 90%-good draft is not finished.

---

## Memory schema (`archive.jsonl`, append-only, single-writer)

```jsonc
{"t":"version","id":"vN","parent":"vN-1","summary":"…"}
{"t":"utility","rung":"E2","rule":"adversarial-equal-stringency","delta":0.4,"s_star":6.1,"s_star_version":"vN"}
{"t":"eval","version":"vN","evaluator":"…","scores":{"…":N,"overall":N},"critiques":[{"target","severity","text"}]}
{"t":"edit","version":"vN","component":"…","hypothesis":"…","dS":0.6,"dC":0.03,"accepted":true,"rejected_by":"screen|G1|G2|G3|G6|null"}
{"t":"calib","rung":"E2","runs":[6.0,6.3,5.8],"sd":0.25}
{"t":"screen","version":"vN","edit":"…","verdict":"pass|reject","reason":"…"}
{"t":"citation","claim":"…","source":"…","status":"verified|failed"}
{"t":"decision","critique":"…","action":"accept|reject","why":"…"}
{"t":"heldout","attempt":1}
{"t":"halt","reason":"REGRESSION|OSCILLATION|BUDGET|STALL|OVERFIT"}
{"t":"substrate","gap":"…","owner":"human-role","status":"open|closed"}
```
Resume = last `version` + last `utility` (δ, `S*`) + edit ledger + open substrates + recomputed Pareto front.

## Retarget
Refill the slots, reset the archive, start at **E1**; THE LOOP is domain-agnostic.
