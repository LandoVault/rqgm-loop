# Cross-family review of RQGM v3.1

**[measured — document inspection]** Reviewed the SKILL.md, INITIATOR.md and DESIGN.md embedded in `consult-3-request.md`, against the v2 text supplied in consultation 1 and the recommendations in consultations 1–2. Date: September 26, 2026. No repository code, auditor, raw journal, decision-scenario outputs, or pilot outcomes were supplied or executed here.

**[measured — attributed reports, not independently verified]** The request reports 110 attack archives, 181 auditor selftests, a ten-round meta-run, 16/16 pairwise preferences, an E2 failure on five of six criteria, subsequent reduction to two failing criteria, and no scored pilot runs yet. Those are maintainer-reported observations. I do not infer an auditor pass rate, scientific improvement rate, or successful implementation of the pending checker changes from them.

**[design-only]** Labels apply to the entire paragraph or table row. `measured` denotes explicitly scoped inspection or attributed observations; `literature` would denote an externally substantiated finding; `design-only` denotes judgments, counterexamples and proposed rules, not tested effects. No new literature claim is needed for this review.

**[design-only]** Review disposition: **v3.1 is preferable to v2 as a design, but does not pass the stated release criteria.** Retain it as a frozen experimental arm if desired; do not describe it as executable and fully auditable from the supplied contract. Cross-family review adds another assessment, not a correctness oracle or an independent replication of the pilot.

## 1. Criterion judgments

| Criterion | Verdict | Decisive reason and scope | Label |
|---|---|---|---|
| d1 — guardrails | **FAIL** | Human-only authority, separated roles, explicit UNKNOWN/ERROR handling and held-out restrictions improve the written contract. However, the primary-source-only rule treats original derivations and proposed mechanisms as unsupported facts, contrary to domain-agnostic operation. The OPEN-waiver resume shortcut can also enter Stop without reestablishing current final-rung Check eligibility. | design-only |
| d2 — executable | **FAIL** | Several next decisions lack defined inputs: first-round “twice the costliest round,” conflicting per-criterion AB/BA ratings, post-Verifier stripping/replacement and rechecks, and accounting/reconstruction of a partially logged round. Generic “fail closed” does not identify the gap, permitted recovery, or next state for each. | design-only |
| d3 — parity | **FAIL** | SKILL triggers Check on a **generator** DONE claim; the paste triggers it when **the orchestrator believes** DONE holds. Those can occur at different steps and costs. SKILL says read GROUNDING first; the paste reads it only on fresh setup. These are operational differences, even though most clauses align closely. | design-only |
| d4 — auditable | **FAIL** | Required records omit some facts needed for recomputation: v0's full content/reference, per-order criterion ratings, non-round cost records and attempt completion before round logging. The explicit unauditable list does not cover all of these. Pending checker work is not delivered audit coverage. | design-only |
| d5 — honest | **FAIL, narrowly** | DESIGN's evidence separation and non-guarantees are substantial improvements. But Output's common `pass` status “by ... judges or held-out” does not require the explicit `preferred`/`verified` distinction in this criterion. COMPLETE must identify the active amended/waived objective, and held-out prompt novelty must not be reported as independent task verification. | design-only |
| d6 — cost | **UNKNOWN** | The consultation names d6 but supplies no acceptance definition. If it means full decision-cost accounting or a computable admission rule, the current text fails those interpretations; if it means demonstrated efficiency, the required comparative evidence is not supplied. Do not silently invent the criterion after judging. | design-only |

**[design-only]** Scope of d1: I am not claiming that the observed implementation fabricated evidence or allowed unauthorized escalation. This is a textual counterexample assessment against a conjunctive criterion. An unverified original mathematical claim needs an appropriate proof/check, while a proposed mechanism needs a design-only label and assumptions; neither universally requires a published source.

**[design-only]** Concrete transition counterexample: a run halts OPEN below the final rung; all open gaps are waived; Resume says “OPEN with all gaps waived → Stop.” Stop can consume held-out prompts before a final-rung Check. The output rule may still force PARTIAL, but consuming final evaluation in an ineligible state violates the intended lifecycle. Re-enter Check/Boundary, not Stop directly.

**[design-only]** Concrete audit counterexample: Judge 1's overall AB and BA preferences agree, but its rating of a protected criterion reverses. The archive stores overall order results and one `criteria` map; it does not require both per-order maps. A reviewer cannot reconstruct whether there should have been an UNKNOWN/veto. Declare the aggregation rule and retain its inputs.

**[design-only]** Held-out status of this review: it is a fresh cross-family assessment of the supplied text. Once the maintainer uses these failure reasons to revise the text, this review is development feedback. It must not be reused as an untouched final assessment of the resulting revision.

## 2. Pairwise judgment against v2

| Criterion | Pairwise verdict | Reason; improvement is not threshold passage | Label |
|---|---|---|---|
| d1 — guardrails | **v3.1 better** | Clearer human authority, external role execution in plain chat, protected-item UNKNOWN veto, explicit check-file restrictions, and optional versus required gaps. Residual domain and transition defects remain. | design-only |
| d2 — executable | **v3.1 better** | More explicit retry, pruning, error-round, Check and output rules reduce unspecified behavior. It still lacks enough detail to pass d2. | design-only |
| d3 — parity | **UNKNOWN** | The previous consultation did not supply v2 INITIATOR.md. I cannot compare old skill/paste parity to new parity from the old SKILL/DESIGN alone. | design-only |
| d4 — auditable | **v3.1 better** | Richer round, citation, probe, Check and held-out records plus explicit auditor limitations. This is a contract-level preference, not an inspection of the auditor implementation. | design-only |
| d5 — honest | **v3.1 better** | Stronger separation of design review, old runs, task validation and non-guarantees; explicit first held-out outcome and PARTIAL status. Reporting semantics still need repair. | design-only |
| d6 — cost | **UNKNOWN** | No defined criterion or comparative cost evidence. More complete bookkeeping could increase overhead while reducing failures; neither direction has been established here. | design-only |
| Overall | **v3.1 better, conditional design preference** | Prefer its clarified safeguards and evidence boundaries for further testing, without certifying it against the six-criterion release gate. | design-only |

**[design-only]** This illustrates why 16/16 pairwise preferences can coexist with a failed absolute Check: “better than the incumbent” and “meets all requirements” are different predicates. The reported votes alone do not distinguish genuine local improvements from agreeableness, inadequate coverage, or both. Do not diagnose agreeableness solely from a unanimous win count.

## 3. Traceability and the auditor/enforcement decision

### 3.1 Earlier eight replacement blocks

| Earlier recommendation | Status in supplied v3.1 | Do I accept the adaptation/rejection? | Label |
|---|---|---|---|
| 1. Correctness versus preference | **Adapted** | Partly. `command/source/judges` is useful, and commands gate regressions. But a preference panel still governs promotion even for a newly correct command-only candidate. This is a conservative search policy, not proof of superior verification. Report its stalls and preserve distinct outcome labels. | design-only |
| 2. Incomplete/failed evaluation | **Adopted in intent; adapted in semantics** | Largely. UNKNOWN, ERROR and one retry are now explicit. Specify per-order criterion aggregation and exactly which missing/error result invalidates a Check; do not leave those to auditor interpretation. | design-only |
| 3. Verification of original work | **Rejected/not incorporated** | No. “Every claim against a primary source ... never loop-written text” retains the problem. Novel derivations and proposed designs need typed evidence paths, not citation-only truth tests. | design-only |
| 4. Protect final assessment | **Adapted** | Partly. External human-held prompts, first-outcome reporting, changed-best requirement and spare prompts help. After primary feedback drives repair, primary is development evidence; spare prompts test new evaluators, not necessarily new task cases. | design-only |
| 5. Budget admission/accounting | **Adapted** | Accept round caps and nulls as an explicitly weaker mode. Reject “twice the costliest round” as a complete admission contract without initialization and non-round costs. It is a heuristic, not a reservation or bound. | design-only |
| 6. Exact versions and resume | **Mostly rejected; coarse adaptation** | Round-level history is an acceptable declared recovery trade-off, but cannot support a no-duplicate-work guarantee. Machine-computed hashes should remain available where code exists; rejecting model-invented hashes is not a reason to reject computed artifact identity. | design-only |
| 7. RETRIEVE versus REFRAME | **Partially adapted** | Removing section-age targeting and allowing human-approved restructures helps. A restructure is not necessarily a conceptual reframe, and there is still no explicit missing-evidence/inadequate-formulation distinction. Do not claim this capability is implemented. | design-only |
| 8. Version the rising bar | **Adapted** | Partly. Human amendments and Check invalidation appear, but no mandatory spec/rubric version binding, and waiver-to-Stop bypasses requalification. Recheck under the changed objective before final assessment. | design-only |

### 3.2 C01–C17 controller recommendations

**[design-only]** “Adopted” below means stated behavior in the supplied contract, not code enforcement. The owning controller was explicitly rejected; a read-only auditor cannot itself prevent a bad write or external call.

| Invariant | Status | Assessment | Label |
|---|---|---|---|
| C01 complete required gates | **Adapted** | Explicit failure states and protected veto; missing record details and pending auditor changes limit recomputation. | design-only |
| C02 candidate/parent/rubric binding | **Adapted** | Version and rung fields help, but exact content and per-order evidence binding are incomplete. | design-only |
| C03 result-ID uniqueness | **Rejected/deferred** | Per-call IDs absent. Accept only as a declared limitation; retries and duplicates cannot be reliably distinguished without identity. | design-only |
| C04 no rerun of recorded completed calls | **Rejected** | Rerunning an unfinished round intentionally allows repeated completed substeps. Report that cost rather than claiming this invariant. | design-only |
| C05 reservations within capacity | **Rejected/adapted to heuristic** | Historical-round admission is not a shared reservation ledger. Serial execution reduces overlap, not the cost of a large next call. | design-only |
| C06 unknown usage liability | **Partially adapted** | Nulls avoid falsely reporting zero, but no retained liability is required. Missing spend cannot support a verified remaining-budget claim. | design-only |
| C07 artifact durability before acceptance | **Rejected** | Log-before-TARGET reduces one failure window but does not supply immutable candidate storage. Resume needs reconstructible v0 plus ordered deltas or snapshots. | design-only |
| C08 final-rung complete gates | **Adapted** | Output distinguishes PARTIAL, but eligibility to enter Stop can be bypassed through waived OPEN recovery. | design-only |
| C09 human-authorized objectives | **Adopted in prose** | Human-only amendment is explicit. The document honestly disclaims authenticity of relayed decisions; do not upgrade it to authenticated authority. | design-only |
| C10 assigned role authority | **Adapted** | Separate contexts and human role execution are required; not authenticated and declared unauditable. Adequate for a cooperative experiment, not adversarial enforcement. | design-only |
| C11 dependency invalidation | **Partially adapted** | Changes to best/rung/DONE invalidate Check, but source or grounding changes are not explicitly included. | design-only |
| C12 one acceptance per frozen round | **Adapted** | At most one keep is explicit. Require all candidates to name the same immutable round parent. | design-only |
| C13 preserve evaluation exposure | **Adapted** | First result and primary/spare attempt are retained. Explicitly mark primary exposure after feedback, rather than describing both attempts generically as untouched held-out validation. | design-only |
| C14 torn-tail recovery | **Partially adapted** | Set-aside rule is useful, but recovery of incomplete `round/version/TARGET` sequences and mid-round costs remains underspecified. | design-only |
| C15 single local writer | **Adopted in prose** | “Only you write” defines ownership; there is no lock or isolation guarantee, which is acceptable if stated. | design-only |
| C16 preserve retries/unknown charges | **Partially adapted** | Retry counters exist, but no complete attempt-level cost evidence or completion-unknown treatment. | design-only |
| C17 permit incremental repair | **Adopted** | Shared command failures need not reject a variant; imperfect v0 may be improved. This resolves the all-or-nothing acceptance trap, though preference-only promotion may still obstruct command improvements. | design-only |

### 3.3 Auditor plus promotion: sound staging, not equivalent protection

**[design-only]** I accept the read-only auditor as a staged experimental choice, **not as an equivalent substitute for enforcement**. Code-free portability is a legitimate product constraint, and a serial loop does not need distributed machinery. However, the architects' preference votes do not establish that prose-first is safer or cheaper, and my proposed single-writer controller did not require distributed concurrency infrastructure.

**[design-only]** An auditor recomputes an expected decision; it does not own the decision. If a violation is detected only after applying an edit or dispatching a costly call, it cannot prevent that effect. If shell-mode audit failure mandatorily blocks the next action, that is already a form of enforcement at a checkpoint. Name the boundary accurately: retrospective detection, pre-action gate, or full acceptance authority.

**[design-only]** Resolve a documentation tension before scoring: the paste says an audit violation pauses the loop, whereas the optional-audit description says “nothing depends on it.” Stage 3 P is explicitly no-audit, and P2's audit mode is not stated in the summary. Freeze `audit=off/posthoc/online-blocking` per arm. The same label must not cover both an unaided prose run and one receiving corrective audit feedback.

**[design-only]** The promotion rule needs four qualifications:

1. **[design-only] Severity:** a single reproduced false COMPLETE, protected-file mutation or unauthorized objective change should block release of that behavior, irrespective of a 3/30 threshold. The threshold can govern discretionary enforcement investment; it should not excuse known critical failures below it.
2. **[design-only] Attribution:** “≥3/30 errors in any context” does not identify which rule to promote unless failures are mapped to rule IDs. Freeze class mapping and adjudication rules before examining model answers.
3. **[design-only] Independence:** derive expected answers from the prose contract through independent adjudication before checking the auditor. An answer key originating from `audit --pending` can make auditor and key agree on the same mistake; human review must resolve that risk rather than rubber-stamp it.
4. **[design-only] Timing:** if Stage 1 triggers an enforcement change, the scored policy has changed. Freeze a new version, audit mode and manifest amendment before pilot scoring; do not mix outcomes from pre- and post-promotion procedures under P2.

**[design-only]** Three contexts are repeated exposures within one model family, not three independent populations. Stage 1 can reveal scenario-specific misapplication; it cannot certify that unseen rules or recovery states are safe. “No threshold crossed” means no trigger in that test, not proof that enforcement is unnecessary.

## 4. Top five remaining defects and smallest fixes

**[design-only]** Each quoted fix is proposed wording of at most 40 words. These repairs do not automatically resolve every release-criterion failure identified above.

### 1. Verifier can alter an already checked candidate, and its evidence rule is too narrow

**[design-only]** Failure: commands run first; Verifier then strips or replaces claims; the revised bytes are not explicitly rechecked. Citation-only verification also excludes original derivations and designs.

> Classify claims as empirical, mathematical, or proposed. Use appropriate sources, derivations/tests, or design labels. The Verifier returns findings, never edits candidates. Any correction creates a new candidate; rerun affected gates before judging its exact text.

### 2. “Check files” can include the very code being repaired

**[design-only]** Failure: “every file it runs” can include target implementation modules imported or executed by tests. Making that entire set immutable would make T1 impossible or depend on an unstated interpretation.

> Distinguish immutable verifier assets from mutable target code. Freeze tests, expected outputs, and verifier configuration; allow declared target files to change. Log both sets. A check's execution dependencies are not automatically protected check files.

### 3. Required archive cannot fully reconstruct decisions or spend

**[design-only]** Failure: no explicit initial artifact snapshot, incomplete AB/BA criterion evidence, missing non-round expense records, and uncertain completed substeps after crashes. Auditor counts cannot repair missing inputs.

> Retain v0 and every judged artifact, both orders' full ratings, immutable input versions, and attempt outcomes. Record setup, probes, Checks, held-out and recovery costs separately. Where unavailable, declare the affected decision or total unauditable, not merely unaudited.

### 4. Budget admission is undefined initially and can starve required finalization

**[design-only]** Failure: there is no costliest observed round before round one; historical cost is not a bound; remaining probes and final checks are not covered explicitly. Null usage prevents verified remaining-token calculations.

> Define a first-round allowance and final-check reserve before execution. Charge every phase. Treat historical round costs as heuristics, not bounds. Unknown spend makes remaining-token capacity unknown; pause or explicitly use a round-only budget approved by the human.

### 5. Recovery/amendment transitions can bypass current eligibility

**[design-only]** Failure: waived OPEN can route directly to Stop; changed sources do not invalidate checks explicitly; parity differs on who triggers a DONE Check.

> After any waiver, source, objective or rung change, invalidate affected results and enter Check, then Boundary; never jump directly to Stop. Use the same explicit Check trigger in SKILL and INITIATOR. Preserve both original and amended completion status.

**[design-only]** Additional release edits: define d6 prospectively; require output fields `verified`, `preferred`, `unchecked`, `waived` and `heldout_assessment` rather than one undifferentiated pass label; specify per-criterion AB/BA aggregation. These are contract corrections, not demonstrated outcome improvements.

## 5. Pilot validity before scoring

### 5.1 Threats that must constrain reporting

| Threat | Required reporting or design clarification before outcomes | Label |
|---|---|---|
| Relay-induced context loss | State that loop arms use a repeatedly reinvoked, archive-only orchestrator. This evaluates the prompt plus serialization/relay system, not an ordinary continuous chat. Record truncation, missing artifacts and context reconstruction separately. | design-only |
| Different orchestration for S/B versus loops | Specify whether S retains context and how B receives source/check results. Differences may be legitimate package differences, but must not be attributed purely to the loop rules. | design-only |
| P/P2 policy drift or inconsistent audit access | Pin actual prompt hashes, auditor version, enforcement mode and Stage-1 promotions for each arm. The Stage-3 summary lists P but not P2; reconcile it with the announced five-arm manifest before scoring. | design-only |
| Frozen manifest versus already executed unscored outputs | State whether any pilot outputs have already been generated or inspected. “Not scored” does not imply no outcome knowledge. If outputs informed revisions, label the affected cells developmental and use fresh cases for confirmation. | design-only |
| 49-call cap and calibration | Disclose which arms determined the “larger minimal complete path,” whose calls count, and rounding. A two-arm calibration may not cover five arms. Count nested model/relay calls and separate tool/CPU costs. | design-only |
| Calls mistaken for matched compute | Equal call ceilings need not equal token/currency/latency ceilings. Report all observed token categories and missingness. If only calls are matched, say matched calls—not matched total compute. | design-only |
| Larger total experiment | Two tasks × five arms × 49 gives a maximum 490 full-cap calls before preparation, half-budget baselines, faults or extra judging. Disclose this changed scope rather than retaining the earlier roughly 200-call description. | design-only — arithmetic from proposed allocation |
| B selection and verifier design | Define how 24 revisions are selected, how many verifier calls occur, and how unverified candidates are handled. Do not let B's selector see the sealed final scorer, or give it an oracle unavailable to loops. | design-only |
| Optional-field T2 co-design | Treat V-versus-P/P2 differences driven by optional OPEN semantics as targeted compatibility tests, not independent evidence of broad advantage. Report outcomes both for core required facts and optional-field handling. | design-only |
| One task per family, one run per cell | Report individual cases, not a population success rate or significance claim. No stable reproducibility estimate, task-level variance estimate or family-wide generalization is available from these cells. | design-only |
| One live model family | Report Claude-family runtime results; this GPT review does not make the live experimental design cross-family. No cross-family generalization follows. | design-only |
| Human proxy versus human-only ownership | A sealed script tests a frozen authorization policy, not real human judgment. Identify what it can approve, waive, restructure or escalate and keep that identical where applicable. Attribute proxy approvals separately. | design-only |
| Scorer scope | Hidden tests and controlled factual answer keys support their exact cases. They do not verify all possible program behavior or the loop's broader scientific-discovery claims. Protect scorer integrity from candidate edits. | design-only |
| Retrospective auditor | Separate prose policy violations from scorer failures. Record which auditor rules were pending at run time and what later posthoc versions found; do not describe later coverage as contemporaneous enforcement. | design-only |
| Excluding contaminated runs | Mark affected outcomes invalid for the intended inference, but retain the attempt, cost and contamination event in the accounting. Do not silently remove unfavorable runs and rerun until clean. | design-only |
| Fault timing and recovery | Inject equivalent logical states/faults, not merely the same elapsed second. Keep clean-run comparisons separate from fault outcomes; preserve completed external work and duplicate costs. | design-only |
| Stage-6 threshold | A false-pass rate below 50% is not a reliability certificate. Report defect-specific numerators/denominators and severity, even if the preregistered promotion trigger is not crossed. | design-only |
| Improvements selected on the same feedback | Meta-run critiques, probes and this review are development inputs. Record their cost and freeze the resulting policy before held-out task evaluation. Do not infer a mechanism's causal benefit from a package comparison. | design-only |

### 5.2 Primary endpoint needs a companion

**[design-only]** False completion is an important safety endpoint, but an arm that always returns PARTIAL can score perfectly on it while solving nothing. Report it together with independently correct final artifact, verified required-criterion coverage, correct completion declaration, and actual cost. Keep the preregistered primary label if already frozen; add the companion interpretation transparently before inspecting outcomes.

**[design-only]** Report both false-COMPLETE/all-runs and false-COMPLETE/COMPLETE-declarations, with the latter undefined when there are no declarations. Distinguish an actually correct artifact honestly marked PARTIAL from a wrong artifact confidently marked COMPLETE. A waiver changes the objective; evaluate original obligations and amended obligations separately.

**[design-only]** “P below S or B on any task: no improved claim” is a conservative reporting rule, not a statistical finding. Specify how ties and quality/cost trade-offs are handled, and whether the same rule applies to P2. Avoid declaring broad superiority merely because P2 is not worse in two cells.

### 5.3 The one comparison I would trust most

**[design-only]** **P2 versus P on T1, at the same declared budget, model, relay, tools, initial artifact and audit mode, scored with the same sealed tests.** This is the cleanest available comparison of the revised text against its immediate predecessor because it can hold the surrounding relay and role structure fixed and avoids the known T2 optional-field co-design issue.

**[design-only]** Preconditions: resolve the mutable-target/check-file distinction; freeze P/P2 versions and audit modes; prevent answer leakage; retain failures and usage gaps. If P2 includes online enforcement but P does not, the comparison estimates the combined prompt-plus-enforcement change, not prose improvement alone. If these conditions cannot be met, treat the comparison as confounded.

**[design-only]** Even under those conditions, the trustworthy conclusion is restricted: which output passed the specified T1 checks, at what recorded cost, in these two runs. It does not establish an expected advantage. P2-versus-S/B on T1 is the practical value comparison and should also be shown, but it changes more of the workflow at once.

**[design-only] Final recommendation:** proceed only with explicit experimental labels and repaired/declared ambiguities. Freeze this review as development feedback, settle d6 and the manifest/audit-mode discrepancies before scoring, and preserve both the pairwise preference and the failed absolute gate. Neither should be rewritten to match the other.
