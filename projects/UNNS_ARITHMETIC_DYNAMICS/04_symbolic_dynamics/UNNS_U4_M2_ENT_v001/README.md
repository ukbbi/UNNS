# UNNS_U4_M2_ENT_v001 (addendum to UNNS_U4_STAGE2_v001; no manuscript)
Author: UNNS Research Collective. STAGE2_v001 is preserved unchanged (hash in inherited/, NOT_RERUN).
* docs/PROOFS_ENT.md — Theorem E1 (h_top(Y_NB(F(x))) >= 1/4 log(tau(x)-1), sup = infinity), entropy conventions E2, separation proposition E5, status table.
* docs/NEXT_STAGE_PROPOSAL.md — U4-GEN proposal (not registered, nothing claimed).
* code/ent_verify.py (independent exact-integer layer), code/verify_ent.py (one command, relative paths), reports/, data/registry_ent_addendum.json.
Verification: block cycles legal for all x<=200 and x=2^m, m=2..9; 16,578 concatenation words incl. join windows; Collatz–Wielandt certified (exact rational) finite-state lower bounds exceed m^(1/4) for m=2..9.
Correction recorded: the divisor N=1 must be excluded (y=4x gives a backtracking walk); branches = tau(x)-1; for x=2^m this is m, as in the review.
Limitations: author-level proofs; no external or prior-art review; irreducibility of countable Y_NB open; no autonomous-generation claim; SELECT/FIELD/GIG preservation open.
