# UNNS-SCALE-I v010 verification report

mode: full

- PASS: window scan file: 999999 records, n = 1..999999 contiguous
- PASS: window scan: 2997 pairs have a <=4-step route inside [1,10^12], 997002 pairs have none (disjoint restricted radius-2 balls); summary file agrees
- PASS: first failing pair n = 683; all n <= 682 pass (boundary of the in-window four-step regime)
- PASS: meeting vertices of passing pairs are <= 10^12
- PASS: independent Python (exact_lib) restricted balls on 609 pairs (random fail/pass + exhaustive n<400): disagreements 0; every passing route edge-checked and <= 10^12
- PASS: n=5: no <=4-step route with ceiling 6,230,015; route with ceiling 6,230,016 = (5000000, 39680, 6230016, 230400, 6000000)
- PASS: fresh g++ rebuild of ball.cpp reproduces stored records on 4 blocks
- PASS: H4 sample (2005 n): H4 <= 10^12 exactly for the pairs that pass the window scan
- PASS: window-distance sample (62 n): d_W <= 4 exactly for passing pairs; d_W >= 5 (or > 10) otherwise
- PASS: n=683: window distance exactly 5 (radius-3/radius-2 balls meet; radius-2/radius-2 balls do not)
- PASS: n=5: 3-step shortest route has minimum height 732,050,000 (v009 data) while allowing 4 steps drops the ceiling to 6,230,016
- PASS: baselines v001-v009 unchanged (read-only hashing)

## Baselines
- v001: OK
- v002: OK
- v003: OK
- v004: OK
- v005: OK
- v006: OK
- v007: OK
- v008: OK
- v009: OK

ALL CHECKS PASS
time 111 s