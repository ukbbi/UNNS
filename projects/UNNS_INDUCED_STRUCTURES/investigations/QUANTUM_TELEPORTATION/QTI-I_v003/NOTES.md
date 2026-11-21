# QTI-I v003 - Channel-conditioned analysis of iPsiM, iPsiP and ps

Scope: research notes, not a manuscript. Substrate fixed. All numbers: 12 data sets (6 per zip), all channels. Channel meanings are not documented in the Zenodo record; statements below are about the timestamp data only.

## Objective 1 - does the iPsiM-ps association survive channel-aware nulls? YES, by a very large margin.
- Fraction of iPsiM events with a ps event at the data set's modal delay (tolerance 2e6 units): 0.9962-0.9993 in all 12.
- Nulls: 200 global time shifts (1e10-2e12): max matched fraction 0.00035; 25 local-rotation nulls (target events rotated within 5e13 windows, preserving local rate and gap pattern): max 0.00014; local-rate Poisson expectation: z >= 28,000. (p resolution 1/201.)
- Delay is a data-set constant (about 8.41e6 units in `1 km`, 1.08e7 in `Short distance`), with 3-4 sub-clusters whose spacing is ~6.4e4-8.0e4 units. ps lies on a 20000-unit grid with 1-4 phases per data set (S5).
- So the association is not a rate or acquisition artefact. It is also not a surprise: it behaves like a derived/linked stream (ps = iPsiM + delay).

## Objective 2 - why is iPsiP different? Not the time base, not rates; the event definitions differ.
- Time base (S1): every iPsiM and iPsiP timestamp is exactly equal to an i1 or i2 timestamp (offset 0), in all 12 data sets. iPsiM, iPsiP, i1, i2 share one time coordinate; a different origin cannot explain the asymmetry. ps is linked to iPsiM at a fixed delay on the same coordinate.
- iPsiM events (S2) are pairs: one i1 and one i2 event within 6e5 units (100% in all data sets; chance 0.6-1.5%); the iPsiM timestamp equals one of the two.
- iPsiP events (S3) are same-detector pairs: 100% have a second event in the same detector within 6e5 units (chance 0.6-1.2%), only ~0.4-1% have a partner in the other detector; the timestamp equals one of the pair. About 28-42% sit in i1 and 58-72% in i2.
- iPsiM and iPsiP are nearly disjoint (S4: <=0.7% shared exact timestamps).
- iPsiP is not ps-linked at any lag (N2): matched fraction <=0.7%; the only peak within +-1e12 sits at the iPsiM delay with 4-18 events, i.e. the iPsiM/iPsiP overlap.
- Rates and windows: event rates of iPsiM and iPsiP are similar (within ~20%) and in 11 of 12 data sets their spans match to within ~1e12-4e12 units; in `1 km` dataL the iPsiM stream stops about 5.7e15 units before ps and iPsiP, which is the one clear acquisition-window difference (and the data set with the weakest ps~iPsiM correlation, 0.74). Rate-profile correlation (2e12 bins), lag 0: ps~iPsiM 0.74-0.97, ps~iPsiP 0.00-0.60, iPsiM~iPsiP 0.02-0.60, i1+i2 ~ iPsiM 0.13-0.76, i1+i2 ~ iPsiP 0.16-0.78. Both share the idler-rate trend about equally; only iPsiM tracks ps tightly, as expected from the event identity.
- Conclusion: the asymmetry is in channel membership/definition (cross-detector pairs get a ps tag; same-detector pairs do not), not in encoding, offsets, rates or windows. No physical interpretation is attempted.
- ps trials without an iPsiM partner (11-36%, S6): in 11/12 data sets >=97% of them have both i1 and i2 events in the delay window (chance ~1e-3); in `1 km` dataL only 36%. What these are is open.

## Objective 3/4 - joint UNNS geometry and controls: nothing beyond clock-grid and coincidence structure.
- Delay lifts (J1): the counter delay of each synchronized pair (about 26,600-27,200 in `1 km`, 34,300-34,900 in `Short distance`) has history count F and R like generic integers: 36 delay values, rank of F among 1500 integers in [c/2, 2c] is <0.97 (square grammar) and <0.98 (cubic grammar) for all; 1 and 6 values reach 0.95 respectively, as expected by chance. Alternative grammar: cubic (incoming edges m>=2 with m^3 | d).
- Joint gaps (J2/J3): in the synchronized iPsiM-ps sequence, counter gaps of the two channels are equal to within ~150-225 ticks (exactly equal <0.3%), ratio ~1, so no T_N relation (ratio >= 4) joins channels. ps gaps are squareful in 99.93-100% of cases (clock grid), so P(R_ps>0 | R_M>0) is uninformative (index-lag and jitter controls: phi ≈ 0). The cubic grammar is saturated/zero in the same way.
- Net: the cross-channel UNNS structure reduces to the clock-lift theorem (ps) and generic integer behaviour (iPsiM, delays). No candidate induced structure survives matched controls.

## Limits
- Channel semantics are inferred from timestamps only; the Zenodo record documents none of it. Pair window 6e5 units is empirical.
- Null models do not include detector dead-time or per-trial structure (no trial index is available); the "trial-conditioned" control requested was replaced by window rotation (local rate and gap pattern preserved) because trials cannot be identified from the files.
- Joint geometry tests use 3000 sampled synchronized gap pairs per data set; delay-lift histories are tested for 36 values.
- `Repetition rate.zip` missing; the teleported-CNOT dataset and QTI-I/B (teleportation-state structure) untouched.

## Open
- O20: nature of the 11-36% of ps trials without an iPsiM partner and their i1/i2 events. O21: why ps phase on the 20000 grid is not constant in 6 data sets. O22: whether iPsiM/iPsiP pair separations (<=5.5e5 units) carry structure under the UNNS lift (QTI-I/B needs a defined phi). O23: independent documentation of channel semantics (authors' paper/data card).
