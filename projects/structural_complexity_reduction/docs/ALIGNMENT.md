# Alignment Check — 2026-10-07

## Canonical scientific state

- Active preregistration: `SCR_I_PREREG_v003`
- Active engine: `src/scr_i_v003/`
- Active adapter: `adapters/scr_i_a_v003_adapter.py`
- Active dashboard: `SCR_I_DASHBOARD v003`
- Primary run: `COMPLETE`, 15/15
- Consolidated result: present under `output/reports/v003/` and `output/exports/v003/`
- Frozen outcome: `STRUCTURAL_COMPRESSION_CONFIRMED_ABOVE_REPRESENTATION_FLOOR`

## Historical state

- v001/v002 preregistrations preserved read-only under `archive/prereg/`;
- only decisive v001/v002 transition audit records remain under `archive/history/`;
- superseded v001/v002 engines, installers, temporary patch notes and generated caches removed from the active tree.

## Reproducibility

- pinned v003 source files retained under `references/source_lock/`;
- design audit retained under `output/v003_phase1/`;
- completed checkpoint retained under `output/checkpoints/`;
- raw primary/null/timing/gate outputs retained;
- final consolidation retained;
- root SHA-256 inventory regenerated after cleanup.

## Primary-rerun protection

The dashboard and canonical runner now recognize the completed primary state and block a rerun.

## Remaining intentional open item

UPI remains blinded and has not yet been used in the primary analysis. Any UPI association study must be a separately declared secondary analysis.

## Non-blocking compatibility notes

Two residual issues are explicitly documented rather than hidden:

1. The frozen result schema names the baseline basin-count field `basin_count_base`, while the completed runner writes `basin_count`. The quantity is the same; see `SCHEMA_COMPATIBILITY.md`.
2. Negative-space persistence is aggregate (`gate_audit_v003.csv`) rather than candidate-level. This does not enter the frozen v003 primary verdict; see `NEGATIVE_SPACE_STATUS.md`.

No other active-path version conflicts were found after cleanup.
