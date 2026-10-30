# Verification report — Paper A manuscript v1.1

Evidence tiers (Section 21.1): T1 source-reported proofs (GEO-I releases); T2 internal written audit with corrections D1–D9; T3 independent numerical tests; T4 external review — NONE; T5 formal proof — NONE.

Finite checks (scripts/verify_all.py full; exact where stated; geometry via shapely, floating point, tolerance 1e-9 — numerical tests, not exact certificates):
- cap cover by explicit family, 5<=d<=12 nonspecial: 2130 boxes, 0 failures
- Pareto inequality (exact integers), nonspecial 5<=d<=120: 33,633 points, 0 failures
- boundary steps Graver, 3<=d<=12: 2343 steps, 0 failures
- U_Q = H_Q (2-dim defect only), 2<=d<=8: 1327 boxes, 0 failures
- realizability (exact), 2<=d<=14: 29,127 lattice points, 0 mismatches
- worked example (exact rationals): PASS, 72,301 grid points covered
- D9: C0 strictly interior in 241 of 366 boxes (d=5..8)

Build: pdflatex x3, 0 errors, 0 LaTeX/package warnings, 0 overfull boxes, 47 underfull-box notices (typographic diagnostics), 71 pages.

Disclosures: GitHub fetch was robots-blocked (local release folders used); references: abstracts/catalogue pages only (Hatcher, Bjorner–Tancer data from an encyclopedia reference list; Serre from memory); Alexander-duality theorem number unconfirmed (cites Hatcher §3.3); Proposition 3.4 (Dirichlet realizability) is new in this manuscript and independent of all other results; D7 count reconciliation is our reading of the release files, not re-run.

v1.1 additions: the independent review of v1.0 reproduced smoke mode, example.py and realize.py; it did not complete full mode (logs bundled, not independently re-run). Geometric checks are numerical (shapely, floating point), not exact certificates. GEO-I releases cited at pinned commit 343f9aef2b6697466058165c5fc2ddf0f00e882b (existence of the twelve directories confirmed by the author and the reviewer; not fetched by the drafting process).

## v1.2 terminology revision
Added Section 1.2 (terminology), Definition 2.5 (arithmetic occurrence fibre; arithmetic occurrence geometry) with a reading remark, and a scope note in the literature section (Section "Literature and context"). No theorem statement, proof, computation or frozen GEO-I release was changed. Only labelled numbering effect: Remark "The deleted origin" is now 2.7 (was 2.5). Version line removed from the title page; date kept (28 October 2026). Package: 72 pages.
