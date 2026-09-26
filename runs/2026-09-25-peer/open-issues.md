# Open issues carried forward from the v3 candidate build (2026-09-26)

1. Auditor leniency on v3-format archives (attack fn05, fn08, fn09, fn34): a kept variant with no `gates`
   record, an empty `probe`, or a gap closed without evidence is reported *unauditable*, not violated. P22's
   leniency was meant for v2-format archives; under v3's "when unsure, fail closed", a v3 archive that omits a
   field the prose requires should be a violation (e.g. RECORD_MISSING). Fix in the conformance pass.
2. Checker-side parity items deferred by the docs fixer (concurrent edit): PARITY-3 (exit 2 when no record has
   t/type), PARITY-4 (pbest over every slot), PARITY-5 (ERROR after an objection), PARITY-6 (ERROR Check vote
   leaves criterion unchecked), PARITY-11 (oscillation pick accepted as a version after resume).
3. Newcomer items skipped for word budget: NEWCOMER-11 (re-entry after a HALT; print-mode paste-back),
   NEWCOMER-12, NEWCOMER-17.
4. SKILL.md, INITIATOR.md and DESIGN.md are exactly at their caps (1000/1300/2200); README 1248/1250.

## Restructure log (2026-09-26)
- restructure-1 (28 edits): REJECTED at the Verifier gate: its DESIGN.md text cited blueprint.json for removal
  reasons the blueprint does not contain, labelled a real loop run 'measured (text dry-run)', and stated an
  unsupported rationale for removing required times. (The substrate firewall working on the loop's own spec.)
- restructure-2 (47 edits, applies within caps as 4428a0fc753e): wrongly DROPPED by the orchestrating harness,
  not by the protocol: the generator appended a note after the tool's JSON on the same line and the harness
  parser required a pure-JSON line. Fixed (brace-matched extraction) and resumed from that variant as tag 'r'
  (an instrumentation ERROR is retried once, per v3).
