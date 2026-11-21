# MUG-I v002 — Maxwell Boundary Geometry and Restricted Carry Admissibility (research notes)

Status: research release; proof records, not a manuscript. Builds on MUG-I v001 (frozen) and the two reference records (Algebraic/Topological Extensions v1.1; Torsion-Class Carry Dynamics v1.0).
Verification: `verification/verify_v002.py` (9 checks, all pass; sympy; full run about 6 minutes). Results: `results/verification_results.json`.

## 0. Corrections to v001 (scope, not integrity)

C1. v001 Sect. 5 said a map R E(αR⁻¹r, αt) sends lattice modes to lattice modes "iff M = αR ∈ GL_D(Q)". Correct statement:
- Whole lattice into itself iff M is an INTEGER matrix.
- For a rational similarity M, the admissible modes are Λ_M = {m ∈ Z^D : Mm ∈ Z^D}, a sublattice of finite index. Example: M = (1−i)/2 has Λ_M = {m_x + m_y even}, index 2 (this is the inverse √2 carry); M = I/2 is a rational similarity that is not whole-lattice. (W1)
- v001 Thm 5.1 classifies rational similarities, i.e. the possible M for a restricted carry with a full-rank support; Cor 5.2 (3-torus) is a statement about WHOLE-lattice carries only.

C2. v001 Cor 5.2 added that a carry between classes "must connect different cavities or involve additional structure". That is overstated. Single modes and rays admit restricted carries on the 3-torus (Sect. 1 below).

C3. Helicity. The helicity LABEL (±, circular polarisation handedness) is preserved. The integrated optical helicity H of a circular wave is ∓𝓔/ω and is DIVIDED by α under the dilation, exactly like the mode action. (W7: symbolic, both handedness.) v001 should be read this way.

## 1. Ray carries on the 3-torus (field level, restricted)

Setting: cubic 3-torus, mode m = g·u, field map E'(r,t) = R E(αR⁻¹r, αt), α² = ρ ∈ Q_{>0}.

R1. (Ray carry.) The ray {g·u} is carried by √ρ into an integer ray iff w₀ ∈ Q³ with |w₀|² = ρ|u|² exists, iff sf(ρ|u|²) is not ≡ 7 (mod 8) (Legendre; Davenport–Cassels for I₃ makes rational targets integral when ρ|u|² is an integer). Then every g·u goes to g·w₀ with R any rotation taking u/|u| to w₀/|w₀|. The class [√sf(ρσ)] is the target class, so the ray-level obstruction is exactly "target class unrealised" (Table of v001, σ ≡ 7 mod 8). (W2: 3640 cases, integer targets.)
R2. Explicit instance (W3): α = √3, e₁ → (1,1,1), R the Rodrigues rotation with R e₁ = (1,1,1)/√3. The transported wave is an exact vacuum solution, transverse to (1,1,1), periodic on L in x, y, z (symbolic residuals zero).
R3. Gauge freedom: R is determined only up to rotation about the target axis, so the transported polarisation state is defined up to a phase angle; the helicity label is unaffected. Out-degree: the number of admissible targets from a ray is the number of lattice vectors of norm ρ|u|² (up to the symmetry used), so carries are BRANCHING on the 3-torus, unlike the single-valued Gaussian carry in the plane. Counting statement only; its dynamical meaning is open.

## 2. Support-rank profile

For a field whose Fourier support spans a rank-k sublattice with Gram form Q, a restricted carry by α into the torus exists iff α²Q embeds isometrically in (Q³, I₃).
- k = 1: sf(ρ|u|²) not ≡ 7 (8) [R1].
- k = 2, Q = I₂ (support {e₁,e₂}): iff ρ is a sum of two squares. Proof: Witt cancellation, ρ⟨1,1⟩ ⊥ ⟨1⟩ ≅ ⟨1,1,1⟩ ⇔ ρ⟨1,1⟩ ≅ ⟨1,1⟩ ⇔ ρ a norm from Q(i). (W4, brute force ρ ≤ 40 agrees for ranks 1, 2, 3.)
- k = 2, general Q: decided by Hasse invariants of ⟨d₁, d₂, d₁d₂⟩ at all p (Hilbert symbols). Implemented; 249 random cases agree with exhaustive integer search, and integral success never contradicts the test (soundness). (W5)
- k = 3: iff α is rational (v001 Thm 5.1(a)).
Consequence: α = √3 carries the ray e₁ → (1,1,1) but NOT the pair {e₁,e₂} (the only norm-3 vectors are (±1,±1,±1), whose mutual dot products are odd), and not the whole lattice. Whether a field can be carried therefore depends on the SHAPE of its Fourier support, not only on its content g.

## 3. Conducting walls

R4. (Necessity.) Let a perfectly conducting rectangular box have its eigenmode with Fourier support the sign orbit S(m) = {(±m₁,±m₂,±m₃)} (the full orbit, or the sub-orbit when some m_i = 0). If M = αR maps S(m) onto the support S(w) of another box eigenmode, M carries the polytope conv S(m) onto conv S(w) and so edges to edges. The edges of S(w) point along coordinate axes, so R permutes the coordinate axes up to sign, hence α m_i = ± w_j integer, hence α ∈ Q. Therefore NO irrational carry maps a box mode to a box mode (maps fixing the box and its origin); in the box only rational isotropic dilations act. Instance (W6): 45° rotation with √2 on the TM_z mode E_z = sin(3πx/a) sin(3πy/a) of a square box gives E_z' = ½(1 − cos(6πy/a)) at x = 0, violating E_z = 0. No irrational carry hit in the exhaustive orbit comparison (W6b, m ∈ {0..4}³, ρ ∈ {2,3,5}).
R5. Reading: the restricted ray carries of Sect. 1 are a property of periodic (translation-invariant) geometry; conducting walls remove them. The torus and the box give genuinely different carry geometries for the same unchanged UNNS law.

## 4. Classification summary (induced vs ordinary)

| Carry type | Periodic torus | Conducting box |
|---|---|---|
| Rational isotropic dilation (T_N, rational c) | acts, admissible iff content divisible | acts, admissible iff α(m,n,p) integral |
| Irrational whole-lattice carry | none for D odd; D=2 iff ρ = sum of two squares | none |
| Irrational restricted carry, rank 1 (ray) | exists iff target class realised; branching, polarisation gauge | none |
| Irrational restricted carry, rank 2 | iff α²Q embeds in I₃ (Hilbert-symbol test) | none |
| Irrational restricted carry, rank 3 | none | none |

Ordinary Maxwell symmetry accounts for all individual maps; what is not ordinary is the SELECTION: which support shapes survive which carry, and the box/torus contrast.

## 5. Limitations

- R1 for non-integer ρ|u|² relies on Davenport–Cassels (cited, not re-proved here).
- R4 is a necessity argument for maps fixing the box and its origin; translations/other boundary shapes not treated. Verified as an instance and by orbit-Gram exhaustive search, not by a mechanised proof.
- W5 is a random sample, not exhaustive; supports of rank 2 only.
- No coupled dynamics with T_N is analysed in this release (ray carries and T_N act on different data: T_N on content g, carries on direction u). Whether their combination produces new reachability is open.
- Vacuum, nondispersive, source-free only. FUG-I v005 records not yet compared.

## 6. Open questions for v003

1. The ray-level carry graph on directions (vertices: primitive u up to the cube symmetry; edges: carries √ρ): connectivity, branching and in-degree; relation to T_N on content (product structure content × direction).
2. Does restricted admissibility of a carry on a rank-2 support interact with enabling by T_N? (T_N changes g only, so supports of rank ≥ 2 keep their shape; probably no, to be shown.)
3. Cylindrical or circular-waveguide boundaries, where rotations are symmetries: do restricted carries survive?
4. Dispersion.
5. Comparison with FUG-I v005 history invariants.
