import Mathlib.Algebra.Divisibility.Basic
import Mathlib.Algebra.GroupWithZero.Defs
import Mathlib.Algebra.Ring.Divisibility.Basic

universe u

def VerifyHasFourFactorRefinement (R : Type u) [CommMonoid R] : Prop :=
  ∀ a b c d : R, a * b = c * d →
    ∃ e f g h : R, a = e * f ∧ b = g * h ∧ c = e * g ∧ d = f * h

section

variable {R : Type u} [CommMonoidWithZero R] [IsCancelMulZero R]

theorem verify_endgame
    (hprimal : ∀ a : R, IsPrimal a) :
    VerifyHasFourFactorRefinement R := by
  intro a b c d hab
  by_cases ha : a = 0
  · subst a
    have hcd : c * d = 0 := by simpa using hab.symm
    rcases eq_zero_or_eq_zero_of_mul_eq_zero hcd with rfl | rfl
    · exact ⟨0, d, b, 1, by simp⟩
    · exact ⟨c, 0, 1, b, by simp⟩
  · have hadvd : a ∣ c * d := ⟨b, hab.symm⟩
    obtain ⟨e, f, hec, hfd, haef⟩ := hprimal a hadvd
    obtain ⟨g, hcg⟩ := hec
    obtain ⟨h, hdh⟩ := hfd
    refine ⟨e, f, g, h, haef, ?_, hcg, hdh⟩
    apply mul_left_cancel₀ ha
    calc
      a * b = c * d := hab
      _ = (e * g) * (f * h) := by rw [hcg, hdh]
      _ = (e * f) * (g * h) := by ac_rfl
      _ = a * (g * h) := by rw [← haef]

end
