import SCR_IV_Witness
open SCR_IV
/-- NEGATIVE CONTROL: this file MUST FAIL to compile. -/
theorem bad : hScaled groundId = claimedGroundNum + 1 := by decide +kernel
