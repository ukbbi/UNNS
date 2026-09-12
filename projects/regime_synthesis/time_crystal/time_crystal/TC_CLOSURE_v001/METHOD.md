# TC_CLOSURE_v001 — Method

## 1. Frozen input layer

The run first verifies that:

`TC_PHYS_v001\outputs\physics_validation.json`

has a PASS status.

The correction and mitigation functions from the frozen `TC_PHYS_v001\src\tc_phys.py` are reused rather than reimplemented.

## 2. Remove the physics fitting alignment before closure analysis

`TC_PHYS_v001` temporarily removes the ideal `(-1)^t` sign alternation so that an exponential hardware-decay envelope can be fitted.

That aligned representation cannot be used for a recurrence search because it would erase the very 2T structure being tested.

Therefore `TC_CLOSURE_v001` exactly inverts that alignment and restores the original stroboscopic state sequence before computing any UNNS closure quantity.

## 3. State object

At every Floquet step t, define the accepted-qubit state vector:

`X_t = (M_1(t), ..., M_N(t))`

where the accepted-qubit mask comes entirely from the frozen physics-validation layer.

## 4. Pair recurrence

For recurrence depth q:

`X_t -> X_(t+q)`

Define bounded geometric similarity:

`S_q(t) = 1 - ||X_t - X_(t+q)|| / (||X_t|| + ||X_(t+q)||)`

A perfect recurrence gives 1.

An opposite state gives a value near 0.

## 5. Anti-thermal support

A near-zero thermal state can otherwise produce the trivial statement `0 ~ 0`.

Define the early-time RMS amplitude reference:

`A0 = median_t=0..4 [ ||X_t|| / sqrt(N) ]`

and pair support:

`A_q(t) = clip( min(||X_t||, ||X_(t+q)||) / (sqrt(N) A0), 0, 1 )`

The supported pair closure is:

`K_q(t) = S_q(t) A_q(t)`

## 6. Temporal closure spectrum

The primary UNNS object is:

`C(q) = mean_t K_q(t)`

for:

`q = 1,2,...,10`

No preferred q is supplied.

The q range stops at 10 so every depth still has at least 41 state-pair comparisons in a 51-step record.

## 7. Temporal ladders

For every q, pair terms are also grouped by:

`t mod q = r`

to form q residue ladders.

Their separate closure values are exported to `ladder_closure.csv`.

For a detected q0=2 these are the empirical:

`L0 = {X0, X2, X4, ...}`

`L1 = {X1, X3, X5, ...}`

## 8. Detecting fundamental recurrence depth

The first five epsilon grid points define the low-perturbation seed region.

Their median closure spectrum is formed.

For each interior q:

`P(q) = C(q) - 0.5[C(q-1) + C(q+1)]`

The fundamental candidate q0 is the q with maximum local contrast P(q).

Thus q0 is detected rather than hard-coded.

## 9. Recurrence-family contrast

After q0 is detected, define:

`family = {q : q is a multiple of q0}`

and:

`F = mean C(q in family) - mean C(q outside family)`

For q0=2 this reduces to an even-depth versus odd-depth closure contrast, but the formula itself is generic.

## 10. Exploratory closure-basin edge

The v001 basin rule is:

- first 5 epsilon points = seed basin;
- baseline center = median F;
- scale = `1.4826 * MAD`;
- lower edge = median - 3 robust sigma;
- basin exit = first epsilon for which 2 consecutive F values are below that edge.

A sensitivity table varies:
- seed points: 4, 5, 6;
- sigma multiplier: 2.0, 2.5, 3.0.

A second sensitivity table varies the frozen physics mitigation thresholds.

## 11. Temporal-order shuffle null

For a fixed representative low-epsilon standard record, 200 deterministic time-order permutations are generated.

The state vectors and their amplitudes are preserved; only temporal ordering is destroyed.

Observed C(q0) is compared with the shuffled null distribution.

## 12. Firewall and post-lock comparison

`closure_result.json` is written before the physical reference epsilon_c is read.

Only afterward does the runner create:

`posthoc_comparison.json`

This does not make v001 a prospective blind experiment—the dataset and physical result are already known—but it prevents the published transition value from entering the closure metric or its numerical boundary detector.

The strongest validation will therefore be an unchanged application of this now-explicit metric to an independent time-crystal dataset.
