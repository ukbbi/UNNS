# E2-P4 source and scope addendum (append-only)
1. This release executes spec phases P4-E0, P4-E1, P4-E2 (the section-14 preflight) and records the first scoped theorems for P4-F110.  P4-E3 (residual planar CP3-A search), P4-E4 (coupled 3D census),
   P4-E5 (adversarial falsification, prior-art review) are NOT STARTED; the gates PLANAR_THEOREM_PASS and COUPLED_3D_THEOREM_PASS are NOT_EVALUATED.
2. The E2-P3 local verification stopped after V03 on the device (shell limit); it was not completed locally.  The cloud result 49/49 (full, 1406 s) is as reported.  E2-P4 verification is sharded (RUN_VERIFY.py --shard S0..S5).
3. The spec labels the E2-P3 witness 'denominator 9 -> 3, primes (2,7,13), box (2,2,3)' as a nontrivial-to-nontrivial failure with RECTANGULAR target; it is used here only as a control (Addendum 004 for the infinite family).
4. Direct exact verification of P4-F110 is limited by cost: m=1 forward+reverse and (opt-in) m=2 forward; m >= 3 direct is UNAVAILABLE_COST, covered by P4-T2.
5. Spec 2.3 asked for the (2,7,13) family to be recorded as an E2-P3 addendum: ERRATA/E2_P3_ADDENDUM_004_INFINITE_FAMILY.md.  Copies go to the project's ERRATA/ without overwriting anything.
