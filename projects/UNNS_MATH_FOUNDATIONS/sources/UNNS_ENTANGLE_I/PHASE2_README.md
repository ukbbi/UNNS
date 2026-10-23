# UNNS_ENTANGLE_I — Phase 2 incremental overlay

Merge the **contents** of this archive into the existing innermost `UNNS_ENTANGLE_I/` folder. It uses `docs/`, `src/`, `tests/`, `config/`, and `output/` only; **no Phase 0 or Phase 1 files are overwritten**. Original canonical XVI remains unchanged.

Commands from project root (no batch file required):

```cmd
python -m unittest discover -s tests -p "test_*.py" -v
python -m src.xvi_refinement_v001
```

The Phase 1 uploaded JSON is saved at `output/frozen/XVI_CLOSURE_v001.json`, with the exact hash in `config/PHASE2_LOCK.json`. The primary theorem is *blocked* until the authentic canonical XVI definition/source can be supplied and mapped. This is deliberate: testing a new surrogate would not establish a canonical theorem.
