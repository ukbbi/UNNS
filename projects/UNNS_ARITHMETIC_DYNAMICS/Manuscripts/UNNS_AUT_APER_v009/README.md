# UNNS_AUT_APER_v009 — Autonomous Aperiodicity in the UNNS Substrate (manuscript Version 2.7)

Author line: UNNS Research Collective. Supersedes UNNS_AUT_APER_v008 (Version 2.6) and earlier packages; all left unmodified.

## Contents
- manuscript/unns_autonomous_aperiodicity_v2_7.tex / .pdf (20 pages)
- figures/: fig_exchange (Fig 3), fig_registers (Fig 4), fig_anatomy2 (Fig 5), fig_returnmap2 (Fig 1), fig_itinerary (Fig 2) — numbers as in the PDF
- tables/: worked00_rows.tex (Appendix C rows)
- code/: run_all.sh and the scripts behind every check and figure
- data/: balance_identity_196.csv, programs_196.csv (all 196 certified programs), predicted_returns.json
- inherited/: copies of audit files used (hashes in INHERITED_SHA256SUMS.txt). The certificate itself was NOT re-run (NOT_RERUN); reproducer is in UNNS_GUP_ADJ4_AUDIT_v001.
- REVIEW_BRIEF.md: brief and questions for an outside reviewer

## Changes from v001
Remark 2.4 replaced as requested (+ explanatory Remark 2.5); new Section 6 (mechanism: three regimes, exchange cycle 5->7->2->5, gain 2869/49, balance identity, congruence delta = -27 r mod 49); Proposition 5.2 (R(1,z)=R(0,z+8)); worked certificate and polyhedral lemma; new figures; extended literature context incl. honest note that unbounded runs are elementary in FRACTRAN.

## Changes from v003
The "Priority" paragraph of Section 9 is replaced by a plain list of the sources examined; no originality gate is stated.

## Changes from v004 (Version 2.2 -> 2.3)
Section 9 rewritten and renamed "Relationship to established mathematics". It now (1) states the FRACTRAN correspondence for the fixed-priority selector in one proposition with its scope (not a statement about the UNNS Substrate as a whole), (2) lists the standard tools shared with existing theory, (3) states what the paper establishes (three-regime mechanism, derived factor 2869/49, selected-return law with certified corrections, scoped consequences). Removed: the "elementary" discussion, the "no standard counterpart" row, the "system never halts" sentence and the decider/cryptid paragraph; abstract, introduction and bibliography adjusted accordingly. No mathematics changed.

## Changes from v005 (Version 2.3 -> 2.4)
Section 9.1 scope now states both domains (Theorem 5.1 on the whole section Sigma; Theorem 5.5 on the designated orbit). Table 2: "first qualifying return to Sigma, subject to z'>=10z"; certificate described as exact emptiness of rational polyhedra excluding integer violations. Figure 2 panel (b) heading: "block shares approach fixed proportions". Section 10 retitled "Mathematical significance and consequences": the "What it does not show" paragraph is removed and replaced by a positive synthesis, one statement of what is established and how, and a short "Further mathematical directions" paragraph; the intro scope paragraph, abstract and Section 6.5 heading tightened. No mathematics changed.

## Changes from v006 (Version 2.4 -> 2.5)
Data-availability paragraph now names package UNNS_AUT_APER_v007; the remark on the word "independent" (Section 8) is simplified to describe the independent implementation within the collective, without reference to external review. No mathematics changed.

## Changes from v007 (Version 2.5 -> 2.6)
Abstract ends with the certified result (FRACTRAN sentence removed); introduction item 6 and the scope paragraph no longer point to FRACTRAN; Section 9 retitled "Mathematical correspondences and methods" with two compact parts (9.1 Proposition 9.1 with proof and scope; 9.2 the methods used); the comparison table and the duplicated inventory of results are removed; Section 10 opens with the central result (the return map and the exchange cycle). Data-availability paragraph names v008. No mathematics changed.

## Status
Complete mathematical research manuscript with independently reproduced computational certification (independent in implementation and method, within the collective).

## Changes from v008 (Version 2.6 -> 2.7)
Bibliographic only; no theorem, proof, figure or table changed. The Data and code availability section and the bibliography now carry commit-pinned references to the research source collection UNNS_ARITHMETIC_DYNAMICS (repository ukbbi/UNNS, commit 22d8c2e23f49fb98a5b04c6b7efe9ba0a3703808) and to two releases in it that support the arithmetic grammar: UNNS_U4_GEN_v001 (archive SHA-256 042eb5b0...) and UNNS_U2_001_v001 (archive SHA-256 561a9558...). A sentence in the introduction cites them where the transition x -> x(N+1)^2/N and its graph are first described. The text states explicitly that the ADJ4 release (UNNS_GUP_ADJ4_v001) and its audit (UNNS_GUP_ADJ4_AUDIT_v001) are not part of that collection and remain separately identified by their own SHA-256 values. The PDF has 20 pages (the stated count now matches the compiled file). Collection contents were checked against the repository at the pinned commit; the collection's own reference map records that the ADJ4 sources are absent from it.
