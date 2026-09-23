# RQGM Loop

**Improve any artifact against separate, adversarial, evolving judges — until it actually holds up.**

`rqgm-loop` is a drop-in **prompt** and **agent skill** that runs a *Red Queen Gödel Machine* loop. A
**generator** proposes small changes, a **screen** and a **verifier** attack them, and **judges** keep a
change only if it beats the current best. Their bar rises as the work improves. It works on anything
you can review: a grant proposal, a paper, a product spec, a system design, a codebase, a strategy memo.

Static reviewers, and LLMs grading their own output, **over-accept polished work**. The RQGM paper
measures up to **1.91× the human rate** for AI-generated papers. This loop keeps the writer and the judges separate,
makes the judges compare rather than score, raises the bar only with you, and **surfaces the gaps only a
human can close** instead of papering over them.

> Every mechanism answers one of ten problems that any judge-driven loop has, and each is backed by
> evidence from papers or from this repo's own runs. See **[`DESIGN.md`](DESIGN.md)**.

---

## Why it works

- **Maker ≠ checker.** The writer never judges its own work.
- **Compare, don't score.** Judges compare a candidate with the current best, blind and with the order
  swapped, per criterion. Our absolute-score run stalled on judge noise; the pairwise run did not.
- **Screen and verify before judging.** Rubric-gaming, inert text, weakened guardrails and unverified
  facts are rejected before any judge sees them.
- **Small changes, remembered failures.** One change per variant, with a ledger of what was rejected.
  Ties go to the shorter version, so dead weight gets pruned.
- **The bar rises, with you.** Rungs E1→E4 escalate only at a human checkpoint.
- **Substrate firewall.** The loop improves *features* but never fabricates *substrates* (real data,
  results, people). Gaps become `[OPEN]`, and you close them.
- **Held-out check.** Judges you write, which the loop never sees, confirm the result.

---

## Two ways to use it

### 1 · Initiator (paste-and-go)
Open **[`INITIATOR.md`](INITIATOR.md)**, fill the six slots, write three held-out judges, and paste the
self-contained **THE LOOP** block into any capable LLM/agent session. No install.

### 2 · Skill (for agent harnesses)
Copy **[`skills/rqgm-loop/`](skills/rqgm-loop/)** into your agent's skills directory (e.g. a
`.claude/skills/` folder or a plugin). Then trigger it in natural language:

```
run the RQGM loop on this proposal until it's fundable
co-evolve this spec against critical reviewers
red-team and iterate this design until it passes
```

A worked, fully generic run is in **[`examples/worked-example.md`](examples/worked-example.md)**.

---

## Quickstart (one paste, no files)

```
Run an RQGM loop on the artifact below.
DONE = every claim is evidence-backed (not asserted), scope is one job, success is one measurable
  metric with a baseline + target — with NO fabricated or unsupported facts.
JUDGES = a domain expert, a rigor skeptic, and a defensibility critic, each a SEPARATE pass (never the writer).
Each round: propose 2 small single-change variants -> reject any that game the rubric or add
  unverified facts -> judges compare each variant with the current best, blind -> keep it only if most
  prefer it and nothing that already passed gets worse -> repeat; stop when DONE holds or 3 rounds keep
  nothing, then tell me the one thing only I can supply.
ARTIFACT: <paste your draft, or describe the target>
```

For the full resumable version (memory, budget, escalation, held-out check), use
**[`INITIATOR.md`](INITIATOR.md)**.

---

## The six slots

| slot | meaning |
|---|---|
| `{{TARGET}}` | the artifact to improve (file / doc / repo / design) |
| `{{GROUNDING}}` | source-of-truth docs/links, plus 1–2 exemplars of the target quality if available |
| `{{DONE}}` | atomic, non-overlapping pass/fail criteria (JSON), must-NOT-change constraints, the hard stop |
| `{{EVALUATORS}}` | 2–5 judge personas, **each a separate agent from the writer** |
| `{{MEMORY}}` | path to the append-only `archive.jsonl` (state + resume) |
| `{{BUDGET}}` | max rounds, token/cost ceiling, wall-clock |

You also write **three held-out judges**, which the loop never sees.

---

## How the loop works (30 seconds)

Each round: **propose** 2 single-change variants → **screen** and **verify** each → **judge** each
against the current best (one judge, a second if needed, a third on a split) → **keep** a winner only if
most judges prefer it and nothing protected gets worse → log. After 3 rounds with nothing kept, or when
`DONE` seems met, **check** every criterion (3 judges, majority). All pass → you decide whether to
**escalate** the bar (E1 fair → E2 adversarial → E3 your second objective → E4 red-team) or stop. Stop
needs every criterion passing, no `[OPEN]` gaps, and your **held-out judges** agreeing.

**Halts:** `STALL` (nothing kept and criteria still failing, so it tells you what only you can supply) ·
`OVERFIT` (held-out check failed twice) · `BUDGET` (emits the best version so far).

---

## Evidence behind the design

| Guardrail / mechanism | Source |
|---|---|
| Separate checker; structured `DONE`; don't edit the tests | Anthropic, *Effective harnesses for long-running agents* |
| Audit before trusting a score | Cursor reward-hacking study (87→73% once git history was sealed **and** network egress restricted) |
| Evolving, escalating evaluator | RQGM (Iacob et al., arXiv:2606.26294) |
| Leakage screen, small edits, complexity-aware acceptance, held-out check | RRSI (Xia et al., arXiv:2609.24972) |
| Pairwise comparison, per-criterion verdicts, escalate only when uncertain, early stop, bias probes | arXiv:2506.03785, 2509.20293, 2602.13110, 2604.13717, 2606.27009, 2609.02942 |
| All of the above, observed in practice | this repo's runs: [`runs/`](runs/) (absolute-score run vs pairwise meta-run) |

The full problem → mechanism → evidence table, and what was removed and why, are in [`DESIGN.md`](DESIGN.md).

---

## Repo layout

```
rqgm-loop/
├── README.md                 ← you are here
├── DESIGN.md                 ← first-principles design + evidence
├── INITIATOR.md              ← paste-and-go prompt (self-contained)
├── skills/rqgm-loop/SKILL.md ← agent-skill version
├── examples/worked-example.md
└── runs/                     ← archives and logs of the runs this design was derived from
```

---

## Sources

- RQGM — Iacob et al., *The Red Queen Gödel Machine: Co-Evolving Agents and Their Evaluators*,
  arXiv:2606.26294 (2026): https://arxiv.org/abs/2606.26294
- RRSI — Xia et al., *RRSI: Regularized Recursive Self-Improvement of Agent Harnesses*,
  arXiv:2609.24972 (2026): https://arxiv.org/abs/2609.24972
- The judge-methods papers listed above; verified abstracts are in `runs/2026-09-22-meta/research.json`.
- Anthropic — *Effective harnesses for long-running agents* (2025):
  https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Cursor — reward-hacking in coding benchmarks (2026): https://cursor.com/blog/reward-hacking-coding-benchmarks
- Karpathy — `autoresearch` loop: https://github.com/karpathy/autoresearch · context engineering:
  https://x.com/karpathy/status/1937902205765607626

*Attribution note: "loop engineering" is a coinage of Cherny/Osmani built around Karpathy's
`autoresearch`, not Karpathy's term. This repo cites primary sources only.*

---

## License

[MIT](LICENSE). Contributions welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).
