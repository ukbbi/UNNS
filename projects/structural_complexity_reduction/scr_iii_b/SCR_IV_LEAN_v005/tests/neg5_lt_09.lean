import SCR_IV_V5
open SCR_IV
/-- NEGATIVE CONTROL: this file MUST FAIL to compile. -/
theorem t : delta4Num claimedGroundNum claimedNonGTrue * 10 < 9 * (delta4Den : Int) := by decide +kernel
