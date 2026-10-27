# GEO-I v011 — certification

Standalone checker: `python3 -I certificates/checker11.py FILE.json …` (standard library only, no import from the release). Earlier formats (BOUNDARY, COVER, GAP, HOMOLOGY, RANK, RANK6) are still checked by the unchanged `checker.py`, `checker8.py`, `checker10.py` inside `verify_v010.py`.

## New formats
**PARTITION** `{type,k,points,two_blocks,n_two_blocks}` — a W2 witness. Accepts iff `points` are distinct points of `AG(k−1,2)` (k-bit ints, top bit set) of rank `k`; at least two distinct unordered pairs `{f,g}` have `supp(w_f), supp(w_g)` disjoint, covering `X`, and each a **circuit** (`X ∩ f^⊥` has rank `k−1`); and `n_two_blocks` equals an independent recount over all `2^k` functionals. By G10-E1 and G10-L5 this certifies a non-embedded box with a rank-3 collision. File `C9_partition.json`: **231** certificates (every minimal class of nullity 3, 4, 5, 6), all accepted. *Not certified by this format:* minimality (the 215 nullity-6 classes carry v010 RANK6 certificates) and the general theorem G11-T3 (a proof, `MATHEMATICS.md` §1).
**CAPCOVER** `{type,d,s,u,cells}` — one-sided small box `Q = (d+u, d)`. Accepts iff every cell has all four corners in `F_Q`, Graver independent generators (box scan), the cap `K = B + W_u` is inside the union of the cells (exact `Fraction` polygon subtraction) and `area(conv F_Q) = area(conv F_{(d,d)}) + area(K)`. File `C10_capcover.json`: **544** certificates (`5 ≤ d ≤ 16`), all accepted. Certifies, per box, that the cap of the one-sided box lies in `U_Q`; it does not prove the universal cap theorem.

## Tamper tests (in `tests/test_geo11.py` and `verify.py`)
PARTITION: a single pair, a corrupted functional, a wrong count → rejected. CAPCOVER: a removed cell, a perturbed generator → rejected.

## Release verification
`verify.py --smoke` (several minutes) and `verify.py` (full, ≈ 2 h): new v011 checks + the inherited v010 verifier (`verify_v010.py`, document paths only changed) as a gate. Both write real JSON reports in `output/reports/` (`verify_{smoke,full}.json` for v011 and `verify_inherited_{smoke,full}.json` for the inherited gate). `MANIFEST.sha256` lists every shipped file except the manifest and the verifier run reports.
