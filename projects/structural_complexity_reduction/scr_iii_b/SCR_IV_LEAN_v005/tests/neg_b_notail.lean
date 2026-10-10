import SCR_IV_Prune
open SCR_IV
/-- NEGATIVE CONTROL: this file MUST FAIL to compile (the claim is false). -/
theorem bad : Apair 0 (fun _ _ => 5) (fun i => if i = 0 then 1 else -1) - Fsum 2 0 (fun _ _ => 5) (fun i => if i = 0 then 1 else -1) ≤ Hs 2 (fun _ _ => 5) (fun i => if i = 0 then 1 else -1) := by decide
