# Worked example — hardening a one-page product spec

A fully generic run, showing how the slots get filled and what the rounds look like. The domain is
arbitrary; the loop is the same for a paper, a grant, or a codebase.

## Slots

| slot | value |
|---|---|
| `TARGET` | `spec.md` — a one-page PRD for a new feature |
| `GROUNDING` | the product brief, two competitor docs, the support-ticket export, one past spec the team rated excellent |
| `DONE` | JSON below |
| `EVALUATORS` | (1) senior PM, (2) staff engineer / feasibility skeptic, (3) skeptical customer |
| `MEMORY` | `./archive.jsonl` |
| `BUDGET` | 12 rounds, 150k tokens, 45 min |
| held-out | three judges the PM lead wrote: a finance reviewer, a support lead, a new engineer |

```json
{
  "criteria": [
    {"id": "problem-evidence", "test": "the problem is backed by >=3 cited tickets, not asserted", "pass": false},
    {"id": "scope-cut",        "test": "exactly one user + one job; no 'and also'", "pass": false},
    {"id": "success-metric",   "test": "one measurable success metric with a real baseline + target", "pass": false},
    {"id": "feasibility",      "test": "build risk stated as <= medium with a reason", "pass": false},
    {"id": "non-goals",        "test": "explicit non-goals listed", "pass": false}
  ],
  "must_not_change": ["the underlying user problem", "the product brief's constraints"],
  "stop": "all criteria pass at E2, no [OPEN] remains, held-out check passes"
}
```

## Setup

`v0` is drafted from the brief. **Bias probe:** judges compare `v0` with an identical copy and with a
reworded copy, and all verdicts are ties, so the normal (majority) keep rule applies.

## Rounds 1–4 — E1 (fair-critical)

- **Round 1.** Variant A cites three tickets in the problem section (for `problem-evidence`). Variant B
  cuts the scope to one job (for `scope-cut`). Both pass the screen and the tickets verify against the
  export. Judge 1 prefers A and judge 2 prefers A, so **A is kept**. B wins too and is offered again next
  round.
- **Round 2.** B is re-proposed against the new best and **kept** 2/2. Variant C (a nicer intro)
  gets a *tie* from judge 1 as a cosmetic change, then a tie from judge 2, so it is not kept.
- **Round 3.** Variant D adds a success metric "engagement +20% from a 35% baseline". The screen sends
  the baseline to the verifier; no source exists, so the number is replaced by
  `[OPEN: real 30-day baseline from analytics]`. Judges prefer D, and it is kept.
- **Round 4.** Non-goals added and kept. The generator believes `DONE` holds, so the loop runs a
  **check**. Four criteria pass. `success-metric` fails because its baseline is `[OPEN]`.

## Rounds 5–7 — nothing more to gain

Three rounds of variants (tightening wording, a feasibility caveat) keep nothing: judges tie or prefer
the current best. That is a **stall** with `success-metric` still failing → **HALT(STALL)**.

## Output

- *Best* = v4: four of five criteria pass. `success-metric` is **blocked on a substrate**, a real
  analytics baseline the loop cannot invent.
- **Loop output:** "Spec is feature-complete. **One action for a human:** pull the real 30-day baseline
  for metric X from analytics; then I'll re-run the check, escalate to E2 with your confirmation, and
  finish with your held-out judges."

This is the loop behaving correctly. It kept only changes independent judges preferred, it refused to
turn a made-up number into a win, and it stopped at the substrate with a precise request. The boundary
between "features done" and "substrate surfaced" is where the machine's part ends and yours begins.
