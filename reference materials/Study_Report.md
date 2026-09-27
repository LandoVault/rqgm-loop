# Yang–Mills classical-core reconstruction: executable pilot

Date: 2026-09-25. Scope: bounded symbolic reconstruction and checks, not autonomous discovery or full-paper replication.

## Source and conventions

C. N. Yang and R. L. Mills, *Conservation of Isotopic Spin and Isotopic Gauge Invariance*, Physical Review 96, 191–195 (1954), DOI: https://doi.org/10.1103/PhysRev.96.191.
The accompanying PDF was downloaded from https://eclass.upatras.gr/modules/document/file.php/PHY2129/PhysRev.96.191.pdf . Its five scanned pages include a fragment of the preceding article. Pages 192 and 193 were visually inspected to resolve OCR ambiguity in equations (1)–(5).

We reconstruct the central classical gauge construction using modern Minkowski notation. We do not reconstruct the quantization section or the discussion of particle masses. The executable matrix fixtures use three independent coordinates to test algebraic identities, not a spacetime simulation.

Set T_a = sigma_a/2, [T_a,T_b] = i epsilon_abc T_c, tr(T_a T_b)=delta_ab/2. Take Hermitian A_mu=A_mu^a T_a, a nonzero real constant g, smooth fields with commuting partial derivatives, and psi'=U psi for U(x) in SU(2). Define D_mu=partial_mu-i g A_mu. For action variation assume compactly supported variations or vanishing boundary terms.

The original paper writes psi=S psi', uses x_4=it, and defines the curl with reversed index order. For the connection and curvature formulas the dictionary is U=S^{-1}, A=B, g=e, and F_here=-F_paper. Its decomposition B=2 b dot T also introduces a factor of two relative to coefficients in A=A^a T_a. Do not compare signs or action normalizations without this dictionary.

## Reconstructed derivation

1. **Local symmetry creates a derivative defect.**
   partial_mu(U psi)=U partial_mu psi+(partial_mu U)psi.
   The second term disappears for global transformations but not local ones.

2. **Demand derivative covariance.** Expanding D'_mu(U psi)=U D_mu psi and cancelling the common derivative gives
   A'_mu=U A_mu U^{-1}-(i/g)(partial_mu U)U^{-1}.
   This fixes the connection transformation given the chosen first-order covariant-derivative ansatz. It does not prove that all conceivable formulations must use this ansatz.

3. **Construct curvature from the operator commutator.** Product-rule expansion gives
   [D_mu,D_nu]psi=-i g F_mu_nu psi,
   F_mu_nu=partial_mu A_nu-partial_nu A_mu-i g[A_mu,A_nu].
   Terms containing first derivatives of psi cancel. The commutator is essential for noncommuting generators.

4. **Derive curvature covariance.** Since D'=U D U^{-1} as operators,
   [D'_mu,D'_nu]=U[D_mu,D_nu]U^{-1}, hence F'_mu_nu=U F_mu_nu U^{-1}.
   This analytic operator argument is general; the finite executable fixtures are regression checks, not its replacement.

5. **Choose and verify a classical action.** Cyclicity of the trace makes
   S_g=-(1/2) integral tr(F_mu_nu F^{mu nu}) d^4x
   invariant, equivalent to -1/4 integral F^a_mu_nu F_a^{mu nu} d^4x under the stated normalization.
   Local gauge invariance alone does not uniquely choose this action. We additionally choose the usual lowest-derivative, quadratic-curvature, parity-even gauge kinetic term. Higher-order invariant terms are not excluded by gauge covariance alone.

6. **Vary the action.** With the adjoint derivative D_mu X=partial_mu X-i g[A_mu,X],
   delta F_mu_nu=D_mu delta A_nu-D_nu delta A_mu.
   Antisymmetry and integration by parts yield
   delta S_g=2 integral tr((D_mu F^{mu nu})delta A_nu) d^4x,
   so the source-free field equation is D_mu F^{mu nu}=0.
   Coupling matter contributes its variational current; that sourced calculation is not implemented here.

7. **Consistency and limiting checks.** The Jacobi identity for covariant derivatives implies D_mu F_nu_rho+D_nu F_rho_mu+D_rho F_mu_nu=0. Restricting all A_mu to the same fixed generator eliminates their commutators and recovers Abelian curvature. Expanding the quadratic action produces cubic and quartic gauge-field interactions.

## What the executed loop does

The Python script proposes connection coefficients q=0,+1,-1 in the explicitly supplied ansatz A'=UAU^{-1}+q(i/g)(partial U)U^{-1}; it checks derivative covariance and accepts the passing candidate. It then tests k=0,+1,-1 in F=dA+i g k[A,A], checking curvature covariance. This is two bounded propose/check/accept loops with six candidate evaluations. The generator, ordering, ansatz and checkpoints are hand-specified. Failed candidates are retained in results.json.

Additional checks cover the operator identity for arbitrary smooth SU(2) fields, another local transformation axis, trace invariance, a Bianchi identity fixture, the Abelian limit, and the first variation of curvature. The general action integration-by-parts argument is written above; it is not a machine-checked theorem.

Run `python run_checks.py` with SymPy 1.14.0. The script writes exact symbolic pass/fail results and its elapsed runtime to results.json. There is no floating-point tolerance. Timing is one local run, not a benchmark. No token counts are available. No original RQGM executable, Lean library, controlled baseline, or live-agent scaling test was used.

## New-resource discovery requirement

The runtime design must allow a worker to report a knowledge gap, propose a query or a new representation, retrieve a source, assess applicability, and offer a versioned state update. The topic, query and candidate model should not come from a fixed reading list. Provenance, budgets, verification requirements and commit rules can remain explicit contracts.

Distinguish missing support for a known claim from a candidate space that is inadequate. The latter may require new variables, operators or hypotheses, not another pass through existing candidates. Retrieval provides candidate evidence, not automatic acceptance. If resources remain insufficient, retain an unresolved result rather than manufacture certainty.

In this pilot, source retrieval and interpretation were performed by the assistant, not triggered autonomously by the script. A concrete insufficiency identified in the reconstruction is that gauge invariance alone does not fix the complete action. The extra action restrictions above are exposed rather than silently treated as consequences. A subsequent test should deliberately withhold a required identity or convention and measure whether the controller retrieves an applicable source or correctly abstains, against a no-retrieval control. That experiment has not run.

## Agent organization for the next implementation

Use a deterministic, event-driven scheduler and durable shared state. Role-specific model calls run on demand against a relevant versioned snapshot and return a proposed patch plus evidence. Role memory can persist without a continuously running model. A subscriber waiting for events need not consume inference tokens; polling the whole state or repeatedly waking every role can be expensive.

Use one worker for tightly sequential derivation and separate workers for genuinely independent candidate tests, source searches, or tool execution. Budget concurrency according to ready work; 200 configured roles should not imply 200 simultaneous model calls. Use distinct contexts where contamination matters, while remembering that identical models can make correlated errors. Commit compatible updates immediately; revalidate stale dependencies and arbitrate conflicting updates.

This is a recommended default, not a measured superiority claim. A controlled comparison should keep models, tools, retrieval permissions, total budget and scientific tasks fixed while comparing one tool-using agent with event-triggered role workers. Measure verified completion, false acceptance, repeated tokens, latency and coordination cost.

## Interpretation

A successful run establishes that this supplied classical construction passes the listed symbolic checks and that the small candidate loops reject specified wrong terms. It does not establish independent rediscovery, correctness of the whole historical paper, superiority of the proposed controller, or scalability. The chosen paper is likely present in model training and was consulted directly, so it cannot be a blind discovery benchmark.
