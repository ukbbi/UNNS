# MUG-I v008 — Admissibility-Rule Resolution

**Research release (local candidate), not a manuscript.** Created to resolve MUG-I v007 O5/O9: determine whether Bloch-sector filtering is a necessary consequence of Maxwell plus the unchanged UNNS law, or an additional declared induction operation.

## Finding

The ambiguity has an exact answer. In the scalar periodic medium `epsilon(z)=1+2*delta*cos(q*z)`, `delta != 0`:

1. Strict whole-field **Fourier-support** nesting preserves original `T_N` admissibility for the current full support. The two sample equal-endpoint histories both survive and produce the same field, but transformed fields are generally *not stationary eigenstates of the original medium*.
2. The v007 rule E equals componentwise filtering for `N|q`, and kills all components when `N` does not divide the fixed medium harmonic `q`. Its unequal survival is real under that **added projector**, not required by passive Maxwell dynamics or original whole-field `T_N`.
3. Strict **same-medium stationary-eigenstate-to-stationary-eigenstate** nesting is obstructed for **every** nontrivial scale factor `r>1` when `delta != 0` (exact no-go theorem).
4. Full eigenbasis expansion is lossless as a change of representation. With a co-dilating medium the transformed field is again an exact eigenmode, but of a *different* Maxwell system.
5. There is **no independent physical predictive advantage** from v007's reported blocking without an independently specified Maxwell coupling/filter implementing the projector.

The first result concerns admissible *fields as Fourier data*, the third concerns *exact stationary eigenstates*; they are not contradictory.

## Reproduction (PowerShell from release root)

Requires only Python 3 for the two exact scripts:

```powershell
py -3 scripts\run_v008.py
py -3 scripts\verify_v008.py
```

Optional numerical eigenmode test (same model and same eigenstate for all rules; requires `numpy`, `scipy`):

```powershell
py -3 scripts\spectral_same_state.py
py -3 scripts\spectral_controls.py
```

Expected final lines: `MUG-I v008 VERIFY PASS` and `PASS SAME-EIGENSTATE spectral comparison` and `PASS held-out scalar Maxwell eigenstate controls: 5`.

## Files

- `theory/THEOREMS.md` — complete proofs T1–T6 and precise limits.
- `results/rule_comparison.csv` — both equal-endpoint words under all three rules.
- `results/summary.json` — machine-readable exact research register.
- `results/spectral_same_state.json` — reconstructed truncated Maxwell eigenstate and spectral residual controls.
- `scripts/core.py` — exact operators (standard-library `Fraction`).
- `scripts/run_v008.py` — deterministic census/research calculation.
- `scripts/verify_v008.py` — independent arithmetic oracle (does not import `core.py`).
- `scripts/spectral_same_state.py` — independent generalized-eigenvalue numerical control.
- `scripts/spectral_controls.py` — five additional medium/label numerical controls.
- `results/spectral_controls.csv` — residual measurements for these controls.
- `SOURCE_PROVENANCE.md` — exact identity of reviewed v007 archive.

Nothing in earlier releases or GitHub was changed. Keep v007 frozen; v008 is a separate local research candidate until validated on the user's Windows machine.
