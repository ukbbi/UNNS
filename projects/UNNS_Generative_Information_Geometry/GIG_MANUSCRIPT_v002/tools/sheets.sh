#!/bin/sh
cd "$(dirname "$0")/.." && rm -rf pages && mkdir pages && pdftoppm -r 70 -png main.pdf pages/p && cd pages
n=$(ls p-*.png | wc -l); s=0; a=1
while [ $a -le $n ]; do files=""; for i in $(seq $a $((a+5))); do f=$(printf "p-%02d.png" $i); [ -f $f ] && files="$files $f"; done; montage $files -tile 3x2 -geometry +4+4 -background gray sheet$s.png; s=$((s+1)); a=$((a+6)); done
