# TC_EXT_MI_v001 — Result Summary

## Status

**EXTERNAL_VALIDATION_COMPLETE**

The frozen metric hash was verified before the independent dataset was analyzed.

## Site-resolved external test — Fig. 2d

### MBL-DTC, g = 0.97

- detected q0: **2**
- C(q0): **0.954047**
- recurrence-family contrast: **0.947453**
- time-shuffle p_ge: **0.004975**

### Thermal control, g = 0.60

- detected q0: **2**
- C(q0): **0.289673**
- recurrence-family contrast: **0.245186**
- time-shuffle p_ge: **0.298507**

The thermal control still contains a transient q=2 alternation, so q0 alone does not identify a DTC. The frozen support/closure and temporal-order tests separate it strongly from the MBL-DTC record.

## MBL-DTC versus prethermal DTC-like control — Fig. 3a

### MBL-DTC

- detected q0: **2**
- C(q0): **0.448274**
- recurrence-family contrast: **0.395113**
- time-shuffle p_ge: **0.004975**

### Prethermal DTC-like control

- detected q0: **2**
- C(q0): **0.292554**
- recurrence-family contrast: **0.231031**
- time-shuffle p_ge: **0.084577**

Again, both regimes can show q=2. The distinction appears in closure strength, temporal-order significance, and consistency across initial-state combinations.

## Exhaustive pairwise initial-state check

MBL-DTC pairwise family contrast:

**0.395071 ± 0.005517**

with significant temporal-order closure in:

**3/3 pairs**

Prethermal pairwise family contrast:

**0.229498 ± 0.035717**

with significant temporal-order closure in:

**1/3 pairs**

## Interpretation

This independent dataset reproduces the central distinction sought by the project:

**period doubling alone is not enough.**

The frozen metric detects q=2 in the MBL-DTC, thermal transient, and prethermal DTC-like data, but robust supported closure and temporal-order significance are much stronger in the MBL-DTC.

The result is therefore a positive external validation of the frozen temporal-closure concept, with one qualification: the dataset adapter was constructed after inspecting the public CSV layout, so this is not yet a fully preregistered end-to-end validation.
