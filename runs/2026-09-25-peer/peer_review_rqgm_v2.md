<!-- Provenance: reply from the peer ChatGPT conversation (GPT-6 Astra, https://chatgpt.com/c/6ab65a7f-facc-83ea-a714-3590b749ad8b) to consult-1-request.md, 2026-09-25. The in-page download did not complete, so this text was extracted from ChatGPT's file preview and its headings/tables re-marked-up by the Claude Code session; wording is unchanged. "genui{...}" markers are ChatGPT citation artifacts, kept as-is. -->

# Peer review of RQGM v2

[design-only] Review scope: answers to consultation sections 1–5; proposed edits only. No RQGM execution, tests, repository edits, or recursive optimization were performed for this review. The only new deliverable is this review file. Date: September 25, 2026, America/New_York.

[design-only] Label convention: measured denotes an explicitly attributed observation, including textual inspection; reported measurements are distinguished from independently inspected measurements. literature denotes a claim supported by an identified external source. design-only denotes an interpretation, recommendation, counterexample, proposed wording, or unexecuted experiment—not demonstrated effectiveness. A label applies to its entire paragraph, table row, or quoted replacement.

[measured] Evidence boundary: I read the supplied verbatim DESIGN.md and SKILL.md and the starter's invariant/ADR documents. The request reports 18/18 contract tests and 5/5 import hashes on the maintainer's rerun; I have not independently rerun them in this review. The attachment reports 995 skill words and several historical run counts; I have not recounted that skill or inspected those underlying run logs. INITIATOR.md and the live rqgm-loop repository were not supplied.

[design-only] Recommendation: retain the small single-artifact loop. Make evidence status, acceptance, incomplete execution, and version boundaries explicit. Do not turn it into the distributed substrate. Approve the design for a bounded pilot only after these ambiguities are resolved; do not describe the revision as better before the comparison.

## 1. Transfer triage

| Constraint | Classification | Exact reduced rule, where needed, and reason | Claim label |
|---|---|---|---|
| I01: commit authority | ADAPT | Only the orchestrator updates best; all other roles return proposals or verdicts. A database service is unnecessary. | design-only |
| I02: scope and assumptions | ADAPT | Each substantive claim records its assumptions, evidence pointer, and status; do not require a general entity ontology. | design-only |
| I03: stale reads/lost writes | ADAPT | Bind each variant and verdict to the parent artifact and rubric hashes; discard or recheck after either changes. This covers parallel variants and resume. | design-only |
| I04: fencing/lease expiry | ADAPT | Use a run/attempt identifier; accept only the currently outstanding attempt. No distributed leases or server-clock machinery in the prompt. | design-only |
| I05: result identity | ADAPT | Record a unique call ID and output hash; a completed call is not reapplied on resume, and conflicting reuse is an error. | design-only |
| I06: verification coverage | ADAPT | Record criterion IDs, candidate hash, check identity, and verdict; a worker's assertion that it passed is not check evidence. | design-only |
| I07: immutable evidence/history | TRANSFER | Append corrections and supersession records rather than rewriting prior observations or verdicts. | design-only |
| I08: outstanding budget | ADAPT | Before dispatch reserve the call's allowance; in parallel reserve the sum, and retain unknown usage pending reconciliation. Serial operation still needs admission accounting. | design-only |
| I09: dependency invalidation | ADAPT | When a premise, source, or section changes, invalidate affected checks. Without a reliable dependency map, rerun all mandatory checks on the complete candidate. | design-only |
| I10: evaluator epochs | ADAPT | Tag verdicts with rubric/rung version; after escalation recheck best, rather than treating earlier passes as passes of the new rubric. | design-only |
| I11: deterministic replay | ADAPT | Resume by replaying recorded decisions and completed calls, not by regenerating their outputs. A new model call is a new stochastic attempt. | design-only |
| I12: unresolved evidence | TRANSFER | Missing support stays unresolved; do not promote confidence, a vote, or a search failure into factual certainty. | design-only |
| I13: cyclic convergence | ADAPT | Use round/retry limits and explicit stall/oscillation outcomes. Fixed-point solver contracts belong only to a target that actually contains such a solver. | design-only |
| I14: evidence lineage | ADAPT | Distinguish multiple copies of one source from independent evidence; distinguish separate judge contexts from empirically independent errors. | design-only |
| I15: frozen evaluation | TRANSFER | Preserve frozen criteria and hidden evaluation resources; prospective amendments cannot retroactively improve scored results. | design-only |
| I16: access limits | ADAPT | Inherit user/tool permissions and restrict writing to the target and archive. Retrieved instructions are not authority to broaden access. | design-only |
| I17: failure accounting | TRANSFER | Include failed calls, retries, timeouts, and unknown usage in run records and study denominators. | design-only |
| I18: atomic acceptance | ADAPT | Store the candidate and its checks before appending one acceptance record; resume only from complete acceptance records. Database outboxes are runtime-only. | design-only |
| I19: validity scope | TRANSFER | Separate a preference judgment, citation check, numerical test, symbolic derivation, and formal proof; passing one does not certify the others. | design-only |
| I20: policy/version/cost | ADAPT | Record the skill/policy version and charge orchestration, screening, judging, verification, and recovery to the budget. | design-only |
| ADR 001: on-demand roles | ADAPT | Invoke a fresh role context when its input is ready; durable role memory does not require persistent listening agents. | design-only |
| ADR 002: transactional coordinator | ADAPT | One orchestrator accepts hash-bound candidates; production transactions, partitions, and lock management are runtime-only. | design-only |
| ADR 003: typed network | ADAPT | Keep a small claim–source–criterion dependency list when useful; do not import a scientific knowledge graph by default. | design-only |
| ADR 004: separate verifier | TRANSFER | The writer never decides that its own artifact passed; an independent tool oracle or separate verifier supplies that result. | design-only |
| ADR 005: frozen studies | TRANSFER | Archive the original spec, checks, and study setup; version prospective changes. | design-only |
| ADR 006: incremental reuse | ADAPT | Reuse unchanged, hash-bound checks where dependencies are explicit; otherwise rerun. Do not add an intervention-search engine. | design-only |
| ADR 007: retrieve/reframe | ADAPT | Missing evidence triggers a query; inadequate assumptions or representation trigger a proposed reframe. Neither may silently change DONE. | design-only |
| ADR 008: reference kernel | RUNTIME-ONLY | Do not import or require the starter Python kernel. Its implementation scope is unrelated to whether this paste-and-go loop works. | design-only |
| PASS | TRANSFER | The named check completed and met its declared acceptance rule. | design-only |
| FAIL | TRANSFER | The named check completed and found a violation; distinguish this from execution failure. | design-only |
| UNKNOWN | TRANSFER | Evidence or determination is insufficient; it neither passes nor becomes a tie. | design-only |
| ERROR | TRANSFER | Timeout, invalid output, or failed execution; retain the attempt and use a bounded retry policy. | design-only |
| V0: contract | ADAPT | Validate output fields, identities, versions, and allowed edits; a full schema service is unnecessary. | design-only |
| V1: execution | ADAPT | Retain tool command/source lookup, output, status, and relevant versions. Tool execution alone does not verify the artifact. | design-only |
| V2: substantive criterion | TRANSFER | Use the declared domain check for each checkable obligation; subjective preference remains a different kind of criterion. | design-only |
| V3: formal verification | ADAPT | Require a pinned proof-checker result only if DONE demands a formal proof; otherwise do not claim V3. | design-only |
| V4: study validation | ADAPT | Place matched-budget comparisons in a separate evaluation protocol, not in every artifact-improvement run. | design-only |
| ACTIVE → DRAINING → VALIDATING_SUCCESSOR | ADAPT | Finish or abandon pending evaluations, record human-approved rung/spec change, and recheck best before continuing. For serial calls this is a boundary checklist. | design-only |
| Knowledge-gap states | ADAPT | Use gap{criterion, missing evidence / inadequate representation / unavailable substrate, next action, owner}; query and applicability outcomes append to it. | design-only |
| RETRIEVE versus REFRAME | ADAPT | RETRIEVE seeks support under the current formulation; REFRAME proposes a different formulation. Human approval is required for objective, permission, or rung changes—not every search query. | design-only |
| Resource accounting | ADAPT | Cap calls/tokens/time; reserve before dispatch; log provider usage semantics and nulls. Charge every role and retry; preserve headroom for final checks. | design-only |
| A/B/C organization study | ADAPT | Preserve its separation of context isolation and concurrency, but do not call a v2/new/simple comparison an A/B/C organization ablation. Hold scheduling fixed first. | design-only |
| Reporting labels | TRANSFER | Label observed results, literature-supported claims, and untested design proposals; attribute measurements not independently inspected. | design-only |

## 2. Conflicts and smallest fixes

### 2.1 The five suspected issues

| Issue | Assessment and smallest repair | Claim label |
|---|---|---|
| (a) Majority preference treated as truth | Partly confirm. Voting is a permissible policy for explicitly subjective objectives, not a correctness oracle. v2 already says mechanical checks override judges, so it is inaccurate to say it uses votes for everything. Tag criteria as checkable or subjective; require completed named checks for the former and report preference-based acceptance for the latter. | design-only |
| (b) Undefined timeout/malformed verdict | Confirm by inspection. The supplied skill defines A/B/tie but no failure/abstention states. Add PASS/FAIL/UNKNOWN/ERROR for check execution, separately from A/B/tie; unknown/error cannot count toward acceptance or pruning. | measured (text inspection) / design-only (repair) |
| (c) Global cap without reservation or missing-usage rule | Confirm by inspection. The supplied cap does not specify admission, outstanding usage, or unknown accounting. Reserve before each call, leave final-check allowance, and retain null usage; if a provider has no bounded billing interface, do not claim a hard token cap. | measured (text inspection) / design-only (repair) |
| (d) Inadequate candidate space versus missing evidence | Confirm as a missing explicit rule. [OPEN] and substrates do not distinguish these cases. Add gap classes and let the loop propose a reframe within the target's scope; route any objective change to the human. | design-only |
| (e) No matched-budget simpler baseline | Confirm, but not an execution invariant violation. DESIGN.md acknowledges the absence. Add the comparison to validation, not to every skill run; remove any statement that redesign success establishes loop superiority. | design-only |

[literature] Judge limitations: Zheng et al. examine position, verbosity, self-enhancement biases and reasoning limits in LLM judging, while also finding usefulness for approximating human preferences. This supports a distinction between preference evaluation and scientific verification; it does not measure error correlation or majority-vote reliability in this particular loop.
L1. genui{"citation":{"ref":"turn1view0"}}

### 2.2 Additional problems worth fixing

| Finding | Minimal rule or interpretation | Claim label |
|---|---|---|
| Primary-source-only verification excludes original derivations and design proposals | Classify claims: empirical/literature facts need evidence; mathematical claims need a derivation/check; new designs are proposals with assumptions. Absence of a prior paper is not falsification. Never fabricate a supporting source. | design-only |
| Verifier strips or rewrites a failed claim after the candidate was screened | Return findings to the generator. Any revised artifact receives a new hash and reruns affected screening/checks; do not silently judge a different version from the one checked. | design-only |
| DONE is immutable, yet E3 adds a criterion | Predeclare the cumulative rung criteria in setup, or make E3 a human-approved, versioned prospective amendment. Recheck the incumbent. Never pool scores across differing objectives as if directly comparable. | design-only |
| Boundary permits stopping below the final rung | Preserve the human's right to stop, but label the output incomplete/partial. Passing a lower rung cannot satisfy a higher-rung DONE. | design-only |
| "Every kept version beat its parent" substitutes for regression checking in DESIGN.md | Pairwise preference need not be transitive or preserve untested behavior. Apply all mandatory regression checks to the exact complete candidate, including pruning variants. | design-only |
| Shortening exception bypasses the stated preference invariant | Make the invariant "verified improvement or verified nonregressing simplification." Require completed reviews; a missing verdict is not evidence that nobody rated the candidate worse. | design-only |
| Two variants can be evaluated against an incumbent that changes mid-round | Freeze the round's parent. Select at most one against that parent; never transplant the other diff without revalidation. | design-only |
| First judge alone controls early rejection and order probing | Treat its high confidence as a heuristic, not calibration. Either accept this declared efficiency trade-off or test an alternative prospectively; a one-time probe cannot certify later immunity to bias. | design-only |
| The meaning-preserving control also changes style | Use identity as an unambiguous tie control. Require a paraphrase tie only when every declared criterion is invariant to that paraphrase; clarity/style criteria can legitimately change. | design-only |
| Bias probe says "all 3 judges," but setup permits 2–5 personas | Define three active judge slots, selected from the persona pool, or specify panel sizing consistently. Personas are not independently trained models. | design-only |
| Fresh judge prompts are called held-out generalization | Separate unseen judge prompts from hidden task cases/oracle checks. The former assesses evaluator robustness; it does not independently establish factual or behavioral generalization. | design-only |
| Failed held-out criterion IDs guide subsequent repairs | Record the first failure as a failed final evaluation. Once feedback is used, that check is development data. A retry needs an untouched evaluation set; do not erase the first outcome. | design-only |
| "Loop never sees" held-out prompts lacks an access boundary | Have the human/evaluator retain them and invoke the check outside generator-visible context. A prompt instruction alone is not a technical secrecy boundary. | design-only |
| Human closes every OPEN, but closure could be confused with proof | Human authorization can close an ownership/decision gap; factual closure still requires the declared evidence. If the requirement is waived, amend the objective and record that it was waived. | design-only |
| Every OPEN blocks output, regardless of relevance | Only unresolved required criteria block DONE; retain optional unknowns without claiming they are resolved. Budget exhaustion and human stop must still emit a partial artifact. | design-only |
| Least-recently-changed section after two empty rounds | Use the unresolved required criterion as the default target. A section's age is not evidence that editing it will help. Permit a declared exploration choice if useful. | design-only |
| Ledger blocks an idea on two judge rejections | Store reason and rubric/source versions. Reconsider when evidence, scope, or the evaluator changes; preserve the rejection history instead of a timeless blacklist. | design-only |
| "Drop a torn last record" without preserving the bytes | Keep the damaged archive for diagnosis; recover its valid prefix. A complete acceptance record must reference an existing artifact and check set. | design-only |
| Stable call order described as deterministic resume | Replay recorded decisions deterministically; do not promise that regenerated LLM outputs or fresh tool executions reproduce them. | design-only |

[literature] Holdout caution: work on adaptive data analysis explains why repeated feedback from evaluation data requires special care to preserve validity. This motivates protecting an untouched final assessment. It does not supply a numerical correction for v2's judge-prompt retry scheme.
L2, author explanation of Dwork et al., Science (2015), DOI 10.1126/science.aaa9375. genui{"citation":{"ref":"turn1view1"}}

[design-only] Priority judgment: defects involving acceptance of unsupported content, skipped/unknown checks, and stale candidate identity are more consequential than changing the search heuristic. Fix those before adding more judges or recursive rounds.

## 3. Top eight reviewable edits

[design-only] Integration rule: these are replacement blocks, not append-only additions. Each proposed block below is under 60 words; the surrounding rationale is not proposed skill text. Apply each to its named section and remove the superseded sentences. The table does not assert that the combined resulting skill has been word-counted or already fits 1,000 words.

### 1 — Separate correctness from preference

[design-only] Section: Setup, replace the DONE definition and use its check semantics throughout.

> DONE assigns each criterion a check and type: checkable or subjective. Checkable criteria require completed evidence checks; judge votes cannot establish them. Subjective criteria may use declared preference voting, reported as preference. Every acceptance, including pruning, must preserve all mandatory checks. The writer never judges. Final completion requires the specified final rung.

[design-only] Prevents: preference votes certifying truth, pruning bypasses, and lower-rung completion claims. Evidence level for this exact edit: design-only; L1 motivates the distinction but does not validate this wording.

### 2 — Define incomplete and failed evaluation

[design-only] Section: Each round, replace the verdict-format sentences in Judge.

> Each check returns PASS, FAIL, UNKNOWN (insufficient evidence), or ERROR (execution or format failure). Preference checks additionally return A/B/tie. UNKNOWN and ERROR never count as ties, votes, or nonregression. Permit one budgeted retry; unresolved required checks block acceptance. All acceptance routes require completed required reviews. Record every failed attempt.

[design-only] Prevents: timeouts becoming abstentions that accidentally permit pruning, malformed votes, and silent retries. Evidence level: design-only.

### 3 — Make verification applicable to original work

[design-only] Section: Each round, Screen: replace its primary-source-only verification sentence with the following contract. The existing Roles bullet can remain: it only specifies the Verifier's inputs.

> Verifier independently checks empirical claims against evidence, mathematical claims against derivations or tools, and proposed mechanisms against explicit assumptions and tests. Unsupported proposals remain design-only, not facts. Return required corrections to the generator; do not silently edit the candidate. Any revision needs a new version and affected checks repeated. Never fabricate evidence or substrates.

[design-only] Prevents: rejecting valid novel reasoning merely for lacking a citation, and checking one candidate while accepting another. Evidence level: design-only.

### 4 — Protect the final assessment

[design-only] Section: Stop, replace the held-out/retry sentences.

> Final checkers stay outside generator-visible context. Use untouched check cases where available; fresh judge prompts alone test preference robustness. Record the first final-check outcome. Once its feedback guides revision, that check is development data. A retry requires untouched checks and remaining budget; otherwise report incomplete. Never turn a first failure into an unqualified first-pass success.

[design-only] Prevents: evaluator novelty being reported as task generalization and adaptive repair hiding first-assessment failure. Evidence level: design-only; L2 supplies general motivation, not direct validation.

### 5 — Admit calls against a real budget

[design-only] Section: Setup, replace the BUDGET definition.

> BUDGET: shared caps for calls, tokens, and elapsed time. Reserve each call's bounded allowance before dispatch, including concurrent calls and final checks. Charge all roles, retries, and orchestration. Log missing usage as null; retain its reservation until reconciled. If token usage cannot be bounded, label that cap best-effort. Budget exhaustion emits the last accepted artifact as incomplete.

[design-only] Prevents: hidden role costs, concurrent oversubscription, unknown usage counted as zero, and no resources remaining for final checks. Evidence level: design-only.

### 6 — Bind accepted work to exact versions

[design-only] Section: Memory, replace the compact schema and resume rule with this minimum contract; put optional field documentation in DESIGN.md.

> Archive artifact, parent, rubric and source hashes; call IDs, completed outputs, check results, usage, and acceptance records. Only the orchestrator accepts. Resume from a complete acceptance record; never rerun completed calls merely to reconstruct state. Reject stale-parent verdicts. Preserve damaged records separately. Changed premises invalidate affected checks; without dependencies, rerun mandatory checks on the complete artifact.

[design-only] Prevents: stale verdict reuse, repeated completed calls, source changes leaving invalid passes, and partial acceptance during recovery. Evidence level: design-only. The starter's contract tests concern a different implementation and do not measure this prompt rule's effectiveness.

### 7 — Distinguish a search gap from a formulation gap

[design-only] Section: Each round, replace the least-recently-changed-section fallback in Propose.

> On a blocked criterion, classify the gap: missing evidence → RETRIEVE; inadequate assumptions or representation → propose REFRAME; unavailable data or authority → OPEN. Search within existing permissions and budget. A reframe may change the artifact, not silently change DONE. The human decides every objective/rung escalation and substrate closure. Target unresolved required criteria before section-age heuristics.

[design-only] Prevents: aimless section rotation, unsupported certainty, and repeated search within an inadequate formulation. Evidence level: design-only.

### 8 — Version the rising bar

[design-only] Section: Boundary, replace its escalation instructions.

> Predeclare cumulative rung criteria. A new criterion requires a human-approved, versioned amendment, never a silent DONE edit. Finish or abandon pending verdicts, record the new rubric, and recheck best before continuing. Earlier passes retain their original scope. Human stop below the final rung produces a partial result. Only the human decides escalation.

[design-only] Prevents: contradictory immutability rules, stale passing criteria, and changing the definition of success after observing outcomes. Evidence level: design-only.

[design-only] Word-budget advice: replace duplicated invariant explanations and schema enumeration with concise cross-references inside the skill, and keep rationale, literature, experiment plans, and detailed record fields in DESIGN.md. Keep the operational rules needed to run the loop inside the skill; do not require fetching an unavailable document mid-run. A paste-and-go INITIATOR needs equivalent essential semantics. The maintainer should use the repository's declared counting convention after consolidation; I do not certify a ≤1,000-word integrated skill from eight isolated substitutions.

[design-only] Size gate: do not merge all eight blocks on top of the reported 995-word version. Treat the 1,000-word ceiling as a release gate: compress superseded prose first, then integrate the replacements and verify the resulting count. If that cannot be achieved without hiding essential rules in inaccessible references, stage the lower-ranked changes rather than exceed the cap.

## 4. Smallest honest validation within roughly 100–200 calls

### 4.1 What is being tested

[design-only] Primary question: on two prespecified small artifacts, does the revised loop produce better independently checked final artifacts than both frozen v2 and a strong simple baseline under identical resource ceilings? This is a feasibility and case-comparison pilot, not a population-level superiority study.

| Arm | Procedure | Relation to the organization design | Claim label |
|---|---|---|---|
| S: simple | One tool-using agent repeatedly revises a single artifact in one context, with public tests and the same source access. It can spend the full allowance on diagnosis, revision, and tool use. An external deterministic harness scores its final output. | Strong single-agent reference; the writer does not provide the outcome score. | design-only |
| V: v2 | The supplied skill, frozen, including its probes, role separation, screens, judges and final check. All internal calls count. | Isolated-role procedure, executed serially for this first comparison. | design-only |
| N: revised | Consolidated skill with the proposed changes, frozen before outcomes; same serial scheduling and model as V. | Tests the revised procedure as a package, not the causal effect of context isolation alone. | design-only |

[design-only] A/B/C compatibility: this respects the earlier study's controls but is not its A/B/C factorial contrast. V versus N mixes the changes intentionally; S versus either loop mixes role organization and policy. Do not attribute a difference to asynchronous scheduling, context isolation, or one edit. Test isolated-serial versus isolated-async later while holding the chosen policy fixed. No concurrency advantage is claimed here.

### 4.2 Call allocation and matched resources

[design-only] Allocation: at most 18 preparation/smoke-test calls on separate disposable examples, then two tasks × three arms × 30 model invocations = at most 180 scored invocations; overall ceiling 198. Count generator, screen, verifier, both order presentations when separately called, all judges, retries, and any model-driven orchestrator calls. "One subagent" is not "one call" if it invokes a model repeatedly. Deterministic tool operations are separately metered.

[design-only] Proposed per-run caps: 30 total model calls, 60,000 accounted input-plus-output tokens using the provider's non-double-counting semantics, 60 tool invocations, and a 15-minute wall deadline. Pin model/sampling/output limits and tool compute ceilings during preparation. These are proposed ceilings, not measured feasibility estimates. If preparation shows they cannot exercise a meaningful v2 round and final check, revise task size or allocation before freezing; do not remove v2 mechanisms to fit after seeing scored outcomes.

[design-only] Budget enforcement: use the same external admission meter for all arms. This is study instrumentation, not a secret patch to v2; its internal stopping logic remains unchanged. Report budget-meter interventions. This common enforcement cannot establish that N's own reservation logic is superior; that requires a separate fault test. Equal ceilings are not equal realized expenditure: report actual usage and do not force efficient runs to burn the remainder.

[design-only] Availability condition: if total usage or nested invocations cannot be observed/bounded, the session can produce a call-capped feasibility report but not a verified matched-token claim. Use the same available model for all roles in this pilot, including held-out judges; record the resulting limitation. No "strongest model" privilege for one arm. All human inputs and checker prompts are prepared in advance and frozen.

### 4.3 Two small tasks with external ground truth

| Task | Starting artifact and available information | Independent evaluation | Claim label |
|---|---|---|---|
| T1: small code repair | A short parser or interval-boundary function with two seeded defects, a written specification, public tests, and a must-not-change interface. No domain secrets required. | Hidden boundary/property cases plus public regression tests, run by a harness inaccessible to the generator. Freeze the reference implementation and tests first. | design-only |
| T2: source-grounded consistency repair | A short report/table with planted arithmetic errors, a false causal statement, and a required field missing from the initial context but available in a controlled source corpus. Add one optional genuinely unknown field that should remain explicitly unknown. | Frozen factual tuple answers, arithmetic checks, source-applicability mapping, and required-versus-optional completion rules. A human prepares the answer key before outputs; no LLM majority establishes truth. | design-only |

[design-only] Avoid test contamination: keep final checker cases and answer keys outside all acting-agent contexts. Each arm gets the same public tests, corpus, access permissions and initial artifact. Human-written held-out judge prompts for V remain part of V's internal process, not the independent endpoint. Give N equivalent access to independent internal review; neither arm may see the experiment's sealed oracle. Do not award new hidden tests exclusively to N.

[design-only] Selection and order: choose the two cases before scoring and exclude preparation examples. Randomize arm order within each case; reset memory between arms. Do not share discovered sources, patches, or critique across arms. Freeze amendments, model identifier, artifacts, prompts, rubric, tool versions, and budget schedule in a manifest. Use one run per arm/task; retries consume that run's allowance rather than creating invisible replacements.

### 4.4 Outcomes and honest interpretation

| Outcome | Definition | Claim label |
|---|---|---|
| Primary | Whether the final emitted artifact passes every required oracle check within the shared ceilings, per arm and task. Score partial outputs too, while retaining incomplete-run status. | design-only |
| False completion | Loop declares DONE but the independent oracle finds a required failure. Distinguish it from an incomplete artifact honestly labeled incomplete. | design-only |
| Secondary correctness | Prespecified obligation pass counts and mandatory regressions; no double-counting correlated checks as independent experiments. | design-only |
| Cost | Actual tokens with accounting gaps, calls, tool usage, time, and human interventions; count failed/aborted work. | design-only |
| Process coverage | Whether a proposal, screening, verification, acceptance/rejection and final assessment actually occurred; identify budget-censored runs. | design-only |
| Mechanism audit | Whether unknown/error responses were mishandled, stale versions accepted, or optional gaps confused with mandatory ones. Do not secretly inject such faults into only one arm. | design-only |

[design-only] Decision rule: report the two paired case outcomes and actual costs without a significance claim. A revision can be described as better on these observed cases under these ceilings only if the reported correctness/cost results justify that restricted statement against both comparators. Mixed outcomes, equal outcomes, or an unexercised revised mechanism remain inconclusive. Do not use token-per-success alone to reward early abandonment.

[design-only] What it can establish: that the frozen procedures can execute within the proposed environment; their outcomes and costs on these exact cases; any observed false completion or bookkeeping failure; and whether a larger preregistered evaluation is worth funding.

[design-only] What it cannot establish: statistically reliable general superiority; benefits of individual changes; robust stochastic reproducibility; performance on papers, proofs, scientific discovery or all artifact types; independent judge errors; live asynchronous advantage; or 100–200-agent scaling. Two cases with one run per arm do not justify such generalizations. The 198-call ceiling is a resource plan, not a power calculation.

[design-only] Stronger follow-up: if the pilot exposes no basic execution defects, use more independently sampled tasks and repeated runs, prespecified task-level paired analysis, and a separate organization ablation. If the actual goal is a defensible broad "better than v2" claim, that larger comparison is necessary; no clever vote aggregation can make this tiny pilot equivalent.

## 5. What not to import

| Do not import | Keep instead | Claim label |
|---|---|---|
| Distributed task brokers, leases, server clocks, fencing services, transactional outboxes, sharding | One orchestrator, version-bound attempts, and complete acceptance records. | design-only |
| The starter's Python kernel or its passing tests as validation of this loop | Treat those as different software; evaluate this loop's own behavior. | design-only |
| A full ontology, embedding space, Bayesian belief engine or typed hypergraph | A small dependency/evidence list where it prevents real reuse errors. | design-only |
| All 20 invariant texts and five verifier levels verbatim in SKILL.md | Essential acceptance rules in the skill; rationale and optional domain contracts in DESIGN.md. | design-only |
| Mandatory Lean, adjoints, NUFFT machinery, or numerical solvers | Invoke a domain checker only when the target and DONE require it. | design-only |
| An intervention-replay/search engine | Recheck affected obligations and reserve expensive audits for a concrete need. | design-only |
| Persistent listening agents or 100–200 concurrent roles | On-demand role calls with a bounded budget; study concurrency separately. | design-only |
| Evaluator self-modification as an automatic privilege | Human-approved, versioned rubric/rung changes with incumbent rechecking. | design-only |
| A requirement that every novel proposal have a published primary source | Explicit design-only status plus assumptions, derivations or tests appropriate to the claim. | design-only |
| Every uncertainty becoming a human blocker | Required/optional gap distinction; permitted retrieval can proceed, while the human retains escalation and closure authority. | design-only |
| "Different family" or "three fresh personas" as proof of independent errors | Record composition and evaluate actual error behavior; preserve objective checks. | design-only |
| The literature's guarantees by sharing the name "Gödel Machine" | Describe the actual empirical prompt procedure and its observed limits. | design-only |
| A superiority benchmark inside every artifact run | A separate frozen evaluation protocol, with its own cost ledger. | design-only |
| All claims from the attached bibliography as independently verified here | Preserve them as attributed background until the exact source/claim is checked. Only L1 and L2 support literature claims made in this review. | design-only |

[design-only] Final disposition: the useful transfer is a small evidence-and-acceptance contract, not a runtime architecture. Preserve the writer/verifier separation, human escalation, fixed artifact scope, and honest incompleteness. Validate the consolidated prompt before calling it an improvement.
