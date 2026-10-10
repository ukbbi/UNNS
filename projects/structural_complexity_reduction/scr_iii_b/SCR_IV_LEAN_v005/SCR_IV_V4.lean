import SCR_IV_CertReal
/-! # IV-4B: corrected non-grammar objective.
Gate 1 of IV-4B (untrusted exact-integer search, `scripts/diag_nong.py`) found a non-grammar configuration with energy strictly below the frozen
SCR-III value `claimedNonGNum`: the ground witness with spin 6 flipped (`nonGTrueId`). Everything in this file is kernel-checked. -/
namespace SCR_IV
def nonGTrueId : Nat := 711243241766
def claimedNonGTrue : Int := -181106494839879485536

theorem nonGTrue_valid : ValidId nonGTrueId := by decide +kernel
theorem nonGTrue_not_in_grammar : ¬ IsGrammar nonGTrueId := by decide +kernel
theorem nonGTrue_violating_vertex : violatingVertices nonGTrueId = [3] := by decide +kernel
theorem nonGTrue_counts : inCounts nonGTrueId = [2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2] := by decide +kernel
theorem nonGTrue_energy_exact : hScaled nonGTrueId = claimedNonGTrue := by decide +kernel
/-- The id differs from the ground witness in exactly one spin. -/
theorem nonGTrue_one_flip : nonGTrueId ^^^ groundId = 64 := by decide +kernel
/-- Gap between the corrected and the frozen non-grammar values, in units of 2^-70 A. -/
theorem frozen_minus_true : claimedNonGNum - claimedNonGTrue = 928 := by decide +kernel

/-- FORMAL STATEMENT OF THE FINDING (unconditional): the frozen SCR-III value `claimedNonGNum` is NOT the exact minimum of the encoded
Hamiltonian over non-grammar configurations; the non-grammar configuration `nonGTrueId` is strictly lower. -/
theorem frozen_nonG_not_min : ¬ ObjNonGrammar claimedNonGNum := by
  intro h
  have := h.2 nonGTrueId nonGTrue_valid nonGTrue_not_in_grammar
  rw [nonGTrue_energy_exact] at this
  have e : claimedNonGNum - claimedNonGTrue = 928 := frozen_minus_true
  omega

/-- CONDITIONAL THEOREM (partitioned form, corrected non-grammar objective). -/
theorem nonGT_min_of_frontier {D0 : Nat} (hD : D0 ≤ 40) {certOf : Nat → Nat}
    (h : ∀ b, b < 2 ^ D0 → subOK Rreal 40 claimedNonGTrue leafGrammar D0 b (certOf b) = true) :
    ObjNonGrammar claimedNonGTrue := by
  refine ⟨⟨nonGTrueId, nonGTrue_valid, nonGTrue_not_in_grammar, nonGTrue_energy_exact⟩, ?_⟩
  intro id _ hng
  have hall : ∀ b, b < 2 ^ D0 → Sub 40 kAt claimedNonGTrue (fun s => (∀ i, i < 40 → s i = sigmaAt id i) ∧ ¬ IsGrammar id) D0 b :=
    fun b hb => subOK_sound (Pp := fun s => (∀ i, i < 40 → s i = sigmaAt id i) ∧ ¬ IsGrammar id) Rreal hR_real
      (fun b hb s hs hP => hP.2 (leafGrammar_sound hb (fun i hi => (hP.1 i hi).symm.trans (hs i hi)))) hD hb (h b hb)
  have := frontier_sound hD hall (sigmaAt id) (pm1_sigmaAt id 0 40) ⟨fun _ _ => rfl, hng⟩
  rw [hScaled_eq]; exact this

theorem batchesOK_nil (R : Nat → List Int) (n : Nat) (U : Int) (leafOK : Nat → Bool) (d lo : Nat) : batchesOK R n U leafOK d lo [] = true := rfl

theorem bcons {R : Nat → List Int} {n : Nat} {U : Int} {leafOK : Nat → Bool} {d lo lo' : Nat} {cs : List Nat} {rest : List (List Nat)}
    (h1 : batchOK R n U leafOK d lo cs = true) (hl : lo + cs.length = lo') (h2 : batchesOK R n U leafOK d lo' rest = true) :
    batchesOK R n U leafOK d lo (cs :: rest) = true := by
  unfold batchesOK; rw [h1, hl, h2]; rfl
end SCR_IV
