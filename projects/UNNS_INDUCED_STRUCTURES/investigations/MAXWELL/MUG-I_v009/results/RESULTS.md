# MUG-I v009 — Verified research results

**Research, not manuscript.** Six cases and thirteen inequality predictions were locked after a disclosed pilot, before the held-out runs. Physical law: time-dependent transverse Maxwell coupling; UNNS unchanged.

## Held-out prospective computational checks

| Experiment | Measurement | Threshold | Observed amplitude | Verdict |
|---|---|---:|---:|---|
| `A_forward` | `after_stage_1` mode 8 | > 0.02 | 0.0305938138 | PASS |
| `A_forward` | `after_stage_2` mode 36 | > 0.002 | 0.00418832834 | PASS |
| `A_forward` | `after_stage_2` mode 9 | < 1e-10 | 8.78902719e-18 | PASS |
| `reverse_nonUNNS` | `after_stage_1` mode 30 | > 0.08 | 0.114273631 | PASS |
| `reverse_nonUNNS` | `after_stage_2` mode 36 | > 0.007 | 0.0156101995 | PASS |
| `reverse_nonUNNS` | `after_stage_2` mode 9 | < 1e-10 | 6.70256569e-18 | PASS |
| `single_6` | `after_stage_1` mode 8 | > 0.02 | 0.0305938138 | PASS |
| `single_6` | `after_stage_2` mode 36 | < 1e-10 | 1.23552917e-17 | PASS |
| `single_28` | `after_stage_2` mode 36 | < 1e-10 | 5.33793721e-18 | PASS |
| `B_alternative_grating` | `after_stage_1` mode 9 | > 0.02 | 0.0344153911 | PASS |
| `B_alternative_grating` | `after_stage_2` mode 36 | > 0.002 | 0.00471149134 | PASS |
| `matched_nonUNNS_target` | `after_stage_1` mode 10 | > 0.02 | 0.0382351888 | PASS |
| `matched_nonUNNS_target` | `after_stage_2` mode 38 | > 0.003 | 0.00552152016 | PASS |

**Total: 13/13 PASS.** Lock SHA-256: `45c50e6d78c6b907b8c8cceab42e989f391198ecacdb88dbbb89e3a55f55d39f`.

## Independent numerics

| Case | Mode | Fourier/RK4 amplitude | Independent Yee/FDTD amplitude | Relative difference |
|---|---:|---:|---:|---:|
| `A_forward` | 8 | 0.0305653039 | 0.0305646389 | 2.1755e-05 |
| `A_forward` | 36 | 0.00418832834 | 0.00418640727 | 0.00045867 |
| `A_forward` | 9 | 8.78902719e-18 | 4.84446674e-17 | symmetry null |
| `matched_nonUNNS_target` | 10 | 0.0381795234 | 0.038178228 | 3.3929e-05 |
| `matched_nonUNNS_target` | 38 | 0.00552152016 | 0.00551863819 | 0.00052195 |
| `reverse_nonUNNS` | 30 | 0.112773849 | 0.112740771 | 0.00029331 |
| `reverse_nonUNNS` | 36 | 0.0156101995 | 0.0155990309 | 0.00071547 |
| `reverse_nonUNNS` | 9 | 6.70256569e-18 | 3.23718482e-17 | symmetry null |

## Grid and timestep refinement

| Case | Mode | Relative change (N=256, dt=.002 vs N=512, dt=.001) |
|---|---:|---:|
| `A_forward` | 36 | 7.04828e-07 |
| `matched_nonUNNS_target` | 38 | 9.39378e-07 |
| `reverse_nonUNNS` | 36 | 1.552e-06 |

## Maxwell perturbative coefficient controls

| Case | Born coefficient of eta² | Born predicted amplitude | Maxwell computed amplitude | Relative difference |
|---|---:|---:|---:|---:|
| `A_forward` | 52.0203142 | 0.00421364545 | 0.00418832834 | 0.00600836 |
| `reverse_nonUNNS` | 195.075 | 0.015801075 | 0.0156101995 | 0.0120799 |
| `B_alternative_grating` | 58.5224478 | 0.00474031827 | 0.00471149134 | 0.00608122 |
| `matched_nonUNNS_target` | 68.6377329 | 0.00555965636 | 0.00552152016 | 0.00685945 |

## Additional post-lock counterfamily samples

| Initial mode | Excited target | Outgoing Maxwell amplitude | UNNS path |
|---:|---:|---:|---|
| 12 | 46 | 0.0119764793 | None: target < 4×source |
| 13 | 47 | 0.0129075875 | None: target < 4×source |
| 20 | 54 | 0.020176514 | None: target < 4×source |

## Exact conclusions

- **PROVED:** The (6,28) grating preserves Fourier parity, hence a start at mode 2 can never populate mode 9, while matched 2→8→36 conversion is perturbatively nonzero.
- **PROVED:** With one harmonic only, mode 36 is unreachable from mode 2 by exact translation congruence.
- **PROVED:** Reversing the external grating schedule can populate 36 through mode 30, a non-UNNS intermediate. Different schedules are different physical protocols.
- **PROVED:** For every integer m≥12, m→m+34 has no forward UNNS history, while this Maxwell pump produces a nonzero second-order outgoing coupling for sufficiently small η.
- **NUMERICAL:** All 13 held-out predictions passed; independent Yee FDTD and convergence and Born checks passed.
- **NOT ESTABLISHED:** UNNS-specific added physical predictive power, laboratory observation, or a Maxwell dynamical realization of the whole-field `T_N` operation.

Full definitions, proofs and limitations: `theory/EXACT_RESULTS.md` and `theory/RESEARCH_LIMITS.md`.
