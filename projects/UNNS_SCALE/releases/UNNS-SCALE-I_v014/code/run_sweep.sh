#!/bin/bash
# usage: run_sweep.sh A M R outdir  (chunks of 50000 n over 1..999999)
A=$1; M=$2; R=$3; D=$4; mkdir -p $D
for lo in $(seq 1 50000 999999); do hi=$((lo+50000)); [ $hi -gt 1000000 ] && hi=1000000
  f=$D/A${A}_$(printf %07d $lo)_$(printf %07d $hi).txt; [ -s $f ] && continue
  /tmp/scale_lift $A $M $lo $hi $f.tmp $R 2 && mv $f.tmp $f; done
echo done > $D/DONE
