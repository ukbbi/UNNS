The next milestone should be GEO-HD-1B / E2-P2 — Arithmetic Criteria for Geometric Transport Between Nontrivial Relation Lattices.

Its purpose is to establish general laws governing geometric change under FIELD-I when both the source and target retain nontrivial modular structure. This moves beyond E2-P1's special transition to the full integer lattice.

I have identified a particularly useful initial specimen:
\[
\boxed{\frac{21^8}{5}\xrightarrow{C}\frac{21^8}{4}}
\]

Both states have active primes \(3,7\) and exponent box \([0,4]^2\), while their relation lattices differ:
\[
\Lambda_5=\{(a,b):a-b\equiv0\pmod4\},
\]

\[
\Lambda_4=\{(a,b):a+b\equiv0\pmod2\}.
\]

An exact preliminary enumeration gives:
Invariant	Source	Target
Occurrence vertices	6	12
Graver edges	11	29
Source edges retained	—	3
Source edges lost	—	8

This is already a useful nontrivial-to-nontrivial transport example. More importantly, it belongs to the family
\[
\frac{21^{2h}}5\longrightarrow\frac{21^{2h}}4,\qquad h\ge1,
\]

which provides a concrete candidate for a general theorem rather than an isolated computation.
GEO-HD-1B / E2-P2
Arithmetic Criteria for Geometric Transport Between Nontrivial Relation Lattices
Specification: E2-P2 v001
Parent programme: GEO-HD-1 — Higher-Dimensional Generative Geometry of the UNNS Substrate
Predecessor: E2-P1 — Geometric Transport Under a Changing Relation Lattice
Status: READY FOR EXECUTION
Working location: GEO_HD_NEXT_MILESTONE/GEO_HD_1_PROJECT/
Source policy: Frozen GEO-I and Foundations references; GitHub read-only.

1. Research objective
E2-P1 established that monotone preservation of UNNS occurrence indices need not preserve Graver edges, higher-dimensional cells, geometric inclusion or topology.

Its principal example involved a transition from a nontrivial parity lattice to the full integer lattice.

E2-P2 investigates the more general problem:
Can arithmetic data predict the geometric structures preserved, destroyed or generated when FIELD-I moves between two distinct, nontrivial modular relation lattices?

The objective is to derive exact criteria that apply to declared families of FIELD-I transitions, rather than constructing the source and target cell complexes for every individual instance.

The scientific target is a transport theorem, not another cell census.
1.1 Primary research hypothesis
Let (x'=C(x)) be a FIELD-I transition with the same active prime-coordinate set and exponent box.

Suppose that both relation lattices are proper sublattices of (\mathbb Z^k).

The working hypothesis is that the arithmetic relationship between these lattices constrains:
1. Survival of existing Graver generators.
2. Survival of abstract cells.
3. Geometric containment of old cell realizations.
4. Appearance of new admissible cells.
5. Changes in embedding and topological structure.
The investigation must determine which constraints are universal, which require additional hypotheses, and which fail.

No general monotonicity of geometry is assumed.
1.2 Scope
Primary scope
- FIELD-I collective transitions (x\to C(x)).
- Source and target with nontrivial relation lattices.
- Fixed active prime-coordinate set.
- Fixed exponent box (q).
- Exact Graver-cell grammar inherited from GEO-I.
- General theorems, finite obstruction criteria and constructive counterexamples.
Secondary scope
- Transitions where active coordinates or exponent bounds change.
- Higher-dimensional examples involving genuinely coupled modular relations.
- Longer FIELD-I orbits and composition of transport maps.
The secondary scope begins only after the fixed-coordinate problem has been characterized.

2. Frozen mathematical baseline
2.1 FIELD-I
For a realized rational state,

[
D(x)={d\ge2^2\mid a,\ d\equiv1\pmod b},
\qquad x=\frac ab
]

in lowest terms.

Define

[
L(x)=\operatorname{lcm}D(x),
\qquad
G(x)=\gcd{d-1\in D(x)}.
]

The adopted collective operator is

[
C(x)=x+\frac{L(x)^2}{G(x)}.
]

The established inclusion law is

[
D(x)\subseteq D(C(x)).
]

This provides occurrence-vertex persistence, but not automatically cell preservation.
2.2 GEO-I
The following are inherited:
- Exact arithmetic fibre construction and region Graver moves: GEO-I v002.
- Abstract and realized cell geometry: GEO-I v003.
- Finite obstruction templates and embedding criteria: GEO-I v004.
- Planar stabilization theorems: GEO-I v005–v012.
- Parity-lattice and higher-dimensional obstruction examples: GEO-I v004 and subsequent releases.
E2-P2 must explicitly compare every candidate result with these sources.
2.3 E2-P1
The preceding experiment supplies the following control:

[
\frac{110^4}{3}
\rightarrow
\frac{2\cdot110^4}{3}
\rightarrow
110^4.
]

The parity-to-integer transition preserves its 13 old vertices but replaces all 45 old abstract Graver edges.

The E2-P1 exact report is retained as a frozen experimental baseline, subject to its two precision addenda:
1. Fibre inclusion does not imply full lattice inclusion without additional hypotheses.
2. Abstract cell survival requires both target-corner membership and target-Graver generators.
Those corrections must be incorporated into the E2-P2 definitions.

3. Exact transport setting
Let

[
x=\frac ab,\qquad
x'=\frac{a'}{b'}=C(x).
]

Assume the source and target have the same active primes

[
P={p_1,\ldots,p_k}
]

and the same exponent box

[
q=(q_1,\ldots,q_k).
]

Define the character maps

[
\chi_b:\mathbb Z^k\to(\mathbb Z/b\mathbb Z)^\times,
\qquad
\chi_b(\alpha)=\prod_i p_i^{\alpha_i}\bmod b
]

and

[
\chi_{b'}:\mathbb Z^k\to(\mathbb Z/b'\mathbb Z)^\times.
]

Their kernels are

[
\Lambda=\ker\chi_b,
\qquad
\Lambda'=\ker\chi_{b'}.
]

The occurrence fibres are

[
F=(\Lambda\cap[0,q])\setminus{0},
]

[
F'=(\Lambda'\cap[0,q])\setminus{0}.
]

For the experiment's primary cases, require

[
\Lambda\ne\mathbb Z^k,
\qquad
\Lambda'\ne\mathbb Z^k,
\qquad
\Lambda\ne\Lambda'.
]

FIELD-I gives (F\subseteq F') under the common-coordinate assumptions.

However, that finite inclusion does not generally establish (\Lambda\subseteq\Lambda').
3.1 Lattice-order classification
Every transition must be classified into exactly one relationship:
Class	Condition
EQUAL	(\Lambda=\Lambda')
ENLARGE	(\Lambda\subsetneq\Lambda')
SHRINK	(\Lambda'\subsetneq\Lambda)
INCOMPARABLE	Neither inclusion holdsDo not infer this classification from denominator size or divisibility alone.
3.2 Source-defined cell transport
Let (\mathcal G_q(\Lambda)) denote the region-restricted Graver basis.

A source cell is

[
c=P(u;g_1,\ldots,g_r),
]

with independent Graver generators and all corners in (F).

The cell survives abstractly precisely when

[
V(c)\subseteq F'
]

and

[
{g_1,\ldots,g_r}
\subseteq\mathcal G_q(\Lambda').
]

These conditions are necessary and sufficient under the frozen cell grammar.

When source vertices are retained, the question reduces to preservation of the generators.

Geometric survival is different:

[
P(c)\subseteq U(x').
]

It must be evaluated independently.

4. Mandatory primary specimen: P2-A
4.1 Exact FIELD-I transition
Take

[
\boxed{
x_0=\frac{21^8}{5}
\quad\longrightarrow\quad
x_1=\frac{21^8}{4}.
}
]

The arithmetic uses

[
L(x_0)=21^4,
\qquad
G(x_0)=20.
]

Therefore
\frac{21^8}{5}+\frac{21^8}{20}
\frac{21^8}{4}.
]

Both numerators are (3^8 7^8), so both exponent boxes equal

[
q=(4,4).
]

The source and target relation lattices are

[
\Lambda_5=
{(a,b)\in\mathbb Z^2\equiv0\pmod4}
]

and

[
\Lambda_4=
{(a,b)\in\mathbb Z^2+b\equiv0\pmod2}.
]

Thus

[
\Lambda_5\subsetneq\Lambda_4
\subsetneq\mathbb Z^2.
]

Neither lattice is trivial.
4.2 Initial exact observations
Preliminary exact enumeration gives:
Property	Source	Target
Reduced denominator	5	4
Active prime axes	2	2
Exponent box	((4,4))	((4,4))
Occurrence vertices	6	12
Region Graver vectors	12	8
Graver edges	11	29
Old edges retained	—	3
Old edges lost	—	8These are preflight calculations and must be independently reproduced in the E2-P2 package.

The eight lost source edges are:

[
\begin{aligned}
&(0,4)-(1,1),\quad (0,4)-(2,2),\
&(0,4)-(3,3),\quad (0,4)-(4,4),\
&(1,1)-(4,0),\quad (2,2)-(4,0),\
&(3,3)-(4,0),\quad (4,0)-(4,4).
\end{aligned}
]

The three retained source edges are the consecutive diagonal edges joining

[
(1,1),(2,2),(3,3),(4,4).
]

This is the experiment's first strict test: Graver-edge destruction can occur even when both relation lattices remain nontrivial and the prime-coordinate box is unchanged.
4.3 Geometric control
The planar GEO-I stabilization results are applicable to this specimen under their corresponding lattice normalization and box hypotheses.

Consequently, the geometric-union comparison must be crosschecked against those inherited results, not presented as independent discovery.

The particularly useful contrast is that abstract edges can be lost even when geometric containment is preserved.

5. Infinite arithmetic family: P2-F21
Extend P2-A to

[
\boxed{
x_h=\frac{21^{2h}}5
\longrightarrow
x_h'=\frac{21^{2h}}4,
\qquad h\ge1.
}
]
Initial mathematical facts
For every (h\ge1),

[
L(x_h)=21^h,
\qquad
G(x_h)=20.
]

The source eligible indices have exponent coordinates

[
a-b\equiv0\pmod4,
\qquad 0\le a,b\le h,
]

excluding the origin.

For the target,

[
a+b\equiv0\pmod2,
\qquad 0\le a,b\le h.
]

The relation lattices are independent of (h), while the box expands.

The transition follows directly from FIELD-I:
\frac{21^{2h}}5+\frac{21^{2h}}{20}
\frac{21^{2h}}4.
]

These formulas provide an exact infinite parameter family. They are not, by themselves, a novel geometric theorem.
5.1 Theorem candidate P2-TF1
For (h\ge4), characterize exactly which Graver edges of the source fibre survive in the target fibre.

The preliminary result suggests that the only common Graver directions are

[
\pm(1,1).
]

The theorem must establish this from the complete Graver bases and then derive a general survival or loss formula as a function of (h).

The minimum acceptable extension is a rigorous result covering all (h\ge4), not a finite enumeration of selected depths.
5.2 Further questions
Determine:
- The exact counts of surviving and destroyed source edges.
- Whether higher-dimensional cells have analogous arithmetic classifications in appropriate extensions.
- How the geometric unions compare for each (h).
- Whether embedding and topology exhibit thresholds.
- Whether the resulting criteria are instances of known planar stabilization or genuinely additional transport laws.
The distinction between inherited planar geometry and new FIELD-I transport conclusions must be explicit.

6. Secondary specimen: P2-B
Use the exact transition

[
\boxed{
\frac{55^{12}}{27}
\longrightarrow
\frac{55^{12}}{18}.
}
]

Here the active primes are (5,11), and

[
q=(6,6).
]

The source and target character relations reduce to

[
\Lambda_{27}=
{(a,b)\equiv0\pmod{18}}
]

and

[
\Lambda_{18}=
{(a,b)\equiv0\pmod6}.
]

Both are nontrivial, with strict lattice enlargement.

The source has six occurrence vertices and five Graver edges. The target has eight vertices and 17 Graver edges. The five old edges survive.

This specimen is deliberately different from P2-A: it exhibits lattice enlargement without destruction of the source edge skeleton.

It must be independently verified and then used as a negative control against any overly broad claim that strict lattice enlargement necessarily destroys old edges.

7. Theorem programme
P2-T1 — Exact lattice-transport criterion
For a common prime-coordinate system, determine when

[
\Lambda_b\subseteq\Lambda_{b'}.
]

A fundamental equivalence to establish and implement is:

[
\boxed{
\ker\chi_b\subseteq\ker\chi_{b'}
}
]

if and only if the generator assignment

[
p_i\bmod b\longmapsto p_i\bmod b'
]

defines a well-defined homomorphism between the subgroups generated by the indicated prime residues.

Prove the equivalence and implement an exact decision procedure using the corresponding lattice or finite-group relations.

This is inherited elementary algebra in substance; its role is to provide a verified transport foundation.

Mandatory test: P2-A has denominators 5 and 4. The second denominator does not divide the first, yet the kernels are ordered.

Thus the implementation must not use denominator divisibility as a necessary condition.
P2-T2 — Arithmetic Graver-survival criterion
Given (\Lambda\subseteq\Lambda'), determine which source Graver vectors remain conformally minimal in (\Lambda').

A source vector (g) fails to survive when a nonzero proper conformal subvector becomes available in the larger lattice.

The task is to express this condition as an effective arithmetic criterion in terms of modular relations.

The algorithm should inspect a bounded arithmetic region associated with (g), rather than constructing all target cells.

Required output: A complete surviving-generator set and exact certificate for every tested transition.
P2-T3 — Abstract-cell transport theorem
Build upon P2-T2 and the inherited E2-P1 cell-survival condition.

The principal objective is a theorem predicting the survival of all source cells from their generators and the relevant arithmetic relation data.

Avoid presenting the already known corner-and-generator criterion as a new theorem.

The new contribution must lie in deriving or simplifying the arithmetic conditions governing the generator changes.
P2-T4 — Geometric containment and obstruction
Determine when

[
U(x)\subseteq U(x').
]

Distinguish:
1. Complete geometric retention.
2. Partial geometric retention.
3. Incomparable geometric unions.
4. Equality of unions despite different cell structures.
Investigate whether a finite family of arithmetic obstruction templates can characterize containment failure for a declared class.

Compare explicitly with GEO-I v004's finite obstruction-template framework and GEO-I v012's planar coverage theorem.

A restatement of those theorems is insufficient.
P2-T5 — Relation-lattice transport in higher dimensions
Investigate whether the two-coordinate transport criteria extend to (k\ge3).

The primary target is a genuinely coupled three-coordinate modular relation, not merely a planar specimen with an independent additional axis.

Seek one of:
- A higher-dimensional general theorem.
- A certified counterexample to a proposed planar extension.
- A proved obstruction that depends essentially on three-coordinate coupling.
A product extension that introduces no new coupled behavior is retained only as a regression control.
P2-T6 — Geometric prediction and complexity
Develop a procedure that accepts arithmetic data for (x\to C(x)) and predicts specified aspects of source-cell survival without enumerating every target cell.

Compare against direct reconstruction using the frozen geometry engine.

Record exact correctness and computational cost separately.

The predictive criterion must have clearly stated input assumptions and output guarantees.

8. Exact experiments
E2-P2/A — Source compatibility and arithmetic preflight
- Verify the complete E2-P1 source and the two precision corrections.
- Reproduce P2-A and P2-B using the frozen fibre/Graver definitions.
- Verify both FIELD-I transitions directly from (D,L,G,C).
- Verify equality of prime-coordinate sets and exponent boxes.
- Confirm full lattice inclusion using independent exact methods.
Gate: ARITH_PASS
E2-P2/B — Graver and abstract-cell transport
- Enumerate source and target Graver bases.
- Compute preserved and lost generators.
- Enumerate cells in all available dimensions.
- Compare the generator-based predictions with direct target-cell construction.
- Include negative controls with complete edge retention.
Gate: CELL_PASS
E2-P2/C — Geometric transport
- Construct exact maximal-cell unions.
- Test containment in both directions.
- Produce exact witnesses for uncovered regions.
- Compare abstract and realized topology wherever computation is certified.
- Verify inherited planar cases against GEO-I results.
Gate: GEOMETRY_PASS
E2-P2/D — Generalization and counterexample search
Search deterministic parameter families, beginning with P2-F21.

Extend to additional pairs of primes, modular orders and selected three-prime systems.

Record both successful predictions and counterexamples.

Classify all encountered lattice relations as EQUAL, ENLARGE, SHRINK or INCOMPARABLE.

Do not silently omit cases where the source fibre fails to generate its full relation lattice.

Gate: GENERALIZATION_CHECKED
E2-P2/E — Proof and novelty audit
For every surviving theorem candidate:
- State exact hypotheses.
- Provide a complete proof or an exact counterexample.
- Compare against GEO-I and prior mathematics.
- Record whether the result is inherited, elementary, new within the model, or unresolved.
- Independently verify the supporting computational certificates.
Gate: THEOREM_PASS, COUNTEREXAMPLE or OPEN, as justified.

9. Preregistered falsification tests
ID	Proposition to test	Falsification condition
P2-F1	Strict lattice enlargement necessarily destroys existing Graver edges	Find a proper enlargement preserving every existing edge; P2-B is a candidate control
P2-F2	Occurrence-fibre inclusion implies full lattice inclusion	Find a transition whose finite fibre is included but whose full lattices are not ordered
P2-F3	Denominator divisibility is necessary for lattice inclusion	P2-A already supplies a candidate counterexample
P2-F4	Abstract edge loss implies geometric segment loss	P2-A and E2-P1 provide controls
P2-F5	Planar transport classification automatically extends to genuine three-coordinate coupling	Produce an exact higher-dimensional violation
P2-F6	Lattice-order data alone uniquely determine geometric transport	Exhibit two transitions with the same lattice-order class but different cell-survival behaviorSome tests already have evident counterexample candidates. Their purpose is to prevent false universal conclusions and to delimit useful theorem hypotheses.

10. Required deliverables
Package name:

GEO_HD_E2_P2_v001.zip

Recommended structure:
GEO_HD_E2_P2_v001/
│
├── README.md
├── MANIFEST.json
├── STATUS.json
│
├── SPEC/
│   └── E2_P2_SPEC_v001.md
│
├── theory/
│   ├── DEFINITIONS.md
│   ├── THEOREMS.md
│   ├── PROOF_OBLIGATIONS.md
│   └── SOURCE_OVERLAP.md
│
├── src/
│   ├── build_p2.py
│   ├── lattice_transport.py
│   ├── graver_transport.py
│   ├── cell_transport.py
│   ├── geometry_audit.py
│   └── make_figures.py
│
├── tests/
│   ├── test_arithmetic.py
│   ├── test_graver.py
│   ├── test_transport.py
│   └── test_negative_cases.py
│
├── data/
│   ├── P2_A.json
│   ├── P2_B.json
│   ├── P2_F21.json
│   └── SEARCH_CORPUS.json
│
├── results/
│   ├── P2_REPORT.md
│   ├── P2_LATTICE_ORDER.json
│   ├── P2_CELL_SURVIVAL.json
│   ├── P2_GEOMETRY.json
│   ├── P2_CERTIFICATES.json
│   ├── P2_COUNTEREXAMPLES.json
│   └── P2_THEOREM_AUDIT.md
│
├── figures/
│   ├── lattice_transport.png
│   ├── edge_survival.png
│   └── geometric_containment.png
│
├── RUN_WINDOWS.bat
└── RUN_VERIFY.py
All files are additions to the active GEO-HD project.

E2-P1, HD-0 and the source archives remain unchanged.
10.1 Report requirements
P2_REPORT.md must contain:
1. Exact source and target FIELD-I arithmetic.
2. Relation-lattice classification.
3. Graver-generator changes.
4. Cell-survival results.
5. Geometric-union comparison.
6. Exact counterexamples.
7. General theorem statements and proofs.
8. Explicit comparison with GEO-I and known mathematics.
9. Reproducibility evidence.
10. Scientific conclusions and unresolved obligations.
The figures must derive from the certified geometry records. No geometric conclusion may depend on visual inspection alone.

11. Acceptance criteria
Exact-computation gate
EXACT_PASS requires:
- Correct arithmetic and reduced rational values.
- Correct occurrence fibres.
- Complete region Graver enumeration.
- Exhaustive source/target cell comparison for declared specimens.
- Exact geometric-containment certificates.
- Independent replay of the key results.
- Tamper-rejection tests.
- No undisclosed unavailable computations.
Scoped theorem gate
THEOREM_PASS (SCOPED) requires at least one proved general result applying beyond the individually enumerated specimens.

A valid example would be a complete edge-survival classification for the infinite P2-F21 family.

However, such a theorem may remain elementary and must be assessed for novelty separately.
Main scientific gate
C3_CANDIDATE requires a genuinely additional general structural result connecting arithmetic lattice transport with geometric behavior beyond inherited GEO-I and standard Graver facts.

Possible qualifying results include:
- A new nontrivial arithmetic criterion for geometric containment.
- A finite transport-obstruction classification for a meaningful family.
- A higher-dimensional theorem identifying an essential coupling obstruction.
- An effective prediction theorem that avoids full target reconstruction.
The governing GEO-HD-1 criterion C3 is not automatically satisfied by proving the basic lattice-order or cell-membership identities.
Negative research verdict
COUNTEREXAMPLE is appropriate when a conjectured transport law fails and an exact witness is certified.

OPEN is appropriate when the computation is complete but no qualifying general theorem has been established.

A negative result must not be relabelled as theorem success simply because all computational tests pass.

12. Preservation and execution rules
1. Preserve the complete E2-P1 package and its verification records.
2. Record the two E2-P1 precision corrections as separate addenda.
3. Reuse GEO-I source-defined cell grammar and certified methods.
4. Work only in the active GEO-HD project.
5. Use exact integers and rationals for proof-relevant computations.
6. Preserve failed predictions and counterexamples.
7. Mark interrupted or unaffordable computations UNAVAILABLE.
8. Keep GitHub strictly read-only.
9. Do not prepare a new manuscript before the general theorem and novelty audit.
10. Do not promote an elementary algebraic reformulation into an independent discovery without justification.

13. Immediate executable task
E2-P2/A — Nontrivial-Lattice Transport Preflight

Begin with

[
\frac{21^8}{5}\longrightarrow\frac{21^8}{4}.
]

Independently verify the FIELD-I transition, compute both relation lattices and Graver bases, and reproduce the preliminary six-to-twelve vertex and eleven-to-twenty-nine edge counts.

Then verify

[
\frac{55^{12}}{27}\longrightarrow\frac{55^{12}}{18}
]

as an example of strict lattice enlargement with complete preservation of the old edge skeleton.

Once both pass, proceed to the infinite P2-F21 family and derive the general arithmetic edge-survival criterion.

The first mathematical obligation is to distinguish which generator changes follow purely from lattice order and which depend on the particular arithmetic realization and exponent box.

14. Scientific question to be answered
The E2-P2 final report must answer:
When FIELD-I changes the modular relations among existing occurrence coordinates, can we determine in advance which parts of the UNNS geometric organization survive, which disappear, and which new relationships become admissible?

The result must be expressed as precise mathematics, supported by exact reproducible experiments, and assessed against the established GEO-I theory.

END — GEO-HD-1B / E2-P2 Specification v001