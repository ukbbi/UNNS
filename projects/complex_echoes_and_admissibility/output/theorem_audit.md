# Theorem audit: s4 and s5 of "Complex Numbers in the UNNS Substrate"

**Source caveat.** The manuscript text was not available to this module (it is not in the project documents or in the ESC_I
folder). Claims are audited **as stated in the review summary**. The s4 model `x_(n+1) = Pi C_eps (T x_n)` is formalised here as
`x_(n+1) = F(x_n)` with `|F(x) - T x| <= err(x)`, under two error models: absolute (`err = h`) and relative (`err = eta |x|`). That formalisation is an
assumption of this audit and should be checked against the paper's definitions of Pi and C_eps.

Status vocabulary: **ESTABLISHED** (proved here, verified computationally) / **CONDITIONAL** (true under stated hypotheses) /
**FALSE AS STATED** (counterexample) / **CONJECTURAL** (not decided here).

## Summary

| Claim | Original (as summarised) | Status | Corrected statement |
|---|---|---|---|
| s5 | rho(U_theta T) = rho(T) | **FALSE AS STATED** | T5.1 counterexample; true under T5.2-T5.5 |
| s4 | projected recursion preserves dominant growth rate and eigendirection | **FALSE AS STATED**, **CONDITIONAL** | T4.1 (relative error), T4.2 (absolute error) |
| s5 generalisation to n > 2 / cyclotomic lattices | not decided | **CONJECTURAL** | see C1 |

## s5  Phase inletting

**T5.1 (counterexample, exact).** T = [[1,1],[1,1]], U = diag(1,-1): rho(T) = 2, rho(UT) = 0, rho(U T U^-1) = 2, UT != TU.
U is even orthogonal, so orthogonality of the phase operator does not rescue the claim.

**T5.2 (similarity, ESTABLISHED).** For invertible U: (U T U^-1)^n (U x0) = U (T^n x0), and U is a bijective bi-Lipschitz map, so rho, the orbit class, its period and its
sub-type are all preserved. Verified exactly on 2000 random integer cases: 0 violations.

**T5.3 (commuting, unimodular, ESTABLISHED).** If UT = TU and every eigenvalue of U has modulus 1, then rho(UT) = rho(T)
(simultaneous triangularisation: the eigenvalues of UT are u_i t_i). In 2x2 with U = R_theta, theta not in {0, pi}, commuting is equivalent to T in C = span(I, J), i.e. complex multiplication.

**T5.4 (phase law, ESTABLISHED).** For U = R_theta and T = [[a,b],[c,d]]: det(R_theta T) = det T and tr(R_theta T) = (a+d) cos(theta) + (b-c) sin(theta).
So the whole family R_theta T is governed by one number, tau_theta in [-m, m], m^2 = (a+d)^2 + (b-c)^2. Verified exactly with rational rotations: 0 violations.

**T5.5 (characterisation, ESTABLISHED).** rho(R_theta T) is independent of theta **iff** T is a scaled isometry, T in C u C-bar = {aI+bJ} u {[[a,b],[b,-a]]}.
*Proof.* rho depends only on (|tau|, det) and is nondecreasing in |tau|; it is constant on |tau| <= 2 sqrt(det) when det > 0 and strictly increasing beyond;
strictly increasing in |tau| when det <= 0. As theta varies, |tau_theta| sweeps [0, m]. For det > 0, constancy needs m^2 <= 4 det, and
4 det - m^2 = -(a-d)^2 - (b+c)^2, so a = d and b = -c. For det <= 0 constancy needs m = 0, i.e. a = -d and b = c. The converse is direct. QED
*Corollary.* rho(UT) = rho(T) for all orthogonal U iff T = r Q with Q orthogonal; and sup over orthogonal U of rho(UT) equals the largest singular value sigma_max(T).
Computational check on integer matrices x 25 rational rotations: 49 scaled-isometry cases, 0 invariance violations;
576 other cases, of which 8 show no variation on the finite grid (grid-limited, not counterexamples: T5.5 asserts variation at some theta, possibly off-grid).
Sup check on 300 matrices: 0 exceed sigma_max; largest shortfall of the sampled sup below sigma_max = 1.40e-05.

**Implication for admissibility.** Left phase multiplication preserves the spectral regime for scaled isometries and for conjugations; for every other T it
sweeps a range of rho and can cross rho = 1. This is the content frozen as AR-1.

## s4  Projection and spectral persistence

Setting: T = V diag(lam, mu) V^-1 with real eigenvalues, |lam| > 1, |lam| > |mu|; eigen-coordinates z = (u, w); eigen sup-norm.

**C4.0 (counterexamples to the unrestricted claim, exact).**
1. *Absolute error, attracting zero.* T = 2I and Pi = rounding to Z^2: x0 = (1/5, 0) maps to 0 at the first step; the projected orbit is identically 0 (all zero: True) although rho(T) = 2.
2. *Relative error >= |lam|.* F = 0 satisfies |F(x) - T x| <= |lam| |x|; the orbit collapses.
3. *Degenerate state.* T = diag(2, 1/2), x0 = (0,1) lies on the stable eigenline: exact class **convergent** although rho = 2. A growth theorem needs u0 != 0.
4. *Projection onto an invariant subspace.* T = diag(2, 1/2), Pi zeroes u when |u| < 1, x0 = (2/5, 1): the unprojected orbit is divergent; the projected orbit is
   ('0', '1/256') after 8 steps (u erased at step 1, then w decays): a **structural transition divergent -> convergent caused by the projection**.
5. *Complex dominant pair.* No real eigendirection exists. With T = 1.5 R_30deg and relative error eta = 0.3 the per-step norm ratio stays in [1.2, 1.8], but an adversary
   rotates the state by up to arcsin(eta/r) = 0.201 rad each step: direction drift after 200 steps up to 40.3 rad. Rate is robust, direction is not.

**T4.1 (relative error, CONDITIONAL).** Suppose |F(x) - T x|_inf <= eta |x|_inf in eigen-coordinates, eta <= (|lam| - |mu|)/2, and |w0| <= |u0|, u0 != 0.
Then for all n: |w_n| <= |u_n| and |u_(n+1)|/|u_n| in [|lam| - eta, |lam| + eta]. The growth rate is preserved **only up to eta**, not exactly; and divergence is guaranteed when |lam| - eta > 1.
In the limit the direction lies in the cone |w|/|u| <= eta/(|lam| - |mu| - eta). In original coordinates eta is multiplied by kappa_inf(V) = |V|_inf |V^-1|_inf.
*Proof.* |u_(n+1)| >= (|lam| - eta)|u_n| and |w_(n+1)| <= (|mu| + eta)|u_n| <= (|lam| - eta)|u_n| <= |u_(n+1)|, using the cone hypothesis; induct. QED
Adversarial exact simulation (1500 cases x 40 steps): 0 violations.

**T4.2 (absolute error, CONDITIONAL, sharp).** Suppose |F(x) - T x|_inf <= h. If |u0| > h/(|lam| - 1) then |u_n| increases strictly, |u_(n+1)|/|u_n| -> |lam|, and the direction converges to the dominant eigenline:
growth rate and eigendirection are preserved **exactly in the limit** (the ratio r_n = |w_n|/|u_n| obeys r_(n+1) <= (|mu| r_n + h/|u_n|)/(|lam| - h/|u_n|) -> 0 because |u_n| -> infinity; only the u-part is checked computationally). If |u0| <= h/(|lam| - 1) an admissible projection can stall or erase u (the adversary u -> |lam||u| - h is not escaping), so the threshold is sharp.
*Proof.* |u_(n+1)| >= |lam||u_n| - h > |u_n| iff |u_n| > h/(|lam| - 1); the threshold is then never re-crossed. QED
Adversarial exact simulation (488 cases above and 1004 below the radius x 50 steps): 0 violations.

**Implication for admissibility.** Projection preserves a divergent regime when it is *small relative to the state* (T4.1) or when the state starts *outside an escape radius* (T4.2); otherwise it can
move the orbit into the stable invariant subspace (C4.0.4). Frozen as AR-3. Original claim as stated: **FALSE**; with these hypotheses: **CONDITIONAL**.

## Conjectures not decided here
**C1.** T5.5 for n x n real matrices: rho(UT) = rho(T) for all orthogonal U iff T is a scaled orthogonal matrix. Only the 2x2 case is proved here.
**C2.** T4.1 and T4.2 for non-diagonalizable T (Jordan blocks), complex dominant pairs (rate only), and cyclotomic lattice projections with non-nearest-point Pi.

Rules module hash (frozen before this audit was written): `c32fa4fd2469fee5ab3654b91cb28843e23463d04f5c56b7d63c7df14ec19b54`
