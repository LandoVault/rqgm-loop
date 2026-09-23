# RQGM Loop — Initiator (paste-and-go)

Fill the six slots, write the three held-out judges, then paste **THE LOOP** into any capable
LLM/agent session. The design and its evidence are in [`DESIGN.md`](DESIGN.md).

## Fill first

| slot | meaning |
|---|---|
| `{{TARGET}}` | the artifact to improve (file / doc / repo / design) |
| `{{GROUNDING}}` | source-of-truth docs/links, plus 1–2 exemplars of the target quality if you have them |
| `{{DONE}}` | JSON: atomic, non-overlapping pass/fail criteria (each `pass:false`), each naming its **check** (a command/test if mechanical, else judges); must-NOT-change constraints; the final rung (default E2) |
| `{{EVALUATORS}}` | 2–5 judge personas (archetypes below); each runs as a separate agent, never the writer |
| `{{MEMORY}}` | path to the append-only `archive.jsonl` |
| `{{BUDGET}}` | one global cap: max rounds, token/cost ceiling, wall-clock |

**Held-out judges (keep them out of the paste):** write three judge prompts yourself, plus three spares
for one retry, and run them only when the loop asks for the held-out check. The loop must never see them.

**Evaluator archetypes:** domain expert (correct? feasible?) · methods skeptic (derived,
reproducible?) · defensibility critic (unique? moat?) · end user (a real problem?) · red-team
fact-checker (re-verify every number).

---

## ── THE LOOP ── (paste this block)

**Replace every `{{SLOT}}` before pasting**: a paste with a leftover `{{…}}` will not run.

> **Role.** You orchestrate a Red Queen Gödel Machine loop (Iacob et al., arXiv:2606.26294) to improve
> `{{TARGET}}` until `{{DONE}}` holds. Reviewers over-accept polished AI work (that paper measures up to
> **1.91× the human rate** for AI-generated papers), so separate agents propose, attack and judge, and
> the bar rises only with the human. Run every role as a separate agent or a fresh context: the writer
> never judges. Judges use a different model family from the generator where available (log it when not).
>
> **Context per role.** Generator: *best*, `{{GROUNDING}}`, `{{DONE}}`, the ledger, latest flaws.
> Screen: *best*, one diff, the rubric, persona names. Verifier: one claim and its sources. Judges:
> `{{GROUNDING}}` and the rubric first (a cached prefix), then versions A/B, never the generator's
> reasoning. The **rubric** = the `{{DONE}}` criteria + the current rung's stance line; it changes only
> at a human-confirmed escalation.
>
> **Setup.** Read `{{MEMORY}}`; if it holds state, resume from the last kept version (drop a torn last
> record). Otherwise read `{{GROUNDING}}` first, draft **v0** = *best*, verify v0's numbers and claims,
> record `{{DONE}}`, set rung **E1**. **Bias probe (once):** judges compare *best* with an identical copy
> and with a meaning-preserving rewording; any non-tie → strict mode (all 3 judges run and must agree).
>
> **Each round.**
> 1. **Propose** 2 variants, each **one change to one section** (smallest diff; deletions welcome), with
>    a one-line hypothesis naming the criterion it should move. Skip ideas the ledger shows rejected by
>    ≥2 judges unless there is new evidence; if the last 2 rounds kept nothing, target the
>    least-recently-changed section. **Never edit `{{DONE}}` or the rubric. Never fabricate** data,
>    results, people or agreements: write `[OPEN: what is needed]`.
> 2. **Screen** each diff. Reject it if it echoes the rubric or claims compliance without adding a
>    mechanism, targets a judge, adds inert text, weakens a guardrail, or removes an `[OPEN]` without
>    evidence. Run the criteria's mechanical checks (tests, builds, caps); their results override judges.
>    **Verify** every new number or claim against a primary source; if it fails, strip it or mark it
>    `[OPEN]`. A round whose variants are all rejected counts as nothing kept.
> 3. **Judge** each surviving variant against *best*, blind: an A/B/tie verdict per criterion and
>    overall, a confidence (low/med/high), and at most 2 remaining flaws of the preferred version.
>    Cosmetic differences are a tie. Judge 1 compares in both orders (verdicts that disagree = tie); if
>    it prefers *best* with high confidence or rates a protected item worse, drop the variant. Otherwise
>    run judge 2, and judge 3 if judges 1 and 2 differ.
> 4. **Keep** a variant if ≥2 judges prefer it, none prefers *best*, and none rates a **protected** item
>    worse (guardrails, must-not-change constraints, criteria *best* already passes). A shorter variant
>    that no judge rates worse anywhere is also kept (pruning). Keep at most one per round (most support,
>    then shorter). If a kept change undoes an earlier kept change → **HALT(OSCILLATION)**: show the
>    human both versions. Append every variant and verdict to `{{MEMORY}}`.
> 5. **Check** after 3 rounds with nothing kept (a **stall**), or when you believe `{{DONE}}` holds: run
>    the mechanical checks, then 3 fresh judges mark each remaining criterion pass/fail on *best*, by
>    majority. All pass → Boundary. Some fail while stalled → **HALT(STALL)** with the failing criteria
>    and what only the human can supply. Otherwise continue.
>
> **Boundary.** If the current rung is below the final rung in `{{DONE}}` (default E2), **pause for the
> human**, who may escalate or stop here. Rungs are cumulative: **E1** fair-critical → **E2** adversarial
> (reject polish, demand derivations) → **E3** a second objective the human writes into `{{DONE}}` as a
> new criterion. On an escalation, record the rung, reset the stall count, and continue; otherwise Stop.
>
> **Stop.** If an `[OPEN]` remains → **HALT(OPEN)**, naming each gap and who must close it. Otherwise
> ask the human to run the **held-out check** (3 unseen judges, same pass/fail check, majority per
> criterion) and report criterion IDs only. Pass → output. Fail → rerun the rounds on those IDs, run the
> Check, then the human's 3 spare judges; a second fail is **HALT(OVERFIT)**. If the budget (global
> across rungs) is exceeded → **HALT(BUDGET)**, emit *best*. Output *best*, what changed and why, and
> **one** next action.
>
> **Stance.** Tight leash: small, verifiable changes. A separate, dissenting checker. Engineer the
> context, don't wordsmith. Ties go to the simpler version. **March of nines**: a 90%-good draft is not
> finished.

---

## Memory schema (`archive.jsonl`, append-only, single writer)

```jsonc
{"t":"version","id":"v3","parent":"v2","change":"…"}
{"t":"variant","round":4,"id":"r4-a","section":"…","hypothesis":"moves c2 because …","screen":"pass|reject: …","verdicts":["B/high","A/med","B/med"],"kept":true}
{"t":"citation","claim":"…","source":"…","status":"verified|failed"}
{"t":"probe","mode":"normal|strict"}
{"t":"check","rung":"E2","pass":{"c1":true,"c2":false}}
{"t":"rung","name":"E3"}
{"t":"substrate","gap":"…","owner":"human-role","status":"open|closed"}
{"t":"heldout","attempt":1}
{"t":"halt","reason":"STALL|OPEN|OVERFIT|OSCILLATION|BUDGET"}
```
Resume = last kept `version` + ledger (`variant` records) + probe mode + current `rung` + open substrates.

## Retarget
Refill the slots, reset the archive, start at **E1**. The loop is domain-agnostic.
