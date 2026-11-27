# Consolidation audit, 27 November 2026 (collection v001)

Historical record: it describes the state before the foundational audit. For the current state see `REVIEW_CONSOLIDATION_v002.md` and `REVIEW_STATUS.md`.

Population examined: `01_THEORY/REGISTER.csv`, the release tables and proof files of ANS-I v001 to v015, ANS-II v001 and v002 and ANS-II-ND v001 to v003, and the baseline note. The audit read statements, review columns and citations. **It did not re-verify the proofs**, apart from the item in section 5.

## 1. Population
- The register has 152 rows. The collection has 130 catalogued entries and 20 open-question lines. ANS-T11 appears in both: a criterion is proved and the classification is open.
- In the register but without an entry: ANS-T29, ANS2-O1, ANS2-O2, ANS2-O4, ANS2-O8. These are earlier questions answered (T29 for the critical line only, by T31) by later results.
- Listed by the collection but absent from the register: ANS-C2 (a conjecture in the v001 table) and ANS-LIM (a label created here for the open limit at s = 1).
- ANS-N1 (a computed second term of A_2, value -4.5451) is in the v001 release table only. It is not catalogued as a theorem.
- AS-003 and AS-004 appear only in the baseline note. They became ANS-T01 onwards and were extended by ANS-T09.
- The register has one row for ANS-T14 (the proofs have parts a and b) and one for ANS-T46s (parts i to iii). The catalogue keeps one entry for each.

## 2. Review status (needs a UNNS Research Collective decision)
- The fifteen ANS-I v001 results (T01 to T15) have no per-result verdict. The register says Pending. The ANS-I release table says "Sharp-boundary and growth proofs reviewed; freeze after the Windows run"; the v001 README says it awaits review.
- Other entries without a verdict: T28a, T49, T50, ANS2N-T12a, ANS2N-T14, ANS2N-T15.
- Entries with an internal check of a UNNS Research Collective proposal only: T16 to T21, T23a, T48a, T48b, ANS2N-T12, ANS2N-C12, ANS2N-T13.
- In the recorded graph, 63 of 91 reviewed results rest on at least one result without a UNNS Research Collective verdict. The fourteen results concerned are T03, T05, T09, T10, T12, T15, T16 to T21, T23a and T28a. Verdicts on these fourteen would clear every such mark. The largest are T15 and T17 (40 reviewed results each), T03 and T12 (33 each).
- No verdict was inferred or entered by this audit.

## 3. Records that are out of step (not edited)
- Register, ANS-T46b: evidence CONJECTURE, although k = 2 and k = 3 are proved (T45, T46k). The catalogue records both.
- Register, ANS-T46q: CONJECTURE without the proved cases k = 2, 3. The catalogue names them.
- ANS-I release table: v003 is shown as "open for review" although T24a and T27 have UNNS Research Collective verdicts.
- ANS-II-ND has no README at its root.
- ANS-I v004 has no release archive of its own. ANS-I v001 is not frozen (Windows run pending).
- `01_THEORY/OPEN.md` contains questions since answered; `OPEN_PROBLEMS/` is the consolidated list.

## 4. Superseded and strengthened results
Recorded as relations in the compendium and in `DEPENDENCIES.json`. All earlier statements are retained under their identifiers.

## 5. ANS-T46h: check of an unwritten step
Release v012 declares valid, without a derivation, the UNNS Research Collective's identity sum Phi(M) M^(-2s) = zeta(2s) zeta(3s) zeta(4s) B_Phi(s). Check made here:

With z = p^(-s), t = z^2 and Phi(p^v) = 1 + (1-z)(floor(v/2) + ceil(v/2) z), the sums of t^v, floor(v/2) t^v and ceil(v/2) t^v are 1/(1-t), t^2/((1-t)(1-t^2)) and t/((1-t)(1-t^2)). The local factor is therefore (1 + z^3 - z^4 - z^5) / ((1-z^2)(1-z^4)). Multiplying by (1-z^2)(1-z^3)(1-z^4) gives B_p = 1 - z^4 - z^5 - z^6 + z^7 + z^8, which agrees with the factor used in v012 section 3.2. The product converges absolutely for Re s > 1/4. The difference between the sums with (M+1)^(-2s) and M^(-2s) converges absolutely for Re s > 0. Hence the stated continuation of R_1 to Re s > 1/4, with the simple pole at 1/3 coming from zeta(3s). This is an internal check made during consolidation; it is not a UNNS Research Collective review.

## 6. Method and limits
- Statements are copied by program from fixed line ranges. The ranges were chosen by hand. Some entries include accompanying text, and some statements refer to definitions or displays elsewhere in the source.
- Dependencies were recorded by hand from citations. They are a lower bound.
- Review codes were assigned from the release tables, the register and the review records kept in the releases.
- Region grouping and entry titles are new editorial material of this collection.
