# GEO-I v001 — Finite Fibre Geometry and Modular Boundaries

*Research note, not a manuscript. Separate active project; the published `UNNS_MATH_FOUNDATIONS` materials are unchanged (GitHub read-only, commit `fefa7910c807a5fdac90980749a5d7993e3ec0ca`).*
*Verifier: `code/geo1_verify.py` — 24/24 checks PASS (exact integer/rational arithmetic).*

Scope tags follow Volumes I–II: **A0** occurrence arithmetic, **A2** SELECT-II, **C** collective map. Status labels: **PROVED** (proof given here), **CHECKED** (exact finite computation, range stated), **COROLLARY** (follows from a cited Volume result plus a proof here), **OPEN**.

---

## 0. Summary

1. The rational fibre is a **sublattice cut of an integer box**: `F(a/b) ∪ {0} = Box(a) ∩ ker χ_b`, where `χ_b: Z^k → (Z/b)^×` is a group homomorphism. Integer fibres are full boxes (b = 1). (A0, PROVED.)
2. The box is closed under **addition** of coordinates (products of indices), but not under coordinatewise **min/max** (gcd/lcm). `x = 2304/5` is the smallest clean example: `D = {6, 16}`, `lcm = 48` is a hole. (A0, PROVED + CHECKED.)
3. For `b > 1`, two fibre points differing by a unit step `e_i` exist only if `p_i ≡ 1 (mod b)`; the grid graph of a rational fibre is therefore generically edgeless, so connectedness (GEO-T1) must be defined by lattice moves in `ker χ_b`. (PROVED.)
4. **SELECT-II is a translation system on the valuation lattice**: `v(m') = v(m) − v(N) + 2 v(N+1)`, enabled iff `v(N) ≤ v(m)`. It is a *pure Petri net* with transition `t_N` (pre `v(N)`, post `2v(N+1)`). (A2, PROVED + CHECKED on all 43,376 edges of 1..5000.)
5. The displacement vectors `Δ(1..K)` have rank exactly `π(K+1)`, so there are `K − π(K+1)` independent multiplicative relations. These relations **are** the source of path multiplicity: the non-graded pair `6 → 784` is the relation `2Δ(1)+Δ(6) = Δ(2)+Δ(27)`. Equal-length relations also exist (`{1,1,14}` vs `{2,4,7}`). (PROVED rank; CHECKED examples.)
6. **Layer-count law (new, COROLLARY of T51 + T61).** Along the eventual regime `x_{n+P} = p^{2s} x_n`, the fibre size obeys `R(x_{n+mP}) + 1 = Σ_{j=0}^{h+ms} c(j)` with `c` periodic of period `o = ord_b(p)`. Hence `R` is exactly linear when `b = 1` and **quasi-linear** otherwise, with mean slope `s·Q_p /(o·P)` per iteration. This links fibre geometry to the rate of evolution. (CHECKED at 176 phase points; only one orbit with b > 1 (the g = 11 benchmark, slope 1/4) was available — see §3.)

The geometry is not 3- or 4-dimensional by nature: its dimension is `k(x)` = number of primes with `⌊v_p/2⌋ ≥ 1`. 3600 has k = 3, 44100 has k = 4, 72 has k = 2.

---

## 1. Occurrence geometry (GEO-I.A)

**Occurrence surface.** `Z = Y(X+1)²/X` in coordinates `(N, M, S_N(M))`. For fixed `X` it is a line through the point `(X,0,0)` with direction `(0,1,(X+1)²/X)`, so the surface is a right conoid with axis the X-axis.

**Prop 1.1 (PROVED).** The slope `(N+1)²/N = N + 2 + 1/N` is strictly increasing in `N ≥ 1`, equals 4 at `N = 1` and exceeds 4 otherwise. So every SELECT-II edge multiplies by a factor ≥ 4, with equality exactly for `N = 1`, and the injectivity `N ↦ m(N+1)²/N` (no multi-edges) holds. *(Recovers the Vol. I acyclicity fact geometrically; CHECKED for N ≤ 10⁵.)*

**Prop 1.2 (fibre = level set, PROVED).** For integer `z`, the lattice points over level `z` are `{(d−1, z(d−1)/d²) : d ≥ 2, d² | z}`. Proof: `M(N+1)² = zN` and `gcd(N, N+1) = 1` force `(N+1)² | z`. CHECKED by brute force for z ≤ 1500. For 72: `(1,18), (2,16), (5,10)`.

**Def 1.3.** For reduced `x = a/b`, `a = ∏ p_i^{e_i}`, let `h_i = ⌊e_i/2⌋`, `Box(a) = ∏[0,h_i] ⊂ Z^k`, and `χ_b(α) = ∏ p_i^{α_i} mod b`. (Each `p_i | a` and `gcd(a,b) = 1`, so `p_i` is a unit mod `b`.)

**Thm 1.4 (rational-fibre lattice, A0, PROVED).** `D(x) ↔ (Box(a) ∩ ker χ_b) ∖ {0}`. The kernel is a sublattice of index `|⟨p_1,…,p_k⟩| ⊂ (Z/b)^×`. In particular:
 (i) b = 1: the fibre is the full box minus the origin, `R = ∏(h_i+1) − 1`, `L(x)` = top corner `∏p_i^{h_i}` (so `L²` = largest square divisor of `m`), and the fibre is closed under gcd and lcm.
 (ii) the fibre ∪ {0} is closed under coordinate addition whenever the sum stays in the box (i.e. `d, d' ∈ D ∪ {1}` and `(dd')² | a` imply `dd' ∈ D ∪ {1}`);
 (iii) `b | G(x)`.
*Proof.* Definition of `D` rewritten in coordinates; `χ_b` is a homomorphism, so its kernel is a subgroup; first isomorphism theorem for the index. (iii): every `d ≡ 1 (mod b)`, so `b | d − 1`. ∎
 CHECKED: integer fibres for m ≤ 20,000; 400 random rational boxes for (ii); fibre ≡ lattice description on the tails of all tested rational orbits.

**Benchmarks (exact, from `data/verify_run.json`).**

| x | primes, box side lengths | R | L | G | notes |
|---|---|---|---|---|---|
| 72 = 2³3² | (2,3), 2×2 | 3 | 6 | 1 | routes N = 1,2,5 ↔ unit-square vertices |
| 144 = 2⁴3² | (2,3), 3×2 | 5 | 12 | 1 | |
| 3600 = 2⁴3²5² | (2,3,5), 3×2×2 | 11 | 60 | 1 | 3D box (Fig. 1) |
| 44100 = 2²3²5²7² | (2,3,5,7), 2×2×2×2 | 15 | 210 | 1 | 4D box (Fig. 1) |
| 2304/5 | (2,3), 5×2, b = 5 | 2 | 48 | 5 | D = {6,16}; 48 ∉ D (Fig. 2) |

**Prop 1.5 (grid adjacency, PROVED).** If `α` and `α + e_i` both lie in `ker χ_b`, then `p_i ≡ 1 (mod b)`. So for `b > 1` and `p_i ≢ 1 (mod b)` the fibre has no grid-adjacent pairs along axis `i`. *Proof.* `χ_b(α + e_i) = χ_b(α)·p_i`. ∎
**GEO-T1 (OPEN, refined).** Define adjacency by a generating set of short vectors of `ker χ_b` (index-`|H|` lattice) and classify connectedness of `Box ∩ ker χ_b`; the 2304/5 hole shows min/max closure fails, so classification must use addition-only closure.

---

## 2. Route and reachability geometry (GEO-I.B)

**Thm 2.1 (SELECT-II as a translation system, A2, PROVED).** `v_p(m') = v_p(m) − v_p(N) + 2v_p(N+1)` for every prime `p`; the step is enabled iff `v(N) ≤ v(m)` coordinatewise. So SELECT-II is the reachability graph of a pure Petri net on places = primes with transitions `t_N` (consume `v(N)`, produce `2v(N+1)`; supports of pre/post are disjoint because `gcd(N,N+1)=1`). CHECKED on all 43,376 edges of 1..5000. From 6: `N = 1,2,3,6` give `24, 27, 32, 49` with displacements `(2,0,0), (−1,2,0), (4,−1,0), (−1,−1,2)` in `(v₂,v₃,v₇)` (Fig. 3).
*Caution.* The net has infinitely many transitions; classical finite-net theory (Karp–Miller 1969 coverability trees; Mayr 1984 decidability of reachability; Ackermann-completeness for finite nets, 2021) is a context, not a transferred result. Whether the structure is simpler than general nets is open.

**Thm 2.2 (relation lattice, PROVED).** For `K ≥ 1`, `rank(Δ(1),…,Δ(K)) = π(K+1)`. *Proof.* All vectors lie in the span of `e_p, p ≤ K+1` (so rank ≤ π(K+1)); for each prime `p ≤ K+1`, `Δ(p−1)` has coordinate `2` at `e_p` and zeros at primes > p (since `p−1 < p`), giving a triangular system of nonzero diagonal. ∎ The relation module of the `K` displacement vectors has rank `K − π(K+1)` (K = 10, 20, 40, 80, 120 give 5, 12, 27, 58, 90; CHECKED).

**Cor 2.3 (path multiplicity has a linear-algebraic source).** Distinct firing multisets with equal total displacement are exactly relations. Example (exact): `(4)(4)(49/6) = (9/2)(784/27)`, i.e. `2Δ(1)+Δ(6) = Δ(2)+Δ(27)`, giving the 6 → 784 paths with 3 edges (Parikh image `{1,1,6}`) and 2 edges (`{2,27}`) (Fig. 4). Consequently **no linear functional φ with φ(Δ(N)) = 1 for all N exists**, so the ungradedness of SELECT-II is not accidental to one pair. CHECKED: 19 (start, end) pairs in 1..2000 have ≥ 2 different Parikh images, 16 of them with different lengths. Equal-length relations also exist (`{1,1,14}` vs `{2,4,7}`, `{1,1,9}` vs `{3,3,4}`; CHECKED), so length alone does not identify the multiset.
**Vol. I reproduction (CHECKED).** 3,124 edges and 8,283 complete histories in 1..5000; 72 has predecessors 10, 16, 18 and four histories.

**History geometry.** Four histories of 72 projected into `(v₂,v₃,v₅)` (Fig. 3, right) are four distinct polylines with the same endpoint; `1→4→16→72` and `1→4→18→72` share a Parikh multiset `{1,1,2}` but differ as sequences — a state-space picture cannot distinguish them, a history-unfolded one can.

---

## 3. Evolution geometry (GEO-I.C)

**Two geometries.** SELECT-II is *translation-invariant in valuation space*. The collective map is *translation-invariant in the additive line*: `x = γL²/G`, `C(x) = (γ+1)L²/G` (γ increments by 1 on a plateau). In valuation space `C` is not a translation; it only becomes one **eventually** (T51).

**Thm 3.1 (eventual strands, COROLLARY of T51 + T61, C).** If `x_{n+P} = p^{2s} x_n` for `n ≥ n₀`, then `v(x_{n+P}) = v(x_n) + 2s e_p`: the eventual orbit is `P` parallel rays in valuation space with common direction `e_p`. For 72: `x_{n+3} = 4x_n`, three rays in the `(v₂,v₃)` plane with step `(+2,0)` (Fig. 5). CHECKED exactly on the tail windows of **375 integer orbits** (x₀ ≤ 1500, all in the G = 1, P = 3 regime) and **13 orbits from rational seeds** (P and ρ a prime power in every case). *Honest limit:* of these 13, only the g = 11 benchmark (P = 8, ρ = 3) stays at G > 1; the other 12 fall into the G = 1 regime (P = 3, ρ = 2), so the G > 1 evidence for Thm 3.1 and 3.2 is a single orbit plus the proof. The test could not decide 23 of 36 rational seeds within 220 steps / a 10 s factoring limit — reported as undetected, not as failures.

**Thm 3.2 (layer-count law, COROLLARY of T51 + T61, C, PROVED).** Let `x_{n+P} = p^{2s}x_n` hold from `n₀`, `x_n = a_n/b` (b is constant since `p | a_n`, so `p ∤ b`). Write `Box' = ∏_{q ≠ p}[0,h_q]` (unchanged along a phase) and `c(j) = #{t ∈ Box' : χ_b(t)·p^j ≡ 1 mod b}`. Then
`R(x_{n+mP}) + 1 = Σ_{j=0}^{h_p + ms} c(j)`, `c(j+o) = c(j)`, `o = ord_b(p)`.
Hence (a) `b = 1`: `c ≡ |Box'|`, so `R(x_{n+mP}) + 1 = |Box'|·(h_p + ms + 1)` exactly linear in `m`; (b) `b > 1`: `R` is quasi-linear in `m`, with mean slope per iteration `s·Q_p /(o·P)`, where `Q_p = #{t ∈ Box' : χ_b(t) ∈ ⟨p⟩}`.
*Proof.* Multiplication by `p^{2s}` raises `h_p` by `s` and fixes every `h_q`; slicing the box at `α_p = j` gives `c(j)`; periodicity is that of `p^j mod b`; each `t` with `χ_b(t) ∈ ⟨p⟩` contributes to exactly one residue class of `j`. ∎
*Example (g = 11, x₀ = 67500²/11, Vol. II F.T50).* `P = 8, ρ = 3 (p = 3, s = 1)`, `Box'` has sides `h₂ ∈ {2,3}` (phase-dependent), `h₅ = 4`, `o = 5`, `Q_p = 10`, `c(j) = 2` for all `j`, so `R(x_{n+8}) = R(x_n) + 2` and slope `1/4` — matches F.T50(iii) `R = 7 + 2k` (Fig. 6). CHECKED at 176 phase points (375 integer orbits for b = 1; one orbit with b > 1); more G > 1 orbits are the obvious next test. Vol. II already records linear growth of `R` in its examples; Thm 3.2 gives the exact form and the rate in terms of fibre geometry. *(Not yet cross-checked against the registry for overlap with a numbered theorem.)*

**Cor 3.3 (arithmetic dimension).** Along the eventual regime the dimension `k(x_n)` is eventually periodic with period dividing `P` (only axis `p` grows).

---

## 4. Conjectures and open problems (no claims beyond this)

* **GEO-T1** — classify connectedness of `Box ∩ ker χ_b` under lattice-move adjacency (§1); structure of "holes" = failures of min/max closure; define a defect invariant such as `[L(x) ∈ D(x)]`.
* **GEO-T3** — characterize which relation classes of the displacement lattice give genuinely different history *shapes*, not just different Parikh images; density of ambiguous pairs.
* **GEO-T4** — does the transient geometry (χ_b, `o`, `Q_p`) determine the eventual `(P, s, p)` before iterating? Thm 3.2 shows the growth rate is determined *by* them once `(P, s, p)` is known; the converse is open.
* **Question for O12.2.** At composite/even `g`, `(Z/g)^×` is not cyclic (e.g. g = 15, 68). Whether the S5 failure is related to this group structure of `χ_g` is **untested**; no claim is made.
* **GEO-T2/T5** — not attempted in v001.

## 5. Relation to existing mathematics
Prime valuations, lattice kernels of characters, Petri-net/vector-addition systems and path-space (Bratteli-type) constructions are standard tools; v001 claims no priority for them. The candidate novelty is only in the **specific consequences** for the UNNS rules (Thms 1.4, 2.1–2.2, 3.2). Square-divisor counting is classical (OEIS A046951). References quoted from memory and not re-verified in this session: R. M. Karp, R. E. Miller, *Parallel program schemata*, J. Comput. System Sci. 3 (1969); E. W. Mayr, *An algorithm for the general Petri net reachability problem*, SIAM J. Comput. 13 (1984); J. H. Silverman, *The Arithmetic of Dynamical Systems*, Springer 2007.

## 6. Source links (pinned to the frozen commit `fefa7910c807a5fdac90980749a5d7993e3ec0ca`)
* Vol. I: https://github.com/ukbbi/UNNS/tree/fefa7910c807a5fdac90980749a5d7993e3ec0ca/projects/UNNS_MATH_FOUNDATIONS/Manuscript/UNNS_Math_Foundations_Vol_I
* Vol. II: https://github.com/ukbbi/UNNS/tree/fefa7910c807a5fdac90980749a5d7993e3ec0ca/projects/UNNS_MATH_FOUNDATIONS/Manuscript/UNNS_Math_Foundations_Vol_II
* Records used: F.T1 (rational fibre), F.T50 (g = 11 orbit), T51/T61 (scaling, ρ = p^s), FIELD-I v012 sources under `projects/UNNS_MATH_FOUNDATIONS/sources/FIELD-I/v012`.
