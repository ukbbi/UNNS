import SCR_IV_Sums
import SCR_IV_Bound
import SCR_IV_Spins
import SCR_IV_Data
import SCR_IV_Hamiltonian
/-! # IV-3 (bridge): the abstract energy `Hs` equals the frozen list-based energy `hScaled` for EVERY configuration id.
`kAt i j` is the frozen coupling K_ij (scaled by 2^70) read from `kRows`. The identity is proved by structural induction over the
list recursion of `hAux`; the 2^40-element space is never enumerated. The only kernel-evaluated fact is that `kRows` is
literally the table `rowsL kAt 40 0 40` (a 780-entry comparison). -/
namespace SCR_IV

/-- Frozen coupling K_ij (numerator, denominator 2^70), upper triangle i < j. -/
def kAt (i j : Nat) : Int := (kRows.getD i []).getD (j - i - 1) 0

/-- `lst f a m = [f a, f (a+1), ..., f (a+m-1)]`. -/
def lst (f : Nat → Int) : Nat → Nat → List Int
  | _, 0 => []
  | a, m + 1 => f a :: lst f (a + 1) m

/-- `rowsL K n a m` = the rows a, a+1, ..., a+m-1 of the upper-triangular table of an `n`-spin coupling matrix. -/
def rowsL (K : Nat → Nat → Int) (n : Nat) : Nat → Nat → List (List Int)
  | _, 0 => []
  | a, m + 1 => lst (K a) (a + 1) (n - (a + 1)) :: rowsL K n (a + 1) m

/-- The frozen table is exactly the table generated from `kAt` (kernel-evaluated; compares 780 integers). -/
theorem kRows_eq : kRows = rowsL kAt 40 0 40 := by decide +kernel

theorem map_range_eq_lst (f : Nat → Int) (m : Nat) : ∀ a, (List.range m).map (fun t => f (a + t)) = lst f a m := by
  induction m with
  | zero => intro a; simp [lst]
  | succ m ih =>
    intro a
    rw [List.range_succ_eq_map]
    simp only [List.map_cons, List.map_map, lst]
    have h := ih (a + 1)
    have e : (fun t => f (a + t)) ∘ Nat.succ = fun t => f (a + 1 + t) := by
      funext t; simp only [Function.comp]; congr 1; omega
    rw [e, h]; simp

theorem sigma_eq_lst (id : Nat) : sigma id = lst (sigmaAt id) 0 40 := by
  have h := map_range_eq_lst (sigmaAt id) 40 0
  simpa [sigma] using h

theorem dot_lst (g s : Nat → Int) (m : Nat) : ∀ a, dot (lst g a m) (lst s a m) = sumFrom (fun j => g j * s j) a m := by
  induction m with
  | zero => intro a; simp [lst, dot, sumFrom_zero]
  | succ m ih => intro a; rw [sumFrom_succ_left]; simp only [lst, dot]; rw [ih (a + 1)]

theorem hAux_lst (K : Nat → Nat → Int) (s : Nat → Int) (n m : Nat) : ∀ a, a + m = n →
    hAux (lst s a m) (rowsL K n a m) = sumFrom (fun i => s i * sumFrom (fun j => K i j * s j) (i + 1) (n - (i + 1))) a m := by
  induction m with
  | zero => intro a _; simp [lst, rowsL, hAux, sumFrom_zero]
  | succ m ih =>
    intro a ha
    rw [sumFrom_succ_left]
    simp only [lst, rowsL, hAux]
    have e : n - (a + 1) = m := by omega
    rw [e, dot_lst, ih (a + 1) (by omega)]

/-- THEOREM (bridge): for EVERY id, the frozen list energy equals the abstract energy of the decoded spins. -/
theorem hScaled_eq_Hs (id : Nat) : hScaled id = Hs 40 kAt (sigmaAt id) := by
  unfold hScaled
  rw [sigma_eq_lst, kRows_eq, hAux_lst kAt (sigmaAt id) 40 40 0 (by omega)]
  unfold Hs
  rw [sumFrom_zero_left]

end SCR_IV
