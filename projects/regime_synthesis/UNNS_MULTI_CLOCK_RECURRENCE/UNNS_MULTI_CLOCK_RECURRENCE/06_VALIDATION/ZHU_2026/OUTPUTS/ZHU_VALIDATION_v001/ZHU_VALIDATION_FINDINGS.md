# ZHU VALIDATION v001 — FINDINGS

## Locked outcome

**Assessment: `PARTIAL_TRANSFER_WITH_COVER_DEPTH_FAILURE`**

The external Zhu transfer is **partially supported, not fully validated** under the
predeclared protocol.

### What transferred

Both independent experimental Fig. 1 time-domain records satisfy:

- `full_r2_cv > axis_r2_cv`
- positive `mixed_interaction_gain`
- positive mixed gain under every frozen robustness perturbation

Numerically:

- ZHU_FIG1_C1: axis R2 = 0.505006,
  full R2 = 0.600458,
  mixed gain = 0.095452
- ZHU_FIG1_C3: axis R2 = 0.022075,
  full R2 = 0.522323,
  mixed gain = 0.500249

Thus the source-defined joint two-clock contribution discovered in Luo is also visible
in the independent Zhu experimental trajectories.

### What failed

The predeclared cover-depth prediction failed.

Both records select:

`best_cover_depth = 1`

rather than the predicted `d = 2`.

The d=2 chart still has positive mixed contribution for both records, but it does not
maximize cross-validated full-torus predictability.

This failure is preserved. No cover range, basis, clock ratio, cross-validation rule,
or source adapter was changed after seeing the result.

## Scientific consequence

v002 has **cross-platform evidence for joint source-clock organization**, but its
automatic cover-depth coordinate cannot yet be treated as a portable DTQC depth
identifier.

Therefore:

- do not freeze v002 as the final multi-clock grammar;
- do not tune v002 on Zhu;
- preserve this as a partial positive + explicit negative result;
- next development must explain or replace the depth-selection mechanism using
  development/validation evidence without C003 retrofitting.

No C003 data were used.
