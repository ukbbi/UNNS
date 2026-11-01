# E2-P2 — Definitions (scope-locked; inherits E2-P1/DEFINITIONS.md and GEO-I v002–v004)

Scope: FIELD-I collective map C only (never SELECT-II). Same notation as E2-P1.

* **State** x = a/b (lowest terms). **D(x)** = {d ≥ 2 : d² | a, d ≡ 1 (mod b)}; **L** = lcm D, **G** = gcd{d−1}; **C(x) = x + L²/G**.
* **Coordinates** (P, q): P = primes p with p² | a, q_i = ⌊v_{p_i}(a)/2⌋ ≥ 1. A **transition x → x′ = C(x) is admissible** iff (P, q) is the same for x and x′ (other primes may divide a′ only to the first power).
* **Relation lattice** Λ_b = ker χ_b ⊂ Z^k, χ_b(α) = ∏ p_i^{α_i} mod b — the *infinite* lattice (E2-P1 compared it only inside a box; here inclusion is decided on Z^k by P2-T1).
* **Classes** EQUAL (Λ = Λ′), ENLARGE (Λ ⊊ Λ′), SHRINK (Λ′ ⊊ Λ), INCOMPARABLE. **Non-trivial** means Λ ≠ Z^k.
* **Fibre** F = (Λ ∩ [0,q]) ∖ {0}; **region Graver set** G_q(Λ) = ⊑-minimal nonzero vectors of Λ ∩ [−q,q]; **oriented** = lex-positive representatives.
* **Cells/complex K_abs**, **union U**, **PRESERVED/LOST/NEW**, **CONTAINED/PARTIAL** exactly as in E2-P1 §3–4, with the **general survival rule (E2-P1 Addendum 002)**: c ∈ K′ ⇔ V(c) ⊆ F′ ∧ Gen(c) ⊆ G_q(Λ′).
* **Generator survival** g ∈ G_q(Λ) survives iff g ∈ G_q(Λ′).
* **Order rule** (P2-L2): for the target moduli, n_i := ord_{b′}(p_i) (the least n with p_i^n ≡ 1 mod b′).
* **Coupled** lattice (k ≥ 3): Λ is not a direct sum along any coordinate partition; used for P2-T5.
* **Planar geometry** (k = 2): exact rational sampling of the line arrangement of all cell edges (see `src/cell_transport.py`); topology of U by the nerve of its cells (nerve theorem), Betti numbers over Q-equivalent rank (builder) and GF(2), GF(3), GF(2³¹−1) (audit).

## Gates (spec §11)
EXACT_PASS · THEOREM_PASS (SCOPED) · C3_CANDIDATE · COUNTEREXAMPLE · OPEN · UNAVAILABLE · NOT_RERUN — used exactly as in the specification. EXACT_PASS never implies a theorem verdict.
