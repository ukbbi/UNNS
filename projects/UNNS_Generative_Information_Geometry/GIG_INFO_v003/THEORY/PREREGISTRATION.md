# GIG-INFO v003 — pre-registration of the held-out tests (written BEFORE any held-out system was generated)

Derived on the census D (labels <=16, six labels, 346,859 regimes): the signatures
  S_A = (N, SB22),  S_B = (sq, Ss2),  S_C = (Sd2, Ss2)
have zero mixed classes for Y = 1[beta2>0]; (N, h1, hq) does not.
Notation: d(w) degree, q(w) square incidence, s(w)=sum_{u~w}(d(u)-1), SB22 = sum_w |B2(w)|^2, Ss2 = sum_w s(w)^2, Sd2 = sum_w d(w)^2, sq = number of commuting squares.

H6 (held-out, six labels): 6000 contents sampled uniformly (random.Random(20261108)) from the six-subsets of {1..22} whose maximum label is in 17..22 (66,605 such subsets); ALL regimes of each content.
 P1: each of S_A, S_B, S_C has zero mixed classes inside H6, and zero mixed classes in the pooled set D u H6 (classes formed on exact signatures).  FALSIFIED by any mixed class.
 P2: the weaker signature (N, h1) has at least one positive regime in a mixed class in D u H6 (prediction that radius 1 stays insufficient).
H7 (exploratory, seven labels): 120 contents sampled (random.Random(20261109)) from the seven-subsets of {1..14}; ALL regimes. NO prediction of success is made: S_A, S_B, S_C, (N,h1), (N,h1,hq) are reported as found; a mixed class is a result, not an error.
Fixed before running: the census D and all features are those of RESULTS/features_all.npz (sha-256 recorded in MANIFEST).
