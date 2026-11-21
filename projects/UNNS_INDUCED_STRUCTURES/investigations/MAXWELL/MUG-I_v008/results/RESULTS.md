# v008 research results — exact rule comparison and Maxwell controls

## Same source and two equal-endpoint histories

Initial Fourier content: `d=6`, eigenstate Bloch class `kappa=0` of medium `q=6`. Both words have total multiplier 288.

| Rule | A: (3,8,3) | B: (1,1,1,2) | Meaning |
|---|---|---|---|
| Strict whole-field Fourier support | 6→32→324→1728; survives | 6→24→96→384→1728; survives | Same final *field*, not fixed-medium eigenstate |
| Componentwise Fourier filter | Survives in full | Survives in full | Here no component needs filtering; distinct from strict rule on general fields |
| v007 Bloch projector E | Blocked at N=8 | Survives | Extra `N|q` veto produces difference |
| Strict exact fixed-medium eigenstate | First step disallowed | First step disallowed | No nontrivial dilation preserves a fixed nonuniform medium eigenmode |
| Co-dilating medium | All steps on-shell in changing media | All steps on-shell in changing media | Same final field and final medium |

The finite exact-support witness has 6 nonzero occupied harmonics. It tests the algebraic operators independently of floating-point spectral computations; the **same** numerical Maxwell eigenmode is separately run through all three operators in `spectral_same_state.py`.

## Numerical Maxwell control (q=6, delta=0.1)

- Lower `|m|=6` eigenstate in `kappa=0`: `omega²≈35.880874957879314`; dominant absolute-harmonic weight ≈ `0.9923143303`.
- Fixed-medium best-fit stationary residual under `r=4`: ≈ `0.1707773680` relative to the transformed `−E''` norm.
- Exact co-dilating medium control under the same r: Galerkin relative residual ≈ `8.5e−14`.
- Vacuum plane-wave control: residual 0 within the numerical diagnostic.

All are descriptive numerical confirmations of the stronger analytic fixed-medium no-go and co-dilation theorems.

## Conclusions

The v007 history survival differences are valid for its **declared** projection rule. They cannot be described as an unavoidable physical Maxwell blockade of an original T_N history. Equally, a strict *on-shell* relation on exact eigenstates of this fixed medium has no nontrivial forward T_N edges. Neither result currently constitutes UNNS-specific physical predictive power. The next experiment must supply an independently justified electromagnetic process if nontrivial field transport is intended.

## Additional five numerical Maxwell controls

The independently reconstructed eigenstates use additional `(q, delta, N)` combinations (see `spectral_controls.csv`):

| q | δ | N | Fixed-medium stationary residual | Co-dilating medium residual |
|---:|---:|---:|---:|---:|
| 4 | 0.08 | 1 | 0.13731 | 3.14e-13 |
| 6 | 0.10 | 2 | 0.17078 | 8.52e-14 |
| 8 | 0.14 | 1 | 0.23595 | 2.86e-14 |
| 12 | 0.06 | 3 | 0.10339 | 1.56e-14 |
| 7 | 0.12 | 1 | 0.20369 | 5.47e-14 |

These are independent numerical checks of an **already proved** analytic obstruction, not independent physical observations.
