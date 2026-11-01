The next milestone must address realized geometric transport, not merely changes in Graver generators or abstract cell counts.

The decisive question is whether arithmetic information can tell us, before reconstructing the full target geometry, which regions of an existing UNNS occurrence geometry remain covered after a generative transition.

I have checked the relevant frozen GEO-I v003, v004 and v012 mathematical records. They give us an exact starting reduction and also identify what would merely repeat existing results.
GEO-HD-1B / E2-P3
Realized Geometric Transport: Coverage, Obstruction, and Higher-Dimensional Persistence
Specification: E2-P3 v001
Parent programme: GEO-HD-1 — Higher-Dimensional Generative Geometry of the UNNS Substrate
Predecessor: E2-P2 — Arithmetic Criteria for Geometric Transport Between Nontrivial Relation Lattices
Status: Proposed governing specification — ready for local execution
Working directory: GEO_HD_NEXT_MILESTONE/GEO_HD_1_PROJECT/
Source policy: Frozen GEO-I and Foundations records; GitHub read-only.

1. Research objective
E2-P1 and E2-P2 established that FIELD-I preserves occurrence indices while the geometric structures constructed from those indices may change substantially.

Their results distinguish three kinds of persistence:

[
F_x\subseteq F_{C(x)}
]

for occurrence vertices;

[
K_{\mathrm{abs}}(x)\not\subseteq
K_{\mathrm{abs}}(C(x))
]

in general for abstract Graver cells; and neither direction of inclusion is guaranteed for realized geometric unions.

E2-P2 further established arithmetic procedures for predicting Graver-generator and abstract-cell survival, together with a complete scoped theorem for the P2-F21 family.

However, these algebraic procedures do not decide the general question

[
\boxed{U(x)\subseteq U(C(x));?}
]

where (U(x)) is the union of the source-defined geometric cells.

E2-P3 investigates whether realized geometric persistence has arithmetic criteria and obstruction laws that extend beyond the established individual-fibre GEO-I theory.
1.1 Primary scientific question
Given a FIELD-I transition

[
x\xrightarrow{C}x',
]

can we determine, using arithmetic information about the source and target relation lattices, which parts of (U(x)) are contained in (U(x')), which are lost, and why?

The principal objective is a mathematical theorem or obstruction classification, not merely a geometric comparison algorithm.
1.2 Two research tracks
Track A — Residual planar geometric containment

Prove or refute the remaining planar containment conjecture CP2 for relation-lattice enlargements whose target geometry is not already covered by the frozen GEO-I convex-stabilization theorem.

Track B — Essential higher-dimensional geometric obstruction

Identify and characterize containment failure in genuinely coupled three-coordinate FIELD-I transitions, preferably where both source and target relation lattices are nontrivial.

These tracks share a common exact-containment engine, but their mathematical obligations and acceptance criteria remain distinct.

2. Frozen results and exclusions
2.1 Inherited mathematical baseline
Source	Established result	E2-P3 treatment
GEO-I v002	Graver-cell construction and source-defined abstract complexes	Reuse
GEO-I v003	Exact geometric realization, intersections, subdivisions and nerve-based topology	Reuse
GEO-I v004	Finite obstruction templates for embeddedness	Reuse; distinguish from transport obstruction
GEO-I v005–v012	Planar coverage, hollow-box geometry and stabilization	Apply before launching new coverage searches
E2-P1	Parity-to-integer transport; noncontainment in three dimensions	Regression and negative control
E2-P2	Abstract-cell survival criteria, P2-F21 theorem and planar transport observations	Frozen experimental baselineThe source lock must preserve the exact theorem hypotheses and statuses.
2.2 Important distinction from GEO-I v004
GEO-I v004 asks whether the cells within one abstract complex intersect as a valid embedded polyhedral complex.

E2-P3 instead asks whether the realized cell union associated with a source fibre is contained in the realized cell union associated with a different target fibre.

These are different questions.

A source complex may be non-embedded while its realized union is fully contained in the target union.

Conversely, source cells can be lost geometrically even though every source occurrence vertex persists.

A new theorem must concern the relationship between two fibres under a declared transition, not simply reclassify the embeddedness of either fibre.

3. Mathematical setting
3.1 Common coordinate space
Let

[
x=\frac ab,\qquad x'=C(x)=\frac{a'}{b'}
]

be reduced rational states with nonempty occurrence fibres.

For the primary experiments assume the same active prime-coordinate set

[
P={p_1,\ldots,p_k}
]

and the same exponent box

[
Q=[0,q_1]\times\cdots\times[0,q_k].
]

Define

[
\Lambda=\ker\chi_b,\qquad
\Lambda'=\ker\chi_{b'},
]

and

[
F=(\Lambda\cap Q)\setminus{0},
\qquad
F'=(\Lambda'\cap Q)\setminus{0}.
]

FIELD-I gives

[
F\subseteq F'.
]

The relation lattices may be equal, ordered or incomparable. No lattice-order assumption is required for the general geometric question.
3.2 Realized geometric unions
Let the source and target cell collections be those specified by the frozen GEO-I Graver grammar.

Write

[
U=\bigcup_{c\in K_{\mathrm{abs}}}P(c),
\qquad
U'=\bigcup_{c'\in K'_{\mathrm{abs}}}P(c').
]

Also define the convex hulls

[
H=\operatorname{conv}(F),
\qquad
H'=\operatorname{conv}(F').
]

Since (F\subseteq F'),

[
H\subseteq H'.
]

Because every source cell is the convex hull of its occurrence vertices,

[
U\subseteq H\subseteq H'.
]

These inclusions are exact and require no assumption about embeddedness.

4. Fundamental reduction — the target coverage gap
Define the target's uncovered hull region:

[
\boxed{\mathcal G'=H'\setminus U'.}
]

Then

[
U\setminus U'=U\cap\mathcal G'.
]

Therefore:

[
\boxed{
U\subseteq U'
\iff
U\cap\mathcal G'=\varnothing.
}
]

This is the Coverage-Gap Reduction.

Its proof is elementary and follows directly from (U\subseteq H'). It is not itself a new theorem qualifying for GEO-HD-1's C3 criterion.

Its importance is operational: it identifies the only region in which geometric persistence can fail.
4.1 Immediate consequence
If

[
U'=H',
]

then automatically

[
U\subseteq U'.
]

Thus any theorem establishing complete target-hull coverage also supplies a sufficient condition for realized geometric persistence.
4.2 Application of GEO-I v012
The frozen GEO-I result G12-T8 proves, for the normalized planar lattice (\Gamma_{d,s}),

[
U'=H'
]

whenever

[
Q_1,Q_2\ge d,
\qquad Q\ne(d,d),
]

under that theorem's full hypotheses.

A general planar lattice must first be reduced to the appropriate normalized model using the established GEO-I scaling correspondence.

Consequently, all E2-P3 cases satisfying G12-T8 are classified as:

INHERITED_CONTAINMENT.

They must not be counted as new discoveries.
4.3 The genuinely unresolved region
The planar research is restricted to target fibres that are not already certified hull-covered by the frozen source theory.

These may include:
- Exceptional hollow boxes.
- Boxes below the planar stabilization thresholds.
- Other target configurations outside the inherited theorem's hypotheses.
The remaining question is whether source cells actually intersect their target's uncovered regions.

An uncovered target region by itself does not imply transport failure.

5. Track A — Residual planar containment
5.1 Conjecture CP3-A
Let (\Lambda,\Lambda'\subseteq\mathbb Z^2) be full-rank relation lattices associated with a FIELD-I transition, with the same coordinate box and

[
\Lambda\subsetneq\Lambda'.
]

The conjecture is:

[
\boxed{U(\Lambda,Q)\subseteq U(\Lambda',Q).}
]

This is the residual version of E2-P2's CP2 conjecture.

It is to be tested and, if possible, proved under the stated conditions.

It is not asserted as true.
5.2 Mandatory source reduction
For every planar specimen:
1. Determine the source and target lattice normalization parameters.
2. Identify the associated pure modular-lattice models.
3. Transform the exponent boxes correctly under the normalization.
4. Test GEO-I v005, v007, v010 and v012 coverage hypotheses.
5. Remove inherited hull-covered cases from the unresolved theorem search.
6. For remaining cases, construct the target uncovered regions exactly.
The research must not repeat the planar stabilization proof or treat previously classified exceptional holes as new.
5.3 Principal theorem obligation
Find arithmetic conditions under which no source Graver cell can intersect a target uncovered region.

Possible proof approaches include:
- Congruence restrictions on source cell vertices.
- Target boundary and strip geometry.
- Constraints on permissible source Graver directions.
- The relationship between source lattice index and target hole geometry.
- Explicit covering cells or separating inequalities.
- Exhaustive classifications of bounded exceptional target families.
A satisfactory result must characterize a general family or establish a universal statement under stated hypotheses.

Finite enumeration alone is insufficient.
5.4 Counterexample obligation
If CP3-A is false, produce a minimal exact witness consisting of:
- A realizable FIELD-I transition (x\to C(x)).
- Strict relation-lattice inclusion.
- A common prime-coordinate box.
- A source cell (c).
- A rational point (w\in P(c)\setminus U').
- A proof that (w\notin U').
- A check that the example is outside the inherited hull-covered class.
A counterexample outside the FIELD-I transition grammar must be labelled as a lattice-model counterexample, not automatically as a FIELD-I counterexample.

6. Track B — Essential three-dimensional containment obstruction
6.1 Research target
Investigate transitions with

[
k=3,
]

fixed prime-coordinate support and box, and both relation lattices nontrivial.

The primary search should include transitions satisfying

[
\Lambda\subsetneq\Lambda'
]

but must separately retain SHRINK and INCOMPARABLE cases, because E2-P2 established that these relationships can occur under FIELD-I despite occurrence-vertex inclusion.
6.2 Essentiality requirements
A candidate obstruction should be classified on three independent levels.

Coordinate support: Does the source cell witnessing failure depend on all three coordinates?

Geometric dimension: What is the affine dimension of the cell and of the region lost?

Irreducibility: Does the corresponding containment failure disappear in every two-coordinate coordinate-face restriction?

A genuinely three-coordinate result must not be declared solely because the ambient representation has three axes.

The strongest acceptable witness is one requiring all three coordinates, absent from all coordinate-face restrictions, and arising from genuinely coupled modular relations.
6.3 Primary control
Reuse E2-P1:

[
\frac{110^4}{3}
\rightarrow
\frac{2\cdot110^4}{3}
\rightarrow
110^4.
]

Its exact containment-failure witness includes

[
w=\left(\frac23,\frac23,\frac23\right).
]

This is a negative control for realized containment.

However, the final target lattice is (\mathbb Z^3). Therefore this example alone cannot establish a theorem about transport between two nontrivial lattices.
6.4 New specimen discovery
Search for actual FIELD-I transitions with:
- Three active prime coordinates.
- Unchanged exponent box.
- Nontrivial source and target relation lattices.
- Verified FIELD-I occurrence inclusion.
- A target uncovered-hull region.
- A source cell intersecting that region.
Lattice-only constructions may be used to discover candidates, but a candidate must be arithmetically realized by a valid FIELD-I transition before entering the primary results.

If no suitable specimen exists within the preregistered search limits, report UNAVAILABLE or NO_WITNESS_IN_SCOPE, not a universal nonexistence theorem.

7. Exact geometric containment certificates
This is a mandatory technical component.
7.1 Maximal-cell representation
Represent the source and target unions as

[
U=\bigcup_{i=1}^{m}P_i,
\qquad
U'=\bigcup_{j=1}^{n}Q_j,
]

where the cells are geometrically maximal convex parallelotopes after removing redundant contained cells.

Use exact rational vertex and inequality representations.
7.2 Noncontainment certificate
A valid noncontainment certificate must contain:
1. The identified source cell (P_i).
2. The exact rational witness (w).
3. Exact parameters proving (w\in P_i).
4. For every target maximal cell (Q_j), an exact violated membership inequality proving (w\notin Q_j).
5. The original source and target occurrence/lattice records.
This is a fully checkable proof of

[
U\not\subseteq U'.
]

No floating-point tolerance may determine this verdict.
7.3 Containment certificate
A positive verdict requires a certificate that each maximal source cell is covered by the union of target cells.

This may use:
- An exact polyhedral subdivision.
- A finite convex covering certificate.
- Exact disjunctive linear-feasibility checks.
- An inherited theorem such as G12-T8, with its hypotheses independently verified.
Checking only the vertices or corners of source cells is insufficient.

Checking only volumes is also insufficient, because lower-dimensional uncovered features may have zero ambient volume.
7.4 Exact disjunctive test
Suppose each target cell has a complete rational inequality description

[
Q_j={z\le b_j},
]

including affine-hull equalities encoded as paired inequalities.

A point lies outside the target union exactly when, for each (j), at least one defining inequality of (Q_j) is strictly violated.

The algorithm may search over the corresponding disjunctions while constraining (z) to a source cell.

For every branch, feasibility must be decided with exact rational arithmetic, including correct treatment of strict inequalities.

Prune redundant or infeasible branches where possible.

This provides an exact general decision procedure, but the existence of a decision procedure is not itself the desired new arithmetic transport theorem.

8. Arithmetic transport-obstruction theory
8.1 Definition of a transport obstruction
A realized transport obstruction is a tuple

[
\mathfrak o=(\Lambda,\Lambda',Q,c,w)
]

such that:
- (c) is a valid source Graver cell.
- Every vertex of (c) persists as an occurrence vertex.
- (w\in P(c)).
- (w\notin U').
For FIELD-I results, the tuple must also include the exact rational transition realizing (\Lambda\to\Lambda').
8.2 Proposed theorem P3-T1
Determine whether a useful finite collection of arithmetic transport-obstruction templates exists for a declared family of lattice pairs.

The templates should identify possible containment failures using relation data, Graver directions and coordinate bounds, without requiring reconstruction of the full target union in every instance.

The search should distinguish:
- Fixed-pair decidability.
- Parameter-family classification.
- Universal results under explicit hypotheses.
A fixed finite-box algorithm is routine and does not establish a universal obstruction classification.
8.3 Proposed theorem P3-T2
Characterize when the target's uncovered-hull regions are inaccessible to all source cells under lattice inclusion.

The strongest planar outcome would resolve CP3-A universally.

A narrower theorem covering a meaningful exceptional family is also acceptable.
8.4 Proposed theorem P3-T3
Establish a higher-dimensional transport-obstruction criterion, or prove a counterexample to a plausible planar extension.

Its contribution must depend essentially on higher-dimensional coupling rather than simply appending a passive axis to a planar example.
8.5 Proposed theorem P3-T4 — Predictive criterion
Construct an arithmetic predictor that determines a specified realized-containment outcome without reconstructing all target cells.

Evaluate it against the exact geometric decision engine.

Report:
- Input assumptions.
- Predicted verdict.
- Proven correctness domain.
- Computational complexity.
- Comparison with direct reconstruction.
- Explicit cases where prediction is unavailable.
A correct exact test is valuable, but C3 requires more than an implementation of generic polyhedral containment.

9. Preregistered experimental programme
P3-E0 — Source and correction lock
Read the frozen GEO-I v003, v004, v005–v012 results and the E2-P1/P2 records.

Apply the two E2-P2 theorem-text corrections and a separate source-overlap addendum.

Classify target cases as inherited hull-covered, residual non-hull-covered, or outside the normalized planar model.

Gate: SOURCE_PASS
P3-E1 — Exact containment engine
Implement and independently audit positive and negative geometric containment certificates.

Reproduce the verified E2-P1 three-dimensional noncontainment and E2-P2 planar containment results.

Verify that the engine handles cells that overlap improperly and lower-dimensional cells correctly.

Gate: GEOMETRY_PASS
P3-E2 — Residual planar classification
Reanalyse the 266 previously sampled planar ENLARGE transitions.

Separate those already settled by GEO-I v012 from the genuinely residual cases.

Search exact target uncovered regions for intersections with source cells.

Prioritize exceptional and sub-threshold targets.

Expand the corpus deterministically, recording the source lattice parameters and every resource limit.

The 337 previously skipped planar states from E2-P2 must remain explicitly classified as skipped unless they are successfully evaluated.

Gate: PLANAR_AUDIT_COMPLETE

This gate records a completed bounded audit, not proof of CP3-A.
P3-E3 — Essential three-dimensional search
Start with the existing E2-P1 and E2-P2 higher-dimensional records.

Generate further valid FIELD-I transitions under fixed-coordinate constraints.

Classify their lattice relationships.

Run exact geometric containment checks, then analyze the essentiality of any witnessed failure.

Gate: 3D_WITNESS_PASS or NO_WITNESS_IN_SCOPE
P3-E4 — General theorem development
From the exact planar and three-dimensional findings, formulate the strongest general theorem candidates.

Attempt full proofs, not merely additional enumeration.

Search adversarially for counterexamples to each hypothesis.

Gate: THEOREM_PASS, COUNTEREXAMPLE or OPEN
P3-E5 — Novelty and synthesis
Determine which results are inherited consequences of existing coverage theory and which constitute additional information about transport between different occurrence geometries.

Compare with established polyhedral covering, lattice and Graver-basis methods.

Identify whether any result satisfies GEO-HD-1's central criterion C3.

Gate: C3_CANDIDATE, SCOPED_THEOREM_ONLY or RESEARCH_NEGATIVE

10. Required package and outputs
Package: GEO_HD_E2_P3_v001.zip
GEO_HD_E2_P3_v001/
│
├── README.md
├── STATUS.json
├── MANIFEST.json
│
├── SPEC/
│   └── E2_P3_SPEC_v001.md
│
├── theory/
│   ├── DEFINITIONS.md
│   ├── THEOREMS.md
│   ├── PROOF_OBLIGATIONS.md
│   ├── SOURCE_OVERLAP.md
│   └── COUNTEREXAMPLES.md
│
├── src/
│   ├── build_p3.py
│   ├── coverage_gap.py
│   ├── exact_containment.py
│   ├── planar_residual.py
│   ├── coupled_3d.py
│   └── make_figures.py
│
├── tests/
│   ├── test_containment.py
│   ├── test_planar.py
│   ├── test_coupled_3d.py
│   └── test_certificates.py
│
├── data/
│   ├── P3_CONTROLS.json
│   ├── P3_PLANAR_CORPUS.json
│   ├── P3_3D_CORPUS.json
│   └── P3_SEARCH_LIMITS.json
│
├── results/
│   ├── P3_REPORT.md
│   ├── P3_PLANAR.json
│   ├── P3_3D.json
│   ├── P3_CONTAINMENT.json
│   ├── P3_CERTIFICATES.json
│   ├── P3_COUNTEREXAMPLES.json
│   └── P3_THEOREM_AUDIT.md
│
├── figures/
│   ├── planar_gap_geometry.png
│   ├── source_target_3d.png
│   └── obstruction_witness.png
│
├── RUN_WINDOWS.bat
└── RUN_VERIFY.py
The package must preserve the earlier HD-0, E2-P1 and E2-P2 releases.

Figures are explanatory representations of exact certified geometry, not substitutes for proof.

11. Verification standards
The verification process must include:
- Exact rational arithmetic for containment and witness checking.
- Full source/target cell consistency.
- Independent replay of key certificates.
- Tamper-rejection tests.
- Correct strict-boundary handling.
- No reliance on sampling alone to certify containment.
- Explicit reporting of resource exhaustion.
- Separate abstract and realized topological calculations.
- Provenance of every specimen and source theorem.
- Clear declaration of which engines share code.
Where topology is calculated, use the realized union's exact subdivision or nerve, not the abstract complex's Betti numbers unless embedding has been established.

Resource limits must be recorded before large searches. The engine should support deterministic resumption without silently changing the sample.

12. Scientific success and falsification
12.1 Exact computation
EXACT_PASS

All declared source/target data, geometric decisions and certificates verify exactly.

This confirms the experiment but does not establish novelty.
12.2 Planar theorem
PLANAR_THEOREM_PASS

CP3-A is proved under explicit general hypotheses, or a meaningful general residual planar class is characterized by a proved containment/obstruction criterion.

A certified counterexample to unrestricted CP3-A is recorded as COUNTEREXAMPLE, with the resulting narrower theorem target identified.
12.3 Higher-dimensional theorem
3D_THEOREM_PASS

A general criterion or obstruction is proved for a genuinely coupled three-coordinate class.

An isolated three-dimensional counterexample is a valid negative result, but does not automatically satisfy this theorem gate.
12.4 Main scientific gate
C3_CANDIDATE

Requires a general mathematical result about realized geometric transport that is not already a consequence of the frozen GEO-I individual-fibre results or standard generic polyhedral-containment facts.

Potential qualifying outcomes include:
1. A new arithmetic criterion for realized containment.
2. A nontrivial finite obstruction classification for a parameter family.
3. A genuinely higher-dimensional structural obstruction theorem.
4. A proved predictor of geometric persistence that avoids full target reconstruction.
The final novelty decision requires explicit prior-art comparison and critical proof review.
12.5 Negative outcome
The programme must preserve and clearly report cases where:
- CP3-A fails.
- Higher-dimensional transport cannot be reduced to planar restrictions.
- A proposed arithmetic invariant does not predict realized geometry.
- A conjectured obstruction template is incomplete.
- A computation exceeds its declared resource budget.
- No qualifying new theorem survives source comparison.
A rigorous negative classification is scientifically legitimate.

13. Immediate executable task
E2-P3 / P3-E0 + P3-E1 — Coverage-Gap Preflight

Start by implementing the coverage-gap and exact-containment machinery against known data.

The first mandatory checks are:

Control A — E2-P2/A

[
\frac{21^8}{5}\to\frac{21^8}{4}.
]

Expected result:

[
U\subsetneq U'.
]

The source loses eight abstract Graver edges while retaining its realized geometric union inside the target.

Control B — E2-P2/B

[
\frac{55^{12}}{27}\to\frac{55^{12}}{18}.
]

Expected result:

[
U\subsetneq U'.
]

All five old Graver edges survive, and the realized first Betti number changes from 0 to 2.

Control C — E2-P1

[
\frac{2\cdot110^4}{3}\to110^4.
]

Expected result:

[
U\not\subseteq U',
]

with exact witness

[
\left(\frac23,\frac23,\frac23\right).
]

The preflight must prove these verdicts independently using exact geometric certificates.

Then classify the previously sampled planar enlargement cases under the GEO-I v012 hypotheses before beginning any new search.

Do not start broad three-dimensional enumeration until the exact positive and negative containment certificates are independently reproducible.

14. Final research mandate
The scientific objective of E2-P3 is:
Determine whether the realized geometric organization of UNNS occurrence fibres obeys arithmetic persistence laws under FIELD-I evolution, and identify the precise obstruction mechanisms when such persistence fails.

The experiment must move beyond identifying which Graver generators survive.

It must explain when whole geometric regions survive, when uncovered regions intersect an inherited source structure, and whether those events can be characterized before geometric reconstruction.

The distinction between arithmetic occurrence inclusion and geometric containment is the central mathematical subject.

END — GEO-HD-1B / E2-P3 Specification v001