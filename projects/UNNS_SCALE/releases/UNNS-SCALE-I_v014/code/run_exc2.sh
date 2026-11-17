#!/bin/bash
# v014: further chain-scale distances for the exceptional n.  Scale 18 at radius 4 only for the 640 pairs with tau^4 = 8 (they are the ones whose bound 18 could still improve); 361/7600/160000 (R=3) for all 8655.
cd "$(dirname "$0")/.."
f=results/exc/EXC_A18_R4_on_eq8.txt; [ -s $f ] || { NLIST=results/EXC_A4_eq8.txt /tmp/scale_lift_v2 18 1000000 1 1000000 $f.tmp 4 2 && mv $f.tmp $f; }
for spec in "361 3" "7600 3" "160000 3"; do set -- $spec; f=results/exc/EXC_A$1_R$2.txt; [ -s $f ] && continue
  NLIST=results/EXC_A4_gt6.txt /tmp/scale_lift_v2 $1 1000000 1 1000000 $f.tmp $2 2 && mv $f.tmp $f; done; echo done > results/exc/DONE
