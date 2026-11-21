# Experimental raw source manifest

Published source: Lago-Rivera et al., *Supporting data for "Long distance multiplexed quantum teleportation from a telecom photon to a solid-state qubit"*, Zenodo v1, DOI https://doi.org/10.5281/zenodo.7680437.

Three source extracts furnished for the initial analysis:

| Filename | Bytes | Events | SHA-256 |
|---|---:|---:|---|
| `iPsiM_156p45_tot.pt` | 56,992 | 7,124 | `0a39978bbe98bb061b53fb0cf3c2e220834ba41187c5e8fe19441b62023a977c` |
| `iPsiP_156p45_tot.pt` | 55,152 | 6,894 | `9c2a1ced59d2fa9ec6abed972454117f82d169be240fdf0de7ebb08312583053` |
| `iPsiM_156p95_tot.pt` | 37,136 | 4,642 | `674a94551d6a290cc0ff79a7cb38cbee7fe95d2be8077610b2aff5e280a3d10a` |

The raw files are not included in this public-repository-oriented ZIP. Do not assume .pt is a PyTorch tensor. The original hardware time units, clock specification and event selection definitions require independent documentation.

To rerun, supply the three named `.pt` files via `--input` to `scripts/RUN_PROBE.py` (see the study `README.md`). `results.json` contains the source hashes for all three.
