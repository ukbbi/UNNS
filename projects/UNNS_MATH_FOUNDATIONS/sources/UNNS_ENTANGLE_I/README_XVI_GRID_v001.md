# UNNS ENTANGLE I — XVI GRID SCALING v001

**Phase:** Source-locked nonlinear grid-geometry, τ-update scaling, conditioning, and structural-preservation audit.

**Status:** The uploaded Phase τ report is frozen with **`FULL_TAU_CERTIFICATION_NOT_ESTABLISHED`**. A separately labeled physical-domain candidate passes **limited finite numerical witnesses** in this release. **Canonical Chamber XVI and the Born rule are NOT certified.**

## Extract safely

Unzip **directly into the existing innermost** `UNNS_ENTANGLE_I/` project directory, allowing folders to merge. This is an incremental overlay: all supplied filenames are new, except that `docs/frozen/XVI_TAU_EVOLUTION_v001.json` is a new frozen duplicate of the uploaded report. Do not replace `src/xvi_tau_evolution_v001.py`, `output/XVI_TAU_EVOLUTION_v001.json`, `docs/sources/XVI_ENGINE_v084.html` or any older research files.

For the uploaded exact baseline, SHA-256:

`8ed0d7afcdaba90cddcd5a51e8468f09c60dd634d85d7cc41048ef25986caab9`

The precomputed output in the prior v001 ZIP is *not* byte-identical to the latest uploaded report. The uploaded copy is authoritative for this freeze. An existing active report is displayed in audit metadata, but does not replace the frozen copy.

## Execute on Windows without launching downloaded .bat files

At the command prompt in `UNNS_ENTANGLE_I`:

```cmd
python -m pip install -r requirements_XVI_GRID_v001.txt
python -m unittest discover -s tests -p "test_*.py" -v
python -m src.xvi_grid_scaling_v001
```

New output: `output/XVI_GRID_SCALING_v001.json`. Tests verify source integrity and that older negative gates are not silently upgraded. A missing/mismatched frozen source aborts the experiment.

## What is actually new?

* A dimensional audit distinguishes the original source's `0.5` neighbor gradient and spectral `2π m/N` Laplacian from a fixed-domain physical gradient and Laplacian.
* A separate periodic fixed-domain candidate evolves the τ-field to identical **physical time T=0.4**, with grid-dependent time steps and consistent finite-volume flux projection. **Its evolution law is not the canonical HTML law**; details are in `docs/XVI_GRID_SPEC_v001.md`.
* Nonlinear diagnostics track the compatible post-projection divergence, absolute/scale-aware idempotence, quadratic decomposition, finite-time field variance, Fourier-band occupancy, coupled and same-Δt grid Cauchy errors, independent half-time-step controls, and a no-closure ablation.
* A conditioning audit marks ratios relative to vanishing flux as *uninterpretable below a fixed reference norm floor*, rather than certifying noise as signal.

## Scope and scientific boundaries

Passing this **new candidate** establishes only a bounded, small-corpus, finite-time, physically indexed numerical witness. Since spatial mesh and timestep are refined together, grid Cauchy differences include time discretization error; the package additionally includes same-Δt mesh comparisons and a fixed-grid half-timestep check. Full grid-independent dynamics, source HTML noise behavior, physical regime invariants μ*, p, R², chamber entropy, a valid exclusive observable event space, and Born weights **remain open**.

Frozen baseline verdict (unaltered): `FULL_TAU_CERTIFICATION_NOT_ESTABLISHED`.

Do not use this package to overwrite, "repair in place", or relabel canonical Operator XVI v0.8.4 STABLE.
