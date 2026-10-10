# SCR-III-B — FREEZE_v005

**Record type:** Scientific milestone freeze / append-only provenance record  
**Freeze date:** 2026-10-10  
**Milestone:** `PREFLIGHT_v005` — Physical Energy and Hamiltonian Convention Lock  
**Verdict:** `PHYSICAL_HAMILTONIAN_LOCK_PASS` (**scoped**)  
**Local reproducibility:** Confirmed by user-run Ubuntu/WSL terminal evidence  
**Successor:** `PREFLIGHT_v006` feasibility preflight — specification only at freeze time

## 1. Freeze decision

`PREFLIGHT_v005` is accepted as the **frozen physical Hamiltonian reference for the precisely specified Dryad SPMMC v1.00 finite-patch model** below. Its files, source identifiers, validation criteria, measured outputs, and conclusions are historical artifacts. Do not overwrite them in subsequent work. This freeze does **not** confer a physical-transfer result, validate the full unmodified Dryad simulator or the published 24×24 production arrays, or authorize an SCR-III-B primary/preregistered experiment.

**SCR-III-A v002 remains independently frozen at `COUPLING_MAP_ONLY`.** The v005 correction does not retroactively alter SCR-III-A or rewrite v001–v004 historical outputs.

## 2. Model and validity domain

- **Reference:** Original Dryad `SPMMC-SSI-Unix-v1.00.cpp`; original-source functions embedded verbatim in a controlled C++ probe and compared with an independently implemented Python physical-energy evaluator. Associated `MMC-SSI-Unix-v1.00.cpp` was used for convention differentiation/corroboration, not substituted for SPMMC.
- **Physics:** SPMMC v1.00 **all-pair dumbbell interactions** (no interaction cutoff), identical islands, free boundary, `stdev=0`.
- **Template parameters:** lattice spacing `a=260 nm`; island length `l=160 nm`; island width `w=60 nm`; island height `h=15 nm`; `M0=7.9×10^5 A/m`; `beta=0.5`; `Tc=820 K`; `kappa=1`.
- **Exhaustive patches:** `1×1` (4 spins, 16 states) and `2×2` (12 spins, 4,096 states). **Targeted-only 3×3:** 24 spins, 48 sampled configurations for field/energy/flip checks; no 16,777,216-state exhaustive enumeration.
- **Temperature:** Validated positive temperature-factor convention for `0<T<Tc`, numerically checked at five temperatures spanning `760–815 K`; ground energies below refer to `792 K`.

The physical conclusions in this record apply **only to that scoped model**, not arbitrary square-ice systems, other boundary choices, size disorder, or Dryad's geometry-specific v1.01 production models.

## 3. Reproduced findings

| Test/observation | Frozen result |
|---|---|
| Package scientific verdict | `PHYSICAL_HAMILTONIAN_LOCK_PASS` |
| Mandatory failures / unresolved mandatory checks | None / none in v005 report |
| Local WSL unit-test result | `Ran 10 tests ... OK` (10/10) |
| 1×1: states; ice states | 16; 6 |
| 1×1: ground energy at 792 K | `−9.528652×10⁻²¹ J` |
| 1×1: ground degeneracy; all ice-rule? | 2; yes (Type 1 vertices) |
| 1×1: first non-ice vs lowest ice energy | `9.529×10⁻²¹ J` |
| 2×2: states; ice states | 4,096; 82 |
| 2×2: ground energy at 792 K | `−4.089422×10⁻²⁰ J` |
| 2×2: ground degeneracy; all ice-rule? | 2; yes (Type 1 vertices) |
| 2×2: first non-ice vs lowest ice energy | `1.041×10⁻²⁰ J` |
| Temperature scaling | `E(s,T) = A(T) E_ref(s)` with positive `A(T)` and zero state-independent offset in selected model; tested ordering unchanged |

**Critical correction:** The v001–v004 normalized-energy implementation used `E_legacy=−Σ K_ij s_i s_j`; the original-source flip convention implies `ΔE=−2 A(T) s_i h_i`, consistent with `E_verified=+Σ K_ij s_i s_j` (with physical scaling). The legacy landscape is the negative of the verified landscape. Previously reported non-ice minima arise under that incorrect sign and are retained as **historical regression evidence**, not amended in place. The corrected model yields ice-rule ground states on both exhaustively studied patches. The v005 source-backed tests attribute this difference to the Hamiltonian sign convention.

## 4. Local reproduction evidence (user-run)

The user extracted the additive v005 package into the existing project on the Windows `D:` drive, then executed these commands in Ubuntu via WSL **from the project root**:

```bash
python3 scr_iii_b/reference_check/validate_v005.py
python3 scr_iii_b/reference_check/test_v005.py
```

The user-provided terminal screenshots show:

- The validator returned `"verdict": "PHYSICAL_HAMILTONIAN_LOCK_PASS"` and `"mandatory_failures": []` with a normal return to the Ubuntu prompt.
- The validator printed the same 1×1 and 2×2 physical ground-state classifications and energies recorded above.
- All ten unit-test names finished with `ok`; unittest printed `Ran 10 tests in 0.061s` and `OK`, and the shell returned to its prompt.

**Evidence boundary:** This records visual confirmation of local execution, *not* a separately captured local filesystem hash or a second full-source audit on the user's machine. The archive hashes below were measured on the uploaded build artifact in this conversation, not inferred from screenshots.

## 5. Frozen artifact fingerprints

**Uploaded package:** `PREFLIGHT_v005.zip`  
**ZIP SHA-256:** `06364833cefe20ed5934c2f2d884fcae007275f33cda76313e43258b35d95917`

SHA-256 of exact files *inside this uploaded ZIP*:

| Archive-relative file | SHA-256 |
|---|---|
| `scr_iii_b/output/validation/v005/REPORT_v005.json` | `64f67fd4fe70de7d28a43561cb522583459ef18f55a66a2482ef71359aa33967` |
| `scr_iii_b/output/validation/v005/TESTS_v005.json` | `bb29055d80d7ffc227545b00edf4ceffffd833debea94419cbaf825b6f9c10c0` |
| `scr_iii_b/output/validation/v005/MANIFEST_v005.json` | `fe7c59c63a58825957d776f92043b49af407978e84f1df6b480268236cf3c44a` |

Source SHA-256 values retained from `REPORT_v005.json`:

- `SPMMC-SSI-Unix-v1.00.cpp`: `f7ffe5ff3bdff923e1281c3ed7431dfece5ce0c596ffe3f60a5b037908ab750a`
- `MMC-SSI-Unix-v1.00.cpp`: `bd4f2e7a139817f7cee71d413d01f8296dcc31b5649bca086c26970d70b8cbc0`
- `SPMMC_Code.zip`: `77c82d83ea20eff5abcab8323b061edf759809cdd4366e86042147f6ea60a5dd`
- `MMC_Code.zip`: `d0aa94e081c733bac963d8d2c52eaaf596f58c43686a6dc66a44d3d1b801ee44` (first recorded in v005)
- `Dryad_README.md`: `b0f39ada4049248934db140fca396d3f3824e31094543c8b1c60d3a66e336f64`

## 6. Unresolved / explicitly outside the lock

1. Geometry-specific v1.01 production island widths/heights were not acquired/validated.
2. The **unmodified full Dryad simulator was not executed**; source functions were used verbatim inside a probe, and the source does not expose a direct total-energy output.
3. The published paper/supplement were not in the package; Dryad README supplied the cited Eq. 3 convention.
4. A periodic boundary alternative was not compared because the v1.00 periodic branch is empty.
5. Gaussian island size disorder (`stdev>0`) was not evaluated.
6. No physical energy-window target preservation, structural-null comparison, charged end-to-end speedup, or SCR transfer has yet been established.

These are **scope limitations**, not hidden passes or grounds to extend the v005 verdict beyond its declared mandatory checks.

## 7. Immutable handling and continuation

1. Preserve `PREFLIGHT_v005.zip` and the `scr_iii_b/output/validation/v005/` outputs byte-for-byte; preserve v001–v004 separately. Keep original Dryad references unchanged.
2. Treat **this `FREEZE_v005.md` as append-only**. Corrections require a new explicitly named amendment/superseding record that references the frozen SHA-256, never editing or replacing this one.
3. Changes for new tests, models, energy windows, nulls, specifications, and reports go into **v006 or later versioned paths only**.
4. Do not alter the repository remotely; GitHub remains reference-only until a separate user instruction.
5. Next planned milestone: `PREFLIGHT_v006` — **Energy-Window Feasibility and Non-Tautology Gate**. Evaluate exact full target-set preservation by the target-blind 2-in/2-out grammar, including adversarial defect-accessible windows and structural-incidence nulls. This is **not** yet a primary physical transfer claim.

**Freeze disposition:** `FROZEN / SCOPED / LOCALLY_REPRODUCED / NO_TRANSFER_CLAIM`
