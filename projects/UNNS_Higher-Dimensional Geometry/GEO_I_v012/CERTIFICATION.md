# CERTIFICATION — certificate types and checker

`certificates/checker12.py` (independent of the release code, exact integers/Fractions; run it with `python -I`). Types:
* **ARITH** `{d,s,t,records:[...]}`: re-derives for every `u` the record minimum `M` of `s i mod d`, checks Pareto-minimality, and checks `max(y+x(d-s), (d-t)y+x) >= x y`. 984 certificates (`C11_arith.json`, `5<=d<=60`, every unit pair).
* **CAPCOVER2** `{d,s,u,v,cells:[[w,g,h],...]}`: every cell has four corners in `F_Q`, Graver generators (box scan), independent; exact rational subtraction shows `H_Q \ (H_0 ∪ cells)` has no area. 2,130 certificates (`C12_capcover2.json`, `d<=12`).
* **GRAVER / STRIP / CORNER / COVER**: the structural facts are verified inside CAPCOVER2 (each cell's generators are scanned; the cover is a COVER check) and by `cap_cover.structure_check` (S1–S6). Separate files are not shipped; no claim is made beyond what the checker re-derives.
* **GAP**: none shipped (no uncovered box found). The checker still accepts a GAP record, but only as an *evidence of failure* which would be refuted by a CAPCOVER2 record.
* **PARTITION / CAPCOVER** (v011 formats) are accepted unchanged (231 + 544 certificates, `C9`, `C10`; `checker11.py` retained).
Tamper tests (tests/test_geo12.py, verify.py): removing a cell, perturbing a generator, `s=d-1` in an ARITH record are rejected.
Certificates support instances; the universal statements rest on the proofs in MATHEMATICS.md.
