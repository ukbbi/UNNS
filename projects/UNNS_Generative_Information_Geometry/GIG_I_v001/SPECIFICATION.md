GIG-I v001 — Research Specification
UNNS Generative Information Geometry · Phase I · 5 November 2026

Project: Generative Information Geometry in the UNNS Substrate: Arithmetic Ancestry, Information Loss, and History Topology

Release: GIG_I_v001

Scientific status: New mathematical research programme built upon frozen SELECT-II and GEO-HD-1 results.

Your screenshot shows an empty UNNS_GInGe folder. We can use that as the active local workspace, with GIG_I_v001 as its first versioned research package.
1. Governing research question
Can the information retained and lost under UNNS generative projections be characterized exactly, and can arithmetic admissibility and the topology of history spaces impose nontrivial constraints on that information?

GIG-I v001 must establish the mathematical definitions, first exact results, reproducible examples and falsifiable conjectures needed to answer this question.

Its objective is not to replace Shannon entropy, but to develop an intrinsic theory of generative information that can be related rigorously to established information theory.
2. Required mathematical framework
A. Generative arithmetic

Use the frozen SELECT-II operator
\[
T_N(m)=m\frac{(N+1)^2}{N},\qquad N\mid m.
\]

Preserve the established definitions of admissible ordered histories, complete histories, source thresholds, generating contents and legal adjacent swaps.

B. History fibres

For a specified finite admissible history space \(\mathcal H\), define
\[
\pi:\mathcal H\to S,\qquad \pi(w)=\operatorname{end}(w),
\]

\[
\mathcal F_t=\pi^{-1}(t).
\]

Distinguish complete-history fibres from fixed-source fibres \(\mathcal F_t(m_0)\). All calculations must state the source convention.

C. Generative ambiguity

For nonempty finite fibres,
\[
\boxed{A(t)=\log_2|\mathcal F_t|.}
\]

This is the first intrinsic information observable, expressed in bits. Define the empty-fibre convention separately rather than applying the logarithm to zero.

D. Probabilistic information

For an explicitly specified history ensemble \(W\), use
\[
H(W\mid T=t)
\]

to measure uncertainty about the generating history conditioned on the endpoint.

Under uniform sampling of \(\mathcal F_t\),
\[
H(W\mid T=t)=A(t).
\]

For nonuniform sampling,
\[
H(W\mid T=t)\leq A(t).
\]

E. Recombination and topology

Construct the legal-swap graph \(G_t\) with histories as vertices. Its connected components define recombination classes \(C\).

Preserve the distinction between this graph and the higher-dimensional history complex already defined in GEO-HD-1.

3. Theorem programme
The release should contain formal statements, complete proofs where possible, and explicit statuses. The first results should be organized as follows.
ID	Mathematical target	Expected disposition
GIG-T1	Finiteness of complete-history fibres and exact reverse-edge characterization	Prove
GIG-T2	Information projection and conditional-entropy decomposition	Prove
GIG-T3	Generative ambiguity bounds and uniform-ensemble equality	Prove
GIG-T4	Exact information decomposition for the four histories of 72	Compute and prove
GIG-T5	Infinite-family ambiguity lower bound for \(72^r\)	Corollary of GEO-HD-1
GIG-T6	Recombination-class entropy versus connected-component count	Prove
GIG-T7	Recombination information profile: monotonicity and stabilization	Prove
GIG-Q1	Whether refined information profiles detect nontrivial history homology	Open investigation
GIG-Q2	Whether distinct arithmetic history structures can be information-equivalent but topologically inequivalent	Construct witnesses or establish restrictions

These IDs belong exclusively to the new GIG-I programme. They must not replace or renumber inherited results.
A particularly useful exact arithmetic lemma
A reverse SELECT-II edge into \(t\) exists with label \(N\) precisely when
\[
(N+1)^2\mid t.
\]

Its predecessor is then
\[
\boxed{m=\frac{Nt}{(N+1)^2}.}
\]

The result follows directly by writing \(m=kN\) in the forward operator.

Moreover,
\[
\frac{T_N(m)}{m}=N+2+\frac1N\geq4.
\]

Thus reverse paths decrease strictly and terminate. These facts provide a simple, exact foundation for complete-history enumeration without using floating-point arithmetic.
4. Core new observable: recombination information profile
For the finite swap graph \(G_t\), let \(B_r(w)\) denote the histories at legal-swap distance at most \(r\) from \(w\).

Define, for a uniform finite fibre of size \(M\),
\[
\boxed{
I_r(t)=\frac1M\sum_{w\in\mathcal F_t}
\log_2|B_r(w)|.
}
\]

The following must be established:
\[
I_0(t)=0,
\]

\[
I_r(t)\leq I_{r+1}(t),
\]

and, once \(r\) reaches the maximum finite component diameter,
\[
\boxed{I_r(t)=H(W\mid C,T=t).}
\]

This last equality is under uniform sampling of the fibre. It is an exact connection between legal-swap accessibility and conditional information.

The research challenge is to determine what the intermediate values of \(I_r\) reveal that ordinary entropy and component counts do not.

Important distinction: \(I_r\) depends on the swap graph's metric structure. Its relationship with higher-dimensional homology must be investigated rather than assumed.
5. Required exact experiments

Experiment E1 — Complete histories of 72

Enumerate all four complete histories, classify them by source, content and legal-swap equivalence, and calculate the complete information decomposition.

Under uniform sampling:
\[
A(72)=2,\quad H(C\mid T=72)=1.5,
\]

\[
H(W\mid C,T=72)=0.5
\]

in bits. The class sizes must be \(2,1,1\).




Experiment E2 — Infinite history-growth family

Compute complete-history counts for \(72^r\), \(r=1,\ldots,6\), using exact dynamic programming.

Required reference sequence:

4, 100, 3,601, 194,864, 14,177,856, 1,258,011,667

Establish from the inherited theorem:
\[
A(72^r)\geq\log_2\binom{2r}{r}.
\]

Do not explicitly materialize over a billion histories.




Experiment E3 — Different generating contents

Reproduce the source-4, endpoint-65536 example with distinct admissible contents satisfying
\[
R(1)^7=R(2)^2R(3)^4.
\]

Calculate the information contributed by content ambiguity separately from ordering ambiguity. Enforce source admissibility for every generated history.




Experiment E4 — Information versus history topology

Use the established GEO-HD-1 examples with \(\beta_1=1\) and \(\beta_2=1\), preserving their source, content, admissibility rules and higher-dimensional cell definitions.

Compute accessible information profiles where the exact graph data is available. Investigate whether histories or complexes with matching scalar information measures can possess different topology.



6. Computational design
The package should contain a small, deterministic, independently runnable Python implementation. It must not require editing an older SELECT-II, FIELD-I or GEO-HD-1 engine.

Required capabilities:
- Exact integer arithmetic and reverse-edge generation.
- Complete-history enumeration for small targets.
- Memoized history counting for large targets.
- Source-conditioned and content-conditioned fibre classification.
- Legal-swap graph construction using actual intermediate-state admissibility.
- Connected-component detection, graph distances, \(I_r\), and exact class-size computation.
- Entropy calculation, with exact rational probability weights where applicable and controlled numerical evaluation of logarithms.
Entropy values should report the probability model and precision. Inherited higher-dimensional complexes must be sourced from their actual cell rules, not approximated automatically by filling every graph clique.
7. Local deliverable structure
Create the following directly inside the currently empty UNNS_GInGe folder:
GIG_I_v001/
├── README.md
├── SPECIFICATION.md
├── MANIFEST.json
├── THEORY/
│   ├── DEFINITIONS.md
│   ├── THEOREMS.md
│   ├── PROOFS.md
│   └── OPEN_PROBLEMS.md
├── ENGINE/
│   ├── history_fibres.py
│   ├── information.py
│   └── swap_graph.py
├── EXPERIMENTS/
│   ├── E1_72.py
│   ├── E2_growth.py
│   ├── E3_content.py
│   └── E4_topology.py
├── TESTS/
│   └── test_gig.py
└── RESULTS/
    ├── results.json
    └── report.md



The source manifest should identify the frozen mathematical references and the exact definitions reused. The package must be self-contained for its elementary arithmetic computations.
8. Completion criteria
Mathematical definitions are unambiguous


GIG-T1–T7 have complete, qualified statements and proofs


E1–E3 reproduce the required exact arithmetic results


E4 includes an exact sourced topology comparison or records a precise unresolved obstruction


All automated tests pass, with no unexplained failures


These are acceptance requirements, not claims that the release has already passed.

Every proposition must distinguish established information-theoretic identities, inherited GEO-HD-1 results, new elementary deductions, and genuinely new theorem candidates.
9. Explicit scope boundary
GIG-I v001 concerns finite arithmetic history information and recombination topology.

The following remain outside this initial release: FIELD-I dynamical information transitions, thermodynamic entropy, quantum entanglement entropy, continuous curvature functionals, non-orientable temporal manifolds, and physical information-loss mechanisms.

Those are potential subsequent research directions. They should not be imported into v001 without a defined mathematical connection.
10. Execution instruction
The task for the local research environment is:
Implement GIG-I v001 as an independent, versioned mathematical research package. Establish the definitions and propositions above, prove the elementary information laws, reproduce the exact SELECT-II history examples, and investigate the first information–topology comparisons. Preserve all existing UNNS mathematical sources and GitHub references. Produce the source code, mathematical records, exact results, tests and a substantive report. Do not claim new theorems merely from successful computations, and do not modify GitHub remotely.
---
Scientific target (added by the project owner with the specification)
The minimum successful outcome is an exact theory of finite generative ambiguity and its decomposition by source, content and recombination class.
The strongest possible v001 outcome would additionally establish a new theorem or sharp counterexample showing how arithmetic history geometry constrains information accessibility beyond ordinary endpoint entropy.
That is where I would concentrate our first genuine discovery effort.
