# GIG-INFO v002 — theorem and result register
Tags: [PROVED] proof in this register; [FINITE-EXACT] exhaustive exact computation on the stated finite domain; [BOUNDED] holds on the domain searched, no claim beyond it; [OPEN].

Domain D = the six-label census of GIG-I v004: 8,008 contents (6 distinct labels in 1..16), 346,859 source regimes (distinct non-empty admissibility sets). System X = (content, regime); N(X) = number of admissible histories; Y(X)=1 iff β₂(K_X; GF(2))>0.

**GI2-1 [FINITE-EXACT] Census reproduction.** The recomputation of every Betti vector with the v001 engine gives 158 regimes with β₂>0 (157 with β₂=1, one with β₂=3), identical as a set to the frozen v004 list; N ranges over 1..720.

**GI2-2 [FINITE-EXACT] The history count does not determine Y on D.** The 158 positive regimes take 59 distinct N values; 326,912 (positive, negative) pairs have equal N; 72 of these lie in the same content (51 positives have a same-content partner). Every one of the 158 positives has at least one equal-N negative. Hence H(Y|N)>0 under each ensemble below.

**GI2-3 [FINITE-EXACT] Exact residual entropy** (bits, uniform ensembles; full 30-digit values in RESULTS/E11):
| ensemble | size | H(Y) | H(Y|N) | H(Y|N,f₁) | H(Y|N,χ) | H(Y|N,h₁) | H(Y|f-vector) | H(Y|N,h₂) | H(Y|N,h₁,h₂) |
|---|---|---|---|---|---|---|---|---|---|
| E_all | 346,859 | 0.005713 | 0.004467 | 0.002172 | 0.000109 | 0.000619 | 0 | 0 | 0 |
| E_band | 93,018 | 0.018078 | 0.016659 | 0.008100 | 0.000406 | 0.002309 | 0 | 0 | 0 |
| E_distinct | 219,146 | 0.008231 | 0.006276 | 0.003140 | 0.000168 | 0.000803 | 0 | 0 | 0 |
E_band = regimes whose N is attained by a positive regime. E_distinct = one system per distinct labelled arrangement set.

**GI2-4 [PROVED] Observation hierarchy is monotone.** O1=(N,h₁,h₂) is a function of the isomorphism class of the swap graph (ball sizes are graph invariants), hence of O2; O2 is a function of the labelled arrangement set O3; Y is a function of O3. Therefore H(Y|O3)=0 always and H(Y|O2) ≤ H(Y|O1).

**GI2-5 [FINITE-EXACT] Persistence under enrichment.** On D, O1 has zero residual entropy in all three ensembles (8,208 classes in E_all, none mixed); so H(Y|O1)=H(Y|O2)=H(Y|O3)=0 (GI2-4). The separation H(Y|N)>0 therefore does NOT persist once ball-2 accessibility is added. Partial observables: (N,h₂) and the full f-vector already give 0; (N,h₁), (N,f₁), (N,χ) leave residual entropy (66, 151, 8 positives still share their signature with a negative).

**GI2-6 [FINITE-EXACT] Representative certified pair.** Content (2,3,4,5,8,15): sources 480 and 800 both give N=396 (direct divisibility simulation), but f-vectors (396,900,669,173,10,0) vs (396,882,636,156,7,0), β=(1,0,1,0,0,0) vs (1,0,0,0,0,0). Positive: an explicit 2-cycle and 2-cocycle with φ(z)=1 verified from the definition (pair_cert.verify). Negative: β₂=0 from two independent GF(2) rank routes and the v001 engine.

**Not claimed.** [BOUNDED] All statements are about D (≤16 labels, six distinct labels). No claim that f-vector or ball-2 data determine β₂ in general, other contents sizes, or repeated labels. The zero residuals are empirical facts of D, not theorems; their arithmetic origin is [OPEN].
