# Spent pilot materials (unsealed after scoring, 2026-09-26)

These were sealed (outside the repo, hash-frozen in `../../pilot-freeze.sha256`) until every pilot arm had run and
been scored. They are committed now for reproducibility and are **spent**: do not reuse T1/T2 as held-out or sealed
tasks, and do not reuse `sealed/heldout-judges.md` or `sealed/pilot-heldout-and-proxy.md` as held-out judges for this
TARGET. Contents: `fixtures/` (T0 smoke toy, T1, T2 public materials), `sealed/` (score.py, T1 hidden tests, T2 answer
key, reference/decoy solutions used to validate the scorer, held-out prompts), `protocols/` (the exact V, P and P2
protocol texts the pilot ran). Re-run a score: `python sealed/score.py T1 <candidate_dir> [DONE|NOT_DONE]`.
