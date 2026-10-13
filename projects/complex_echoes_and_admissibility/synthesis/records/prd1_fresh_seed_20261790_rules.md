# PRD-1  Projection route dependence (frozen before any case is generated)

Status of AR-3.1 when this was frozen: **closed as confirmed within its tested domain.** The corrected conversion eta_eig = kappa_inf(V) |lam| 2^-k holds
under the rule's stated conditions, and the cone condition is sufficient but conservative. The standalone checker (`independent_check_ar31.py`) is the evidence for the
bound itself; the stored records are evidence of internal consistency only. The condition is not to be adjusted using the observation that the cone often holds outside it.
Existing AR-1..3 and AR-3.1 files and results are not modified by this experiment.

## Question
Two systems with identical unprojected spectral data (T, x0) can have different projected asymptotic behaviour. Does a rule that examines the *structure of the projection*
predict the projected regime, on unseen systems and projections, where a classical method that knows only the projection's error bound cannot?

## Domain (a stated restriction)
x_(n+1) = Pi(T x_n) in the **spectral frame**: T = diag(lam, mu), lam, mu rational, |lam| > 1, |lam| > |mu|, state z = (u, w), u0 != 0, Pi(0) = 0.
Projections written in another frame need a frame conversion and are out of scope here.

## Projection families (all five are retained)
- **DZ(theta)** dead-zone: u -> 0 if |u| < theta, else identity; w untouched.
- **CLIP(c)** saturation: each coordinate clamped to [-c, c].
- **LAT(h)** lattice rounding: each coordinate rounded to the nearest multiple of h (ties to even).
- **GATE** state-gated zeroing: u -> 0 if |u| <= |w|, else identity.
- **LINP(a), LINQ(b)** linear kernel projections (control): LINP(y) = (0, a y1 + y2), LINQ(y) = (y1 + b y2, 0). The orbit is the linear recursion with matrix Pi T.
Pi is applied to y = T z.

## Verdicts
DIVERGENT (|z_n| -> infinity), COLLAPSE (z_n = 0 exactly from some step), CONVERGENT (z_n -> 0), BOUNDED(B) (|z_n|_inf <= B for all n >= 1), ABSTAIN,
and, for linear Pi only, LINEAR-REDUCTION (the rule recognises the case as reducible to the classical analysis of Pi T and claims no regime).

## Rule R (structure-aware; may not simulate and may not call the exact classifier)
Notation: al = |lam|, am = |mu|.
- DZ: if al |u0| >= theta: DIVERGENT. Else u is erased at step 1 and stays 0; w1 = mu w0. If w1 = 0: COLLAPSE; am < 1: CONVERGENT; am = 1: BOUNDED(|w0|); am > 1: DIVERGENT.
- CLIP: BOUNDED(c).
- LAT: (i) DIVERGENT if |u0| > (h/2)/(al-1); (ii) DIVERGENT if am > 1 and |w0| > (h/2)/(am-1); (iii) COLLAPSE if al |u0| < h/2 and am |w0| < h/2;
  (iv) BOUNDED(am |w0| + h/2) if al |u0| < h/2 and am <= 1; (v) otherwise ABSTAIN.
- GATE: if al |u0| > am |w0|: DIVERGENT (the ratio |w|/|u| shrinks by am/al, so u is never gated). Else u is erased at step 1 and stays 0: am < 1: CONVERGENT; am = 1: BOUNDED(|w0|); am > 1: DIVERGENT.
- LINP, LINQ: LINEAR-REDUCTION.

## Classical comparator C (knows T and the projection's *error bound* only; plus the exact classifier on Pi T for linear Pi)
Error bounds: DZ: absolute theta; LAT: absolute h/2; CLIP and GATE: no finite absolute bound, and the relative bound of GATE (eta = al) violates eta <= (al-am)/2, so C abstains.
For DZ and LAT: DIVERGENT if |u0| > e/(al-1), or am > 1 and |w0| > e/(am-1) (escape-radius theorem, e the absolute bound); otherwise ABSTAIN.
For LINP/LINQ: the exact classifier applied to the matrix Pi T (divergent -> DIVERGENT, convergent -> CONVERGENT, periodic or bounded -> BOUNDED).

## Ground truth and evidence levels
Exact rational simulation, N = 200 steps, no floating point. Finite-horizon evidence alone never certifies an asymptotic claim. Asymptotic certificates used:
- exact return to 0 (Pi(0) = 0, so 0 is absorbing) -> COLLAPSE;
- exact repetition of a state (deterministic autonomous recursion) -> periodic forever, hence BOUNDED;
- an a posteriori escape-radius certificate from the orbit (DZ and LAT only, the families with a finite absolute error bound).
Each certified prediction is scored: CONFIRMED_ASYMPTOTIC (a certificate above agrees), CONSISTENT_FINITE_HORIZON (no contradiction within N, no certificate), or CONTRADICTED.
Contradiction rules: DIVERGENT is contradicted by a zero hit, a repeated state, decay below |z0|/1000000, or growth below 1000000 x max(1,|z0|); COLLAPSE by no zero hit;
CONVERGENT by neither a zero hit nor decay below |z0|/1000000; BOUNDED(B) by growth or by any |z_n|_inf > B for n >= 1.
Growth and decay thresholds are fixed constants, chosen so that every divergent or convergent system in the test set clears them by orders of magnitude at N = 200.

## Test set (fresh seed 20261790; nothing from earlier experiments is reused)
30 systems: lam = +-m/4 with m in 5..20, |mu| drawn from ['0', '1/4', '1/2', '3/4', '7/8', '1', '5/4', '3/2', '2'] with |mu| < |lam|, random signs. For each system, every family and parameter
(DZ theta in ['1/4', '1/2', '1', '2'], CLIP c in ['1', '2', '4'], LAT h in ['1/4', '1/2', '1'], GATE, LINP a in ['1/2', '2'], LINQ b in ['1/2', '2']): 12 random states (u0 in +-['1/8', '1/4', '1/2', '1', '2', '4'], w0 in +-['0', '1/8', '1/4', '1/2', '1', '2', '4'], u0 != 0) plus exact tie states
(DZ: |lam u0| = theta; GATE: |lam u0| = |mu w0|; LAT: |lam u0| = h/2).
Recognition check: for every family, additivity and homogeneity of Pi are tested exactly on 40 seeded random triples; the declared linear/nonlinear status must match.
Route dependence is measured against the unprojected exact classifier, which for every system and u0 != 0 returns divergent.

## Success criteria (stated in advance)
1. Zero CONTRADICTED among the certified predictions of R, and among those of C.
2. Coverage reported per family: certified / abstained, for R and for C, with the cases certified by R only, by C only, and by both.
3. Of the cases where the unprojected classifier is wrong about the projected regime (projection-induced flips), the number certified correctly by R and by C.
4. The recognition check passes for all five families, and for the linear control the orbit equals the matrix recursion Pi T exactly for all N steps.
5. Computational cost is reported separately from correctness: R evaluates a closed-form condition (no orbit); simulation costs N steps per case.
The strongest claim these criteria can support: for the stated domain, a structure-aware rule certifies the projected regime without trajectory simulation, with broader coverage than error-bound classical analysis.
They do not support a claim of superiority over classical mathematics: a classical analyst who reads the same projection definition can derive the same conditions.

---
SHA-256 of this text + frozen parameters: `7b4d80391b32dbca663b2614507e4b0782b4d2e54ba6e21ce0f23187406e5b63`

---
## PRD-1 outcome (appended after the run)
Cases: 5637 (4197 nonlinear scored for R and C, 1440 linear control).
Rule R: certified 3989 (confirmed-asymptotic 2979, consistent-finite-horizon 1010), abstained 208, **contradicted 0**.
Comparator C: certified 1838, abstained 2359, contradicted 0. Coverage overlap: {'R_only': 2151, 'C_only': 0, 'both': 1838, 'neither': 208}.
Projection-induced flips: 1526; certified correctly by R: 1406; by C: 0.
Linear control: orbit equals the matrix recursion in 1440/1440 cases; classical Pi T verdicts contradicted: 48.
Success criteria met (first run, as frozen): **False** ({'zero_contradicted_R': True, 'zero_contradicted_C': False, 'recognition_passed': True, 'linear_control_orbit_equals_matrix_recursion': True, 'all_criteria_met': False}).

### Post-hoc comparator amendment (exploratory; first-run numbers above are retained)
The 48 first-run contradictions were all in the comparator on the linear control. Cause: the exact classifier's "convergent" includes
convergence to a nonzero fixed point or 2-cycle, which the frozen mapping read as CONVERGENT (to the origin). This is a mapping error in the control comparator; rule R is untouched.
With the corrected mapping the control has 0 contradictions; criteria met after amendment: **True**.
Because the amendment was made after seeing the data, it is exploratory until confirmed on a fresh seed.
