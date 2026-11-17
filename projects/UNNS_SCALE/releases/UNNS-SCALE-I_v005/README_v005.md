# UNNS-SCALE-I v005 — Trillion-Window Metric Closure and Infinite-Scale Investigation

**Part A (closed theorem):** for B = 10⁶, max over 1 ≤ n ≤ 999999 of d_G(10⁶n, 10⁶(n+1)) = **4** — every consecutive million-spaced pair inside the trillion window is joined by ≤ 4 SELECT-II edges in the full infinite graph, and distance 4 occurs (n = 11, 13). Accounting: 999,384 identity members + n = 1 (3 steps) + 614 explicit exact 4-step paths. Ambient statement: path vertices reach 3.3·10²², beyond the trillion window.

**Part B (exploratory, open):** D_{10⁶} ∈ {4,5,6} is undecided. The 614 exceptional paths show no single repeating pattern; 55 further length-4 identities cut the uncovered window set to 407 but the refinement does not close; 299 exact distances outside the window (families where B = 10 has distance 6) are all 4.

Layout: THEORY/, SPEC_v005.md, code/, results/ (+ results/raw), reports/VERIFICATION_REPORT_v005.md, SHA256SUMS_v005.txt.
Run: `cd code && python verify_all_v005.py --quick` (or `RUN_VERIFY_v005.bat`). Needs Python 3, numpy, sympy; sits next to UNNS-SCALE-I_v002–v004 inside UNNS_SCALE (read-only).
