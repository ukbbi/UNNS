import SCR_IV_Prune
/-! IV-3 axiom audit (separate from the frozen v001 `SCR_IV_Check.lean`, which is unchanged and still audits the 25 IV-1/IV-2 theorems).
Every theorem below must depend on no `sorryAx` and no `Lean.ofReduceBool`. -/
open SCR_IV
#print axioms decomposition
#print axioms mul_pm_ge
#print axioms cross_ge
#print axioms uu_ge
#print axioms lower_bound_self
#print axioms lower_bound
#print axioms bound_exact_at_leaf
#print axioms prune_sound
#print axioms prune_no_strict_improvement
#print axioms prune_strict_keeps_ties
#print axioms prune_may_discard_tie
#print axioms guarded_prune_interface
#print axioms partition_cover
#print axioms partition_disjoint
#print axioms partition_sound
#print axioms kRows_eq
#print axioms hScaled_eq_Hs
#print axioms Apair_succ
#print axioms pathAcc_eq_Apair
#print axioms solverBound_eq
#print axioms solverBound_eq_Bnd
#print axioms solver_leaf_exact
#print axioms guard_prune_sound
#print axioms lower_bound_ids
#print axioms prune_sound_ids
#print axioms prune_strict_ids
#print axioms solver_prune_sound_ids
#print axioms leaf_acc_eq_hScaled
#print axioms partition_ids_cover
#print axioms partition_ids_disjoint
#print axioms partition_ids_sound_plus
#print axioms partition_ids_sound_minus
#print axioms cppCL_eq
#print axioms inCount_bounds
#print axioms violated_persists
#print axioms completed_violation_persists
#print axioms grammar_prune_sound
#print axioms cppPossible_false_sound
#print axioms cppViolates_iff
#print axioms objectives_distinct
#print axioms objective_relation
#print axioms discard_sound_generic
#print axioms discard_ground
#print axioms discard_nonGrammar
