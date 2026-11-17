# UNNS-SCALE-I v003 — Scaled-Successor Metric Geometry

Local-only research release. v001 and v002 are frozen and untouched. GitHub: read-only reference, nothing published. Gate 4 deferred.

Question: does exact arithmetic self-similarity (BN ≅ G) coexist with scale-dependent shortening of the *ambient* distance d(Bn, B(n+1))?

Headline results (see `THEORY/UNNS_SCALE_I_THEORY_v003.md` for statuses and proofs):
1. PROVED laws: pointwise monotonicity d_B(n) ≤ d_A(n) for A | B; hence D_B ≤ D_A, lower bounds propagate to divisors, mean route length is monotone; every shortening uses routes outside BN.
2. CERTIFIED: D_B = 6 for B | 7 and 20 other scales ≤ 96 (list in THEORY §4). D_12 ≥ 5 (n=25199), although every n ≤ 6000 gives ≤ 4; B=24, 48 likewise reach 5 on smooth n+1.
3. PROVED class covers: d_B(n) ≤ 5 on ≥ 98% (B=3) to 99.88% (B=6) of n for B = 2,3,4,5,6,10; d_12(n) ≤ 4 on all n except 1/6300 (2 classes), with exact exceptional classes listed. The exceptional classes are where n+1 is highly smooth.
4. EXPERIMENTAL: typical route length decreases with divisibility by 2 and 3 (mean 4.28 → 3.70, plateau), δ_B(n) = d_1(n) − d_B(n) ∈ {0,1,2}, P(δ>0) ≈ 0.47 for 6 | B.
5. OPEN: whether any B ≥ 2 has D_B ≤ 5.

Files: `THEORY/`, `SPEC_v003.md`, `code/` (run `python code/verify_all_v003.py`, or `code\RUN_VERIFY_v003.bat`), `results/` (JSON), `reports/VERIFICATION_REPORT_v003.md`, `SHA256SUMS_v003.txt`.
