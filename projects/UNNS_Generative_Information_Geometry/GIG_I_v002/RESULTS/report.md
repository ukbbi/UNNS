# GIG-I v002 — Arithmetic Realizability and Graph–Topology Separation

Status tags: **[PROVED]** general proof · **[FINITE-EXACT]** exhaustive on the stated finite domain · **[BOUNDED-NEGATIVE]** exhaustive search found nothing · **[CAND]** conjecture.
Proofs: `THEORY/PROOFS.md`. Raw data: `results.json`, `search_coverage.json`. Certificates: `CERTIFICATES/`.

## Headline

1. **Arithmetic admissibility forbids a whole class of geometries.** Inside any commuting cube of the permutohedron the admissible vertices form a coordinate box (T11), so a six-vertex slice of a 3-cube — the Petrie hexagon, or a domino — can never be the admissible set of a SELECT-II source. [PROVED]
2. **Realizability is decidable by a closure test** (T12): `S` is realizable iff `cl_K(S)=S`, with `L(S)=lcm K(w)` the minimal source. [PROVED]
3. **The generator-coloured swap graph determines the whole permutohedral complex** (T13), for any arrangement set. [PROVED] The ordinary swap graph does not — for arbitrary sets the Petrie and braid hexagons have isomorphic graphs and different homology (certificate Z1) — but arithmetic realizability removes exactly that example.
4. **New theorem T15: under arithmetic admissibility, the uncoloured swap graph already determines the 2-skeleton**, hence f₂, β₀ and β₁ of every realizable piece (k≤8). So a graph-isomorphic pair with different homology could only differ in β_j, j≥2. [PROVED, using the 6-cycle classification, FINITE-EXACT for k≤8]
5. **No graph-isomorphic realizable pair with different homology exists in any searched domain** (k=6 with labels ≤10 and ≤12; k=5 ≤16; k=4 ≤40): Outcome B + C. This is a bounded negative result, **not** an impossibility theorem. GIG-Q3 stays open.

## 1. What arithmetic arrangement configurations are rigorously forbidden, and why?

**T11 [PROVED].** For a source m and a word with d disjoint adjacent pairs, each exchangeable independently, the exit state of a pair is x·R(a)R(b) in either order (T_aT_b=T_bT_a=xR(a)R(b) on ℚ), so the *formal* entry state of every later block is independent of earlier orientations. Admissibility then splits: Adm∩Q_d = G×E₁×…×E_d. Hence slice sizes are 0 or 2^j; for d=3 only 0,1,2,4,8.
Consequences: square closure (three corners of a commuting square ⇒ the fourth), the cube-product property (CP) for every realizable set, and **the Petrie-hexagon and domino six-vertex slices are impossible**. It does *not* forbid every hexagon: braid hexagons (genuine 2-faces) are realizable — 12 exactly-realizable braid hexagons occur in the L≤12 census.
**Finite-exact confirmation:** all 1,170 commuting cubes of dimension ≥2 of P₆ against all 26,802 realizable sets (contents ⊂ {1..12}): 31,358,340 pairs, 0 violations; 3-cube slice counts observed `{0:1,342,363, 1:15,904, 2:131,415, 4:421,803, 8:500,695}` and never 3, 5, 6, 7. The proof's formal-state recursion reproduces simulation on 4.3·10⁶ (source, cube) pairs. Every one of the 2,002,780 (realizable set, Petrie cycle) incidences with the six vertices present contained the whole cube.

## 2. Does threshold closure give a complete characterization of realizability?

**Yes (T12) [PROVED].** S=A_C(m) ⇔ cl_K(S)=S; L(S) is the unique divisibility-minimal (hence smallest) realizing source; cl_K is a closure operator and cl_K(S) is the smallest realizable superset; realizable sets are closed under intersection (A(m)∩A(m')=A(gcd)); S is realizable by a squarefree (complete-history) source iff L(S) is squarefree.
Independent checks [FINITE-EXACT]: 4,564 realizable sets over sampled contents (k=4,5,6) are closed with L(S) equal to the direct lcm of thresholds and no proper divisor of L(S) realizing S; the squarefree criterion matches brute force over all squarefree sources for 220 contents; 5,500 random subsets confirm extensive/monotone/idempotent and "smallest realizable superset"; 480 sets agree with direct forward simulation (including multiples of the minimal source).
A by-product: a per-prime level-mask construction enumerates *every* realizable set of a content (no lcm-closure cap), so all censuses below are exhaustive for their stated domains.

## 3. Six-cycle types in P₆ and which are arithmetically realizable

P₆ has 4,080 six-cycles in 14 translation classes [FINITE-EXACT]: **braid hexagon** 480 (4 classes, chordless 2-faces), **cube-Petrie** 360 (chordless, in a Q₃), **cube-domino** 1,080, **mixed-domino** 2,160 (both with one chord). No other type exists for any k≤8.
As *exact* arithmetic vertex sets (contents ⊂{1..10}, all sources): braid hexagons — 4 cycles realizable (5 content/source incidences); **Petrie, cube-domino and mixed-domino — never**. Cube types are excluded by T11; mixed-domino exclusion is an observation of the census (no theorem). In the L≤12 census the only 6-vertex realizable sets whose graph is a 6-cycle are 12 braid hexagons.

## 4. Does generator-coloured adjacency determine the inherited permutohedral complex?

**Yes (T13) [PROVED, no arithmetic hypothesis].** A face is a parabolic coset xW_J; it lies in K_A iff the J-coloured component of x in G_A has |W_J| vertices. So faces, incidence, boundary matrices and Betti numbers are functions of (G_A, colours); colour-preserving isomorphisms (up to the diagram reversal j↦k−j) induce isomorphisms of the complexes. Verified on all 6,914 k=6 realizable sets (L≤10): faces, boundary ranks and β reconstructed from the coloured graph alone match the inherited engine; β_j=f_j−rank∂_j−rank∂_{j+1} and the Euler identity hold for all.
**What the uncoloured graph forgets:** Z1 gives the Petrie and braid hexagons with isomorphic graphs (explicit bijection) and Betti (1,1,0,…) vs (1,0,…). Of the uncoloured isomorphism classes of realizable sets, 54 (k=6, L≤12; 148 for k=5) contain several coloured classes mod the Coxeter reversal — colours are genuinely not determined by the graph — yet their f-vectors and Betti vectors agree in every case.

## 5. Are there graph-isomorphic realizable pieces with different topology?

**Not in the searched domains [BOUNDED-NEGATIVE]; GIG-Q3 remains open.** Exact (individualisation–refinement, never hash-based) isomorphism classes of the uncoloured swap graphs of *all* realizable sets:

| domain (all k-subsets of {1..L}, all sources) | sets | exact iso tests | iso classes | classes with >1 Betti vector |
|---|---|---|---|---|
| k=4, L≤40 | 2,382 | 2,306 | 76 | **0** |
| k=5, L≤16 | 32,063 | 28,114 | 3,956 | **0** |
| k=6, L≤10 | 6,914 | 3,473 | 3,441 | **0** |
| k=6, L≤12 | 26,802 | 15,753 | 11,052 | **0** |

No closure caps, no skipped contents (`search_coverage.json`). Within every class the f-vector is also constant. Weisfeiler–Leman collisions do occur (one non-isomorphic pair sharing all invariants in each of k=5 and k=6, L≤12), which is why hashes are used only as filters.
**Why the negative is structural, not accidental (T15 [PROVED]).** In a realizable set squares are exactly the 4-cycles of the graph and braid hexagons exactly the chordless 6-cycles with no outside vertex adjacent to two of their vertices (Petrie cycles are recognised by the antipodal vertices that CP forces into A). So f₂, β₀, β₁ are graph invariants (verified for all 6,914 sets; 0 failures). A counterexample would have to differ in β₂ or higher.
Contrast, v001 witnesses W5/W6 and the closest approaches below are **non-isomorphic** (exact), consistent with T14: equal profiles through radius 2 cannot make graphs isomorphic.

## 6. What does k=6 establish about GIG-C1 and GIG-C2?

* **C1 (a radius-3 fine profile determines the Betti vector):** holds for the new domains. For k=6 (L≤10 and ≤12) the fine radius-**2** profile already determines the Betti vector (3 ambiguous groups at r=1, none at r=2); k=5 (L≤16) needs radius 3 (v001's value), k=4 (L≤40) radius 1. [FINITE-EXACT, not a theorem]
* **C2 (separating radius unbounded in k):** k=6 shows **no growth** (2 vs 3 at k=5) within L≤12. Because label bounds that suffice for a long-range hexagonal obstruction grow with k, this is weak evidence: C2 is neither supported nor refuted. Closest approaches (certificates K4L40, K5L16, K6L10/12): k=5 pair (2,3,8,9,14)@63 vs (6,8,9,14,15)@168 agree through radius 2; k=6 pair (1,3,6,7,8,9)@108 vs (3,6,7,8,9,10)@1080 agree through radius 1 (β₁ 0 vs 1).
* **Consequence of T14/T15:** graphs with different β₁ are never isomorphic, so for β₁ the all-radius graph-derived information is never blind in realizable pieces; blindness could only concern β_j, j≥2.

## 7. What remains recoverable from the graph, and what needs higher cells?

Recoverable from the (uncoloured) graph of a realizable piece: f₀, f₁, f₂, ∂₂, β₀, β₁ (T15). Needing more: in the k=6, L≤10 census the sub-vector (f₀,f₁,f₂) does **not** determine the Betti vector, while **(f₀,f₁,f₂,f₃) does** (63 f-subvectors tested; it is the unique minimal one) — the first information beyond the graph is the number of 3-cells. Only 2 sets in the census have β₂>0 (β=(1,0,1,0,0,0); N=372 and 276; contents (2,3,4,5,8,9)@288 and (2,3,6,7,8,9)@432); these are the natural place to look for a future separation. Unfilled cycles: among 80 class representatives with β₁>0 the shortest unfilled cycle is exactly 12 for 19 and none is shorter (61 have none ≤12). GIG-Q4 stays open; a smaller-than-homology signature candidate is (f₀..f₃) in this domain.

## Separation of results

* **General proofs:** T11, T12, T13, T14, T15 (T15 uses the 6-cycle classification, exhaustive for k≤8).
* **Exact finite results:** cube slices, closure checks, cycle census, certificates, coloured/uncoloured iso-class counts.
* **Unsuccessful bounded searches:** graph-isomorphic/homology-differing realizable pairs (domains above).
* **Conjectures:** that the graph determines the full face poset of every realizable complex; extension of the classification to all k; C2.

## Procedure and validation (secondary)

Tests: `python -m unittest discover -s TESTS` (v002 tests; the 28 v001 tests run unchanged as a subprocess, v001 file hashes checked). Frozen GEO-HD-1D v004 cross-check: see `crosscheck_frozen_v002.json` (or recorded as not run). Certificates are independently re-verified from contents+sources (forward simulation, two topology implementations, bijection check) — `verification_errors` is empty for all seven. Deterministic seed 20261105. Full run: 1,696 s, Python 3.13.
