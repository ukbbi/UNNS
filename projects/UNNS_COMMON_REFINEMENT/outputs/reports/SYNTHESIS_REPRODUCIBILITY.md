# Synthesis Reproducibility

The decisive comparative synthesis is mechanically reproducible.

- Build ID: `a183bee1e553fa9797c91319a0a748bd30f1319c327c75347a311fb73ac243dd`
- Status: **PASS**
- Exact byte-for-byte reproduction of the approved five outputs: `True`
- Integer cases validated: `500`
- Rank-one generator families validated: `793`
- Rank-one canonical counterexamples verified: `513`
- Affine systems checked: `7`
- Conway audited commit: `264445c93b78554c408e99e4e7f663693b4e91ab`

Run on Windows:

```text
scripts\\RUN_SYNTHESIS.bat
```

Or:

```text
python scripts/BUILD_SYNTHESIS.py
python scripts/BUILD_SYNTHESIS.py --check
```

The build fails if a pinned input changes, an evidence invariant fails, or a generated artifact differs from the approved baseline.
