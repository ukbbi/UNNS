# STRUC_BRIDGE

Stage-2 bridge from the frozen CEA_2017 VREF-I/B extraction to canonical STRUC-I v1.0.4 and STRUC-PERC-I v2.5.0.

## Merge location

Extract this package into the root of:

```text
UNNS_VACUUM_CONTINUITY/
```

## Input ladders

```text
data/derived/struc_bridge/
├── R1_NATIVE.csv
├── R2_NATIVE.csv
├── R1_COMMON.csv
├── R2_COMMON_LIN.csv
└── R2_COMMON_PCHIP.csv
```

All five are one-column numeric CSV ladders and can be loaded directly by both canonical chambers.

## Order

1. Read `stage2/STRUC_BRIDGE_FREEZE.md`.
2. Run STRUC-I v1.0.4 with all five ladders and the frozen controls.
3. Save exports under `output/struc_bridge/struc_i/`.
4. Run STRUC-PERC-I v2.5.0 in Batch Mode with the same five ladders.
5. Save exports under `output/struc_bridge/struc_perc_i/`.
6. Upload the four required exports for bridge synthesis.

Do not modify either chamber.
