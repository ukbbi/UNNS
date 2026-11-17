# UNNS-SCALE-I Verification Report v001

Overall: **PASS**

## Scripts
| script | exit | seconds |
|---|---|---|
| run_gate1.py | 0 | 2.5 |
| run_gate2.py | 0 | 3.3 |
| run_gate3.py | 0 | 2.6 |
| run_witness.py | 0 | 1.5 |

## Gate verdicts
- Gate 1 (representation): PASS
- Gate 2 (scale embedding, boundary law, obstruction, edge counts): PASS
- Gate 3 slice (distance non-expansion, no T2 violation): PASS
- Gate 4 (complexity): NOT STARTED

## Numbers quoted in THEORY re-checked against result files
- OK  e(10^12)=644932606630
- OK  e(10^6)=643494
- OK  deg(10^6)=64, exits=63
- OK  mean exits 18.9/49.7/87.3/260.2
- OK  strict counts 155/120/159/128/83
- OK  stable pairs 394/394/297/295/151
- OK  certified d(1,2)=5, d(7,8)=4
- OK  witness paths legal
- OK  d(163,164)=6

## Scope notes
- Gate 3 base distances are truncation-stable upper bounds; only d(1,2)=5 and d(7,8)=4 are exactly certified (untruncated lower bounds).
- Gate 3 strict-shortcut frequencies are experimental.
- Frozen releases were not re-run; only definitions and the single value d(163,164)=6 were used as reference.
- No file in the UNNS GitHub repository was changed; nothing was published.
