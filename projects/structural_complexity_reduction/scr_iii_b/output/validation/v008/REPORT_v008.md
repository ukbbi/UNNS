# REPORT_v008 — Solver Implementation Gate (outcome-blind)

**Verdict:** `SOLVER_IMPLEMENTATION_GATE_PASS`

Implementation verdict only. It implies nothing about H-G, H-P, H-T or H-C primary success. No G_net, no 3×3 W>0 outcome, specification and preregistration remain unfrozen.

## What passed

- **F1** frozen v005–v007 untouched; **G0** the binary refuses 3×3 W>0 without the post-freeze flag; **S8** audit: 3×3 was run only at the published W=0 anchor.
- **S1** B0=B1 (exact target set) and G1=G2 (S_T∩S_G) on 1×1 and 2×2 at W=0, every level threshold, 10τ below it and every midpoint; false-exclusion counts equal v006.
- **S2** same equivalence on synthetic instances (random mixed-sign couplings and incidence, ferromagnet, antiferromagnet, all-degenerate).
- **S3** B1 lower bound is admissible on 530 partial assignments and equals an independent python formula.
- **S4** 3×3 W=0 dry run: all four solvers return the same two (complementary) ground states; E0 equals the v007 anchor; outputs and operation counts deterministic over repeats.
- **S6** candidate tie policy is conservative on synthetic near-ties (**proposed for testing only, not frozen**). **S7** Δ_G and ρ_G verified on public 1×1/2×2: ρ<1 ⇔ FN=0.

## Public-patch gap diagnostics and the thermal window

| Patch | Δ_G (J) | Δ_G / k_BT | ρ_G for W = k_BT | classification |
|---|---|---|---|---|
| 1x1 | 9.529e-21 | 0.871 | 1.15 | FAIL_AT_OR_ABOVE_GAP |
| 2x2 | 1.041e-20 | 0.952 | 1.05 | FAIL_AT_OR_ABOVE_GAP |

W = k_BT lies above both known gaps. 3×3 preservation failure is a genuine possibility and the window must not be altered to avoid it.

## Cost ledger (3×3, W=0 only; single thread; median of 5)

| Solver | wall (s) | spread | nodes / states | pair ops | grammar checks | full energy evals | peak RSS (MB) |
|---|---|---|---|---|---|---|---|
| B0 | 0.1465 | 1% | 16777216 | 402653436 | 0 | 1 | 26.6 |
| G1 | 0.08586 | 2% | 16777216 | 718704 | 16777216 | 2604 | 26.6 |
| G2 | 0.0002613 | 1% | 25786 | 103260 | 0 | 0 | 26.6 |
| B1 | 7.06e-05 | 6% | 4232 | 59210 | 0 | 0 | 26.6 |

Phase timers are exclusive only where the algorithm separates the phases (G1: scan vs energy). In B0, G2 and B1 energy updates are intertwined with traversal, so their energy cost is reported as pair_ops/field_updates, not as a separate wall time. maxrss is per process and includes ~1-2 MB runtime baseline.

## Observations (not conclusions)

- W=0 dry run on 3x3: B1 visited 4232 nodes and G2 25786 nodes (B0 visited 16777216 states); wall medians B0 0.146 s, G1 0.0859 s, G2 0.000261 s, B1 7.06e-05 s.
- At W=0 the exact branch-and-bound sensitivity comparator B1 is FASTER than constructive grammar generation G2. This is a W=0 observation only (a very restrictive target); it must not be generalised to W>0, but it shows that the C axis against B1 is not guaranteed and must be reported honestly.
- Neither G_net nor any speedup headline is derived from these figures; they are acceptance-only component measurements.

## Test table

| ID | Test | Status |
|---|---|---|
| F1 | Frozen v005, v006, v007 code/outputs equal the hashes in their local manifests (read-only) | **PASS** |
| G0 | Outcome-blind guard: the binary refuses any 3x3 (n>16) run with W>0 unless --unblind-after-freeze is given, and prints no result | **PASS** |
| S1 | Solver equivalence on public 1x1 and 2x2 patches at W=0, every level threshold, 10*tau below it, and every midpoint: B0=B1=exact brute-force target set; G1=G2=S_T∩S_G (E0-hat over S_G); false-exclusion counts equal v006 | **PASS** |
| S2 | Solver equivalence on 33 synthetic instances (random mixed-sign couplings, random 2-in/2-out-style incidence, ferromagnet, antiferromagnet, all-degenerate zero coupling), 5 windows each | **PASS** |
| S3 | B1 lower bound is admissible: C++ LB <= exact minimum completion energy for 530 partial assignments (synthetic, real 2x2, real 3x3 depth 14-20); C++ LB equals independent python formula | **PASS** |
| S4 | 3x3 acceptance-only dry run at the published W=0 anchor only: B0=B1=G1=G2 return the same 2 ground states (complementary pair, both grammar-admissible), E0 equals the v007 anchor within 1e-12, deterministic output and operation counts over 5 repeats | **PASS** |
| K1 | Cost ledger recorded per architecture (preprocessing, traversal, grammar, energy, finalisation; operation counts; peak RSS; repeat spread) -- W=0 dry run only, no G_net computed | **PASS** |
| S6 | Candidate tie policy (E <= E0+W+tau; PRESERVED iff W+tau < Delta) tested on 3000 synthetic near-tie cases: tolerance never removes a target and never converts an excluded target into a preserved one; classification agrees with membership; edge cases handled | **PASS** |
| S7 | Gap diagnostics Delta_G and rho_G=W/Delta_G implemented and verified on the PUBLIC 1x1 and 2x2 patches: rho<1 (policy: W+tau<Delta) <=> FN=0 at every window. Not computed for 3x3 or nulls (post-freeze). | **PASS** |
| S8 | Outcome-blind audit: 3x3 was run only at W=0 (the single W>0 attempt is the guard refusal test); no run used --unblind-after-freeze; Delta_G/rho_G not computed on 3x3; solver outputs contain no level/spectrum fields | **PASS** |

## Still open (to be fixed before any freeze, never from v008 performance)

- Window constant/rule (c in W = c*A(T_ref) or c*k_B*T_ref, or a level-respecting cardinality rule).
- Tie-policy constant and rule (candidate tested here is not frozen).
- Numerical success thresholds for G, P, C and the uncertainty/margin rule.
- Primary seed registry and null sample sizes; E2 design; state/variable ordering policy for B1 and G2; runtime and memory limits.
- Whether global-reversal (Z2) symmetry may be exploited by B0/G2/B1 (it halves every search; not used in v008 for any solver).
