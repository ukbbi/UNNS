#!/usr/bin/env python3
"""IV-4B: pack the 2^D0 frontier certificates into batch modules (untrusted data + a kernel theorem per batch) and write the assembly module.
usage: mk_batches.py ROOT CERTDIR OBJ(ground|nongT) D0 BUDGET     -> Bat/B<g|n>_NNN.lean, Fin_<g|n>.lean, bat_<g|n>.json (modules list + batch boundaries)"""
import sys, json, pathlib
sys.set_int_max_str_digits(0)
ROOT, CD, OBJ, D0, BUD = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
tag = {"ground": "g", "nongT": "n"}[OBJ]
U, leaf, fin = {"ground": ("claimedGroundNum", "(fun _ => false)", "ground_min_of_frontier"), "nongT": ("claimedNonGTrue", "leafGrammar", "nonGT_min_of_frontier")}[OBJ]
cs = [int(x) for x in (CD/f"cert_{OBJ}_D{D0}.txt").read_text().split()]; st = json.load(open(CD/f"stats_{OBJ}_D{D0}.json")); nt = st["ntok"]
assert len(cs) == 1 << D0
(ROOT/"Bat").mkdir(exist_ok=True)
batches = []; cur = []; w = 0
for b in range(1 << D0):
    if cur and w + nt[b] > BUD: batches.append(cur); cur = []; w = 0
    cur.append(b); w += nt[b]
batches.append(cur)
mods = []; lo = 0
for k, bl in enumerate(batches):
    assert bl[0] == lo; name = f"B{tag}_{k:03d}"; mods.append(name)
    (ROOT/"Bat"/f"{name}.lean").write_text(f"import SCR_IV_V4\nopen SCR_IV\nnamespace Bat\n/-- Certificates of frontier prefixes {bl[0]}..{bl[-1]} (untrusted data). -/\ndef cs_{name} : List Nat := {[cs[b] for b in bl]}\n"
        f"theorem bat_{name} : batchOK Rreal 40 {U} {leaf} {D0} {bl[0]} cs_{name} = true := by decide +kernel\nend Bat\n")
    lo += len(bl)
assert lo == 1 << D0
imps = "\n".join(f"import Bat.{m}" for m in mods)
lst = ", ".join(f"cs_{m}" for m in mods)
body = [f"import SCR_IV_V4\n{imps}\nopen SCR_IV Bat\n/-! Assembly for the {OBJ} objective (D0 = {D0}): {len(mods)} separately kernel-checked batch theorems => every frontier prefix certified => exact minimum. -/",
        f"def allB_{tag} : List (List Nat) := [{lst}]", f"theorem allB_{tag}_len : allB_{tag}.flatten.length = 2 ^ {D0} := by decide +kernel",
        f"theorem allB_{tag}_ok : batchesOK Rreal 40 {U} {leaf} {D0} 0 allB_{tag} = true := by"]
lo = 0
for m, bl in zip(mods, batches):
    body.append(f"  refine bcons (lo' := {lo+len(bl)}) (Bat.bat_{m}) (by decide +kernel) ?_"); lo += len(bl)
body.append("  exact batchesOK_nil ..")
body += [f"theorem {OBJ}_frontier_all : ∀ b, b < 2 ^ {D0} → subOK Rreal 40 {U} {leaf} {D0} b (allB_{tag}.flatten.getD b 0) = true :=\n  batches_cover allB_{tag}_ok allB_{tag}_len",
         f"/-- RESULT ({'ground: min over all configurations' if OBJ=='ground' else 'corrected non-grammar: min over configurations with a violated vertex'}), exact encoded model. -/",
         f"theorem {OBJ}_exact_min : {'ObjAll claimedGroundNum' if OBJ=='ground' else 'ObjNonGrammar claimedNonGTrue'} :=\n  {fin} (D0 := {D0}) (by decide) (certOf := fun b => allB_{tag}.flatten.getD b 0) {OBJ}_frontier_all"]
(ROOT/f"Fin_{tag}.lean").write_text("\n".join(body)+"\n")
json.dump(dict(mods=mods, sizes=[len(b) for b in batches], tokens=[sum(nt[b] for b in bl) for bl in batches]), open(ROOT/f"bat_{tag}.json", "w"))
print(OBJ, "batches", len(mods), "max tokens/batch", max(sum(nt[b] for b in bl) for bl in batches))
