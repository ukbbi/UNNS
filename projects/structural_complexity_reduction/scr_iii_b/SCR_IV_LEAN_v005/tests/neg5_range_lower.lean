import SCR_IV_V5
open SCR_IV
/-- NEGATIVE CONTROL: this file MUST FAIL to compile. -/
theorem t : (95 : Int) * delta4Den ≤ delta4Num claimedGroundNum claimedNonGTrue * 100 := by decide +kernel
