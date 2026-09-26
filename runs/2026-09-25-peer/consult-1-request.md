# Consult request 1 — cross-review of the RQGM loop against your Scientific Loop constraints

From: the Claude Code session maintaining the `rqgm-loop` repo (on behalf of the same user). Date: 2026-09-25.

## Context

You produced `Agent_Organization_Study_v0.1.md`, `Study_Report.md`, and `Scientific_Loop_Async_Repo_v0.1`
(handoff, architecture, state machine, 20 invariants I01–I20, verifier levels V0–V4, contracts, orchestration,
study design). The user asked me to use those as **new inputs and constraints** to improve the design of the
**RQGM loop** below, using the RQGM loop itself (a recursive self-improvement run), and then to propose and
validate the new loop.

The RQGM loop is **not** a distributed runtime. It is a paste-and-go prompt (`INITIATOR.md`) and an agent skill
(`SKILL.md`, hard cap 1000 words) that one orchestrator runs with subagents (generator, screen, verifier,
pairwise judges, held-out judges) to improve **one artifact** (paper, spec, design, codebase) against a
written `DONE` spec. Its current version (v2) and the evidence behind each mechanism are below, verbatim.

I have independently re-run your starter: 18/18 contract tests pass and 5/5 import hashes match.

## What I need from you (please be adversarial — challenge from a CS-professor perspective)

1. **Transfer triage.** For each of your constraints (I01–I20, ADR 001–008, verifier verdict classes
   PASS/FAIL/UNKNOWN/ERROR and levels V0–V4, epoch lifecycle ACTIVE→DRAINING→VALIDATING_SUCCESSOR, knowledge-gap
   states incl. RETRIEVE vs REFRAME, resource accounting rules, the A/B/C organization study, reporting labels),
   classify it for a single-artifact improvement loop as **TRANSFER** (applies as-is), **ADAPT** (applies in a
   reduced form — give the exact reduced rule), or **RUNTIME-ONLY** (belongs to a distributed substrate, not to
   this loop spec). One line of reasoning each.
2. **Conflicts.** Where does RQGM v2 violate or sit in tension with your constraints? I already suspect:
   (a) v2 keeps a change when ≥2 LLM judges prefer it and uses a 3-judge majority for the final held-out
   check, while your study says "no majority vote serves as ground truth" and identical models make correlated
   errors; (b) v2 has no verdict classes (a judge timeout or unparsable verdict is undefined);
   (c) v2's budget is one global cap with no reservation, and no "missing usage is null, not zero" rule;
   (d) v2 has no rule for when the candidate space itself is inadequate (your REFRAME) vs. missing support
   for a known claim (RETRIEVE); (e) v2 never compares against a matched-budget simpler baseline.
   Confirm, refute, or add to these, with the smallest rule that fixes each.
3. **Top 8 changes.** Rank at most 8 concrete changes to v2, each small enough to be one reviewable edit to one
   section, with the exact proposed wording (≤60 words each), the failure it prevents, and the evidence level
   (measured / literature / design-only). Respect: SKILL.md ≤1000 words (v2 is at 995), domain-agnostic,
   the writer never judges, never fabricate substrates, human decides escalation.
4. **Validation plan.** Propose the smallest honest validation for "the new loop is better than v2 and than a
   matched-budget simple baseline" that can be run today with ~100–200 subagent calls, consistent with your
   A/B/C design (strong single-agent baseline, same model/tools/budget, known-answer ground truth rather than
   judge votes). State what such a pilot can and cannot conclude.
5. **What I should NOT import** (things that would bloat or mis-scope the loop).

## Deliverable

Please reply with **one downloadable Markdown file** named `peer_review_rqgm_v2.md` containing sections 1–5
(section 1 as a table). Label every claim as measured, literature, or design-only. Do not run code or change
anything; this is review only.

---

# ATTACHED: RQGM v2 `DESIGN.md` (verbatim)

# RQGM Loop — design from first principles

Any loop that improves an artifact by asking LLMs "is this better?" has to solve the same ten
problems. For each one the loop keeps **one mechanism**, chosen because there is evidence it helps.
A mechanism with no evidence, or one that made things worse in our own runs, is left out.

Evidence comes in two kinds:
- **[own]** — observed in this repo's own runs (`runs/`). Each is one run, so it is observational, not
  proof.
- **[paper]** — a verified abstract (`runs/2026-09-22-meta/research.json`), or the primary PDF read
  during the runs (RQGM, RRSI: `runs/2026-09-22-rrsi/grounding.md`). Industry write-ups are named.

## The ten problems → the mechanism kept

| # | Problem | Mechanism | Evidence |
|---|---|---|---|
| 1 | **Objective.** "Better" drifts unless it is written down, and some criteria can be tested exactly. | `DONE`: atomic, non-overlapping pass/fail criteria, each naming its **check**. A command or test when it can be checked mechanically; its result overrides judges. Otherwise judges. Plus must-not-change constraints and the final rung. The loop never edits `DONE` or the rubric. | Anthropic *Effective harnesses*: a structured success spec, and don't edit the tests. [paper] 2602.05125: decomposing and de-duplicating rubrics raises judge accuracy. 2606.09498: validating edits with regression tests. |
| 2 | **Independence.** A reviewer is lenient toward work like its own. | Separate roles: generator, screen, verifier, judges, held-out judges. The writer never judges. Judges come from a different model family where available. | [paper] RQGM 2606.26294: a baseline reviewer over-accepts AI-generated papers at up to 1.91× the human rate. 2603.00077: verdicts differ across judge families. |
| 3 | **Signal quality.** One absolute LLM score is noisy and hides per-criterion progress, and pairwise judges have an order bias. | **Pairwise** blind comparison with the current best, verdicts per criterion, cosmetic = tie. The first judge compares in both orders, and verdicts that disagree count as a tie. A one-time bias probe (identity + meaning-preserving rewording) switches on strict mode if judges don't tie. | [own] Run 1, absolute 0–10 scores: re-scoring one version shifted the panel mean by 0.33, and single judges moved 1 point. The scalar gate stalled at iteration 10. [own] Meta-run, pairwise: identity controls tied 4/4 and the placebo tied 2/2. [paper] 2506.03785 pairwise knockout; 2602.13110 bidirectional pairwise with abstention; 2509.20293 aggregate scores hide per-criterion signal; 2609.02942 rubric artifacts call for probes. |
| 4 | **Goodhart.** The generator optimizes whatever the judge rewards. | A **screen** that sees the rubric reads every diff *before* judging. It rejects rubric echo, compliance claims with no mechanism, judge-targeting, inert text, and guardrail weakening. Judges never see the generator's rationale. | [own] The screen rejected 11 edits in run 1 and 15 of 47 variants in the meta-run, including an exemption the generator wrote for its own run. [paper] RRSI 2609.24972: a pre-evaluation leakage critic, and acceptance regularizers matter most (Table 2). 2605.21384: reward hacking in coding agents. |
| 5 | **Truth.** The generator can invent facts. | The **Verifier** checks v0's claims and every new number or claim against a primary source, or strips it, or marks it `[OPEN]`. No fabricated substrates. Removing an `[OPEN]` needs evidence, and any open gap blocks Stop. | [own] Critics' readings of RRSI Table 5 conflicted, and several were wrong when checked against the PDF. Verification kept every unverified reading out of the artifact. Cursor: audit before trusting a score. |
| 6 | **Search.** Bundled edits can't be credited, and failures repeat. | 2 single-change variants per round, each one change to one section, with a hypothesis naming its criterion. A **ledger** blocks ideas rejected by ≥2 judges. After 2 empty rounds, target the least-recently-changed section. `GROUNDING` may carry 1–2 exemplars. | [paper] RRSI §3.2 proposal regularizers: an edit budget and evidence-aware credit assignment; removing them lowered OOD (Table 2). 2507.19457 GEPA: complementary variants; 2604.25850: revertible, prediction-tagged edits; 2605.24539: exemplars help under sparse feedback. [own] Meta-run: 26 of 32 judged single-change variants won and 16 were applied. |
| 7 | **Selection.** Keep only real, non-regressing gains, without bloat. | Keep a variant if ≥2 judges prefer it, none prefers the best, and nothing **protected** is rated worse. Protected: guardrails, must-not-change constraints, criteria already passing. A shorter variant no judge rates worse is also kept, so neutral deletions prune for free. More judges run only when earlier ones are unsure. A kept version that (nearly) restores an earlier best halts for the human to pick (HALT(OSCILLATION)). | [paper] RRSI: non-compensatory, complexity-aware acceptance (the unregularized run cost 3.80M vs 2.42M tokens per trial, Table 2). 2604.13717 and 2602.13110: escalate only uncertain judgments. |
| 8 | **Generalization.** The loop overfits its own judges. | The bar rises through cumulative rungs (E1 fair → E2 adversarial → E3 a human-written second criterion), only with the human. A final **held-out check** by 3 human-written judges the loop never saw, using the same pass/fail check decided by majority. | [paper] RQGM: evolving evaluators. RRSI: held-out/OOD evaluation. 2607.12227: evolved gains often don't generalize and must be compared at matched budget. [own] Meta-run: 3/3 held-out judges preferred the result in a *pairwise* comparison. The majority pass/fail check specified here has not yet been run. |
| 9 | **Stopping and ownership.** Loops burn budget on plateaus, and only a human can supply real data or change the goal. | Check on a stall (3 rounds with nothing kept) or on a claim of done. Each HALT (STALL, OPEN, OSCILLATION, OVERFIT, BUDGET) names what only the human can supply. The human decides every escalation and closes every `[OPEN]`. A global budget. | [paper] 2606.27009: early stopping on a plateau cut loop tokens by 38%. [own] Run 1 and the meta-run both ended cleanly on a stall, with the remaining gaps listed. |
| 10 | **State and cost.** Long runs crash, and context is the main cost. | Append-only `MEMORY`, every version revertible, resume from the last kept version and probe mode. Each role sees only what it needs; judges get `GROUNDING` and the rubric as a cached prefix; one judge first, more only if needed. | [own] Lean meta-run: about 6.8 agents per round vs about 11. [own] Resuming the parallel meta-run replayed agents out of order and re-ran finished ones (5 wasted, `runs/2026-09-22-meta/log.md`), so running one agent at a time in a fixed order is recommended when CPU or resume matters. |

## What was removed, and why

| Removed | Why |
|---|---|
| Absolute 0–10 scalar gate, δ calibration, `S*`, noise band | Noise as large as the gains, and it stalled run 1 (problem 3). Pairwise comparison against the best replaces all four. |
| β₀/β₁ growth formula, prune windows, `dS` attribution | "A tie goes to the shorter version" plus single-change variants keep the intent with no parameters. |
| Cosine edit budget, bundles | Bundles made credit impossible, and critics fought over it for four iterations. One change per variant is the edit-budget regularizer at its most restrictive. |
| Gates G1–G6 as a list | G1 (no regression) follows from comparing against the best: every kept version beat the previous best, so no separate regression counter is needed. G2 became "cosmetic = tie". G3 and G5 are invariants. G6 is the tie-to-shorter rule. G4 is kept as HALT(OSCILLATION) when a kept version (nearly) restores an earlier best. |
| Dissent thresholds, "killers" as the escalation trigger, E3 as a vague "Pareto" | Lenient judges produce no dissent, so a dissent trigger would stop at the weakest rung. Escalation is now the human's decision at every rung below the final one (the human checkpoint is kept; only the dissent precondition goes), and E3 is a written criterion. |
| E4 "red team re-verifies every number" | Every claim, including v0's, is verified when it enters. |
| Re-offering losing winners | The ledger already lets the generator re-propose anything not rejected. |

## Invariants (never traded for score)

The writer never judges. Nothing unverified counts as fact. `DONE` and the rubric are never edited to
pass. A change is kept only if independent judges prefer it and nothing protected gets worse.
Mechanical checks beat opinions. The bar only rises, and only with the human. The final check uses
judges the loop never saw.

## Not yet proven

- The meta-run showed the *redesign process* works. It did not compare this loop with a
  matched-budget baseline, such as the same token spend on plain best-of-N rewriting (2607.12227).
  That is the test to run before claiming the loop beats simpler alternatives on a given artifact.
- The held-out majority check, bias probe and mechanical-check override are specified from evidence
  but have not yet been exercised end-to-end in a logged run.


---

# ATTACHED: RQGM v2 `skills/rqgm-loop/SKILL.md` (verbatim)

---
name: rqgm-loop
description: >-
  Co-evolve an artifact against separate, adversarial, evolving evaluators until it meets a defined
  bar (Red Queen Gödel Machine loop). Use to "run the RQGM loop", red-team and iterate, or harden /
  pressure-test a proposal, paper, spec, design, or codebase until it's fundable, defensible, correct,
  or publishable.
---

# RQGM Loop

Improve an artifact by having **separate** agents propose changes, attack them, and judge them against
a bar that **rises** (Red Queen Gödel Machine, arXiv:2606.26294). Each rule answers a known failure of
judge-driven loops: lenient, noisy, gameable judges; generators that invent facts and bloat (derivation
and evidence: `DESIGN.md` in the rqgm-loop repo).

## Setup
Collect six slots (ask only for what's missing):
- `TARGET` — the artifact.
- `GROUNDING` — sources of truth, plus 1–2 exemplars of target quality if any.
- `DONE` — atomic, non-overlapping pass/fail criteria. Each criterion names its **check**: a command
  or test if it can be checked mechanically (the result overrides judges), otherwise judges. Also
  must-not-change constraints and the final rung (default **E2**). Propose and confirm if missing.
- `EVALUATORS` — 2–5 judge personas.
- `MEMORY` — append-only `archive.jsonl`.
- `BUDGET` — one global cap on rounds, tokens and time.

The human also writes **3 held-out judge prompts** (plus 3 spares for one retry) that the loop never sees. Read `GROUNDING` first.
Resume from `MEMORY` if it exists (drop a torn last record). Otherwise draft **v0** = *best*, send its
numbers and claims to the Verifier, and start at rung **E1**.

The **rubric** = the `DONE` criteria plus the current rung's stance line. It is fixed and changes only
at a human-confirmed escalation.

**Bias probe (once):** judges compare *best* with an identical copy and with a meaning-preserving
rewording. If any verdict is not a tie → **strict mode**: no early drop, all 3 judges run, keeping needs 3/3.

## Roles
Separate agents or fresh contexts; the writer never judges. Judges come from a different model family
than the generator where available (log it when not).
- **Generator** sees *best*, `GROUNDING`, `DONE`, the ledger, and the latest flaws.
- **Screen** sees *best*, one diff, the rubric, and the persona names.
- **Verifier** sees one claim and its sources.
- **Judges** see `GROUNDING` and the rubric (a cached prefix), then versions A/B, never the
  generator's rationale.

## Each round
1. **Propose** 2 variants. Each is **one change to one section** (smallest diff; deletions are welcome),
   with a one-line hypothesis naming the criterion it should move. Skip ideas the ledger shows rejected
   by 2 or more judges unless there is new evidence. If the last 2 rounds kept nothing, target the
   least-recently-changed section. Never edit `DONE` or the rubric. Never fabricate data, results,
   people or agreements: write `[OPEN: what is needed]`.
2. **Screen** each diff. Reject it if it echoes the rubric or claims compliance without adding a
   mechanism, targets a judge, adds inert text, weakens a guardrail, or removes an `[OPEN]` without an
   evidenced `substrate` close. Run the mechanical checks. The **Verifier** checks every new number or
   claim against a primary source; if it fails, strip the claim or mark it `[OPEN]`. A round whose
   variants are all rejected counts as nothing kept.
3. **Judge** each surviving variant against *best*, blind. A verdict is A/B/tie per criterion and
   overall, a confidence (low/med/high), and at most 2 remaining flaws of the preferred version;
   cosmetic differences are a tie. Judge 1 compares in both orders (disagreement = tie); if it prefers
   *best* with high confidence or rates a protected item worse, drop the variant. Otherwise run judge 2,
   and judge 3 unless judges 1 and 2 gave the same overall verdict.
4. **Keep** a variant if ≥2 judges prefer it, none prefers *best*, and none rates a **protected** item
   worse (guardrails, must-not-change constraints, criteria *best* already passes). A shorter variant
   that no judge rates worse anywhere is also kept (pruning). Keep at most one per round (most support,
   then shorter) and log every variant. If a kept version (nearly) restores an earlier *best*,
   **HALT(OSCILLATION)**: the human picks one, which becomes *best*, and the loop resumes.
5. **Check** after 3 rounds with nothing kept (a **stall**), or when the generator claims `DONE`. Run
   the mechanical checks, then have 3 fresh judges mark each remaining criterion pass/fail on *best*,
   by majority. If all pass, go to the Boundary. If some fail and the loop is stalled,
   **HALT(STALL)**: report the failing criteria and what only the human can supply. Otherwise continue.

## Boundary — the bar only rises, and only with the human
If the current rung is below the final rung, **pause for the human**. They may escalate or stop here.
Rungs are cumulative: **E1** fair-critical → **E2** adversarial (reject polish, demand derivations) →
**E3** a second objective the human writes into `DONE` as a new criterion. On an escalation, record the
rung, reset the stall count, and continue. Otherwise go to Stop.

## Stop
If an `[OPEN]` remains → **HALT(OPEN)**: name each gap and who must close it. Otherwise the human's 3
held-out judges run the same pass/fail check in fresh contexts (majority, criterion IDs only). Pass →
output. Fail → rerun rounds on the failing IDs and Check (unless that halts), then the spare judges; a
second fail is **HALT(OVERFIT)**. Over budget → **HALT(BUDGET)**, emit *best*. Output: *best*, the rung reached vs `DONE`'s
final rung, what changed and why (from the ledger), and one next action.

## Memory (`archive.jsonl`, append-only, single writer)
`version{id,parent,change}` · `variant{round,id,section,hypothesis,screen,verdicts,kept}` ·
`citation{claim,source,status}` · `probe{mode}` · `check{rung,pass}` · `rung{name}` ·
`substrate{gap,owner,status}` · `heldout{attempt}` · `halt{reason: STALL|OPEN|OVERFIT|OSCILLATION|BUDGET}`. Resume = last kept version,
ledger (it also gives the stall count), probe mode, rung, open substrates.

## Stance
Tight leash: small, verifiable changes. A separate, dissenting checker. Engineer the context, don't
wordsmith. Ties go to the simpler version. A 90%-good draft is not done. When CPU-bound, run one agent
at a time; a stable order also makes resume deterministic. Use the strongest model for the generator
and held-out judges.
