"""E03 -- renders RESULTS/report.md from E01/E02 JSON (no new mathematics)."""
import json, os
from math import log2
import _path
R = json.load(open(os.path.join(_path.ROOT, "RESULTS", "E01_information_recovery.json")))
Q = json.load(open(os.path.join(_path.ROOT, "RESULTS", "E02_relabeling.json")))
L = []
L.append("# GIG-INFO v001 — Information recovery across arithmetic topological transitions (findings, mathematics first)\n")
for tag in ("A1", "A2"):
    r = R[tag]
    L.append("## Anchor %s: content %s, m0=%d\n" % (tag, tuple(r["content"]), r["m0"]))
    e = r["ensembles"]["sources_60_binaryY"]
    L.append("Survival law on the 60 sources t=1..60: Y=1 iff gcd(t,%d)=1 (%s); survivors %d/60; %d distinct systems among the 60.\n" % (r["law_check"]["gcd_modulus"], r["law_check"]["survives_iff_gcd(t,modulus)=1_for_all_60"], e["survivors"], e["distinct_systems_among_60"]))
    L.append("| level | classes | H(O) bits | H(Y) | H(Y given O) | I(Y;O) |\n|---|---|---|---|---|---|")
    for lev, v in e["levels"].items():
        L.append("| %s | %d | %s | %s | %s | %s |" % (lev, v["observation_classes"], v["H(O)"][:9], v["H(Y)"][:9], v["H(Y|O)"][:9], v["I(Y;O)"][:9]))
    L.append("")
    sp = r["separating_pairs"]
    L.append("Pair search over ALL %d system classes (every source m, grouped by capped valuations): binary-Y separating pairs per level %s; three-valued (NA = anchor class not contained) %s.\n" % (r["lattice_classes"], {k: len(v) for k, v in sp["binaryY"].items()}, {k: len(v) for k, v in sp["threevalued"].items()}))
    for p in sp["binaryY"]["O0"] + sp["threevalued"]["O0"]:
        L.append("- equal N: m=%d (Y=%s) vs m=%d (Y=%s), first separating level %s" % (p["m_a"], p["Y_a"], p["m_b"], p["Y_b"], p["first_level_separating"]))
    L.append("")
    a = r.get("additivity")
    L.append("History count over prime indicators on the comparable window: N0=%d, ΔN=%s, additive: %s.\n" % (a["N_at_minimal_survivor"], a["delta_N_by_prime_indicator"], a["N_equals_N0_plus_sum_delta_over_indicators"]))
    L.append("Divisibility arrows m→mp (comparable classes): Y transitions by prime %s. Information change from the surviving source:" % r["arrow_Y_transitions_by_prime"])
    n0 = a["N_at_minimal_survivor"]
    for p, d in a["delta_N_by_prime_indicator"].items():
        L.append("- ×%s: N %d → %d, ΔH_hist = log2(%d/%d) = %.6f bits, Y 1→0" % (p, n0, n0 + d, n0 + d, n0, log2((n0 + d) / n0)))
    L.append("\nCertificates (all comparable classes): %d, all independently verified: %s.\n" % (len(r["certificates"]), r["certificates_all_verified"]))
L.append("## Relabelling\n%s\n" % json.dumps(Q))
open(os.path.join(_path.ROOT, "RESULTS", "report.md"), "w").write("\n".join(L))
print("\n".join(L)[:3500])
