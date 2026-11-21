# MUG-I v005 — The induced structure G_U(Maxwell; φ) for one fixed system

Research notes. No manuscript. Redirect from the v004 review: stop testing single correspondences; give a precise
definition of G_U(Maxwell; φ) for one explicit electromagnetic system, then read off its invariants.
Results file sha256: 8866c1cf…  (verification/verify_v005.py, all of Z1–Z7 pass, ~20 s, needs mpmath).

## 1. The fixed system A = 𝔐_p
- Geometry: 3-torus ℝ³/(2πℤ)³, c = 1, so a wave vector is an integer vector m ∈ ℤ³∖{0}.
- Medium: cold electron plasma in the infinite-magnetisation limit, B0 ∥ z: ε = diag(1, 1, 1 − p/ω²), μ = 1.
  p = (ω_p L/2π)² is the only parameter. Medium and cell enter only through p.
- Solutions: on-shell modes (m, b). With s = |m|², z = m_z², Φ = ω²:
  - b = O (E ⊥ z, E ⊥ k): Φ = s.
  - b = E±: roots of Φ² − (s+p)Φ + zp = 0. E− exists iff z ≠ 0 (otherwise its root is the static Φ = 0).
  - Field data (E-direction, longitudinal fraction |k̂·Ê|², |B|/|E|) come from the null vector of ω²ε − (|k|²I − kkᵀ).
- Vacuum control: p = 0 (every branch scale-covariant).

## 2. The induction rules (kept separate, per the PDF §4)
- **R-transport (primary).** Vertices: modes (m, b). Edges: (m,b) →_N (r_N m, b), r_N = (N+1)²/N, admissible iff N | content(m).
  The branch label is carried, the target is the on-shell mode of the same branch at r_N m. Edge labels: N, the defect
  Δ = Φ_b(r_N m) − r_N² Φ_b(m), and the field data at both ends. This is φ(m,b) = m lifted to the substrate occurrence g = content(m) along direction u = m/g.
- **R-restriction.** Observed states = shell integers |m|² ∈ S₃ (non-excluded by Legendre). Edges = T_N restricted to S₃.
- **R-ordered vs R-analytic labelling.** Branch identity by ordering (E+ upper root) or by analytic continuation.
Different rules give different graphs (below). None is declared universal.

## 3. Structure of G (R-transport)
**S1. Product form.** Edges never change u or b. So G = ⊔_{(u,b)} U, one copy of the substrate graph per (primitive direction, branch). All Maxwell content sits in labels on this product, not in its connectivity. (Z2a; truncated component counts in Z2b are a cutoff artefact.)

**S2. Sector census.** Per primitive direction u: branches O and E+ always, E− iff u_z ≠ 0. Vacuum: 2 light-cone polarisations per u. For |u|² ≤ 30: 313 directions, 907 plasma sectors vs 626 vacuum sectors (Z7). The medium creates a third sector, the plasma-oscillation branch, which does not exist in vacuum.

**S3. Potential.** Θ_b(g,u) = Φ_b(gu)/g² = v_ph²·|u|². For every edge g → g′:
Δ/g′² = Θ(g′) − Θ(g)  (Z1a, residual ≤ 1e-60 over 35 358 edges).
So the "correct weighting" in the v004 endpoint statement is division by the target wavenumber squared. Along any path
Σ Δ_i (g_f/g_i′)² = Φ(g_f u) − (g_f/g_0)² Φ(g_0 u) (Z1b). The defect field is exact on every sector.

**S4. Sign and Lyapunov character (new).** With q = p/g²: Θ_±′(q) = ±(Θ_± − z)/√D, and z lies between the roots (z(z−s) ≤ 0), Θ_+ ≥ max(s,z), Θ_− ≤ z. Hence both Θ_± are non-increasing in g. Every forward edge has r_N ≥ 4, so g strictly increases; therefore **forward edges never increase Θ** and strictly decrease it off the axis (u not ∥ z) (Z3a,b over 355 116 edges, p = 36, 2, 7).
Interpretation: UNNS forward flow drives each branch monotonically toward its scale-covariant asymptote:
Θ_O ≡ s; Θ_+ → s (light cone, from above: phase velocity ≥ c); Θ_− → 0 with Φ_− → p z/s (the resonance cone ω = ω_p cosθ).
The vacuum control has Θ ≡ const: zero defect, the flat case. The potential is the structure that the medium adds to the product graph.

**S5. Mergers.** Distinct histories to the same endpoint have identical final mode, identical field data and identical total weighted defect (S3). They differ only in intermediate vertices, lengths and Θ-profiles: for p=36, u=(1,1,1), 6 → 3600 there are 17 histories of lengths 3 and 4 with 17 distinct profiles (Z5a). In the linear lossless medium a merger therefore carries no field-level information beyond the endpoint; only the combinatorial/dispersion trace differs. A history-sensitive field relation would need memory or nonlinearity (not studied).

**S6. Branch crossing on the axis; labelling is part of the induction rule.** For u = e_z the two roots are Θ_T = 1 (transverse, vacuum-like, zero defect) and Θ_L = p/g² (Langmuir). They cross at g = √p. Ordered labels (E+/E−) are max/min of these (Z3c); off the axis the branches never touch (D > (s−q)² ≥ 0, Z4b).
Forward edges that jump the crossing carry a defect that matches neither analytic branch: p=36: edge g=2→8 (N=1), ordered-upper defect −512, T-defect 0, L-defect −540 (9 such edges for g < 400); p=2: edge 1→4, −16 vs 0 and −30 (Z4).
So the ordered-label graph and the analytic-label graph are different induced structures; they coincide off the axis. The analytic labelling is the physically meaningful one (it splits the axis into a defect-free T-sector and a defect-carrying L-sector).

**S7. Field relations along a fibre (observation, 8 sample points per sector, p = 36).** Along a fixed (u,b), longitudinal fraction and |B|/|E| vary with g; the vacuum control is constant (Z5d). E+ → transverse (longitudinal fraction → 0, |B|/|E| → 1); E− → electrostatic (longitudinal fraction → 1, |B|/|E| → 0, ~1/g); O is constant. On the axis the same quantities jump at the crossing. Monotonicity in g is seen in the table, not proved.

**S8. Alternative rules.**
- Restriction to S₃ (cutoff 4000): 3335 vertices, 1963 of the 2491 full-graph edges survive on the induced vertex set. This is a different graph from G (no direction or branch structure at all).
- Non-commutation: for the vector lift, |r_N m|² = r_N²|m|² while T_N(|m|²) = r_N|m|². The shell map does not intertwine the two actions; the vector lift induces x → x r_N² (N² | x) on shells. No N ≤ 10⁶ has r_N² = r_M for a single step M (equivalent to (N²+1)(N²+4N+1) never a square; searched, not proved) (Z6b,c).

## 4. What is inherited, imposed, joint
- Inherited from Maxwell: branch set, field data, Φ_b, the crossing.
- Inherited from UNNS: product form S1, the multiplier set r_N, forward monotone g, admissibility N | content, mergers as multiplicative histories.
- Joint (neither alone): Θ as a monotone potential on the product graph (S3–S4), the sector census (S2), and the ordered-vs-analytic dichotomy (S6) — these need both the graph and the dispersion.

## 5. Limits and open questions
- One fixed system (infinite-magnetisation limit). Finite Ω (Appleton–Hartree, oblique) not done.
- Boundaries: only through the cell datum (p). Walls/waveguides (v002 restriction + dispersion) not done.
- Z2b component counts are truncation artefacts; one fibre component rests on the arithmetic-dynamics result.
- Monotonicity of field data (S7) and r_N² ≠ r_M (S8) are numerical.
- FUG-I v005 comparison still not done (records not read).
