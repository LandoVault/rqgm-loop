# Worked example — hardening a one-page product spec

**Illustrative, not a logged run**: no outcome here is evidence. It shows how the slots fill and how
v3's rules play out, in any domain.

## Slots

| slot | value |
|---|---|
| `TARGET` | `spec.md` — a one-page PRD for a new feature |
| `GROUNDING` | the product brief, two competitor docs, the support-ticket export, one exemplar spec |
| `DONE` | JSON below |
| `EVALUATORS` | (1) senior PM, (2) staff engineer / feasibility skeptic, (3) skeptical customer |
| `MEMORY` | `./archive.jsonl` |
| `BUDGET` | 12 rounds, 45 minutes; tokens as your host reports them |
| held-out | three judges plus three spares, written by the PM lead and stored outside the repo |

```json
{
  "criteria": [
    {"id": "problem-evidence", "required": true, "kind": "source", "test": "the problem is backed by >=3 tickets from the export"},
    {"id": "scope-cut", "required": true, "kind": "judges", "test": "exactly one user + one job; no 'and also'"},
    {"id": "success-metric", "required": true, "kind": "source", "test": "one success metric with a real baseline + target"},
    {"id": "feasibility", "required": true, "kind": "judges", "test": "build risk stated as <= medium with a reason"},
    {"id": "non-goals", "required": true, "kind": "command", "command": "grep -A2 '^## Non-goals' spec.md", "test": "a Non-goals heading exists"},
    {"id": "competitor-price", "required": false, "kind": "source", "test": "competitor pricing, if public"}
  ],
  "must_not_change": {"same-problem": "the underlying user problem", "brief": "the product brief's constraints"},
  "final_rung": "E2"
}
```

## Setup

`v0` is drafted from the brief. **Probe:** judge 1 ties `v0` with an identical copy in both orders and
prefers `v0` over a copy the orchestrator seeded with a second job; a Check judge fails the seeded copy
on `scope-cut`. No miss: normal mode.

## Rounds 1–4 — E1 (fair-critical)

- **Round 1.** Variant A adds a Non-goals section (failing commands first); B cuts the scope to one job.
  The `non-goals` command passes on A and fails on B and *best*: a shared failure, not a rejection.
  Judges 1 and 2 prefer each variant, so judge 3 is skipped; the tie-break keeps the shorter, **B**.
- **Round 2.** A, never rejected, is re-proposed and **kept**. Variant C (a nicer intro) gets ties from
  judges 1 and 2, so judge 3 runs and ties; C is not kept.
- **Round 3.** Variant D adds "engagement +20% from a 35% baseline". The Verifier finds no source, so
  the baseline becomes `[OPEN: real 30-day baseline from analytics]`, a required gap. Judges prefer D;
  **kept**.
- **Round 4.** A variant cites three tickets the Verifier finds; **kept**. The orchestrator believes
  `DONE` holds, so it runs a **Check** on v4: `non-goals` passes by command, `problem-evidence` by
  source, `scope-cut` and `feasibility` by 3 fresh judges each. `success-metric` fails (its baseline is
  `[OPEN]`); `competitor-price` fails, but it is optional.

## Rounds 5–7 — nothing more to gain

- **Round 5.** A variant swaps the `[OPEN]` for an "industry-typical" baseline; the Verifier finds no
  source and the Screen rejects the unevidenced `[OPEN]` removal.
- **Round 6.** Judge 1's two orders disagree (UNKNOWN), judge 2 ties, judge 3 prefers *best*: not kept.
- **Round 7.** One diff will not apply (ERROR, retried once, then dropped); the other ties. Not every
  variant ended ERROR, so this is still a stall.

*Best* is still v4, so the round-4 Check stands: `success-metric` fails after 3 stalls →
**HALT(STALL)**, naming what it needs: a source.

## Output

- *Best* = v4, **PARTIAL** at E1. `problem-evidence` pass (source); `scope-cut`, `feasibility` pass
  (judges, one model family = one source); `non-goals` pass (command); `success-metric` fail (needs a
  source); `competitor-price` fail (optional). 7 rounds, minutes as recorded, tokens `null` unless
  reported; not audited by `rqgm_check.py`.
- **One next action:** pull the real 30-day baseline from analytics. Then the loop re-checks, you decide
  on E2, and your held-out judges finish it.

The loop refused to turn a made-up number into a win.
