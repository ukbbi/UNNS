import SCR_IV_Sums
import SCR_IV_Bound
import SCR_IV_Bridge
/-! # IV-3 (solver-faithful bound): the exact bound formula of `solver_v010.cpp::bound(d, acc)` and of its path accumulator,
transcribed loop-for-loop (in exact integer arithmetic) and proved equal to the abstract bound `Bnd`.

C++ (frozen):
  double l = acc;
  for j = d .. n-1:  field = 0; for i < d: field += k[i][j]*spin[i];   l -= fabs(field);   for h = j+1 .. n-1: l -= fabs(k[j][h]);
  return l - guard;                       // guard = 1e-11 * max(1, sum|K|)
  dfs: acc' = acc + s * field_d,   field_d = sum_{i<d} k[i][d]*spin[i]

Scope: the REAL-NUMBER structure of the bound. Binary64 rounding and the outward guard are NOT formalised here (they are the
subject of the SCR-III numerical audit); `guard_prune_sound` shows the guard can only make pruning more conservative in exact
arithmetic, and `guarded_prune_interface` (SCR_IV_Bound) states what a floating-point error bound would have to supply. -/
namespace SCR_IV

/-- field_j = Σ_{i<d} K_ij s_i, accumulated by a left fold exactly like the C++ inner loop. -/
def fieldLoop (K : Nat → Nat → Int) (s : Nat → Int) (d j : Nat) : Int :=
  (List.range d).foldl (fun f i => f + K i j * s i) 0

/-- The C++ `bound(d, acc)` without the guard: the loop nest over j (outer) and h (inner), in the same order. -/
def solverBound (n d : Nat) (K : Nat → Nat → Int) (s : Nat → Int) (acc : Int) : Int :=
  (List.range' d (n - d)).foldl
    (fun l j => (List.range' (j + 1) (n - (j + 1))).foldl (fun l' h => l' - absZ (K j h)) (l - absZ (fieldLoop K s d j)))
    acc

/-- The C++ path accumulator: acc_0 = 0, acc_{d+1} = acc_d + s_d * field_d. -/
def pathAcc (K : Nat → Nat → Int) (s : Nat → Int) : Nat → Int
  | 0 => 0
  | d + 1 => pathAcc K s d + s d * fieldLoop K s d d

theorem foldl_add_range (g : Nat → Int) (m : Nat) : ∀ c, (List.range m).foldl (fun a i => a + g i) c = c + sumTo g m := by
  induction m with
  | zero => intro c; simp [sumTo_zero]
  | succ m ih => intro c; rw [List.range_succ, List.foldl_append, ih, sumTo_succ]; simp; omega

theorem fieldLoop_eq (K : Nat → Nat → Int) (s : Nat → Int) (d j : Nat) : fieldLoop K s d j = fld K s d j := by
  unfold fieldLoop fld
  rw [foldl_add_range]; omega

theorem foldl_range'_sub {F : Int → Nat → Int} (g : Nat → Int) (hF : ∀ l j, F l j = l - g j) (m : Nat) :
    ∀ a c, (List.range' a m).foldl F c = c - sumFrom g a m := by
  induction m with
  | zero => intro a c; simp [sumFrom_zero]
  | succ m ih =>
    intro a c
    rw [List.range'_succ, List.foldl_cons, hF, ih, sumFrom_succ_left]; omega

/-- Triangular Fubini step: the accumulator increment equals the new pair terms. -/
theorem Apair_succ (K : Nat → Nat → Int) (s : Nat → Int) (d : Nat) :
    Apair (d + 1) K s = Apair d K s + s d * fld K s d d := by
  unfold Apair
  rw [sumTo_succ]
  have row : ∀ i, i < d →
      s i * sumFrom (fun j => K i j * s j) (i + 1) (d + 1 - (i + 1)) =
        s i * sumFrom (fun j => K i j * s j) (i + 1) (d - (i + 1)) + s i * (K i d * s d) := by
    intro i hi
    have e : d + 1 - (i + 1) = (d - (i + 1)) + 1 := by omega
    have e2 : i + 1 + (d - (i + 1)) = d := by omega
    rw [e, sumFrom_succ_right, e2, Int.mul_add]
  have hs : sumTo (fun i => s i * sumFrom (fun j => K i j * s j) (i + 1) (d + 1 - (i + 1))) d =
      sumTo (fun i => s i * sumFrom (fun j => K i j * s j) (i + 1) (d - (i + 1))) d +
        sumTo (fun i => s i * (K i d * s d)) d := by
    rw [← sumTo_add]; exact sumTo_congr (fun i hi => row i hi)
  have h2 : sumTo (fun i => s i * (K i d * s d)) d = s d * fld K s d d := by
    unfold fld
    rw [← sumTo_mul_left]
    exact sumTo_congr (fun i _ => by grind)
  have h3 : d + 1 - (d + 1) = 0 := by omega
  rw [hs, h2, h3, sumFrom_zero]; omega

theorem pathAcc_eq_Apair (K : Nat → Nat → Int) (s : Nat → Int) (d : Nat) : pathAcc K s d = Apair d K s := by
  induction d with
  | zero => simp [pathAcc, Apair, sumTo_zero]
  | succ d ih => rw [pathAcc, ih, Apair_succ, fieldLoop_eq]

theorem solverBound_eq (n d : Nat) (K : Nat → Nat → Int) (s : Nat → Int) (acc : Int) :
    solverBound n d K s acc = acc - Fsum n d K s - Tail n d K := by
  unfold solverBound
  have inner : ∀ l j, (List.range' (j + 1) (n - (j + 1))).foldl (fun l' h => l' - absZ (K j h)) (l - absZ (fieldLoop K s d j))
      = l - (absZ (fld K s d j) + sumFrom (fun h => absZ (K j h)) (j + 1) (n - (j + 1))) := by
    intro l j
    rw [foldl_range'_sub (fun h => absZ (K j h)) (fun l h => rfl), fieldLoop_eq]; omega
  rw [foldl_range'_sub (fun j => absZ (fld K s d j) + sumFrom (fun h => absZ (K j h)) (j + 1) (n - (j + 1))) inner]
  unfold Fsum Tail
  rw [sumFrom_add]; omega

/-- THEOREM (faithful bound): the C++ bound evaluated at the C++ accumulator is exactly `Bnd`. -/
theorem solverBound_eq_Bnd (n d : Nat) (K : Nat → Nat → Int) (s : Nat → Int) :
    solverBound n d K s (pathAcc K s d) = Bnd n d K s := by
  rw [solverBound_eq, pathAcc_eq_Apair]; unfold Bnd; omega

/-- At a full assignment the C++ bound (before the guard) is the exact leaf energy. -/
theorem solver_leaf_exact (n : Nat) (K : Nat → Nat → Int) (s : Nat → Int) :
    solverBound n n K s (pathAcc K s n) = Hs n K s := by
  rw [solverBound_eq_Bnd, bound_exact_at_leaf]

/-- THEOREM (solver prune soundness): if the C++ test `bound ≥ incumbent` holds, with any non-negative guard subtracted,
no completion has energy strictly below the incumbent. -/
theorem guard_prune_sound (K : Nat → Nat → Int) {p s : Nat → Int} {d n : Nat} {U g : Int} (hd : d ≤ n)
    (hext : Extends p d s) (hp : Pm1 s d n) (hg : 0 ≤ g)
    (hB : U ≤ solverBound n d K p (pathAcc K p d) - g) : ¬ Hs n K s < U := by
  rw [solverBound_eq_Bnd] at hB
  have := prune_sound K (U := U) hd hext hp (by omega); omega

end SCR_IV
