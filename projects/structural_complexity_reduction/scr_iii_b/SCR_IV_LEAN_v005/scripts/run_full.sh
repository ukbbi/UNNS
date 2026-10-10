#!/usr/bin/env bash
cd "$(dirname "$0")/.."; R=$PWD
python3 -I scripts/verify_batches.py $R g 2 > output/verify_g.log 2>&1; echo $? > output/verify_g.rc
python3 -I scripts/verify_batches.py $R n 2 > output/verify_n.log 2>&1; echo $? > output/verify_n.rc
date -u +%FT%TZ > output/full_build_end.txt
