# CORR-I v0.1.2

CORR-I v0.1.2 adds genuine multi-channel batch execution while preserving the v0.1.1 single-channel analysis.

## New in v0.1.2

- Select **multiple CSV files at once**, or load one wide multi-channel CSV.
- `RUN BATCH + ZIP` analyzes every loaded channel using the same visible chamber settings.
- A single ZIP is downloaded automatically.
- The ZIP contains, for every channel:
  - `corr_i_<channel>.json`
  - `corr_i_<channel>_envelope.csv`
- The ZIP also contains:
  - `batch_summary.csv`
  - `batch_record.json`
  - `README.txt`
- A batch summary table remains visible in the chamber after the run.
- Duplicate channel names from separate files are automatically disambiguated.

## Existing behavior retained

The baseline positivity / monotonicity / log-convexity / Hankel tests and the v0.1.1 `alpha_max(mu)` envelope are unchanged.

## Current gapless-family experiment

You may select `p05.csv`, `p2.csv`, `p4.csv`, and `p8.csv` simultaneously, then click:

`RUN BATCH + ZIP`

No manual channel-by-channel reruns are required.

## Files

- `corr_i_v012.html` — standalone offline chamber.
- `corr_i_selftest.csv` — original single-channel self-test.
- `corr_i_batch_selftest.csv` — three-channel batch ingestion test.
- `PROTOCOL.md`
- `CHANGELOG.md`
- `SELFTEST_RECORD.json`
- `manifest.json`
