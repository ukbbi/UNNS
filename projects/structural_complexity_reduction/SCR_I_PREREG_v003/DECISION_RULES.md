# Decision Rules

For a primary seed × pool-size cell:

- `INDETERMINATE_NO_TARGETS` — independent oracle finds no target-positive candidates.
- `INDETERMINATE_NO_BASINS` — target-positive candidates exist but no frozen-density basin is identified.
- `REPRESENTATION_LOSS` — any frozen basin/class preservation criterion fails.
- `NO_REDUCTION` — basin/class preservation passes but candidate reduction is not positive.
- `STRUCTURAL_COMPRESSION_PRESERVED` — all preservation criteria pass and candidate reduction is positive.

A separate null-comparison layer classifies whether preservation is stronger than rate-matched random pruning. Failure to beat the null does not erase Level-A compression; it prevents a Level-B claim of structurally selective advantage.
