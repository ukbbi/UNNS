import SCR_IV_V5
open SCR_IV
/-- NEGATIVE CONTROL: this file MUST FAIL to compile. -/
theorem t : delta4Num claimedGroundNum claimedNonGTrue * 10 ^ 16 < 9459172223430820 * (delta4Den : Int) := by decide +kernel
