import SCR_IV_Witness
open SCR_IV
/-- NEGATIVE CONTROL: this file MUST FAIL to compile. -/
theorem bad : IsGrammar groundId ∧ violations groundId = 1 := by decide +kernel
