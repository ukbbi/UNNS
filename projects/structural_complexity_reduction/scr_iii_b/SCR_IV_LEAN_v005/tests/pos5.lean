import SCR_IV_V5
open SCR_IV
/-- Positive twins: must compile. -/
theorem t1 : claimedNonGTrue - claimedGroundNum = 12095447728404694790 := by decide +kernel
theorem t2 : delta4Num claimedGroundNum claimedNonGTrue * 10 ^ 16 < 9459172223430826 * (delta4Den : Int) + (delta4Den : Int) := by decide +kernel
theorem t3 : (94 : Int) * delta4Den ≤ delta4Num claimedGroundNum claimedNonGTrue * 100 := by decide +kernel
theorem t4 : delta4Num claimedGroundNum claimedNonGTrue * 10 < 10 * (delta4Den : Int) := by decide +kernel
