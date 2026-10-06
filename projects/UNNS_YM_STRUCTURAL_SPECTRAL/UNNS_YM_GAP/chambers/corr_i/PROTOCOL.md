# CORR-I v0.1.2 Protocol

## Single-channel mode

Unchanged from v0.1.1.

1. Load one CSV.
2. Select a channel if more than one is present.
3. Run CORR-I.
4. Export JSON and envelope CSV if desired.

## Batch mode

1. Load either:
   - one wide CSV containing multiple correlator columns, or
   - multiple CSV files selected together.
2. Set the visible chamber parameters once.
3. Click `RUN BATCH + ZIP`.
4. CORR-I analyzes all loaded channels with identical settings.
5. One ZIP download is created containing one JSON and one envelope CSV per channel plus aggregate records.

Batch mode does not alter the mathematics of the baseline or adversary layers. It only automates repeated execution and export.

## Batch invariants

- Same PSD tolerance for every channel.
- Same plateau tolerance and minimum plateau points for every channel.
- Same alpha cap, mu range, mu point count, z limits, and relative limits for every channel.
- Each channel retains its own error-model status based on whether sigma data were supplied.
- A failed/unavailable envelope for one channel does not redefine the other channels.

## Interpretation

Batch processing is operational convenience, not a new inference layer. CORR-I remains a correlator-compatibility chamber and does not by itself prove a Yang-Mills mass gap.
