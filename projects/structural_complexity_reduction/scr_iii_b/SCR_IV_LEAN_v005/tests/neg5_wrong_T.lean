import SCR_IV_V5
open SCR_IV
/-- NEGATIVE CONTROL: this file MUST FAIL to compile. -/
theorem t : delta4Num claimedGroundNum claimedNonGTrue < ((2 ^ kShift * 2 ^ aJoule.2 * kBNum * 700 : Nat) : Int) := by decide +kernel
