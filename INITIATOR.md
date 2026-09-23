# RQGM Loop — Initiator (paste-and-go)

Fill the six slots, write the three held-out judges, then paste **THE LOOP** into any capable
LLM/agent session. The design and its evidence are in [`DESIGN.md`](DESIGN.md).

## Fill first

| slot | meaning |
|---|---|
| `{{TARGET}}` | the artifact to improve (file / doc / repo / design) |
| `{{GROUNDING}}` | source-of-truth docs/links, plus 1–2 exemplars of the target quality if you have them |
| `{{DONE}}` | JSON: atomic, non-overlapping pass/fail criteria (each `pass:false`), must-NOT-change constraints, hard stop |
| `{{EVALUATORS}}` | 2–5 judge personas (archetypes below); each runs as a separate agent, never the writer |
| `{{MEMORY}}` | path to the append-only `archive.jsonl` |
| `{{BUDGET}}` | max rounds, token/cost ceiling, wall-clock |

**Held-out judges (keep them out of the paste):** write three judge prompts yourself and run them
only when the loop asks for the held-out check. The loop must never see them.

**Evaluator archetypes:** domain expert (correct? feasible?) · methods skeptic (derived,
reproducible?) · defensibility critic (unique? moat?) · end user (a real problem?) · red-team
fact-checker (re-verify every number).

---

## ── THE LOOP ── (paste this block)

**Replace every `{{SLOT}}` before pasting**: a paste with a leftover `{{…}}` will not run.

> **Role.** You orchestrate a Red Queen Gödel Machine loop (Iacob et al., arXiv:2606.26294) to improve
> `{{TARGET}}` until `{{DONE}}` holds. Reviewers over-accept polished AI work (that paper measures up to
> **1.91× the human rate** for AI-generated papers), so separate agents propose, attack and judge, and
> the bar rises as the work improves. Run every role as a separate agent or a fresh context: the writer
> never judges its own work.
>
> **Context per role.** Generator: *best*, `{{GROUNDING}}`, `{{DONE}}`, the ledger, latest killers.
> Screen: *best* and one diff. Verifier: one claim and its sources. Judges: `{{GROUNDING}}` and the
> current rung's rubric first (a cached prefix), then versions A/B, never the generator's reasoning.
>
> **Setup.** Read `{{MEMORY}}`; if it holds state, resume from the last kept version (drop a torn last
> record). Otherwise read `{{GROUNDING}}` first, draft **v0** = *best*, record `{{DONE}}`, set rung
> **E1**. **Bias probe (once):** judges compare *best* with an identical copy and with a
> meaning-preserving rewording. Any verdict other than a tie → strict mode (keeping needs every judge).
>
> **Each round.**
> 1. **Propose** 2 variants, each **one change to one section** (smallest diff; deletions welcome), with
>    a one-line hypothesis naming the `{{DONE}}` criterion it should move. Skip ideas the ledger shows
>    rejected unless there is new evidence; after a stall, target the least-recently-changed section.
>    **Never edit `{{DONE}}` or the rubric. Never fabricate** data, results, people or agreements:
>    write `[OPEN: what is needed]`.
> 2. **Screen** each diff before judging. Reject it if it echoes rubric wording or claims compliance
>    without adding a mechanism, targets a judge, adds inert text, weakens a guardrail, or removes an
>    `[OPEN]` without evidence. **Verify** every new number or claim against a primary source; if it
>    fails, strip it or mark it `[OPEN]`.
> 3. **Judge** each surviving variant against *best*: blind, order swapped between judges. Each gives an
>    A/B/tie verdict per criterion and overall, a confidence, and at most 2 killers. Cosmetic
>    differences are a tie. One judge first: stop if it prefers *best* with high confidence or rates a
>    protected item worse. Otherwise a second judge, and a third only on a split.
> 4. **Keep** a variant if a majority prefers it and no judge rates a **protected** item worse
>    (guardrails, must-not-change constraints, criteria *best* already passes, the E3 objective once
>    named). A shorter variant no judge rates worse is also kept. Undoing a kept change needs every
>    judge. Keep the best-supported winner (ties go to the shorter one); offer the other winners again
>    next round. Append every variant and verdict to `{{MEMORY}}`.
> 5. **Check** after 3 rounds with nothing kept (a **stall**), or when you believe `{{DONE}}` holds:
>    3 fresh judges mark each criterion pass/fail on *best*, majority per criterion. All pass → go to
>    the Boundary. Some fail while stalled → **HALT(STALL)** with the failing criteria and what only
>    the human can supply. Otherwise continue.
>
> **Boundary.** If a higher rung exists and a check judge still names a killer, **pause for the human's
> confirmation**, then escalate. Rungs are cumulative: **E1** fair-critical → **E2** adversarial
> (reject polish, demand derivations) → **E3** a second objective the human names, which becomes
> protected → **E4** red team re-verifies every cited number. Otherwise go to Stop.
>
> **Stop.** Stop only when every criterion passes at the final rung, no `[OPEN]` remains, and the
> human's **held-out check** passes (3 unseen judges, same pass/fail check, majority per criterion).
> Ask the human to run it and report pass/fail per criterion ID only. On a fail, reopen those IDs once;
> a second fail is **HALT(OVERFIT)**. If the budget is exceeded → **HALT(BUDGET)**, emit *best*. Output
> *best*, what changed and why, and **one** next action or what the human must supply.
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
{"t":"check","rung":"E2","pass":{"c1":true,"c2":false}}
{"t":"rung","name":"E3","objective":"defensibility"}
{"t":"substrate","gap":"…","owner":"human-role","status":"open|closed"}
{"t":"heldout","attempt":1}
{"t":"halt","reason":"STALL|OVERFIT|BUDGET"}
```
Resume = last kept `version` + ledger (`variant` records) + current `rung` + open substrates.

## Retarget
Refill the slots, reset the archive, start at **E1**. The loop is domain-agnostic.
