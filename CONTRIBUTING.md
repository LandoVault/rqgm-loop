# Contributing to RQGM Loop

Thanks for your interest. This repo is a small, focused prompt + skill — contributions should keep it
that way.

## Ground rules (they mirror the loop itself)
- **Smallest useful change.** One idea per PR; keep diffs reviewable.
- **Cite, don't assert.** Any new factual claim (a statistic, a paper, a guardrail) needs a primary
  source in the PR description. Unsourced numbers will be asked to be cut or cited.
- **Keep it domain-agnostic.** `INITIATOR.md` and `SKILL.md` must stay generic; put anything
  domain-specific in `examples/`.
- **Don't weaken the guardrails.** Changes that remove the maker/checker separation, the substrate
  firewall, or the gates need a strong, sourced rationale.

## How to propose a change
1. Open an issue describing the problem and the proposed fix.
2. For prose/spec edits, run the loop on your own change: have a separate model red-team it against the
   bar in the README before opening the PR.
3. Submit a PR; keep `README.md`, `INITIATOR.md`, and `skills/rqgm-loop/SKILL.md` consistent if you
   touch the loop logic.

## What's especially welcome
- New `examples/` for fresh domains (paper, RFC, threat model, dataset card…).
- Adapters for specific agent harnesses (how to wire the subagent/evaluator step).
- Better, sourced guardrails from the latest agentic-loop literature.

By contributing you agree your work is released under the repo's [MIT license](LICENSE).
