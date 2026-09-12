# TC_RIGIDITY_v001

Higher-order rigidity test for the UNNS Time Crystal branch.

## Purpose

Test whether the already-frozen temporal-closure observables become
DTC-specific when their geometry, perturbation-basin breadth, and initial-state
universality are considered together.

## Required sibling packages

You can use either extracted folders or ZIPs:

```text
Time_crystal\
├── TC_CLOSURE_LOCK_v001\
├── TC_CLOSURE_v001\
├── TC_EXT_MI_v001\
├── TC_CTRL_v001\
└── TC_RIGIDITY_v001\
```

or the corresponding `.zip` files.

## Windows

The simplest arrangement is the extracted-folder layout above. Then
double-click:

`RUN_WINDOWS.bat`

Manual command:

```bat
python run_rigidity.py ^
  ..\TC_CLOSURE_LOCK_v001 ^
  ..\TC_CLOSURE_v001 ^
  ..\TC_EXT_MI_v001 ^
  ..\TC_CTRL_v001 ^
  outputs
```

The runner also accepts `.zip` paths.

## Outputs

- `outputs/rigidity_result.json`
- `outputs/rigidity_vectors.csv`
- `outputs/geometry_comparison.csv`
- `outputs/basin_comparison.csv`
- `outputs/classical_initial_states.csv`
- `outputs/classical_initial_spectra.csv`
- `outputs/geometry_profiles.png`
- `outputs/rigidity_axes.png`
- `outputs/universality.png`
- `outputs/basin_retention.png`
- `outputs/RUN_LOG.txt`

See `METHOD.md` for the exact definitions.
