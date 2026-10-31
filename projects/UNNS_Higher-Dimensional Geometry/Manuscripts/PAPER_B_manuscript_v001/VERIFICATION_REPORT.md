# Verification report, Paper B v001
Build: pdfTeX 2.6-1.40.25, 53 pages, 0 errors, 0 undefined references, 2 minor overfull boxes (<6 pt).

## Proved in the text (no computation used)
E1 criterion; minimality => full support, 1 in C, no singleton circuits; rigidity and its converse; vector-space partition; counting identity; Parseval identity; threshold lemma; n2 >= p-1 for p >= 9 with equality cases; local rank-3 extraction; B-LOW; universality r_min = 3 for p >= 9 and conditional on the p <= 8 enumeration.

## Finite computations (own code, exact integer/rational arithmetic) 
- crosscheck.py: 4213 codes, E1 vs direct cell enumeration, 0 mismatches, all minimum ranks = 3; circuit test 0 mismatches.
- classify.py: k=3,4,5 exhaustive over all spanning subsets of AG(k-1,2): 1, 3, 12 classes (matches the release).
- small_p.py: complete enumeration for p <= 8 (simplex normal form); every minimal box has n2 >= 2 (W2).
- verify6.py: 215 source-reported k=6 representatives: all spanning, non-embedded, shortenings embedded; counting/Parseval/vsp hold; equiv6.py: 8 invariant-tied pairs inequivalent.
- Source checkers run unchanged: 231 partition certificates accepted, 0 rejected.

## Source-reported, not reproved
Completeness of the k=6 classification (215 classes), GEO-I v010 BINARY6.md.

## Limits
GitHub not fetchable; local release copies and the author-supplied commit were used. External references read at catalogue/abstract level only. Rank three is a statement about a local witness, not a polynomial-time algorithm; the binary model does not assert that every binary code is realized by a rational UNNS occurrence fibre. No novelty or priority claims.

## v001a corrections (after external review)
- Abstract now states that W2/r_min=3 rest on analytic proof for p>=9 plus exhaustive enumeration for p<=8.
- verify_all.sh: pipefail, no `|| true`; runs checker11 and checker10 with enforced exit status.
- Math removed from PDF bookmarks (texorpdfstring).
- verify_all.sh: optional checker8 now an if/else (a failing checker cannot be mistaken for a missing one); final line reads ALL EXECUTED CHECKS PASSED.

## v001b: Section 20 literature comparison
Sources read in full: Heden survey (arXiv:1103.1031), Kurz (1708.01113, 2302.08939), Cooper-Okur (2504.08083), Margolis-Saliola-Steinberg (1508.05446, Bohne-Dress statement only), D.S. Kim (0909.0809, Pless identity statement). Others catalogue-level only. New checks in scripts/lit_checks.py (Heden tail bound on 231 classes: 0 violations; E1 vs Cooper-Okur on 2000 random multigraphs: 0 mismatches). Both are consistency checks, not proofs; no proof in the paper uses them.

## Terminology addition
Added Section 1.1 (relation to arithmetic occurrence geometry) and a notation note; no proof, theorem statement or computation changed.

Terminology revision 2: explicit adoption sentence in Section 1.1; Appendix A corrected (Paper A scope; collision and witness rank defined in Paper B).
