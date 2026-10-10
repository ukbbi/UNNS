#!/usr/bin/env bash
# SCR-IV v001 test runner. Distinguishes: [0] environment, [1] data fidelity, [2] COMPILATION, [3] WITNESS VERIFICATION,
# [4] negative controls and differential test, [5] GLOBAL CERTIFICATE (PENDING). Logs go to output/. Exit 0 only if stages 0-4 pass.
set -u
cd "$(dirname "$0")"; ROOT="$PWD"; OUT="$ROOT/output"; mkdir -p "$OUT"; LOG="$OUT/RUN_TEST_LOG.txt"; : > "$LOG"
say() { echo "$@" | tee -a "$LOG"; }
fail=0
say "== SCR-IV v001 RUN_TEST $(date -u +%Y-%m-%dT%H:%M:%SZ)"
say "[0] ENVIRONMENT"
{ lean --version; lake --version; python3 --version; uname -srm; } 2>&1 | tee -a "$LOG"
EXPECT=3d47ed1256da7620292a5fe4c64e0bc226b9836768ac87df0ff4fdbf91c5f7a2
GOT=$(sha256sum data/real_4x4.txt | cut -d' ' -f1)
[ "$GOT" = "$EXPECT" ] && say "  instance sha256 OK ($GOT)" || { say "  INSTANCE HASH MISMATCH $GOT"; fail=1; }

say "[1] DATA FIDELITY (non-kernel check): regenerate Lean data from the frozen instance and compare byte-for-byte"
TMP=$(mktemp -d); mkdir -p "$TMP/data"; cp data/real_4x4.txt "$TMP/data/"
python3 scripts/gen_lean_data.py "$TMP" > /dev/null
if cmp -s "$TMP/SCR_IV_Data.lean" SCR_IV_Data.lean && cmp -s "$TMP/data/coeff_bits.csv" data/coeff_bits.csv && cmp -s "$TMP/data/instance_manifest.json" data/instance_manifest.json; then say "  generated data == committed data: OK"; else say "  DATA FILES DIFFER FROM REGENERATION"; fail=1; fi
rm -rf "$TMP"
python3 scripts/scan_source.py "$ROOT" | tee -a "$LOG"; [ "${PIPESTATUS[0]}" = 0 ] || fail=1

say "[2] COMPILATION (Lean kernel): lake build, all modules"
lake build > "$OUT/lake_build.log" 2>&1; rc=$?
grep -v '^trace' "$OUT/lake_build.log" | grep -v '^info: SCR_IV_Check' | tail -15 | tee -a "$LOG"
[ $rc = 0 ] && say "  COMPILATION: PASS" || { say "  COMPILATION: FAIL"; fail=1; }
grep -qi "sorry" "$OUT/lake_build.log" && { say "  WARNING: build log mentions sorry"; fail=1; }

say "[3] WITNESS VERIFICATION (kernel-checked theorems in SCR_IV_Witness.lean + axiom audit)"
grep "^info: SCR_IV_Check" "$OUT/lake_build.log" | sed 's/^info: SCR_IV_Check.lean:[0-9]*:[0-9]*: //' > "$OUT/axiom_audit.txt"
if [ ! -s "$OUT/axiom_audit.txt" ]; then lake env lean SCR_IV_Check.lean > "$OUT/axiom_audit.txt" 2>&1; fi
cat "$OUT/axiom_audit.txt" | tee -a "$LOG" | tail -30
n_thm=$(grep -c "SCR_IV\." "$OUT/axiom_audit.txt")
if grep -q "sorryAx\|ofReduceBool" "$OUT/axiom_audit.txt"; then say "  AXIOM AUDIT: FAIL (sorryAx or ofReduceBool)"; fail=1
elif grep -v "does not depend on any axioms" "$OUT/axiom_audit.txt" | grep -v "propext\|Classical.choice\|Quot.sound" | grep -q "depends on"; then say "  AXIOM AUDIT: FAIL (unexpected axiom)"; fail=1
else say "  AXIOM AUDIT: PASS ($n_thm theorems; only propext / Classical.choice / Quot.sound)"; fi
for th in ground_in_grammar nonG_violating_vertex ground_energy_exact nonG_energy_exact ground_matches_reported nonG_matches_reported; do
  grep -q "SCR_IV.$th'" "$OUT/axiom_audit.txt" || { say "  MISSING THEOREM $th"; fail=1; }; done
[ $fail = 0 ] && say "  WITNESS VERIFICATION: PASS"

say "[4] NEGATIVE CONTROLS (each false claim must be REJECTED by the kernel) and DIFFERENTIAL TEST (evidence, not proof)"
for f in tests/neg_*.lean; do
  if lake env lean "$f" > "$OUT/$(basename "$f" .lean).log" 2>&1; then say "  $f: ACCEPTED (BAD - false claim proved)"; fail=1; else say "  $f: rejected (good)"; fi
done
python3 scripts/diff_test.py "$ROOT" 2>&1 | tee -a "$LOG"; [ "${PIPESTATUS[0]}" = 0 ] || fail=1
rm -f tests/_Diff.lean

say "[5] GLOBAL CERTIFICATE VERIFICATION: PENDING_NOT_STARTED (IV-3 pruning theorem, IV-4 certificates, IV-5 finite gap are not implemented)"
say "== STAGE VERDICTS"
if [ $fail = 0 ]; then say "  IV-1 MODEL_FORMALIZED : PASS (scope: see CERT_STATUS.md)"; say "  IV-2 WITNESSES_CERTIFIED : PASS"; else say "  IV-1 / IV-2 : NOT ESTABLISHED (see failures above)"; fi
say "  IV-3 PRUNING_THEOREM_PROVEN : PENDING"; say "  IV-4 GLOBAL_OPTIMA_CERTIFIED : PENDING"; say "  IV-5 FINITE_GAP_CERTIFIED : PENDING"
exit $fail
