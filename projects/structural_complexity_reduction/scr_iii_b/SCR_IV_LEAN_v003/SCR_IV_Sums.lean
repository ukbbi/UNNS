/-! # IV-3 infrastructure: finite sums over exact integers, by structural recursion (core Lean only, no Mathlib). -/
namespace SCR_IV

/-- `sumTo f k = f 0 + f 1 + … + f (k-1)`. -/
def sumTo (f : Nat → Int) : Nat → Int
  | 0 => 0
  | k + 1 => sumTo f k + f k

/-- `sumFrom f a m = f a + f (a+1) + … + f (a+m-1)`. -/
def sumFrom (f : Nat → Int) (a m : Nat) : Int := sumTo (fun t => f (a + t)) m

theorem sumTo_zero (f : Nat → Int) : sumTo f 0 = 0 := rfl
theorem sumTo_succ (f : Nat → Int) (k : Nat) : sumTo f (k + 1) = sumTo f k + f k := rfl
theorem sumFrom_zero (f : Nat → Int) (a : Nat) : sumFrom f a 0 = 0 := rfl
theorem sumFrom_succ_right (f : Nat → Int) (a m : Nat) :
    sumFrom f a (m + 1) = sumFrom f a m + f (a + m) := rfl

theorem sumTo_const_zero (d : Nat) : sumTo (fun _ => (0 : Int)) d = 0 := by
  induction d with
  | zero => rfl
  | succ k ih => rw [sumTo_succ, ih]; rfl

theorem sumTo_congr {f g : Nat → Int} {m : Nat} (h : ∀ t, t < m → f t = g t) :
    sumTo f m = sumTo g m := by
  induction m with
  | zero => rfl
  | succ k ih =>
    rw [sumTo_succ, sumTo_succ, ih (fun t ht => h t (by omega)), h k (by omega)]

theorem sumFrom_congr {f g : Nat → Int} {a m : Nat} (h : ∀ t, t < m → f (a + t) = g (a + t)) :
    sumFrom f a m = sumFrom g a m :=
  sumTo_congr (fun t ht => h t ht)

theorem sumTo_add (f g : Nat → Int) (m : Nat) :
    sumTo (fun t => f t + g t) m = sumTo f m + sumTo g m := by
  induction m with
  | zero => rfl
  | succ k ih => rw [sumTo_succ, sumTo_succ, sumTo_succ, ih]; omega

theorem sumTo_neg (f : Nat → Int) (m : Nat) :
    sumTo (fun t => - f t) m = - sumTo f m := by
  induction m with
  | zero => rfl
  | succ k ih => rw [sumTo_succ, sumTo_succ, ih]; omega

theorem sumTo_mul_left (c : Int) (f : Nat → Int) (m : Nat) :
    sumTo (fun t => c * f t) m = c * sumTo f m := by
  induction m with
  | zero => simp [sumTo_zero]
  | succ k ih => rw [sumTo_succ, sumTo_succ, ih, Int.mul_add]

theorem sumTo_le {f g : Nat → Int} {m : Nat} (h : ∀ t, t < m → f t ≤ g t) :
    sumTo f m ≤ sumTo g m := by
  induction m with
  | zero => exact Int.le_refl _
  | succ k ih =>
    rw [sumTo_succ, sumTo_succ]
    have h1 := ih (fun t ht => h t (by omega)); have h2 := h k (by omega); omega

theorem sumTo_split (f : Nat → Int) (m1 m2 : Nat) :
    sumTo f (m1 + m2) = sumTo f m1 + sumTo (fun t => f (m1 + t)) m2 := by
  induction m2 with
  | zero => simp [sumTo_zero]
  | succ k ih =>
    show sumTo f (m1 + k + 1) = _
    rw [sumTo_succ, ih, sumTo_succ]; omega

theorem sumFrom_split (f : Nat → Int) (a m1 m2 : Nat) :
    sumFrom f a (m1 + m2) = sumFrom f a m1 + sumFrom f (a + m1) m2 := by
  unfold sumFrom
  rw [sumTo_split]
  congr 1
  apply sumTo_congr
  intro t _
  rw [Nat.add_assoc]

theorem sumFrom_succ_left (f : Nat → Int) (a m : Nat) :
    sumFrom f a (m + 1) = f a + sumFrom f (a + 1) m := by
  have h := sumFrom_split f a 1 m
  rw [Nat.add_comm 1 m] at h
  rw [h]
  show (sumTo _ 0 + f (a + 0)) + _ = _
  simp [sumTo_zero]

theorem sumFrom_zero_left (f : Nat → Int) (m : Nat) : sumFrom f 0 m = sumTo f m := by
  unfold sumFrom
  apply sumTo_congr
  intro t _
  rw [Nat.zero_add]

/-- Interchange of a rectangular double sum. -/
theorem sumTo_swap (g : Nat → Nat → Int) (d m : Nat) :
    sumTo (fun i => sumTo (fun t => g i t) m) d = sumTo (fun t => sumTo (fun i => g i t) d) m := by
  induction m with
  | zero => simp only [sumTo_zero]; rw [sumTo_const_zero]
  | succ k ih =>
    simp only [sumTo_succ]
    rw [sumTo_add, ih]

theorem sumFrom_add (f g : Nat → Int) (a m : Nat) :
    sumFrom (fun t => f t + g t) a m = sumFrom f a m + sumFrom g a m := sumTo_add _ _ _

theorem sumFrom_neg (f : Nat → Int) (a m : Nat) :
    sumFrom (fun t => - f t) a m = - sumFrom f a m := sumTo_neg _ _

theorem sumFrom_mul_left (c : Int) (f : Nat → Int) (a m : Nat) :
    sumFrom (fun t => c * f t) a m = c * sumFrom f a m := sumTo_mul_left _ _ _

theorem sumFrom_le {f g : Nat → Int} {a m : Nat} (h : ∀ t, t < m → f (a + t) ≤ g (a + t)) :
    sumFrom f a m ≤ sumFrom g a m := sumTo_le (fun t ht => h t ht)

end SCR_IV
