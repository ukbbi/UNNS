# UNNS Relational Invariants — UNNS_RELATIONAL_I

**Status:** RGG-1 baseline preserved; RGG-2 is the active, focused investigation.
**Date:** 2026-10-21. **Scope:** integer-anchor nest routes only.

Purpose: advance *Observable Equivalence and Relational Invariants in Recursive Generative Systems* with explicitly defined route operations, rather than inventing a separate comprehensive grammar. New constructs are introduced only to solve specific mathematical questions and are labelled as proposed, proved, or checked.

## What is included
- `baseline/`: unchanged, available RGG-1 files and the 43-page v2 manuscript. The original `verify_ri.py` was **not among the available uploads**, so it is not included. `baseline/README.md` records this.
- `rgg2/SPEC.md`, `rgg2/THEOREMS.md`: precise candidate operations and proofs of the Phase I–III statements.
- `rgg2/src/`: executable reference implementations with Python standard library only.
- `rgg2/tests/`: deterministic regression, edge-case, and adversarial checks.
- `rgg2/run_report.py`: generates numeric JSON/CSV and a compact SVG example figure.
- `rgg2/synthesis/`: current claims, interpretation and manuscript insertion plan.
- `manuscript/REVISION_PLAN.md`: controlled extension procedure; manuscript is not modified.

## Windows quick start
From File Explorer open `rgg2/` and double-click **RUN_TESTS.bat**, then **RUN_REPORT.bat**. Or use a terminal:

```powershell
cd rgg2
python -m unittest discover -s tests -v
python run_report.py
```

Generated files appear under `rgg2/output/`.

## Scientific scope
The original nest operation is `M ⟂ N = M(N+1)^2/N`. Integer-anchor routes are `(k,d)` with `d=N+1 >= 2` and `M=kN`; their value is `v(k,d)=k d^2`. `J_join(r,s)` is **a proposed new operation**, not an inferred physical interaction. Exact theorems conditional on this definition are distinguished from independent empirical evidence. Jointly covariant refinement on partial domains does **not** by itself establish a physical law or the linear hypotheses of the existing manuscript.

The original manuscript is unchanged. No GitHub repository is touched.
