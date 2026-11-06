GIG-I v003 — Research Specification
UNNS Generative Information Geometry · Phase III · 5 November 2026

Research title: Higher-Dimensional Information and Arithmetic Boundary Rigidity in UNNS Generative Histories

Release: GIG_I_v003

Research workspace: UNNS_GInGe\GIG_I_v003\

Frozen baselines: GIG-I v001, GIG-I v002, SELECT-II and GEO-HD-1D v004.

Research character: Rigorous mathematical development supported by exact arithmetic experiments, cellular homology calculations and independently verifiable certificates.
1. Governing scientific question
GIG-I v001 established that generative entropy and radius-2 accessibility statistics can fail to determine history topology.

GIG-I v002 established something more surprising: arithmetic admissibility imposes sufficient rigidity that the uncolored swap graph determines low-dimensional topology in the proved range \(k\leq8\).

Its exhaustive finite censuses found no graph-isomorphic arithmetic complexes with different Betti vectors.

This changes the direction of our investigation.

The next question is:
Does the arithmetic structure of admissible generation determine higher-dimensional topological information from lower-dimensional history geometry, and, if not, precisely which additional arithmetic information is required?

The immediate mathematical target is the third cellular boundary operator,
\[
\partial_3:C_3(X;\mathbb F_2)\longrightarrow C_2(X;\mathbb F_2).
\]

Its image determines which two-dimensional cycles become boundaries of three-dimensional cells.

For any finite complex,
\[
\boxed{
\beta_2(X)=
f_2(X)-\operatorname{rank}\partial_2
-\operatorname{rank}\partial_3.
}
\]

Under GIG-T15, for realizable distinct-label complexes with \(k\leq8\), the uncolored swap graph determines the 2-skeleton and therefore the first two terms.

Consequently, a pair of graph-isomorphic admissible complexes with different \(\beta_2\) must have different ranks of \(\partial_3\).

GIG-I v003 will investigate whether that remaining boundary information is also arithmetically rigid.
2. Research objectives
Objective A — Generalize arithmetic factorization

Extend the commuting-cube theorem GIG-T11 to ordered blocks of arbitrary size. Determine which higher-dimensional arrangements source admissibility forces or excludes.


Objective B — Establish exact 3-cell arithmetic

Classify the three-dimensional permutohedral faces, derive their realizability thresholds, and compute their cellular boundary operators.


Objective C — Investigate boundary recoverability

Determine whether the uncolored swap graph constrains or determines \(\operatorname{rank}\partial_3\), and characterize possible ambiguities.


Objective D — Discover arithmetic topological transitions

Study how two-dimensional cycles appear or become boundaries when source divisibility permits additional histories and higher-dimensional cells.



The priority order is A → B → C → D. The programme should lead with mathematics, not a large exploratory census.
3. The foundational example: two nontrivial 2-cycles
The principal experimental anchors are the two GIG-I v002 examples with nonzero second homology.
EXAMPLE A
288
Source

Content: (2,3,4,5,8,9)

372 admissible arrangements
\(\beta_2=1\)
EXAMPLE B
432
Source

Content: (2,3,6,7,8,9)

276 admissible arrangements
\(\beta_2=1\)


These examples have genuine nontrivial second homology under the inherited distinct-label permutohedral cell construction. They are starting points for understanding arithmetic control of 3-dimensional boundaries, not yet graph-isomorphic counterexamples.

The first experimental task is to reconstruct exactly which 2-cycles survive, which 3-cell boundaries are available, and which changes in source divisibility alter those relationships.
4. Theorem programme
Preserve GIG-T1–T15 and the existing conjecture identifiers. Begin new results at GIG-T16.
ID	Proposed mathematical result	Required status
GIG-T16	General ordered-block admissibility factorization	Prove or exhibit a precise counterexample
GIG-T17	Exact arithmetic face thresholds	Prove
GIG-T18	Divisibility-indexed complex filtration and face activation	Prove
GIG-T19	Third-boundary-rank obstruction to graph–topology separation	Prove as a corollary of T15
GIG-T20	Reconstruction or obstruction theorem for 3-dimensional faces from uncolored graphs	Open theorem target
GIG-T21	Arithmetic conditions governing changes in second homology	Open theorem target
GIG-Q3	Graph-isomorphic realizable complexes with different homology	Remains open
GIG-Q5	Whether the uncolored graph determines third-boundary rank	New open problem
GIG-Q6	Minimal additional data needed to reconstruct higher cellular boundaries	New open problem

T20 and T21 must not be labeled proved until complete arguments are available. Their failure in a proposed general form should lead to sharp counterexamples and corrected statements rather than weaker numerical evidence being presented as theorems.
5. GIG-T16 — General block-admissibility factorization
The commuting-cube theorem GIG-T11 concerns independent adjacent swaps. The next natural generalization concerns independent permutations within disjoint ordered blocks.

Let a generating word be divided into consecutive blocks
\[
w=B_1B_2\cdots B_s,
\]

where each block has a fixed multiset of labels, but its internal order may vary.

The cumulative multiplier of a completed block is independent of its ordering:
\[
R(B_i)=\prod_{N\in B_i}\frac{(N+1)^2}{N}.
\]

Therefore the state entering block \(B_{i+1}\) is independent of the chosen admissible ordering inside \(B_i\).

Let \(E_i\) be the set of internally admissible permutations of block \(B_i\), evaluated at its fixed entry state.

Target theorem:
\[
\boxed{
\operatorname{Adm}(B_1,\ldots,B_s)
=E_1\times\cdots\times E_s.
}
\]

The proof must account for the intermediate legality of every operation, not merely equality of the final multipliers.

This result would extend the cubical factorization law to products of permutohedra. Its consequences for which 3-cell patterns can be partially realized should be derived explicitly.
6. GIG-T17 — Arithmetic thresholds of higher-dimensional cells
For fixed distinct-label content \(C\), let \(F\) be a face of the associated permutohedron and let \(V(F)\) denote its vertex set.

Define its arithmetic activation threshold:
\[
\boxed{
K_F=\operatorname{lcm}_{w\in V(F)}K(w).
}
\]

Because the inherited history complex is the full permutohedral subcomplex on the admissible vertices, the target theorem is
\[
\boxed{
F\subseteq X_C(m)
\iff K_F\mid m.
}
\]

This makes every face's realization an exact arithmetic divisibility decision.
Required classification for \(k=6\)
The six-label permutohedron \(P_6\) has 540 three-dimensional faces, belonging to three combinatorial types.
Cubes
90
\(P_2\times P_2\times P_2\)

Hexagonal prisms
360
\(P_3\times P_2\)

Truncated octahedra
90
\(P_4\)



Exact combinatorial face counts in the complete \(P_6\). Arithmetic admissibility determines which of these faces are actually present for a chosen content and source.
The engine must construct all three types from ordered partitions, obtain their vertex sets, compute \(K_F\), and build their cellular boundaries.

The classification should become a reusable exact reference for subsequent research.
7. GIG-T18 — Arithmetic filtration and topological events
The source variable provides a natural divisibility ordering.

For fixed content \(C\),
\[
m\mid m'
\quad\Longrightarrow\quad
X_C(m)\subseteq X_C(m').
\]

This follows because any threshold dividing \(m\) also divides \(m'\).

Therefore, the history complexes form a monotone family over the divisibility poset of source integers.

This is a mathematical opportunity.

It gives us an arithmetic filtration in which vertex, edge and higher-cell appearances are governed by threshold divisibility.

The research must establish:
- Exact birth conditions for individual faces.
- The changes to cellular boundary ranks when new faces appear.
- Conditions under which a nontrivial 2-cycle first appears.
- Conditions under which a previously nonbounding 2-cycle becomes a boundary.
- Which changes can be predicted solely from arithmetic threshold data.
For a comparable pair \(m\mid m'\),
\[
\Delta\beta_2
=
\Delta f_2
-\Delta\operatorname{rank}\partial_2
-\Delta\operatorname{rank}\partial_3.
\]

This identity should be used as the exact accounting law.

A crucial distinction: the source-divisibility filtration concerns changing the initial source for the same fixed content. It must not be confused with the actual evolution of a state under SELECT-II or FIELD-I operators.
A possible further achievement
If the arithmetic activation thresholds determine when specific nonbounding cycles become boundaries, we gain a rigorous notion of an arithmetic topological event.

That could eventually connect GIG research to persistence theory and information dynamics through source-defined mathematical constructions.
8. GIG-T19/T20 — Can the swap graph reconstruct 3-cells?
This is the central investigation of v003.

For two realizable complexes \(X\) and \(Y\) satisfying \(k\leq8\), suppose
\[
G_X\cong G_Y.
\]

GIG-T15 implies that their recognized 2-skeleta have the same cellular structure.

Accordingly,
\[
\boxed{
\beta_2(X)-\beta_2(Y)
=
\operatorname{rank}\partial_3(Y)
-\operatorname{rank}\partial_3(X).
}
\]

This is the proposed GIG-T19 consequence.
New problem: uncolored 3-cell recognition
Determine whether each of the three cell types can be recognized intrinsically from the uncolored graph:
Cell type	Reconstruction question
Cube	Does the relevant embedded cube graph uniquely determine an actual 3-cell?
Hexagonal prism	Are its six square and two hexagonal boundary faces sufficient to identify its attachment?
Truncated octahedron	Can the arrangement of its square and hexagonal faces be recovered without knowing generator colors?

Care is required: finding an abstract subgraph shaped like a cell's 1-skeleton does not automatically establish that the corresponding permutohedral cell exists.

For each proposed criterion, compare the graph-derived structure with the genuine face list obtained from the inherited ordered-partition construction.

The desired outcomes are either a reconstruction theorem or an explicit arithmetic obstruction explaining why an apparent cell cannot be realized.

No assumption that the graph ultimately fails—or succeeds—to determine higher topology should be built into the search.
9. A new information invariant: third-boundary information
Introduce
\[
\boxed{
J_3(X)=\operatorname{rank}_{\mathbb F_2}\partial_3.
}
\]

This is not Shannon entropy. It is a structural invariant measuring the number of independent cellular boundary relations contributed by 3-cells.

Also record
\[
D_3(X)=f_3(X)-J_3(X),
\]

the number of independent linear dependencies among the 3-cell boundary columns.

The research should determine whether \(J_3\) and \(D_3\) contain information absent from the uncolored swap graph.

To quantify possible graph-level ambiguity in a specified finite comparison domain \(\mathcal D\), define
\[
\mathcal R_3([G];\mathcal D)
=
\{J_3(X):X\in\mathcal D,\ [G_X]=[G]\}.
\]

Then
\[
\boxed{
A_3([G];\mathcal D)
=
\log_2|\mathcal R_3([G];\mathcal D)|.
}
\]

If \(A_3=0\), the graph-isomorphism class has one observed third-boundary rank within that domain. If it is positive, a genuine ambiguity has been demonstrated.

The v002 census implies zero such rank ambiguity over its covered \(k\leq6\) domain. This does not establish that \(A_3\) must vanish in larger domains.

Unlike \(J_3\), \(A_3\) is explicitly domain-relative. It is a combinatorial ambiguity measure; an associated Shannon entropy would require an additional probability ensemble.
10. Exact experimental programme
ID	Experiment	Principal deliverable
E9	Three-dimensional face grammar	Complete \(P_6\) 3-face classification and exact threshold tables
E10	Two \(\beta_2=1\) anchor complexes	Exact boundary matrices, ranks and nonbounding cycle certificates
E11	Arithmetic source transitions	Divisibility-indexed face events and changes in \(H_2\)
E12	Graph-to-3-cell reconstruction	Structural criteria, exact examples and counterexamples
E13	Boundary-information comparison	\(f_3\), \(J_3\), \(D_3\), graph classes and topological ambiguity
E14	Targeted larger-content search	Conditional \(k=7\) exploration, informed by the preceding results

E10 — Required topology certificates
For each anchor complex, calculate
\[
f_0,f_1,f_2,f_3,\quad
\operatorname{rank}\partial_1,\quad
\operatorname{rank}\partial_2,\quad
\operatorname{rank}\partial_3.
\]

Find an explicit nonzero 2-cycle \(z\) satisfying
\[
\partial_2z=0,\qquad
[z]\ne0\in H_2(X;\mathbb F_2).
\]

For independent verification, produce a 2-cochain \(\varphi\) satisfying
\[
\varphi(\partial_3c)=0
\quad\text{for every }c\in C_3,
\qquad
\varphi(z)=1.
\]

This certifies that \(z\) is not a boundary.

The report must identify the actual 3-cells and incidence relations relevant to this nontrivial class.
E11 — Source-transition experiment
For each anchor content, construct the neighboring source regimes in the divisibility order, including relevant divisors and source enlargements whose face thresholds create new events.

For every distinct regime, record the number and types of newly activated faces, boundary-rank changes and Betti-vector changes.

Distinguish genuine homology transitions from events that change the cell structure without changing Betti numbers.
E12 — Reconstruction experiment
Test proposed recognition criteria first on the full \(P_6\) face grammar and then on arithmetically realizable subcomplexes.

Retain v002's abstract nonrealizable Z1 certificate as a negative control. It demonstrates why abstract graph configurations must not be treated as automatically arithmetically realizable.
E14 — Larger-content exploration
Do not immediately launch an exhaustive \(k=7\) census.

Begin with structures suggested by the two \(H_2\) examples, particularly controlled content extensions and threshold-closure constructions.

Any finite search must report its exact content bounds, source-regime coverage, symmetry reductions and unresolved branches.

If no new structural distinction is found, report that result without promoting it into a universal recoverability theorem.
11. Computational requirements
Use the v002 threshold-closure and graph engines as read-only dependencies or reproduce the necessary algorithms within v003.

New computational capabilities should include:
- Exact enumeration of 3-dimensional permutohedral faces.
- Arithmetic face-threshold construction using integer lcm.
- Sparse cellular boundary matrices over \(\mathbb F_2\).
- Exact rank calculations and explicit kernel representatives.
- Cohomological certificates for nonbounding 2-cycles.
- Source-regime construction from threshold divisibility.
- Graph-based cell-recognition tests and independent full-face comparisons.
- Exact graph-isomorphism classification for targeted candidate pairs.
For v003, computing \(H_2\) requires only the 3-skeleton. However, claims about the full Betti vector, especially \(\beta_3\) and higher, must include the appropriate higher cellular boundary operators.

Use exact rational and integer arithmetic. Floating-point computations may be used for presentation, never as the basis of a divisibility, rank or homology certificate.
12. Package structure
Create the release beside the preserved v001 and v002 folders.
UNNS_GInGe/
├── GIG_I_v001/             [FROZEN]
├── GIG_I_v002/             [FROZEN]
└── GIG_I_v003/
    ├── README.md
    ├── SPECIFICATION.md
    ├── MANIFEST.json
    ├── THEORY/
    │   ├── DEFINITIONS.md
    │   ├── THEOREMS.md
    │   ├── PROOFS.md
    │   └── OPEN_PROBLEMS.md
    ├── ENGINE/
    │   ├── block_factor.py
    │   ├── face_threshold.py
    │   ├── cell_boundary.py
    │   ├── source_filtration.py
    │   ├── cell_recognition.py
    │   └── boundary_info.py
    ├── EXPERIMENTS/
    │   ├── E9_faces.py
    │   ├── E10_h2.py
    │   ├── E11_events.py
    │   ├── E12_recovery.py
    │   ├── E13_info.py
    │   └── E14_k7.py
    ├── CERTIFICATES/
    ├── TESTS/
    │   └── test_v003.py
    ├── RESULTS/
    │   ├── results.json
    │   ├── search_coverage.json
    │   └── report.md
    ├── CORRECTIONS/
    │   └── V002_T12_SCOPE.md
    └── RUN_V003.bat



CORRECTIONS/V002_T12_SCOPE.md should document the minor empty-set convention issue identified in v002's T12. The earlier release must remain untouched.

The runner should support test, quick and full modes so mathematical development can proceed without repeatedly executing every expensive search.
13. Verification and completion requirements
The release must meet the following criteria:
Requirement	Acceptance condition
Mathematical foundations	T16–T19 have complete, explicitly scoped proofs or recorded corrections where necessary
3-cell classification	All 540 faces of \(P_6\) are reproduced with correct types, vertices and incidence
Arithmetic thresholds	Face activation agrees with direct vertex admissibility
Anchor examples	Both nontrivial \(H_2\) examples are reproduced with exact cycle and boundary certificates
Chain-complex consistency	\(\partial_2\partial_3=0\), with corresponding consistency checks in other computed dimensions
Source filtration	Inclusion and face-event laws are verified on every reported transition
Graph reconstruction	T20 is proved under precise hypotheses, falsified by an exact counterexample, or retained as an open problem
Information results	Domain-dependent conclusions are distinguished from universal mathematical results
Regression	Existing v001/v002 tests and frozen-source cross-checks remain valid
Provenance	Manifest hashes, exact sources, software requirements and certificates are recorded

The release must not be delayed solely because T20 or T21 remains open. A proved obstruction or a carefully delimited negative result may be a substantive scientific outcome.
14. What will count as a discovery?
There are three primary possibilities.

Discovery A — Higher-dimensional arithmetic rigidity. A theorem proves that, for a specified class of realizable complexes, the graph and arithmetic admissibility jointly force the 3-cell boundary structure. This would extend the structural recoverability established in v002.

Discovery B — Genuine higher-dimensional information loss. Two realizable complexes have isomorphic uncolored swap graphs but different third-boundary ranks or second homology. This would establish the first all-radius graph-information obstruction within the UNNS arithmetic grammar.

Discovery C — Arithmetic topology-transition law. A theorem predicts the birth or elimination of particular second-homology classes from exact face thresholds and incidence data, without repeatedly recomputing complete homology.

Any one of these would be a valuable advance. They are alternative possible outcomes, not assumptions to be built into the code.
15. Required mathematical report
RESULTS/report.md should answer:
1. How does admissibility factor across arbitrary ordered blocks?
2. Which three-dimensional cells can the arithmetic grammar realize?
3. What determines each cell's arithmetic activation threshold?
4. Which 3-dimensional boundaries are present in the two \(\beta_2=1\) anchor complexes?
5. Can new source-admissible cells eliminate nontrivial 2-cycles, and under what exact conditions?
6. Does the uncolored swap graph determine third-boundary rank in any proved class?
7. What information must be retained beyond graph connectivity and accessibility to reconstruct higher-dimensional topology?
8. What do the results imply for GIG-Q3 and the existing separating-radius conjectures?
The report should lead with mathematical results, exact examples, and implications. Verification counts, implementation details and bounded-search limitations belong in their appropriate supporting sections.

16. Execution directive for the research environment
GIG-I v003 — Implementation brief
Develop GIG_I_v003 as an independent mathematical research release inside UNNS_GInGe.

Preserve v001, v002, SELECT-II and GEO-HD-1D v004 as frozen references.

First establish ordered-block admissibility factorization, arithmetic face-threshold laws, and the source-divisibility filtration.

Then reconstruct the complete 3-dimensional permutohedral face grammar and investigate the two inherited \(H_2\ne0\) examples using exact cellular boundary matrices, independent rank calculations and explicit nonbounding-cycle certificates.

Determine whether uncolored swap graphs recover the third-boundary structure of realizable history complexes. Seek a general theorem, a precisely scoped reconstruction result, or a certified arithmetic counterexample.

Investigate arithmetic changes in second homology and develop structural information invariants sensitive to cellular boundary relations.

Use targeted larger-content experiments only where the preceding mathematics identifies useful candidate configurations.

Produce complete theory records, proofs, executable experiments, test results, search coverage, source hashes and a substantive mathematical report.

Do not alter frozen releases or GitHub remotely.

17. Scientific direction
The research progression is now especially compelling:
GIG-I v001

Information ambiguity

Different generative structures can share information statistics


GIG-I v002

Arithmetic rigidity

Admissibility excludes configurations and forces low-dimensional recoverability


GIG-I v003

Higher-dimensional information

Determine how arithmetic controls cellular boundaries and surviving homology


The greatest opportunity is to derive a law connecting arithmetic divisibility, geometric cell realization and topological information.