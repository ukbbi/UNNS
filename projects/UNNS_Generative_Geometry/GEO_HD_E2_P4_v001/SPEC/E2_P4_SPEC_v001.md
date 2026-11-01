GEO-HD-1B / E2-P4 — Research direction
E2-P4 will investigate realized geometric transport into genuinely coupled, nonrectangular relation lattices. Its central problem is to determine whether arithmetic relations can predict which regions of an occurrence geometry survive FIELD-I evolution, without reconstructing the entire target geometric union.

The distinction is important: a nontrivial lattice need not be nonrectangular. E2-P3's new three-dimensional failure ended at a rectangular target lattice, so it does not resolve this next problem.

I have identified an exact FIELD-I family that gives E2-P4 a concrete starting point:
\[
\boxed{
\frac{2\cdot110^{4m}}9
\xrightarrow{C}
\frac{110^{4m}}3,\qquad m\ge1.
}
\]

Both relation lattices are nonrectangular in the original prime coordinates \(2,5,11\). For \(m=1\), the transition has 5 source occurrences and 13 target occurrences, with the common exponent box \([0,2]^3\). This is an appropriate primary specimen for the new investigation; geometric containment for the family remains to be established.

The specification below also retains the outstanding planar CP3-A problem, but excludes all cases already settled by GEO-I v012.
GEO-HD-1B / E2-P4
Arithmetic Obstruction Theory for Nonrectangular Target Geometry
Research specification: E2-P4 v001
Parent programme: GEO-HD-1 — Higher-Dimensional Generative Geometry of the UNNS Substrate
Predecessor: E2-P3 — Realized Geometric Transport: Coverage, Obstruction, and Higher-Dimensional Persistence
Status: READY FOR EXECUTION
Research directory: GEO_HD_NEXT_MILESTONE/GEO_HD_1_PROJECT/
Repository policy: GitHub read-only; frozen releases preserved
Scientific priority: General obstruction theorems and arithmetic prediction of realized geometric transport.

1. Research objective
E2-P1 through E2-P3 established that FIELD-I occurrence-index inclusion does not generally imply preservation of abstract Graver cells or containment of their realized geometric unions.

E2-P3 also established exact containment criteria for rectangular target lattices and found a three-dimensional containment failure between two nontrivial relation lattices.

Its new counterexample, however, has a rectangular target. The corresponding result does not characterize transport into a target whose prime coordinates remain coupled by nontrivial modular relations.

E2-P4 investigates the arithmetic conditions governing realized geometric persistence when the target relation lattice itself remains nonrectangular.

The principal problem is:

[
\boxed{
\text{Given }x\xrightarrow{C}x',
\quad\text{can arithmetic data decide }U(x)\subseteq U(x')?
}
]

The desired result is an explicit theorem, criterion or obstruction classification that avoids exhaustive reconstruction of the entire target geometric union.
1.1 Central research hypothesis
The working hypothesis is that the modular relation structure of the target constrains its uncovered geometric regions and therefore determines which source Graver cells can survive geometrically.

E2-P4 must establish whether that relationship admits:
1. Exact necessary or sufficient arithmetic conditions.
2. A finite or parametrically bounded obstruction description.
3. A general preservation theorem for a nontrivial family.
4. An effective predictor for geometric containment.
5. An essentially higher-dimensional obstruction beyond planar behavior.
These possibilities are to be investigated, not assumed.
1.2 Scientific success condition
The objective is to progress toward GEO-HD-1 criterion C3:
Establish a general, nontrivial mathematical result about the geometric organization of UNNS generation that is not merely an inherited GEO-I theorem or a routine consequence of standard lattice/polyhedral theory.

An exact numerical experiment, however extensive, does not by itself satisfy C3.

2. Source baseline and prior results
2.1 Frozen research sources
Source	Established contribution	E2-P4 use
GEO-I v002	Occurrence fibres, Graver moves, abstract cell construction	Reuse
GEO-I v003	Exact realizations, polyhedral intersections and geometric topology	Reuse
GEO-I v004	Embedding obstructions and finite templates	Comparison and methodological baseline
GEO-I v005–v012	Planar hollow-box classification and stabilization	Exclude inherited coverage cases
FIELD-I v012	Collective dynamics, arithmetic persistence and scaling	Transition grammar
E2-P1	Parity-to-integer transport and geometric noncontainment	Negative control
E2-P2	Abstract-cell survival criterion and P2-F21 family	Algebraic control
E2-P3	Rectangular-target containment, planar audit and essential 3D witness	Geometric controlThe GEO-I source reference remains pinned to:

343f9aef2b6697466058165c5fc2ddf0f00e882b

Relevant manuscript-specific later commits must be identified separately in the provenance record.
2.2 Established E2-P3 results
The following are inherited and must not be presented as new E2-P4 discoveries:
- The coverage-gap reduction (U\subseteq U'\iff U\cap(H'\setminus U')=\varnothing).
- The rectangular-target corner-region criterion under its proved hypotheses.
- Planar containment for rectangular targets under the corresponding source conditions.
- The certified noncontainment witness ((2/3,2/3,2/3)) for the parity-to-integer example.
- The nontrivial-to-nontrivial 3D containment failure associated with primes (2,7,13), denominator (9\to3), and box ((2,2,3)).
- The distinction between full source-cell dimensionality and the dimension of a geometric obstruction.
E2-P3's 49/49 full-cloud result and 26 unit tests are preserved as reported. A local run that stopped after V03 must not be represented as a completed local full verification.
2.3 E2-P3 infinite-family extension
The family

[
x_{a,b,c}=\frac{2R^2}{9},
\qquad
R=2^{2+6a}7^{2+3b}13^{3+3c},
]

with (a,b,c\ge0), gives

[
C(x_{a,b,c})=\frac{R^2}{3}.
]

Its persistent source-cell witness provides an infinite family of containment failures with a rectangular target lattice.

This result should be recorded in an append-only E2-P3 theorem addendum, with its proof and scope explicitly checked.

It remains a control, not the main E2-P4 theorem target.

3. Definition of nonrectangular target geometry
3.1 Modular relation lattice
For a positive rational state (x=a/b) with active prime coordinates (p_1,\ldots,p_k), define

[
\chi_b:\mathbb Z^k\longrightarrow(\mathbb Z/b\mathbb Z)^\times,
\qquad
\chi_b(\alpha)=\prod_{i=1}^k p_i^{\alpha_i}\bmod b.
]

Its kernel is

[
\Lambda_b=\ker\chi_b.
]

Let

[
o_i=\operatorname{ord}_b(p_i),
\qquad
H_b=\langle p_1,\ldots,p_k\rangle
\subseteq(\mathbb Z/b\mathbb Z)^\times.
]
3.2 Rectangular lattice
A relation lattice is coordinate-rectangular when

[
\Lambda_b=\bigoplus_{i=1}^k o_i\mathbb Z e_i.
]

Equivalently,

[
|H_b|=\prod_i o_i.
]

In this case, the prime-coordinate relations are independent, and the Graver structure is axis-aligned after coordinate scaling.

This definition concerns the relation lattice, not the visual shape of an individual cell or its bounding box.
3.3 Nonrectangular lattice
A relation lattice is nonrectangular when

[
\boxed{|H_b|<\prod_i o_i.}
]

It possesses nontrivial relations coupling at least two prime coordinates.

A lattice may be proper and nontrivial while still being rectangular. Therefore the conditions

[
\Lambda_b\ne\mathbb Z^k
]

and

[
\Lambda_b\text{ nonrectangular}
]

must not be conflated.
3.4 Primary transition class
The principal E2-P4 class consists of FIELD-I transitions

[
x\longrightarrow x'=C(x)
]

with:
- The same active prime-coordinate set.
- The same exponent box (Q).
- Occurrence inclusion (F_x\subseteq F_{x'}).
- Nonrectangular source and target lattices.
- Distinct source and target relation lattices.
Strict lattice enlargement

[
\Lambda\subsetneq\Lambda'
]

is the first theorem track.

SHRINK and INCOMPARABLE lattice relationships form separate secondary tracks, because E2-P2 demonstrated that they can occur under FIELD-I while finite occurrence inclusion still holds.

4. Geometric transport objects
For each relation lattice (\Lambda) and exponent box (Q), define

[
F(\Lambda,Q)=(\Lambda\cap Q)\setminus{0}.
]

Let

[
U(\Lambda,Q)
]

denote the realized union of all source-defined Graver cells, including lower-dimensional cells.

For a fixed-coordinate FIELD-I transition, write

[
U=U(\Lambda,Q),
\qquad
U'=U(\Lambda',Q).
]

Define the transport-loss region

[
\boxed{\Delta(\Lambda,\Lambda';Q)=U\setminus U'.}
]

Also define

[
H'=\operatorname{conv}(F')
]

and the target coverage gap

[
\mathcal G'=H'\setminus U'.
]

Because FIELD-I ensures source occurrence inclusion,

[
U\subseteq H'.
]

Therefore

[
\boxed{\Delta=U\cap\mathcal G'.}
]

This is an inherited elementary reduction.

The research objective is to characterize (\Delta) through arithmetic properties of (\Lambda,\Lambda') and (Q), rather than reconstructing all cells in both unions for every instance.
4.1 Exact transport outcomes
Every specimen must be assigned one of four geometric relationships:
Classification	Exact condition
EQUAL	(U=U')
SOURCE_CONTAINED	(U\subsetneq U')
TARGET_CONTAINED	(U'\subsetneq U)
INCOMPARABLE	Neither union contains the otherThe program must separately report abstract-cell survival, realized geometric containment and topology.

A change in Betti numbers is not sufficient to determine any of these containment relationships.

5. Primary coupled-target family — P4-F110
5.1 Exact FIELD-I transition
Define, for every integer (m\ge1),

[
\boxed{
x_m=\frac{2\cdot110^{4m}}9
\quad\xrightarrow{C}\quad
x_m'=\frac{110^{4m}}3.
}
]

The active prime coordinates are

[
P=(2,5,11),
]

and both states have the same box

[
Q_m=[0,2m]^3.
]

The source and target remain nonrectangular.
5.2 Arithmetic derivation
The source eligible indices satisfy

[
d\equiv1\pmod9.
]

Since (10) and (55) are eligible,

[
G(x_m)\mid\gcd(10-1,55-1)=9.
]

Every eligible index is congruent to 1 modulo 9, so (G(x_m)) is divisible by 9. Hence

[
G(x_m)=9.
]

The indices (10^{2m}) and (55^{2m}) are also eligible, and their least common multiple is (110^{2m}). Therefore

[
L(x_m)=110^{2m}.
]

The collective operator gives

\frac{110^{4m}}3.
]

Thus the entire family consists of exact FIELD-I transitions.
5.3 Relation lattices
Modulo 9,

[
2\equiv2,\qquad
5\equiv2^5,\qquad
11\equiv2.
]

Since 2 has multiplicative order 6 modulo 9,

[
\boxed{
\Lambda_9=
{(a,b,c)\in\mathbb Z^3:
a-b+c\equiv0\pmod6}.
}
]

Modulo 3, all three primes are congruent to (-1), giving

[
\boxed{
\Lambda_3=
{(a,b,c)\in\mathbb Z^3:
a+b+c\equiv0\pmod2}.
}
]

Consequently,

[
\Lambda_9\subsetneq\Lambda_3,
]

and both lattices are genuinely coupled and nonrectangular.

This makes P4-F110 a direct test of the question left open by E2-P3.
5.4 Initial benchmark (m=1)
For

[
x_1=\frac{2\cdot110^4}{9},
\qquad
x_1'=\frac{110^4}{3},
]

the box is ([0,2]^3).

An initial exact enumeration gives:
Property	Source	Target
Denominator	9	3
Occurrence vertices	5	13
Graver vectors in the region	8	18
Abstract edges	7	45
Abstract two-cells	2	36
Abstract three-cells	0	3These preflight counts must be reproduced by the E2-P4 builder and by an independent audit before being promoted to certified package results.

No geometric containment verdict is preregistered as true.
5.5 Main theorem obligation
For the family P4-F110, determine whether

[
U(\Lambda_9,Q_m)
\subseteq U(\Lambda_3,Q_m)
]

holds for all (m\ge1), fails beyond a threshold, or displays a more complicated pattern.

The result must cover the parameter (m) generally, under stated hypotheses, rather than merely report a finite census.

A successful theorem may characterize the exact parameter values for which containment holds or construct an infinite family of noncontainment witnesses.

The geometric result must be distinguished from the elementary arithmetic proof establishing the FIELD-I transition.

6. Track A — Residual planar containment CP3-A
6.1 Open conjecture
Let (\Lambda,\Lambda'\subseteq\mathbb Z^2) be the relation lattices of a valid fixed-box FIELD-I transition, with

[
\Lambda\subsetneq\Lambda'.
]

The unresolved conjecture is:

[
\boxed{
U(\Lambda,Q)\subseteq U(\Lambda',Q).
}
]

E2-P3 found no counterexample in the tested planar enlargement cases, but the unrestricted statement remains unproved.
6.2 Exclusions from the new proof search
GEO-I v012 already proves target hull coverage in its normalized stabilized regime.

Whenever the target satisfies G12-T8,

[
U'=H'.
]

Because

[
U\subseteq\operatorname{conv}(F)
\subseteq\operatorname{conv}(F'),
]

containment follows automatically.

These cases must be labelled INHERITED.

The new proof search concerns:
- Exceptional hollow-box targets.
- Sub-threshold targets.
- Other planar targets outside the inherited coverage hypotheses.
Rectangular-target cases already covered by E2-P3 must also be separated.
6.3 Main planar theorem target — P4-T1
Prove or refute CP3-A for the remaining nonrectangular target cases.

A proof should explain why source Graver cells cannot penetrate the uncovered target regions.

Possible approaches include arithmetic restrictions on source-cell generators, boundary congruences, and exact descriptions of target holes.

A counterexample must provide an exact FIELD-I transition and a rational point belonging to a source cell but outside every target cell.
6.4 Exact planar audit
Reclassify the completed E2-P3 corpus before generating new instances.

Preserve the recorded partition of its 266 original ENLARGE cases:
- 40 inherited hull-covered.
- 164 rectangular-target cases.
- 14 hollow-box cases.
- 48 sub-threshold cases.
The expanded planar corpus and its resource-limited/skipped cases must be retained with unchanged provenance.

The experiment must distinguish already proved containment from finite-exact containment that still lacks a general theorem.

7. Track B — Nonrectangular three-dimensional transport
7.1 Main question
Does a genuinely coupled target lattice admit an arithmetic criterion predicting whether an inherited source cell intersects its uncovered geometric region?

The primary target is an exact characterization of

[
\Delta(\Lambda,\Lambda';Q)
]

for a meaningful class of coupled three-coordinate transitions.
7.2 Essentiality classification
Every noncontainment witness must be classified by:

Coordinate support: the coordinates on which the witness and source-cell generators depend.

Geometric dimension: the affine dimension of the failing source cell.

Coordinate-face irreducibility: whether containment fails after restricting the paired lattice geometries to any coordinate face.

Arithmetic coupling: whether the target relation lattice is genuinely nonrectangular and whether the obstruction uses those relations.

A witness is called ESSENTIAL_3D only if the declared coordinate-face restrictions are all contained and the obstruction depends on all three coordinates.

The restriction procedure must be defined mathematically. A coordinate-face lattice restriction is not automatically a separately realizable FIELD-I transition.
7.3 Existing controls
Retain the following negative controls:
- E2-P1: parity lattice to (\mathbb Z^3), noncontainment at ((2/3,2/3,2/3)).
- E2-P3: the nontrivial-to-nontrivial (9\to3) case with primes ((2,7,13)), ending at a rectangular target lattice.
These controls are not new discoveries in E2-P4.
7.4 New coupled-target search
The first search class is the P4-F110 family.

Next, explore FIELD-I transitions whose target residue groups have multiple nontrivial coordinate relations, with source and target remaining inside the same prime-coordinate box.

Classify each pair as:

EQUAL, ENLARGE, SHRINK or INCOMPARABLE.

Search for:
1. Strict enlargement with complete geometric containment.
2. Strict enlargement with noncontainment.
3. Incomparable lattices with occurrence inclusion and noncontainment.
4. Cases where abstract cells disappear but their realizations remain covered.
5. Essentially three-coordinate containment failures.
A lattice-only candidate must not be promoted to a FIELD-I result without an exact realization.

8. Arithmetic obstruction theory
8.1 Transport obstruction definition
A transport obstruction is a tuple

[
\mathcal O=(\Lambda,\Lambda',Q,c,w)
]

such that:

[
c\in K_{\mathrm{abs}}(\Lambda,Q),
]

[
w\in P(c),
]

and

[
w\notin U(\Lambda',Q).
]

For a FIELD-I obstruction, include the exact states (x,x') and verify (x'=C(x)).
8.2 Proposed P4-T2 — Coupled-target obstruction criterion
Determine whether a noncontainment witness can be characterized by finitely many arithmetic relations among the source and target Graver directions, target congruence constraints and coordinate bounds.

Seek a theorem of the form

[
U\not\subseteq U'
\iff
\text{an explicitly defined arithmetic obstruction occurs}
]

within a declared class.

The right-hand side must be independently computable without simply rebuilding the complete target geometric union.

A one-sided sufficient obstruction criterion is also acceptable if it applies generally and is proved.
8.3 Proposed P4-T3 — Parameter-family classification
For a fixed pair of nonrectangular lattices and a family of growing boxes (Q_m), characterize containment as a function of (m).

The primary candidate is P4-F110.

Do not assume containment failure is monotone as the box grows.

Unlike GEO-I v004's embeddedness-obstruction problem, target coverage can change when new cells become available. An obstruction that exists in one box may disappear in a larger box.

Therefore a finite obstruction antichain or a bounded search window must be proved, not inferred from Dickson's lemma alone.
8.4 Proposed P4-T4 — Higher-dimensional extension
Establish a general result applying to a coupled family in dimension (k\ge3), or prove that a plausible planar transport principle fails in an essentially higher-dimensional way.

A construction obtained by adding passive independent coordinates is not sufficient as evidence of essential higher-dimensional coupling.
8.5 Proposed P4-T5 — Predictive arithmetic criterion
Develop a procedure accepting the modular relation data of a valid FIELD-I transition and predicting realized containment or a certified obstruction.

For each supported case, provide:
- Input hypotheses.
- Exact prediction.
- Mathematical correctness proof.
- Computational cost.
- Comparison with full geometric reconstruction.
- Explicit unsupported cases.
Prediction is successful only within its proved domain.

9. Exact containment certification
9.1 Negative certificate
For (U\not\subseteq U'), produce:
1. A valid source maximal cell (c).
2. A rational witness (w).
3. Exact cell parameters demonstrating (w\in P(c)).
4. A complete list of target maximal cells or equivalent exact target coverage representation.
5. An exact violated inequality for every target cell, proving (w\notin U').
6. The arithmetic and lattice provenance of the transition.
This certificate must be checkable without rerunning the original search.
9.2 Positive certificate
For (U\subseteq U'), certify that every maximal source cell is covered by the target union.

Acceptable methods include exact polyhedral subdivision, complete rational disjunctive feasibility, or a proved general theorem whose hypotheses have been checked.

Source-cell vertex inclusion is not sufficient.

Numerical probes and volume comparisons are supporting diagnostics only.
9.3 Geometry and topology
Compute abstract Betti numbers separately from realized-union Betti numbers.

Where feasible, derive the latter from an exact embedded subdivision or the nerve of a certified convex-cell cover.

Do not treat topology as a substitute for containment: a target may gain or lose holes while retaining the entire source union.

10. Preregistered experimental phases
Phase	Work	Acceptance
P4-E0	Source lock, E2-P3 addenda, theorem-overlap classification	SOURCE_PASS
P4-E1	Reproduce P4-F110 arithmetic, fibres and Graver cells	ARITH_PASS
P4-E2	Exact geometric containment for the coupled-target benchmark	GEOMETRY_PASS
P4-E3	Residual planar CP3-A theorem or counterexample search	PLANAR_AUDIT_COMPLETE
P4-E4	Coupled 3D parameter-family and obstruction investigation	COUPLED_3D_AUDIT_COMPLETE
P4-E5	General proof, adversarial falsification and prior-art review	THEOREM_PASS, COUNTEREXAMPLE or OPEN10.1 Resource limits
E2-P3 required approximately 1,406 seconds for its full-cloud verification, and the local device stopped longer runs.

Accordingly, E2-P4 must use:
- Individually executable verification phases.
- Deterministic and resumable search checkpoints.
- Fast and full verification modes.
- Immutable intermediate certificates.
- Explicit resource ceilings and timeout outcomes.
- Independent certificate checking without rebuilding all data.
Prefer local verification shards that can complete within the observed shell limit; expensive global audits must be decomposed rather than silently skipped.

The initial three-dimensional search should prioritize small boxes and the primary (m=1) specimen before broader parametric runs.

Do not claim completion of a computational range unless every member was processed.

11. Falsification programme
ID	Hypothesis	Falsification target
P4-F1	Strict enlargement between nonrectangular lattices preserves realized geometry	Exact coupled-target noncontainment
P4-F2	A planar containment principle extends automatically to 3D coupled targets	Essential 3D counterexample
P4-F3	Lattice index and coordinate orders determine geometric containment	Two cases with equal such coarse data and different outcomes
P4-F4	Target-hole existence implies source-to-target noncontainment	Target has holes but no source cell intersects them
P4-F5	Containment failure persists under box enlargement	Exact failure followed by containment in a larger box
P4-F6	Preserved source vertices and Graver generators determine realized containment	Counterexample distinguishing abstract persistence from region coverageThese are hypotheses to test, not asserted universal laws.

Where the data already supply a counterexample, record it as an inherited control.

Every new counterexample must be checked against GEO-I and the E2-P1/P2/P3 records.

12. Required outputs
Package: GEO_HD_E2_P4_v001.zip
GEO_HD_E2_P4_v001/
│
├── README.md
├── STATUS.json
├── MANIFEST.json
│
├── SPEC/
│   └── E2_P4_SPEC_v001.md
│
├── theory/
│   ├── DEFINITIONS.md
│   ├── THEOREMS.md
│   ├── PROOF_OBLIGATIONS.md
│   ├── SOURCE_OVERLAP.md
│   └── COUNTEREXAMPLES.md
│
├── src/
│   ├── build_p4.py
│   ├── arithmetic_family.py
│   ├── coupled_lattices.py
│   ├── target_gap.py
│   ├── exact_containment.py
│   ├── planar_residual.py
│   ├── coupled_3d.py
│   ├── audit_p4.py
│   └── make_figures.py
│
├── tests/
│   ├── test_arithmetic.py
│   ├── test_lattices.py
│   ├── test_containment.py
│   ├── test_coupled_3d.py
│   └── test_certificates.py
│
├── data/
│   ├── P4_F110.json
│   ├── P4_PLANAR_CORPUS.json
│   ├── P4_3D_CORPUS.json
│   └── SEARCH_LIMITS.json
│
├── results/
│   ├── P4_REPORT.md
│   ├── P4_ARITHMETIC.json
│   ├── P4_GEOMETRY.json
│   ├── P4_PLANAR.json
│   ├── P4_3D.json
│   ├── P4_CERTIFICATES.json
│   ├── P4_COUNTEREXAMPLES.json
│   ├── P4_THEOREM_AUDIT.md
│   └── P4_VERIFY_LAST.json
│
├── ERRATA/
│   └── SOURCE_AND_SCOPE_ADDENDUM.md
│
├── figures/
│   ├── coupled_target_geometry.png
│   ├── planar_residual_gaps.png
│   └── transport_obstruction.png
│
├── RUN_WINDOWS.bat
└── RUN_VERIFY.py
The package must be self-contained and runnable on Windows.

Source-engine copies must be hash-pinned, attributed and separated from new implementation code.

Existing project files and all earlier packages must remain untouched.
12.1 Mandatory final report
P4_REPORT.md must state:
1. Exact FIELD-I arithmetic and relation-lattice data.
2. Whether both lattices are nonrectangular.
3. Verified source and target occurrence fibres.
4. Abstract-cell changes.
5. Realized geometric containment or noncontainment.
6. Exact positive or negative containment certificates.
7. Parameter-family results and theorem proofs.
8. Planar CP3-A status.
9. Essential higher-dimensional findings.
10. Novelty assessment and unresolved obligations.
The scientific conclusions must be understandable independently of the code and figures.

13. Verification and scientific gates
EXACT_PASS
All declared arithmetic, lattice and geometric computations have exact certificates and pass their verification tests.

This does not imply a new theorem.
PLANAR_THEOREM_PASS
The residual planar CP3-A conjecture is proved, falsified or characterized within a meaningful general class by a complete mathematical argument.

Finite absence of counterexamples alone does not qualify.
COUPLED_3D_THEOREM_PASS
A general theorem or obstruction classification is proved for genuinely coupled target geometry in at least three dimensions.

An isolated exact witness is reported as 3D_WITNESS_PASS, not as a universal theorem.
SCOPED_THEOREM_PASS
A complete general result is proved for a declared parameter family such as P4-F110.

It may be elementary or an inherited specialization; novelty must be assessed separately.
C3_CANDIDATE
A general result has been established that adds substantive mathematical information about inter-fibre realized geometry beyond existing GEO-I and standard geometric results.

A prior-art audit is mandatory before promoting this to the governing GEO-HD-1 C3 verdict.
COUNTEREXAMPLE
A proposed transport law fails with an independently checkable exact witness.
OPEN / UNAVAILABLE
Unproved questions and incomplete computations retain their explicit statuses.

14. Immediate executable milestone
E2-P4 / P4-E0–E2 — Coupled-Target Transport Preflight

Begin with the exact family

[
\frac{2\cdot110^{4m}}9
\longrightarrow
\frac{110^{4m}}3.
]

For (m=1):
1. Reproduce the FIELD-I transition using (D,L,G,C).
2. Certify the source lattice (a-b+c\equiv0\pmod6).
3. Certify the target lattice (a+b+c\equiv0\pmod2).
4. Confirm both lattices are nonrectangular.
5. Reproduce the 5-to-13 occurrence-fibre transition and the abstract-cell census.
6. Determine exact realized containment in both directions.
7. Produce complete containment or noncontainment certificates.
8. Check the outcome against frozen GEO-I results.
9. Investigate the next parameter values under explicit resource limits.
10. Formulate the first general P4-F110 theorem candidate.
Do not begin a broad coupled-lattice census before this preflight is certified.

15. Final research question
E2-P4 must answer:
When FIELD-I changes the modular coupling among existing UNNS occurrence coordinates, can we characterize the resulting geometric persistence or obstruction through arithmetic laws rather than exhaustive geometric reconstruction?

Its central deliverable is an exact mathematical understanding of realized transport into nonrectangular target geometries.

A successful result would connect the arithmetic of generation with the geometric organization of admissible occurrence relationships across different states.

That is the intended contribution of E2-P4 to the broader GEO-HD-1 programme.

END — GEO-HD-1B / E2-P4 Specification v001