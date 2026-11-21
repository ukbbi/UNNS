# QTI-I v002 register
| ID | Result | Status |
|---|---|---|
| D1 | Raw .pt = LE uint64 timestamps; 72 streams, 108,976,996 events; v001 hashes reproduced | VERIFIED |
| D2 | All 72 streams fit the 312.5-unit counter (max round-off 4.5) | COMPUTED |
| D3 | ps streams: gap gcd 20000 (6/12) => counter gaps multiples of 64 => fully squareful; follows from clock-lift inclusion | PROVED consequence + COMPUTED |
| D4 | i1, i2, s, iPsiM, iPsiP: R, F, merger statistics indistinguishable from integer and exponential controls (pooled |z|<2.4) | COMPUTED, exploratory |
| D5 | iPsiM aligned with ps (>=99.6% within 2e7; median offset 8.41e6-1.08e7); iPsiP not | COMPUTED, descriptive |
| D6 | "All raw gaps divisible by 4" is not universal (5/12 per channel) | COMPUTED; corrects v001 wording |
| O16-O19 | channel-aware nulls; iPsiP offset; per-run stability; metadata | OPEN |
