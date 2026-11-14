# UNNS_GRAPH_ENT_v006 — Intrinsic Symbolic Dynamics and Entropy of Arithmetic Graphs (Version 1.5)

Author line: UNNS Research Collective.

Main results: exact nonbacktracking entropy of the arithmetic subgraphs F_m, h = log(lambda_m) with lambda^3 - lambda^2 + lambda = m
(proved for all m, bounds (1/3)log m < h < (1/3)log m + 1/(3 m^{1/3})); the induced-subgraph theorem G[V(F_m)] = F_m; the full spectrum and Ihara-type determinant;
periodic-path counts; maximal-entropy chain; infinite finite-subsystem capacity H_fin(G) = infinity; reconciliation with the frozen U4-M2-ENT rows.

Layout: manuscript/ (LaTeX), figures/, tables/, code/ (graphent.py, verify_graph_ent.py, make_figures.py, make_tables.py, run_all.sh), data/, reports/verification_report.json (37 checks, all PASS),
inherited/ (read-only inherited archives with SHA-256; their verifiers are NOT re-run).
PDF: unns_graph_entropy_v1_5.pdf. Reproduce: `cd code && ./run_all.sh` (about 1 minute, plus LaTeX).
Version 1.3: corrects the shortest-cycles statement in the synthesis (adds the four-cycle 6-27-144-32 without N=1 to Theorem 4.1), removes the remaining FRACTRAN sentence and its reference, and anchors the floats within Sections 8-11.

Version 1.4 (GitHub reference alignment; bibliographic and provenance only):
- Commit-pinned bibliography (collection commit 22d8c2e23f49fb98a5b04c6b7efe9ba0a3703808): new entries for the collection, U1-BND, U2-TI-DYN and U4-STAGE2; commit-pinned release directories added to the existing U3, U3-COR and U4-M2-ENT entries (U4-M2-ENT also its docs/PROOFS_ENT.md). Existing archive names and SHA-256 fingerprints, and the PRIME_DYN v002 entry (not in the collection), are unchanged.
- Citations added in the introduction, at the degree proposition, the cycle theorem (girth 4 attributed to U3-COR; triangle-freeness and odd girth 5 to U3), the Y_NB definition (U4-STAGE2), the capacity convention and theorem (U4-M2-ENT E1/E2), the entropy theorem, and the zero-entropy proposition (U4-M2-ENT E5).
- Provenance paragraph corrected: Y_NB is attributed to U4-STAGE2; F(x), the 1/4 log bound and sup = infinity to U4-M2-ENT. The exact formula log(lambda_m), spectrum, Ihara-type determinant, periodic counts, maximal-entropy chain, spectral gap and induced-subgraph theorem are stated as results of this paper.
- New Appendix "Source provenance" with a table of theorem families (inherited / this paper); inherited/COLLECTION_SOURCES.txt lists the pinned paths and recorded hashes.
- No theorem, proof, formula, figure, table or computation changed. Verifier re-run: 37 checks ALL PASS (inherited verifiers NOT_RERUN). PDF: 23 pages.

Version 1.5 (two documentary corrections to Version 1.4; no mathematical change):
- Bibliography [PRIME_DYN] now references the current companion manuscript, Version 1.2 (UNNS_PRIME_DYN_v003.zip, SHA-256 23ddd619ac87990b7dbf18a7791830f7cf2c7066d65b9254b2a2123d3bf59ee8), and retains Version 1.1 (UNNS_PRIME_DYN_v002.zip, 99fc793a...) as the historical archive held in inherited/, which is unchanged. The provenance paragraph in the introduction is aligned.
- Appendix B: the check of the inherited archive hashes is stage G10 (G8 checks the inherited numerical rows).
