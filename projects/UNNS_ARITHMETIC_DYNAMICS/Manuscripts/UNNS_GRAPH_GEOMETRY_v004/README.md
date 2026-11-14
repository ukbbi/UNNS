# UNNS_GRAPH_GEOMETRY_v004
**Geometry and Metric Structure of the UNNS Arithmetic Graph** -- UNNS Research Collective, Version 1.4, 11 November 2026.

Graph G: vertices = positive integers, edges {kN, k(N+1)^2} (k,N >= 1; N = 1 included; undirected).

## Results (see the PDF for proofs)
- Structure: simple, locally finite, connected; deg(x) = tau(x) + #{q>=2 : q^2 | x}; no vertex of degree 3; edge ratio >= 4; d(m,n) <= 6|m-n|.
- Sharp laws: sup d(n,n+1) = 6 (d(163,164)=6); sup d(n,2n) = 5 (d(1,2)=5); sup d(n^2,(n+1)^2) = 5 (d(23^2,24^2)=5).
- Scaling d(ma,mb) <= d(a,b); product inequality; power lifting d(x^k,y^k) <= k d(x,y); d(1,n) <= 11 log2 n.
- Triangle-free, girth 4, odd girth 5. Primes have neighbours {4p,(p+1)^2}; d(61,67)=7, d(661,673)=8.
- d(F_k,F_{k+1}) <= 12 (certified routes, not shortest); exact for k <= 29 (<= 6).

## Layout
manuscript/ (LaTeX: main.tex + preamble/part1-5, compiled PDF), figures/, tables/ (generated), code/, data/, inherited/, reports/.

## Reproduce
sh code/run_all.sh   (about one minute for the checks; needs python3, sympy, matplotlib); then in manuscript/: pdflatex main.tex (three passes).

## Status
Certified = exact symbolic computation (sympy), not a proof assistant. Lower bounds (ball disjointness) are exact finite computations.
Occurrence of the extremal values infinitely often is not established.

## Source provenance (GitHub reference alignment, Version 1.4)
Earlier releases are cited at commit 22d8c2e23f49fb98a5b04c6b7efe9ba0a3703808 of https://github.com/ukbbi/UNNS (projects/UNNS_ARITHMETIC_DYNAMICS), each by release directory: U1-BND (successor distance), U2-001 (doubling), U2-SQ (squares, scaling, power lifting), U2-TI-DYN (degrees, prime degree), U2-FP (primes, first Fibonacci routes), U2-FP-SYM (twelve certified Fibonacci families), U3 (triangle-free, odd girth 5), U3-COR (girth 4 correction). Archive SHA-256 values in the bibliography are those recorded in the collection's SOURCE_PROVENANCE.md; not recomputed here. The collection's U3 native manifest has one documented historical self-entry mismatch (recorded in the collection). The collection does not contain this manuscript or its verifier.

## Inherited, not re-run (NOT_RERUN)
Archive SHA-256 (see inherited/ARCHIVE_SHA256SUMS.txt): U1-BND 912a068e...; U2-001 561a9558...; U2-SQ c13a9be6...; U2-FP-SYM a614e196...; U3-COR 038c9d11...
Frozen releases and the Autonomous Aperiodicity manuscript are unchanged.

## Changes from Version 1.0 (UNNS_GRAPH_GEOMETRY_v001)
- Theorem 5.4 (power lifting): edge orientation stated (+N for x<y, -N for x>y).
- Fibonacci certificates: all twelve route families listed one move per line (Section 8.4); compact length table retained.
- Section 11 retitled "Mathematical significance and geometric consequences"; open-question list and limitations removed; positive synthesis and a concise proof-scope subsection added.
- No theorem, figure, certificate or inherited release changed; verifier re-run: ALL PASS.

## Changes from Version 1.1 (UNNS_GRAPH_GEOMETRY_v002)
- Abstract and Section 11.2: the three upper-bound constructions distinguished (nine and 24 polynomial identity families; doubling by scaling a single five-edge path).
- Section 11.2: global statements reworded to proved upper bounds ("impose strong global metric constraints"; diameter has a logarithmic upper bound).
- No theorem, figure, certificate or data changed.

## Changes from Version 1.2 (UNNS_GRAPH_GEOMETRY_v003)
- Section 10 status table anchored in place (captioned, labelled) so it no longer floats into Section 11.
- Stale root-level v1.0 PDF removed; the current PDF is manuscript/unns_graph_geometry_v1_3.pdf.
- No mathematical content changed.

## Changes from Version 1.3 (UNNS_GRAPH_GEOMETRY_v003 as delivered, 34 pages)
- Bibliographic only. Commit-pinned references to the collection and to eight release directories (U1-BND, U2-001, U2-SQ, U2-TI-DYN, U2-FP, U2-FP-SYM, U3, U3-COR) with archive SHA-256 values; the combined entries for U2-FP/U2-FP-SYM and U3/U3-COR are split so each citation names one release.
- Citations added in Section 1 (summary theorem, "Relation to earlier releases"), at the Prime-rigidity remark, and as a one-line Source note after the theorems on degree, successor distance, connectivity, scaling, powers, doubling, squares, triangle-free, girth, prime distances and the Fibonacci theorem.
- U3 (triangle-free, odd girth 5) is distinguished from U3-COR (girth 4, withdrawal of the value 5).
- New Section 10.4 "Source provenance". Existing inherited-verification records and hashes unchanged.
- No theorem, proof, equation, figure, table, certificate or data changed. PDF: manuscript/unns_graph_geometry_v1_4.pdf (35 pages).
