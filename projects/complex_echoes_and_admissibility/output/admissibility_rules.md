# ESC-I admissibility rules AR-1, AR-2, AR-3 (frozen)

Status: **hypotheses derived from the audited mathematics in `theorem_audit.md`; not established UNNS laws.**
These definitions, thresholds and test-set parameters were written, hashed and saved *before* any exact
comparison was run. The hash is recorded in `admissibility_report.json`.

Verdict vocabulary: ADMIT / ESCAPE / CONE / RHO-INVARIANT / REGIME-PRESERVED (a transition or projection is
predicted to keep the regime), REGIME-CAN-CHANGE / NO-ESCAPE (predicted to leave it), CERTIFIED / KNIFE-EDGE /
UNCERTIFIED (robustness), ABSTAIN (the rule makes no claim). Rule code never calls the exact classifier.

## AR-1  Route preservation (phase and similarity transformations of a recursion T)
(a) Conjugation T -> U T U^-1 with x0 -> U x0, U invertible: **ADMIT**. Exact class, period and sub-type of the orbit are preserved.
(b) Left rotation family T -> R_theta T. With A = a+d, B = b-c, det(R T) = det T and tr(R T) = A cos(theta) + B sin(theta),
    so the family spans |tau| in [0, m], m^2 = A^2 + B^2.
    - T in C u C-bar (T = aI+bJ or [[a,b],[b,-a]], i.e. T a scaled isometry): **RHO-INVARIANT** for every theta.
    - otherwise compare the regime of rho at |tau|=0 and |tau|=m (exact, Jury form):
      equal -> **REGIME-PRESERVED**; one '<' and the other '>' -> **REGIME-CAN-CHANGE**; else **ABSTAIN** (touching rho=1 only at isolated phases).
(c) General left multiplication T -> U T: **ABSTAIN** (negative control: no certificate is asserted).
Falsification: (a) any case where the exact class/period/sub-type of (U T U^-1, U x0) differs from that of (T, x0);
(b) any rational rotation in the grid whose regime or rho contradicts the verdict (CAN-CHANGE must be witnessed by the grid or is recorded as unconfirmable).

## AR-2  Boundary sensitivity (certified margin)
For diagonalizable T with rho != 1: eps_cert = min(|rho-1|, gap/2 if rho>1) / kappa_2(V) (gap = |lambda1 - lambda2|; scalar T: kappa=1, gap=inf).
**CERTIFIED**: the regime (rho vs 1) of T+E is preserved for every real E with ||E||_2 < eps_cert.
rho = 1: **KNIFE-EDGE**: for every eps>0 some perturbation of norm <= eps*||T|| changes the regime.
Non-diagonalizable: **UNCERTIFIED**.
Falsification: (i) a regime change under ||E||_2 <= 0.98 eps_cert; (ii) a KNIFE-EDGE T whose scalings (1+-eps)T fail to change the regime.
Sharpness hypothesis (this one can fail): the smallest regime-changing perturbation is at most K = 10 times eps_cert.
It is confirmed per matrix by an explicit witness found by a fixed direction search; absence of a witness is recorded as 'unconfirmed', not as refutation.

## AR-3  Projection persistence (x_{n+1} = Pi(T x_n), T = V diag(lam, mu) V^-1, |lam| > 1, |lam| > |mu|, u0 != 0)
Eigen-coordinates z = (u, w); error measured in the eigen sup-norm.
- Absolute error <= h: **ESCAPE** iff |u0| > h/(|lam|-1); otherwise **NO-ESCAPE** (two-sided, sharp for the adversarial projection).
- Relative error <= eta: if eta <= (|lam|-|mu|)/2 and |w0| <= |u0|: **CONE**: every step satisfies |u_{n+1}|/|u_n| in [|lam|-eta, |lam|+eta] and |w_n| <= |u_n|. If eta >= |lam|: **NO-ESCAPE**. Else ABSTAIN.
- Dead-zone projection (u zeroed if |u|<theta): ESCAPE if |u0|>theta/(|lam|-1); NO-ESCAPE if |lam||u0|<theta; else ABSTAIN.
- Nearest rounding to the lattice h Z^2 (original coordinates): ESCAPE if |u0| > ||V^-1||_inf (h/2)/(|lam|-1); NO-ESCAPE if T x0 rounds to 0; else ABSTAIN.
- k-bit relative quantizer: eta_eig = ||V||_inf ||V^-1||_inf 2^-k, then the relative-error rule.
Falsification: simulate the projected orbit in exact rational arithmetic for N = 60 steps. ESCAPE fails if |u_n| is not strictly increasing; CONE fails if a ratio leaves its interval or |w|>|u|; NO-ESCAPE fails if the orbit escapes.

## Outcome vocabulary for the comparison
AGREE, DISAGREE (rule falsified or implementation error), ABSTAIN (the exact computation resolves the case; the rule does not),
UNCONFIRMABLE (prediction needs a witness outside the finite grid). Every DISAGREE is listed individually in the report.

---
SHA-256 of rules text + frozen parameters: `c32fa4fd2469fee5ab3654b91cb28843e23463d04f5c56b7d63c7df14ec19b54`
Seed: 20261013. Frozen parameters: `{"ar1_conj_cases": 400, "ar1_phase_grid_t": ["-3", "-11/4", "-5/2", "-9/4", "-2", "-7/4", "-3/2", "-5/4", "-1", "-3/4", "-1/2", "-1/4", "0", "1/4", "1/2", "3/4", "1", "5/4", "3/2", "7/4", "2", "9/4", "5/2", "11/4", "3"], "ar1_negctl_cases": 300, "ar2_cert_cases": 300, "ar2_violation_samples": 40, "ar2_violation_scale": 0.98, "ar2_sharp_cases": 120, "ar2_sharp_K": 10, "ar2_sharp_dirs": 14, "ar2_sharp_step": 1.12, "ar3_N": 60}`

---
## AR-3.1  Corrected k-bit quantizer clause (frozen before the confirmation set is generated)
Clause: for the k-bit relative quantizer (each coordinate of T y rounded to k significant bits), eta_eig = kappa_inf(V) |lam| 2^-k,
and the CONE verdict of AR-3 applies with this eta_eig (conditions: |lam| > 1, |lam| > |mu|, u0 != 0, eta_eig <= (|lam|-|mu|)/2, |w0| <= |u0|), else ABSTAIN.
Origin: the frozen AR-3 clause used eta_eig = kappa_inf(V) 2^-k and was falsified in 92 of 540 REL_QUANT cases (retained in the report).
The amended clause was then explored post hoc on the same 540 cases (234 agree, 306 abstain, 0 disagree). The source hash of the amended rule function in
this run must equal the hash recorded in that earlier run: `2cf5d68ae0b293fb2f06a37579e0dd216870ae3046efb0ec11cf6b9c713ff3f1`.
Confirmation set (all fresh; the original test set is not reused): seed 20261113; 60 random systems (V with entries n/2, n in -6..6, det != 0; lam = +-m/4 in [1.25, 6]; |mu| < |lam|)
x bits [4, 8, 12] x 15 states (u0 in {1/2,-1,3}, w0/u0 in {0,1/2,-1/2,1,3/2}); plus 20 near-boundary base systems with lam = 3 and
|mu| = |lam| - 2 eta (1+delta) for delta in {-1/100, 0, +1/100}, bits [7, 8, 9, 10], same 15 states. The boundary families put eta_eig 1% above the cone-theorem limit (just outside: the rule must abstain), exactly at the limit (the rule must apply), and 1% below it (just inside), with |w0| = |u0| included.
Independent check of the conversion itself: at every step, the observed eigen-coordinate quantization error |V^-1 (Q(Ty) - Ty)|_inf / |z|_inf must not exceed eta_eig.
Simulation: exact rational arithmetic, N = 60 steps.
Success criteria: zero DISAGREE among CONE predictions (rate in [|lam|-eta, |lam|+eta] at every step, |w| <= |u|), zero violations of the per-step error bound, and
the frozen-original conversion (without |lam|) is violated by the observed error in at least one case (shows the factor is needed, not decorative).
The 92 original disagreements remain part of the record.

SHA-256 of AR-3.1 text + confirmation parameters: `36d7bea38dd1b9217edc5a6654c7ca5020fd93d019ed49dba91d56097965da41` (computed at the start of the run, before any test case was generated)

---
## Post-hoc amendment (written AFTER the frozen comparison; exploratory; not covered by the hash above)
The frozen comparison falsified the k-bit quantizer clause of AR-3 (REL_QUANT): 92 of 540 cases disagreed, all of that one clause.
Cause (a derivation error in the frozen rule, found by the comparison): the quantizer rounds the image T y, so its error is relative to |T y|,
not to |y|. The frozen conversion eta_eig = kappa_inf(V) 2^-k omitted the factor |lam|. Amended clause: eta_eig = kappa_inf(V) |lam| 2^-k.
Re-run of the amended clause on the same 540 cases (exploratory, same exact simulation): AGREE 234, DISAGREE 0, ABSTAIN 306.
This amendment must be confirmed on a fresh seeded test set before it is treated as part of AR-3.

---
## AR-3.1 confirmation outcome (fresh set; appended after the run)
Cases: 3600; AGREE 2148, DISAGREE 0, ABSTAIN 1452.
Per-step error-bound violations of the amended conversion: 0 of 3600;
frozen-original conversion violated in 1359 cases; largest observed/amended bound = 0.748.
Success criteria met: **True**. Amended-rule source hash equals the earlier recorded hash: True.
The 92 original AR-3 disagreements are unchanged in `admissibility_report.json`.
