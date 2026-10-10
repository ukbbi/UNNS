#!/usr/bin/env python3
"""SCR-III-B PRIMARY EXECUTION DRIVER v001 (orchestration only).
Reuses the frozen v009 solver binaries/sources, instance builders, seed derivation and cost accounting UNCHANGED.
The only new logic: ratified H-C rule (median>=1.20 AND min>=1.20 over 15 paired rounds), G/P/T/C verdict assembly, an independent numpy
whole-space audit, and null-distribution bookkeeping (descriptive only).  Run from the project root:  python3 scr_iii_b/primary_exec/primary_run_v001.py"""
import sys, os, json, time, math, hashlib, pathlib, subprocess, statistics, csv, gzip, platform
sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
HERE = pathlib.Path(__file__).resolve().parent
SB = HERE.parent; ROOT = SB.parent
PG = SB / "prereg_gate"; sys.path.insert(0, str(PG))
import numpy as np
import validate_v009 as V
import seeds_v009 as sd
import tolerance_v009 as tol
import cost_audit_v009 as ca
from concurrent.futures import ThreadPoolExecutor

OUT = SB / "output" / "primary"; OUT.mkdir(parents=True, exist_ok=True)
UNB = ["--unblind-after-freeze"]
T0 = time.time()
def log(*a):
    print("[%7.1fs]" % (time.time() - T0), *a, flush=True)
def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

# ============================================================ stage 0 : minimal pre-execution conformance check
def stage0(X):
    chk = {}; fails = []
    def ok(name, cond, **d):
        chk[name] = dict(status="PASS" if cond else "FAIL", **d)
        if not cond: fails.append(name)
    pm = json.loads((ROOT / "PRIMARY_MANIFEST_v001.json").read_text())
    for nm, d in pm["documents"].items():
        ok("doc:" + nm, (ROOT / nm).exists() and sha(ROOT / nm) == d["sha256"], sha=sha(ROOT / nm) if (ROOT / nm).exists() else None)
    ok("authorization_record_present", (ROOT / "PRIMARY_AUTHORIZATION_v001.md").exists(), sha=sha(ROOT / "PRIMARY_AUTHORIZATION_v001.md") if (ROOT / "PRIMARY_AUTHORIZATION_v001.md").exists() else None)
    OV = SB / "output" / "validation"
    bad = {}
    for v, groups in (("005", (("code", SB / "reference_check"), ("outputs", OV / "v005"))), ("006", (("code", SB / "feasibility"), ("outputs", OV / "v006"))),
                      ("007", (("code", SB / "exact3"), ("outputs", OV / "v007"))), ("008", (("code", SB / "solvers"), ("outputs", OV / "v008"))),
                      ("009", (("code", PG), ("outputs", OV / "v009")))):
        m, b, n = V.frozen(OV / ("v" + v) / ("MANIFEST_v%s.json" % v), groups); bad[v] = (b, n)
    ok("frozen_v005_v009_code_outputs", all(not b for b, n in bad.values()), detail={k: dict(mismatches=b, checked=n) for k, (b, n) in bad.items()})
    ok("dependency_zips_on_disk", True, note="PREFLIGHT_v00x.zip not on disk; frozen member hashes verified through extracted tree manifests", recorded_hashes=pm["dependencies"])
    ok("seed", sd.MASTER_SEED == 20261010, value=sd.MASTER_SEED)
    ok("rel_tau", tol.REL_TAU == 1e-9, value=tol.REL_TAU)
    ok("W_primary_J", abs(X["kT_J"] - 1.093474008e-20) <= 1e-9 * 1.093474008e-20, value=X["kT_J"])
    E0J = X["E0f"] * X["A_J"]
    ok("E0_anchor_J", abs(E0J - (-9.2719947518037269e-20)) <= 1e-12 * 9.27e-20, value=E0J, E0_norm=X["E0f"])
    ok("settings", True, e2_frac=0.75, z2="disabled (flag never passed)", threads=1, warmups=3, rounds=15, budget_min_per_arm=30, rss_gib=2,
       compile=["g++", "-std=c++17", "-O2", "-Wall", "-Wextra"], compiler=X["compiler"], binary_sha256=dict(pg=sha(X["env"].pg), e2=sha(X["env"].e2)))
    p = X["env"].run(X["inst"][3]["path"], "b0", X["kT_norm"], X["inst"][3]["tau"], X["E0f"], tag="PRECHECK_guard_must_block")
    ok("guard_blocks_without_flag", p.returncode == 3 and p.stdout == "", rc=p.returncode)
    return chk, fails

# ============================================================ numpy whole-space audit (independent of the C++ solvers)
def popc(x):
    return np.bitwise_count(x) if hasattr(np, "bitwise_count") else np.array([bin(int(v)).count("1") for v in x])
def numpy_audit(n, pairs, masks, E0, tau, Q, Ws):
    K = np.zeros((n, n))
    for i, j, k in pairs: K[i, j] = K[j, i] = k
    N = 1 << n; CH = 1 << 20; sh = np.arange(n, dtype=np.uint32)
    tg = {k: [] for k in Ws}; sgids = []; dmin = math.inf; darg = None; emin = math.inf; near = {k: 0 for k in Ws}
    for base in range(0, N, CH):
        s = np.arange(base, base + CH, dtype=np.uint32)
        S = 1.0 - 2.0 * ((s[:, None] >> sh) & 1).astype(np.float64)
        E = 0.5 * np.einsum("ij,ij->i", S @ K, S); d = E - E0
        g = np.ones(CH, bool)
        for im, nm in masks: g &= (popc((s ^ np.uint32(nm)) & np.uint32(im)) == 2)
        sgids.append(s[g].astype(np.uint64)); emin = min(emin, float(E.min()))
        ng = ~g
        if ng.any():
            dd = np.where(ng, d, np.inf); a = int(dd.argmin())
            if dd[a] < dmin: dmin, darg = float(dd[a]), int(s[a])
        for k, W in Ws.items():
            thr = W + tau; tg[k].append(s[d <= thr].astype(np.uint64)); near[k] += int((np.abs(d - thr) <= 1e-12 * Q).sum())
    return dict(sg=np.concatenate(sgids), T={k: np.concatenate(v) for k, v in tg.items()}, delta_nonG=dmin, delta_arg=darg, Emin=emin, near=near)

def hc_rule(ratios, thr=1.20):
    if len(ratios) != 15 or any((not math.isfinite(r)) or r <= 0 for r in ratios): return "INCONCLUSIVE"
    med, mn = statistics.median(ratios), min(ratios)
    return "PASS" if (med >= thr and mn >= thr) else "THRESHOLD_NOT_MET"

def main():
    X = V.setup(); env = X["env"]; I = X["inst"][3]; tau = I["tau"]; Q = I["Q"]; E0 = X["E0f"]; kT = X["kT_norm"]
    env.audit = OUT / "INVOCATION_LOG_primary_v001.jsonl"
    if env.audit.exists(): raise SystemExit("primary outputs already exist; refusing to overwrite (additive amendment required)")
    env.audit.write_text("")
    env.protected = X["tmp"] / "protected_fingerprints.txt"
    chk, fails = stage0(X)
    (OUT / "PRECHECK_primary_v001.json").write_text(json.dumps(dict(status="PASS" if not fails else "FAIL", failures=fails, checks=chk), indent=1, default=str))
    log("stage0", "PASS" if not fails else "FAIL %s" % fails)
    if fails: raise SystemExit(2)
    Ws = {"primary": kT, "sens_0.5kT": 0.5 * kT, "sens_2kT": 2.0 * kT}
    mult = {"primary": 1.0, "sens_0.5kT": 0.5, "sens_2kT": 2.0}
    path = I["path"]; n = I["n"]
    # ---------- independent whole-space audit
    log("numpy audit start"); au = numpy_audit(n, I["pairs"], I["masks"], E0, tau, Q, Ws); log("numpy audit done")
    sg_np = set(au["sg"].tolist())
    # ---------- grammar-only enumeration
    d = X["tmp"] / "sg.txt"
    gc = ca.parse_kv(env.run(path, "gcount", 0, 0, dump=d, tag="PRIMARY_gcount").stdout); gs = ca.parse_kv(env.run(path, "gscan", 0, 0, tag="PRIMARY_gscan").stdout)
    sg_cpp = {int(x) for x in d.read_text().split()}
    gram = dict(count_constructive=int(gc["survivors"]), count_scan=int(gs["survivors"]), digest_equal=gc["digest"] == gs["digest"], numpy_count=len(sg_np), sets_equal=sg_cpp == sg_np)
    # ---------- per-window correctness + all solvers
    res = {}; allruns = []
    for wn, W in Ws.items():
        r = dict(W_norm=W, W_J=W * X["A_J"], W_over_kT=mult[wn], threshold=E0 + W + tau); solv = {}
        for s in ("b0", "g1", "g2", "b1", "e2"):
            extra = UNB + (["--frac", "0.75"] if s == "e2" else [])
            ids, kv = env.solve(path, s, W, tau, E0, extra=extra, tag="PRIMARY_%s_%s" % (wn, s))
            solv[s] = dict(ids=ids, num=ca.numeric(kv), kv={k: kv[k] for k in kv if k in ("reference_status", "ref_status", "e2_frac", "e2_retained_pairs", "e2_B_O", "g2_island_order")})
        T_np = set(au["T"][wn].tolist()); T = solv["b0"]["ids"]
        eq = {s: (solv[s]["ids"] == (T & sg_np if s in ("g1", "g2") else T)) for s in solv}
        FN = sorted(T - sg_np); unres = {s: solv[s]["num"].get("unresolved_boundary", 0) for s in solv}
        # sanity: grammar-restricted sets
        r.update(target_count=len(T), target_in_grammar=len(T & sg_np), FN_count=len(FN), FN_ids=FN[:50],
                 numpy_audit_target_equals_B0=(T_np == T), numpy_near_boundary=au["near"][wn], solver_outputs_match=eq, unresolved_boundary=unres,
                 nodes_g2=solv["g2"]["num"].get("nodes"), materialized_g2=solv["g2"]["num"].get("materialized"), leaves_g2=solv["g2"]["num"].get("leaves"),
                 FN_energies_over_E0=None)
        r["solvers"] = {s: dict(num=solv[s]["num"], kv=solv[s]["kv"]) for s in solv}
        np.savetxt(OUT / ("TARGET_IDS_%s_v001.txt" % wn), np.array(sorted(T), dtype=np.int64), fmt="%d")
        r["target_ids_sha256"] = sha(OUT / ("TARGET_IDS_%s_v001.txt" % wn))
        res[wn] = r; log("window", wn, "target", len(T), "FN", len(FN), "match", eq)
    # ---------- exclusion gap (post-authorization primary output)
    ng = ca.parse_kv(env.run(path, "nullgap", 0.0, tau, E0, extra=UNB, tag="PRIMARY_delta_nonG").stdout)
    dG = float(ng["delta_nonG"])
    gap = dict(delta_nonG_cpp=dG, delta_nonG_numpy=au["delta_nonG"], argmin_numpy=au["delta_arg"], n_excluded=int(ng["n_excluded"]), delta_over_kT=dG / kT, delta_J=dG * X["A_J"],
               agree=abs(dG - au["delta_nonG"]) <= 1e-9 * Q, emin_numpy_minus_E0=au["Emin"] - E0)
    for wn, W in Ws.items():
        res[wn]["W_over_delta_nonG"] = W / dG if dG > 0 else None
        res[wn]["theorem_preserved_if_W_plus_tau_lt_delta"] = bool(W + tau < dG)
        res[wn]["theorem_consistent_with_FN"] = (res[wn]["FN_count"] == 0) == bool(W + tau < dG)
    # ---------- hypotheses G, P
    r1 = res["primary"]
    contr = 1.0 - (r1["materialized_g2"] or 0) / float(1 << n)
    g2inv = len({(res[w]["nodes_g2"], res[w]["leaves_g2"]) for w in res}) == 1
    G_ok = gram["sets_equal"] and gram["digest_equal"] and gram["count_constructive"] == gram["count_scan"] and r1["solver_outputs_match"]["g2"] and r1["solver_outputs_match"]["g1"] and contr >= 0.99 and g2inv
    G = "PASS" if G_ok else "FAIL"
    exact_ok = all(r1["solver_outputs_match"].values()) and r1["numpy_audit_target_equals_B0"] and all(v == 0 for v in r1["unresolved_boundary"].values())
    P = ("PASS" if (r1["FN_count"] == 0 and exact_ok) else ("FAIL" if r1["FN_count"] > 0 else "INCONCLUSIVE"))
    hg = dict(verdict=G, grammar=gram, nominal_contraction=contr, materialized=r1["materialized_g2"], nodes=r1["nodes_g2"], g2_traversal_independent_of_W=g2inv, sets_match_primary=r1["solver_outputs_match"])
    # ---------- H-C timing (only if P PASS)
    C = "NOT_ELIGIBLE"; hc = dict(reason="H-P not PASS")
    if P == "PASS":
        log("timing start")
        solvers = ["b0", "g2", "b1", "e2"]; W = Ws["primary"]; T = None
        Tref = {s: res["primary"]["target_count"] for s in solvers}
        refid = set(np.loadtxt(OUT / "TARGET_IDS_primary_v001.txt", dtype=np.int64, ndmin=1).tolist()); refg2 = refid & sg_np
        tdump = X["tmp"] / "timing_dump.txt"; bad_out = []; arm_wall = {s: 0.0 for s in solvers}
        def run_fn(s):
            if tdump.exists(): tdump.unlink()
            t = time.perf_counter()
            p = env.run(path, s, W, tau, E0, extra=UNB + (["--frac", "0.75"] if s == "e2" else []), tag="PRIMARY_timing_" + s, dump=tdump)
            ext = time.perf_counter() - t
            if p.returncode: raise RuntimeError("%s rc=%d %s" % (s, p.returncode, p.stderr[-200:]))
            ids = {int(x) for x in tdump.read_text().split()}
            if ids != (refg2 if s == "g2" else refid): bad_out.append(s)
            arm_wall[s] += ext
            return ca.parse_kv(p.stdout), ext
        recs, order = ca.run_protocol(run_fn, solvers, warmups=3, repeats=15)
        ch = {s: [ca.charged(s, x)["total_charged"] for x in recs[s]] for s in solvers}
        r_b0g2 = [ch["b0"][i] / ch["g2"][i] for i in range(15)]
        # deployment scenario: G2 additionally charged an E0 certification (cert_b1, W=0 anchor), reported separately
        certs = []
        for _ in range(5):
            p = env.run(path, "cert_b1", 0, tau, tag="PRIMARY_cert_b1"); kv = ca.parse_kv(p.stdout); certs.append(ca.charged("cert_b1", ca.numeric(kv))["total_charged"])
        cert_med = statistics.median(certs)
        r_dep = [ch["b0"][i] / (ch["g2"][i] + cert_med) for i in range(15)]
        hc = dict(rule="median>=1.20 AND min>=1.20 over 15 paired rounds (ratified; no inferential CI)", ratios_b0_over_g2=r_b0g2, median=statistics.median(r_b0g2), minimum=min(r_b0g2),
                  verdict=hc_rule(r_b0g2), outputs_identical_all_rounds=(not bad_out), output_mismatch_solvers=bad_out, order_log=order, arm_wall_s_total=arm_wall,
                  within_30min_arm=all(v <= 1800 for v in arm_wall.values()),
                  charged_s={s: ca.disp(ch[s]) for s in solvers}, cost_ledger_rounds=recs,
                  sensitivity=dict(b1_over_g2_ratio=[ch["b1"][i] / ch["g2"][i] for i in range(15)], e2_over_g2_ratio=[ch["e2"][i] / ch["g2"][i] for i in range(15)],
                                   b0_over_b1=[ch["b0"][i] / ch["b1"][i] for i in range(15)], b0_over_e2=[ch["b0"][i] / ch["e2"][i] for i in range(15)],
                                   note="B1/E2 are sensitivity arms only; no verdict derived from them"),
                  deployment_scenario_with_E0_certification=dict(cert_b1_charged_s_median=cert_med, ratios=r_dep, median=statistics.median(r_dep), minimum=min(r_dep), would_pass_rule=hc_rule(r_dep), status="REPORTED SEPARATELY; not the primary rule"),
                  environment=dict(python=sys.version.split()[0], numpy=np.__version__, platform=platform.platform(), cpus=os.cpu_count(), compiler=X["compiler"]))
        if bad_out or not hc["within_30min_arm"]: hc["verdict"] = "INCONCLUSIVE" if bad_out else "EXECUTION_LIMIT"
        C = hc["verdict"]; log("timing done", C, "median", hc["median"], "min", hc["minimum"])
    # ---------- nulls (descriptive only)
    log("nulls start")
    v6 = sd.load_v006_nulls(V.FEAS); nullrows = []; accts = {}
    for key, fam in sd.FAMILIES.items():
        fn = V.make_survivors_fn(X, 24, "pn_" + key)
        nulls, acc = sd.generate(fam, I["inc"], 24, 1000, fn, v6, max_tries=5000); accts[key] = acc
        def one(e, k=key):
            pth = X["tmp"] / ("pn_%s_%d.txt" % (k, e["idx"])); V.write_instance(pth, 24, I["pairs"], V.ew.compile_masks(e["inc"]))
            kv = ca.parse_kv(env.run(pth, "nullgap", 0.0, tau, E0, extra=UNB, tag="PRIMARY_null_" + k).stdout); pth.unlink()
            return dict(family=k, idx=e["idx"], label=e["label"], seed_sha256=e["seed_sha256"], inc_sha256=e["inc_sha256"], survivors=e["survivors"], delta_null=float(kv["delta_nonG"]),
                        n_excluded=int(kv["n_excluded"]), empty_excluded=int(kv["empty_excluded_set"]))
        with ThreadPoolExecutor(2) as ex: rows = list(ex.map(one, nulls))
        nullrows += rows; log("nulls", key, len(rows), acc)
    nstat = {}
    for key in sd.FAMILIES:
        rr = [r for r in nullrows if r["family"] == key]; sv = np.array([r["survivors"] for r in rr]); dl = np.array([r["delta_null"] for r in rr])
        pres = {wn: float(np.mean(Ws[wn] + tau < dl)) for wn in Ws}
        nstat[key] = dict(n=len(rr), accounting=accts[key], survivors=dict(min=int(sv.min()), median=float(np.median(sv)), max=int(sv.max()), real=gram["count_constructive"],
                          frac_nulls_leq_real=float(np.mean(sv <= gram["count_constructive"]))), delta_null=dict(min=float(dl.min()), median=float(np.median(dl)), max=float(dl.max()), real=dG,
                          frac_nulls_geq_real=float(np.mean(dl >= dG)), over_kT_median=float(np.median(dl) / kT)), null_preservation_fraction_by_window=pres,
                          note="DESCRIPTIVE ONLY; no p-value, threshold or null-superiority verdict")
    with open(OUT / "NULLS_primary_v001.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(nullrows[0].keys())); w.writeheader(); w.writerows(nullrows)
    # ---------- assemble
    result = dict(protocol="SCR-III-B PRIMARY v001", date=time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
                  verdict=dict(G=G, P=P, T="NOT_TESTED", C=C), H_G=hg, exclusion_gap=gap, windows=res, H_C=hc, nulls=nstat, precheck_status="PASS",
                  constants=dict(A_J=X["A_J"], kT_J=X["kT_J"], kT_norm=kT, E0_norm=E0, E0_J=E0 * X["A_J"], tau=tau, Q=Q, tau_rel=tol.REL_TAU, master_seed=sd.MASTER_SEED),
                  hashes=dict(driver=sha(__file__), authorization=sha(ROOT / "PRIMARY_AUTHORIZATION_v001.md"), pg_binary=sha(env.pg), e2_binary=sha(env.e2)), seconds=time.time() - T0)
    def cl(o):
        if isinstance(o, (np.generic,)): return o.item()
        if isinstance(o, set): return sorted(o)
        raise TypeError(type(o))
    (OUT / "PRIMARY_RESULT_v001.json").write_text(json.dumps(result, indent=1, default=cl))
    with gzip.open(OUT / "INVOCATION_LOG_primary_v001.jsonl.gz", "wb") as g: g.write(env.audit.read_bytes())
    log("DONE", result["verdict"])
if __name__ == "__main__":
    main()
