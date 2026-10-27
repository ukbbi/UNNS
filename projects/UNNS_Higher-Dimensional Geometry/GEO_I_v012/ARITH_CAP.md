# ARITH_CAP — the arithmetic strip inequality (G12-T1)

Statement: for every Pareto-minimal `M = (x,y) in Gamma_{d,s}`, `0<x,y<d`: `max(y + (d-s)x, x + (d-t)y) >= x y`.
Proof: MATHEMATICS.md §1 (three steps: the two failing inequalities force `y > d-s`, `x > d-t`; a lattice point on the line one level below `M` then lies in `[0,x]x[0,y]` unless `y + (d-s)x = d`; the symmetric statement gives `x + (d-t)y = d`; combining, `m x = (d-t) - 1 < x`, contradiction).
Role: guarantees that the bottom cell `P(B-g; g, M)` contains the bottom triangle `conv{B, B+M, (d,y_M)}` for `g in {(1,s-d), (d-t,-1)}`.
Computational support: all 6,022 Pareto-minimal points for `5<=d<=60` (tests/test_geo12.py), 984 ARITH certificates (`certificates/C11_arith.json`; checker12 re-derives record minimum, Pareto-minimality and the inequality for every `u` and every unit pair).
Status: PROVED+CHECKED. v011's 657,526-triple check of the same inequality is superseded by the proof.
