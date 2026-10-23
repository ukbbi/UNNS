# XVI Tau Evolution v001 — Incremental nonlinear audit

**Install:** Extract the ZIP directly into the existing innermost `UNNS_ENTANGLE_I` project root. Merge directories, **do not overwrite existing files**. Do not extract another nested project folder. All package paths are new. The original Chamber XVI HTML and Phases 0–3 remain unchanged.

**Important:** This phase is an attempted **certification**, not a guaranteed positive result. The full 180-step run found obstructions and is reported honestly as `FULL_TAU_CERTIFICATION_NOT_ESTABLISHED`.

The existing project must contain the earlier repaired projector `src/xvi_projection_repair_v001.py`, the source-locked HTML at `docs/sources/XVI_ENGINE_v084.html`, and NumPy from `requirements_XVI_REPAIR_v001.txt`.

From Command Prompt in the project root (no batch file required):

```cmd
python -m pip install -r requirements_XVI_TAU_v001.txt
python -m unittest discover -s tests -p "test_*.py" -v
python -m src.xvi_tau_evolution_v001
```

The final command regenerates `output/XVI_TAU_EVOLUTION_v001.json` without modifying frozen baselines. `--quick` runs a **24-step diagnostic only**; it is not comparable to the precomputed 180-step results.

For an **optional original-source JavaScript witness** (requires Node.js installed, not essential for the Python run):

```cmd
python -m src.xvi_tau_evolution_v001 --js-input-only
node tools/xvi_tau_js_witness_v001.cjs
```

This recreates `output/XVI_TAU_JS_INPUT_v001.json` and `output/XVI_TAU_JS_WITNESS_v001.json`. Node executes the byte-locked original JavaScript class and compares the 24-step final τ arrays with the Python source translation on two predetermined smooth inputs. Setting `eng.sigma=0` after construction is deliberate; HTML uses a truthy default for `sigma` and cannot otherwise be configured with zero noise. No JS application is modified.

## Key files

* `config/XVI_TAU_LOCK_v001.json` — byte-level frozen baseline and original HTML SHA-256.
* `docs/frozen/XVI_PROJECTION_REPAIR_v001.json` — original uploaded report, byte-identical.
* `docs/XVI_TAU_SPEC_v001.md` — frozen hypotheses, procedure, gate definitions, mathematical limitations.
* `docs/XVI_TAU_FINDINGS_v001.md` — precomputed findings, including failures and remaining obligations.
* `src/xvi_tau_evolution_v001.py` — runnable deterministic source-grounded nonlinear comparator.
* `tests/test_xvi_tau_evolution_v001.py` — 17 automated checks; scientific gates are separate.
* `tools/xvi_tau_js_witness_v001.cjs` — optional original HTML JS corroboration.
* `output/XVI_TAU_EVOLUTION_v001.json` — full 180-step result generated and preserved; replay locally.
* `output/XVI_TAU_JS_INPUT_v001.json` / `output/XVI_TAU_JS_WITNESS_v001.json` — precomputed short direct-JS crosscheck.
* `MANIFEST_XVI_TAU_v001.json` — file inventory with SHA-256.

## Outcome boundary

The repaired flux projector remains an independently certified mathematical component. End-to-end τ evolution has **not** yet met all preregistered numerical conditions (T2, T4), and Chamber's μ*, p, R² and entropy invariants have not been independently certified (T5). This phase must **not** be described as proof of Born's rule, quantum entanglement, physical unitarity, or unconditional XVI closure.
