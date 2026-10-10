import SCR_IV_Prune
open SCR_IV
/-- NEGATIVE CONTROL: this file MUST FAIL to compile (the claim is false). The non-grammar witness has a violated vertex, so the filter must keep it. -/
theorem bad : cppPossible nonGId 40 = false := by decide +kernel
