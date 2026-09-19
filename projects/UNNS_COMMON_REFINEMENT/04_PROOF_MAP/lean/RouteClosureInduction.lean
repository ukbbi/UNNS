/-
UNNS Common Refinement
Well-Founded Route-Closure Induction

Source alignment:
  gaearon/conway-refinement
  commit 264445c93b78554c408e99e4e7f663693b4e91ab

This file formalizes the narrow route-closure induction proposition extracted by the
UNNS_COMMON_REFINEMENT project.  It deliberately reuses the Conway repository's own
`IsPrimal`, `HasFourFactorRefinement`, and splice theorem rather than introducing a parallel
refinement notion.
-/

import ConwayRefinement.Algebra.Divisibility.Refinement
import Mathlib.Order.WellFounded

universe u v

namespace UNNS.CommonRefinement

section RouteClosureInduction

variable {R : Type u} [CommMonoidWithZero R] [IsCancelMulZero R]
variable {W : Type v}

/--
`HasWellFoundedRouteClosure r rank Base` packages the local hypotheses used by the
well-founded route-closure induction argument.

* `Base 0` keeps the zero case inside the terminal/base regime used by the Conway
  `CommMonoidWithZero` interface.
* Every base element is primal.
* Every nonzero non-base divisibility `a ∣ b * c` admits a retained factor `t`, a
  complementary residual `w`, and routed factors `e,f`, with the residual at strictly
  smaller structural rank.
-/
def HasWellFoundedRouteClosure
    (r : W → W → Prop) (rank : R → W) (Base : R → Prop) : Prop :=
  Base 0 ∧
    (∀ a : R, Base a → IsPrimal a) ∧
      ∀ ⦃a b c : R⦄, a ≠ 0 → ¬ Base a → a ∣ b * c →
        ∃ t w e f : R,
          a = t * w ∧
          t = e * f ∧
          e ∣ b ∧
          f ∣ c ∧
          r (rank w) (rank a)

/--
**Well-Founded Route-Closure Induction.**

If the route-closure hypotheses hold over a well-founded structural rank, then every
element is primal.

The proof uses the Conway repository's
`exists_primalRefinement_of_factor_refinement`: the locally routed block is spliced with
primality of the strictly lower-rank residual supplied by well-founded induction.
-/
theorem forall_isPrimal_of_wellFoundedRouteClosure
    {r : W → W → Prop} {rank : R → W} {Base : R → Prop}
    (hr : WellFounded r)
    (hroute : HasWellFoundedRouteClosure r rank Base) :
    ∀ a : R, IsPrimal a := by
  have hRank : WellFounded (fun x y : R => r (rank x) (rank y)) :=
    WellFounded.onFun (f := rank) hr
  intro a
  induction a using hRank.induction with
  | _ a ih =>
      by_cases hBase : Base a
      · exact hroute.2.1 a hBase
      by_cases ha0 : a = 0
      · subst a
        exact hroute.2.1 0 hroute.1
      · intro b c habc
        obtain ⟨t, w, e, f, hatw, htef, heb, hfc, hwlt⟩ :=
          hroute.2.2 ha0 hBase habc
        have hw : IsPrimal w := ih w hwlt
        obtain ⟨q, hq⟩ := habc
        have heq : a * q = b * c := hq.symm
        exact exists_primalRefinement_of_factor_refinement
          ha0 heq hatw htef heb hfc hw

/--
The route-closure induction hypotheses imply Conway's binary four-factor refinement
property through the repository's exact equivalence between every-element primality and
`HasFourFactorRefinement`.
-/
theorem hasFourFactorRefinement_of_wellFoundedRouteClosure
    {r : W → W → Prop} {rank : R → W} {Base : R → Prop}
    (hr : WellFounded r)
    (hroute : HasWellFoundedRouteClosure r rank Base) :
    HasFourFactorRefinement R := by
  rw [hasFourFactorRefinement_iff_forall_isPrimal]
  exact forall_isPrimal_of_wellFoundedRouteClosure hr hroute

-- Source-interface checks.  These make the intended dependency on the audited Conway
-- algebra layer explicit when this file is compiled inside that repository.
#check IsPrimal
#check HasFourFactorRefinement
#check exists_primalRefinement_of_factor_refinement
#check hasFourFactorRefinement_iff_forall_isPrimal
#check WellFounded.onFun

end RouteClosureInduction

end UNNS.CommonRefinement
