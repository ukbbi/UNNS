# XVI Grid Scaling v001 — Executed Findings

## Source integrity / negative baseline

The **exact user-uploaded** `XVI_TAU_EVOLUTION_v001.json` is frozen at `docs/frozen/XVI_TAU_EVOLUTION_v001.json`, SHA-256 `8ed0d7afcdaba90cddcd5a51e8468f09c60dd634d85d7cc41048ef25986caab9`. Its overall verdict is `FULL_TAU_CERTIFICATION_NOT_ESTABLISHED`; its T2 and T4 failures are unchanged. Original source HTML SHA-256 is `da4f217eaba86eba02517e6f6c2d70d8e5da43b189158b3ad22b93399d47d44d` and is untouched. Earlier repair baseline SHA-256 is `875cdce0399a97a8a645c0df063d67bd1ff589bece3ee87c8415d976f9d95a6c`.

**This phase does not change any earlier scientific verdict.** The candidate below has a different explicitly defined evolution law, not a hidden modification of canonical XVI.

## Fixed-physical-domain candidate results

Periodic `[0,2π]²`, terminal physical time `T=0.4`, seeds 41/137, grids 64²/128²/256². Scheme and CFL defined in `docs/XVI_GRID_SPEC_v001.md`.

| Seed | Coupled mesh/time 64→128 | Coupled 128→256 | SAME Δt 64→128 | SAME Δt 128→256 |
|---|---:|---:|---:|---:|
| 41 | 0.0017768604 | 0.0006351997 | 0.0008133804 | 0.0002233544 |
| 137 | 0.0015375616 | 0.0005508981 | 0.0006874202 | 0.0001931526 |

Same Δt: 0.004 for all three grids, 100 steps. Coupled mesh/time step schedules: 8, 25, 100 steps respectively. The separate N=128 half-Δt control yields relative errors 0.000460010 (seed 41) and 0.000396736 (seed 137). These are deterministic, finite-horizon discretization witnesses, *not* a numerical error theorem or a claim of physically calibrated τ dynamics.

| N | Seed 41 final spatial std / initial spatial std | Seed 137 ratio |
|---:|---:|---:|
| 64 | 0.894887 | 0.895275 |
| 128 | 0.892662 | 0.893325 |
| 256 | 0.891912 | 0.892670 |

Thus the candidate does not collapse to a spatially uniform field over the tested time window. This retention metric is NOT the Chamber XVI μ*, p, R² or entropy invariants, which remain **OPEN**. All tested candidate finite-volume flux projection errors remained below the numerical acceptance thresholds in S4. The α=0 versus α=0.08 ablation changes the final field by 0.018156 (relative L2), so the closure term is nontrivial under this test.

## Conditioning warning

A separate centered-projection test scales the same flux amplitude by factors 1, 10⁻⁶, 10⁻¹², and 10⁻¹⁶. Below the declared `1e-12` of reference flux norm, the relative P²−P diagnostic is marked **not interpretable**, while absolute and scale-to-reference residuals remain reported. This avoids silently upgrading the old T2 failure on the basis of a new error normalization. The old 256² source-T2 failure still exists.

## Scientific gate outcomes

`S0 PASS_FROZEN`; `S1 PASS_GEOMETRY_DISCREPANCY_IDENTIFIED`; `S2 PASS_CONDITIONING_DIAGNOSTIC_IMPLEMENTED`; `S3 PASS_NEW_COUPLED_SPACE_TIME_CAUCHY`; `S3b PASS_FIXED_DT_MESH_CONTROL`; `S4 PASS_NEW_CANDIDATE_FLUX`; `S5 PASS_NEW_FINITE_STRUCTURAL_RETENTION`; `S5a PASS_FIXED_GRID_DT_REFINEMENT`; `S5b PASS_NONTRIVIAL_CLOSURE_ABLATION`; `S6 OPEN_CHAMBER_XIV_XV_INVARIANTS_NOT_TRANSLATED`; `S7 NOT_DERIVED_OBSERVABLE_MEASURE`.

**New candidate verdict:** `LIMITED_PHYSICAL_GEOMETRY_WITNESS`.

**Original full-τ verdict:** `FULL_TAU_CERTIFICATION_NOT_ESTABLISHED`.

**Quantum measure / Born rule:** `NOT_DERIVED`.

## Required further evidence

The next test should translate and freeze the authentic Chamber XVI μ*, spectral slope p/R², and entropy calculations; introduce controlled physical/noisy data; expand across high-frequency and perturbation families; separately establish source-model grid calibration. Only a fully defined observable-event map could eventually connect a certified classical flux projector with a probabilistic representation theorem. It is not supplied by the current work.
