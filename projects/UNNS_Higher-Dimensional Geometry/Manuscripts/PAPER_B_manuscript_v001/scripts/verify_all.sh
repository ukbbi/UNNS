#!/bin/bash
# Acceptance gate: re-runs every finite computation of Paper B; exits non-zero on ANY failure.
set -euo pipefail
cd "$(dirname "$0")"
for s in classify crosscheck verify6 small_p lit_checks; do
  t0=$(date +%s); python3 $s.py > ../logs/$s.out 2>&1
  echo "$s done in $(( $(date +%s)-t0 ))s"; tail -2 ../logs/$s.out
done
echo "== source certificate checkers (exit status enforced)"
python3 ../src/certificates/checker11.py ../src/certificates/C9_partition.json
python3 ../src/certificates/checker10.py ../src/certificates/C6_rank6.json
if [[ -f ../src/certificates/checker8.py ]]; then
  python3 ../src/certificates/checker8.py ../src/certificates/C5_rank5.json
  echo "rank-5 certificate: checked"
else
  echo "SKIPPED: rank-5 certificate; checker8 not bundled."
fi
echo "ALL EXECUTED CHECKS PASSED"
