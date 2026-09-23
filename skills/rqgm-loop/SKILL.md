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
a bar that **rises** (Red Queen Gödel Machine, arXiv:2606.26294). Each rule answers a known failure of
judge-driven loops: lenient, noisy, gameable judges; generators that invent facts and bloat (derivation
and evidence: `DESIGN.md` in the rqgm-loop repo).

## Setup
Collect six slots (ask only for what's missing):
- `TARGET` — the artifact.
- `GROUNDING` — sources of truth, plus 1–2 exemplars of target quality if any.
- `DONE` — atomic, non-overlapping pass/fail criteria. Each criterion names its **check**: a command
  or test if it can be checked mechanically (the result overrides judges), otherwise judges. Also
  must-not-change constraints and the final rung (default **E2**). Propose and confirm if missing.
- `EVALUATORS` — 2–5 judge personas.
- `MEMORY` — append-only `archive.jsonl`.
- `BUDGET` — one global cap on rounds, tokens and time.

The human also writes **3 held-out judge prompts** that the loop never sees. Read `GROUNDING` first.
Resume from `MEMORY` if it exists (drop a torn last record). Otherwise draft **v0** = *best*, send its
numbers and claims to the Verifier, and start at rung **E1**.

The **rubric** = the `DONE` criteria plus the current rung's stance line. It is fixed and changes only
at a human-confirmed escalation.

**Bias probe (once):** judges compare *best* with an identical copy and with a meaning-preserving
rewording. If any verdict is not a tie → **strict mode**: keeping a change needs every judge.

## Roles
Separate agents or fresh contexts; the writer never judges. Where available, judges come from a
different model family than the generator.
- **Generator** sees *best*, `GROUNDING`, `DONE`, the ledger, and the latest flaws.
- **Screen** sees *best*, one diff, the rubric, and the persona names.
- **Verifier** sees one claim and its sources.
- **Judges** see `GROUNDING` and the rubric (a cached prefix), then versions A/B, never the
  generator's rationale.

## Each round
1. **Propose** 2 variants. Each is **one change to one section** (smallest diff; deletions are welcome),
   with a one-line hypothesis naming the criterion it should move. Skip ideas the ledger shows rejected
   by 2 or more judges unless there is new evidence. If the last 2 rounds kept nothing, target the
   least-recently-changed section. Never edit `DONE` or the rubric. Never fabricate data, results,
   people or agreements: write `[OPEN: what is needed]`.
2. **Screen** each diff. Reject it if it echoes the rubric or claims compliance without adding a
   mechanism, targets a judge, adds inert text, weakens a guardrail, or removes an `[OPEN]` without an
   evidenced `substrate` close. Run the mechanical checks. The **Verifier** checks every new number or
   claim against a primary source; if it fails, strip the claim or mark it `[OPEN]`.
3. **Judge** each surviving variant against *best*, blind.
   - Each verdict is A/B/tie per criterion and overall, plus a confidence (low/med/high) and at most 2
     remaining flaws of the version it prefers. Cosmetic differences count as a tie.
   - Judge 1 compares in both orders; if its two verdicts disagree, that counts as a tie.
   - If judge 1 prefers *best* with high confidence, or rates something protected worse, drop the
     variant.
   - Otherwise run judge 2, and judge 3 only on a split.
4. **Keep** a variant if a majority of the judges who ran prefers it and none rates a **protected**
   item worse. Protected items are the guardrails, must-not-change constraints, and criteria *best*
   already passes.
   - A tie goes to the shorter version, so neutral deletions are kept (pruning).
   - Undoing a kept change needs every judge and is reported to the human as a possible thrash.
   - With no majority, the variant is not kept.
   - Keep the best-supported winner and log every variant.
5. **Check** after 3 rounds with nothing kept (a **stall**), or when the generator claims `DONE`. Run
   the mechanical checks, then have 3 fresh judges mark each remaining criterion pass/fail on *best*,
   by majority. If all pass, go to the Boundary. If some fail and the loop is stalled,
   **HALT(STALL)**: report the failing criteria and what only the human can supply. Otherwise continue.

## Boundary — the bar only rises, and only with the human
If the current rung is below the final rung, **pause for the human**. They may escalate or stop here.
Rungs are cumulative: **E1** fair-critical → **E2** adversarial (reject polish, demand derivations) →
**E3** a second objective the human writes into `DONE` as a new criterion. On an escalation, record the
rung, reset the stall count, and continue. Otherwise go to Stop.

## Stop
- If an `[OPEN]` remains, **HALT(STALL)** and name each gap and who must close it.
- Otherwise run the **held-out check**: the human's 3 judges, in fresh contexts, run the same
  pass/fail check by majority and report criterion IDs only.
- If it fails, rerun the rounds on those IDs only, then Check. Then run the held-out check again with
  new human-written judges. A second fail is **HALT(OVERFIT)**.
- Exceeding the budget is **HALT(BUDGET)**, which emits *best*.
- Output *best*, what changed and why (from the ledger), and one next action.

## Memory (`archive.jsonl`, append-only, single writer)
`version{id,parent,change}` · `variant{round,id,section,hypothesis,screen,verdicts,kept}` ·
`citation{claim,source,status}` · `probe{mode}` · `check{rung,pass}` · `rung{name}` ·
`substrate{gap,owner,status}` · `heldout{attempt}` · `halt{reason}`. Resume = last kept version,
ledger, probe mode, rung, open substrates.

## Stance
Tight leash: small, verifiable changes. A separate, dissenting checker. Engineer the context, don't
wordsmith. Ties go to the simpler version. A 90%-good draft is not done. When CPU-bound, run one agent
at a time; a stable order also makes resume deterministic. Use the strongest model for the generator
and held-out judges.
