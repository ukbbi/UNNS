# THEOREM CROSSWALK — GIG Comprehensive Manuscript v001
Authorship: UNNS Research Collective. Written BEFORE the chapters; every theorem, number and construction in the manuscript must appear here.
Sources are the frozen releases (read-only copies in the build workspace): `G1`..`G7` = GIG-I v001..v007; `G5a`,`G5b`,`G5c` = GIG-I v005 stage 1/S2/S3 (folders `GIG_I_v005`, `GIG_I_v005_S2`, `GIG_I_v005_S3`); `I1`..`I6` = GIG-INFO v001..v006; `FH` = `forbidden_histories_manuscript_v1` (frozen 9-page paper).
Release-level proof text: `<release>/THEORY/PROOFS.md`; register: `<release>/THEORY/THEOREMS.md`.
**Repository pin.** v001-era file. In v002 the GIG collection is cited at commit a115e4bc6b8ee734e6146b3b17a6b121e65d31c3 (as supplied by the author; not independently retrievable from the build environment).
Status vocabulary used in the manuscript: ANALYTIC (complete human-checkable proof), COMPUTER-ASSISTED (proof reduces to a stated finite check; certificate named), FINITE-EXACT (exact computation on a stated finite domain, no generalisation), BOUNDED (observed on a sampled/searched domain), CONJECTURAL/OPEN, FALSIFIED. `M:` marks results re-derived by the manuscript's own verifier (`verify/`), independent of the frozen engines.

## Part I — Foundations
| Manuscript label | Content | Source (release/ID) | Status | Proof / evidence |
|---|---|---|---|---|
| def:grammar, def:history, def:swap | abstract grammar, histories, fibre, legal swap, swap graph | G1 DEFINITIONS §1-4 (generalised) | definition | — |
| prop:reverse-edge | reverse-edge law: edge m→t with label N iff (N+1)²\|t | G1 T1(1) | ANALYTIC | G1 PROOFS §1 |
| prop:fibre-finite | strict growth ≥4, histories of bounded length, finite fibres, count of reverse edges τ(s(t))−1, nonemptiness of complete fibres | G1 T1(2)-(5) | ANALYTIC | G1 PROOFS §1 |
| thm:hierarchy | T⊂(M,Q)⊂C⊂W; chain-rule decomposition | G1 T2 | ANALYTIC | G1 PROOFS §2 |
| prop:entropy-bounds | 0≤H(W\|T)≤A(t); all values attained | G1 T3 | ANALYTIC | G1 PROOFS §3 |
| ex:72 | the four histories of 72 and the exact decomposition (2 = 1.5+0.5) | G1 T4 | FINITE-EXACT; M: | G1 PROOFS §4; verify/ch03 |
| prop:72r | A(72^r) ≥ log2 C(2r,r); exact counts r=1..10 | G1 T5 | ANALYTIC (bound), FINITE-EXACT (counts); M: r≤6 | G1 PROOFS §5 |
| prop:class-entropy | H(C\|T=t) ≤ log2 β0; equality iff equal sizes | G1 T6 | ANALYTIC | G1 PROOFS §6 |
| conv:prob | probability conventions: uniform on fibre, natural vs balanced ensembles, Hartley vs Shannon | G1 DEF §3; I4 §B | convention | — |

## Part II — Arithmetic admissibility
| lem:F | Lemma F: admissible ⇔ D(I)\|m for every prefix set | G3 Lemma F | ANALYTIC | G3 PROOFS; M: simulation vs law on 720 perms × 5 sources |
| prop:valuation | v_p(D(I)) = max(0, Σ(v_p(ℓ)−2v_p(ℓ+1))) | G5 PS-6 | ANALYTIC | G5 PROOFS |
| prop:finite-lattice | A(m) depends only on min(v_p(m),cap_p): finite lattice of systems | I1 GI-0 | ANALYTIC | I1 THEOREMS (one-line proof) |
| thm:cube | cubical factorization Adm∩Q_d = G×E_1×…×E_d; no six-vertex slice | G2 T11 | ANALYTIC | G2 PROOFS |
| thm:closure | threshold closure; minimal source L(S); closure operator; ∩ = gcd; squarefree | G2 T12 + G3 CORRECTIONS (∅ convention) | ANALYTIC | G2 PROOFS; G3 V002_T12_SCOPE |
| thm:block | ordered-block factorization V(F)∩A=E_1×…×E_r | G3 T16 | ANALYTIC | G3 PROOFS |
| thm:face-threshold | K_F=lcm D(Pref(F)); F∈X(m) ⇔ K_F\|m | G3 T17 | ANALYTIC | G3 PROOFS |
| thm:filtration | divisibility filtration monotone; Δβ_j = Δf_j−Δρ_j−Δρ_{j+1} | G3 T18 | ANALYTIC | G3 PROOFS |
| thm:swap-reconstruction | complex from coloured swap graph (any A⊂S_k) | G2 T13 | ANALYTIC | G2 PROOFS |
| prop:iso-profiles | graph isomorphism ⇒ equal accessibility profiles | G2 T14 | ANALYTIC | G2 PROOFS |
| thm:skeleton | 2-skeleton from the uncoloured graph under CP, k≤8 | G2 T15 | ANALYTIC modulo the 6-cycle classification (FINITE-EXACT, k≤8) | G2 PROOFS |
| prop:petrie | Petrie vs braid hexagon: negative control (graph alone fails without CP) | G2 T13 sharpness, G3 T20e | FINITE-EXACT | G2 cert Z1 |
| thm:third-boundary | β2(X)−β2(Y)=ρ3(Y)−ρ3(X) for graph-isomorphic realizable X,Y (k≤8) | G3 T19 | ANALYTIC (given T15) | G3 PROOFS |
| thm:face-recognition | T20a completeness (ANALYTIC); T20b soundness for P_k-convex sets k≤7 (COMPUTER-ASSISTED); T20c domains FINITE-EXACT; T20d OPEN | G3 T20a-d | as stated | G3 PROOFS, E12 |
| prop:H2-depends-low | β2 depends on faces of dim ≤3; covers without new 2-faces cannot raise β2 | G3 T21a | ANALYTIC | G3 PROOFS |
| thm:anchor | anchor obstruction: z (96 faces), φ (6 hexagons); six obstructed truncated octahedra; non-bounding iff 288\|m, gcd(m/288,30)=1; B: 432, gcd(m/432,42)=1 | G3 T21b | ANALYTIC (non-bounding), FINITE-EXACT (fillings, β2≡0 elsewhere); M: β2 recomputed for the anchor A sources | G3 PROOFS; CERT H2_anchor_{A,B}.json |
| thm:hole-survival | parametric hole survival (PS-1) for arbitrary six labels; PS-0 finite check; PS-4 existence | G4 PS-0,1,4 | ANALYTIC modulo PS-0 (COMPUTER-ASSISTED: 540 3-faces) | G4 PROOFS; CERT pattern_H2.json |
| prop:gate0 | gate-0 filling (34 faces) | G4 PS-2 | COMPUTER-ASSISTED | G4 PROOFS |
| thm:exact-survival | exact survival criterion: 4 minimal families B0..B3 over 2^20 families | G5 PS-5 | FINITE-EXACT | G5 PROOFS, E19 |
| prop:gate-nec | gate 1/3 not necessary (refutes v004 P1); explicit CRT counterexamples | G5 PS-3′, PS-6 | FINITE-EXACT | G5 CERT gate{1,3}_counterexample.json |
| thm:AT1 | survival law for a given cycle (dualised minimal filling families); AT-2 existence criterion | G5b AT-1, AT-2 | FINITE-EXACT / ANALYTIC (AT-2) | G5b PROOFS |
| obs:census-H2 | six-label census: 8,008 contents, 346,859 regimes, 158 positive (β2=3 once); 52 explained by PS-1; EX-2 soundness | G4 EX-1, EX-2; I2 GI2-1 | FINITE-EXACT | G4 RESULTS; I2 |

## Part III — Higher-dimensional topology
| obs:atlas | atlas: 160 basis cycles → 70 canonical → 23 → 32 law classes; coverage; held-out prediction (0 false positives) | G5b AT-3, AT-4 | FINITE-EXACT (listed cycles); BOUNDED (prediction) | G5b RESULTS, E22–E26 |
| def:lift | lift operator Λ, first, last, two-sided suspension | G5c definitions | definition | — |
| lem:LT0 | ∂Λ(f)=Λ(∂f)+first(f)+last(f) | G5c LT-0 | ANALYTIC | G5c PROOFS |
| thm:lift-cycle | lift is a cycle (LT-1); diagonal lift bounds (LT-2); L=∂Λ(c1)+last(c1+c2) | G5c LT-1, LT-2 | ANALYTIC | G5c PROOFS |
| thm:cochain-lift | cochain lift pairing φ3(L)=φ2(z); six obstructed 4-faces | G5c LT-3 | ANALYTIC (pairing), COMPUTER-ASSISTED (obstruction set over 1,806 4-faces of P_7) | G5c PROOFS |
| prop:H3-examples | four β3=1 regimes (k=7) reproduced as lifts; 16 lifts of the Stage-1 cycle; minimal families by pair | G4 H3-C/E, G5c LT-4, LT-5 | FINITE-EXACT | G5c CERT lift_pairs.json |
| obs:nondeg | non-degeneracy of 554 off-diagonal pairs (32 classes) | G5c LT-6, G6 ND-1 | FINITE-EXACT; general proof OPEN | — |
| obs:AS1 | 1,560,780 seven-label contents (labels 2..30): 202 admit a lifted hole; 214 regimes verified; β3 ∈{1,2,3,4} | G5c AS-1 | BOUNDED | G5c RESULTS E30 |
| thm:filling-dependence | FI-1..FI-4 (ANALYTIC); FI-5, FI-6 certified filling dependence; criterion FI-2 sharp | G6 FI-1..FI-6 | ANALYTIC / FINITE-EXACT | G6 PROOFS |
| thm:iterated-lift | HL-1 (ANALYTIC), HL-2 (FINITE-EXACT), HL-3 certified arithmetic H4 example (content (2,3,4,5,8,9,15,20), m=86400) | G6 HL-1..HL-3 | as stated | G6 CERT h4_certificate_first_hit.json |
| obs:rolemap | role-map correction RM-1 | G6 RM-1 | FINITE-EXACT | G6 E36 |
| thm:JX | facet theorem (J-1), retraction criterion (J-2) — ANALYTIC; J-3..J-5 FINITE-EXACT; J-6 conditional; J-7 OPEN | G7 | as stated | G7 PROOFS |

## Part IV — Information recovery
| prop:profile | recombination information profile I_r: monotone, strict until ρ, = H(W\|C,T) iff r≥ρ; additivity; first-step cycle law | G1 T7 | ANALYTIC | G1 PROOFS §7 |
| thm:radius2 | radius-2 identity \|B2\|=1+d+s−q; fine radius ≤2 data determine (N,E,Q) | G1 T8; I3 T1 | ANALYTIC | G1 PROOFS §8; I3 T1 proof; M: checked on random subsets |
| cor:moments | SB2 = N+Sd2−4Q; second-order sums (C1–C4) | I3 C1–C4 | ANALYTIC | I3 |
| prop:witnesses | information-equivalent, topologically inequivalent pieces W1–W6; separating radii | G1 T9 | FINITE-EXACT, COMPUTER-ASSISTED | G1 cert; M: W1,W2,W5 re-derived |
| prop:complete-loop | complete-history fibre of 1,382,400 contains a β1=1 piece (210) | G1 T10 | FINITE-EXACT | G1 E4 |
| obs:anchor-recovery | two anchor experiments: survival entropy, recovery profile H(Y\|O_i)=0, history count injective on comparable window, arrow law | I1 GI-1..GI-8 | FINITE-EXACT | I1 CERT |
| obs:equal-N | census: H(Y\|N)>0; exact residual-entropy table; ball-2 restores zero | I2 GI2-1..GI2-6 | FINITE-EXACT | I2 RESULTS E11 |
| thm:hierarchy-obs | observation hierarchy monotone | I2 GI2-4 | ANALYTIC | I2 |
| obs:S2 | smallest separating pairs; Ss2 as empirical separator; sharp witness (2520,3780) | I3 R1–R3 | FINITE-EXACT | I3 |
| obs:preregistered | pre-registered held-out test: S_B,S_C confirmed; S_A falsified | I3 R5 | BOUNDED; FALSIFIED (S_A) | I3 PREREGISTRATION |
| obs:S2-falsified | (Q,S2) sufficiency falsified for prefix-family systems; certified counterexample | I4 R-A1 | FINITE-EXACT; FALSIFIED as general principle | I4 CERT |
| obs:oos | plug-in vs out-of-sample information | I4 R-B1, R-B2 | BOUNDED | I4 |

## Part V — Forbidden histories
| thm:AD | Alexander duality for history complexes | I4 T-AD | ANALYTIC (classical inputs) | I4 THEOREMS (proof); FH |
| lem:star | star-intersection lemma L1 | I5 L1 | ANALYTIC | I5 |
| thm:nerve | T-NERVE, C1 dead-set nerve theorem; β2=dim H1(N[D]) | I5 T-NERVE, C1; I6 Result I | ANALYTIC | I5, I6 |
| prop:prefix-def | arithmetic admissibility is prefix-defined (P1) | I5 P1 | ANALYTIC | I5 |
| prop:cocycle | cycle/cocycle sufficient criterion; 290/290 positive certificates | I5 C2 | ANALYTIC (criterion), FINITE-EXACT (certificates); M: 158 census positives re-certified by verify/ | I6 CERT positives_cycle_cocycle.json |
| obs:motifs | hollow triangles (288/290), complementary squares (2/290); negatives: 707/1000 hollow, 0 non-bounding; no cone-point criterion | I5 R-A1, R-A2 | FINITE-EXACT | I5 |
| obs:sharp-pairs | pairs (480,800) at (2,3,4,5,8,15); (2520,3780) at (2,4,5,9,14,15) | I5 R-A3 | FINITE-EXACT | I5 |
| obs:collapse | exhaustive dead-set pattern analysis: 338,851 regimes, 219,145 patterns, 151 positive patterns; strong-collapse cores; observation table | I6 D21 | FINITE-EXACT | I6 RESULTS |
| lem:Zp | description of Z_S by block-index differences; nonemptiness iff S not strongly connected | I5 L2 | ANALYTIC (+FINITE-EXACT check) | I5 |
| thm:pairwise | T-ADJ pairwise-adjacency theorem (k=6) | I5 T-ADJ; I6 Result II | COMPUTER-ASSISTED (30/435/4060 finite lemmas; M: re-verified independently) | I6 standalone_verify [ADJ]; verify/ch14 |
| prop:triple | sharpness: forbidden triples (1,2,0),(5,4,3) give β=(1,2,5,0,0,0), N=674 | I5 S-3 | FINITE-EXACT; M: reproduced | I5 CERT |
| obs:sym-sweeps | symbolic sweeps: 512 rule sets; 28 multisets; SYM-6 60,000 + 600,000 draws: β2=0 in all (now explained by T-ADJ for pairwise) | I4 R-C1, R-C2; I5 §2 | FINITE-EXACT / BOUNDED | I4 |

## Part VI — Synthesis / conventions
| status taxonomy, NOT_RERUN policy | ways-of-working | all | — | — |
| parent provenance | v005 manifest erratum (V004 path); 11/14 parent manifests match | I6 ERRATUM_v005 | disclosure | — |

## Explicit gaps carried into the manuscript (stated, not repaired)
1. No release file proves T20d, T21c, PS-3 (as a universal statement; it is false in its strong form, PS-3′), LT-6 for all cycles, J-7, or GI-8 (history-count injectivity).
2. T15's 6-cycle classification is verified for k≤8 by enumeration; no uniform proof exists in the sources.
3. T-ADJ's three finite lemmas and T20b's soundness are computer-assisted; the manuscript re-checks the T-ADJ lemmas with an independent implementation (verify/ch14) and records the others as NOT_RERUN.
4. "Prior-art review has not been performed" (I6); this manuscript supplies PRIOR_ART.md, with search-verified references only.
5. Inherited expensive computations (6-label censuses, k=7 scans, HL-3 search) are recorded NOT_RERUN; their certificates are named, not re-derived.
