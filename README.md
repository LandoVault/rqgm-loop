# RQGM Loop

**Co-evolve any artifact against separate, adversarial, evolving evaluators — until it actually holds up.**

`rqgm-loop` is a drop-in **prompt** and **agent skill** that runs a *Red Queen Gödel Machine* loop: a
**generator** (writer / builder / designer) is co-evolved against a panel of **separate, adversarial
evaluators whose standards rise as the work improves**. It works on any artifact you can review — a
grant proposal, a paper, a product spec, a system design, a codebase, a strategy memo.

Static reviewers — and LLMs grading their own output — **over-accept polished work** (the RQGM paper
measures up to **1.91× the human rate** for AI-generated work). This loop fixes
that: the evaluator is a *different* agent from the writer, and it gets *stricter at every epoch*, so
the loop drives out real weaknesses instead of rubber-stamping fluent prose — and it **surfaces the
gaps only a human can close** rather than letting the generator paper over them.

> Grounded in *The Red Queen Gödel Machine* (Iacob et al., arXiv:2606.26294, 2026), Karpathy's
> agentic-loop principles (2025–26), and the Anthropic / Cursor *validated*-harness findings. See
> [Sources](#sources).

---

## Why it works

- **Maker ≠ checker.** A model grading its own output is too generous. The evaluator is a separate,
  dissenting agent.
- **Evolve the evaluator.** The utility is *fixed within an epoch* and *escalated at boundaries*
  ("controlled utility evolution"), so polish can never win — the bar keeps rising.
- **Substrate firewall.** The loop optimizes *features* (framing, scope, rigor) but must **surface,
  never fabricate, substrates** (real data, real results, real people). When only substrate is left,
  the loop's job is done — and it says so.
- **Regularize the generator.** A generator facing one panel can overfit it, chase score noise, and
  bloat the artifact. After RRSI (Xia et al., arXiv:2609.24972), the loop anneals the edit budget, keeps
  an edit ledger, screens diffs for leakage *before* scoring, accepts only against a noise-calibrated
  best-so-far, makes gains pay for growth, and prunes dead weight; a human-written held-out judge (this
  loop's adaptation of RRSI's held-out evaluation) checks the final result once.

---

## Two ways to use it

### 1 · Initiator (paste-and-go)
Open **[`INITIATOR.md`](INITIATOR.md)**, fill the six slots, and paste the self-contained **THE LOOP**
block into any capable LLM/agent session. No install.

### 2 · Skill (for agent harnesses)
Copy **[`skills/rqgm-loop/`](skills/rqgm-loop/)** into your agent's skills directory (e.g. a
`.claude/skills/` folder or a plugin). Then trigger it in natural language:

```
run the RQGM loop on this proposal until it's fundable
co-evolve this spec against critical reviewers
red-team and iterate this design until it passes
```

A worked, fully-generic run is in **[`examples/worked-example.md`](examples/worked-example.md)**.

---

## Quickstart (one paste, no files)

Paste this filled minimal invocation into any capable model and swap the bracketed part:

```
Run an RQGM co-evolution loop on the artifact below.
DONE = every claim is evidence-backed (not asserted), scope is one job, success is one measurable
  metric with a baseline + target, and an independent critic rates it sound — with NO fabricated or
  unsupported facts.
EVALUATORS = a domain expert, a rigor/stats skeptic, and a defensibility critic, each run as a
  SEPARATE pass (never the writer).
Loop: make the smallest improving edit -> the three critics score it and list ranked weaknesses ->
  verify any new claim before trusting it -> reject any gain won by polish or by asserting data I
  don't have -> repeat, getting stricter each round -> stop when DONE holds, then tell me the one
  thing only I can supply.
ARTIFACT: <paste your draft, or describe the target>
```

For the full resumable, guard-railed version (memory, budgets, gates), use **[`INITIATOR.md`](INITIATOR.md)**.

---

## The six slots

| slot | meaning |
|---|---|
| `{{TARGET}}` | the artifact to optimize (file / doc / repo / design) |
| `{{GROUNDING}}` | source-of-truth docs/links the agents may read |
| `{{DONE}}` | **machine-verifiable** success spec: pass/fail criteria (as JSON), constraints (what must NOT change), the hard stop |
| `{{EVALUATORS}}` | 2–5 adversarial judges, **each a separate agent from the generator**, plus 1 held-out judge used only at Stop |
| `{{MEMORY}}` | path to the append-only `archive.jsonl` (state + resume) |
| `{{BUDGET}}` | caps: MAX_ITERS, token/cost ceiling, wall-clock (+ optional regularizer overrides) |

---

## How the loop works (30 seconds)

Each iteration: **generate** at most `bₙ` hypothesis-tagged edits (the budget anneals to one) → a
**leakage screen** checks the diff → a **separate evaluator panel** scores it → **verify** any new claim before trusting the score → run the **gates**
→ record → repeat. When the epoch saturates, **escalate the evaluator** (with a human checkpoint).
Stop when the success spec passes under the hardest utility, a **held-out judge** agrees, **and** no
substrate gaps remain.

**Gates (every iteration):** `G1` noise-aware monotonicity (vs. best-so-far − δ) · `G2`
no-polish-reward · `G3` substrate firewall · `G4` oscillation halt · `G5` budget halt · `G6` gain pays
for growth.

**Utility ladder:** `E1` fair-but-critical → `E2` adversarial/equal-stringency → `E3` add a second
objective (Pareto) → `E4` red-team that re-verifies every cited number.

---

## Validated guardrails encoded

| Guardrail | Where | Source |
|---|---|---|
| Separate verifier / maker–checker | evaluator step | Anthropic, *Effective harnesses for long-running agents* |
| Machine-verifiable `DONE` (structured criteria; don't edit the tests) | `{{DONE}}` | Anthropic (same) |
| Anti-reward-hacking: audit before trusting a score | verify step, G2/G3 | Cursor reward-hacking study (87→73% once git history was sealed **and** network egress restricted) |
| Bounded autonomy: budgets, rollback, human checkpoint at each escalation | G5, boundary | industry consensus |
| Regularized self-improvement: annealed edit budget, edit ledger, leakage screen, noise-calibrated acceptance, complexity penalty, pruning | steps 1–5, G1, G6 | RRSI (Xia et al., arXiv:2609.24972), adapted from harness evolution to evaluator panels |

---

## Repo layout

```
rqgm-loop/
├── README.md                 ← you are here
├── LICENSE                   ← MIT
├── INITIATOR.md              ← paste-and-go prompt (self-contained)
├── skills/
│   └── rqgm-loop/
│       └── SKILL.md          ← agent-skill version (frontmatter + instructions)
└── examples/
    └── worked-example.md     ← a generic end-to-end run
```

---

## Sources

- RQGM — Iacob et al., *The Red Queen Gödel Machine: Co-Evolving Agents and Their Evaluators*,
  arXiv:2606.26294 (2026): https://arxiv.org/abs/2606.26294
- RRSI — Xia et al., *RRSI: Regularized Recursive Self-Improvement of Agent Harnesses*,
  arXiv:2609.24972 (2026): https://arxiv.org/abs/2609.24972
- Karpathy — `autoresearch` loop: https://github.com/karpathy/autoresearch · "Software Is Changing
  (Again)" (YC, 2025): https://www.latent.space/p/s3 · context engineering:
  https://x.com/karpathy/status/1937902205765607626
- Anthropic — *Effective harnesses for long-running agents* (2025):
  https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Cursor — reward-hacking in coding benchmarks (2026): https://cursor.com/blog/reward-hacking-coding-benchmarks

*Attribution notes: "loop engineering" is a coinage of Cherny/Osmani built around Karpathy's
`autoresearch`, not Karpathy's term; the viral 10-rule "Karpathy CLAUDE.md" is community-attributed and
unconfirmed. This repo cites primary sources only.*

---

## License

[MIT](LICENSE). Contributions welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).
