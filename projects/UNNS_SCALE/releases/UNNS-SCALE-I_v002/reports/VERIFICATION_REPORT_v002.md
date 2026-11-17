# UNNS-SCALE-I v002 Verification Report

Overall: **PASS**

## Scripts
| script | exit | seconds |
|---|---|---|
| run_A_boundary.py | 0 | 3.5 |
| run_B_composition.py | 0 | 3.4 |
| run_C_information.py | 0 | 5.2 |
| run_W_window.py | 0 | 5.8 |

## Part verdicts
- Part A: PASS
- Part B: PASS
- Part C: PASS
- Part W: PASS
- Part D (distance supremum): not started
- Gate 4: deferred

## Numbers quoted in THEORY v002 re-checked against result files
- OK  c_B-1 for B=10^6 equals 22.2
- OK  slope(10^6) within 0.01 of 22.2
- OK  A2 total error < 0.01 at X=4e6 for all B
- OK  A2 table values (mean at 4e6: 27.9522, 39.5917, 160.9865, 126.4490, 379.7874)
- OK  A1 zero mismatches, 13 B values
- OK  B1 zero mismatches, 9 pairs
- OK  B2 zero mismatches, 9 chains
- OK  10^12 profiles 153,63,1 / 112,72,32,1
- OK  C: threshold 10 for 10^6; 9 steps not injective; 10 injective
- OK  C: C1 formula mismatches 0
- OK  W: 10^6 has 63 infinite exits, 62 in window; beyond-window neighbour 1000002000001
- OK  W: vertex 10^12 deg 217, window degree 48 (15 in-lattice + 33 exits)
- OK  W: trillion table 10^6 (643,494 / 20,054,629)
- OK  W: trillion table 10^3 (644,887,919 / 6,193,421,292)
- OK  W: trillion table 10^4 (64,478,820 / 1,128,650,367)
- OK  W: infinite exit total 349,007,877; lost 328,953,248
- OK  W: 'both' = e(floor(L/B)) for the three trillion rows
- OK  W: edge-class closed form equals brute force (8 pairs)

## Baseline protection
- v001: all v001 files match ../SHA256SUMS.txt
- scale_lib.py identical to v001 copy: True
- scale_lib.py sha-256: 436d6a850aa6fdb3bff89712cad96887ed6e9bd69e198ad19a4bd35f5f6f75d5

## Scope notes
- The asymptotic law (A4) is proved; the sieve measurements are numerical confirmation up to X = 4,000,000.
- Theorem C concerns deterministic exact reproduction of one move's outer trajectory; it makes no claim about approximate or stochastic models.
- Trillion-window rows come from the proved edge-class formula (checked against brute force at smaller (L, B)); no trillion-scale enumeration was performed.
- No GitHub changes; nothing published.
