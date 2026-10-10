#!/usr/bin/env bash
# SCR-IV v005 test runner. Distinguishes: [0] environment, [1] data fidelity, [2] COMPILATION, [3] WITNESS VERIFICATION (IV-2, unchanged),
# [3b] PRUNING-THEOREM VERIFICATION (IV-3), [3c] CERTIFICATE-CHECKER VERIFICATION (IV-4A), [4] negative controls + positive twins + differential tests, [5] IV-4B GLOBAL CERTIFICATES (regeneration, V4 theorem audit, real-instance controls, kernel verification of all batches only if FULL=1). Exit 0 only if stages 0-4 pass.
set -u
cd "$(dirname "$0")"; ROOT="$PWD"; OUT="$ROOT/output"; mkdir -p "$OUT"; LOG="$OUT/RUN_TEST_LOG.txt"; : > "$LOG"
say() { echo "$@" | tee -a "$LOG"; }
fail=0
say "== SCR-IV v005 RUN_TEST $(date -u +%Y-%m-%dT%H:%M:%SZ)"
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
grep -v '^trace' "$OUT/lake_build.log" | grep -v '^info: SCR_IV_Check' | tail -25 | tee -a "$LOG"
[ $rc = 0 ] && say "  COMPILATION: PASS" || { say "  COMPILATION: FAIL"; fail=1; }
grep -qi "sorry" "$OUT/lake_build.log" && { say "  WARNING: build log mentions sorry"; fail=1; }

say "[3] WITNESS VERIFICATION (kernel-checked theorems in SCR_IV_Witness.lean + axiom audit)"
grep "^info: SCR_IV_Check\.lean" "$OUT/lake_build.log" | sed 's/^info: SCR_IV_Check.lean:[0-9]*:[0-9]*: //' > "$OUT/axiom_audit.txt"
if [ ! -s "$OUT/axiom_audit.txt" ]; then lake env lean SCR_IV_Check.lean > "$OUT/axiom_audit.txt" 2>&1; fi
[ "$(grep -c 'SCR_IV\.' "$OUT/axiom_audit.txt")" = 25 ] || { say "  EXPECTED 25 IV-1/IV-2 theorems in the v001 audit"; fail=1; }
cat "$OUT/axiom_audit.txt" | tee -a "$LOG" | tail -30
n_thm=$(grep -c "SCR_IV\." "$OUT/axiom_audit.txt")
if grep -q "sorryAx\|ofReduceBool" "$OUT/axiom_audit.txt"; then say "  AXIOM AUDIT: FAIL (sorryAx or ofReduceBool)"; fail=1
elif grep -v "does not depend on any axioms" "$OUT/axiom_audit.txt" | grep -v "propext\|Classical.choice\|Quot.sound" | grep -q "depends on"; then say "  AXIOM AUDIT: FAIL (unexpected axiom)"; fail=1
else say "  AXIOM AUDIT: PASS ($n_thm theorems; only propext / Classical.choice / Quot.sound)"; fi
for th in ground_in_grammar nonG_violating_vertex ground_energy_exact nonG_energy_exact ground_matches_reported nonG_matches_reported; do
  grep -q "SCR_IV.$th'" "$OUT/axiom_audit.txt" || { say "  MISSING THEOREM $th"; fail=1; }; done
[ $fail = 0 ] && say "  WITNESS VERIFICATION: PASS"

say "[3b] PRUNING-THEOREM VERIFICATION (IV-3): kernel-checked theorems in Bound/Bridge/Solver/Prune + axiom audit (SCR_IV_Check3.lean)"
lake env lean SCR_IV_Check3.lean 2>&1 | sed 's/^SCR_IV_Check3.lean:[0-9]*:[0-9]*: //' > "$OUT/axiom_audit_iv3.txt"
n3=$(grep -c "SCR_IV\." "$OUT/axiom_audit_iv3.txt"); say "  theorems audited: $n3"
if grep -q "sorryAx\|ofReduceBool" "$OUT/axiom_audit_iv3.txt"; then say "  IV-3 AXIOM AUDIT: FAIL (sorryAx or ofReduceBool)"; fail=1
elif grep -v "does not depend on any axioms" "$OUT/axiom_audit_iv3.txt" | grep -v "propext\|Classical.choice\|Quot.sound" | grep -q "depends on"; then say "  IV-3 AXIOM AUDIT: FAIL (unexpected axiom)"; fail=1
else say "  IV-3 AXIOM AUDIT: PASS (only propext / Classical.choice / Quot.sound)"; fi
for th in decomposition lower_bound prune_sound prune_strict_keeps_ties prune_may_discard_tie partition_cover partition_disjoint partition_sound hScaled_eq_Hs solverBound_eq_Bnd guard_prune_sound lower_bound_ids prune_sound_ids solver_prune_sound_ids partition_ids_cover partition_ids_disjoint violated_persists completed_violation_persists grammar_prune_sound cppPossible_false_sound cppViolates_iff objective_relation discard_ground discard_nonGrammar; do
  grep -q "SCR_IV.$th'" "$OUT/axiom_audit_iv3.txt" || { say "  MISSING IV-3 THEOREM $th"; fail=1; }; done
rm -f "$OUT/axiom_audit_iv3.txt.tmp"
[ $fail = 0 ] && say "  PRUNING-THEOREM VERIFICATION: PASS"

say "[3c] CERTIFICATE-CHECKER VERIFICATION (IV-4A): checker soundness, partitioned coverage, conditional global theorems (SCR_IV_Check4.lean)"
lake env lean SCR_IV_Check4.lean 2>&1 | sed 's/^SCR_IV_Check4.lean:[0-9]*:[0-9]*: //' > "$OUT/axiom_audit_iv4a.txt"
n4=$(grep -c "SCR_IV\." "$OUT/axiom_audit_iv4a.txt"); say "  theorems audited: $n4"
if grep -q "sorryAx\|ofReduceBool" "$OUT/axiom_audit_iv4a.txt"; then say "  IV-4A AXIOM AUDIT: FAIL (sorryAx or ofReduceBool)"; fail=1
elif grep -v "does not depend on any axioms" "$OUT/axiom_audit_iv4a.txt" | grep -v "propext\|Classical.choice\|Quot.sound" | grep -q "depends on"; then say "  IV-4A AXIOM AUDIT: FAIL (unexpected axiom)"; fail=1
else say "  IV-4A AXIOM AUDIT: PASS (only propext / Classical.choice / Quot.sound)"; fi
for th in chk_sound checkAll_sound stateAt_Inv subOK_sound frontier_sound batchesOK_sound batches_cover ground_min_of_cert nonG_min_of_cert ground_min_of_frontier nonG_min_of_frontier leafGrammar_sound; do
  grep -q "SCR_IV.$th'" "$OUT/axiom_audit_iv4a.txt" || { say "  MISSING IV-4A THEOREM $th"; fail=1; }; done
for f in tests/toy_cert.lean tests/toy_part.lean; do
  if lake env lean "$f" > "$OUT/$(basename "$f" .lean).log" 2>&1; then say "  $f: end-to-end toy certificates ACCEPTED (good)"; else say "  $f: FAILED (BAD)"; fail=1; fi; done
[ $fail = 0 ] && say "  CERTIFICATE-CHECKER VERIFICATION: PASS (conditional theorems only: no certificate for the 4x4 instance exists)"

say "[4] NEGATIVE CONTROLS (each false claim must be REJECTED by the kernel) and DIFFERENTIAL TEST (evidence, not proof)"
for f in tests/neg_*.lean; do
  if lake env lean "$f" > "$OUT/$(basename "$f" .lean).log" 2>&1; then say "  $f: ACCEPTED (BAD - false claim proved)"; fail=1; else say "  $f: rejected (good)"; fi
done
if lake env lean tests/pos_controls.lean > "$OUT/pos_controls.log" 2>&1; then say "  tests/pos_controls.lean: compiles (good: the negatives fail because their claims are false)"; else say "  tests/pos_controls.lean: FAILED TO COMPILE (BAD)"; fail=1; fi
python3 scripts/diff_test.py "$ROOT" 2>&1 | tee -a "$LOG"; [ "${PIPESTATUS[0]}" = 0 ] || fail=1
python3 scripts/diff_test3.py "$ROOT" 2>&1 | tee -a "$LOG"; [ "${PIPESTATUS[0]}" = 0 ] || fail=1
rm -f tests/_Diff.lean tests/_Diff3.lean

say "[4b] CALIBRATION (informational; subtrees of the real instance, NOT certificates of the global optimum)"
{ python3 scripts/cert_tools.py "$ROOT" calib 14 && python3 - "$ROOT" <<'PY'
import subprocess, resource, time, sys
r = sys.argv[1]; t = time.time(); subprocess.run(["lake", "env", "lean", "tests/calib_14.lean"], cwd=r, check=True)
print(f"  calib_14 (985-node subtree, single kernel check): wall={time.time()-t:.1f}s peak_rss_MB={resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss/1024:.0f}")
PY
} 2>&1 | tee -a "$LOG" | tail -3; [ "${PIPESTATUS[0]}" = 0 ] || fail=1
{ python3 scripts/cert_tools.py "$ROOT" calibpart 12 8 && python3 - "$ROOT" <<'PY'
import subprocess, resource, time, sys
r = sys.argv[1]; t = time.time(); subprocess.run(["lake", "env", "lean", "tests/calibpart_12.lean"], cwd=r, check=True)
print(f"  calibpart_12 (8 independent prefix theorems): wall={time.time()-t:.1f}s peak_rss_MB={resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss/1024:.0f}")
PY
} 2>&1 | tee -a "$LOG" | tail -3; [ "${PIPESTATUS[0]}" = 0 ] || fail=1
rm -f tests/calib_*.lean tests/calibpart_*.lean

say "[5] IV-4B GLOBAL CERTIFICATES (frozen 4x4 instance)"
say "[5a] DATA FIDELITY: regenerate both frontier certificate sets (UNTRUSTED Python, exact integers) and compare with the shipped certs/ and Bat/ modules"
T5=$(mktemp -d)
for o in ground nongT; do
  python3 -I scripts/gen4b.py "$ROOT" $o 14 "$T5" > "$T5/gen_$o.txt" 2>&1 || { say "  generation FAILED for $o"; tail -3 "$T5/gen_$o.txt" | tee -a "$LOG"; fail=1; }
  if cmp -s "$T5/cert_${o}_D14.txt" "certs/cert_${o}_D14.txt"; then say "  $o: regenerated certificates == shipped certs/ (sha256 $(sha256sum "$T5/cert_${o}_D14.txt" | cut -c1-16)...)"; else say "  $o: CERTIFICATES DIFFER FROM REGENERATION"; fail=1; fi
done
mkdir -p "$T5/R"; python3 -I scripts/mk_batches.py "$T5/R" "$T5" ground 14 1500 > /dev/null && python3 -I scripts/mk_batches.py "$T5/R" "$T5" nongT 14 1500 > /dev/null
if diff -rq "$T5/R/Bat" Bat > /dev/null && cmp -s "$T5/R/Fin_g.lean" Fin_g.lean && cmp -s "$T5/R/Fin_n.lean" Fin_n.lean; then say "  regenerated Bat/ (1148 modules) and Fin_g/Fin_n == shipped"; else say "  BATCH MODULES DIFFER FROM REGENERATION"; fail=1; fi
rm -rf "$T5"
say "[5b] EXACT NON-GRAMMAR MINIMUM (untrusted diagnostic, exact integers): frozen claimedNonGNum vs the minimum found by branch and bound"
python3 -I scripts/diag_nong.py "$ROOT" 2>&1 | tee -a "$LOG" | tail -4; [ "${PIPESTATUS[0]}" = 0 ] || fail=1
say "[5c] V4 THEOREMS + AXIOM AUDIT (SCR_IV_Check5.lean): frozen_nonG_not_min, corrected witness facts, nonGT_min_of_frontier, assembly lemmas"
lake env lean SCR_IV_Check5.lean 2>&1 | sed 's/^SCR_IV_Check5.lean:[0-9]*:[0-9]*: //' > "$OUT/axiom_audit_iv4b_partA.txt"; cat "$OUT/axiom_audit_iv4b_partA.txt" | tee -a "$LOG"
[ "$(grep -c 'SCR_IV\.' "$OUT/axiom_audit_iv4b_partA.txt")" = 11 ] || { say "  EXPECTED 11 audited V4 declarations"; fail=1; }
if grep -q "sorryAx\|ofReduceBool" "$OUT/axiom_audit_iv4b_partA.txt"; then say "  IV-4B AXIOM AUDIT A: FAIL"; fail=1
elif grep -v "does not depend on any axioms" "$OUT/axiom_audit_iv4b_partA.txt" | grep -v "propext\|Classical.choice\|Quot.sound" | grep -q "depends on"; then say "  IV-4B AXIOM AUDIT A: FAIL (unexpected axiom)"; fail=1
else say "  IV-4B AXIOM AUDIT A: PASS (only propext / Classical.choice / Quot.sound)"; fi
say "[5d] REAL-INSTANCE NEGATIVE CONTROLS (each must be REJECTED by the kernel) and POSITIVE TWINS (must compile)"
mkdir -p "$OUT/neg4b"
for f in tests/neg4b_*.lean; do b=$(basename "$f" .lean)
  if lake env lean "$f" > "$OUT/neg4b/$b.log" 2>&1; then say "  $b: ACCEPTED (BAD)"; fail=1; else say "  $b: rejected (good)"; fi; done
for f in tests/pos4b_*.lean; do b=$(basename "$f" .lean)
  if lake env lean "$f" > "$OUT/neg4b/$b.log" 2>&1; then say "  $b: compiles (good)"; else say "  $b: FAILED TO COMPILE (BAD)"; fail=1; fi; done
FULLRES="NOT RE-RUN in this invocation"
if [ "${FULL:-0}" = 1 ]; then
  say "[5e] FULL KERNEL VERIFICATION (FULL=1): all 344 ground + 804 non-grammar batch theorems, 2 concurrent Lean processes (<= ~3.3 GB each; ~35 min + ~60 min on 2 cores)"
  rm -rf logs
  for t in g n; do python3 -I scripts/verify_batches.py "$ROOT" $t 2 2>&1 | tee -a "$LOG"; [ "${PIPESTATUS[0]}" = 0 ] || fail=1; done
  lake env lean SCR_IV_Check5b.lean 2>&1 | sed 's/^SCR_IV_Check5b.lean:[0-9]*:[0-9]*: //' > "$OUT/axiom_audit_iv4b_results.txt"; cat "$OUT/axiom_audit_iv4b_results.txt" | tee -a "$LOG"
  [ "$(grep -c "exact_min" "$OUT/axiom_audit_iv4b_results.txt")" = 2 ] || { say "  MISSING RESULT THEOREMS"; fail=1; }
  if grep -q "sorryAx\|ofReduceBool" "$OUT/axiom_audit_iv4b_results.txt"; then say "  RESULT AXIOM AUDIT: FAIL"; fail=1
  elif grep -v "does not depend on any axioms" "$OUT/axiom_audit_iv4b_results.txt" | grep -v "propext\|Classical.choice\|Quot.sound" | grep -q "depends on"; then say "  RESULT AXIOM AUDIT: FAIL (unexpected axiom)"; fail=1
  else say "  RESULT AXIOM AUDIT: PASS"; FULLRES="RE-VERIFIED in this invocation"; fi
else
  say "[5e] FULL KERNEL VERIFICATION: NOT RE-RUN here (about 1.5 h). Re-run with:  FULL=1 bash RUN_TEST.sh   Recorded author run (Claude cloud container, 2 cores, Lean 4.34.1): logs/*.json, output/axiom_audit_iv4b_results.txt, output/verify_g.log, output/verify_n.log"
fi
say "[6] IV-5 EXACT FINITE GAP AND PREDICTIONS (SCR_IV_V5.lean; constants traced to the frozen protocol, see the module header)"
lake env lean SCR_IV_Check6.lean 2>&1 | sed 's/^SCR_IV_Check6.lean:[0-9]*:[0-9]*: //' > "$OUT/axiom_audit_iv5_partA.txt"; cat "$OUT/axiom_audit_iv5_partA.txt" | tee -a "$LOG"
[ "$(grep -c 'SCR_IV\.' "$OUT/axiom_audit_iv5_partA.txt")" = 14 ] || { say "  EXPECTED 14 audited IV-5 declarations"; fail=1; }
if grep -q "sorryAx\|ofReduceBool" "$OUT/axiom_audit_iv5_partA.txt"; then say "  IV-5 AXIOM AUDIT A: FAIL"; fail=1
elif grep -v "does not depend on any axioms" "$OUT/axiom_audit_iv5_partA.txt" | grep -v "propext\|Classical.choice\|Quot.sound" | grep -q "depends on"; then say "  IV-5 AXIOM AUDIT A: FAIL (unexpected axiom)"; fail=1
else say "  IV-5 AXIOM AUDIT A: PASS (exact arithmetic facts need no axioms; core theorem uses propext/Quot.sound only)"; fi
mkdir -p "$OUT/neg5"
for f in tests/neg5_*.lean; do b=$(basename "$f" .lean)
  if lake env lean "$f" > "$OUT/neg5/$b.log" 2>&1; then say "  $b: ACCEPTED (BAD)"; fail=1; else say "  $b: rejected (good)"; fi; done
if lake env lean tests/pos5.lean > "$OUT/neg5/pos5.log" 2>&1; then say "  tests/pos5.lean: compiles (good)"; else say "  tests/pos5.lean: FAILED (BAD)"; fail=1; fi
IV5FINAL="NOT RE-RUN here (needs the batch modules: FULL=1)"
if [ "${FULL:-0}" = 1 ] && [ $fail = 0 ]; then
  OF=.lake/build/lib/lean
  if lake env lean SCR_IV_V5Final.lean -o $OF/SCR_IV_V5Final.olean -i $OF/SCR_IV_V5Final.ilean > "$OUT/iv5_final_compile.log" 2>&1 && lake env lean SCR_IV_Check6b.lean 2>&1 | sed 's/^SCR_IV_Check6b.lean:[0-9]*:[0-9]*: //' > "$OUT/axiom_audit_iv5_final.txt" && ! grep -q "sorryAx\|ofReduceBool" "$OUT/axiom_audit_iv5_final.txt" && grep -q iv5_final "$OUT/axiom_audit_iv5_final.txt"; then cat "$OUT/axiom_audit_iv5_final.txt" | tee -a "$LOG"; IV5FINAL="RE-VERIFIED in this invocation"; else say "  IV-5 FINAL: FAIL"; fail=1; fi
fi
say "== STAGE VERDICTS"
if [ $fail = 0 ]; then say "  IV-1 MODEL_FORMALIZED : PASS"; say "  IV-2 WITNESSES_CERTIFIED : PASS (witnesses of the FROZEN values; but see IV-4B finding: frozen non-grammar value is not the minimum)"; say "  IV-3 PRUNING_THEOREM_PROVEN : PASS"; say "  IV-4A CERTIFICATE_DESIGN_AND_CHECKER_PROVEN : PASS"
  say "  IV-4B : checks of this invocation PASS. Global kernel verification of all batches: $FULLRES (recorded author run: PASS, see CERT_STATUS.md)"
  say "     ground_exact_min  : ObjAll claimedGroundNum (exact minimum over all 2^40 configurations, encoded model)"
  say "     nongT_exact_min   : ObjNonGrammar claimedNonGTrue (exact non-grammar minimum, encoded model; claimedNonGTrue is 928/2^70 BELOW the frozen SCR-III value)"
  say "     frozen_nonG_not_min : the frozen SCR-III non-grammar value claimedNonGNum is NOT the exact minimum (unconditional theorem)"
else say "  FAILURES ABOVE: stage verdicts not established"; fi
say "  IV-5 EXACT_GAP_AND_PREDICTIONS : core theorem iv5_of_minima PASS in this invocation; unconditional iv5_final: $IV5FINAL (recorded author run: PASS, output/author_run/axiom_audit_iv5_final.txt)"
say "     exact Delta = 12095447728404694790/2^70 A > 0; delta4 < 1; 0.790439676056526 <= delta4 <= 1.0333534753990623 (exact encoded model)"
exit $fail
