# UNNS Entanglement I — Canonical XVI Bridge v001

**Incremental overlay:** unzip directly into the **innermost** `UNNS_ENTANGLE_I`
project directory where `src/`, `tests/`, `docs/`, `config/`, `output/` live.
Merge folders; this ZIP has no collisions with earlier numbered work.

**Never overwrite the historical Phase 3/2C/2B/2/1/0 reports.** Their locked
copies and original XVI source live under `docs/frozen/` and `docs/sources/`.
The manifest and integrity checks are provided in `config/` and `MANIFEST_XVI_BRIDGE_v001.json`.

## Run using the already-working Python 3.12 Command Prompt

```cmd
python -m unittest discover -s tests -p "test_*.py" -v
python -m src.xvi_canonical_bridge_v001
```

Report path: `output\XVI_CANONICAL_BRIDGE_v001.json`.

Optional (only when Node.js is installed; **not required**):

```cmd
node tools\xvi_original_engine_probe_v001.cjs
```

The optional Node probe calls **original, unchanged JS** from the frozen HTML.
The Python-only audit reproduces its Fourier mode calculation algebraically.
No internet, pip installations, or administrator permissions are required.
Do not disable Windows Smart App Control to run a batch launcher.

## Scientific outcome
The source-locked v0.8.4 engine fails the exact Helmholtz projection condition
for a known longitudinal Fourier mode. At grid 64/128/256 the source leaves
~90.2/95.1/97.5% residual divergence. An ideal spectral comparator eliminates
this mode; this is a discretization inconsistency, not a Born rule derivation.
`B5/B6` remain blocked. The original chamber remains untouched.

**No fictitious quantum evidence. No silent operator fixes.**
