import SCR_IV_CertReal
/-! IV-4A axiom audit (separate from the unchanged `SCR_IV_Check.lean` and the v002 `SCR_IV_Check3.lean`). No `sorryAx`, no `Lean.ofReduceBool`. -/
open SCR_IV
#print axioms sabs_map
#print axioms addScaled_map
#print axioms bound_of_Inv
#print axioms Tail_succ
#print axioms fld_assign
#print axioms Inv_child
#print axioms chk_sound
#print axioms rootT_eq
#print axioms checkAll_sound
#print axioms stateAt_Inv
#print axioms subOK_sound
#print axioms bitsOf_spec
#print axioms frontier_sound
#print axioms batchOK_sound
#print axioms batchesOK_sound
#print axioms batches_cover
#print axioms hR_real
#print axioms inCount_congr
#print axioms isGrammar_congr
#print axioms leafGrammar_sound
#print axioms ground_min_of_cert
#print axioms nonG_min_of_cert
#print axioms ground_min_of_frontier
#print axioms nonG_min_of_frontier
