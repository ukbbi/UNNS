# REPORT_v009 — Preregistration Closure Gate (outcome-blind)

**Verdict:** `PREREG_CLOSURE_GATE_PASS`

This is a **technical-readiness** verdict. It does not freeze `SCR_III_B_SPEC_v001.md` or `SCR_III_B_PREREG_v001.md`, ratifies none of the proposed values, authorises no primary run and implies nothing about H-G, H-P, H-T or H-C primary success. Authorization remains `SCR-III-B / V008_LOCALLY_REPRODUCED / V009_SPECIFIED / PRIMARY_NOT_AUTHORIZED`.

## Test table

| ID | Test | Status |
|---|---|---|
| F1 | Frozen v005-v008 code/outputs equal the hashes in their local manifests (read-only) | **PASS** |
| P0 | Prerequisites and original-source provenance: compiler, numpy, frozen manifests present; Dryad source hashes recorded by v005 | **PASS** |
| R1 | Common physical E0: the frozen v007 anchor (hash-matched, unit-checked, independently re-certified by Gray-code and branch-and-bound minimisation) is passed to B0, G1, G2, B1 and E2; every solver echoes it bitwise and thresholds E | **PASS** |
| R2 | Inconsistent ground-energy references are rejected (exit 4) or flagged; missing reference refused; harness reconciliation rejects a different estimate; a grammar-restricted minimum never replaces E0 | **PASS** |
| E1 | E2 omitted-interaction bound: H_R - B_O <= H <= H_R + B_O verified in exact rational arithmetic (6000 state/fraction checks); the C++ certified B_O is >= the exact omitted weight (outward rounded); retained set and its ordering di | **PASS** |
| E2 | E2 returns the complete target set equal to B0 and to the brute-force oracle on public 1x1 and 2x2 at W=0, every level threshold, 10*tau below it and every midpoint, for retained fractions (0.0, 0.1, 0.25, 0.5, 0.9, 1.0); equals B | **PASS** |
| E3 | E2 ambiguous-case handling: 150 random synthetic instances/windows/fractions (117 with fallbacks, 35842 fallback evaluations) all equal the oracle; with zero retained pairs every undecided state falls back to the full exact evalua | **PASS** |
| E4 | Charged-cost completeness: E2 and B0 pair-operation counters equal an independent analytic model EXACTLY (including Gray-code resynchronisation, certified decisions and fallback evaluations) on 2x2 and the 3x3 anchor; G1 counters  | **PASS** |
| T1 | Threshold equality and near-boundary behaviour: classification table (gap > / = / < W+tau, zero gap, empty excluded set) and exact dyadic instances with gap-minus-(W+tau) in {+-2^-30, +-2^-45, +-2^-50, 0}: B0, B1 and E2 agree with | **PASS** |
| T2 | Zero-gap and empty-excluded-set handling, and the gap/preservation equivalence: ground level excluded -> Delta = 0 and FAIL; S_G = S_0 -> Delta = +inf, PASS with the empty-excluded-set flag; C++ nullgap equals a Python brute force | **PASS** |
| T3 | Conservative numerical error treatment (659 randomised near-threshold cases, offsets from 0.3 eps_input to 100 eps_gray and wide, across B0/B1/E2/G2): every solver set equals the exact-rational oracle (UNRESOLVED_BOUNDARY included | **PASS** |
| W1 | Thermal windows vs the PUBLIC small-patch gaps: k_BT_ref(792 K) = k_B*792 = 1.093474008e-20 J (the specification prints 1.093473608e-20 J, a 3.7e-7 relative typo vs the SI-exact product; 1.09347e-20 agrees) = 0.010831 (A units); C | **PASS** |
| N1 | Deterministic seed regeneration: the domain-separated derivation '<master>|<family>|<idx>' equals the frozen v006 derivation (200 draws/family, NULLS_v006.csv labels), the first 100 accepted nulls per family regenerate bit-identic | **PASS** |
| N2 | Null well-formedness and acceptance accounting: 2000 accepted nulls (N1 degree-preserving, N2 free incidence) are structurally valid; attempted = accepted + duplicates + rejections with reasons, none exhausted; constructive surviv | **PASS** |
| N3 | Null feasibility gate: 2 x 1000 valid nulls generated deterministically within the draw cap and the primary Delta_null evaluation (one Gray-code scan per null, timed on a synthetic 24-spin instance) fits the per-arm budget | **PASS** |
| O1 | Deterministic candidate ordering: every solver repeats counters/ids exactly across runs (2x2 at two windows, 3x3 at the W=0 anchor); G2 island order equals the specified first-appearance order; E2 breaks equal |K| by pair index; B | **PASS** |
| Z1 | Global-reversal (Z2) symmetry: H(-s) = H(s) exactly on every public state; the ice grammar is complement-invariant (public patches and all 2604 3x3 survivors); the optional --z2 sensitivity mode gives identical target sets for ALL | **PASS** |
| C1 | Complete operation-cost ledger: all 15 required cost items are recorded for B0, G1, G2, B1 and E2 (and, separately, for the E0 certification); each operation belongs to exactly one bucket (setup / generation / filter / energy / ot | **PASS** |
| C2 | Timing protocol and resource feasibility: single thread, 3 warm-ups + 15 timed rounds, deterministic balanced interleaving (position-balanced: True), median and dispersion; worst-case synthetic 24-spin windows keep every arm under | **PASS** |
| B1 | 3x3 W>0 guard: every attempt on the real 3x3 instance with W>0 (five solvers, three windows), the excitation-gap (nullgap) mode, the synthetic-flag bypass (with and without the protected list) is REFUSED with exit 3 and no result  | **PASS** |
| B2 | No primary-window outcome disclosure: the invocation audit shows only W=0 anchor and grammar-only executions of the real 3x3 instance (all W>0 / excitation-gap requests BLOCKED), every W>0 run on n>16 used a non-protected syntheti | **PASS** |
| H1 | Decision functions implement the axis decision table (G exact membership + >=99% contraction; P FN=0 with a complete verifier; T NOT_TESTED; C needs P and certified completeness plus the paired lower-bound rule) and reproduce the  | **PASS** |
| D1 | Draft decisions and open items are faithfully recorded: the shipped SPEC/PREREG copies stay UNFROZEN, contain every one of the 18 register decisions with their PROPOSED values marked AWAITING RATIFICATION, the thermal-window discl | **PASS** |

## Common ground-energy reference (R1/R2)

- Frozen v007 anchor E0 = `-0.09184041396072776` (A units) = -9.2719947518037269e-20 J; hash of REPORT_v007.json matches the frozen record: **True**; unit scaling E0·A(792 K) = -9.2719947518037269e-20 J.
- Independent re-certification (Gray-code minimisation and branch-and-bound minimisation) reproduces it within τ (bitwise: {'cert_b0': True, 'cert_b1': True}) with the two disclosed complementary ground states.
- Limit: G1/G2/E2 cannot certify E0 themselves; mismatches are caught by the exit-4 checks where possible and always by the harness bitwise reconciliation.

## Tolerance hierarchy (proposed, not frozen)

For the 3×3 coupling set Q = Σ|K| = 0.1721: eps_input = 3.821e-17 < eps_direct = 5.349e-15 < eps_gray = 1.721e-11 < τ = 1.721e-10.
Membership: E ≤ E0 + W + τ; PRESERVED ⇔ W + τ < Δ_nonG; |d| ≤ eps_input is UNRESOLVED_BOUNDARY and counted as target (conservative).

## E2 comparator

Exact for every tested retained fraction (public patches at all windows, mixed-sign / zero / tie-heavy instances, 150 random synthetic cases, 3×3 anchor). Synthetic n=24 fraction sweep (cost only; B0 wall at 1 k_BT shown for reference):

| instance | retained fraction | wall @1 k_BT (s) | pair ops @1 k_BT | fallbacks @1 k_BT | wall @2 k_BT (s) |
|---|---|---|---|---|---|
| gauss | 0.05 | 5.788 | 4684185600 | 16777216 | 5.685 |
| gauss | 0.1 | 5.741 | 4713086976 | 16777216 | 5.711 |
| gauss | 0.25 | 5.825 | 4789436496 | 16757508 | 5.748 |
| gauss | 0.5 | 0.9938 | 857550504 | 2154658 | 2.53 |
| gauss | 0.75 | 0.2164 | 346158928 | 13764 | 0.2977 |
| gauss | 0.9 | 0.2465 | 419951984 | 940 | 0.2587 |
| gauss | 1.0 | 0.254 | 455344128 | 0 | 0.2546 |
| gauss | B0 | 0.1836 | | | 0.1883 |
| realmag | 0.05 | 5.724 | 4688576512 | 16777216 | 5.7 |
| realmag | 0.1 | 3.41 | 2746188512 | 9631064 | 4.737 |
| realmag | 0.25 | 0.1316 | 150832848 | 14372 | 0.1686 |
| realmag | 0.5 | 0.177 | 259922608 | 1212 | 0.1839 |
| realmag | 0.75 | 0.2136 | 347046240 | 120 | 0.2151 |
| realmag | 0.9 | 0.2467 | 425798984 | 42 | 0.2466 |
| realmag | 1.0 | 0.2558 | 455344128 | 0 | 0.2761 |
| realmag | B0 | 0.1832 | | | 0.1819 |

The spec-proposed 25% is exact (E1-E3) but, on flat-coupling synthetic 24-spin instances, its certified interval is rarely decisive, so E2 degenerates towards a full fallback scan (wall ratio E2(25%)/B0 at 1 kT: gauss 31.7x, realmag 0.7x). Measured worst-case pair operations over {gauss, realmag} x {1 kT, 2 kT} are lowest at a retained fraction of 75% (candidates 5-90%; 100% is B0 in disguise and is excluded). v009 therefore RECOMMENDS 75% as the prospective E2 setting and keeps 25% only as the spec's nominal value; neither is frozen. The choice used synthetic data only, no 3x3 target. The real 3x3 W=0 anchor E2 cost is reported in the ledger.

## Thermal windows vs public gaps (W1)

| patch | window | Δ/k_BT | (W+τ)/Δ | status |
|---|---|---|---|---|
| 1x1 | sensitivity_A_0.5kT | 0.8714 | 0.574 | PASS |
| 1x1 | primary_1kT | 0.8714 | 1.148 | FAIL |
| 1x1 | sensitivity_B_2kT | 0.8714 | 2.295 | FAIL |
| 2x2 | sensitivity_A_0.5kT | 0.9524 | 0.525 | PASS |
| 2x2 | primary_1kT | 0.9524 | 1.050 | FAIL |
| 2x2 | sensitivity_B_2kT | 0.9524 | 2.100 | FAIL |


## Seeds and nulls

Master seed 20261010; accounting per family: {"N1": {"move_attempts": 459014, "move_rejections": 99014, "attempted": 1000, "accepted": 1000, "exhausted": false}, "N2": {"move_attempts": 0, "move_rejections": 0, "rejected:empty grammar (no surviving configuration)": 9, "attempted": 1009, "accepted": 1000, "exhausted": false}}
Primary Δ_null evaluation needs one Gray-code scan per null: median 0.3956 s on a synthetic 24-spin instance → estimated {'N1': 397, 'N2': 397} s per family (budget 1800 s). 2×1000 nulls fit: **True**.

## Cost ledger (3×3, W=0 anchor only; 1 thread; 3 warm-ups + 15 rounds; median)

| Solver | wall (s) | rel. MAD | charged total (s) | + E0 certification (s) | pair ops | nodes / states | peak RSS (MB) |
|---|---|---|---|---|---|---|---|
| B0 | 0.1835 | 0.4% | 0.1836 | 0.1838 | 473628948 | 16777216 | 4.5 |
| G1 | 0.07749 | 0.6% | 0.07761 | 0.0778 | 718704 | 16777216 | 4.5 |
| G2 | 0.0001982 | 1.3% | 0.0003174 | 0.000509 | 103536 | 25786 | 4.5 |
| B1 | 5.817e-05 | 0.7% | 0.0001788 | 0.0003704 | 46900 | 3186 | 4.5 |
| E2 | 0.1254 | 0.4% | 0.1255 | 0.1257 | 146941800 | 16777216 | 4.5 |

One-time E0 certification: cert_b0 0.184 s (charged); cert_b1 0.0001916 s (charged). **These are acceptance-only component measurements: no speedup, no G_net and no C verdict follows.**

## H-C uncertainty rule (simulation on synthetic correlated timings)

| true ratio | bootstrap coverage | P(decision PASS) |
|---|---|---|
| 1.00 | 0.85 | 0.00 |
| 1.10 | 0.83 | 0.00 |
| 1.20 | 0.85 | 0.07 |
| 1.50 | 0.78 | 1.00 |
| 2.00 | 0.83 | 1.00 |

**Honest limitation:** the nominal 95% interval has simulated coverage of only 0.78-0.85 with 15 rounds (moving-block bootstrap, block 3); a log-scale t interval is similar. The rule is therefore anti-conservative as an interval; what the proposal relies on is the simulated decision error: false-pass rate for true ratio <= 1.1 and power at 1.5 (table above and C2).

## Things you should know before ratifying

1. **H-G ≥ 99% cannot discriminate**: 2,604/2^24 (99.985%) is already known, so the condition only fails if constructive membership disagrees with the independent count.
2. **H-C ≥ 1.20× against B0 is unlikely to bind**: the disclosed W=0 timings differ by about three orders of magnitude; B1 (and possibly E2) are the informative sensitivity arms. B1 beat G2 at W=0 in v008.
3. **The primary window k_BT exceeds the known exclusion gaps of 1×1 (0.871 k_BT) and 2×2 (0.952 k_BT)**; a P FAIL at 3×3 is a genuine possibility and must be reported, not repaired.
4. The guard and audit are procedural. The v007 upper-spectrum leak means the study is low-energy-outcome blinded, not spectrum-blind. W=0 operation counters are published.
5. The tolerance τ = 1e-9·Q is a convention validated for conservatism, not derived from physics; the v007 drift threshold revision (1e-12 → 1e-10) was post hoc and is not a precedent.

## Readiness

Technical readiness to freeze **without outcome-dependent modification**: the implementation, numerical and blindness prerequisites tested here are satisfied; the remaining steps are your ratification of the register, assembly of the final documents with source hashes, a separate freeze record and a separate authorization.

