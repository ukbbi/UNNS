# SCR-II v002 Primary Runner v001

## Purpose

This package adds the outcome-bearing primary runner for the already frozen `SCR_II_PREREG_v002`.

It does not modify:

- the v002 multiplicity band;
- the v002 grammar;
- any v002 seed;
- any success threshold;
- the v001 closure record;
- the SCR-I result.

## Primary grid

- depth 14: 10 frozen seeds;
- depth 16: 10 frozen seeds;
- depth 18: 10 frozen seeds.

Total: 30 cells.

## Per-cell outputs

Each cell records:

- exact baseline solution count and hash;
- exact SCR solution count and hash;
- exact set equality;
- exact-solution recall;
- any extra SCR solutions;
- node and leaf counts;
- node and leaf reduction;
- baseline and total SCR runtime;
- structural-filter runtime;
- time gain;
- C1 solver-native exactness/runtime;
- gate first-rejection counts.

## Run behavior

The runner completes all 30 cells even if the first cell already fixes the primary verdict as `PRESERVATION_FAIL`. This is deliberate: the full grid measures the systematic depth dependence of non-transfer.

A Windows-safe checkpoint is written after every completed cell.

If interrupted, rerun the same batch file to resume.

After `PRIMARY_RESULT_v002.json` is created, a second primary run is refused.

## Before running

First run:

`RUN_SCR_II_V002_PRIMARY_TEST.bat`

This regression uses only a design-audit seed and confirms that the runner is installed without exposing any v002 primary seed.
