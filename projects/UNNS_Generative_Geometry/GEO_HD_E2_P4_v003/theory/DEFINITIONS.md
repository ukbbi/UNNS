# E2-P4 definitions (append-only; inherits E2-P3/DEFINITIONS.md)

* **FIELD-I step.**  For x = a/b in lowest terms, D(x) = { d >= 2 : d^2 | a, d = 1 (mod b) }, L = lcm D, G = gcd{ d-1 : d in D }, C(x) = x + L^2/G.
* **Coordinates.**  P = primes p with v_p(a) >= 2, box Q = (floor(v_p(a)/2))_p.  chi_b(alpha) = prod p_i^alpha_i mod b;  Lambda_b = ker chi_b;
  F(Lambda,Q) = (Lambda cap [0,Q]) \ {0}.
* **Graver cells.**  Region Graver set = conformally minimal vectors of Lambda inside [-Q,Q]; a j-cell P(u; g_1..g_j) has linearly independent
  g_i from the (lex-positive) Graver set and all 2^j corners in F.  U(Lambda,Q) = union of the closed parallelotopes; H = conv F;
  coverage gap G' = H' \ U'.
* **Rectangular / nonrectangular (spec 3.2-3.3).**  o_i = ord_b(p_i), H_b = <p_1..p_k> in (Z/b)^x.  Lambda_b is rectangular iff |H_b| = prod o_i,
  nonrectangular iff |H_b| < prod o_i.  [Z^k : Lambda_b] = |H_b|.
* **E_3** = { z in Z^3 : z1+z2+z3 even }.  **Cube cell** C(w) = w + [0,2]^3 = P(w; 2e_1, 2e_2, 2e_3).
* **Transport outcomes (spec 4.1).**  EQUAL, SOURCE_CONTAINED (U strictly inside U'), TARGET_CONTAINED, INCOMPARABLE.
* **P4-F110.**  x_m = 2*110^(4m)/9 -> y_m = 110^(4m)/3, primes P = (2,5,11), box Q_m = [0,2m]^3.
