import SCR_IV_Prune
open SCR_IV
/-- NEGATIVE CONTROL: this file MUST FAIL to compile (the claim is false). -/
theorem bad : (0:Int) < Hs 1 (fun _ _ => 0) (fun _ => 1) := by decide
