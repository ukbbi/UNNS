import SCR_IV_Spins
import SCR_IV_Data
/-! # IV-1 (Hamiltonian): H(s) = sum_{i<j} K_ij s_i s_j with the 780 frozen couplings as EXACT dyadic rationals.
K_ij = kRows[i][j-i-1] / 2^kShift. Provenance: the coefficient is the binary64 value read by the frozen solver from data/real_4x4.txt
(see data/coeff_bits.csv and scripts/gen_lean_data.py); no rounding is applied beyond that parse. The Lean statements below are about this
EXACT ENCODED finite Hamiltonian, not about an idealised infinite-precision physical coupling. -/
namespace SCR_IV

def dot : List Int → List Int → Int
  | a :: as, b :: bs => a * b + dot as bs
  | _, _ => 0

/-- sum_{i<j} K_ij s_i s_j (scaled by 2^kShift), with the spins given as a list. -/
def hAux : List Int → List (List Int) → Int
  | si :: srest, row :: rows => si * dot row srest + hAux srest rows
  | _, _ => 0

/-- Scaled energy: H(id) = hScaled id / 2^kShift  (A units). -/
def hScaled (id : Nat) : Int := hAux (sigma id) kRows

/-- Exact rational energy in A units. -/
def hRat (id : Nat) : Rat := (hScaled id : Rat) / ((2 ^ kShift : Nat) : Rat)

/-- Second, independently written evaluation with explicit index arithmetic (checks the row/column convention). -/
def hIndexed (id : Nat) : Int :=
  (List.range nSpins).foldl (fun acc i =>
    acc + ((List.range nSpins).foldl (fun a j =>
      if i < j then a + (kRows.getD i []).getD (j - i - 1) 0 * sigmaAt id i * sigmaAt id j else a) 0)) 0

theorem kRows_count : (kRows.map List.length).sum = 780 := by decide +kernel

theorem kRows_shape : (kRows.length = 40) ∧
    ((List.range 40).all (fun i => (kRows.getD i []).length == 39 - i) = true) := by
  constructor <;> decide +kernel

end SCR_IV
