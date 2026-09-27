<!-- Provenance: reply from the peer ChatGPT conversation (GPT-6 Astra, https://chatgpt.com/c/6ab65a7f-facc-83ea-a714-3590b749ad8b) to consult-2-request.md, 2026-09-25. The in-page download did not complete, so this text was extracted from ChatGPT's file preview and its headings/tables re-marked-up by the Claude Code session; wording is unchanged. -->

# RQGM infrastructure peer review

[measured — document inspection] I read consult-2-request.md. It explicitly widens the scope to infrastructure and requests a review of a single-writer, offline, standard-library Python controller. The previous consultation supplied the v2 prompt and design, not an implemented controller. No implementation, fault suite, or pilot was executed for this review.

[design-only] The changed scope changes my recommendation: build a small controller for acceptance, accounting, and recovery. Do not copy the earlier reference kernel wholesale. Its interfaces and tests can inform the work, but it does not implement the complete persistence, trust, or recovery contracts needed here.

[design-only] Labels apply to the entire paragraph, list item, or table row. measured is explicitly scoped to inspected or attributed observations; literature would denote externally sourced results; design-only denotes proposed behavior, failure scenarios, and analysis without an executed validation. This review makes no literature-dependent effectiveness claim.

## 1. Prose versus deterministic enforcement

[design-only] Enforce rules about identities, versions, resources, completeness, and lifecycle in code. Keep judgments about scientific support, quality, novelty, and relevance with the appropriate verifier or human. The controller can ensure that the required verifier supplied a PASS for a particular artifact; it cannot establish that an LLM's PASS is scientifically correct.

| Rank | Rule and earlier invariant mapping | Plausible prose-only failure | Deterministic enforcement and its limit | Label |
|---|---|---|---|---|
| 1 | Gate completeness and fail-closed verdicts — I06, I12, I19 | Treat ERROR as tie; overlook a missing check; prune because nobody explicitly objected. | Validate typed results and require the exact gate set for the exact artifact. UNKNOWN/ERROR never satisfies a gate. This validates the protocol, not the truth of the verifier's answer. | design-only |
| 2 | Artifact, parent, rubric and evidence identity — I03, I09, I10 | Apply a verdict to a revised candidate or changed incumbent; retain a PASS after changing its premise. | Bind results to immutable hashes and scope versions. Changed dependencies invalidate eligibility. Default to full mandatory recheck when dependencies are incomplete. | design-only |
| 3 | Idempotent acceptance and crash recovery — I05, I11, I18 | Repeat a completed call after resume; accept the same candidate twice; recover best from a partial record. | Replay committed records, deduplicate IDs, and recognize only complete acceptance events referencing durable artifacts/checks. An unrecorded external completion remains uncertain, not safely retryable by assumption. | design-only |
| 4 | Resource admission and reconciliation — I08, I17 | Overspend by launching overlapping calls; forget screening/retries; treat missing usage as zero. | Serialize reservations against shared limits; retain outstanding liabilities and unknown usage; reserve final-check capacity. Actual external execution remains controllable only if the launcher obeys admission. | design-only |
| 5 | One acceptance authority and deterministic selection — I01, I20 | Generator declares its own success; choose two variants against different parents; bypass a protected criterion. | Only decide updates best, under a versioned policy and fixed round parent; emit machine-readable rejection reasons. Producer/verifier separation requires trusted role assignment, not merely a self-declared role field. | design-only |
| 6 | Objective/rung boundaries and incomplete termination — I10, I15 | Silently modify DONE; call a lower-rung output done; resume using an old rubric. | Human-authorized version changes, boundary quiescence, incumbent recheck, explicit COMPLETE/PARTIAL/HALTED status. Code cannot decide whether a new objective is desirable. | design-only |
| 7 | Attempt and evidence provenance — I07, I14, I17 | Drop failures, overwrite a source correction, or count repeated source copies as independent support. | Append attempts and supersessions; preserve lineage IDs and costs. Code can detect matching identities, but semantic independence still needs assessment. | design-only |
| 8 | Final-evaluation exposure — I15 | Repair using held-out feedback and later describe the result as an untouched first-pass success. | Record exposure, consume evaluation-set IDs, and preserve first-assessment outcomes. Actual secrecy needs an external evaluator/access boundary; a local flag does not hide files from an agent. | design-only |
| 9 | Gap and halt classification — I12, I13, I20 | Search indefinitely when a formulation is inadequate; confuse optional uncertainty with failed DONE. | Require gap class, required/optional status, action allowance and stop reason. The LLM/human proposes the diagnosis; the controller enforces transitions and scope. | design-only |

[design-only] The strongest reason for code is consistent enforcement under recovery and missing data—not an assumption that code "reasons better." A wrong acceptance policy becomes reliably wrong when encoded. Review the policy before implementing it, and test counterexamples rather than only happy paths.

[design-only] Do not encode the original "two judges prefer it" as a universal correctness rule. Use two layers: mandatory evidence checks must pass; declared preference criteria may then use a fixed panel rule. A subjective PASS stays a preference-based assessment in the report. It does not become independent evidence merely because a deterministic function counted it.

## 2. Minimal controller specification

### 2.1 Boundary and implementation size

[design-only] Start with an offline command-line controller and pure reducer, implemented with the Python standard library. One process owns writes. External roles receive request records and return result records; the controller does not call a model, browse, execute submitted code, or manufacture verifier evidence. The controller's API is a file/JSON boundary, not a distributed service.

[design-only] Minimal components: strict input validation; canonical hashing and immutable artifact storage; append-only event writer; replay reducer; budget ledger; pure acceptance policy; report generation. Suggested modules are records, archive, state, policy, and cli; module names are illustrative, not an implemented file tree. Do not start with a database, broker, plugin framework, or generalized workflow language.

[design-only] Treat this as a cooperative local controller, not a security sandbox. An agent with unrestricted write access could alter artifacts, archive or role assignments. To claim enforced isolation against such an agent, the surrounding environment must restrict writes and authenticate result origins. Checksums alone detect some inconsistencies; they do not authenticate an attacker-controlled replacement history.

### 2.2 State and record types

| State element | Minimum contents and rule | Label |
|---|---|---|
| Run identity | run_id, schema/controller/policy version, mode, target type and initial artifact hash. Unsupported versions refuse normal resume. | design-only |
| Specification | DONE/rubric hash, required criteria and check types, protected constraints, cumulative rungs, final rung, permission scope. | design-only |
| Artifact history | Immutable bytes by hash; artifact IDs, parent IDs and proposed change. best points to an accepted artifact, not a mutable filename. | design-only |
| Round | Round ID, frozen incumbent hash, proposed candidate IDs, required review slots, and accepted candidate or none. | design-only |
| Requests/attempts | Call ID, attempt ID, trusted assigned role, input hashes, expected result schema, reservation, dispatched/result status. No role may invent its own authority. | design-only |
| Checks | Candidate/parent/rubric/source-scope hashes; criterion ID; check identity/version; PASS/FAIL/UNKNOWN/ERROR; evidence references. Preference results additionally use A/B/tie. | design-only |
| Budget | Caps, known expenditure, outstanding reservations, unknown liabilities, finalization allowance, run deadline and retry caps. | design-only |
| Gaps | Criterion, required/optional, missing-evidence/inadequate-formulation/unavailable-substrate class, owner, proposed action, closure evidence or human authorization. | design-only |
| Evaluation exposure | Evaluation-set IDs, sealed/exposed/consumed status, first outcome, and any feedback passed into subsequent revisions. | design-only |
| Termination | ACTIVE, BOUNDARY_PENDING, HALTED, COMPLETE or PARTIAL; reason, unmet criteria and last accepted artifact. | design-only |

[design-only] Use an event envelope with schema_version, monotone seq, unique event_id, run_id, type, timestamp, payload, previous-record hash and record hash. Pin the canonical JSON encoding; reject duplicate keys, nonfinite numbers and oversized records. Use integer resource units to avoid ambiguous rounding. The hash chain is an integrity aid, not a signature.

| Record family | Examples and purpose | Label |
|---|---|---|
| Configuration | RunInitialized, SpecAmended, RungAdvanced, PolicySelected; changes require the appropriate authority and apply prospectively. | design-only |
| Work | RoundOpened, CandidateProposed, RequestAdmitted, RequestDispatched, ResultRecorded, AttemptErrored. | design-only |
| Evidence | CheckRecorded, EvidenceSuperseded, GapOpened, GapClosed, EvaluationExposed. | design-only |
| Resources | ReservationCreated, UsageReconciled, BoundViolation, DeadlineReached; request admission and reservation should be one event/atomic reducer action. | design-only |
| Decisions | CandidateAccepted, CandidateRejected, RoundClosed, Halted, Completed; record relevant hashes and reason codes. | design-only |
| Recovery | RecoveryNoted, AttemptCompletionUnknown, RunResumed; retain the earlier failed attempt and any unresolved charge. | design-only |

[design-only] A complete historical artifact need not have every criterion passing before it can be improved. Keep candidate admission, acceptance as the next best, and final completion distinct: admission requires structurally valid inputs; acceptance requires passed hard constraints, preserved previously passing obligations, and the declared improvement/simplification rule; COMPLETE requires every required DONE criterion at the final rung. Otherwise the controller could reject every intermediate step toward a solution.

### 2.3 Operations

| Operation | Inputs and behavior | Label |
|---|---|---|
| init | Freeze initial configuration, caps and artifact; assign allowed external roles; record pending initial verification. Do not label v0 verified automatically. | design-only |
| propose | Store candidate bytes and parent hash; admit only against the frozen round parent; store its hypothesis as untrusted rationale. | design-only |
| admit_request | Check run/rung status, role allowance and available resources; create request plus reservation atomically. Refuse requests that consume protected final-check allowance. | design-only |
| record_dispatch | Record that the external launcher is about to execute an admitted attempt. This is not proof that execution occurred or finished. | design-only |
| record_verdict | Validate request identity, payload structure, artifact scope, expected criterion and assigned role; append result without changing best. Identical result replay is a no-op; same ID with different content is a conflict. | design-only |
| reconcile_usage | Settle reported actual usage once; retain unresolved liabilities. A bound violation preserves real cost and halts new admission—it is not hidden by clipping. | design-only |
| decide | Pure decision over recorded evidence; enforce hard gates and exact panel policy, select at most one eligible candidate and append acceptance. Missing checks return WAIT/UNRESOLVED, not fabricated rejection evidence. | design-only |
| check | Report required missing/stale checks and prepare external check requests. It evaluates recorded results; it does not execute arbitrary tool commands. | design-only |
| boundary | Require no unresolved candidate acceptance in flight; accept only trusted human approval for rung/spec changes; version the rubric and invalidate affected passes. | design-only |
| resume | Validate archive and artifact references; reconstruct state without invoking roles; identify outstanding/uncertain attempts and resource liabilities. | design-only |
| halt / report | Emit last accepted artifact, completion status, required gaps, rung, evidence types, first final outcome and known/unknown costs. Halting does not erase valid partial work. | design-only |

[design-only] Panel policy must be explicit before execution: active slot count, order-reversal aggregation, early rejection, pruning requirements and tie-break order. An ordinary preference verdict can be a tie while the review is structurally valid; UNKNOWN means no usable determination. Do not conflate these. For pruning, require all reviews specified by the pruning policy to complete and find no regression. Panel slots identify assigned requests, not interchangeable favorable votes collected until a threshold is met.

[design-only] Enforce the writer-never-judges rule against assigned producer/reviewer identities or contexts. One model family may fill separate contexts if declared; this is role separation, not demonstrated statistical independence. External deterministic checks can serve as independent check evidence without inventing a "judge agent."

### 2.4 Durability and external-call ambiguity

[design-only] Proposed commit order: write candidate/check artifacts to temporary files, flush and sync them, rename to their immutable hash paths, then append and sync one complete acceptance event. Update the in-memory state only after that append succeeds. Orphaned artifacts are harmless; an accepted event referencing missing bytes is an integrity failure. Declare the supported filesystem/OS durability assumptions rather than promising power-loss safety everywhere.

[design-only] Define a valid event as newline-terminated, parseable, schema-valid and hash-chain-valid. On a damaged final tail, preserve its bytes and continue in a new archive segment referencing the last valid record; never append onto the malformed line or silently rewrite history. Interior corruption, a broken hash chain, or missing accepted artifacts requires an integrity halt. A new segment preserves the append-only contract; it does not make corruption acceptable.

[design-only] Enforce the single-writer assumption through one long-lived owner process or an exclusive local lock acquired at startup. A second writer must fail to open for mutation. If using a standard-library exclusive-create lock file, stale lock removal requires explicit recovery after confirming no writer remains; do not automatically steal it on a timeout. This is local ownership, not a distributed lease.

[design-only] A crash after an external call finishes but before its result is recorded cannot be solved by JSONL alone. Mark the attempt COMPLETION_UNKNOWN. Reconcile an existing external result if available; otherwise require an explicit budgeted retry with a new attempt ID and retain possible duplicate cost. Guarantee idempotent acceptance, not exactly-once external execution.

[design-only] A no-network controller can serialize multiple outstanding reservations because all requests pass through one writer. It cannot prevent an external launcher from making unauthorized calls. A hard budget claim therefore requires the launcher to dispatch only admitted requests and to honor output/time bounds. Otherwise report the controller as an accounting/admission mechanism with best-effort enforcement. Unknown usage stays reserved or becomes an explicit liability; it never becomes zero by default.

[design-only] Use a monotonic clock for elapsed time within a process and persist a run deadline and cumulative accounted duration for recovery. Define whether downtime counts; a wall-time study should count it. Detect inconsistent time on resume and halt for reconciliation rather than allowing a negative duration to restore budget.

### 2.5 Invariants and one negative test each

[design-only] All tests below are proposed deterministic fixtures. They require no model calls, and none was run for this review.

| ID | Controller invariant | Negative test and expected outcome | Label |
|---|---|---|---|
| C01 | Only complete required gates permit the relevant decision | Submit ERROR in a mandatory screen slot; decide cannot accept. | design-only |
| C02 | Every verdict is bound to its candidate, parent and rubric | Present a PASS for parent p1 after the current round moved to p2; reject as STALE. | design-only |
| C03 | One result ID identifies one payload | Resubmit an existing result ID with a changed vote; reject IDENTITY_CONFLICT. | design-only |
| C04 | Completed recorded calls are not rerun during replay | Resume an archive with a completed result and no acceptance yet; expose pending decision, not a new call request. | design-only |
| C05 | No new admission exceeds known plus reserved capacity | Under cap 100 reserve 60, then request 50; deny the second request. | design-only |
| C06 | Unknown usage remains a liability | Timeout a request reserving all remaining tokens; another request must be denied pending reconciliation. | design-only |
| C07 | Accepted artifact bytes precede acceptance | Remove the referenced artifact from a valid acceptance event; resume halts on integrity failure. | design-only |
| C08 | Final completion requires every required final-rung gate | Supply all E1 passes when final rung is E2; report PARTIAL, not COMPLETE. | design-only |
| C09 | Objective changes need external human authority | Submit a SpecAmended payload from a generator request; reject unauthorized operation. | design-only |
| C10 | Role assignment cannot be self-certified | Producer returns a result labeled "verifier" against an unassigned slot; reject role mismatch. | design-only |
| C11 | Changed dependencies invalidate affected passes | Supersede a claim's source hash; its earlier evidence check cannot support a new acceptance until rechecked. | design-only |
| C12 | One candidate per frozen round is accepted | After accepting candidate A, try accepting sibling B against the same round; reject ROUND_CLOSED. | design-only |
| C13 | Final-assessment exposure is preserved | Reveal failed criterion feedback, then ask to report that same evaluation as untouched; reject the status change. | design-only |
| C14 | A torn tail cannot alter reconstructed best | Cut an acceptance line before its newline; recover the prior best, preserve the tail, and require a new segment. | design-only |
| C15 | Only one local writer mutates state | Start a second writer while ownership is active; reject its write access. | design-only |
| C16 | Retry does not erase failed attempt or cost uncertainty | Retry a completion-unknown attempt; retain the original attempt and liability alongside the new reservation. | design-only |
| C17 | Initial invalidity does not block every repair | Give v0 a failing target criterion, then a candidate that improves it and preserves all hard constraints; do not reject merely because another target criterion is still unresolved. | design-only |

### 2.6 Degraded prompt-only mode

[design-only] Keep the essential behavioral contract in the skill, with controller mode as an optional adapter. When unavailable, the orchestrator performs the same checks and records manually, serializes work, and explicitly labels the run enforcement=prose. Do not import prior code-mode certification into that run or silently switch modes mid-run.

[design-only] On code→prose fallback, first halt the controller run, preserve outstanding liabilities and emit a handoff. A continuation gets a new mode record or run ID and inherits the remaining—not original—budget. A prompt should never claim atomic persistence, hard budget enforcement, or crash-safe recovery simply because it describes those properties.

## 3. What stays out, and what becomes an interface

| Capability | Decision under widened scope | Minimal interface or reason | Label |
|---|---|---|---|
| Distributed broker, leases, fencing, sharding and consensus | Keep out of this controller | One writer and local attempts suffice for the proposed scope; a later substrate owns distributed task delivery. | design-only |
| Full scientific knowledge graph and ontology migrations | Keep implementation out; expose references | Pass assumption/evidence/dependency IDs and immutable snapshot hashes; RQGM need not own the scientific state. | design-only |
| Model invocation, web retrieval and arbitrary command execution | Keep outside the offline core | Controller emits request envelopes; external adapters return results, provenance and usage. | design-only |
| Numerical, symbolic and Lean verifiers | Plug-in boundary, not bundled framework | Named verifier contract, candidate hash, scoped verdicts, evidence and tool versions. Invoke outside the core. | design-only |
| Adjoint sensitivity, Bayesian optimization and experiment selection | Keep out by default | Domain tools may return proposals; the controller enforces their cost and acceptance contract, not their algorithm. | design-only |
| Scientific belief update and hypothesis reconciliation | Substrate-owned | RQGM proposes a change against a snapshot; scientific commit authority checks current validity. | design-only |
| Local artifacts, verdicts and acceptance archive | Implement now | These are the controller's own state and evidence, with exportable records. | design-only |
| Source/criterion dependency tracking | Minimal local implementation | Accept optional dependency references; use conservative full checks when incomplete. No speculative inference engine. | design-only |
| Evaluator replacement | Proposal interface, never unilateral authority | Return successor evaluator artifact, comparison evidence and limitations. Outer human/substrate authorizes promotion. | design-only |
| Global multi-project resource allocation | Keep out; accept allocation | Parent supplies a scoped budget allocation ID and limits; local reservations consume it, then return usage and unknown liabilities. | design-only |
| Multi-agent repository branching/merge service | Keep separate | RQGM may improve a branch artifact; Git permissions, merge checks and release authority remain outside. | design-only |
| 100–200-agent scheduler | Keep out of this MVP | A substrate can host many bounded RQGM jobs; this controller must not create that pool itself. | design-only |

[design-only] Define one portable request/result envelope now so later integration changes the adapter, not the acceptance policy:

| Direction | Required fields | Label |
|---|---|---|
| Substrate → RQGM | request_id, immutable target reference/hash, parent snapshot ID, objective/rubric version, assumption/evidence references, allowed capabilities, budget allocation, expected output contract and stop conditions. | design-only |
| RQGM → substrate | request_id, candidate artifact/hash, original snapshot and parent hashes, check/verifier versions, scoped outcomes, provenance, known/unknown costs, unresolved gaps, completion status and proposed change. | design-only |
| Substrate → RQGM receipt | Accepted/rejected/stale outcome, reason, authoritative committed revision and any permitted revalidation request. | design-only |

[design-only] Local best is not a committed scientific fact or deployed evaluator. The outer substrate can reject it because the source snapshot changed. Make this two-stage promotion explicit: RQGM selects a candidate; the outer authority admits it to its own state. Do not let a local COMPLETE field bypass the outer verifier.

[design-only] For Meta-Evaluator use, freeze the current evaluator for the run, keep successor development evidence separate from untouched evaluation evidence, and submit a promotion proposal. Let the outer epoch controller decide draining and activation. Otherwise the same loop can change the judge and then use that changed judge to certify its own improvement.

[design-only] Budget interfaces need one owner: either the parent allocates a bounded sub-budget that this controller reserves internally, or the parent authorizes individual dispatches. Do not let both layers independently spend the same nominal remaining balance. Report nested call lineage so the parent aggregates actual usage once rather than counting both an allocation and its expenditures.

[design-only] This revises my earlier ADR 008 recommendation precisely: importing a kernel is now within scope, but direct adoption is not justified by its existence or its test count. Reuse its ideas and suitable negative cases; implement the minimum persistent controller against the new contracts. Do not infer that the prior in-memory reference already satisfies them.

## 4. Validation delta

### 4.1 Separate the rules from their enforcement

[design-only] Do not silently replace the original revised-prose arm with a controller arm and attribute the resulting difference to the prose edits. Give them different identities:

| Arm | Procedure | Contrast available | Label |
|---|---|---|---|
| S | Strong single-agent iterative revision with the same tools, public checks and budget | Simple baseline for practical value. | design-only |
| V | Frozen v2 with LLM orchestration | Existing loop baseline. | design-only |
| P | Revised prose with LLM orchestration | P versus V estimates the effect of the revised procedure as a package. | design-only |
| C | The same revised prose and role inputs, with the controller enforcing its specified rules | C versus P estimates the effect of enforcement as implemented, including altered scheduling or feedback it causes. | design-only |

[design-only] Recommended first use of the approximately 200-call budget: preserve the prior three-arm S/V/P comparison and add a zero-model-call controller conformance/fault suite plus shadow replay of P's recorded outputs. This avoids reducing already-small task coverage merely to add an arm. Here, the original "N" means P, revised prose; controller effectiveness is reported separately and narrowly.

[design-only] Shadow replay can identify that code rejects an ERROR or stale result that the prose orchestrator accepted. It cannot show what final artifact C would have produced after that rejection: the future generator inputs would differ. Freeze the trace at the first divergent decision, report the divergence, and do not splice later P outputs into C as if they were a valid controlled continuation.

[design-only] This staged design can establish controller conformance and observed enforcement disagreements, but it cannot establish live C-versus-P outcome superiority. That limitation is preferable to attributing a counterfactual outcome to an unrun controller.

### 4.2 If live controller impact must be tested now

[design-only] Use four explicitly named arms with two frozen small tasks, one run per arm and at most 24 model invocations per run: 2 × 4 × 24 = 192 scored calls, leaving up to eight preparation calls within 200. Count nested model invocations, both order presentations when separate, retries, all verifier/judge roles and LLM orchestration. Controller operations and offline fault checks consume no model calls but still consume measured CPU/time.

[design-only] The 24-call allowance is an allocation proposal, not evidence that v2 can finish its probes, improvement round and final assessment. Check that feasibility before freezing. If it cannot, retain the three-arm plan and defer live C; do not suppress v2's required mechanisms or give C privileged hidden checks to force a result. Report all budget-censored runs rather than dropping them.

[design-only] Keep the prior task types: small known-answer code repair and controlled-corpus factual/consistency repair, with independently frozen oracle checks inaccessible to every acting arm. Hold models, role prompts for P/C, tools, source access, initial artifacts and ceilings fixed. Use serial role execution in both P and C to avoid confounding code enforcement with parallelism. Randomize arm order and reset run memory.

[design-only] Measure all orchestration tokens actually used. A deterministic controller may need fewer model-driven orchestration calls; that is part of its practical cost effect. Do not add sham LLM calls to C to equalize realized expenditure. Match ceilings, report cost/outcome trade-offs, and state that C versus P is a package-level enforcement comparison, not a pure test of code language with every intermediate request held identical.

[design-only] Both P and C still require the same external study budget meter. This prevents uncontrolled spending but masks some local budget-failure consequences. Therefore assess reservation correctness in the no-model fault suite and report outer-meter interventions separately in live runs. Do not claim a measured budget-safety advantage if the common harness prevented both from violating the cap.

### 4.3 No-model-call fault-injection suite

[design-only] Prepare synthetic request/result records, a fake clock, dummy immutable artifacts and a controlled append writer with selectable crash points. No provider or LLM is needed. The table specifies expected outcomes, not results obtained.

| Fault | Injection | Required observation | Label |
|---|---|---|---|
| Malformed verdict | Missing criterion ID, invalid enum or duplicate JSON keys | Reject/quarantine result; record error; no accepted candidate and no implied tie. | design-only |
| Timeout | Admit and dispatch a call, advance fake clock, provide no result | Mark attempt unresolved/error according to policy; preserve outstanding usage and prevent acceptance from the missing review. | design-only |
| Stale parent | Supply a valid-looking PASS for candidate parent p1 after round parent p2 is active | STALE; no change to best; explicit new review required. | design-only |
| Crash before acceptance append | Persist artifact/checks, terminate before the acceptance line | Resume old best; completed checks available; do not reissue recorded completed calls. | design-only |
| Crash during acceptance append | Write only a line prefix | Recover the valid prefix, preserve the torn tail, and start a linked segment; no partial acceptance. | design-only |
| Crash after synced acceptance | Persist the complete acceptance, terminate before returning success | Resume accepted best; repeating the operation returns the existing receipt without a second acceptance. | design-only |
| External completion not recorded | Mark dispatch, simulate external success, then crash before result record | COMPLETION_UNKNOWN, not automatic replay; explicit reconciliation/retry and potential duplicate liability. | design-only |
| Budget contention | Serially submit outstanding reservations of 60 and 50 against cap 100, in both orders | At most one admitted; total known plus reserved never exceeds cap. Single-writer serialization handles contention without threads. | design-only |
| Unknown usage | Replace settlement with null after a failed attempt | Reservation remains; no artificial budget restoration. | design-only |
| Late old attempt | Retry under a new attempt ID, then deliver the old result | Preserve provenance, but do not let the superseded attempt fulfill the new review slot silently. | design-only |

[design-only] Also run fault-free trace conformance: the reference policy and controller must produce the same decisions for complete valid inputs. Otherwise the fault suite could "pass" because the controller rejects everything. Include an initially imperfect artifact, a valid incremental improvement, valid nonregressing pruning, a final complete case and an honest partial halt.

[design-only] Define success as zero invalid acceptances, no duplicate acceptance, no unexplained loss of recorded completed work, and no admission overspend in the specified traces. Do not call this a proof of all crash, OS, filesystem or concurrency behavior. Separately distinguish a simulated I/O crash test from a real process-termination/restart test; both can be model-free, but they establish different coverage.

### 4.4 Claims allowed after validation

| Evidence obtained later | Appropriate claim | Inappropriate claim | Label |
|---|---|---|---|
| Deterministic fault suite passes | The implementation handled the enumerated faults under the tested persistence/clock assumptions. | The loop is scientifically correct or universally crash-safe. | design-only |
| Shadow replay finds a divergence | The controller rejected a recorded protocol violation or applied the policy differently at this point. | The controller would have produced a better final artifact. | design-only |
| Live C outperforms P on the two cases | Better observed outcomes/cost on these cases at the declared caps. | General superiority across artifact types or reliable statistical significance. | design-only |
| P and C tie on correct outputs | No observed correctness difference in these runs; compare actual costs and protocol coverage. | Code enforcement has no value under faults or at scale. | design-only |
| Controller has no live outcome study | Infrastructure conformance demonstrated to the measured extent, if tested; outcome benefit remains design-only. | The revised loop is already better because its controller tests pass. | design-only |

[design-only] Final recommendation: implement the offline acceptance/accounting/recovery controller, validate it without model calls first, and preserve the original pilot's attribution. Infrastructure is now in bounds; unsupported infrastructure claims are not.
