# TEL-FINGERPRINT-I Chamber v0.1.0 — Operation guide

## 1. Start

Windows:

```text
RUN_TEL_FINGERPRINT_I_CHAMBER.bat
```

Or open directly:

```text
TEL_FINGERPRINT_I_CHAMBER_v0_1_0.html
```

The chamber is a standalone local HTML application and loads no external code.

## 2. Engineering check

Click:

```text
LOAD ENGINEERING DEMO
```

Then:

```text
RUN FINGERPRINT ANALYSIS
```

The demo exists only to verify schema, trajectory analysis, retrieval, controls, charts, and exports. It is not quantum-teleportation evidence.

## 3. Real input

Prepare one CSV according to `INPUT_SCHEMA.md`.

Every perturbation group must contain exactly:

```text
PHI_PLUS
PHI_MINUS
PSI_PLUS
PSI_MINUS
```

The CSV must already contain conventionally derived and physically validated invariants. The chamber does not reconstruct them from counts or matrices.

## 4. Thresholds

Prototype defaults:

```text
Closed pairwise maximum       0.05
Connected-graph edge          0.15
```

Any exploratory change is recorded in the result JSON. Confirmatory work requires a separately accepted protocol that freezes thresholds before results are inspected.

## 5. Run

The chamber validates:

- required columns;
- finite physical values;
- Choi and probability ranges;
- descending PTM singular values;
- `physicality_pass`;
- exact four-route completeness;
- at least two physical perturbation levels per trajectory.

Invalid input is not analyzed.

## 6. Inspect

The interface reports:

```text
trajectory verdicts
route-class diameter curves
scenario consensus
route-label permutation control
deterministic lambda-thinning control
leave-one-coordinate-out sensitivity
leave-one-realization-out retrieval, when identifiable
```

## 7. Export

Preserve all applicable files:

```text
TEL_FINGERPRINT_I_RESULT_RECORD.json
TEL_FINGERPRINT_I_LAMBDA_SUMMARY.csv
TEL_FINGERPRINT_I_PAIR_DISTANCES.csv
TEL_FINGERPRINT_I_TRAJECTORY_SUMMARY.csv
TEL_FINGERPRINT_I_RETRIEVAL.csv
TEL_FINGERPRINT_I_CONTROLS.csv
```

Do not rename an engineering demo export as a scientific run.

## 8. Package verification

Run:

```text
RUN_VERIFY_PACKAGE.bat
```

This verifies the bounded package structure and engine-lock markers. It does not validate browser execution or scientific data.