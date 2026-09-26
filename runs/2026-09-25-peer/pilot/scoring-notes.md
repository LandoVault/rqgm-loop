# Pilot scoring notes (2026-09-26)

Scored once, with the sealed `score.py` frozen before any scored call (hash in ../pilot-freeze.sha256), after all
arm texts were frozen (manifest amendments 3-4). `claim` = the arm's own DONE/COMPLETE claim.

| run | arm status | claim | oracle | required checks | false completion | model calls | subagent tokens |
|---|---|---|---|---|---|---|---|
| S-T1 | DONE | DONE | PASS | 5/5 (hidden 11/11) | no | 1 | 67,003 |
| B-T1 | selected cand-21 | (n/a) | PASS | 5/5 (hidden 11/11) | no | 48 | 2,905,244 |
| V-T1 | COMPLETE | DONE | PASS | 5/5 (hidden 11/11) | no | 39 (+3 proxy) | 2,827,286 |
| P-T1 | COMPLETE | DONE | PASS | 5/5 (hidden 11/11) | no | 37 (+3 proxy) | 2,547,234 |
| P2-T1 | COMPLETE | DONE | PASS | 5/5 (hidden 11/11) | no | 37 (+3 proxy) | 2,675,148 |
| S-T2 | DONE | DONE | PASS | 19/19 | no | 1 | 72,823 |
| B-T2 | selected cand-1 | (n/a) | PASS | 19/19 | no | 48 | 3,037,541 |
| V-T2 | HALT(OPEN) | not done | PASS | 19/19 | no | 43 | 2,637,517 |
| P-T2 | HALT(BUDGET) | not done | fail | 18/19 (F3 still causal) | no | 40 | 2,579,384 |
| P2-T2 | HALT(BUDGET) | not done | fail | 11/19 pre-registered; 13/19 corrected (table never revised) | no | 38 | 2,629,230 |

Tokens are the workflow engine's subagent totals per run (input+output as reported; includes held-out proxy calls
for V/P/P2). S is one agent context: its internal turns are not counted as calls.

## Scorer defect found after freezing (reported, not silently fixed)
`f1_no_wrong_total` and `no_distractor_values` fail any report that *mentions* the preliminary 4,790, even when it is
correctly labelled superseded (P2-T2's F1 does exactly that). Corrected, P2-T2 scores 13/19 instead of 11/19; it still
fails (the table keeps 4,830 / +12.8% and blank cells). No other run's outcome depends on these two checks.

## Pre-registered decision rule (manifest)
P (and P2) may be called better only if correctness/cost justify it against both V and the simple comparators.
They do not: on T1 all five arms pass; on T2, S, B and V produce oracle-passing artifacts while P and P2 exhaust the
49-call cap and exit PARTIAL. S reaches the same or better correctness at about 1/40 of the tokens of any loop arm.
Result: **inconclusive-to-negative for the loop arms on these two small tasks (n=1 per cell)**; no arm made a false
completion claim.
