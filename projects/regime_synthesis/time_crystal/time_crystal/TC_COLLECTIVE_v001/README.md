# TC_COLLECTIVE_v001

Collective / many-body extension of the UNNS Time Crystal branch.

## Required siblings

Use extracted folders or ZIPs for the frozen packages. The simplest layout is:

```text
Time_crystal\
├── DTC_Data.zip
├── TC_CLOSURE_LOCK_v001\
├── TC_EXT_MI_v001\
├── TC_CTRL_v001\
└── TC_COLLECTIVE_v001\
```

## Windows

Double-click:

`RUN_WINDOWS.bat`

Manual command:

```bat
python run_collective.py ^
  ..\DTC_Data.zip ^
  ..\TC_CLOSURE_LOCK_v001 ^
  ..\TC_EXT_MI_v001 ^
  ..\TC_CTRL_v001 ^
  outputs
```

The runner also accepts the three prior packages as `.zip` files.

## Main outputs

- `outputs/collective_result.json`
- `outputs/spin_glass_scaling.csv`
- `outputs/localization.csv`
- `outputs/bitstring_breadth.csv`
- `outputs/typicality.csv`
- `outputs/collective_vectors.csv`
- `outputs/classical_spin_glass.csv`
- `outputs/spin_glass_scaling.png`
- `outputs/spin_glass_exponent.png`
- `outputs/perturbation_profiles.png`
- `outputs/typicality_mean.png`
- `outputs/temporal_collective_plane.png`
- `outputs/RUN_LOG.txt`

See `METHOD.md` for the interpretation boundary.
