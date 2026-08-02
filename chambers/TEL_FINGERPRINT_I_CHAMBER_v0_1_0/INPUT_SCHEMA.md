# TEL-FINGERPRINT-I v0.1.0 — Input schema

## Row meaning

One row represents one corrected or control teleportation route at one physical perturbation coordinate.

The unique row key is:

```text
scenario_id
realization_id
lambda
route_id
correction_status
control_type
```

Every analysis group must contain exactly four unique rows, one for each Bell route.

## Required columns

| Column | Type | Rule |
|---|---|---|
| `scenario_id` | text | Physical scenario identity, such as a noise family/location combination |
| `realization_id` | text | Independent calculation, bootstrap, or experimental acquisition |
| `lambda` | number | Physically ordered perturbation coordinate |
| `route_id` | enum | `PHI_PLUS`, `PHI_MINUS`, `PSI_PLUS`, `PSI_MINUS` |
| `correction_status` | text | Recommended: `CORRECT`, `WRONG`, or `NONE` |
| `control_type` | text | Recommended: `PRIMARY`, `WRONG_CORRECTION`, `CLASSICAL`, `ENTANGLEMENT_BREAKING` |
| `noise_family` | text | Physical noise family or `IDEAL` |
| `noise_location` | text | Where the perturbation acts |
| `branch_probability` | number | Inclusive range `[0,1]` |
| `closure_defect` | number | Bounded route-to-target defect in `[0,1]` |
| `process_fidelity` | number | Inclusive range `[0,1]` |
| `choi_purity` | number | Normalized Choi-state purity in `[0.25,1]` for a single-qubit channel |
| `choi_entropy_norm` | number | Choi entropy divided by `log(4)`, in `[0,1]` |
| `ppt_negativity` | number | Choi-state negativity in `[0,0.5]` |
| `ptm_sv_1` | number | First ordered Pauli-transfer singular value |
| `ptm_sv_2` | number | Second ordered Pauli-transfer singular value |
| `ptm_sv_3` | number | Third ordered Pauli-transfer singular value |
| `nonunital_displacement` | number | Bloch translation magnitude; chamber clips the defect coordinate to `[0,1]` |
| `physicality_pass` | boolean-like | `true`, `1`, `pass`, or `yes` accepted as passing |

## Canonical physical conventions

- `ptm_sv_1 >= ptm_sv_2 >= ptm_sv_3` is required.
- Choi quantities refer to the normalized Choi state.
- `closure_defect` must be declared before chamber analysis, including its distance definition.
- All four routes at one group must use the same quantum representation and estimator.
- `lambda` must carry physical meaning. Row number, file order, and arbitrary matrix-entry order are forbidden substitutes.

## Example header

```csv
scenario_id,realization_id,lambda,route_id,correction_status,control_type,noise_family,noise_location,branch_probability,closure_defect,process_fidelity,choi_purity,choi_entropy_norm,ppt_negativity,ptm_sv_1,ptm_sv_2,ptm_sv_3,nonunital_displacement,physicality_pass
```

## What the chamber derives

The raw quantum invariants are converted into ten frozen defect coordinates:

```text
probability imbalance
terminal closure defect
process infidelity
Choi mixing
Choi entropy
Choi entanglement loss
PTM contraction defect 1
PTM contraction defect 2
PTM contraction defect 3
nonunital displacement
```

The chamber never sorts or flattens density-matrix entries.

## Minimum viable input

A single trajectory requires:

```text
1 scenario
1 realization
at least 2 distinct lambda values
4 routes at every lambda
```

Scenario retrieval requires at least:

```text
2 scenarios
2 realizations per scenario
one common lambda grid across all compared realizations
```

## Invalid input conditions

The run stops when any of the following occurs:

- a required column is missing;
- a group does not contain exactly the four locked route IDs;
- a duplicate route occurs in a group;
- a required number is non-finite or outside its physical range;
- `physicality_pass` is false;
- PTM singular values are not descending;
- a realization repeats the same `lambda` group;
- fewer than two perturbation levels exist for a trajectory.