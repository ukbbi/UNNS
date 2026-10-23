# XVI_SPECTRAL_CONDITIONING_v001

Incremental ZIP overlay for the **existing innermost** `UNNS_ENTANGLE_I` project. Do not create a nested project or replace earlier files.

## Local Windows execution (Python 3.12)

Extract the ZIP into the project root. The source witness and precomputed report are included; Node.js is **optional**.

```cmd
python -m unittest discover -s tests -p "test_*.py" -v
python -m src.xvi_spectral_conditioning_v001
```

Output: `output\XVI_SPECTRAL_CONDITIONING_v001.json`.

Optional direct replay of the **original** JS engine, when Node.js is available:

```cmd
node tools\xvi_spectral_source_probe_v001.cjs
python -m src.xvi_spectral_conditioning_v001
```

The Node probe reads the locked original HTML class and writes **new** raw-field snapshots and the original JS spectrum on them. It does not alter the HTML. Replaying is deterministic for the recorded seed and zero-noise configuration.

## Scientific verdict

The previous **`INVARIANT_FIDELITY_NOT_CERTIFIED`** is frozen unchanged, including its failed spectral conditions. Fresh source-executed fields permit a like-for-like JS-versus-Python comparison without confounding different raw arrays. The original all-bin fit is retained and evaluated; the separately conditioned fit has fixed independent bin-support rules. Calibrated power-law, narrowband, and white-noise nulls expose which fitted slopes are actual signals versus derivative and algorithm artifacts. A suitable fit does **not** prove UNNS structural invariance or the Born rule.

## Files

- `docs/frozen/XVI_INVARIANTS_AUDIT_v001.json` — exact user-uploaded negative baseline, SHA-256 locked
- `config/XVI_SPECTRAL_LOCK_v001.json` — baseline/source SHA and claim limits
- `docs/XVI_SPECTRAL_SPEC_v001.md` — immutable source formulas, gates, thresholds, limitations
- `docs/XVI_SPECTRAL_FINDINGS_v001.md` — outcome and unresolved issues
- `src/xvi_spectral_conditioning_v001.py` — deterministic evaluation + report
- `tools/xvi_spectral_source_probe_v001.cjs` — optional direct engine raw-field exporter
- `tests/test_xvi_spectral_conditioning_v001.py` — 20 tests
- `output/XVI_SPECTRAL_SOURCE_RAW_v001.json` — 4 source-executed raw τ-field snapshots + native JS spectra
- `output/XVI_SPECTRAL_CONDITIONING_v001.json` — precomputed audit (reproducible)
- `MANIFEST_XVI_SPECTRAL_v001.json` — complete file hashes and software verification

No existing `README.md`, `RUN_WINDOWS.bat`, earlier phases, original Chamber XVI, or existing report are overwritten.
