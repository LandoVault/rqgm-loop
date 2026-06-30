# Worked example — hardening a one-page product spec

A fully generic run, to show how the slots get filled and what the epochs look like. (Domain is
arbitrary; the loop is the same for a paper, a grant, or a codebase.)

## Slots

| slot | value |
|---|---|
| `TARGET` | `spec.md` — a one-page PRD for a new feature |
| `GROUNDING` | the product brief, two competitor docs, the support-ticket export |
| `DONE` | JSON below |
| `EVALUATORS` | (1) senior PM, (2) staff engineer / feasibility skeptic, (3) skeptical customer |
| `MEMORY` | `./archive.jsonl` |
| `BUDGET` | MAX_EPOCHS=4, 150k tokens, 30 min |

```json
{
  "criteria": [
    {"id": "problem-evidence", "test": "the problem is backed by >=3 cited tickets, not asserted", "pass": false},
    {"id": "scope-cut",        "test": "exactly one user + one job; no 'and also'", "pass": false},
    {"id": "success-metric",   "test": "one measurable success metric with a baseline + target", "pass": false},
    {"id": "feasibility",      "test": "an eng reviewer rates build risk <= medium with a reason", "pass": false},
    {"id": "non-goals",        "test": "explicit non-goals listed", "pass": false}
  ],
  "must_not_change": ["the underlying user problem", "the product brief's constraints"],
  "stop": "all criteria pass under the E2 (adversarial) rubric AND no [OPEN] substrate remains"
}
```

## Epoch 1 — E1 (fair-but-critical)

- **v0** drafted from the brief. **Panel mean: weak.** Killers: the problem is asserted (no tickets);
  scope creeps three jobs; success metric is "engagement" with no baseline.
- **v1** revises: cite three tickets, cut to one job, name a metric. Re-score: improved. Rung saturates.
- Boundary → at least one evaluator still dissents ("metric has no target") → **escalate to E2**
  (human confirms).

## Epoch 2 — E2 (adversarial / equal-stringency)

- The staff-engineer critic refuses to reward the cleaner prose and finds the real problem: the metric's
  "baseline" was **made up** to satisfy `success-metric`. → **G3 substrate firewall fires**: revert that
  criterion to `false`, mark `[OPEN: needs a real baseline from analytics]`.
- **v2** rewrites everything that *is* in the team's control (scope, non-goals, feasibility framing) and
  leaves the baseline `[OPEN]`.

## Outcome

- 4 of 5 criteria pass under E2. The 5th (`success-metric`) is **blocked on a substrate** — a real
  analytics baseline the loop cannot invent.
- **Loop output:** "Spec is feature-complete and adversarially clean. **One action for a human:** pull
  the real 30-day baseline for metric X from analytics; then I'll close `success-metric` and we're done."

This is the loop behaving correctly: it optimized every *feature* it could, then **stopped at the
substrate** instead of fabricating a number to score a win. That boundary — features done, substrate
surfaced — is the signal that the machine has finished its part and the human's part begins.
