# MUG-I v009 — Physically Coupled Maxwell–UNNS Histories

**Research release only — no manuscript, no remote GitHub changes, and no edits to v001–v008.**

Research target: Can a physically specified Maxwell interaction selectively connect electromagnetic mode states that also lie along UNNS histories, rather than only annotate an inert arithmetic graph?

## Short result

**YES, conditionally:** A real Maxwell mode-coupling mechanism in a prescribed time-modulated dielectric populates 2→8→36 (both steps are valid `T_N` index edges), while translation symmetry exactly forbids the alternative intermediate index 9 for that fixed pump. **NO independent UNNS physical predictive advantage is shown:** the same pump also reaches 36 via a non-UNNS conversion route if pulse order is reversed, and it excites infinitely many mode pairs that have no UNNS connection at all (m→m+34, m≥12). Maxwell/Fourier theory independently predicts every tested modal selection rule.

All statements refer to mode-index overlaps. The Maxwell dynamical pump **does not implement** `T_N` as a whole-field coordinate-substitution operator.

## Source model

`∂t D = −∂z B`, `∂t B = −∂z E`, `D = ε(z,t) E`, on the 2π torus, with `ε(z,t) = 1+2η[f1(t)cos(q1(z−t))+f2(t)cos(q2(z−t))]`. The pulses occupy successive nonoverlapping time intervals; the pump is off at the start and finish, allowing unambiguous incoming/outgoing vacuum mode amplitudes. See `theory/EXACT_RESULTS.md`.

## Reproduction on your Ubuntu / WSL terminal

Extract **alongside** `MUG-I_v008`, do not overwrite earlier releases. From the new release root run:

```bash
python3 scripts/verify_exact.py
python3 scripts/run_v009.py
python3 scripts/verify_heldout.py
python3 scripts/verify_born.py
python3 scripts/convergence.py
python3 scripts/independent_fdtd.py
python3 scripts/counterfamily.py
```

Only **NumPy** and the Python standard library are needed. Your Ubuntu environment already had NumPy installed for MUG-I v008. No SciPy is required for this phase. The two first commands can be run in the reverse order; `verify_heldout`, `verify_born`, `convergence`, and `independent_fdtd` need `run_v009` outputs.

Expected success markers: `EXACT VERIFY PASS`, `HELDOUT PASS 13/13`, `HELDOUT VERIFY PASS`, `BORN COEFFICIENT VERIFY PASS`, `GRID/TIME CONVERGENCE PASS`, `INDEPENDENT FDTD PASS`, `COUNTERFAMILY NUMERICAL EXAMPLES PASS`.

## Contents

- `protocol/PREDICTIONS_LOCK.json` — frozen numerical test cases/inequalities and explicit pilot disclosure.
- `protocol/PREDICTIONS_LOCK.sha256` — checksum of the pre-run lock.
- `theory/EXACT_RESULTS.md` — mathematical results T1–T6 with scope and derivations.
- `theory/RESEARCH_LIMITS.md` — distinctions among arithmetic overlay, physical coupling, and prospective physical prediction.
- `scripts/maxwell_solver.py` — Fourier-pseudospectral RK4 for Maxwell's D,B evolution (no UNNS logic inside the solver).
- `scripts/independent_fdtd.py` — independently written staggered-grid Maxwell Yee finite differences.
- `scripts/verify_born.py` — separate analytic second-order mode-coupling coefficient oracle.
- `scripts/verify_exact.py` — independent standard-library UNNS/symmetry and nonUNNS witnesses.
- `scripts/run_v009.py`, `verify_heldout.py`, `convergence.py`, `counterfamily.py` — reproducible tests and controls.
- `results/` — archived computed results and a human-readable report.
- `REGISTER.md`, `SOURCE_PROVENANCE.md`, `MANIFEST.json` — statuses, source fingerprints and file inventory.

**Interpretation:** Research establishes a definite Maxwell-controlled *intersection* with the UNNS history graph and an equally definite limit on its claimed specificity. It does not establish a new electromagnetic law.
