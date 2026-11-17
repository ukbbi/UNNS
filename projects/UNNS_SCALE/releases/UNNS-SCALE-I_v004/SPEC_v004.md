# UNNS-SCALE-I v004 — Specification

Release: exceptional-class closure and metric certification (local only; v001–v003 frozen; no GitHub changes; Gate 4 deferred).

Objects: SELECT-II graph on N>0, edges {kN, k(N+1)²}; d_B(n)=d(Bn,B(n+1)); D_B=sup_n d_B(n) (D_B ≤ 6 from v003).
Deliverables / acceptance (as approved):
* D_B = 5: universal bound ≤ 5 plus one exact distance-5 witness. D_B = 6: one exact distance-6 witness. 5 ≤ D_B ≤ 6: certified lower bound 5, no universal conclusion.
* Universal symbolic statements cover arbitrary exponents and residual factors (class identities in t, valid for all t ≥ t0; members below t0 checked exactly).
* All distance certificates refer to the full infinite graph; lower bounds by disjoint balls (indep_check, sympy).
* Results are labelled PROVED / CERTIFIED / EXPERIMENTAL / OPEN.

Task map: D4-A (B=10) → THEORY §2; D4-B (B=10⁶, prioritised) → §3; D4-C (B=12) → §4; D4-D synthesis → §5–§7.
Result files: results/D4A_*, D4B_*, D4C_*, D4_open_class_members_exact.json, results/raw/ (raw cover outputs).
Verifier: code/verify_all_v004.py [--quick]; baseline hashes read from ../SHA256SUMS.txt, ../UNNS-SCALE-I_v002/SHA256SUMS_v002.txt, ../UNNS-SCALE-I_v003/SHA256SUMS_v003.txt.
