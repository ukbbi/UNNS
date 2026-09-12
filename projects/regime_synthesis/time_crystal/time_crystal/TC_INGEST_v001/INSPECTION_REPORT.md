# INSPECTION_REPORT

## Ingestion

- Status: **PASS**
- Validated `.dat` files: **84 / 84**
- Decoded binary shape: **5 x 51 x 57** (`float32`)
- Epsilon values: **30** values spanning 0.00 to 1.00
- Devices: {'Brooklyn': 54, 'Manhattan': 30}

## Raw physics sanity check

The raw data already separate a representative epsilon=0.05 run from the epsilon=0.5 thermal run strongly enough to validate the ingestion path. The representative half-frequency-amplitude ratio is **11.73x** and passes the deliberately coarse >5x gate.

Across standard/unflagged files, the median raw half-frequency amplitude is **0.2029** at epsilon=0.05 and **0.0181** at epsilon=0.50. These are raw proxy values, not the fully error-mitigated quantities plotted in the paper.

## Next gate

Reconstruct the paper's methods-faithful error mitigation and qubit filtering, then test whether the critical-fluctuation maximum and depolarization-rate change recover the published transition near epsilon_c ~ 0.075. Only after that gate passes should the temporal closure spectrum C(q) and UNNS temporal ladders be introduced.
