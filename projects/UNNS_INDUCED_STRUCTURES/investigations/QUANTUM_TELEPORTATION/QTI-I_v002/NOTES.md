# QTI-I v002 - QTI-I/A on the complete raw data (both zips, 72 streams)

Scope: research notes. Substrate fixed (T_N(x)=x(N+1)^2/N, N|x). External system A = detector event-time streams. phi unchanged from v001: t -> counter k=floor((2t+312)/625), gap h=k_{i+1}-k_i>0, gaps >1000*median excluded. Induced object: history structure of h (R, F, depth, mergers). This is a statement about timestamp structure under phi, not about the teleportation mechanism (QTI-I/B still needs a defined correspondence).

## Data (verified)
- `Short distance.zip` and `1 km.zip`, 36 `.pt` members each; 6 channels (i1, i2, s, ps, iPsiM, iPsiP) x 6 data sets (data110 x2 settings, data155 x2, dataE pole1, dataL pole2). 108,976,996 events in all.
- Format: flat little-endian uint64 timestamps, no header; events = bytes/8 (matches the manifest). Native unit not documented; picoseconds is an assumption.
- The three v001 extracts sit in `Short distance.zip/data110`; their SHA-256 hashes match SOURCE_MANIFEST.md, and v002 reproduces the v001 analysed-gap counts (C2). `Repetition rate.zip` is not present.
- Grid: every stream fits the 312.5-unit counter (max round-off 4.5 units; ps streams <=2). Raw gaps are divisible by 4 in only 5/12 streams of each non-ps channel, so the v001 statement "all raw gaps divisible by 4" holds for the three v001 streams and some others, not universally (C5).

## Results
1. **ps is a clock channel, and its structure is exactly the lift theorem (C3).** 6 of 12 ps streams have raw gap gcd 20000; counter gaps are then multiples of 64 = 8^2, so every gap has incoming edge m=8 (R>=3). P(R>0)=P(R>=2)=P(merger)=1.0 in those, 0.9995-1.0 in the other six. This follows from W(d) subset W(hd) with h=64, and does not depend on the physics.
2. **All other channels (i1, i2, s, iPsiM, iPsiP; 60 streams) match the controls.** Pooled over streams (4000-gap sample each): P(R>0)~0.39, P(R>=2)~0.115-0.118, P(merger)~0.075-0.080 in observed data and both controls (magnitude-matched +-10% integers; exponential, same mean). Pooled z (jitter/exp): R>0 +0.8/+2.4, R>=2 -0.5/-0.8, merger -1.6/-0.7. |z|>3 counts out of 180 tests per control: 3 (jitter), 6 (exp); chance would give ~0.5, so the exponential control (different shape) shows a mild excess that I read as control mismatch, not signal; no multiplicity correction.
3. **Channel alignment (descriptive).** at least 99.6% of iPsiM events have a ps event within 2e7 time units, with median offset 8.41e6 to 1.08e7 across the 12 data sets; iPsiP events do not (0.2-0.7% within 2e7). So iPsiM times are tied to the ps clock while iPsiP times are not; I do not interpret this physically.
4. Lift monotonicity (d->4d never lowers F) holds on every stream sample (T1 check).
5. Independent full-stream recomputation (trial-division, no sympy) agrees with the sampled P(R>0) on 7 streams (C1).

## Limits / not established
- Only 4000 gaps per stream enter F/depth/merger (cost of exact factorisation); P(R>0) was checked on full streams for 7 only.
- Controls are marginal-distribution controls; no channel-aware, rate-preserving or dead-time-aware null yet. No pre-registered threshold.
- phi's 312.5 grid is a numerical reconstruction, not a certified hardware clock. Absence of a signal here limits nothing about the Substrate.
- Teleportation-state structure (QTI-I/B) and the NIST teleported-CNOT dataset are untouched.

## Open
- O16: channel-aware nulls (iPsiM-vs-ps conditioning, dead-time, rate-preserving shuffles).
- O17: whether iPsiP's offset to ps is structured; O18: per-run (not per-stream) stability; O19: decode data-set/setting metadata (156p45 etc.) from the Zenodo record.
