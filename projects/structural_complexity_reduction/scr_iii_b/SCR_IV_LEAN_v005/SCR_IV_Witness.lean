import SCR_IV_Spins
import SCR_IV_Grammar
import SCR_IV_Hamiltonian
/-! # IV-2: the two frozen witnesses. These theorems certify the WITNESSES only (membership, exact energy, agreement with the reported
doubles). They say NOTHING about global optimality (that is IV-3/IV-4, PENDING). -/
namespace SCR_IV

def groundId : Nat := 711243241830
def nonGId : Nat := 161487427942

theorem ground_valid : ValidId groundId := by decide +kernel
theorem nonG_valid : ValidId nonGId := by decide +kernel

/-! ## Membership -/
theorem ground_in_grammar : IsGrammar groundId := by decide +kernel
theorem ground_counts : inCounts groundId = List.replicate 16 2 := by decide +kernel
theorem nonG_violations : violations nonGId = 1 := by decide +kernel
theorem nonG_not_in_grammar : ¬ IsGrammar nonGId := by decide +kernel
theorem nonG_violating_vertex : violatingVertices nonGId = [3] := by decide +kernel
theorem nonG_counts :
    inCounts nonGId = [2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2] := by decide +kernel

/-! ## Exact energies (scaled by 2^kShift, A units) -/
theorem ground_energy_exact : hScaled groundId = claimedGroundNum := by decide +kernel
theorem nonG_energy_exact : hScaled nonGId = claimedNonGNum := by decide +kernel
theorem ground_energy_indexed : hIndexed groundId = hScaled groundId := by decide +kernel
theorem nonG_energy_indexed : hIndexed nonGId = hScaled nonGId := by decide +kernel

/-- Exact rational energies of the encoded Hamiltonian. -/
theorem ground_hRat : hRat groundId = (claimedGroundNum : Rat) / ((2 ^ kShift : Nat) : Rat) := by
  unfold hRat; rw [ground_energy_exact]
theorem nonG_hRat : hRat nonGId = (claimedNonGNum : Rat) / ((2 ^ kShift : Nat) : Rat) := by
  unfold hRat; rw [nonG_energy_exact]

/-! ## Agreement with the reported solver doubles: |H_exact - reported| <= 1e-16 A (observed ~4e-17) -/
theorem ground_matches_reported :
    (hScaled groundId * 2 ^ reportedGround.2 - reportedGround.1 * 2 ^ kShift).natAbs * 10 ^ 16
      ≤ 2 ^ (kShift + reportedGround.2) := by decide +kernel
theorem nonG_matches_reported :
    (hScaled nonGId * 2 ^ reportedNonG.2 - reportedNonG.1 * 2 ^ kShift).natAbs * 10 ^ 16
      ≤ 2 ^ (kShift + reportedNonG.2) := by decide +kernel

/-! ## Witness-level ordering (NOT a claim about minima) -/
theorem witness_order : hScaled groundId < hScaled nonGId := by decide +kernel

/-- Witness-level normalised gap d = (H(nonG)-H(ground)) * A / (kB*792 K), with A = aJoule (exact double) and
kB*792 = 1093474008 / 10^29 J = 1.093474008e-20 J exactly (kB = 1.380649e-23 J/K, SI-exact). This bounds nothing about the true minima; it only evaluates the two witnesses. -/
theorem witness_gap_interval :
    9459172 * (2 ^ (kShift + aJoule.2) * 1093474008) <
      ((hScaled nonGId - hScaled groundId) * aJoule.1 * 10 ^ 29 * 10 ^ 7).toNat ∧
    ((hScaled nonGId - hScaled groundId) * aJoule.1 * 10 ^ 29 * 10 ^ 7).toNat <
      9459173 * (2 ^ (kShift + aJoule.2) * 1093474008) := by
  decide +kernel

end SCR_IV
