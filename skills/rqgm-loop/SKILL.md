---
name: rqgm-loop
description: >-
  Co-evolve an artifact against separate, adversarial, evolving evaluators until it meets a defined
  bar (Red Queen Gödel Machine loop). Use to "run the RQGM loop", red-team and iterate, or harden /
  pressure-test a proposal, paper, spec, design, or codebase until it's fundable, defensible, correct,
  or publishable.
---

# RQGM Loop

Improve an artifact by having **separate** agents propose changes, attack them, and judge them against
a bar that **rises** (Red Queen Gödel Machine, arXiv:2606.26294). Each rule below answers one problem
that every judge-driven loop has; the derivation and its evidence are in `DESIGN.md` in the rqgm-loop repo.

## Setup — six slots (ask only for what's missing)
`TARGET` artifact · `GROUNDING` sources of truth (plus 1–2 exemplars of target quality, if any) ·
`DONE` atomic, non-overlapping pass/fail criteria (JSON), must-not-change constraints, hard stop —
propose and confirm if missing · `EVALUATORS` 2–5 judge personas · `MEMORY` append-only
`archive.jsonl` · `BUDGET` max rounds, token and time caps. The human also writes **3 held-out
judge prompts** that the generator never sees. Read `GROUNDING` first. Resume from `MEMORY` if it
exists (drop a torn last record); otherwise draft **v0** = *best*, and start at rung **E1**.
**Bias probe (once):** judges compare *best* with an identical copy and with a meaning-preserving
rewording. If any verdict is not a tie, keeping a change needs every judge (strict mode).

## Roles (always separate agents or fresh contexts; the writer never judges)
- **Generator** sees only *best*, `GROUNDING`, `DONE`, the ledger, and the latest killers.
- **Screen** sees *best* and one diff.
- **Verifier** sees a claim and its sources.
- **Judges** see `GROUNDING` and the current rung's rubric (a cached prefix), then two versions
  labelled A/B. They never see the generator's rationale.

## Each round
1. **Propose** K = 2 variants. Each is **one change to one section** (smallest diff; deletions are
   welcome), with a one-line hypothesis naming the `DONE` criterion it should move. Skip ideas the
   ledger shows rejected unless there is new evidence. After a stall, target the least-recently-changed
   section. Never edit `DONE` or the rubric. Never fabricate data, results, people, or agreements:
   write `[OPEN: what is needed]`.
2. **Screen** each diff before any judging. Reject it if it echoes rubric wording or claims compliance
   without adding a mechanism, targets a judge, adds inert text, weakens a guardrail, or removes an
   `[OPEN]` without an evidenced `substrate` close. Send every new number or claim to the **Verifier**:
   primary source, or strip it, or mark it `[OPEN]`.
3. **Judge** each surviving variant against *best*: blind, with order swapped between judges. Each
   judge gives an A/B/tie verdict per criterion and overall, a confidence, and at most 2 killers of the
   version it prefers. Cosmetic differences count as a tie. Run one judge first; stop if it prefers
   *best* with high confidence or rates a protected item worse. Otherwise run a second judge, and a
   third only if the two split.
4. **Keep** a variant if a majority of judges prefers it and no judge rates a **protected** item worse.
   Protected items are the guardrails, must-not-change constraints, criteria *best* already passes, and
   the E3 objective once named. A shorter variant that no judge rates worse is also kept (pruning).
   Undoing a kept change needs every judge. Keep the winner with the most support (ties go to the
   shorter one); offer the other winners again next round against the new *best*. Log each variant.
5. **Check** after w = 3 rounds with nothing kept (a **stall**), or when the generator claims `DONE`.
   3 fresh judges mark each criterion pass/fail on *best* at the current rung, and each criterion is
   decided by majority. If all criteria pass, go to the Boundary. If some fail and the loop is stalled,
   **HALT(STALL)**: report the failing criteria and what only the human can supply. Otherwise continue.

## Boundary — the bar only rises, and only with the human
If a higher rung exists and a check judge still names a killer, **pause for human confirmation**, then
escalate. Rungs are cumulative: **E1** fair-critical → **E2** adversarial (reject polish, demand
derivations) → **E3** a second objective the human names, which then becomes protected → **E4** a red
team re-verifies every cited number. Record the rung. Otherwise go to Stop.

## Stop
Stop only when every `DONE` criterion passes at the final rung, no `[OPEN]` remains, and the
**held-out check** passes. The held-out check is the human's 3 judges, in fresh contexts, running the
same pass/fail check by majority. If it fails, reopen only those criterion IDs, once (no critique
text), and use new human-written judges next time. A second fail is **HALT(OVERFIT)**. Exceeding the
budget is **HALT(BUDGET)**, which emits *best*. Output: *best*, what changed and why (from the ledger),
and one next action or what the human must supply.

## Memory (`archive.jsonl`, append-only, single writer)
`version{id,parent,change}` · `variant{round,id,section,hypothesis,screen,verdicts,kept}` ·
`citation{claim,source,status}` · `check{rung,pass}` · `rung{name,objective}` ·
`substrate{gap,owner,status}` · `heldout{attempt}` · `halt{reason}`. Resume = last kept version,
ledger, rung, open substrates.

## Stance
Tight leash: small, verifiable changes. A separate, dissenting checker. Engineer the context, don't
wordsmith. Ties go to the simpler version. A 90%-good draft is not done. For cost: run one agent at a
time when CPU-bound (a stable order also makes resume deterministic); use a cheaper model for the
screen and judges and the strongest for the generator and held-out judges.
