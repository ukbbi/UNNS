# Blind Mode

Blind Mode prevents the chamber from using the experiment's known physical
classification while producing its verdict.

1. Put only neutral identifiers and measured evidence in the candidate bundle.
2. Keep the physical class / expected answer in a separate `ground_truth.json`.
3. Run:
   `python run_external.py candidate.zip output --blind`
4. The chamber writes `blind_verdict.json` and `analysis_lock.json`.
5. Only after those files exist run:
   `python reveal_external.py output ground_truth.json`
6. `posthoc_comparison.json` records the locked blind verdict versus the revealed answer.

The analyzer ignores a manifest label in Blind Mode and displays only the
candidate ID.
