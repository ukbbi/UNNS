# GIG-I v005 Stage 2 — theorems and status (Arithmetic H₂ Obstruction Atlas)

Notation. A(m) = {prefix sets I ⊆ ranks : D(I) | m} (rank bitmasks 1..63). For a 2-cycle z of P_6: P_z = ∪ Pref(F), F ∈ supp z. A *minimal filling family* of z is a minimal S ⊆ (63 sets) \ P_z such that z ∈ im ∂_3 using the 3-faces F of P_6 with Pref(F) ⊆ P_z ∪ S.

**AT-1 (survival law for a given cycle) [FINITE-EXACT, universal over contents].** For every six-label content and source m:
 z ⊂ X_λ(m) and [z] ≠ 0 in H_2(X_λ(m);F_2) ⇔ P_z ⊆ A(m) and no minimal filling family of z is contained in A(m).
 The families are computed exactly (E23: dualisation, i.e. minimal transversals of the complements of maximal non-bounding families; no enumeration cut-off). It reproduces the Stage 1 result for the distinguished 96-face cycle (4 families) — this is a regression test.

**AT-2 (existence criterion) [PROVED].** For any cycle z with families 𝔉(z): a source m with [z] ≠ 0 exists iff no F ∈ 𝔉(z) is contained in A(K_{P_z}), K_{P_z} = lcm_{I∈P_z} D(I). Proof: P_z ⊆ A(m) ⇔ K_{P_z} | m, and A is monotone under divisibility, so A(m) ⊇ A(K_{P_z}); survival at some m forces survival at K_{P_z}. (S₆ images: apply to each σ(z).)

**AT-3 (atlas, round 2) [FINITE-EXACT as a statement about the listed cycles; coverage BOUNDED].** 160 homology-basis cycles of the 158 census regimes (labels ≤ 16) fall into 70 canonical cycles, and these into **23 law classes** (canonical (P_z, 𝔉) under S₆); with the 9 classes added from held-out failures, **32 law classes**. Family counts: 24 classes have 4 minimal families, 7 have 6, 1 has 8; singleton families (single necessary gates) per class: 0 (8 classes), 1 (10), 2 (14).
 Coverage: all 158 census regimes, in particular all 106 not explained by the Stage-1/v004 PS-1 mechanism, are explained by at least one class (136 by several: overlap is large, a greedy cover needs 9 classes). The exact Stage 1 class (class 0) alone covers 59 regimes, i.e. 7 more than the 52 recorded in v004 (the exact criterion is weaker than "all gates closed"). 99 of the 106 are not covered by it.

**AT-4 (prediction test; BOUNDED, not a theorem).**
 Atlas v1 (23 classes) on 600 fresh contents (labels ≤ 40, 33,584 regimes): 193 regimes predicted, 0 false positives, 18 false negatives (β₂>0 not predicted). Atlas v2 (+ those 18): fresh set 2 (600 contents): v1 13 false negatives, v2 **0** of 171; fresh set 3 (1000 contents, 54,091 regimes): 289 predicted, **3 false negatives** (1%). No false positive ever occurred, as AT-1 requires. **The atlas is not closed**: new classes still appear at ~1% of hole regimes for larger labels.

**Not proved / not claimed.** (i) That 32 is the full list of classes, or that classes depend only on the cycle's homology class (they are relative to the chosen low-weight representatives; different representatives of one class can give different laws). (ii) Which families are *arithmetically* realisable, i.e. the Stage-1 style counterexamples to gate necessity for the new classes. (iii) A construction of the cycles or families independent of the finite census.
