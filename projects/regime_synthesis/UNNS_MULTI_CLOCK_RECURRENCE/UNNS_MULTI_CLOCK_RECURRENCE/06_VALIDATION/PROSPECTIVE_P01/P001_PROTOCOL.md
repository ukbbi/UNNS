# P001 PROSPECTIVE PAIR PROTOCOL

## Status

**PRE-GENERATION LOCK**

This prospective pair is registered after `MC_GRAMMAR_v001` was frozen and before either
trajectory is generated.

## Scientific role

P001 is a prospective **external-model transfer test**.

It is not a direct reproduction of the source paper's exact irrational ratio.

The published Marripour–Abouie model is retained, but the ratio is pre-registered as

`Omega / omega_d = 1 / phi`

so that the test lies inside the frozen empirical ratio domain of `MC_GRAMMAR_v001`.

No outcome from this adapted model has been inspected.

## Pair

Both records use the same:

- model Hamiltonian;
- disorder realizations;
- J = 5.5;
- h = 0.3;
- L = 4 periodic chain;
- initial |+x> product state;
- observable mx(t);
- 64 drive periods;
- 16 samples per period;
- 100 disorder realizations.

Only the overall drive-frequency scale differs.

### Candidate hypothesis

`omega_d = 12`

Expected from the source model's frequency hierarchy:
long-lived prethermal quasiperiodic temporal order.

### Control hypothesis

`omega_d = 1`

Expected from the source model:
rapid heating / loss of long-lived temporal order.

## Blind assignment

The two trajectories are exposed to the grammar only as:

- `P001_A`
- `P001_B`

The A/B mapping has been cryptographically committed before generation.

The mapping itself is not present in this package.

## Frozen grammar run

The blind run must produce:

- domain eligibility;
- ratio-domain eligibility;
- P_src phase-label null probability;
- J_frac;
- M_frac;
- Fourier-phase null probability;
- six frozen robustness M values;
- frozen temporal state;
- failure flags.

All numeric outputs must be hashed before reveal.

## Prohibitions

- no parameter tuning after generation;
- no changing L, J, h, time horizon, sampling, disorder count, or ratio;
- no changing grammar gates;
- no changing surrogate counts;
- no C003;
- no reveal before the quantitative lock.

The next research-chain box after blind analysis is **reveal**.
