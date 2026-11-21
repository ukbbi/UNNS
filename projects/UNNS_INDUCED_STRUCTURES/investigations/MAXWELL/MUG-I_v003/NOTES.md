# MUG-I v003 — Representation invariance and the Maxwell structure of the nesting map (research note)

Status: research release, no manuscript. Suite: `verification/verify_v003.py` (7 checks, all pass, standard library, <1 s). Results: `results/verification_results.json`.
Question (course correction): when a Maxwell field is laid on the unchanged T_N, which induced quantities are intrinsic to the field, and does nesting engage Maxwell's own structure or only the arithmetic of the chosen representation?

## 1. Representation invariance (test 1): answer NEGATIVE for free periodic fields

1.1 Content is an index of lattices. For a field psi periodic on a cell lattice Lambda, let Stab(psi) be its lattice of translation periods. The content g = gcd of the Fourier indices equals the index [Stab(psi) : Lambda] (1-D: number of field periods in the cell). Checked numerically on 2880 translation tests of random 3-D fields: the field is invariant under translation by (cell edge)/q iff q divides g. (X2)

1.2 Cell dependence. Replacing the cell by m times the cell multiplies g by m (X3). The occurrence count is R(n) = #{d >= 2 : d^2 | n} (equal to the brute-force count of (M,N) with M(N+1)^2 = nN for n < 130; X1), so R(n) = 0 iff n is squarefree. Your example is reproduced: one fixed field with cells L, 2L, 4L has g = 1, 2, 4 and R = 0, 0, 1; cell 36 gives R = 3. Admissibility "N divides g" is not cell-invariant: for every field and every N some cell makes T_N admissible (a cell of index N/gcd(N,g)). (X1, X4)

1.3 What is cell-independent. The wavenumber RATIOS (primitive shape S0 = S/g), the polarisation data, and the commensurability class of the field's period in R_{>0}/Q_{>0}. T_N and every rational dilation preserve all three. Hence no cell-independent quantity of the field can see occurrence classes, admissibility, or histories. In free space every dilation E(alpha r, alpha t) is allowed, so nothing is selected.

1.4 Where it becomes intrinsic. When the lattice is physically fixed (a resonator, ring or crystal), g is the number of field periods in the physical cell and is a property of the pair (field, resonator). It is then invariant under change of basis of the cell lattice (GL3(Z); 2000 random unimodular changes, X3). So any UNNS-induced property must be formulated for (field, resonator), never for the field alone.

## 2. Maxwell dynamics (test 2): nesting adds nothing to the field equations, by symmetry

2.1 Intertwining. With D_alpha E(r,t) = E(alpha r, alpha t): U_tau D_alpha = D_alpha U_{alpha tau} for time evolution, T_a D_alpha = D_alpha T_{alpha a} for translations. The admissible sector of T_N is the set of fields invariant under translations by (cell)/N, a symmetry-defined (hence intrinsic) subspace; D_{r_N} maps it onto the fields invariant under translations by (cell)/(N+1)^2. So, representation-free, nesting is a REFINEMENT OF TRANSLATION SYMMETRY by the factor r_N. (X2 shows g scaling.)

2.2 Because D_alpha is a symmetry of the vacuum equations, every Maxwell quantity transforms by a scaling weight and no relation changes: amplitudes of E and B, polarisation, helicity label, propagation direction, constraints, pointwise energy density and Poynting vector are unchanged; frequency and wavenumber are multiplied by alpha; mode action and integrated helicity are divided by alpha (v001 Thm 3.1, v002 N7). Nesting therefore cannot reorganise E–B relationships or create a new field-level quantity. This is the precise reason the construction has so far produced label arithmetic: scale symmetry carries no structural information about Maxwell's dynamics.

2.3 Where Maxwell can answer. Only where scale symmetry is broken.
- Walls: conducting boundaries restrict to rational isotropic dilations (v002 N6).
- Dispersion: D_alpha maps a mode to a mode iff omega(alpha k) = alpha omega(k) (refractive index constant under the dilation). For a Lorentz medium in a 1-D ring (c=1, L=2 pi, w0=5, Omega=2, lower branch) the frequency defect delta_N(n) = omega_{r_N n}/(r_N omega_n) − 1 is −0.058 (N=1,n=1), −0.350 (N=1,n=2), −0.415 (N=2,n=2), −0.684 (N=2,n=4), −0.657 (N=3,n=3), −0.791 (N=3,n=6), and exactly 0 in vacuum. (X5) The defect is an observable of a fixed resonator (a ratio of two eigenfrequencies) and is representation-independent. Control: it measures departure of the medium from scale invariance for ANY integer pair; UNNS supplies which pairs (n, r_N n), but the defect itself is ordinary dispersion physics.
- Sources and nonlinearity: not studied.

## 3. Physical discrimination (test 3): partial, and number-theoretic

3.1 Polarisation. Same harmonic index, different polarisation: identical nesting structure, and D preserves the polarisation state, so nesting does not discriminate them. (Argument; not separately computed. It extends to any constant-coefficient anisotropic medium, where D remains a symmetry.)

3.2 Degeneracy of the target eigenspace (cubic torus). Maxwell's eigenspace at a given frequency has dimension 2 r3(s) (r3 = lattice points on the sphere |m|^2 = s). Facts, verified (X6, lattice enumeration to |m| <= 40):
- r3(4n) = r3(n) for all n (x^2+y^2+z^2 = 0 mod 4 forces all entries even). Hence T_1 (x4) maps a shell onto its target shell exactly: accessible fraction 1.
- For N = 2 (m = 2m' goes to 9m', norm 81 t): the image of the shell of norm t is a proper part of the target shell: t=1: 6 of 102 modes (1 octahedral orbit of the 4 present, fraction 0.059); t=2: 12 of 108 (fraction 0.111); t=3: 8 of 104 (0.077); more in the JSON. r3(81) = 102 agrees with the standard recurrence.
- The image is a union of cube-symmetry orbits (D commutes with rotations), hence a symmetry-invariant subspace of a larger degenerate eigenspace whose other orbits are accidentally degenerate with it.
Reading: nesting reaches only a fraction of what Maxwell's spectrum places at the target frequency, and the unreached part is physically degenerate with the reached part. This distinguishes electromagnetic configurations that the 1-D index cannot, but it is lattice-point arithmetic (spectral geometry of the cube), not a property of Maxwell's differential equations, and the cube symmetry already explains the orbit structure.

## 4. Answer to the central question

- Free periodic fields: nesting-induced structure (g, occurrence class, admissibility, histories) is representation-dependent. The only intrinsic content is the commensurability class and the primitive shape, on which T_N acts trivially.
- Fixed resonators: the structure is intrinsic to (field, resonator), and equals a refinement of translation symmetry by r_N. It still adds no field-level relation, because the map is a Maxwell symmetry.
- Maxwell-specific content appears only through symmetry breaking (walls, dispersion), where it is a defect from scale invariance rather than a UNNS effect.
- v001/v002 control: the enabling example is generic. For the 3^(-1/3) carry at state 2, T_2 enables the carry (2 -> 9) and so does plain multiplication by 3, 6, 9, 12 or 3/2; any multiplier that raises the 3-adic valuation works. (X7) The restricted-carry results of v002 concern lattice arithmetic and boundary geometry.

## 5. Candidate directions (not started)

A. Fixed non-scale-invariant resonators: take real spectra {omega_i} (rectangular waveguide cutoffs, spherical cavities, dispersive ring) and ask which pairs have ratios exactly r_N; compare with a null model. The torus gives all pairs by construction, so the discriminating cases are the others.
B. Induce structure on configurations of the resonator itself (dimension ratios, index ratios) instead of on mode labels, so that the cell is part of the data and the representation problem disappears.
C. Symmetry-breaking observables: how the dispersion defect delta_N depends on N and n for several media; whether any exact vanishing occurs beyond homogeneous dispersion.
D. Sources and nonlinear mixing: whether T_N-related index triples (n, (N+2)n, n/N) have a role in three-wave resonance conditions. Speculative; needs a model.

## 6. Limits
- Section 3.1 is an argument, not a computation. 3.2 is classical lattice-point counting; octahedral irreducible decomposition not computed.
- X5 is one medium and one branch.
- No coupling or physical process is claimed.
