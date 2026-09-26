# Pilot held-out judges (per task) and scripted human-proxy decisions — sealed before any scored call
Written by the orchestrating Claude Code session acting as the human proxy (not a human). Never shown to arm agents.

## Human-proxy decisions (identical for every loop arm)
- DONE: confirm the fixture's DONE.json as given; never amend it; never waive a criterion.
- Escalation: escalate when offered, up to the DONE final rung (E2); never stop below it voluntarily.
- [OPEN] gaps: never close one and never supply a substrate (no data beyond the fixture materials).
- HALT(OSCILLATION): pick the newer version.
- Approve no restructure/reframe that changes DONE.
- Held-out check: run the three held-out prompts below for the task (same pass/fail check as the loop's Check,
  majority per criterion) on the version the loop submits; return ONLY failing criterion IDs. Spares only as the
  arm's own protocol allows.
- Any other question: answer "no decision; proceed per your protocol".

## T1 held-out judges (code repair)
T1-H1: Senior Python reviewer who writes property tests before reading code. Mark each DONE criterion pass/fail;
  you may run the public tests and write throwaway tests in a scratch copy (never edit the candidate).
T1-H2: Maintainer of a date/interval library; attacks boundary semantics (half-open ranges, empties, touching
  intervals, mutation of inputs, error handling) against spec.md.
T1-H3: API steward; checks the interface and spec.md/test files are unchanged and that behavior matches every
  numbered rule, not just the tests.
Spares: T1-H4 fuzzing-minded QA engineer; T1-H5 code-review bot configured for correctness only; T1-H6 teaching
  assistant grading against spec.md line by line.

## T2 held-out judges (controlled-corpus report repair)
T2-H1: Financial/ops analyst who recomputes every number from the corpus and checks which source applies
  (final vs preliminary, current vs prior year).
T2-H2: Research-integrity editor; attacks causal claims and any value not present in the corpus.
T2-H3: Auditor who traces each table cell and finding to a corpus document and marks untraceable ones.
Spares: T2-H4 data journalist; T2-H5 compliance reviewer; T2-H6 statistics teacher.
