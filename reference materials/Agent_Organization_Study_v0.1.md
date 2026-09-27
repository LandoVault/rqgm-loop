# Agent organization study v0.1

Date: 2026-09-25. Status: designed, not executed. Separate extension; no modification of the earlier frozen protocol is claimed.

## Question and challenge

Under which task conditions does separating role contexts, then introducing asynchronous execution, improve independently verified outcomes at matched resources?

An agent process, a model invocation, a role, a memory store, and a concurrent worker are different objects. Event listeners can wait without consuming inference tokens. If persistent and newly invoked workers receive identical model inputs and state, process lifetime alone should not change the intended model-call distribution; caching, latency, transport, hidden state and nondeterminism can still differ. Establish this systems-level equivalence before attributing gains to persistent agents.

The scientific contribution would be a predictive relationship between task properties and useful organization, not an assertion that one organization universally wins. The literature already compares single- and multi-agent systems.

## Primary arms

| Arm | Context and execution | Contrast |
|---|---|---|
| A | One role-switching worker, common conversation, sequential calls | Strong single-agent baseline, same tools and role instructions |
| B | Four isolated role contexts invoked on demand, serialized execution | Effect of separating role contexts and associated information routing |
| C | Same isolated role contexts, event-triggered parallel execution, at most four concurrent calls | Additional effect of asynchronous scheduling |

All arms have the same durable scientific state, source-search capability, candidate proposal tools, deterministic verification gates, model version and overall budget. Scheduling code is shared where the design permits; document unavoidable differences. Candidate propositions and retrieval queries remain model-selected; no fixed sequence of scientific moves is imposed. The scheduler enforces resource and commit contracts.

First run a lifecycle equivalence check using mocked model outputs: persistent event subscribers versus on-demand workers supplied with identical explicit state must generate equivalent commits under a fixed event schedule. Report runtime and cache overhead separately. A live lifecycle ablation follows only if the implementation exhibits a relevant difference. Do not give the persistent arm extra memory and call the difference persistence.

## Five small task families

1. **Sequential dependence:** short algebraic derivations with later steps genuinely depending on earlier results; verify with symbolic identities and explicit domain restrictions.
2. **Independent branches:** separable calculations or independent candidate checks followed by aggregation; compare the same total work, not four times as many attempts.
3. **Coupled constraints:** small linear systems or consistency puzzles with shared variables, where local solutions must agree globally.
4. **Knowledge gaps:** generated problems that require an unfamiliar, synthetic definition or lemma available only in a controlled document corpus. Include distractors and cases where the required information is absent. All arms have equal retrieval access. Score applicability and justified abstention, not citation count. Later external-web replication is separate because web state changes.
5. **Revisions:** introduce a changed assumption at a fixed logical checkpoint; measure selective invalidation, reuse and final correctness. Deliver equivalent information at that checkpoint in every arm; evaluate timing effects separately.

Prepare eight held-out instances per family with balanced difficulty, plus separate development examples. Freeze instances and checks before comparative execution. Use three stochastic repeats per instance and three arms: 360 pilot runs. This is an exploratory pilot, not a power calculation or evidence of significance. Include negative controls where no coordination or retrieval is needed.

For the next confirmatory study, choose sample size using pilot variance and a declared minimum useful effect. Generate fresh held-out instances. Do not treat repeated runs of the same problem as independent problems.

## Resource controls

Proposed pilot ceiling per run: 24,000 provider-reported total tokens across every model call, including reported reasoning tokens; 24 tool calls; 60 aggregate CPU seconds for bounded local tools; and a 10-minute emergency wall-time ceiling. These ceilings must be checked on development tasks and frozen before held-out testing. Provider-specific context limits, cache accounting, model ID, sampling settings and exact prices are unresolved execution prerequisites. Do not report the pilot as fully preregistered until these are recorded.

Count input, cached input, output and reported reasoning tokens separately, avoiding double counting when output includes reasoning. Include planning, routing, retries, summaries, failed calls and verification-model calls. Reserve token allowances before concurrent calls so Arm C cannot overshoot the shared budget. Missing usage is missing data, not zero. Report currency cost and CPU time separately because tokens are not equal compute across all implementations.

Use the same model throughout the first comparison. Randomize arm order by task block and limit cross-run infrastructure contention. Reset memory between tasks. Never transfer answers or source discoveries between arms. Permit the single-agent arm the same total reasoning allowance and tools. Charge shared-state serialization and context rebuilding. Retain all timeouts and failures in denominators.

## Outcomes and inference

Primary: proportion of tasks completed correctly and verified within the common resource ceiling. Verification is independent of the acting agent; no majority vote serves as ground truth.

Secondary: false acceptance, appropriate abstention on insufficient information, latency, full token use, currency cost, repeated tool work, stale-result rejection, communication load and sensitivity to changed assumptions. Report quality versus cost curves in the later multi-budget study, not only success per token (which can reward early abandonment).

Compare A versus B and B versus C on paired task instances. Report per-family effects with task-cluster bootstrap confidence intervals; repeats remain nested within task. Label exploratory subgroup findings and avoid selecting a universal winner by averaging away opposing effects. For generalization, repeat with a second model and an independent task set after the pilot, not by assuming one model establishes a law.

Hypotheses: isolation may help when context interference is substantial; concurrency may reduce latency on parallel work; coordination may hurt sequential or densely coupled work. These are hypotheses, not current findings. Retain a simpler organization unless the measured quality/cost/latency tradeoff justifies complexity for the relevant task.

## Scale and physics transfer

Only after the small study, stress the scheduler at 16, 64, 100 and 200 logical subscribers using replayed events. This tests queueing, event delivery, memory and commit correctness, not collective LLM intelligence. Live-agent scaling is a separate stage with explicit shared budgets and sufficient independent work.

The Yang–Mills reconstruction in this package is a known-answer integration fixture. It cannot establish discovery due to source consultation and likely pretraining familiarity. Its first run evaluated six supplied candidate forms (four rejected) and passed six additional symbolic verification groups in approximately 33.38 seconds. No organization comparison or token-efficiency test has been run. The candidate grammar is hand-supplied and does not implement autonomous knowledge expansion.

## Verified literature and relevance

- **AgentDropout**, ACL 2025: dynamically removes redundant agents and communication. Relevant to avoiding fixed participation by every role; not a direct lifecycle comparison. https://aclanthology.org/2025.acl-long.1170/
- **Why Do Multi-Agent LLM Systems Fail?**, NeurIPS 2025 Datasets and Benchmarks: supplies a failure taxonomy useful for diagnosing coordination and termination failures. https://proceedings.neurips.cc/paper_files/paper/2025/hash/b1041e52d3be19f0a9bc491657488e4a-Abstract-Datasets_and_Benchmarks_Track.html
- **Towards a Science of Scaling Agent Systems**, inspected arXiv v3, April 8, 2026: compares five architectures across multiple benchmarks with standardized resources and reports task-dependent effects. Cite this inspected version; journal publication metadata was not verified from its publisher during this search. https://arxiv.org/abs/2512.08296v3
- **Scaling LLM-Driven Multi-Agent Systems: Design Principles and Architectural Scalability Analysis**, July 30, 2026 preprint: examines four configurations on terminal tasks and reports bounded benefits and consistency difficulties. Within the requested June 25–September 25 window; conference acceptance not verified. https://arxiv.org/abs/2607.27942

The two verified conference publications are older than the requested three-month window. None of the inspected sources establishes the precise persistent-listener versus on-demand-equivalent-worker conclusion. This targeted search is not an exhaustive novelty review.
