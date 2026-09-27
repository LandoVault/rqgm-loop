<!-- Provenance: reply from the peer ChatGPT conversation (GPT-6 Astra, https://chatgpt.com/c/6ab869a2-ba54-83ea-b6aa-4ee2153ceeef) to consult-5-request-run-report.md, 2026-09-26. Captured from the chat reply text; headings and the three tables re-marked-up by the Claude Code session, wording unchanged. The peer had the brief (doc 33 §14-§16, skill §9, the relations FINAL_REPORT) only; it saw no repository code, tests, archives or samples. Its own evidence labels are kept verbatim. Development feedback for v4.3, not a held-out assessment. -->

# Peer review: loop v4.2 and the relations run report

Date: 2026-09-26 (America/New_York). Source: consult-5-request-run-report.md, including attachments A–C. Review only: no project code, tests, or experiments executed; no subject information requested, inferred, or reconstructed. Recommendations concern architecture, synthetic harness validation, and aggregate reporting. This is development feedback, not held-out evaluation.

Evidence labels: [measured—reported] means an observation stated in the supplied brief, without independent inspection or reproduction. [design-only] covers logical critique, proposed specifications, and prospective experiments; it does not establish effectiveness. No independently verified literature claims are made. Labels apply to the paragraph, bullet, or table row they introduce. Administrative provenance is given above.

[design-only] Main assessment: Keep a small enforced acceptance boundary, and let proposal methods remain flexible. v4.2 improves the stated control structure, but its remaining weaknesses are evidence authenticity, evaluator calibration, and invalidation of previously accepted work. More search cannot repair inadequate identification or information. The report supports "no candidate met the stated contract"; it does not establish that the data are the uniquely dominant cause, that the target is absent, or that the proposed numerical envelopes are exclusion bounds.

## 1. Restricted versus "in spirit"

### 1.1 The split should follow consequence and observability

[design-only] "Previously broken or likely to be broken by an optimizer" is a useful prioritization rule, but an incomplete architecture rule. It overfits the last failure log, conflates research allocation with safety, and implies code can enforce semantic truth. Prefer: enforce observable conditions whose violation corrupts acceptance, provenance, permissions, or budgets; make search-allocation rules configurable; leave scientific judgment and proposal construction in prose. A strong model may follow flexible guidance well, but that does not independently establish that its completion claim is supported.

[measured—reported] The brief reports 85 passing tests and a replay that rejects 10/10 late-run children. These establish reported test and replay outcomes. They do not measure prospective discovery, false-completion reduction, cost savings, or whether the rules would have improved that historical search.

[design-only] Keep enforced: immutable evaluation identities; authenticated acceptance receipts; suspended evidence barred from keep/exit; declared spending limits; controller-owned writes and transition authorization; frozen evaluation cohorts; access restrictions around protected evaluation assets. Bind a next identifier to the current archive head, policy revision, action type, and target hash, and consume it atomically. Matching only "the last id" leaves stale or duplicated action submissions insufficiently specified.

[design-only] Narrow these purported invariants:

- "Writer never judges": Allow local self-checks for development. Enforce that the writer's assertions never substitute for independent final acceptance. Separation concerns authority and accessible assets, not merely role names.
- "Nothing unverified counts as fact": Enforce typed evidence and explicit uncertainty. Software cannot establish universal semantic truth from an evidence field.
- "Human-only records carry by: human": Retain the field as a label, but require approval provenance supplied by the trusted host or authenticated human channel. An agent can type that string.
- "Identifiers never enter tracked files": Enforce a restricted artifact export path and deny protected inputs to exporting roles. A pattern scan is defense in depth, not a universal detector; legitimate artifact IDs must be distinguished from prohibited identifying content.
- "Assets never change": Freeze assets within a cohort, while permitting authorized replacement with invalidation and rebaseline. Permanent immutability prevents legitimate instrument repair.

[design-only] Demote fixed lineage fractions, mandatory slot-a novelty, a three-round stall threshold, and "exclude the exhausted family" from universal invariants to versioned allocation policies. If a run preregisters them, enforce compliance for that run; otherwise a documented boundary amendment can alter them. A deterministic violation verdict can protect an experiment's protocol without proving the protocol is a good search strategy. Preserve ancestry truth as an invariant even when quotas change.

[design-only] Promote independent command-result capture, complete evaluator case coverage, dependency-closure invalidation, withdrawal of unsupported keeps, and a final-assessment reserve to enforced transition conditions. Repeated evaluator requests should create an explicit unmet-capability or unresolved-hypothesis record, not automatically assert an instrument defect. Neither recurrence nor a persuasive critic proves that a requested operator is appropriate.

### 1.2 A small experiment that can distinguish the claims

[design-only] Use four entirely synthetic tasks: a small module with sealed executable tests; a prose contract with a planted cross-section contradiction; a portfolio search with a deliberately attractive single-seed shortcut; and a workflow receiving a scorer correction after a keep. Supply attainable valid solutions to the evaluator designer, but withhold them from solvers. Compare three arms using the same capable generator model and common final evaluation:

- Spirit: concise "use RQGM/RSI" guidance plus purpose and acceptance contract.
- Kernel: the same guidance plus the minimal enforced acceptance/provenance boundary.
- Full v4.2: the current routing, slots, screens, judges, and gate relays.

[design-only] Run two repetitions per task/arm: 24 runs. Cap each run at 18 model calls, including admission, relays, screens, retries, and final assessment: at most 432 calls. Also impose the same preregistered monetary or token ceiling per run; unused calls need not be spent. Reserve final assessment within the cap. The full arm may exhaust its budget early, which is an outcome. A 12-run, one-repetition first stage costs at most 216 calls; proceed to the second repetition under a rule set before seeing results. These are budget ceilings, not cost estimates or a powered efficacy study.

[design-only] Report sealed correctness, false completion, successful completion, honest unresolved exits, denied invalid transitions, human interventions, elapsed time, and total billed input/output/cache usage. Present quality versus total cost, not only compliance counts. Fork synthetic traces to inject stale approvals, omitted cases, forged exit codes, and new evidence; mechanical fault tests need no extra model calls. If the kernel prevents invalid acceptance with comparable completion and lower cost than full v4.2, keep the kernel and simplify the method. If quotas only raise rejection counts, their benefit remains unshown. Zero false completions in this small pilot is not proof of reliability.

## 2. Search limits, mappings, and the cheapest useful changes

### 2.1 Assessment of §16

[design-only] Each row below is fewer than 60 words. The limits are taken from the supplied report; each assessment is a proposed interpretation or correction, not a reproduced result.

| Reported limit | Mapping assessment and needed correction | Evidence |
|---|---|---|
| Lineage collapse | Ancestry checks prevent misdeclared or disallowed descent, not semantic convergence. Quotas can reject all feasible candidates. Preserve root provenance, reserve an independent-root opportunity, and report blocked allocation separately from scientific failure. | design-only |
| Single-seed verdicts; unstable null SD | Versioning records a scorer defect but does not calibrate it. Freeze a multi-seed case manifest, aggregation, sign convention, and uncertainty rule; reserve separate synthetic validation. "20 draws" is a budget choice, not a reliability guarantee. | design-only |
| Sign-blind D6; carrier-dependent D2 | Split effect existence, signed direction, and robustness. Define absolute perturbation sensitivity even when effect is null; relative robustness is undefined or uninformative near zero. Robustness alone cannot qualify a candidate as a discovered effect. | design-only |
| One-unit floor | Freeze physical units and the scientific relevance threshold separately. A small observed effect does not prove the threshold is defective. Test unit-conversion invariance and distinguish detection capability from meaningful effect size; never lower a bar because the front misses it. | design-only |
| One-grid contract blocks fusion | A multi-grid interface enables computation, not independent evidence or precision gain. Declare acquisition grouping, covariance handling, missingness, and fusion weights. Validate on synthetic correlated channels before scoring; do not count derived maps as independent replicates. | design-only |
| M21 never executed | This is incomplete search coverage, not evidence for the operator. Reserve a bounded synthetic trial if scientifically justified. Resolve conditioning/negative-control incompatibility first; residualization may remove target signal or preserve coupled error. Do not extend the cap merely because an idea remains. | design-only |
| Probe bank frozen | Dormancy and rotation improve scheduling only if calibrated probes actually execute. Log attempted/completed cases, mandatory coverage, and retirement reasons. Preserve a core set; version changes require comparable incumbent reassessment. | design-only |
| Limited power and independent information | Not repairable by search allocation. A candidate detecting its own chosen twin does not establish sensitivity to the intended target. Use externally specified target ranges and nuisance scenarios; synthetic feasibility failure can block expensive evaluation but cannot prove biological absence. | design-only |
| Physics reproduces the sign | Primarily an identification problem. A matching sign is neither proof of confounding nor evidence against it. Require discrimination of target-plus-nuisance from nuisance-only across declared conditions. If observationally indistinguishable, stop the target claim. | design-only |
| Repeated request for an unavailable mark | Route to capability-gap or hypothesis-proposal, not automatically instrument-defect or frame-exhausted. Name the executable contract change and independent feasibility test. Repetition is scheduling evidence, not scientific justification. | design-only |

### 2.2 What the report may and may not conclude

[measured—reported] The report states that no variant met DONE after the allotted search, that the final rung was never reached, that evaluation banks changed during the run, and that only a subset of the front received the later broader assessment. It also identifies some aggregate quantities without a stored supporting aggregate artifact. These are explicit limitations of the supplied record.

[design-only] Historical pass counts under different banks are not a common-test leaderboard. Separate "passed at evaluation time" from "passes the final frozen cohort." Include missing evaluations as unknown, and separate duplicate outputs from distinct candidates. An 11-item mechanical pass count also does not exhaust a contract containing additional judgment-based requirements. Preserve per-criterion vectors and contract versions rather than ranking by count alone.

[design-only] The report's use of "MDE" needs correction. A maximum over a scaled jackknife error, sampled-null extremes, and selected perturbation responses is an operational detection envelope unless calibrated against specified false-positive and false-negative rates under a declared model. Its components have different meanings. Increasing the number of null draws can increase their maximum and thus the gate threshold even without any scientific change. Specify whether the intended quantity is a fixed quantile, a worst-case stress envelope, or a statistically calibrated detection threshold.

[design-only] Similarly, |observed| + envelope is not automatically an upper confidence bound or an exclusion limit. Such a conclusion would require justified coverage or a valid deterministic bound on all relevant error, neither supplied by a finite probe list. The report appropriately disclaims coverage, but "ruled out" and "underpowered null with bounds" still overstate the result. Suggested replacement: "No candidate met the specified acceptance criteria. The reported sensitivity envelopes summarize the tested controls and perturbations; they do not exclude an underlying effect or establish a confidence bound."

[design-only] "The data are the main ceiling" is plausible as a working diagnosis, but not identified by this run: scorer flaws, incomplete operator coverage, changing banks, and lineage concentration also constrain the outcome. Distinguish deficient sensitivity under tested controls, insufficient independent information, and nonidentifiability from nuisance mechanisms. No orchestration mechanism creates independent observations or separates exactly observationally equivalent mechanisms. More samples can improve precision without necessarily resolving nonidentifiability.

[design-only] A further logical correction: failure to meet a sufficient condition such as a Dobrushin contraction criterion does not by itself prove the opposite property, including "supercriticality." Likewise, failed attempts to construct a powered nesting-preserving null do not prove none exists. Report "the stated sufficient-condition certificate was not obtained" and "the attempted constructions failed," respectively, unless an additional applicable theorem supplies the stronger conclusion. This is a critique of inference form, not a new analysis of the underlying observations.

### 2.3 Two discovery changes and one honest-stop change

[design-only] The highest-priority low-cost changes are below. Each row is fewer than 60 words. "Discovery" means improving the prospect of a valid methodological candidate, not establishing a biological finding from these records.

| Priority / purpose | Concrete change | Failure prevented | Evidence |
|---|---|---|---|
| 1 — Discovery | Add a controller-run scorer wrapper: frozen multi-seed manifest, explicit sign and unit contracts, full case inventory, and hash-bound raw receipts. Keep robustness separate from effect. Use a distinct synthetic validation set after selection. | Search optimizes a lucky seed, arbitrary scale, missing case, or sign-blind score. | design-only |
| 2 — Discovery | Add a small independent synthetic challenge matrix: nuisance-only, target-only, and target-plus-nuisance over prespecified amplitudes, including coupling/partial-volume cases where relevant. Require specificity and sensitivity before expensive evaluation; candidate authors cannot choose their sole positive control. | A variant passes its own easy twin or mistakes nuisance structure for the target. | design-only |
| 3 — Honest stop | Add HALT(UNINFORMATIVE_FOR_CONTRACT): unresolved required identification/sensitivity obligations block completion; reports must state tested scope and cannot emit exclusion language without a validated bound. Distinguish exhausted search budget, inadequate instruments, and unmet information needs. | Unsupported absence claims and endless search to repair an information deficit. | design-only |
| 4 — Trust | Import command results and human approvals from trusted channels; bind them to artifact, action, and policy hashes. Treat agent-reported exit codes and by: human as assertions until authenticated. | Structurally valid but fabricated acceptance records. | design-only |
| 5 — Recovery | Invalidate the transitive dependency closure, withdraw affected accepted status, preserve historical records, and re-admit only when dependencies and revised scope warrant it. | Stale keeps survive new evidence and unchanged checks repeatedly pass. | design-only |
| 6 — Cost | Replace verbatim gate-agent relays with direct driver calls where supported; record every attempt and reserve final evaluation. Benchmark screened-out candidates on a small blinded audit sample. | Hidden overhead and cheap screens silently eliminating valid work. | design-only |

[design-only] These first two changes mostly reuse the described scorer and synthetic-probe infrastructure. Their marginal cost is additional deterministic evaluation plus human specification/review; neither requires a new persistent agent role. The brief lacks execution timings, so no numerical runtime saving is claimed. Keep the matrix small and preregister its scope. The stop rule applies to this contract and instrument configuration; it must not become "this research question is impossible."

## 3. Cost, fidelity, and the rethink protocol

### 3.1 Account for the run, not just an average round

[design-only] The table's 7–18 call range is arithmetically compatible with its listed row extrema, but it does not specify a complete dispatch tree. Its cheap-tier rows span 3–6 calls (gate 2–4 plus screen 1–2), while the prose says 3–5; a policy restriction may explain the difference, but must be stated. "Typical 9–11" is a forecast unless backed by v4.2 receipts. Up to two keeps with the second re-judged also needs an explicit branch; it is not automatically included without extra calls.

[design-only] Use:

C_run = C_setup + C_admission + Σ(C_round + C_retry + C_repair + C_rebaseline) + C_final + C_closure.

[design-only] For each model attempt, record model/version, uncached input, cache-read input, cache-write input if billed separately, output/reasoning usage as exposed by the host, and actual charge. Add deterministic compute and human effort as separate quantities. Record elapsed critical-path time separately from summed worker time. Unknown usage remains unknown; call counts are a fallback workload measure, not interchangeable with cost. Divide by verified keeps only as a secondary measure: when there are no keeps, report total cost and outcome rather than an undefined ratio or suppressing the run.

[design-only] Specifically missing or ambiguous costs are baseline S and its Check, admission controls, final held-out assessment, cross-family review, second-keep re-evaluation, serialization/schema repairs, dropped candidates, retries, new-claim verification, nested DERIVE repairs, probe authorship/calibration, bank rebaseline, rethink/meta calls, resume reconciliation, and final report correction. A gate-relay cap bounds a category; it does not make calls above it cease to be incurred or turn them into "not a budget line." Reserve before dispatch and count failed attempts.

[design-only] "A completed S costs zero" should read "no subsequent search rounds are needed." S, its independent assessment, setup, and closure still cost resources. Likewise command execution may use zero model tokens while consuming CPU time, latency, and agent interaction. A command invoked through a model-controlled tool cycle may also induce another model turn. Count the actual host events, not only named subagents.

### 3.2 Caching is an optimization, not a budget guarantee

[design-only] An identical rendered GROUNDING/rubric is only part of the effective request. Cache reuse can fail when earlier system/tool content, tool schemas, role/model configuration, prefix serialization, or timestamps change; when provider cache thresholds or routing requirements are not met; or when cache lifetime expires. Instrument and policy amendments may intentionally change the prefix. A different model family does not share that cache by default. Provider behavior must be verified from host receipts rather than inferred from visible prompt similarity.

[design-only] Cache reads may still be billed, generated output remains work, and shorter prompts can reduce the cacheable portion. Keep stable content before varying candidate material where supported, but never retain stale rubric content to preserve a cache hit. Budget assuming the documented worst permissible cache behavior, then report observed savings. No particular provider TTL or current pricing is assumed here.

### 3.3 Role boundaries still leak authority and information

[design-only] Generator-run commands are useful development feedback but not an acceptance receipt. A generator can run against different bytes, omit a failing case, misreport an exit code, or branch on visible test context. Have the driver execute immutable acceptance commands in a restricted environment, capture outputs directly, and bind them to the submitted artifact hash. Separate public development tests from protected final tests. In particular, a reported practice of object-identity-based behavior is a reason to expose an explicit execution interface and test equivalent inputs under varied object construction—not to trust reported exits more strongly.

[design-only] "Verifier only when the variant declares new claims" gives the writer authority to bypass verification. A diff can strengthen a claim, drop an assumption, change a unit, or alter applicability without adding a new sentence. Use a claim/dependency manifest plus independent change classification; conservatively review edits to claim-bearing material. A screen's false rejection cannot be repaired by later judges who never see the candidate, so screen conservatively and audit a bounded sample of rejections.

[design-only] An A/B diff is not fully blind: additions/deletions disclose ancestry, can frame the patch as an improvement, and can omit the context needed to evaluate consistency. Give judges randomly labeled old/new affected sections with shared necessary context, and an explicit dependency summary. A neutral diff can be supplemental. AB/BA checks address order, not missing context or exposure. Whole-document acceptance still needs a final consistency check even if local comparisons remain section-scoped.

[design-only] PLAYBOOK and LESSONS pointers are indirect information channels. Resolved content may reveal ancestry, favored families, historical judgments, per-case outcomes, or held-out feedback even when the archive itself is hidden. Log exact input manifests, sanitize role-specific lesson views, and constrain actual file/tool access. The red team can infer past scoring information from annotated front code and summaries; remove unnecessary score annotations. A fresh role name or generated brief does not establish capability separation.

[design-only] The refuter needs the claim's assumptions, definitions, and necessary derivation dependencies, not only the revised sentence and previous finding. Otherwise narrow context can miss a new defect introduced by the repair. Conversely, preserving independence does not require hiding legitimate mathematical premises. Human authority must be verified outside agent-editable JSON. These controls establish accountable access and authority, not proof that all semantic bias has disappeared.

### 3.4 New evidence requires withdrawal and repair before recheck

[design-only] evidence → invalidated check → re-check is necessary but insufficient. An unchanged invalid instrument can reproduce the same pass. Also, records described as "context" can materially change next by invalidating, suspending, or resolving obligations; those records are state-changing inputs and need schema, authorization, provenance, and reference validation appropriate to their consequence.

[design-only] Use this minimal sequence:

1. Evidence intake: assign a stable ID, provenance, affected claim/instrument hypotheses, and triage status. A credible applicability challenge suspends dependent acceptance before final adjudication; not every source automatically invalidates every result.
2. Dependency closure: compute affected claims, Checks, selected versions, frontier membership, descendants, and admission protections. If scope is unresolved, suspend the potentially affected acceptance boundary conservatively.
3. Withdraw current authority: mark affected keeps/COMPLETE status unsupported or superseded while preserving the historical events. Notify downstream consumers of the status change. Unaffected siblings need not be discarded.
4. Resolve: classify as rejected challenge, artifact repair, instrument recalibration, contract amendment, or information gap. Resolution requires evidence; it is not a self-authored resolved: true flag.
5. Re-evaluate under a valid cohort: rebuild affected results after repairs. Re-admit if S's protected criteria, target scope, budget viability, or acceptance contract changed; otherwise reuse unaffected valid evidence.
6. Recommit or halt: reselect eligible accepted work with current evidence, or issue a scoped unresolved exit. Final assessment and reporting follow the revised status.

[design-only] "Suspended criteria are excluded from targets" also needs refinement: exclude them from acceptance and score optimization, but permit explicitly authorized remediation work targeting the suspension. Otherwise the controller can prohibit the very repair needed to unsuspend them. Evidence arriving after exit should create a linked supersession/review event; terminality cannot imply permanent scientific validity.

### 3.5 Failed paths need a decision before resuming work

[design-only] Prefer HALT → bounded rethink proposal → authorize revised plan → re-admit if needed → resume. The current resume → mandatory rethink is safe only if resume enters a review-only state with no generation authority. Writing a rationale is not sufficient: require the rejected assumption or route, evidence supporting that diagnosis, a genuinely changed action, expected discriminatory result, cost ceiling, and stop condition. The next trial should distinguish explanations, not merely restate the aim.

[design-only] Remove the automatic exhausted-family exclusion, which remains in §15 despite the earlier critique. An unsuccessful budget allocation rejects neither a family nor every hypothesis in it. Likewise, hypotheses_rejected should distinguish falsified, instrument-invalid, inconclusive, and untested. A weaker DONE may define a legitimate new task, but cannot retroactively certify the failed original task. An unexecuted operator is a proposed next test, not a reason that resumption must occur.

[design-only] Recommended default: stop the current scientific acceptance attempt when the contract cannot be resolved with its available information; allow a separately scoped, synthetic-only instrument or estimand study if authorized. This preserves a useful research output—tested limitations, calibrated mechanisms, and a discriminating next experiment—without converting search persistence into evidence.
