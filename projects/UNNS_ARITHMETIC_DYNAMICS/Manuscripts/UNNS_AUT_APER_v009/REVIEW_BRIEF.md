# Review brief (outside reader)
Claim: for the 22-move, 4-prime priority selector ADJ4 (see paper Defs 4.3-4.4), the selected return on Sigma = {2^a 5^z} is z' = (2869 z + delta_{a,r})/49 with the 98-entry table, and the itinerary is not eventually periodic.
Reproduce: `sh code/run_all.sh` (~1 min); certificate re-run via UNNS_GUP_ADJ4_AUDIT_v001.
Questions:
1. Are Props 6.2-6.4 (regimes I-III) and the balance identity 6.6 correct and complete as proofs?
2. Is the emptiness lemma (7.2) and the obligation scheme (E,D,S,F) sufficient for Lemma 7.1?
3. Is the final-state/selected-return definition well posed given the first-return remark?
4. Is the relation to FRACTRAN and other established mathematics (Section 9) stated with the right scope?
5. Is the non-periodicity claim framed fairly, with the return law and the three-regime mechanism as the main content?
Not claimed: universality, other seeds/orders/prime sets.
