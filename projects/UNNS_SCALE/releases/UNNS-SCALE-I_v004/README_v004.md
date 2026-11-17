# UNNS-SCALE-I v004 — Exceptional-Class Closure and Metric Certification

Result in one paragraph: **D_10 = 6 is certified** (n = 365759 and n = 351359 have exact d(10n, 10(n+1)) = 6 in the infinite graph), so the seven exceptional classes of B=10 are genuine obstructions; D_B = 6 also for B = 1, 2, 5. A new universal 2-adic theorem (G) gives d_B(n) ≤ 4 for v2(n+1)=1 and ≤ 5 for v2(n+1)=3, for every B. The B=10 proved-≤5 coverage rises from 359/360 to 1 − 6.5·10⁻⁴; B=12 to 1 − 2.8·10⁻⁵ (5 ≤ D_12 ≤ 6); at B=10⁶ every exact distance computed is ≤ 4 (4 ≤ D_{10⁶} ≤ 6, open).

Layout: THEORY/ (full write-up), SPEC_v004.md, code/, results/ (+ results/raw), reports/VERIFICATION_REPORT_v004.md, SHA256SUMS_v004.txt.
Run: `cd code && python verify_all_v004.py --quick` (or `RUN_VERIFY_v004.bat`). Expected layout: this folder sits next to UNNS-SCALE-I_v002 and UNNS-SCALE-I_v003 inside the UNNS_SCALE folder; those folders are only read.
Requires Python 3, numpy, sympy.
