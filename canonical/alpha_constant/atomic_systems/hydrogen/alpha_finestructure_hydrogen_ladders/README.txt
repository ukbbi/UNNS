Alpha fine-structure sweep pack for STRUC-I
==========================================

Purpose:
  Chamber-ready ladders where alpha changes more than overall scale.

Model:
  Approximate hydrogen fine-structure energies (distinct n,j values):
  E_(n,j) ≈ -1/2 α^2/n^2 - 1/2 α^4/n^4 * ( n/(j+1/2) - 3/4 )
  with n = 1..20 and j = 1/2, 3/2, ..., n-1/2.

Encodings included:
  1) levels      -> sort(|E_(n,j)|)
  2) transitions -> first 1000 sorted unique |E_i - E_j|

Sweeps:
  coarse  : alpha_scale = 0.80..1.20 step 0.01
  refined : alpha_scale = 0.95..1.05 step 0.002

alpha_0 = 7.297352569283801528e-03

Suggested first run:
  Compare 0.800, 0.900, 1.000, 1.100, 1.200 for BOTH encodings.
  Track mean_rho, max_rho, regime, and state.
