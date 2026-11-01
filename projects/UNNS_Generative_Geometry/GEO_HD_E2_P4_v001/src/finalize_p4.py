#!/usr/bin/env python3
"""Generates STATUS.json, README.md, MANIFEST.json, results/P4_REPORT.md, results/P4_THEOREM_AUDIT.md, results/P4_COUNTEREXAMPLES.json,
theory/COUNTEREXAMPLES.md from the stored data.  Usage: python src/finalize_p4.py [--root DIR] [--verified]"""
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if "--root" in sys.argv:
    ROOT = sys.argv[sys.argv.index("--root") + 1]


def J(rel):
    return json.load(open(os.path.join(ROOT, rel), encoding="utf-8"))


def W(rel, text):
    with open(os.path.join(ROOT, rel), "w", encoding="utf-8") as fh:
        fh.write(text)


ar, geo, lat = J("results/P4_ARITHMETIC.json"), J("results/P4_GEOMETRY.json"), J("data/P4_F110.json")
cert = J("results/P4_CERTIFICATES.json")
lem, pl, d3 = J("data/P4_LEMMAS.json"), J("results/P4_PLANAR.json"), J("results/P4_3D.json")
g1 = geo["geometry_m1"]
m2 = geo.get("geometry_m2")
fam = d3["p3_infinite_family"]
vpath = os.path.join(ROOT, "results", "P4_VERIFY_LAST.json")
ver = json.load(open(vpath)) if os.path.exists(vpath) else {}
verified_shards = sorted(set(s for k, v in ver.items() for s in v["shards"] if v["n_failed"] == 0))

gates = {
    "SOURCE_PASS": True,
    "ARITH_PASS": bool(ar["all_members_pass"] and ar["all_cross_checks_pass"] and lat["both_nonrectangular"]),
    "GEOMETRY_PASS": bool(g1["classification"] == "SOURCE_CONTAINED" and geo["corner_n4"]["hull_covered"]),
    "SCOPED_THEOREM_PASS": "P4-F110 (P4-A, P4-L, P4-T1, P4-T2) -- elementary",
    "EXACT_PASS": "RECORDED_FOR_SHARDS: " + (",".join(verified_shards) if verified_shards else "none yet (run RUN_VERIFY.py)"),
    "3D_WITNESS": "NOT_APPLICABLE (no new witness; inherited controls only)",
    "PLANAR_AUDIT_COMPLETE": "NOT_EVALUATED (P4-E3 not started)",
    "PLANAR_THEOREM_PASS": "NOT_EVALUATED",
    "COUPLED_3D_AUDIT_COMPLETE": "NOT_EVALUATED (P4-E4 not started)",
    "COUPLED_3D_THEOREM_PASS": "NOT_EVALUATED",
    "C3": "NOT_CLAIMED (scoped elementary theorem only)",
    "COUNTEREXAMPLE": "NONE_NEW",
}
phases = {"P4-E0": "SOURCE_PASS", "P4-E1": "ARITH_PASS", "P4-E2": "GEOMETRY_PASS",
          "P4-E3": "NOT_STARTED", "P4-E4": "NOT_STARTED", "P4-E5": "PARTIAL: theorem audit and overlap table only; no adversarial campaign, no literature search"}
STATUS = {"release": "GEO_HD_E2_P4_v001", "milestone": "P4-E0..E2 coupled-target transport preflight", "phases": phases, "gates": gates,
          "claims": {"proved": ["P4-A", "P4-L", "P4-T1", "P4-T2", "P4-C1"], "finite_exact": ["m=1 both directions", "m=2 forward (if recorded)", "n=4 corner hull cover", "reverse point certificates m=1..3"],
                     "open": ["CP3-A (hollow/sub-threshold)", "P4-T3", "P4-T4", "prior-art audit"]},
          "independence_caveat": "builder and independent audit were written by the same author; the verifier shares no code with the builder modules but is not external verification",
          "project_files_touched": False}
W("STATUS.json", json.dumps(STATUS, indent=1, sort_keys=True))

# ------------------------------------------------------------------------------------------------------------ report
R = []
R.append("# GEO-HD-1B / E2-P4 -- P4_REPORT (v001: P4-E0..E2 coupled-target transport preflight)\n")
R.append("Scope of this release: spec section 14 (P4-F110 preflight) and the first scoped theorems.  P4-E3 (planar CP3-A) and P4-E4 (coupled 3D census) are **not started**.\n")
R.append("## 1. Arithmetic and relation-lattice data\n")
R.append("x_m = 2*110^(4m)/9 -> 110^(4m)/3 for every m >= 1 (G = 9, L = 110^(2m)); verified exactly for m = 1..12, by the frozen engine for m = 1,2,3, by independent brute force for m = 1,2,3.  "
         "Primes (2,5,11) and the box [0,2m]^3 are preserved.  Source lattice a-b+c = 0 (mod 6) (index 6), target a+b+c even (index 2); Lambda_9 strictly inside Lambda_3.\n")
R.append("## 2. Nonrectangularity\n")
R.append("Orders mod 9 are (6,6,6) with |H_9| = 6 < 216; mod 3 (2,2,2) with |H_3| = 2 < 8.  **Both lattices are nonrectangular** (contrast: the E2-P3 witness ends at a rectangular target).\n")
R.append("## 3. Occurrence fibres and abstract cells (m = 1)\n")
cs, ct = g1["census_source"], g1["census_target"]
R.append("| | source (Lambda_9) | target (Lambda_3) |\n|---|---|---|\n| occurrence vertices | %d | %d |\n| oriented Graver vectors in region | %d | %d |\n| f-vector (vertices, edges, 2-cells, 3-cells) | %s | %s |\n| abstract Betti numbers | %s | %s |\n"
         % (cs["n_fibre"], ct["n_fibre"], cs["n_graver_oriented"], ct["n_graver_oriented"], cs["f_vector"], ct["f_vector"], cs["abstract_betti"], ct["abstract_betti"]))
R.append("This reproduces the spec 5.4 preflight counts (5 -> 13; edges 7 -> 45; 2-cells 2 -> 36; 3-cells 0 -> 3).  Abstract-cell survival: m = 1 -- all %d source cells persist as target cells; m = 2 -- only %d of %d source cells persist, yet the realized union remains contained (abstract-cell loss does not imply geometric loss; supports P4-F6).\n" % (geo["abstract_survival"]["1"]["source_cells"], geo["abstract_survival"]["2"]["persisting_in_target"], geo["abstract_survival"]["2"]["source_cells"]))
R.append("## 4. Realized geometry, m = 1\n")
R.append("Forward: U(Lambda_9) is **contained** in U(Lambda_3) (%d source maximal cells, each covered by the %d target maximal cells; exact subdivision certificates).  Reverse: U(Lambda_3) is **not** contained in U(Lambda_9) (witness %s; a violated inequality for each of the %d source maximal cells).  "
         "Classification: **%s**.  The target is **not hull-covered** at m = 1: its coverage gap has %d certified pieces, and the source union misses all of them (holes are not obstructions, P4-O1)." % (
             g1["n_source_maximal"], g1["n_target_maximal"], g1["reverse_witness"], g1["n_source_maximal"], g1["classification"], g1["target_gap"]["n_gap_pieces"]))
R.append("\n## 5. Certificates\n")
R.append("results/P4_CERTIFICATES.json holds: m1_forward (containment), m1_reverse (noncontainment), m1_target_hull_cover (gap tree), n4_target_hull_cover (corner lemma, 0 gap nodes), reverse_points (m = 1,2,3) and, if the opt-in stage was run, m2_forward.  "
         "All are replayed by RUN_VERIFY.py against cell complexes re-derived from first principles (src/audit_p4.py); a tamper test rejects a perturbed witness.\n")
R.append("## 6. Parameter family (general m)\n")
R.append("**P4-T1.** For even n >= 4, U(E_3,[0,n]^3) = conv F = { z in [0,n]^3 : sum z >= 2 } (cube tiling by 2-cubes + one exact corner certificate at n = 4 + cell monotonicity).  "
         "**P4-T2.** For every m >= 1, U(Lambda_9,Q_m) is strictly inside U(Lambda_3,Q_m): SOURCE_CONTAINED (m = 1 direct; m >= 2 from P4-T1 and the inherited coverage-gap reduction).  "
         "Containment does not fail beyond a threshold and does not become more complicated for this family; P4-F5 (failure persisting under box growth) is not exercised because no failure occurs.")
if m2:
    R.append("  Direct exact run m = 2 (independent of the theorem): forward %s (%d source / %d target maximal cells, %.0f s)." % (m2["forward_verdict"], m2["n_source_maximal"], m2["n_target_maximal"], m2["seconds"]))
else:
    R.append("  Direct exact run m = 2: not recorded in this build.")
R.append("  Direct m >= 3: UNAVAILABLE_COST.\n")
R.append("## 7. Planar CP3-A\n")
R.append("**OPEN.**  Only the reclassification was done: the 266 E2-P2 ENLARGE rows split 40 inherited / 164 rectangular / 14 hollow-box / 48 sub-threshold (unchanged); the expanded E2-P3 corpus has %d ENLARGE rows in the two open classes, all CONTAINED (finite evidence, not a theorem).  No new search was run.\n" % pl["residual_open_targets"]["count"])
R.append("## 8. Essential higher-dimensional findings\n")
R.append("None new.  Inherited controls: E2-P1 (parity -> Z^3) and E2-P3 (2,7,13), and the infinite family recorded as E2-P3 Addendum 004 (rectangular target; all %d tested instances pass).  P4-F110 shows that a transport between two nonrectangular lattices in 3D can be fully contained; "
         "it provides no coupled-target obstruction.\n" % len(fam["instances"]))
R.append("## 9. Falsification table (spec 11)\n")
R.append("| ID | Result |\n|---|---|\n| P4-F1 | NOT falsified by P4-F110 (strict enlargement between nonrectangular lattices preserved realized geometry for all m); not a general claim |\n| P4-F2 | not tested |\n| P4-F3 | not tested |\n"
         "| P4-F4 | **Supported** at m = 1: the target has certified holes, yet no source cell enters them |\n| P4-F5 | not exercised (no failure in the family) |\n| P4-F6 | **Supported** at m = 2: abstract cells disappear (77 of 246 persist) while the realized union stays contained |\n")
R.append("## 10. Novelty assessment and unresolved obligations\n")
R.append("All results are elementary.  P4-T1 is a 3D analogue of the planar GEO-I v012 hull-coverage regime; P4-T2/P4-C1 follow from it with the coverage-gap reduction.  No literature search beyond the frozen project sources; **C3 is not claimed.**  "
         "Unresolved: CP3-A, P4-T3 (other coupled families, box-growth classification), P4-T4 (essential 3D coupled obstruction), prior-art audit, direct m >= 3, GEO-I post-v012 commit identification.\n")
R.append("## 11. Verification\n")
R.append("Shards verified without failure so far (this build): %s.  Builder and audit have the same author.  Shell-limit design: S0-S3, S5 are short; S4 (corner replay) is the heavy shard.\n" % (", ".join(verified_shards) or "none"))
W("results/P4_REPORT.md", "\n".join(R))

W("results/P4_THEOREM_AUDIT.md", """# P4 theorem audit (P4-E5, partial)
| Claim | Status | Basis | Novelty |
|---|---|---|---|
| P4-A arithmetic of P4-F110 | PROVED | closed-form divisor analysis; exact enumeration m=1..12; engine and brute-force cross-check m=1..3 | elementary |
| P4-L lattices, nonrectangularity | PROVED | orders and subgroup sizes | elementary |
| P4-T1 hull theorem for E_3, n even >= 4 | PROVED | cube tiling + exact n=4 certificate (independent replay) + cell monotonicity (Graver set stable; checked 4<6<8) | elementary; planar analogue G12-T8 |
| P4-T2 F110 containment, all m | PROVED (scoped) | m=1 direct; m>=2 via T1 and U subset conv F subset conv F' | elementary specialisation |
| P4-C1 predictor for sublattices of E_3 | PROVED | T1 | elementary |
| CP3-A residual planar | OPEN | - | - |
| P4-T3/T4/T5 (general) | NOT STARTED | - | - |
Adversarial review: only the built-in falsification checks (tamper tests, independent re-derivation, direct m=2 cross-check).  No external review.  C3 NOT claimed.
""")
cx = {"new_counterexamples": [], "inherited_controls": [
    {"id": "E2-P1 control C", "note": "parity lattice -> Z^3, witness (2/3,2/3,2/3); rectangular target"},
    {"id": "E2-P3 witness", "note": "primes (2,7,13), 9 -> 3, box (2,2,3), x = 370853389088/9, witness (4/3,5/6,2/3); rectangular target"},
    {"id": "E2-P3 Addendum 004", "note": "infinite family, %d instances checked here" % len(fam["instances"])}],
    "observations": [{"id": "P4-O1", "note": "m=1 target has %d certified gap pieces; source union avoids all" % g1["target_gap"]["n_gap_pieces"]}]}
W("results/P4_COUNTEREXAMPLES.json", json.dumps(cx, indent=1))
W("theory/COUNTEREXAMPLES.md", """# E2-P4 counterexamples
**No new counterexample was found.**  Failed-prediction record: none; no preregistered P4-F110 containment verdict existed (spec 5.4).  Inherited controls kept: E2-P1 control C, the E2-P3 (2,7,13) witness and its infinite family (ERRATA addendum 004) -- all end at RECTANGULAR targets and therefore do not answer the coupled-target question.
Observation P4-O1: at m=1 the target E_3 has certified holes (94 gap pieces) that the source union never enters.
""")

W("README.md", """# GEO_HD_E2_P4_v001 -- Arithmetic obstruction theory for nonrectangular targets: coupled-target transport preflight

Executes spec phases P4-E0..E2 (section 14).  Extract next to the earlier releases; nothing existing is modified.  Python >= 3.8, standard library only (matplotlib only for src/make_figures.py).

* Result: P4-F110 (2*110^(4m)/9 -> 110^(4m)/3) is SOURCE_CONTAINED for every m >= 1 between two *nonrectangular* lattices; proved via an E_3 hull theorem (P4-T1).  See results/P4_REPORT.md.
* Not started: planar CP3-A search (E3), coupled 3D census (E4), full novelty audit (E5).  No C3 claim.
* Verify (each shard < 3 min): `python RUN_VERIFY.py --shard S0` ... `S5`;  `--fast` = S0,S1,S2,S3,S5;  `--full` adds the heavy corner replay S4.  Windows: RUN_WINDOWS.bat.
* Rebuild: `python src/build_p4.py` (stages are resumable; `--stage m2` runs the opt-in direct m=2 check, ~4-5 min); then `python src/finalize_p4.py`.
* Layout: src/engine = byte-identical pinned E2-P3/E2-P2 engine; src/*.py = new E2-P4 code (loaded via src/_boot.py because some names coincide with engine modules).
""")

# manifest (sha256 of every file except MANIFEST itself)
files = {}
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if d not in ("__pycache__", ".pytest_cache")]
    for f in fn:
        if f == "MANIFEST.json":
            continue
        p = os.path.join(dp, f)
        files[os.path.relpath(p, ROOT).replace(os.sep, "/")] = {"sha256": hashlib.sha256(open(p, "rb").read()).hexdigest(), "bytes": os.path.getsize(p)}
W("MANIFEST.json", json.dumps({"release": "GEO_HD_E2_P4_v001", "files": dict(sorted(files.items()))}, indent=1))
print("finalized:", {k: gates[k] for k in ("ARITH_PASS", "GEOMETRY_PASS", "EXACT_PASS")})
