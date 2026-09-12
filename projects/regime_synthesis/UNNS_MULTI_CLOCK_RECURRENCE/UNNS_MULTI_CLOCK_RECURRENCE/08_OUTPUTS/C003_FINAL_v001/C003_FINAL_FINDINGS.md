# C003 FINAL EVALUATION UNDER MC_GRAMMAR_v001

## Historical boundary

Under the frozen integer-depth TIME-CRYSTAL-I grammar, C003 was not supported:

- candidate: q0=6, C=0.198765,
  F=0.093433, p=0.960199,
  `NO_TEMPORAL_ORDER`;
- control: q0=6, C=0.094640,
  F=0.030874, p=0.995025,
  `NO_TEMPORAL_ORDER`.

## Final frozen multi-clock result

### C003 candidate — Fig.1d

- P_src phase-label p = 1.000
- J_frac = 0.910688
- M_frac = 0.596092
- Fourier-phase p = 0.020
- minimum robust M_frac = 0.595093
- state = `SOURCE_UNANCHORED`
- failure flags = `SOURCE_UNANCHORED`

### Matched breakdown control — Fig.1b

- P_src phase-label p = 0.010
- J_frac = -0.593846
- M_frac = -0.003958
- Fourier-phase p = 0.780
- minimum robust M_frac = -0.558942
- state = `MIXED_ORGANIZATION_WEAK`
- failure flags = `MIXED_ORGANIZATION_WEAK;MIXED_ORGANIZATION_SPECTRAL_NULL;MIXED_ORGANIZATION_UNSTABLE`

## Final outcome

`C003_REMAINS_OUTSIDE_FROZEN_MULTI_CLOCK_GRAMMAR`

The grammar was not changed for C003.

This result must also be read alongside the failed P001 prospective transfer:
MC_GRAMMAR_v001 is already known not to admit every external multi-clock/prethermal
construction, so the C003 result is not produced by a universally permissive detector.
