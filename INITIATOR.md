# RQGM Loop — Initiator (paste-and-go)

Fill the six slots, then paste **THE LOOP** block into any capable LLM/agent session. The block is
self-contained — it runs without the rest of this file.

## Fill first

| slot | meaning |
|---|---|
| `{{TARGET}}` | the artifact to optimize (file / doc / repo / design) |
| `{{GROUNDING}}` | source-of-truth docs/links the agents may read |
| `{{DONE}}` | **machine-verifiable** success spec: a list of pass/fail criteria (write as JSON, each `pass:false`), the constraints (what must NOT change), and the hard stop |
| `{{EVALUATORS}}` | 2–5 adversarial judges, **each a separate agent from the generator** (archetypes below), plus **1 held-out judge** the generator never sees before Stop |
| `{{MEMORY}}` | path to the append-only `archive.jsonl` (state + resume) |
| `{{BUDGET}}` | caps: MAX_EPOCHS (= N, total iterations), token/cost ceiling, wall-clock; optional overrides of the regularizer defaults (`b_max=3`, `w=3`, `β₀=2%`, `β₁=5%`/point, `δ_min=0.3`) |

**Evaluator archetypes** (pick `{{EVALUATORS}}`): domain-expert (correct / feasible?) · rigor-&-methods
skeptic (derived, reproducible, powered?) · strategy / defensibility critic (unique? moat? competitive
threat?) · end-user (solves a real problem?) · red-team fact-checker (re-verify every number).

---

## ── THE LOOP ── (paste this block)

**Before pasting, replace every `{{SLOT}}` with your values** — a literal paste that still contains
`{{…}}` will not run.

> **Role.** You orchestrate a Red Queen Gödel Machine loop (Iacob et al., arXiv:2606.26294): co-evolve a
> *generator* against *separate, adversarial, evolving* evaluators to drive `{{TARGET}}` to `{{DONE}}`.
> Static evaluators over-accept polished/AI work — that paper measures up to **1.91× the human rate** for
> AI-generated work — so the checker must be a **different agent** from the writer and must get
> **stricter** as the writer improves. Because the writer re-faces the same panel every iteration, it can
> also overfit that panel, chase score noise, and bloat the artifact, so the loop is **regularized**
> following RRSI (Xia et al., arXiv:2609.24972), adapted from harness benchmarks to evaluator panels.
> **Score scale:** every judge scores each criterion and `overall` on 0–10; `S(v)` = panel mean `overall`.
>
> **0 · Setup (load or bootstrap).** Read `{{MEMORY}}`. If it holds prior state → resume (last version,
> utility rung, open critiques, open `[OPEN]` substrates); if its last record is torn, discard it and use
> the prior. If empty → bootstrap: read `{{GROUNDING}}` **first** (never generate before reading), draft
> **v0** of `{{TARGET}}`, write `{{DONE}}` as a checkable JSON criteria-list (every item `pass:false`),
> set utility rung **E1**. Exactly one writer to the archive at a time. **Calibrate noise:** have the
> panel score the unchanged current version twice; `δ = max(δ_min, |S₁ − S₂|)`, best-so-far `S*` = their
> mean. Recalibrate δ and reset `S*` at every rung change.
>
> **1 · Generator step.** Produce/revise **vₙ** with at most `bₙ = ⌈1 + (b_max − 1)·½(1 + cos(π·n/N))⌉`
> edits, highest-leverage critiques first — bundled early for coordinated fixes, one at a time late so
> gains are attributable. Each edit names its component and a one-line falsifiable hypothesis. Read the
> edit ledger first: don't retry a hypothesis already rejected on that component without new evidence.
> If **stalled** (no gain > δ over the last `w` iterations), spend ≥1 edit on a never-edited component.
> Smallest reviewable diff; version each vₙ so any state is revertable. **Never edit `{{DONE}}` or the rubric to pass. Never fabricate a substrate** (real data,
> people, results, agreements) — mark gaps `[OPEN]`.
>
> **2 · Evaluator step.** First a **leakage screen**: a checker (≠ the generator) reads the diff *before*
> scoring and rejects edits that echo a judge's rubric wording, target a named judge, or add inert text
> (claims compliance without doing it). Then each `{{EVALUATORS}}` agent (≠ the generator) scores vₙ under the **current**
> rung's rubric (dimensions exclude formatting / length / tone) and returns per-criterion scores + one
> overall number + **ranked killers** + required fixes, each tagged to the claim it targets.
>
> **3 · Verify before trust.** Any number or claim newly entering vₙ without a citation event in the
> archive → BLOCK; dispatch a verification agent; prefer primary sources; audit before trusting any score
> (assume the generator will take any shortcut the rubric leaves open).
>
> **4 · Gates (run every iteration — `assert … else <action>`):**
> - **G1 noise-aware monotonicity** — on the *fixed* rung utility, if `S(vₙ) < S* − δ` → reject vₙ,
>   restore the best version, retry once with the critique appended; on 2nd consecutive failure →
>   **HALT(REGRESSION)**. A change within ±δ is noise: keep it only if it doesn't grow the artifact. On
>   accept with `S(vₙ) > S*`, set `S* = S(vₙ)`.
> - **G2 no-polish-reward** — if the top-scoring change is purely presentational → discard, re-revise on
>   substance.
> - **G3 substrate firewall** — if a score rose on an asserted-but-unevidenced substrate → revert, mark
>   `[OPEN]`; a version with open substrates can never be "done".
> - **G4 oscillation** — if vₙ ≈ vₙ₋₂ (thrash between two versions) → **HALT(OSCILLATION)**, surface both.
> - **G5 budget** — if epochs / tokens / wall-clock exceed `{{BUDGET}}` → **HALT(BUDGET)**, emit best-so-far.
> - **G6 gain pays for growth** — if size/cost rose by `ΔC%`, require `ΔC% ≤ β₀ + β₁·ΔS`, else reject.
>
> **5 · Record & repeat.** Append (version, scores, critiques, per-edit `dS`/`dC`/accepted, decisions)
> to `{{MEMORY}}`. **Prune:** any component edited in the last `w` iterations with net gain ≤ 0 goes on a
> deletion list the generator must delete or justify next. Repeat 1–4 until the rung **saturates**: no
> gain > δ over `w` iterations OR every criterion for this rung passes.
>
> **6 · Boundary (evolve the utility).** Advance one rung **only if** the current bar is met **and** ≥1
> evaluator still dissents (else you are done, or stuck → HALT). Escalating the evaluator *changes the
> definition of success*, so **pause for a human checkpoint here**. Record the utility event; scores
> across a boundary are not comparable. Rungs: **E1** fair-but-critical → **E2** adversarial /
> equal-stringency (reject polish; demand every number derived) → **E3** add a 2nd objective as a Pareto
> axis (e.g. defensibility / moat) → **E4** red-team that re-verifies every cited number.
>
> **7 · Stop & output.** Before claiming done, the **held-out judge** scores the final candidate
> **once**; any criterion it fails that the panel passed means the loop overfit the panel → reopen it and
> do not claim done (never reuse that held-out persona). STOP when `{{DONE}}` passes under the escalated
> utility, the held-out check passes, **and** no `[OPEN]` substrates remain — or when any HALT fires. Output: the current version, the provenanced critiques, the
> updated archive + a human-readable log, and **one** next action (or, on HALT, the reason + exactly what
> a human must supply).
>
> **Stance (hold throughout).** Keep the generator on a **tight leash** — small, verifiable steps you can
> review. Make verification **fast and visual**; a model grading itself is too generous, so the checker
> is a separate, *dissenting* agent. Engineer the **context** (just-enough right information), don't
> wordsmith. Prefer the simpler version on ties. Expect the **march of nines**: each reliability nine costs as much as all the prior ones
> combined — don't mistake a 90%-good draft for a finished one.

---

## Memory schema (`archive.jsonl`, append-only, single-writer)

```jsonc
{"t":"version","id":"vN","parent":"vN-1","summary":"…"}
{"t":"utility","rung":"E2","rule":"adversarial-equal-stringency","delta":0.4,"s_star":6.1}
{"t":"eval","version":"vN","evaluator":"…","scores":{"…":N,"overall":N},"critiques":[{"target","severity","text"}]}
{"t":"edit","version":"vN","component":"…","hypothesis":"…","dS":0.6,"dC":"+3%","accepted":true}
{"t":"decision","critique":"…","action":"accept|reject","why":"…"}
{"t":"substrate","gap":"…","owner":"human-role","status":"open|closed"}
```
Resume = last `version` + last `utility` (δ, `S*`) + edit ledger + open substrates + recomputed Pareto front.

## Retarget
Refill the six slots, reset the archive, start at **E1**. THE LOOP is domain-agnostic.
