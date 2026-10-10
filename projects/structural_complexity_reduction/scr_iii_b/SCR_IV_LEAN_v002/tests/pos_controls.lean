import SCR_IV_Prune
open SCR_IV
/-! POSITIVE TWINS of the negative controls: the same concrete instances with the TRUE statements. This file MUST compile; it shows the
negative controls fail because their claims are false, not because of a syntax or elaboration problem. -/
abbrev Kc : Nat → Nat → Int := fun _ _ => 5
abbrev s01 : Nat → Int := fun i => if i = 0 then 1 else -1
theorem t_nofield : Hs 2 Kc s01 < Apair 1 Kc s01 - Tail 2 1 Kc := by decide
theorem t_notail : Hs 2 Kc s01 < Apair 0 Kc s01 - Fsum 2 0 Kc s01 := by decide
theorem t_reverse : Bnd 2 0 Kc (fun _ => 1) ≤ Hs 2 Kc (fun _ => 1) := by decide
theorem t_tie : Hs 1 (fun _ _ => 0) (fun _ => 1) = 0 ∧ (0:Int) ≤ Bnd 1 0 (fun _ _ => 0) (fun _ => 1) := by decide
theorem t_partition : ¬ (Extends (assign (fun _ => 0) 0 1) 1 (fun _ => 1) ∧ Extends (assign (fun _ => 0) 0 (-1)) 1 (fun _ => 1)) :=
  partition_disjoint _ _ _
theorem t_gfilter : cppPossible 0 0 = true := by decide +kernel
theorem t_solver : solverBound 2 0 Kc (fun _ => 1) 0 = -5 := by decide
theorem t_gfilter_leaf_nonG : cppPossible nonGId 40 = true := by decide +kernel
theorem t_gfilter_leaf_ground : cppPossible groundId 40 = false := by decide +kernel
theorem t_viol_ground : cppViolates groundId = false := by decide +kernel
theorem t_viol_nonG : cppViolates nonGId = true := by decide +kernel
