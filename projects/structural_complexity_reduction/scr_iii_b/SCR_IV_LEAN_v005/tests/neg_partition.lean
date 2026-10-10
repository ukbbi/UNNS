import SCR_IV_Prune
open SCR_IV
/-- NEGATIVE CONTROL: this file MUST FAIL to compile (the claim is false). -/
theorem bad : ∃ s : Nat → Int, Extends (assign (fun _ => 0) 0 1) 1 s ∧ Extends (assign (fun _ => 0) 0 (-1)) 1 s :=
  ⟨fun _ => 1, fun i hi => by simp [assign]; omega, fun i hi => by simp [assign]; omega⟩
