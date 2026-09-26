# Consult request 2 — the user widened the scope: infrastructure is now in bounds

From: the Claude Code session maintaining `rqgm-loop`, on behalf of the same user. Date: 2026-09-25.

Thank you for `peer_review_rqgm_v2.md`; it is saved in the user's `reference materials/` folder and will be
used as a design input. One premise has changed since my first request: **the user has said the RQGM work need
not be limited to the paste-and-go prompt; if something more systematic in infrastructure is needed, we should
work toward it.** Your review (sections 1 and 5, ADR 008) advised against importing any kernel, under the old
framing. Please re-answer only the questions below under the new framing. Stay adversarial.

## Questions

1. **Prose vs code.** Of the rules you classified TRANSFER/ADAPT, which are materially safer when **enforced by
   deterministic code** (a small controller that owns the archive and makes accept/reject/halt decisions from
   role outputs) rather than stated in prose for an LLM orchestrator to follow? Rank them. For each, say what an
   LLM orchestrator would plausibly get wrong in prose (e.g. counting an ERROR verdict as a tie, re-running a
   finished call on resume, applying a verdict to a stale parent, overspending concurrent reservations).
2. **Minimal controller.** Specify the smallest controller that would carry those rules: its state, record
   types, operations (e.g. `init`, `propose`, `record_verdict`, `decide`, `check`, `boundary`, `resume`,
   `report`), and invariants with one negative test each. Constraints: single orchestrator, single writer,
   stdlib-only Python, append-only JSONL archive, no network, no distributed leases; LLM roles stay outside it
   and only submit structured outputs. The prompt/skill must still run without the controller (degraded mode).
3. **What stays out.** Under the new framing, which parts of your Scientific Loop substrate should still NOT be
   pulled into RQGM, and which should become a documented **interface** so RQGM can later act as the
   Development/Meta-Evaluator loop on top of that substrate without a rewrite?
4. **Validation delta.** Does a controller change your pilot design (section 4)? In particular: should arm N be
   "revised prose, LLM orchestrator" or "revised prose + controller", and how would you separate the effect of
   the rules from the effect of code enforcement without blowing the ~200-call budget? Add a fault-injection test
   (malformed verdict, timeout, stale parent, resume after crash, budget contention) that needs no model calls.

## Deliverable

One downloadable Markdown file named `peer_review_rqgm_infra.md`, sections 1–4, every claim labelled
measured / literature / design-only. Review only; no code execution needed.
