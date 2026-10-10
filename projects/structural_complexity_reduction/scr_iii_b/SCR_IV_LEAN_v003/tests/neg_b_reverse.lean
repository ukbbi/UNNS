import SCR_IV_Prune
open SCR_IV
/-- NEGATIVE CONTROL: this file MUST FAIL to compile (the claim is false). -/
theorem bad : Hs 2 (fun _ _ => 5) (fun _ => 1) ≤ Bnd 2 0 (fun _ _ => 5) (fun _ => 1) := by decide
