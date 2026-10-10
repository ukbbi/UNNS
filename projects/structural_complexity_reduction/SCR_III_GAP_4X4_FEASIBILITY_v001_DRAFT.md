# SCR_III_GAP_4X4_FEASIBILITY_v001 — Outcome-Blind Solver Feasibility Protocol (DRAFT, UNFROZEN)

**Date:** 2026-10-10 · **Status:** design only; nothing has been run. Companion to `SCR_III_GAP_4X4_v001_DRAFT.md`. This protocol is frozen and executed **before** the gap protocol's interval is locked, and it never touches a real 4×4 energy. Items marked ◇ need Igor's decision.

## 1. Question
Can ground energy E0 and the minimum ice-rule-violating energy Δ_nonG be **certified** for n = 40 spins within 30 minutes and 2 GiB per arm, on instances that are statistically comparable to the real 4×4 problem but reveal nothing about it?

## 2. Constraint found in the frozen code
The v009 grammar masks are 32-bit (`vector<u32> IM, NM`; `(u32)s` in the grammar check) and there is no guard for n > 32. At n = 40 they would silently truncate. The frozen binaries are therefore **not to be used for n > 32**, and cannot be edited. A new solver (v010) with 64-bit masks and an explicit refusal for unsupported n is required, with its own implementation gate (§4) before any n = 40 run. Old frozen files stay untouched.

## 3. Instances (synthetic only)
- Geometry-derived parts only: the real 4×4 incidence (grammar masks) and the magnitudes |K_ij| from the frozen geometry. **Signs are generated, never taken from the real Hamiltonian.**
- Family S (random signs, iid ±): conservative, likely harder than the real ordered dipolar problem. Family P (planted ground state: K_ij = −|K_ij| s*_i s*_j, frustration-free, ground energy −Σ|K| known exactly): easier, gives an independent correctness check on E0. Real difficulty is expected between the two; a failure on S is not proof of infeasibility, a pass on P is not proof of feasibility.
- Size ladder n = 24, 28, 32, 36, 40 built from sub-lattices with the same construction. Seeds from master 20261010 with family labels `FEAS_S`, `FEAS_P`; count per (family, n) ◇ (suggest 10).
- Before building, register the real 4×4 instance fingerprint in the protected list; the guard must refuse any energy, E0 or gap request on it until separate authorization.

## 4. Gates (all before any n = 40 timing is interpreted)
1. **Implementation gate.** New solver reproduces frozen v009 results exactly at n ≤ 24 (public 1×1, 2×2; 3×3 at W = 0 only; synthetic instances including Δ_nonG) and returns an explicit error for unsupported n.
2. **Correctness gate.** At n = 28 and 32, certified E0 and Δ_nonG equal an independent brute-force (Gray-code) scan on the same synthetic instances; planted instances reproduce the known E0 exactly at all n.
3. **Feasibility gate.** At n = 40, on at least a pre-set fraction ◇ of instances per family, both certificates (E0, and Δ_nonG per constrained vertex or with a violation flag) complete within 30 min and 2 GiB per arm. Record wall time, nodes, bound evaluations, RSS, failures.

## 5. Outcomes
- **FEASIBLE:** all gates pass; the gap protocol may be frozen with certified computation.
- **PARTIAL:** correct but over budget on part of the ladder; report the scaling and what budget or algorithm would be needed. No silent loosening of the certification requirement.
- **INFEASIBLE_AS_SPECIFIED:** reported as such; the gap protocol then needs a bounds-only (interval) variant decided before any real computation.
Every failure, timeout and discarded instance is logged. The feasibility run informs only solver design, never the prediction interval.

## 6. Decisions needed ◇
Instances per cell; pass fraction; whether the new solver is built under a new version label (suggest v010) and gated by this protocol; whether family P counts toward the feasibility gate or only the correctness gate; approval to extend the guard fingerprint list.
