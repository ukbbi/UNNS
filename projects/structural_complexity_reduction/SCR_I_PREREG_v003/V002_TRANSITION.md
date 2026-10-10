# v002 → v003 Transition Record

v002 successfully repaired the empty-target defect in v001 by introducing the pinned LIII empirical-viability oracle. Design-only audit then revealed a different mismatch: G1→G4 retained only about 14.7–15.3% of target-positive **candidate identities**.

This does not contradict LIII. LIII's closure result concerns mechanism classes/basins under gate relaxation, not identity preservation for every viable point in a redundant mechanism sample.

v003 therefore changes the preservation unit to target-basin/class geometry while leaving the generator, viability oracle, and G1→G4 unchanged. v002 primary seeds were not executed and are not reused for v003.
