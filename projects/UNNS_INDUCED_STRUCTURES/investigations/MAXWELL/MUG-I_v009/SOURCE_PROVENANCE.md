# MUG-I v009 — Source/provenance

Latest validated reference (read-only): `MUG-I_v008.zip`, SHA-256 `94f5ea447a672f707ea2b1e747026fb89fa3b6b24d424133c35010c65d2640c0`.

Earlier induction ambiguity source (read-only): `MUG-I_v007.zip`, SHA-256 `7d0de5b1065bf1f0e9bdf976fcb9a7058486c6a25a18644acd1a06344744a2b8`.

UNNS grammar fixed: `T_N(x)=x(N+1)^2/N`, `N|x`, positive integer N. v009 does not change the original nesting law, does not redefine the frozen FUG-I baseline, and does not modify any GitHub repository.

The electromagnetic dynamical system is **newly specified here** (external time-dependent dielectric on a periodic 1D transverse Maxwell reduction), and numerical propagation uses a separately written Fourier/RK4 implementation and a Yee FDTD implementation. This model is a fresh test, not content silently inherited from v008.

A preliminary pilot at η=.012, stage duration 2.0 was run before the separate held-out protocol lock. Then `protocol/PREDICTIONS_LOCK.json` was written and SHA-256 recorded as `45c50e6d78c6b907b8c8cceab42e989f391198ecacdb88dbbb89e3a55f55d39f`. Only then were held-out η=.009, stage duration 1.7 cases computed. Lock checks are reproducible, but the lock is not externally timestamped and this is not a blinded physical experiment.

The modulation harmonics were explicitly engineered to illustrate both UNNS-compatible and non-UNNS mode conversions. Experimental independence and novelty relative to Maxwell-only physics are not claimed.
