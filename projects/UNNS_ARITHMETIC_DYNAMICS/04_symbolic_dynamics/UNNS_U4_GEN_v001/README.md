# UNNS_U4_GEN_v001 — Intrinsic Branching and Autonomous Generative Dynamics (no manuscript)
Author: UNNS Research Collective. STAGE2_v001 and M2_ENT_v001 preserved unchanged (hashes: inherited/INHERITED_RELEASES.txt).
Contents: docs/PROOFS_GEN.md (GEN-1..GEN-4, accounting, observations, status), data/gen_config.json + gen_registration.json (grammar, starts, predictions, tolerances, hashes), code/ (experiments, theory checks, independent layers, verifier), data/ and reports/ (machine-readable results, ledger, registry addendum), SHA256SUMS.
Run `python3 code/verify_gen.py` (~6 min; `--quick` skips the 229 s theory checks). Exact results are compared exactly, floats within 1e-9 (the ENT verifier's strict float comparison problem is handled by code/ent_compat_check.py without modifying ENT).

Headline results
* GEN-1 (proved): a finite-control, K-history, time-independent selector that returns to any vertex infinitely often is eventually periodic (entire trajectory); non-periodic itineraries need a moving hub and unbounded state.
* GEN-2 (proved): prime-fire selectors fire primes >=5 only finitely often; tail alphabet {2,3}.
* GEN-3 (proved): the smallest-prime-factor rule is eventually (3,2,2,2,2)^inf.
* GEN-4 (proved, (c) modulo the classical Sturmian theorem): MAXPP — fire the prime with the largest prime-power part — is a vertex-only, K=0 rule on forward SELECT-II edges whose branch itinerary is not eventually periodic, is Sturmian (complexity n+1), has zero entropy, uses unbounded integer state (>=2n bits at step n) and no external input.
* Not established: positive-entropy autonomous branching, universality, composite-branching theory (observations only: periods 164, 2, 5), preservation of SELECT/FIELD/GIG, originality.

Disclosures
1. The rules and the MAXPP idea came from development exploration (data/dev_exploration_log.txt, code/dev_explore*.py: starts 2..39 and a handful of others, float comparison) BEFORE registration; registered starts are disjoint (41..200 and structured) except the structured seeds.
2. The experiment and theory scripts were first run once BEFORE their hashes were written to gen_registration.json (outputs kept in reports/unregistered_first_run_*.json); after registration they were re-run and are byte-identical in content (deterministic), but the registration order was not ideal.
3. Random-selector corroboration of GEN-1 is weak (14 of 162 runs had a repeated configuration). Stage-2 replay: 133 rows, 0 mismatches, 5 larger rows skipped (x>1e10).
4. The GEN-G3 audit in the verifier only checks that every rule has a recorded one-line description; the substantive evidence is the rule sources in code/gen_experiments.py.
5. Proofs are author-level; Sturmian complexity (c) is imported; prior-art review (Fractran/Conway counter dynamics, rotation codings) not done; inherited releases NOT_RERUN except where stated.
