# SCR_III_HELDOUT_FREEZE_v001 — Freeze record for the two held-out studies

**Date:** 2026-10-10 · **Status:** PROTOCOLS_FINAL_FOR_RATIFICATION. The freeze takes effect when Igor confirms (or amends) the six defaults below; hashes are in `SCR_III_HELDOUT_MANIFEST_v001.json`. Nothing has been executed: no discrimination run, no synthetic instance, no real 4×4 energy, no pilot image value.

**Unchanged:** SCR-III-B result (G PASS, P FAIL, T NOT_TESTED, C NOT_ELIGIBLE). It is not weakened or reopened by anything here.

**Frozen choices (from your decision record):** M0/M1/M2; exact enumeration over 1×1, 2×2, 3×3; k = 3 as a screening threshold; T grid 300, 500, 600, 650, 700, 725, 750, 775, 790, 792, 810 K; primary observable nearest-neighbour vertex-type correlation, secondary type fractions and violation density; 30 images per condition as a hypothetical budget; image-level independence, no vertex independence; no effective-temperature fit; gate needs M1 separated from both M0 and M2 on the primary observable. R2 interval [0.790439676056526, 1.0333534753990623] computed from exact frozen values, plus the independent δ_4 < 1 prediction. v010 additive 64-bit solver; n = 24, 28, 32, 36, 40; families S and P; 20 per cell (200 total); ≥18/20 certified at n=40 **per family**; 30 min and 2 GiB per arm; exhaustive comparison at n=28 and no "exhaustive" label for partial n=32 checks; real 4×4 energy prohibited.

**Defaults I chose (please confirm or change before the freeze takes effect):**
1. T1/T2 geometric split (T1 adjacent ins, T2 collinear ins) is a candidate; a mapping record citing the source definition must precede any prediction.
2. Gating SE uses one independent patch per image (most conservative), R = 2000 simulated replicates, with B = 16 and 256 as non-gating sensitivity.
3. Patches 2×2 and 3×3 gated separately and not pooled.
4. Intermediate sizes n = 24…36 are island-prefix sub-instances of the 4×4 geometry.
5. One thread per arm, hardware recorded.
6. The cloud sandbox cannot host 30-minute jobs; the execution host is yours to choose.

**Not authorized:** real 4×4 E0/ground state/gap; external data as confirmatory T evidence; any change to frozen SCR-III-B results. Authorized without freezing anything: building v010 and preparing the logged image pilot (`SCR_III_T_PILOT_LOG_v001.md`).
