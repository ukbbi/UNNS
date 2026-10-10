# PREFLIGHT_v004 — original Dryad function cross-check

Add files without replacing or editing older preflights:
- `source_probe_v004.cpp` and `validate_v004.py` → `scr_iii_b/reference_check/`
- `SOURCE_PROVENANCE.md` → `scr_iii_b/reference_check/`

From the **project root** in Ubuntu/WSL:

```bash
python3 scr_iii_b/reference_check/validate_v004.py
```

Writes `scr_iii_b/output/validation/v004/REFERENCE_RUN_v004.json` and `.md` and compiled probe binary. Requires `g++` and Python 3; no Python packages or Windows executable needed. `validate_v004.py` uses the existing `models/physical_energy.py` and `reference_check/validate_v002.py` geometry helpers without running v002 or overwriting its output.

**Scope:** Three functions copied verbatim from the original SPMMC v1.00 source, plus a new minimalist geometry driver, compared against independent Python pair calculation for L=1/2/3. Absolute physical energy and full-source simulation are *not* validated. Do not freeze SCR-III-B spec or preregistration yet. SCR-III-A remains untouched.
