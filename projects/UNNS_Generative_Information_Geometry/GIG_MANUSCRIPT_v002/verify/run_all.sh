#!/bin/sh
# Runs every verification script (Python 3, standard library only) and the stand-alone certificate checker.
set -e
cd "$(dirname "$0")"
for f in run_checks.py run_checks2.py run_checks3.py run_checks4.py run_checks5.py; do python3 "$f" > "last_$f.txt"; echo "$f: done"; done
python3 inherited/standalone_verify.py --cert inherited/positives_cycle_cocycle.json | tee last_standalone.txt | tail -3
