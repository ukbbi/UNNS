# Paper A manuscript v1.0 — verification review
28 October 2026

## Overall verdict
**SUBSTANTIALLY COMPLETE DRAFT — TARGETED REVISION ADVISED BEFORE EXTERNAL CIRCULATION.** This is a technical/documentary verification, NOT peer review or proof-assistant certification. No counterexample to the central theorem was found in the examined proofs and executable smoke tests. The universal result is not independently proved by this report.

## Package and build
- Input: `PAPER_A_manuscript_v1.zip` (as uploaded).
- Manuscript PDF: 68 pages, A4, searchable.
- LaTeX source rebuilt successfully with three `pdflatex` passes; 68 pages.
- 57/57 entries in `MANIFEST.sha256` pass. `MANIFEST.sha256` itself is not included in its own manifest (normal); working Python caches should not be shipped.
- Final LaTeX pass: no errors, no LaTeX/package warnings, no overfull boxes; 30 **underfull hbox** notices. The original verification report's blanket phrase '0 warnings' is best replaced by the precise counts.
- PDF title metadata contains a literal `[2pt]` formatting command between title/subtitle. The visible title page looks correct; set `pdftitle` explicitly in `hyperref` to fix the metadata.
- PDF uses embedded fonts and contains visible mathematical figures. A 10-page visual sampling revealed no obvious clipping, but this was not a complete manual examination of all 68 pages.

## Reproduced executable checks
`python verify_all.py smoke` completed with:
- cap cover: 366 boxes, 0 failures;
- Pareto points: 2,114, 0 failures;
- boundary steps: 997, 0 failures;
- universal boxes: 451, 0 failures.

`python example.py` passed, reproducing 7 and 8 occurrence pairs and 72,301 exact-rational test-grid points with no uncovered points. `python realize.py` passed (29,127 points compared; 0 mismatches).

A separate attempt at `python verify_all.py full` exceeded the 200-second execution limit. The supplied full logs report 2,130 cap boxes, 33,633 Pareto points, 2,343 boundary steps and 1,327 universal boxes without failures; these are **not independently re-run in this review**. The geometrical coverage methods depend on Shapely and floating-point tolerances, not exact polygon arithmetic; the integer-valued checks and the worked-example rational grid are exact where specified.

## Mathematical review scope
Read and inspected the central manuscript sources concerning occurrence coordinates, normalization/realizability, special exceptional geometry, special classes, column-strip coverage, G12-T1, the repaired G12-T2 reflection argument, outer chain and cap cover, and universal case assembly. Compared the central release scopes with GitHub read-only files v005/v007/v010/v011/v012. These reviewed arguments have coherent stated hypotheses and I identified no demonstrable counterexample. This is a *targeted plausibility/proof audit*, not a line-by-line independent proof of all 68 pages and not formal certification.

Points confirmed:
- G5-C1 excludes `Q=(d,d)` correctly.
- G7-T1 has the range `Q_i>=d` and `max(Q)>=2d` as used in the paper.
- The explicit `s=+1` complement is clearly marked as an extension beyond what v005 originally stated.
- The origin/reflection issue of G12-T2 is explicitly addressed via axis-pair nonconsecutiveness, for `Q_i>=d` with no upper bound.
- D9 counterexample is included and the false assertion that `C0` must lie on the outer chain is not used.
- Central universal theorem has the proper exceptional-box exclusion.

## Corrections and outstanding items
**A — Prior to circulation**
1. Strengthen the literature review: the manuscript openly states it is not a systematic prior-art comparison and consulted mainly catalogue/abstract pages. Do not characterize journal-level originality as externally established.
2. Correct the Björner–Tancer characterization: that article proves *combinatorial Alexander duality of simplicial complexes*, not directly the precise planar complement theorem quoted from Hatcher. It can be presented as related background, but not as a substitute proof of the theorem used here.
3. Identify Hatcher's Alexander duality precisely as *Algebraic Topology*, Theorem 3.44, §3.3 (confirmed against an online text).
4. Distinguish the D7 smoke/full counts as the manuscript authors' interpretation of archived release records; the 25/27 and 125/132 reconciliation was not independently rerun here.
5. Keep a clear statement that the full executable suite was not completed in this review, though full logs are bundled.

**B — Editorial/package polish**
6. Fix PDF metadata stray `[2pt]` via explicit `pdftitle` and `pdfauthor`.
7. Rephrase build report as 'no overfull boxes, 30 underfull hbox notices on this environment', instead of implying no typography diagnostics.
8. Consider reducing some underfull spacing and checking all vector figure labels before release.
9. Add exact version/lock instructions for Python (notably Shapely and Matplotlib), and avoid certifying numerical area checks as exact geometric certificates.
10. Keep mathematical sources and GEO-I frozen; prepare fixes in new manuscript v1.1 only.

## Publication decision
The uploaded package is genuinely a substantial first full manuscript rather than another preflight. It is ready for a focused v1.1 editorial and literature pass, followed by external mathematical assessment. No mandatory Lean formalization or new GEO-I engine is necessary to keep manuscript writing and review moving.
