# FIELD-I v006 — Results

**New prover/verifier:** `field6.py`, exact standard-library Python. `output/field6_output.txt` is a reproduced execution, not a substituted report.

## New proved consequences

1. **L1 plateau escape:** For a realised x with G>1, if the fibre does not grow then the hypothetical progression y_k=Gx+kL² must enter the forbidden G=1 state in <=4G steps if L is odd, and <=G steps if L is even. An exact modular inverse gives a tighter seed-specific k. The actual orbit must therefore grow its fibre within k steps, possibly without reducing G.
2. **L2 finite collapse regimes:** From `G=2`, collapse to 1 in <=7 steps; from `G=3`, <=2 steps; from `G=6`, <=29 steps. These are universal conditional-orbit theorems, **not** extrapolations from samples.
3. **L3 normal form:** After entry into G=1 and absorption into the 1→2→3→1 t-cycle, `x_(n+3)=4x_n`, gamma cycles 1,2,3 (up to phase) and `R_(n+3)-R_n=tau(odd(s))`.
4. **L4 reach counting:** In the G=1 branch, exactly `U(X)=sum_{q|o,q<=X}(floor(log2(X/q))+1)-1`, hence `U(X)=tau(o) log2(X)+O(1)` and natural density zero.
5. **L5 v005 T33 erratum:** Its general non-universality claim is sound; `O(log X)` / zero density are **proved only for G=1 branches**. Hypothetical G∞>1 yields only an upper density ≤1/G∞ from the current argument.

## What has NOT been proved

General collapse `G→1` from **every** realised x is open. A run of examples, even if all collapse, cannot certify this. Repeated fibre growth without G reduction is the unresolved phenomenon. There is no new unique interaction-selection rule or physical conclusion.

## Next testable task

Investigate persistent G≥4 regimes via modular growth-event constraints, searching for either (i) a general descent invariant, or (ii) an exact infinite counterexample orbit. Avoid enlarging numerical sweeps without a discriminatory modular invariant.
