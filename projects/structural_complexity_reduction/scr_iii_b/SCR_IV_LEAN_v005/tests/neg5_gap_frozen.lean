import SCR_IV_V5
open SCR_IV
/-- NEGATIVE CONTROL: this file MUST FAIL to compile. -/
theorem t : claimedNonGTrue - claimedGroundNum = 12095447728404695718 := by decide +kernel
