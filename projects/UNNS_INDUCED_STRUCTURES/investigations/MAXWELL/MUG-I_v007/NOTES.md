# MUG-I v007 — Eigenmode-resolved induced geometry

Research notes. No manuscript. Question: when the fixed T_N law meets the exact eigenstates of a Maxwell system (mixed Fourier content,
Bragg splitting, parity sectors) rather than their Fourier labels, does it induce a well-defined relation between exact states, and does that
preserve, restrict or transform the nesting histories? Verification: verification/verify_v007.py, 10 checks, all pass (~2 s; numpy, scipy).
Results-file sha256 (of the file as archived) starts 565be6c5… (the printed hash of the canonical JSON is the same content).

## 1. System and rule
- Periodic medium ε(z) = 1 + 2δ cos(qz) on the torus ℝ/2πℤ, field −E'' = ω² ε E (k ∥ z, E transverse; scalar Hill problem). Fourier index m, Bloch class κ = m mod q; classes decouple. Eigenvectors are ε-weighted orthonormal. Main runs: q = 4, δ = 0.1 (also q = 6, 12).
- Exact state = eigenvector. Its Fourier support is κ + qℤ (harmonics g ± jq nonzero, checked ≥ 1e-12 for |j| ≤ 2). Fourier label g = dominant |m|. Whole-field content of a state = gcd of its support = gcd(κ, q) = gcd(g, q).
- **Rule E (eigenstate-resolved, fixed medium).** A step N acts on a field x by (i) keeping the components in Bloch classes whose support content is divisible by N (whole-field admissibility, from v003), then (ii) dilating the surviving indices m → r_N m with r_N = (N+1)²/N. Step (ii) is an exact ℓ² isometry; step (i) can lose norm ("blocking"). This is a declared induction rule (the componentwise alternative, which drops only non-divisible harmonics, is a different rule and is not tested).

## 2. Results
**Y1. The label is meaningful only in a window.** Two exact states per label g (parity pair), dominant weight ≥ 0.83 for g ≤ 24 at δ = 0.1. The window ends when the phase-modulation index β = δg/q reaches about 1.1: first failing g is 113, 75, 45, 22 for δ = 0.04, 0.06, 0.1, 0.2 (β = 1.13, 1.125, 1.125, 1.10). Heuristic: the WKB field ~ exp(i(ωδ/q) sin qz) has dominant harmonic J₀(β). Beyond g ≈ 1.1 q/δ the Fourier label no longer tracks any exact state, so v006's label-level statements for the periodic medium are valid only below that bound.

**Y2. Parity splitting is exactly the resonant set (proved + checked).** z → −z maps Bloch class κ to −κ, so the two parity partners are exactly degenerate unless κ ≡ −κ (mod q), i.e. g ∈ (q/2)ℤ (this is the v006 resonant set aℤ). There the pair lies in one self-conjugate class and splits; numerical relative splitting (q=4, δ=0.1) at j = 2g/q = 1…6: 0.22, 2.0e-2, 2.6e-3, 3.6e-4, 5.4e-5, 8.3e-6 (≈ δ^j). Off resonance the pair is degenerate to < 1e-9 (eigensolver level) for g ≤ 24. Both parities occur at resonant labels. So the v006 "resonance trace" is exactly the set of labels with split parity sectors.

**Y3. Whole-field admissibility restricts the vocabulary (rule E).** N is admissible on a state iff N | gcd(g,q), which forces N | q: the step alphabet is Div(q). Fraction of label edges (g < 3000) removed: 78.6% (q=4, alphabet {1,2,4}), 75.5% (q=6, {1,2,3,6}), 71.4% (q=12, {1,2,3,4,6,12}). The v006 closure statement (Maxwell cannot remove edges) applied to label vertex sets; for exact states of a periodic medium it fails under rule E.

**Y4. Transformation: Bloch-class splitting (checked on 292 states, q = 4, 6, 12).** The image of a state with class κ under an admissible N lies in the classes κ′ = (N+1)²κ/N + i q/N (i = 0…N−1), N classes. The image is an exact eigenstate of the dilated medium (period r_N q), so T_N is exact as a relation between (medium, state) pairs; with the medium held fixed it is not a function. (The smallest main-class weights, ≈ 0.44–0.5, are the ±m pair of a parity state landing in classes κ′ and −κ′.)

**Y5. A weighted relation with leakage.** Expanding the image in the exact eigenstates of the same medium (δ = 0.03, g ≤ 16, N | gcd(g,q)): the weight on the two exact states labelled r_N g is between 0.741 and 0.992 (typically 0.93–0.99), the rest leaks to other eigenstates. So T_N induces a transition kernel on exact states concentrated near the label image, not a map.

**Y7. Without blocking, histories are path independent exactly.** For 78 ordered pairs of admissible words in Div(q) with full survival, the final field is identical (the multiplier group is abelian).

**Y6. History dependence enters only through blocking.** Groups of ≥ 2 label histories with the same endpoint (g₀ ≤ 24, g₁ ≤ 3000, length ≤ 4):
- q = 6: 216 groups: 117 fully blocked (every history dies), 76 all survive and agree, 17 differ in survival, 6 mixed.
- q = 12: 118 groups: 27 fully blocked, 78 all survive and agree, 8 differ in survival, 5 mixed.
Examples (q = 6): g 6 → 1728: (1,1,1,2), (1,1,2,1), (1,2,1,1), (2,1,1,1) survive with weight 1, (3,8,3) is blocked (survival 0). g 12 → 972: (1,2,2) and (2,1,2) survive 1, (2,2,1) survives 0.975372. So equal-endpoint histories can give different fields or die, for an intrinsic reason (a step passes through a Bloch class whose content is not divisible by the next N). The surviving part is path independent; the history dependence is in what is blocked.

## 3. What it means for O5
Under exact-eigenmode induction with whole-field admissibility, Maxwell structure does change the induced geometry: it restricts the step alphabet to Div(q), splits each field into N Bloch classes, and makes composition depend on the history through blocking. These are not invented operators; they follow from the Bloch-class content of exact eigenstates and the divisibility rule. Under Fourier-label induction (v005, v006) none of this appears. The two inductions are different objects and both are retained.

## 4. Limits
- One scalar 1D medium (k ∥ z); vector structure, polarization and the plasma of v005 not combined with it.
- Everything depends on rule E (whole-field admissibility and re-resolution in Bloch classes each step). The componentwise rule and a rule with the medium co-dilating (then no blocking occurs and histories are exactly path independent) were not compared quantitatively.
- Survival is measured in Fourier-coefficient ℓ² weight, not energy.
- The nonvanishing of harmonics g ± jq (hence content = gcd(g,q)) is leading-order perturbative, checked numerically for |j| ≤ 2, not proved. Y2's nonzero splitting on resonance is checked for g ≤ 14 (double precision) and relies on all Mathieu tongues being open.
- Y1b's window law is empirical (4 values of δ).
- FUG-I v005 comparison still not done.
