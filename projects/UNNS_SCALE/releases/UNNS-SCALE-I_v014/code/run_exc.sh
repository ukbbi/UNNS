#!/bin/bash
# exact distances at chain scales for the exceptional n (list mode): A=4 R=4 first, then 1, 18 (R=4), then 361, 7600, 160000 (R=3)
cd "$(dirname "$0")/.."; L=results/EXC_A4_gt6.txt
for spec in "4 4" "1 4" "18 4" "361 3" "7600 3" "160000 3"; do set -- $spec; f=results/exc/EXC_A$1_R$2.txt; [ -s $f ] && continue
  NLIST=$L /tmp/scale_lift_v2 $1 1000000 1 1000000 $f.tmp $2 2 && mv $f.tmp $f; done; echo done > results/exc/DONE
