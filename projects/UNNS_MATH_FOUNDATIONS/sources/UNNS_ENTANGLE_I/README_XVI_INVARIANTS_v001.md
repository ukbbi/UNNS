# XVI_INVARIANTS_AUDIT_v001

Incremental, **local-only** invariant-fidelity audit for `UNNS_ENTANGLE_I`.

## Install (do not make an extra nested project folder)

Extract directly into the **innermost** `UNNS_ENTANGLE_I` directory, merging `src/`, `tests/`, `config/`, `docs/`, `output/`, `tools/`. This overlay adds **new filenames only**. It does not modify the original Chamber XVI HTML, Phase 0–3 files, or prior scientific reports.

Python 3.12 + NumPy required (installed by prior grid phase). Windows Command Prompt in the project root:

```cmd
python -m unittest discover -s tests -p "test_*.py" -v
python -m src.xvi_invariants_audit_v001
```

Outputs: `output/XVI_INVARIANTS_AUDIT_v001.json` and the included source-JS comparison fixture/witness. If Node.js is installed, optionally rerun the original, **unmodified** JavaScript diagnostic formulas on the stored common fields:

```cmd
node tools/xvi_invariants_js_probe_v001.cjs
```

Node is NOT necessary to execute the Python audit or tests; a reference witness from direct Node execution is already included and checked.

## Locked inputs

- Exact uploaded `XVI_GRID_SCALING_v001.json` preserved at `docs/frozen/XVI_GRID_SCALING_v001.json`.
- Original HTML at `docs/sources/XVI_ENGINE_v084.html` and all four archived original JSON exports are SHA-256 checked before the audit can run.
- Previous verdict `FULL_TAU_CERTIFICATION_NOT_ESTABLISHED` is retained in the frozen prior grid report. The grid candidate was a `LIMITED_PHYSICAL_GEOMETRY_WITNESS` only.

## The scientific result

`INVARIANT_FIDELITY_NOT_CERTIFIED`.

The audit runs the original *definitions* of μ★ scale-mismatch minimization, 2-D FFT radial spectral slope (p, R²) and 50-bin histogram entropy on the new fixed-domain candidate plus no-closure and diffusion-only controls. It does NOT change the source formulas to obtain favorable results.

- The original export files contain post-run metrics but **no raw τ field**: their individual numerical metrics cannot be independently recomputed. I2 remains **BLOCKED**.
- Restricted μ search includes φ by construction, and some tests select the upper search boundary. A numerically close μ is not a demonstrated scale attractor.
- Unfiltered log spectrum produces numerically unstable p/R² values; direct original-JS-versus-NumPy comparison agrees for μ and entropy but **fails strict p/R² parity** on the same 64² arrays. This is itself a material numerical finding. Neither numerical implementation's p is given physical-invariant status.
- The tested candidate retains ~89% of its initial spatial variation; no-closure and diffusion-only controls also retain substantial variation. The closure correction produces a distinguishable field but its invariants are not certified.
- Tail entropy changes are small for the candidate and its controls; this is a **non-specific** property of these finite smooth-field runs, not quantum information entropy and not proof of original Chamber C4.
- The source HTML checks for p near +2.28, while the four original JSON exports report negative p approximately −3. This discrepancy is recorded without a sign flip or threshold redefinition.

The full canonical τ evolution remains **uncertified**, and the Born rule is **NOT DERIVED**.

## Inventory

- `docs/XVI_INVARIANTS_SPEC_v001.md` — source-grounded definitions and frozen gates
- `docs/XVI_INVARIANTS_FINDINGS_v001.md` — key quantitative results, limitations and next steps
- `docs/CTX_XVI_INVARIANTS_v001.md` — continuity and no-overwrite guidance
- `config/XVI_INVARIANTS_LOCK_v001.json` — exact source and baseline SHA-256 checks
- `docs/frozen/XVI_GRID_SCALING_v001.json` — byte-identical user-uploaded baseline
- `src/xvi_invariants_audit_v001.py` — complete deterministic experiment and report CLI
- `tests/test_xvi_invariants_audit_v001.py` — 20 new tests including explicit fail-gate preservation
- `tools/xvi_invariants_js_probe_v001.cjs` — optional original-engine direct comparison
- `output/XVI_INVARIANTS_JS_FIXTURE_v001.json` — locked-size common array samples for parity
- `output/XVI_INVARIANTS_JS_WITNESS_v001.json` — direct original-JS calculations
- `output/XVI_INVARIANTS_AUDIT_v001.json` — complete precomputed scientific report
- `MANIFEST_XVI_INVARIANTS_v001.json` — file list and checksums

No placeholder scripts, no source edits, no new quantum physics claims.
