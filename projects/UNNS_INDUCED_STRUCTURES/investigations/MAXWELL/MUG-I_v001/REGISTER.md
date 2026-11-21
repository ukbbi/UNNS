# MUG-I v001 — research release register

Status: research release (not a manuscript chapter). Source record: `MUG-I_v001_Maxwell_Mode_Geometry_and_Carry_Activation.tex` (proof record), suite `verification/verify_all.py` (12 checks, all pass, sympy required).
Reference records (frozen, unchanged): Algebraic and Topological Extensions v1.1; Torsion-Class Carry Dynamics v1.0.

## Theorem register

| ID | Statement | Level | Evidence | Status |
|----|-----------|-------|----------|--------|
| M1 | Torus mode m = g·u; r_N·m integral iff N divides g; T_N fixes u | label | proof; V1 (30k random trials, full mode) | proved + verified |
| M2 | Spectral class of mode is [sqrt(sf(u·u))]; realised squarefree sigma are exactly sigma not 7 mod 8 | label (spectral) | Legendre three-square theorem; V2 (sigma ≤ 70, exhaustive search) | proved + verified |
| M3 | Dilation E(αr,αt) is an exact vacuum Maxwell symmetry; fixes direction, polarisation, amplitude, energy; frequency ×α; action ÷α | field | proof; V4, V4b, V8 (symbolic residuals, exact rational arithmetic) | proved + verified |
| M4 | Multimode admissibility of a history = admissibility on gcd of support | label | proof; V3 | proved + verified |
| M5 | Transported field depends on a history only through ∏ r_N; dilation has no fixed nonzero field | field | proof (composition of dilations) | proved (no separate computation) |
| M6 | Conducting box (TM_z): dilated field keeps wall conditions iff α(m,n,p) integral; then equals TM_{α(m,n,p)} with same amplitude | field | proof; V7 (TM_(2,4,6): N=2 exact, N=4 violates walls) | proved + verified for the stated mode family only |
| M7 | Inter-cavity carry between cells of side L_i = L_0/a_i is the rational index map c_i; admissible iff den(c_i) divides content; spectra of the d cells disjoint | label (spectral) | proof; V5 (exact radicals), V6 | proved + verified |
| M8 | Lattice similarities M in GL_D(Q), M^T M = λ²I: need λ² rational; D odd forces λ rational; D=2 iff λ² sum of two rational squares; D=4 always | field (symmetry) | proof; V9 (integer brute force sigma ≤ 40, D=2,3; D=4 sigma ≤ 15) | proved; brute force covers integer matrices only |
| M9 | No field-level similarity carry with irrational alpha on the 3-torus | field | corollary of M8(a) | proved |
| M10 | Planar torus: carry by (1+i) reproduces the sqrt2 layers exactly (c0=1, c1=2; inverse c0=1/2, c1=1; inverse admissible iff m_x+m_y even) | field | proof; V10 (symbolic field map, m=(3,0)->(3,3)->(0,6)), V11 (888 modes) | proved + verified |

## Controls and classification

- Inherited from integer labels (no field content): M1, M2, M4, M7.
- Implied by Maxwell's dilation and rotation symmetries: M3, M5, M6.
- Structural restriction from field-level geometry: M8, M9, M10.
- Every inter-cavity carry is a rational map after choosing cavity-adapted coordinates; no coupling, mode conversion or energy transfer is defined or claimed.

## Limitations

- M6 verified symbolically for one TM family at one index triple per case, not for all mode types.
- M8 brute-force check is a sanity check on the proof, not additional proof.
- M5 has no independent computational check.
- FUG-I v005 records were not read for this release; no comparison with its history invariants is made.
- Vacuum, nondispersive, source-free only.

## Unresolved questions (candidates for v002)

1. Does the 45-degree similarity carry fail on conducting walls (expected, not checked)?
2. Planar torus with several carries (sqrt2 with sqrt5, classes with primes 1 mod 4): does the coupled system on Z[i] contain connectivity or branching absent from the abstract layers?
3. Ancestry and reconvergence of T_N-histories on mode rays against the FUG-I v005 baseline. M5 says fields see only the product, so any history invariant must be label-level; is there one that is also compatible with boundary conditions?
4. Dispersion: where dilation symmetry breaks, and what survives.
5. Is there a field-level quantity that distinguishes states with equal label and equal class but different content g? (Currently none found.)
