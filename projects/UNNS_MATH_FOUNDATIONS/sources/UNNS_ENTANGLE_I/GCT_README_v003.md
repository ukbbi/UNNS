# GCT-III — Observable-Null Refinement Audit v003

This is an **incremental overlay** for the existing innermost `UNNS_ENTANGLE_I` directory. It does not overwrite GCT v001, v002, or Chamber XVI files.

## Install

Extract the archive's contents directly into your project root, merging the existing `config`, `docs`, `src`, `tests`, and `output` folders. No replacement of earlier files is required.

## Run (Python 3.12; no dependencies)

```cmd
python -m unittest discover -s tests -p "test_gct_null_refinement_v003.py" -v
python -m src.gct_null_refinement_v003
```

The report is `output/GCT_NULL_REFINEMENT_v003.json`.

## Results

The source-constrained countermodel satisfies nontrivial recurrent refinement, an exact observable morphism, rotational covariance, bilinearity, simultaneous refinement invariance, and elementary aligned anticorrelation. It **violates** the observable-null interaction condition, with `Pi(X)=0` and `B(X,Y)=-1`.

**Verdict:** `NOT_ENTAILED_BY_DOCUMENTED_UNNS_AXIOMS`.

The conclusion is an insufficiency of the checked axioms. It does not disprove all possible UNNS entanglement models, and it does not derive the Born rule. Do not promote this result to physical certification.

## Integrity

The exact user-supplied GCT v002 JSON is frozen under `docs/frozen/GCT_JOINT_ORIGIN_v002.json`; the runtime records its SHA-256 and checks its negative verdict. The original v002 source/outputs remain unchanged.
