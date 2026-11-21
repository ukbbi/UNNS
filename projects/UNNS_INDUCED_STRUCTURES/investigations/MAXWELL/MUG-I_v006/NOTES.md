# MUG-I v006 — Maxwell-constrained generative histories

Research notes. No manuscript. Question (O5): can Maxwell's field structure change the admissibility or composition of UNNS
histories, rather than only label a graph whose connectivity is already fixed? Order followed: (A) no-go baseline for
polarization transport, (B) admissibility restrictions, (C) mode conversion only where Maxwell supplies one, (D) classification.
Verification: verification/verify_v006.py, 14 checks, all pass (~9 s; mpmath, numpy, scipy). Results sha256 b57e1be5…
System: the v005 uniaxial cold plasma M_p (B0 ∥ z, torus 2π, c = 1) for Part A; PEC box, PEC waveguide and a periodic medium for Part B.
Modes/directions are counted modulo u ~ −u (v005 convention).

## A. Polarization transport: the no-go baseline
Diamond used throughout: histories (N=1,2): 2→8→36 and (N=2,1): 2→9→36 (both checked admissible). Question: U_{8→36}U_{2→8} =? U_{9→36}U_{2→9}.

**A1 (simple eigenmodes).** Off the axis (u ∦ z) and p > 0, the three branches have pairwise distinct Φ at every g (s lies strictly between Θ_− and Θ_+ because q(z−s) < 0; Θ_− < z < Θ_+; z = 0 gives Θ_+ = s+q > s). So each polarization is a single real line (simple eigenvalue), a real-analytic curve in g. Minimal normalised separation over u ≤ 14, g < 150: 9.0e-6; it tends to 0 as g → ∞ (branches approach the covariant asymptotes) but never vanishes (Z A1). On the axis the two transverse polarizations are degenerate for all g and the Langmuir branch crosses them at g² = p (A1b, as in v005 S6).

**A2 (baselines, constant polarization).** Vacuum (p = 0) and the isotropic plasma have g-independent polarization along every ray (A2a, A2b: deviation 0 to 1e-35). Every transport rule is then trivially path independent: nothing to detect.

**A3 (anisotropy rotates polarization).** In M_p the E± eigenlines rotate along the ray: for u = (1,1,1), p = 36, the angle from g=1 is 5.7° at g=2, 18.3° at 4, 29.3° at 9, 32.8° at 36, 33.1° at 324 (E− is the in-plane orthogonal line, same angles).

**A-NoGo.** For polarization transport that is (a) parallel transport of a connection on the eigenline bundle over the ray, or (b) a representation of the multiplier group (an operator depending only on r_N, multiplicatively):
- (a) The base is a real interval and the line bundle is trivial (A1). Transport along concatenated segments composes, and both diamond histories traverse the same interval [2,36], so U_A = U_B; any holonomy would be ±1 on a trivial bundle over a contractible base.
- (b) ℚ_{>0} is abelian; U depends only on ∏r_N = 4·(9/2) = 18 = 36/2 for both histories (A5 checks the product invariance on 500 random multisets).
So **under any such rule U_A = U_B exactly; polarization transport as parallel transport or as a multiplier-group representation cannot distinguish histories.** v001–v004 already showed the vacuum dilation symmetry has this form. History dependence would need an edge rule that depends on intermediate vertices without factoring through the multiplier — i.e. an additional physical operation, not Maxwell evolution.

**A4 (the one natural candidate: matched-polarizer cascade).** Define the amplitude of a history as the product of overlaps ∏|⟨e_i|e_{i+1}⟩| of the eigen-polarizations at successive vertices (an ideal polarizer matched to each mode in turn; Bargmann-type, gauge invariant). It is non-unitary and measurement-defined, not field evolution.
- Diamond, E+ (E− gives the same numbers, since the E± lines are orthogonal in the k–z plane): u=(1,1,1): 0.92010 (1,2) vs 0.91477 (2,1), direct 2→36: 0.89007; u=(1,0,1): 0.85098 vs 0.83924, direct 0.78437; u=(1,2,3): 0.95405 vs 0.95287.
- 17 merger histories, 6→3600, u=(1,1,1): amplitude spread 5.2e-4.
- Vacuum: spread 0 (exactly), isotropic plasma: 0 (constant polarization).
So the cascade distinguishes histories, but only because polarization rotates (anisotropic dispersion), and only as a projective-measurement amplitude. It is recorded as a candidate, not as a Maxwell-derived transport; whether it is physically wanted is a decision, not a theorem.

## B. Do Maxwell constraints remove or restrict T_N edges?
An edge can disappear only if its source or target is not a vertex of the induced structure. So the question is which vertex sets V arise.

**B1 (closure).**
- Translation-invariant linear media on the torus (all of v001–v005): every m ∈ ℤ³∖0 has a real-k mode in each branch (E− needs u_z ≠ 0). V is everything; nothing is removed.
- PEC box: multiplicity of (|m1|,|m2|,|m3|) is 2 if no index is zero, 1 if one is, 0 if two are. PEC waveguide (periodic in z): TM needs m1 m2 ≠ 0, TE needs (m1,m2) ≠ (0,0). Both depend only on the zero pattern, which positive scaling preserves: every admissible edge keeps source and target in V with equal multiplicity (24 800 edges checked).
- General statement: a vertex set defined by a condition invariant under positive rational scaling is closed under all T_N and inverses, so Maxwell cannot remove edges there. **A Maxwell restriction needs a non-scale-invariant (arithmetic) vertex set.** None of the systems above has one under k-labelled induction.

**B2 (periodic medium: the first arithmetic Maxwell structure).** ε = 1 + 2δ cos(qz) (Mathieu/Hill). Bragg resonance occurs at integer wave number g = j·q/2 = j·a (a = q/2): the plane-wave pair ±g is degenerate and splits into standing waves with a gap of order δ^j. Numerical check of the order (q = 4, Fourier–Galerkin on the torus): fitted gap exponents 1.0007, 2.0010, 3.0013 for j = 1,2,3 (B3). So the resonant set is ℛ_a = aℤ.
**Law (proved + exhaustively checked on 174 976 edges, a ∈ {1,2,3,5,6,10,12}, g < 6000):** for an edge g → g(N+1)²/N with N | g and a | g, the target is resonant iff Na | g (because a | (N+1)²g/N ⇔ N | g/a, as gcd(N,N+1)=1). Hence resonance is preserved forward whenever gcd(N,a) = 1, and can be lost only through a shared factor between N and a.
Edge counts (g < 6000): a=2: R→R 24 464, R→n 13 274, n→R 15 363, n→n 0 (an odd g only ever lands on an even g′); a=6: 7 053 / 11 703 / 13 015 / 21 330; a=5: 8 682 / 7 339 / 7 710 / 29 370.
**Consequence for histories:** equal-endpoint histories can differ in their resonance trace. The diamond with a = 2: (1,2) 2→8→36 stays on resonance throughout; (2,1) 2→9→36 passes through the non-resonant vertex 9. Over the 17 merger histories the number of resonant vertices visited is 3–5 (a=2: 1 history with 3, 6 with 4, 10 with 5; a=3: 2/4/4/7 for 2–5; a=5: 7/6/4 for 1–3). This is a genuine Maxwell×UNNS arithmetic structure; it modifies labels (band-edge frequencies at resonant vertices), not admissibility. (Parity sectors under z → −z are expected to be conserved and keep the graph unbranched; not verified here.)

## C. Mode conversion
The only real coupling mechanism in these systems is Bragg coupling m ↔ m − jq in the periodic medium, active exactly on the resonant set ℛ_a. No conversion transport is defined here; B2 identifies where it could act. Not developed (no invented operators).

## D. Classification (O5)
| system | edge removal | polarization transport (parallel / multiplier rep.) | matched-polarizer cascade | other history trace |
|---|---|---|---|---|
| vacuum, isotropic plasma | none | path independent | independent (constant polarization) | Θ-profile only (isotropic plasma) |
| uniaxial plasma M_p | none | path independent (no-go) | history dependent, ≤ ~1e-2 on the diamond | Θ-profile (v005) |
| PEC box / waveguide | none (closed) | path independent | not computed | none |
| periodic medium | none | path independent in the same sense (not separately tested) | not computed | resonance trace (B2), gap labels at resonant vertices |
Answers to the three outcomes: all histories endpoint-equivalent: true for every intrinsic transport rule tested; edge elimination: not realised in any k-labelled system studied, with a closure theorem explaining why; physically specified history-dependent transport: only non-intrinsic (cascade) or at label/trace level (Θ-profile, resonance trace). So O5 is answered **negatively for admissibility under k-labelled induction** and **positively only at the level of label and trace structure**.

## D2. Scope qualification added before freezing (Fourier label versus exact eigenmode)
In the periodic medium of B2/B3 the vertex g is the Fourier (plane-wave) label of a mode. The exact eigenstates of ε(z) = 1 + 2δcos(qz) are not plane waves: each carries Fourier support g + qℤ (Bloch class g mod q), mixed with harmonics g ± jq. So every periodic-medium statement in B2 (resonance membership, Bragg arithmetic law, resonance trace) concerns the dominant-Fourier-label graph, not the graph of exact field states. The PEC statements (B1) are unaffected: PEC box and waveguide modes are exact eigenstates and the index vector is their exact label. Whether T_N induces a well-defined relation between exact eigenstates, and what it does to admissibility, is not decided in v006; it is the subject of v007 (answer there: under whole-field admissibility the exact eigenstates restrict the step alphabet to divisors of the period q, so the closure statement of B1 does not carry over to exact states of a periodic medium).

## E. Limits and open items
- Closure (B1) is a statement about vertex sets defined by scale-invariant conditions; frequency-labelled induction (vertices defined by ω rather than k, where stop bands do remove vertices) is not defined here (O6).
- A1 gap tends to 0 as g → ∞ (asymptotic near-degeneracy); A-NoGo uses simplicity, not a uniform gap.
- The cascade is not a derived Maxwell transport. Whether a measurement-defined rule belongs in the induced structure is undecided.
- Periodic-medium results are for ε(z) = 1 + 2δcos(qz) propagating along z only; the cascade and no-go were not repeated there. Parity sector conservation unverified.
- FUG-I v005 comparison still not done.
