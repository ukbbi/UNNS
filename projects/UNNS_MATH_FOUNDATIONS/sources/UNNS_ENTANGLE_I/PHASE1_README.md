# Phase 1 overlay — XVI_CLOSURE_THEOREM_v001

Extract this ZIP **into the existing `UNNS_ENTANGLE_I` folder** (the folder containing `src`, `docs`, `tests`, `output`). It intentionally contains no top-level project folder and does not replace Phase 0, the original `RUN_WINDOWS.bat`, or canonical Operator XVI.

Run `RUN_XVI_v001.bat` on Windows, or from the project root run:

```bash
python -m unittest discover -s tests -p 'test_xvi_closure_v001.py' -v
python -m src.xvi_closure_v001 --output output/XVI_CLOSURE_v001.json
```

The result is a **negative theorem finding**: rotation-averaging recursion derives rotational symmetry but not orthogonal refinement conservation. All radial power weights are fixed points. The rule selecting q=2 still requires a separate derivation from the real UNNS Operator XVI. See `docs/XVI_CLOSURE_THEOREM_v001.md` before interpreting results.
