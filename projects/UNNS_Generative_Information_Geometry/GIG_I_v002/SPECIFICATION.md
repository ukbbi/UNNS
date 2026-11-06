# GIG-I v002 — Research Specification (as supplied, verbatim)

GIG-I v002 — Research Specification
UNNS Generative Information Geometry · Phase II · 5 November 2026

Research title: Arithmetic Realizability and Graph–Topology Separation in UNNS Generative Histories

Release: GIG_I_v002

Parent baseline: GIG_I_v001 — preserved unchanged.

Research character: Theorem-driven mathematical investigation, with exact computational searches and independently verifiable counterexample certificates.
1. Scientific objective
GIG-I v001 established that generative ambiguity and accessibility information through two legal swaps do not determine history topology. It produced six exact arithmetic witness pairs, including W5 and W6, where a single hexagonal 2-cell distinguishes the homology of structures with otherwise matching radius-2 information.

GIG-I v002 will address a stronger question:
To what extent does the arithmetic admissibility grammar determine the topology of a generative history complex from its swap graph, and can two arithmetically realizable complexes have isomorphic swap graphs but different homology?

The project has two complementary aims:
- Arithmetic realizability: derive mathematical constraints on the arrangement sets and higher-dimensional configurations that SELECT-II can generate.
- Graph–topology distinguishability: determine whether graph-based information observables can ever become fundamentally insufficient, even when every finite swap radius is known.
The priority is to obtain a general arithmetic theorem and either a sharp exact counterexample or a meaningful structural obstruction.
2. Mathematical framework to preserve
The established v001 constructions remain authoritative:
\[
T_N(m)=m\frac{(N+1)^2}{N},\qquad N\mid m.
\]

For a content \(C\) of \(k\) distinct labels and positive integer source \(m\), write
\[
\mathcal A_C(m)=\{w\in S_k:K(w)\mid m\}.
\]

Here \(K(w)\) is the frozen SELECT-II admissibility threshold.

Define:
- \(G_C(m)\): the induced adjacent-swap graph on \(\mathcal A_C(m)\).
- \(X_C(m)\): the full permutohedral subcomplex determined by the same vertex set.
- \(\beta(X_C(m))\): its Betti vector over \(\mathbb F_2\).
- \(\mathcal I_r(G_C(m))\): the exact v001 fine accessibility signature through radius \(r\).
The distinction between the graph and the full complex must be maintained throughout. Two graph-isomorphic pieces have identical graph-based accessibility information at every radius, but their higher-dimensional cell structures must be computed from the actual permutohedral embeddings.
3. First theorem target — Cubical admissibility factorization
This is the first mathematical task, before expanding the census.

Consider a combinatorial \(d\)-cube in the permutohedron corresponding to \(d\) disjoint adjacent pairs of labels whose orientations can be independently exchanged.

For a fixed source and fixed order of the blocks, let \(E_i\subseteq\{0,1\}\) be the locally admissible orientations of the \(i\)-th pair.

The target theorem is
\[
\boxed{
\mathcal A_C(m)\cap Q_d
=E_1\times E_2\times\cdots\times E_d.
}
\]

Its justification must establish rigorously that every admissible orientation of a two-label block leaves the same exit state:
\[
T_aT_b(x)=T_bT_a(x)=xR(a)R(b).
\]

Consequently, the entry state of a later disjoint block is independent of earlier orientation choices.

If correct under the stated hypotheses, the theorem yields a stronger corollary:

Every nonempty intersection of an admissible arrangement set with such a cube is a coordinate face of that cube.

For a 3-cube, its possible vertex counts are therefore
\[
\boxed{1,\;2,\;4,\;8}
\]

or zero for an empty intersection.

A Petrie six-cycle formed by retaining six vertices of a 3-cube and deleting two opposite vertices cannot be the exact admissible-vertex intersection with that cube.

This is a proposed arithmetic obstruction theorem, not a claim that every hexagonal graph configuration is forbidden.

In particular, v002 must distinguish the forbidden six-vertex cube slice from a braid hexagon, whose six vertices form a genuine permutohedral 2-face.
4. Second theorem target — Threshold-closure characterization
A further useful result follows directly from the frozen admissibility-threshold law. It should become part of v002 because it makes the k=6 search considerably more systematic.

For a fixed distinct-label content \(C\), let \(V=S_k\) be all possible arrangements. For a nonempty proposed arrangement set \(S\subseteq V\), define
\[
L(S)=\operatorname{lcm}\{K(w):w\in S\}
\]

and its arithmetic closure
\[
\boxed{
\operatorname{cl}_K(S)=
\{v\in V:K(v)\mid L(S)\}.
}
\]

Proposed theorem GIG-T12 — Exact realizability criterion
\[
\boxed{
S=\mathcal A_C(m)\text{ for some }m
\iff
\operatorname{cl}_K(S)=S.
}
\]

Furthermore, whenever the set is realizable, \(L(S)\) is its smallest positive realizing source under ordinary numerical order, and is the divisibility-minimal realizing source.

The proof is short:

If \(S=\mathcal A_C(m)\), then every threshold \(K(w)\) for \(w\in S\) divides \(m\). Hence \(L(S)\mid m\). Any arrangement whose threshold divides \(L(S)\) must therefore also be in \(S\).

Conversely, if \(S\) is closed, choosing \(m=L(S)\) realizes exactly \(S\).

An additional corollary is
\[
\boxed{
S\text{ is squarefree-source realizable}
\iff
L(S)\text{ is squarefree},
}
\]

provided \(S\) is a nonempty closed set.

This produces a direct arithmetic decision procedure for whether a proposed geometric arrangement set can occur.

The map \(\operatorname{cl}_K\) is also a closure operator: it is extensive, monotone and idempotent. Its fixed points form a finite closure system.

Research significance: rather than relying exclusively on brute-force searches over sources, we can construct a candidate combinatorial configuration and test exactly which additional permutations arithmetic admissibility forces into it.

This provides the basis for a new realizability-first search engine.
5. Third theorem target — Recoverability from generator-colored graphs
We must distinguish an abstract swap graph from a swap graph that retains the adjacent-transposition generators.

Write \(s_i\) for exchange of positions \(i\) and \(i+1\).

The edge-colored graph records which \(s_i\) generates each swap. The ordinary information profile \(I_r\) does not retain these colors.

Candidate GIG-T13:

If two distinct-label history graphs admit an isomorphism preserving their adjacent-transposition colors, up to an automorphism of the Coxeter diagram, investigate whether that isomorphism extends to an isomorphism of their full permutohedral history complexes.

The proof should use the fact that a permutohedral face is a coset of the subgroup generated by a specified subset of adjacent transpositions.

For each such subgroup, all vertices of its orbit must be present for the corresponding face to belong to the history complex.

This suggests a precise reconstruction hierarchy:
\[
\begin{aligned}
&\text{Uncolored swap graph}\\
&\quad\downarrow\ \text{add generator labels}\\
&\text{Generator-colored swap graph}\\
&\quad\downarrow\ \text{recover eligible faces}\\
&\text{Permutohedral history complex}.
\end{aligned}
\]

The target is to prove an exact reconstruction theorem with its full hypotheses.

If this succeeds, a graph-isomorphic but topologically inequivalent pair must fail to preserve the required generator-color structure. This would identify precisely what additional geometric information the ordinary swap graph has forgotten.
6. The k=6 investigation
The first new experimental chamber is the six-distinct-label arrangement space.
EXACT COMBINATORIAL SETTING
720
Possible permutations
5
Adjacent-swap generators
3
Disjoint simultaneous swaps possible


The full permutohedron \(P_6\) has dimension 5. Its higher-dimensional faces are defined by ordered partitions, exactly as in the inherited GEO-HD-1 construction.

Experiment E5 — Six-cycle classification
Enumerate and classify six-cycles in the unweighted, unlabeled 1-skeleton of \(P_6\).

For each cycle, record its actual adjacent-transposition word and embedding, distinguishing:
- Braid hexagons that bound genuine permutohedral 2-faces.
- Petrie-type hexagons contained in three-dimensional cubes.
- Any additional cycle types found by exact classification.
Do not assume every graph-theoretic six-cycle is the boundary of a permutohedral face.

For every candidate cycle, apply the threshold-closure procedure to determine whether a legal arithmetic source can realize its proposed vertex set exactly.

The cubical factorization theorem should independently exclude Petrie-type six-vertex cube slices.
Experiment E6 — Realizable arrangement-set search
Search arithmetically realizable sets with six distinct labels.

Use the existing threshold and lcm-closure machinery, enhanced by the proposed \(\operatorname{cl}_K\) operator.

Search priority:
1. Small connected components containing six-cycles.
2. Components containing both braid and non-braid six-cycles.
3. Pairs sharing graph order, edge count, degree multiset and component sizes.
4. Pairs with matching fine information signatures through radius 3.
5. Candidate pairs with isomorphic uncolored swap graphs.
A bounded census should be run in increasing label ranges, initially \(L\leq10\), then \(L\leq12\), with further extensions determined by the number of distinct realizable sets and computational cost.

Record all closure-cap exclusions, search bounds and incomplete branches. Only a search with fully enumerated source thresholds and no skipped cases qualifies as exhaustive for its stated domain.
Experiment E7 — Graph-isomorphism comparison
For each candidate pair \(A,B\), test
\[
G_A\cong G_B.
\]

The isomorphism test must ignore arithmetic label names and adjacent-swap generator colors.

Use cheap necessary filters first, followed by an exact graph-isomorphism algorithm. Do not treat matching degree sequences, Weisfeiler–Leman signatures or graph hashes as proof of isomorphism.

If a graph isomorphism exists, calculate independently
\[
\beta(X_A),\qquad \beta(X_B).
\]

The decisive target is
\[
\boxed{
G_A\cong G_B
\quad\text{but}\quad
\beta(X_A)\ne\beta(X_B).
}
\]

A verified pair of this kind would establish that graph-only information observables cannot determine history homology even when all finite swap radii are available.
Experiment E8 — Higher-dimensional information
Investigate which information must be added to the graph to recover the differing topology.

Begin with exact structural data:
\[
f_j(X)=\#\{\text{\(j\)-dimensional faces of }X\},
\]

the generator-colored adjacency, hexagonal face incidence and higher cellular boundary operators.

For example, over \(\mathbb F_2\),
\[
\boxed{
\beta_j=f_j-\operatorname{rank}\partial_j
-\operatorname{rank}\partial_{j+1}.
}
\]

This identity supplies an exact reconstruction benchmark.

The research task is to find smaller arithmetic or informational signatures that determine the required boundary ranks, rather than simply repackaging a full homology calculation as an entropy measure.
7. Theorem and problem register
v002 must append to the existing theorem registry without changing GIG-T1–T10.
ID	Statement or research target	Required disposition
GIG-T11	Cubical admissibility factorization and subcube-intersection law	Formal proof or precise counterexample
GIG-T12	Threshold-closure characterization of realizable arrangement sets	Formal proof and independent computational checks
GIG-T13	Reconstruction of permutohedral faces from generator-colored swap graphs	Prove under explicit hypotheses or delimit the obstruction
GIG-T14	Graph isomorphism implies equality of all graph-derived accessibility profiles	Prove
GIG-Q3	Existence of arithmetically realizable graph-isomorphic pieces with different homology	Open until settled
GIG-Q4	Minimal additional information required to distinguish their higher-dimensional cells	Open
GIG-C1/C2	Existing separating-radius conjectures	Preserve; report any new evidence or falsification

If E7 finds a valid graph-isomorphic, homologically inequivalent pair, register it under a new theorem ID with a complete finite-exact certificate.

If no such pair is found, record the precisely bounded negative result. Do not convert an unsuccessful finite search into a universal impossibility theorem.
8. Computational implementation
Build upon the verified v001 engine without altering its sources.
New module	Responsibility
cube_factor.py	Enumerate disjoint-swap cubes and verify product factorization
threshold_closure.py	Construct arithmetic closures and minimal realizing sources
cycle_types.py	Classify six-cycles and their generator sequences
realizability.py	Generate and classify k=6 realizable arrangement sets
graph_iso.py	Test uncolored and generator-colored graph isomorphism
cell_signature.py	Compute face incidence and cellular boundary ranks
certificates.py	Produce independently checkable witness records

All admissibility calculations must use exact integer arithmetic.

The k=6 arrangement space contains only 720 permutations, but the number of possible contents and arithmetic threshold closures grows rapidly. The engine should therefore cache permutation masks and thresholds, use closure-based pruning, compare graph invariants before isomorphism tests, and avoid repeated homology computations for identical arrangement masks.

Where possible, symmetry-reduced candidates should be used, while retaining original labels and sources in the evidence records.
Exact witness requirements
A successful graph–topology separation certificate must contain:
1. The two six-label contents and their positive integer sources.
2. The complete admissible arrangement masks, with independent threshold-based reconstruction.
3. An explicit vertex bijection establishing graph isomorphism.
4. The full permutohedral face counts and boundary ranks for both complexes.
5. Their Betti vectors, with an independent Euler-characteristic check.
6. A statement identifying exactly which higher-dimensional cells or incidence relations differ.
7. The source convention, squarefree-source status, software version and source hashes.
A certificate must be verifiable independently without rerunning the entire search.
9. Required regressions and independent verification
GIG-I v002 must preserve all earlier established results.
v001 regression: Reproduce all 28 existing tests, and preserve E1–E4, T1–T10, W1–W6 and the existing result files.


Independent admissibility: Compare threshold-derived arrangement sets with direct SELECT-II forward simulation.


Cubical theorem: Check all relevant three-swap cube slices in the targeted finite k=6 cases.


Topology: Independently verify face attachment, boundary-matrix consistency and Betti numbers. Do not substitute graph cycle rank for complex homology.


Source cross-check: Use frozen GEO-HD-1D v004 when accessible. Record explicitly if an optional external cross-check cannot run.



All random exploration must have deterministic seeds, while the principal mathematical certificates must rely on exact reconstruction rather than statistical significance.
10. Package structure
Create the next release alongside v001 in the existing UNNS_GInGe workspace.
UNNS_GInGe/
├── GIG_I_v001/                [FROZEN]
└── GIG_I_v002/
    ├── README.md
    ├── SPECIFICATION.md
    ├── MANIFEST.json
    ├── THEORY/
    │   ├── DEFINITIONS.md
    │   ├── THEOREMS.md
    │   ├── PROOFS.md
    │   └── OPEN_PROBLEMS.md
    ├── ENGINE/
    │   ├── cube_factor.py
    │   ├── threshold_closure.py
    │   ├── cycle_types.py
    │   ├── realizability.py
    │   ├── graph_iso.py
    │   ├── cell_signature.py
    │   └── certificates.py
    ├── EXPERIMENTS/
    │   ├── E5_cycles.py
    │   ├── E6_realizability.py
    │   ├── E7_graph_iso.py
    │   ├── E8_cell_info.py
    │   └── run_all.py
    ├── CERTIFICATES/
    ├── TESTS/
    │   └── test_gig_v002.py
    └── RESULTS/
        ├── results.json
        ├── search_coverage.json
        └── report.md


A Windows-compatible runner is desirable. Preserve short, Windows-safe names for generated files and do not modify the existing folder structure of any frozen release.
11. Required research report
RESULTS/report.md must be a substantive mathematical account, not merely a collection of test counters.

It should address these questions in order:
- What arithmetic arrangement configurations are rigorously forbidden, and why?
- Does threshold closure give a complete characterization of realizability?
- What six-cycle types occur in \(P_6\), and which are arithmetically realizable?
- Does generator-colored adjacency determine the inherited permutohedral complex?
- Are there graph-isomorphic realizable pieces with different topology?
- What does k=6 establish about GIG-C1 and GIG-C2?
- Which information remains recoverable from the graph, and which requires higher-dimensional cell data?
The report must separate general proofs, exact finite results, unsuccessful bounded searches, and open conjectures.
12. Completion and scientific outcomes
Three possible outcomes are scientifically meaningful.

Outcome A — Graph–topology separation

Find a valid arithmetic pair with isomorphic swap graphs but different Betti vectors.

This would prove that no invariant depending only on the abstract swap graph can recover history homology universally. It would be the strongest sought-after v002 discovery.



Outcome B — Arithmetic rigidity

Prove a nontrivial restriction demonstrating that particular graph–topology counterexamples cannot be realized by SELECT-II.

This would establish a positive structural property of the generative grammar, even without finding a separating pair.



Outcome C — Exact bounded classification

Determine the realizability and distinguishability landscape within a fully stated k=6 search domain, identifying the first unresolved configurations and their obstructions.

This would constrain future conjectures without claiming a general theorem beyond the searched domain.



The release reaches its minimum completion standard when GIG-T11 and T12 are rigorously settled, the k=6 experiments produce reproducible records, and the graph-isomorphism investigation has either exact witnesses or a precisely documented bounded result.

The more ambitious reconstruction theorem GIG-T13 and the general existence problem GIG-Q3 may remain open if the mathematical investigation does not resolve them.
13. Execution directive
GIG-I v002 — Implementation brief
Develop an independent, versioned GIG-I v002 research package in the existing UNNS_GInGe workspace.

Begin by proving or falsifying the cubical admissibility factorization and exact threshold-closure characterization. Use these results to construct an arithmetic realizability engine for six-label history arrangements.

Classify the relevant six-cycle geometries, distinguish graph isomorphism from generator-colored and permutohedral equivalence, and search for exact pairs of arithmetically realizable history complexes whose swap graphs are isomorphic but whose homology differs.

Preserve the inherited distinct-label full-permutohedral cell definition, compute homology over \(\mathbb F_2\), and produce complete certificates for every claimed new result.

Continue the existing GIG-C1/C2 investigations without assuming a universal separating radius.

Treat GIG-I v001, SELECT-II and GEO-HD-1 as frozen, read-only references. No remote GitHub modifications.

Report mathematical discoveries, their proofs and their significance before procedural validation details.