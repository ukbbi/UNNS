# UNNS_ENTANGLE_PHASE0 v0.1.0

Local-only incremental research package. Does not overwrite `UNNS_ENTANGLE_I_v010`.

The first Phase 0 objective is a frozen q-window check and a falsifiable protocol separating a known quantum reconstruction from any independently derived UNNS principles. Start with `PHASE0_SPEC.md`.

Windows: double click `RUN_WINDOWS.bat`. Other OS: `python -m pip install -r requirements.txt; python -m unittest discover -s tests -v; python src/q_window.py --output output`.

`output/q_table.csv` and `output/phase0_results.json` contain fixed-angle and numerically optimized CHSH results. Optimization is not an analytical upper bound. Source definitions and prior conclusions are in `PHASE0_SPEC.md`.
