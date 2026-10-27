# GEO-I v012 — Report: Universal Planar Cap Closure

**Result.** For every `d>=2`, every unit `s`, every `Q1,Q2>=d`, `Q != (d,d)`: `U_{d,s,Q} = conv(F_{d,s,Q})` (G12-T8, PROVED+CHECKED). The result is **conditional** only on three inherited PROVED+CHECKED results (G5-C1 for `s=±1`, G7-T1 for `max Q>=2d`, G10-R1 for `H_0 ⊆ U_Q`); no other hypothesis is used and no finite range of `d` is a required case.

**Proof structure** (full text in MATHEMATICS.md).
1. *G12-T1* (the "G11-A" gate): for any Pareto-minimal `M=(x,y)` of `Gamma`, `max(y+(d-s)x,(d-t)y+x) >= xy`. If both fail then `y>d-s`, `x>d-t`; a lattice point one level below `M` then lies in `[0,x]x[0,y]` unless `y+(d-s)x=d`; symmetry gives `x+(d-t)y=d`; then `x<=d-t-1`, contradiction.
2. *G12-T2* (uniform Graver steps): consecutive boundary Gamma-points of `H_Q` differ by a Graver vector (reflection through the edge midpoint).
3. Boundary Omega of `H_Q` from `(d,0)` to `(0,d)`: `H_Q ∩ [0,d]^2 = H_0`; Omega ∈ `R*C*T*`; no R→T step (reflect `(d,d)`); first step `B+M` with `M` the record minimum (descent argument).
4. One cell family — L-cells (shift `(-d,0)`), D-cells (shift `(0,-d)`), bottom cell and its transpose — covers `H_Q \ H_0` for one-sided and mixed boxes alike (T3–T7); closedness of `U_Q` turns a.e. coverage into equality. The v011 "corner pentagon" is not a separate region.
5. Assembly (T8): `s=±1`; `max Q>=2d`; small boxes.

**Machine support (CHECKED, instance level).** 6,022 Pareto-minimal points (`d<=60`) satisfy T1; 984 ARITH and 2,130 CAPCOVER2 certificates accepted by the independent `checker12.py` (and tamper-rejected when corrupted); exact cover of all 29,206 small boxes with `d<=22`, structure lemmas on 7,464 boxes `d<=16`, 19,731 adversarial boxes up to `d=399`, 3,000 random boxes: 0 failures; no GAP certificate. v011's 657,526-triple check of G11-A is superseded by the proof.

**Interrupted job.** A standalone exact sweep `d=13..30` was stopped before completion to prioritise proof certification; it is recorded `PARTIAL` (no PASS claimed, no completed range) in `output/data/v12_sweep_13_30_PARTIAL.json`. Nothing in the proof, registry or verifier depends on it; the completed run above covers `d<=22` exactly.

**Verification.** `verify.py` (smoke ~10 min; full ~15 min). **Protocol change, disclosed:** the 2-hour inherited v011/v010 full gate is *not re-executed* by default (status `NOT_RERUN - FROZEN BASELINE VERIFIED`, not PASS): v001-v011 are frozen and sha-256-verified unchanged, their full reports from the v011 release (v011 33/33, v010 132/132) are preserved in `output/baseline_v011/`, and a targeted compatibility regression (the inherited verifier in smoke mode, 33/33 + 125/125) runs every time; `python verify.py --rerun-inherited-full` re-executes the full gate. A partial attempt at it was stopped by the operator and is not counted. `verify.py` (original description: re-derives T1, S1–S6 and the cell cover on fresh instances, runs the certificate checker isolated, tamper tests, documentation/honesty checks, and gates on `verify_v011.py` (which gates `verify_v010.py`): v001–v011 are hash-verified unchanged and regression-checked (smoke gate), W2 and universal rank 3 preserved.

**Not claimed.** Closure of the broader global geometric organisation of the occurrence geometry (G12-O1 OPEN). The proofs are written for human review; independent review of MATHEMATICS.md §1–§5 is the recommended next step. No priority claim.
