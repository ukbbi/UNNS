nuclei_alpha_structactive
=========================

What this pack is
-----------------
Alpha-swept nuclear level ladders for STRUC-I evaluation.
15 isotopes spanning light sd-shell to heavy actinide nuclei.
Built from ENSDF (Evaluated Nuclear Structure Data File) raw data.

Source files
------------
ensdf_24Mg.txt, ensdf_28Si.txt, ensdf_48Ca.txt, ensdf_56Fe.txt,
ensdf_60Ni.txt, ensdf_90Zr.txt, ensdf_100Mo.txt, ensdf_116Sn.txt,
ensdf_120Sn.txt, ensdf_150Nd.txt, ensdf_152Sm.txt, ensdf_166Er.txt,
ensdf_174Yb.txt, ensdf_208Pb.txt, ensdf_238U.txt

Isotopes and nuclear structure context
---------------------------------------
24Mg   Z=12  vibrational (sd-shell)
28Si   Z=14  oblate-deformed (sd-shell)
48Ca   Z=20  doubly-magic spherical
56Fe   Z=26  collective (stability peak)
60Ni   Z=28  vibrational (Z=28 magic)
90Zr   Z=40  spherical (N=50 magic)
100Mo  Z=42  transitional
116Sn  Z=50  magic-Z spherical (tin)
120Sn  Z=50  magic-Z spherical (tin)
150Nd  Z=60  transitional → deformed (N=90)
152Sm  Z=62  strongly deformed (N=90 onset)
166Er  Z=68  rotational (rare-earth)
174Yb  Z=70  rotational (rare-earth)
208Pb  Z=82  doubly-magic spherical
238U   Z=92  actinide rotational

Why this is not uniform alpha^2 scaling
-----------------------------------------
Simple uniform rescaling leaves gap-structure geometry unchanged.
This pack applies a spin-weighted proxy deformation:

    E_alpha(i) = centroid(i) + delta_fs(i) * alpha^q(J_i)

Where:
    centroid(i) = running median of nearby levels (window=20)
    delta_fs(i) = E(i) - centroid(i)  [fine-structure offset]
    q(J)        = 2 + (J / J_max) * 2  [spin-weighted exponent]
                  ranges from 2.0 (J=0) to 4.0 (J=J_max)
    J from ENSDF Jp field; unknown J → q=2.0 (conservative)

Physical motivation: electromagnetic corrections to nuclear level
energies (fine-structure splittings, Coulomb shifts) scale with α
and are larger for high-spin states. The spin-weighted exponent
captures this differential sensitivity: J=0 states deform as α²
(pure EM scaling), high-J states deform as up to α⁴.

Structural activity verification (normalized gap MAD, α=0.80 vs 1.00):
    152Sm:  4.70  (strongly deformed — highest sensitivity)
    208Pb:  1.78
    48Ca:   1.37
    116Sn:  1.34
    120Sn:  1.69
    24Mg:   0.71
    150Nd:  0.18
    166Er:  0.16

All nuclei show non-zero MAD → α is structurally active in all cases.

Important boundary
------------------
This is a physically motivated proxy extension, not an ab initio
nuclear structure calculation. The spin-weighted exponent q(J) is
physically grounded but approximate. Spin values are parsed directly
from ENSDF Jp fields; coverage varies (37-92% per nucleus).

Files
-----
For each nucleus and each alpha in sweep:
    nucleus_{NUC}_levels_alpha_{XX}.csv  — sorted level energies (keV)
    nucleus_{NUC}_gaps_alpha_{XX}.csv    — sorted positive gap values (keV)

Sweep
-----
Coarse:   0.80 to 1.20 step 0.05
Refined:  0.95 to 1.05 step 0.01
Total:    17 alpha values per nucleus per ladder type

Chamber format
--------------
All files chamber-ready:
    - single column, header: value
    - sorted ascending
    - no NaN, all gaps positive

Total files: 510 (+ manifest.csv + README.txt)
