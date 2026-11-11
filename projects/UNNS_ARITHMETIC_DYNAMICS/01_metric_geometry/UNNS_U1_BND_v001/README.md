# UNNS-U1-BND v001 — Bounded Successor Distance

Authors: UNNS Research Collective · Date: 8 November 2026 · Version 1.0 (v001)

## Result

Let G be the graph on the positive integers with edges `kN — k(N+1)^2` (k, N ≥ 1), the undirected closure of the
SELECT-II transformation `m -> m(N+1)^2/N` (N | m). Then for every n ≥ 1

    2 <= d(n, n+1) <= 6,        and        d(163, 164) = 6,

so `sup_n d(n, n+1) = 6`. Consequently the total distance along 1, 2, ..., k+1 is at most 6k.

* **Upper bound (proved):** nine explicit path identities, one per residue class of n (mod 4, 8 or 24). Each step
  is certified by an integral positive cofactor, so legality holds for the whole class at once. Full step
  certificates are in Appendix A of the manuscript and in `data/identities.json`.
* **Sharpness (exhaustive computation):** meeting-in-the-middle at n = 163, reproduced by two independent programs.
* **Not claimed:** that the value 6 occurs for infinitely many n; proof-assistant certification; a prior-art review;
  anything about a state-computable selector.

## Layout

| path | content |
|---|---|
| `manuscript/UNNS_U1_BND_v001.pdf` / `.tex` | the note (PDF and LaTeX source) |
| `manuscript/figures/` | figures (PDF and PNG), generated from computed data |
| `code/u1_bnd_lib.py` | exact engines (two independent neighbour enumerators) and the nine identities |
| `code/verify_u1_bnd.py` | deterministic exact-arithmetic verifier (checks V1–V9) |
| `code/build_tables.py`, `build_numbers.py`, `make_figures.py` | generate manuscript tables, macros and figures from the certificates/report |
| `code/search/` | the path-identity search tool used to discover the identities (optional; not needed to verify) |
| `data/successor_distance_table.csv` | exact d(n, n+1) for the computed range |
| `data/identities.json` | machine-readable step certificates |
| `reports/u1_bnd_verification_report.json` | verification report (no timestamps; reproducible) |
| `SHA256SUMS.txt` | integrity hashes of every file in the package |

## Reproduce

Requires Python 3 and `sympy` (`pip install sympy`). From inside `code/`:

    python3 verify_u1_bnd.py --out ../reports/u1_bnd_verification_report.json --csv ../data/successor_distance_table.csv
    python3 build_tables.py ../manuscript ../data
    python3 build_numbers.py ../reports/u1_bnd_verification_report.json ../manuscript
    python3 make_figures.py ../manuscript/figures ../data/successor_distance_table.csv

The full verifier run takes several minutes (most of it is the exact distance table). Use `--table-max` and
`--replay-max` for a quick run. Then compile the manuscript in `manuscript/` with `pdflatex` (twice).

## Status

The symbolic check V2 is an exact computer-algebra statement; the remaining checks are finite computations supporting the
proofs in the manuscript. U0-001, the U1 connectivity note and the frozen reference collection are left unchanged.
