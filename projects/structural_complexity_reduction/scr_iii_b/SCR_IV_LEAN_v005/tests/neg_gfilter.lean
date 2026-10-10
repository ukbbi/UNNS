import SCR_IV_Prune
open SCR_IV
/-- NEGATIVE CONTROL: this file MUST FAIL to compile (the claim is false). -/
theorem bad : cppPossible 0 0 = false := by decide +kernel
