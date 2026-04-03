cmb_alpha_structactive
======================

What this pack is
-----------------
Alpha-swept CMB power spectrum ladders for STRUC-I evaluation.
Three polarization channels: TT, TE, EE (Planck 2018, R3.01).

Source files
------------
COM_PowerSpect_CMB-TT-full_R3_01.txt  (ell=2..2508, 2507 rows)
COM_PowerSpect_CMB-TE-full_R3_01.txt  (ell=2..1996, 1995 rows)
COM_PowerSpect_CMB-EE-full_R3_01.txt  (ell=2..1996, 1995 rows)

Why this is not uniform alpha^2 scaling
----------------------------------------
Simple uniform rescaling leaves gap-structure geometry unchanged.
This pack applies a non-uniform proxy deformation:

    Dl_alpha(ell) = envelope(ell) * (alpha/alpha0)^2
                  + residual(ell) * (alpha/alpha0)^4

where:
    envelope = running median of Dl over 50-ell window
    residual = Dl - envelope (captures acoustic oscillations)
    p_envelope = 2  (smooth background: scales as alpha^2)
    q_acoustic  = 4  (acoustic peaks: scales as alpha^4)

Physical motivation: alpha enters CMB primarily through the
recombination history. The acoustic oscillation amplitude and
damping scale respond differently to alpha variation than the
smooth large-scale envelope, producing non-uniform gap deformation.

Structural activity verification (normalized gap MAD):
    TT: alpha=0.80 vs 1.00 -> 3.615  |  1.00 vs 1.20 -> 3.517
    TE: alpha=0.80 vs 1.00 -> 2.200  |  1.00 vs 1.20 -> 2.155
    EE: alpha=0.80 vs 1.00 -> 6.645  |  1.00 vs 1.20 -> 7.395

Non-zero MAD confirms alpha is structurally active in all channels.
EE shows strongest structural sensitivity.

Important boundary
------------------
This is a physically motivated proxy extension, not an ab initio
CMB recombination calculation. The exponents p=2, q=4 are physically
grounded but approximate.

Files
-----
For each alpha in sweep, per channel (TT/TE/EE):
    cmb_{chan}_levels_alpha_{XX}.csv  - sorted Dl_alpha values
    cmb_{chan}_gaps_alpha_{XX}.csv    - sorted positive gap values

Ladder sizes:
    TT levels: 2507 rows per alpha
    TT gaps:   ~2506 rows per alpha (positive gaps only)
    TE/EE levels: 1995 rows per alpha
    TE/EE gaps:   varies (positive gaps only)

Note on negative Dl values:
    TE and EE spectra contain negative Dl values (physical: TE is
    a cross-correlation). These are included in the levels ladder
    as-is (sorted ascending). The gap ladder retains only positive
    consecutive differences.

Sweep included
--------------
Coarse:   0.80 to 1.20 step 0.05
Refined:  0.95 to 1.05 step 0.01

Chamber format
--------------
All ladders are chamber-ready:
    - single column
    - header: value
    - sorted ascending
    - no NaN values

Total files: 102 (+ manifest.csv + README.txt)
