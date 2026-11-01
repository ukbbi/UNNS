# E2-P4 v002 counterexamples (append-only; v001 counterexample file preserved).  Failed predictions are kept.

## CE-1  P4-C1 equality clause (v001) is false
Lambda = 2Z^3 < E_3, n = 4: conv F(Lambda) = H = U(E_3), but U(Lambda) = {max z_i >= 2} omits (1,1,1) (witness (4/7,4/7,10/7)).  Withdrawn; see the ERRATA addendum.

## CE-2  P4-F1 ("strict enlargement between nonrectangular relation lattices preserves realized geometry") is FALSE in general
Smallest FIELD-I instance (21 recorded in `results/P4_FIELDI3.json:noncontained`, exact witnesses, independently re-checked by RUN_VERIFY S10):
x = 2^5 * 5^4 * 7^6 / 9 = 2352980000/9  ->  C(x) = 2^4 * 5^4 * 7^6 / 3 = 1176490000/3.  Active primes (2,5,7), box Q = [0,2]x[0,2]x[0,3].
Source relation lattice Lambda_9 = ker chi_9 (index 6, nonrectangular), target Lambda_3 = ker chi_3 (index 2, nonrectangular, free coordinate: 7 = 1 mod 3).
Source cell P((0,0,3); (0,2,-1), (2,0,-2)) contains w = (16/9, 10/9, 2/3), which lies in no maximal cell of U(Lambda_3,Q).
Mechanism (P4-S1.a): 0 < w_3 = 2/3 < 1, and the planar part (16/9,10/9) lies in the hollow gap of the planar target ker(chi_3) on (2,5) = E2, box (2,2).
The source map has a zero-vertex decomposition: (0,0,3) + (0,0,-1) + (0,0,-2) = 0 (P4-Z1 flag) -- the flag is necessary here, as it is for all 57 recorded failures.
Other FIELD-I failures: primes (2,5,13), (5,7,11), (5,11,13) with (b,b') in {(9,3),(9,6),(18,3),(36,3),(36,6)}; all have target index 2, a free prime and an essential 3D source cell.
Lattice-only analogues (36, `results/P4_LATTICE3.json:failures`), e.g. source HNF basis [[1, 0, 1], [0, 1, 2], [0, 0, 4]] inside target HNF basis [[1, 0, 1], [0, 1, 0], [0, 0, 2]], box (2, 2, 2), witness ('1', '2/3', '5/3'); these are lattice candidates only (never FIELD-I results).
These do NOT contradict P4-T2: P4-F110's target E_3 is hull-covered at box >= 4 (no hollow gap), so there is no gap to hide a source point in.

## CE-3  "Hull-vertex coverage forces realized equality" (see CE-1)
Same counterexample; kept as a separate entry because it removes a tempting predictor: the target's uncovered region, not its vertex set, governs transport.

## Not counterexamples (recorded for completeness)
* 51 planar and 18 spatial lattice-level runs are zero-vertex flagged yet CONTAINED: P4-Z1 is a sufficient screen, not a criterion.
* 21 FIELD-I rows are UNAVAILABLE_COST (box (3,3,3), zero-vertex flagged, free coordinate); the slab sample finds no witness there; neither containment nor failure is claimed.
