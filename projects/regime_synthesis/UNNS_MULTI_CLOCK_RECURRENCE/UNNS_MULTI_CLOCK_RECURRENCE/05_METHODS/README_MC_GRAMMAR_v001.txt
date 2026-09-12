MC_GRAMMAR_v001 — FROZEN

This package completes the `freeze` stage.

Frozen temporal grammar:
  D_2clk -> [P_src ; J_frac | M_frac]

Separate physical extension:
  + C_coll

Frozen gates:
  P_src phase-label null p_upper <= 0.10
  M_frac >= 0.12
  M_frac Fourier-phase null p_upper <= 0.10
  M_frac raw gate must survive all six frozen robustness transforms

J_frac is mandatory output, not a gate.

Current empirical ratio support:
  golden-ratio branch only

Next stage:
  prospective unseen candidate/control

C003 remains prohibited until after prospective reveal.
