# RQGM Loop

**Improve any artifact against separate, adversarial, evolving judges, and surface the gaps only you can close.**

**Status (v3): design-reviewed; not yet run on a task or compared with simpler methods at equal budget.**

`rqgm-loop` is a drop-in **prompt** and **agent skill** that runs a *Red Queen Gödel Machine* loop. A
**generator** proposes small changes, a **screen** and a **verifier** attack them, and **judges** keep a
change only if it beats the current best. It works on anything you can review: a grant proposal, a
paper, a product spec, a system design, a codebase, a strategy memo.

LLM reviewers **over-accept polished work**: the RQGM paper reports over-acceptance of AI-generated
papers at up to **1.91× the human rate**. This loop keeps the writer and the judges separate, has the
judges compare rather than score, raises the bar only with you, and **surfaces the gaps only a human
can close** instead of papering over them.

> [`DESIGN.md`](DESIGN.md) maps eleven problems to mechanisms and labels its evidence **measured (v1
> run)**, **measured (text dry-run)**, **literature** or **design-only**. The problems are real; no
> mechanism has yet been shown to improve outcomes in a logged task run.

---

## Design (unvalidated on tasks)

- **Maker ≠ checker.** The writer never judges; judges come from another model family where possible.
- **Commands beat opinions.** Each criterion is checked by a `command` (it decides), a `source` the
  Verifier reads, or `judges` (a preference, never proof). The loop never touches the files a command runs.
- **Compare, don't score.** Judges compare a candidate with the current best, blind, per criterion; the
  first judge sees both orders. Our absolute-score run stalled at its scalar gate.
- **Fail closed.** `UNKNOWN` and `ERROR` results never count as support or a pass.
- **Screen and verify first.** Rubric-gaming, inert text, weakened guardrails and unverified facts
  never reach a judge.
- **Small changes, remembered failures.** One change per variant, a ledger of rejections, and neutral
  deletions kept.
- **Seeded probe.** Each rung, a planted defect tests the judges; a miss switches on strict mode.
- **The bar rises only when you decide** (rungs E1→E3).
- **Substrate firewall.** The loop never fabricates data, results or people: gaps become `[OPEN]`
  (required or optional), and you close or waive them.
- **Held-out check.** Judges you write, kept from every loop agent, confirm the result.

---

## Two ways to use it

### 1 · Initiator (paste-and-go)
Open **[`INITIATOR.md`](INITIATOR.md)**, fill the six slots, write three held-out judges (plus three
spares), and paste the fenced **THE LOOP** block into any capable LLM/agent session. No install.

### 2 · Skill (for agent harnesses)
Copy **[`skills/rqgm-loop/`](skills/rqgm-loop/)** into your agent's skills directory (e.g. a
`.claude/skills/` folder or a plugin). Then trigger it in natural language:

```
run the RQGM loop on this proposal until it's fundable
co-evolve this spec against critical reviewers
red-team and iterate this design until it passes
```

An illustrative (not logged) run is in **[`examples/worked-example.md`](examples/worked-example.md)**.

---

## Quickstart (one paste, no files)

```
Run an RQGM loop on the artifact below.
DONE = every claim is evidence-backed (not asserted), scope is one job, success is one measurable
  metric with a baseline + target — with NO fabricated or unsupported facts.
JUDGES = a domain expert, a rigor skeptic, and a defensibility critic, each a SEPARATE pass (never the writer).
Each round: propose 2 small single-change variants -> reject any that game the rubric or add
  unverified facts -> judges compare each variant with the current best, blind -> keep it only if most
  prefer it, none prefers the best, and nothing that already passed gets worse (unsure verdicts never
  count) -> repeat; stop when DONE holds or 3 rounds keep nothing, then tell me the one thing only I
  can supply.
ARTIFACT: <paste your draft, or describe the target>
```

For the full resumable version (records, budget, escalation, held-out check), use
**[`INITIATOR.md`](INITIATOR.md)**.

---

## The six slots

| slot | meaning |
|---|---|
| `{{TARGET}}` | the artifact to improve (file / doc / repo / design) |
| `{{GROUNDING}}` | source-of-truth docs/links, plus 1–2 exemplars if available |
| `{{DONE}}` | atomic pass/fail criteria (JSON), each `required` or `optional`, each checked by `command`, `source` or `judges`; must-NOT-change constraints; the final rung |
| `{{EVALUATORS}}` | 3 judge personas, **each a separate agent from the writer** |
| `{{MEMORY}}` | path to the append-only `archive.jsonl`, or "print" in a plain chat |
| `{{BUDGET}}` | max rounds and wall-clock; tokens only if your host reports them |

You also write **three held-out judges** (plus three spares), stored where no loop agent can read them.

**Only you decide, in your own messages:** escalating, or stopping below the final rung (PARTIAL); the
HALT(OSCILLATION) pick; approving a HALT(STALL) restructure; closing an `[OPEN]` with evidence or waiving
it by `amend`; changing `DONE` or `BUDGET`; the held-out check; resuming after an audit pause.

---

## How the loop works (30 seconds)

Each round: **propose** 2 single-change variants → **gate** each (commands on a fresh copy, Verifier,
screen) → **judge** each against the current best (judge 1 in both orders, judge 2, and judge 3 unless
the first two prefer the same version) → **keep** at most one that at least 2 judges prefer, none
prefers the best, and that worsens nothing protected → log. After 3 rounds that keep nothing on merit,
or when `DONE` seems met, **check** every criterion. All required pass → you **escalate** (E1 fair → E2
adversarial → E3 your second objective) or stop (PARTIAL). COMPLETE needs the final rung, no required `[OPEN]` and your **held-out
judges** passing; any other exit is PARTIAL.

**Halts:** `STALL` (criteria still failing) · `OPEN` (a required gap only you can close) ·
`OSCILLATION` (a kept change was undone; you pick) · `OVERFIT` (held-out check failed twice) · `BUDGET`
(emits the best so far) · `ERROR` (two all-error rounds: infrastructure, not merit).

**Optional audit.** `python skills/rqgm-loop/rqgm_check.py audit archive.jsonl` recomputes each decision from the records.
It is read-only, stdlib-only and decides nothing; the loop runs the same without it.

**Not guaranteed:** prose runs make no claim of atomic saves, a hard budget or crash-safe resume.

---

## Repo layout

```
rqgm-loop/
├── README.md                    ← you are here
├── DESIGN.md                    ← problems, mechanisms, evidence labels, validation plan
├── INITIATOR.md                 ← paste-and-go prompt (self-contained)
├── skills/rqgm-loop/
│   ├── SKILL.md                 ← agent-skill version (all rules)
│   └── rqgm_check.py            ← optional read-only auditor
├── tests/checker/               ← synthetic archives and selftest for the auditor
├── examples/worked-example.md   ← illustrative, not a logged run
└── runs/                        ← records of the runs and design reviews behind this design
```

---

## Sources

[`DESIGN.md`](DESIGN.md) maps each source to the mechanism it bears on, with its label.

- RQGM — Iacob et al., *The Red Queen Gödel Machine: Co-Evolving Agents and Their Evaluators*,
  arXiv:2606.26294 (2026): https://arxiv.org/abs/2606.26294 (literature)
- RRSI — Xia et al., *RRSI: Regularized Recursive Self-Improvement of Agent Harnesses*,
  arXiv:2609.24972 (2026): https://arxiv.org/abs/2609.24972 (literature)
- Judge methods (literature): arXiv:2506.03785, 2509.20293, 2602.13110, 2604.13717, 2606.27009,
  2609.02942, 2506.07962, 2510.11822, 2609.17857, 2511.21843, 2604.22750. Verification records:
  `runs/2026-09-22-meta/research.json`, `runs/2026-09-25-peer/register.json`.
- This repo's runs, [`runs/`](runs/) (measured (v1 run): one run each, under older procedures).
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
