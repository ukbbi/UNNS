# ESC-I v0.1 report

Echo horizon N=2000, tolerance=1e-09. Exact side: rational arithmetic, no floating point.

| id | exact class | naive eigenvalue test | echo class | verdict | rho | hold eps (generic / area / state) |
|---|---|---|---|---|---|---|
| rot90 | periodic - root of unity, order 4 | marginal (inconclusive) | periodic | agree | 1 | 0 (knife-edge) / 0 (knife-edge) / >=0.1 (whole grid) |
| rot60 | periodic - root of unity, order 6 | marginal (inconclusive) | periodic | agree | 1 | 0 (knife-edge) / 0 (knife-edge) / >=0.1 (whole grid) |
| rot_pyth | bounded - quasi-periodic (theta/2pi irrational, Niven) | marginal (inconclusive) | bounded | agree | 1 | 0 (knife-edge) / >=0.1 (whole grid) / >=0.1 (whole grid) |
| spiral_in | convergent - to origin | convergent | convergent | agree | 0.9 | >=0.1 (whole grid) / >=0.1 (whole grid) / >=0.1 (whole grid) |
| spiral_out | divergent - geometric (spiral) | divergent | divergent | agree | 1.1 | 0.01 / >=0.1 (whole grid) / >=0.1 (whole grid) |
| shear_gen | divergent - linear (Jordan block, lambda=1) | marginal (inconclusive) | divergent | agree | 1 | 0 (knife-edge) / 0 (knife-edge) / >=0.1 (whole grid) |
| shear_eig | periodic - fixed point | marginal (inconclusive) | periodic | agree | 1 | 0 (knife-edge) / 0 (knife-edge) / 0 (knife-edge) |
| saddle_stable | convergent - to origin along eigenvector | divergent | convergent | agree | 2 | 0 (knife-edge) / 0 (knife-edge) / 0 (knife-edge) |
| saddle_gen | divergent - geometric (dominant real eigenvalue) | divergent | divergent | agree | 2 | >=0.1 (whole grid) / >=0.1 (whole grid) / >=0.1 (whole grid) |
| T_ones | divergent - geometric (dominant real eigenvalue) | divergent | divergent | agree | 2 | >=0.1 (whole grid) / >=0.1 (whole grid) / >=0.1 (whole grid) |
| UT_ones | convergent - finite-time collapse (A nilpotent) | convergent | convergent | agree | 0 | >=0.1 (whole grid) / >=0.1 (whole grid) / >=0.1 (whole grid) |
| proj_fixed | convergent - to a nonzero fixed point | marginal (inconclusive) | convergent | agree | 1 | 0 (knife-edge) / 0 (knife-edge) / >=0.1 (whole grid) |
| jordan_m1 | divergent - linear (Jordan block, lambda=-1) | marginal (inconclusive) | divergent | agree | 1 | 0 (knife-edge) / 0 (knife-edge) / >=0.1 (whole grid) |
| trap_horizon | divergent - geometric (spiral) | divergent | bounded | echo-misses | 1 | 1e-08 / >=0.1 (whole grid) / >=0.1 (whole grid) |
| trap_resolution | bounded - quasi-periodic (theta/2pi irrational, Niven) | marginal (inconclusive) | periodic | echo-overclaims | 1 | 0 (knife-edge) / >=0.1 (whole grid) / >=0.1 (whole grid) |

## Notes per example

- **rot90** (baseline): Baseline: J with J^2=-I. Exactly periodic (order 4). Why: tau in {0,+-1}: A^n = I (cyclotomic).
- **rot60** (baseline): tau=1: A^6=I. Periodic, but orbit is an ellipse, not a circle. Why: tau in {0,+-1}: A^n = I (cyclotomic).
- **rot_pyth** (baseline): A genuine rotation, yet never periodic: tau=6/5 not in {0,+-1,+-2}. Why: |lambda|=1, tau not in {0,+-1,+-2}: never returns exactly.
- **spiral_in** (baseline): Complex pair, |lambda|=0.9. Why: rho < 1.
- **spiral_out** (baseline): Complex pair, |lambda|=1.1. Why: rho > 1 and x0 not an eigenvector.
- **shear_gen** (designed to contradict): Expectation 'rho=1 => bounded' is false: Jordan block gives linear growth. Why: defective at +1.
- **shear_eig** (designed to contradict): Same matrix, different x0: fixed point. Class depends on the state, not only on A. Why: x0 is an eigenvector, eigenvalue 1.
- **saddle_stable** (designed to contradict): rho=2 yet the orbit converges: the eigenvalue test alone says 'divergent'. Why: x0 is an eigenvector, eigenvalue 1/2.
- **saddle_gen** (baseline): Same matrix as above; generic state diverges. Why: rho > 1 and x0 not an eigenvector.
- **T_ones** (baseline): rho(T)=2, divergent. Why: rho > 1 and x0 not an eigenvector.
- **UT_ones** (designed to contradict): Audit S5 counterexample: rho(UT)=0, so UT is nilpotent. Phase inletting does not preserve rho. Why: rho < 1.
- **proj_fixed** (designed to contradict): rho=1 (marginal) but convergent to (1,0): an attractor that is not the origin. Why: eigenvalues 1 and |mu|<1.
- **jordan_m1** (baseline): Linear growth with alternating sign. Why: defective at -1.
- **trap_horizon** (designed to contradict): Exactly divergent, but growth over 2000 steps is e^(2e-4): the echo reads 'bounded'. Why: rho > 1 and x0 not an eigenvector. Echo vs exact: horizon: drift is below resolution within N=2000; ~138155113 steps needed.
- **trap_resolution** (designed to contradict): Exactly quasi-periodic (bounded), but within tol=1e-9 it looks period-6. Why: |lambda|=1, tau not in {0,+-1,+-2}: never returns exactly. Echo vs exact: resolution: orbit returns within tol although exact orbit never returns.

## Tally

- examples: 15; echo agrees with exact: 13
- naive eigenvalue-only test differs from exact class: 9
- every echo/exact disagreement explained by horizon or resolution: True

## Phase-inletting counterexample (audit S5)

T=[[1,1],[1,1]], U=diag(1,-1): rho(T)=2, rho(UT)=0, rho(UTU^-1)=2, commute=False. rho(UT)=rho(T) is false in general; similarity preserves rho, multiplication does not.
