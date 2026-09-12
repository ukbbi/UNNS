# PROSPECTIVE CAMPAIGN PROTOCOL — MC_GRAMMAR_v001

## Purpose

Test the frozen grammar on previously unused candidate/control data.

## Before candidate data are opened numerically

1. Register candidate and matched control identities/provenance.
2. Confirm neither was used in development, selection, null qualification, or freeze.
3. Confirm source-defined two-clock metadata and time-domain observables exist.
4. Hash original source files.
5. Define a neutral adapter using source metadata only.
6. Lock the adapter before computing grammar coordinates.

## Blind / firewall sequence

`ingest -> neutral adapter -> analysis -> audit -> quantitative lock -> reveal`

Where feasible, candidate/control identity should be hidden from the metric runner.

## Frozen computation

Use exactly:

- `rep_study_v002.py` representation formulas;
- `grammar_dev_v001.py` null procedures;
- `MC_GRAMMAR_v001` gates and state logic.

No response-frequency fitting.
No threshold tuning.
No null replacement.
No selective robustness omission.

## Required outputs per record

- domain eligibility;
- ratio-domain eligibility;
- `P_src` and phase-label null probability;
- `J_frac`;
- `M_frac`;
- Fourier-phase null probability;
- all six robustness M values;
- temporal state;
- all failure flags;
- separate collective annotation if legitimate.

## Lock before reveal

Hash:

- canonical ingest;
- all numeric outputs;
- audit;
- temporal states.

Only after those hashes are written may candidate/control identity be revealed and interpreted.

## C003

C003 remains prohibited during the prospective campaign.

Only after prospective reveal is complete may C003 be evaluated under the unchanged frozen
grammar.
