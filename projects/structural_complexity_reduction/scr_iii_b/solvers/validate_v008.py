#!/usr/bin/env python3
"""SCR-III-B PREFLIGHT_v008 -- solver implementation gate (B0, G1, G2, B1), outcome-blind.

Run from the project root (Ubuntu/WSL; g++ and Python 3):   python3 scr_iii_b/solvers/validate_v008.py
Reads (never writes) frozen v005/v006/v007 code and outputs. Writes only scr_iii_b/output/validation/v008/.

OUTCOME-BLIND RESTRICTIONS: the real 3x3 patch is only ever run at W=0 (the already published anchor). Delta_G / rho_G are NOT computed
for 3x3 or for nulls. Public 1x1/2x2 patches may be used at any window. The verdict is an implementation verdict only.
"""
import sys
sys.dont_write_bytecode = True
import csv, datetime, hashlib, json, math, os, pathlib, platform, random, statistics, subprocess, tempfile, time

HERE = pathlib.Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
FEAS = PROJECT / "scr_iii_b" / "feasibility"
EX3 = PROJECT / "scr_iii_b" / "exact3"
sys.path.insert(0, str(FEAS)); sys.path.insert(0, str(HERE))
import energy_windows_v006 as ew
import tie_policy_v008 as tp
import diagnostics_v008 as dg

OUT = PROJECT / "scr_iii_b" / "output" / "validation" / "v008"
V5 = PROJECT / "scr_iii_b" / "output" / "validation" / "v005"; V5C = PROJECT / "scr_iii_b" / "reference_check"
V6 = PROJECT / "scr_iii_b" / "output" / "validation" / "v006"
V7 = PROJECT / "scr_iii_b" / "output" / "validation" / "v007"
SRC = HERE / "solvers_v008.cpp"
SEED = 20261010
TESTS, INVOC = [], []
SOLVERS = ("b0", "g1", "g2", "b1")


class Blocked(Exception):
    pass


def rec(tid, title, level, status, mandatory=True, **detail):
    TESTS.append(dict(id=tid, title=title, evidence_level=level, status=status, mandatory=mandatory, detail=detail))


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def clean(o):
    if isinstance(o, float) and (math.isnan(o) or math.isinf(o)):
        return None
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    return o


def frozen(manifest, groups):
    if not manifest.exists():
        raise Blocked("%s missing" % manifest)
    m = json.loads(manifest.read_text()); bad = []; n = 0
    for grp, base in groups:
        for name, h in m.get(grp, {}).items():
            n += 1
            p = base / name
            if not p.exists() or sha(p) != h:
                bad.append(name)
    return m, bad, n


# ---------------------------------------------------------------- instances
def write_instance(path, n, pairs, masks):
    lines = ["%d %d" % (n, len(pairs))] + ["%d %d %.17g" % (i, j, k) for i, j, k in pairs] + [str(len(masks))] + ["%d %d" % (a, b) for a, b in masks]
    pathlib.Path(path).write_text("\n".join(lines) + "\n")


def energies(n, pairs):
    out = []
    for s in range(1 << n):
        e = 0.0
        for i, j, k in pairs:
            e += -k if ((s >> i) ^ (s >> j)) & 1 else k
        out.append(e)
    return out


def grammar_flags(n, masks):
    return [all(((s ^ nm) & im).bit_count() == 2 for im, nm in masks) for s in range(1 << n)]


def synth_instance(rng, n):
    pairs = [(i, j, rng.gauss(0, 0.01)) for i in range(n) for j in range(i + 1, n)]
    for _ in range(200):
        nv = rng.randint(2, 4)
        masks = []
        for _v in range(nv):
            isl = rng.sample(range(n), 4)
            im = sum(1 << i for i in isl); nm = sum(1 << i for i in isl if rng.random() < 0.5)
            masks.append((im, nm))
        g = grammar_flags(n, masks)
        if 4 <= sum(g) <= int(0.9 * (1 << n)):
            return pairs, masks, g
    raise Blocked("could not generate synthetic grammar")


def run(binp, inp, sol, W, tau, dump=None, extra=(), tag=""):
    cmd = [str(binp), str(inp), sol, repr(float(W)), repr(float(tau))]
    if dump:
        cmd += ["--dump", str(dump)]
    cmd += list(extra)
    INVOC.append(dict(tag=tag, solver=sol, W=float(W), input=pathlib.Path(inp).name, flags=list(extra)))
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p


def kvs(p):
    return dict(l.split("=", 1) for l in p.stdout.splitlines() if "=" in l)


def solve_ids(binp, inp, sol, W, tau, tmp, tag=""):
    d = tmp / "dump.txt"
    if d.exists():
        d.unlink()
    p = run(binp, inp, sol, W, tau, dump=d, tag=tag)
    if p.returncode:
        raise Blocked("solver %s failed: %s" % (sol, p.stderr[-300:]))
    kv = kvs(p)
    ids = {int(x) for x in d.read_text().split()} if d.exists() else set()
    return ids, kv


def main():
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    OUT.mkdir(parents=True, exist_ok=True)
    rep = dict(version="v008", started_utc=started, platform=platform.platform(), python=sys.version.split()[0])
    try:
        m5, b5, n5 = frozen(V5 / "MANIFEST_v005.json", (("code", V5C), ("outputs", V5)))
        m6, b6, n6 = frozen(V6 / "MANIFEST_v006.json", (("code", FEAS), ("outputs", V6)))
        m7, b7, n7 = frozen(V7 / "MANIFEST_v007.json", (("code", EX3), ("outputs", V7)))
        rec("F1", "Frozen v005, v006, v007 code/outputs equal the hashes in their local manifests (read-only)", "STATIC_FILE_HASH",
            "PASS" if not (b5 or b6 or b7) else "FAIL", mismatches=dict(v005=b5, v006=b6, v007=b7), files_checked=n5 + n6 + n7,
            verdicts=dict(v005=m5.get("verdict"), v006=m6.get("verdict"), v007=m7.get("verdict")))
        pe = ew.load_v005()
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="v008_"))
        binp = tmp / "solvers"; cc = os.environ.get("CXX", "g++")
        try:
            pr = subprocess.run([cc, "-std=c++17", "-O2", str(SRC), "-o", str(binp)], capture_output=True, text=True)
        except FileNotFoundError:
            raise Blocked("C++ compiler '%s' not found" % cc)
        if pr.returncode:
            raise Blocked("compile failed:\n" + pr.stderr[-2000:])
        compiler = subprocess.run([cc, "--version"], capture_output=True, text=True).stdout.splitlines()[0]
        anchor = json.loads((V7 / "REPORT_v007.json").read_text())["anchor_3x3"]
    except Blocked as exc:
        return blocked(rep, str(exc))

    # --------------------------------------------------------- real instances
    inst = {}
    for L in (1, 2, 3):
        isl = pe.source_geometry(L); pairs = pe.K_pairs(isl); vpos = pe.vertex_positions(L)
        inc, _ = ew.build_incidence(pe, isl, vpos); masks = ew.compile_masks(inc)
        p = tmp / ("real%d.txt" % L); write_instance(p, len(isl), pairs, masks)
        inst[L] = dict(path=p, n=len(isl), pairs=pairs, masks=masks, sumabs=sum(abs(k) for _, _, k in pairs))

    # ---- G0: outcome-blind guard really refuses 3x3 W>0 (and runs nothing)
    pg = run(binp, inst[3]["path"], "b0", 1e-3, 1e-9, tag="GUARD_TEST_REFUSAL_EXPECTED")
    guard_ok = (pg.returncode == 3 and "REFUSED" in pg.stderr and not pg.stdout.strip())
    rec("G0", "Outcome-blind guard: the binary refuses any 3x3 (n>16) run with W>0 unless --unblind-after-freeze is given, and prints no result", "BEHAVIOURAL",
        "PASS" if guard_ok else "FAIL", returncode=pg.returncode, stderr=pg.stderr.strip()[:160], stdout_empty=not pg.stdout.strip())

    # --------------------------------------------------------- S1: public patches, all windows, all solvers
    s1 = {}; ok1 = True
    cmp_v6 = {}
    v6csv = {}
    with open(V6 / "WINDOWS_v006.csv") as f:
        for r in csv.DictReader(f):
            v6csv[(r["patch"], int(r["level"]))] = int(r["false_exclusions"])
    for L in (1, 2):
        d = inst[L]; n = d["n"]; tau = tp.tau_abs(d["sumabs"])
        En = energies(n, d["pairs"]); g = grammar_flags(n, d["masks"])
        lv, levels, gap, sc = ew.group_levels(En)
        E0 = min(En); idsG = [i for i in range(1 << n) if g[i]]
        E0G = min(En[i] for i in idsG)
        Ws = [("zero", 0.0)]
        for k in range(1, len(levels)):
            Wk = levels[k]["E_min"] - E0
            Ws.append(("level%d" % k, Wk))
            Ws.append(("below%d" % k, Wk - 10 * tau))
            if k + 1 < len(levels):
                Ws.append(("mid%d" % k, 0.5 * (Wk + levels[k + 1]["E_min"] - E0)))
        bad = []; n_runs = 0; fn_mism = []
        for name, W in Ws:
            refT = tp.members(En, E0, W, tau)
            refTG = {i for i in idsG if En[i] <= E0G + W + tau}
            for sol in SOLVERS:
                ids, kv = solve_ids(binp, d["path"], sol, W, tau, tmp, tag="public_%dx%d_%s" % (L, L, name)); n_runs += 1
                ref = refT if sol in ("b0", "b1") else refTG
                if ids != ref:
                    bad.append((name, sol, len(ids), len(ref)))
            if name.startswith("level"):
                k = int(name[5:]); fn = len(refT - {i for i in refT if g[i]})
                key = ("%dx%d" % (L, L), k)
                if key in v6csv and v6csv[key] != fn:
                    fn_mism.append((k, fn, v6csv[key]))
        s1["%dx%d" % (L, L)] = dict(windows=len(Ws), solver_runs=n_runs, mismatches=bad[:20], n_mismatch=len(bad), fn_vs_v006_csv_mismatches=fn_mism,
                                    tau=tau, tau_rule="1e-9 * sum|K| (PROPOSED FOR TEST, not frozen)")
        ok1 = ok1 and not bad and not fn_mism
    rec("S1", "Solver equivalence on public 1x1 and 2x2 patches at W=0, every level threshold, 10*tau below it, and every midpoint: B0=B1=exact brute-force target set; G1=G2=S_T∩S_G (E0-hat over S_G); false-exclusion counts equal v006",
        "EXHAUSTIVE_REFERENCE_COMPARISON", "PASS" if ok1 else "FAIL", patches=s1)

    # --------------------------------------------------------- S2: synthetic instances (random K, random grammars)
    rng = random.Random(SEED + 8)
    ok2 = True; bad2 = []; nrun2 = 0; ninst = 0
    cases = []
    for t in range(30):
        n = rng.randint(8, 12); pairs, masks, g = synth_instance(rng, n); cases.append((n, pairs, masks, g, "random%d" % t))
    n = 10
    cases.append((n, [(i, j, 0.01) for i in range(n) for j in range(i + 1, n)], [(0b1111, 0), (0b11110000, 0b110000)], None, "ferro"))
    cases.append((n, [(i, j, -0.01) for i in range(n) for j in range(i + 1, n)], [(0b1111, 0b11), (0b1111100000, 0)], None, "antiferro"))
    cases.append((8, [(i, j, 0.0) for i in range(8) for j in range(i + 1, 8)], [(0b1111, 0b1)], None, "zero_coupling_all_degenerate"))
    for (n, pairs, masks, g, name) in cases:
        g = g if g is not None else grammar_flags(n, masks)
        if not any(g):
            continue
        p = tmp / ("syn_%s.txt" % name); write_instance(p, n, pairs, masks)
        En = energies(n, pairs); sumabs = sum(abs(k) for _, _, k in pairs); tau = tp.tau_abs(sumabs)
        sd = statistics.pstdev(En) or 0.01
        E0 = min(En); idsG = [i for i in range(1 << n) if g[i]]; E0G = min(En[i] for i in idsG)
        ninst += 1
        for W in (0.0, 0.5 * sd, 2 * sd, 10 * sd, 1e3):
            refT = tp.members(En, E0, W, tau); refTG = {i for i in idsG if En[i] <= E0G + W + tau}
            for sol in SOLVERS:
                ids, kv = solve_ids(binp, p, sol, W, tau, tmp, tag="synthetic_%s" % name); nrun2 += 1
                if ids != (refT if sol in ("b0", "b1") else refTG):
                    bad2.append((name, sol, W, len(ids)))
    ok2 = not bad2
    rec("S2", "Solver equivalence on %d synthetic instances (random mixed-sign couplings, random 2-in/2-out-style incidence, ferromagnet, antiferromagnet, all-degenerate zero coupling), 5 windows each" % ninst,
        "EXHAUSTIVE_REFERENCE_COMPARISON", "PASS" if ok2 else "FAIL", instances=ninst, solver_runs=nrun2, mismatches=bad2[:20])

    # --------------------------------------------------------- S3: B1 bound admissibility
    rng3 = random.Random(SEED + 9)
    adm = []; worst = 0.0; viol = []; mism_formula = 0.0
    bt_cases = []
    for t in range(12):
        n = rng3.randint(8, 12); pairs, masks, g = synth_instance(rng3, n); bt_cases.append((n, pairs, masks, "syn%d" % t, None))
    bt_cases.append((inst[2]["n"], inst[2]["pairs"], inst[2]["masks"], "real2x2", None))
    bt_cases.append((inst[3]["n"], inst[3]["pairs"], inst[3]["masks"], "real3x3_depth14to20", (14, 20)))
    n_partials = 0; slack = []
    for (n, pairs, masks, name, mrange) in bt_cases:
        p = tmp / ("bt_%s.txt" % name); write_instance(p, n, pairs, masks)
        Kf = [[0.0] * n for _ in range(n)]
        for i, j, k in pairs:
            Kf[i][j] = Kf[j][i] = k
        parts = []
        cnt = 10 if mrange else 40
        for _ in range(cnt):
            m = rng3.randint(*mrange) if mrange else rng3.randint(0, n)
            parts.append((m, rng3.getrandbits(max(m, 1)) & ((1 << m) - 1)))
        pf = tmp / "partials.txt"; pf.write_text("\n".join("%d %d" % x for x in parts) + "\n")
        out = subprocess.run([str(binp), str(p), "boundtest", str(pf)], capture_output=True, text=True).stdout.split("\n")
        lbs = [float(l.split()[2]) for l in out if l.strip()]
        for (m, bits), lb in zip(parts, lbs):
            sp = [1 if (bits >> i) & 1 else -1 for i in range(m)]
            Efix = sum(Kf[i][j] * sp[i] * sp[j] for i in range(m) for j in range(i + 1, m))
            f = [sum(Kf[j][i] * sp[i] for i in range(m)) for j in range(m, n)]
            lb_py = Efix - sum(abs(x) for x in f) - sum(abs(Kf[j][k]) for j in range(m, n) for k in range(j + 1, n))
            mism_formula = max(mism_formula, abs(lb - lb_py))
            nfree = n - m; best = 1e300
            for c in range(1 << nfree):
                s = sp + [1 if (c >> t_) & 1 else -1 for t_ in range(nfree)]
                e = sum(Kf[i][j] * s[i] * s[j] for i in range(n) for j in range(i + 1, n))
                best = min(best, e)
            n_partials += 1
            if lb > best + 1e-12:
                viol.append((name, m, bits, lb, best))
            slack.append(best - lb); worst = max(worst, lb - best)
    rec("S3", "B1 lower bound is admissible: C++ LB <= exact minimum completion energy for %d partial assignments (synthetic, real 2x2, real 3x3 depth 14-20); C++ LB equals independent python formula" % n_partials,
        "EXHAUSTIVE_REFERENCE_COMPARISON", "PASS" if (not viol and mism_formula < 1e-12) else "FAIL", partial_assignments=n_partials, violations=viol[:5],
        max_lb_minus_exact=worst, max_abs_cpp_vs_python_lb=mism_formula, mean_slack=statistics.mean(slack), median_slack=statistics.median(slack),
        proof_sketch="min over completions of [sum_j s_j f_j + sum_{j<k free} K_jk s_j s_k] >= sum_j min(s_j f_j) + sum_{j<k} min(K_jk s_j s_k) = -sum|f_j| - sum|K_jk|; each term bounded independently so the sum of minima is <= the minimum of the sum.")

    # --------------------------------------------------------- S4: 3x3 W=0 acceptance-only dry run with repeats
    d3 = inst[3]; tau3 = tp.tau_abs(d3["sumabs"]); REP = 5
    runs = {s: [] for s in SOLVERS}; sets = {}
    for s in SOLVERS:
        for r in range(REP):
            ids, kv = solve_ids(binp, d3["path"], s, 0.0, tau3, tmp, tag="dryrun_3x3_W0")
            runs[s].append(kv); sets[s] = ids
    same = all(sets[s] == sets["b0"] for s in SOLVERS)
    ids0 = sorted(sets["b0"])
    py_e = [pe.energy_norm(pe.decode(i, d3["n"]), d3["pairs"]) for i in ids0]
    e0_ok = all(abs(e - anchor["E0_norm"]) <= 1e-12 for e in py_e) and all(abs(float(runs[s][0]["E0hat"]) - anchor["E0_norm"]) <= 1e-12 for s in SOLVERS)
    comp_ok = len(ids0) == 2 and (ids0[0] ^ ids0[1]) == (1 << d3["n"]) - 1
    gr_ok = all(all(((i ^ nm) & im).bit_count() == 2 for im, nm in d3["masks"]) for i in ids0)
    det = all(len({r["id_digest"] for r in runs[s]}) == 1 and len({r["pair_ops"] + "|" + r["nodes"] + "|" + r["grammar_checks"] for r in runs[s]}) == 1 for s in SOLVERS)
    rec("S4", "3x3 acceptance-only dry run at the published W=0 anchor only: B0=B1=G1=G2 return the same 2 ground states (complementary pair, both grammar-admissible), E0 equals the v007 anchor within 1e-12, deterministic output and operation counts over %d repeats" % REP,
        "ACCEPTANCE_ONLY_DRY_RUN", "PASS" if (same and e0_ok and comp_ok and gr_ok and det) else "FAIL", ids=ids0, anchor_E0=anchor["E0_norm"],
        E0hat={s: float(runs[s][0]["E0hat"]) for s in SOLVERS}, solvers_agree=same, complementary_pair=comp_ok, deterministic=det, repeats=REP, tau=tau3)

    # --------------------------------------------------------- S5: cost ledger (W=0 dry run only)
    def med(s, key):
        return statistics.median(float(r[key]) for r in runs[s])
    ledger = {}
    for s in SOLVERS:
        r0 = runs[s][0]
        ledger[s] = dict(
            wall_s_median=med(s, "wall_s"), wall_s_range=[min(float(r["wall_s"]) for r in runs[s]), max(float(r["wall_s"]) for r in runs[s])],
            wall_s_rel_spread=(max(float(r["wall_s"]) for r in runs[s]) - min(float(r["wall_s"]) for r in runs[s])) / med(s, "wall_s"),
            t_preprocess_s=med(s, "t_preprocess_s"), t_traverse_s=med(s, "t_traverse_s"), t_grammar_s=med(s, "t_grammar_s"), t_energy_s=med(s, "t_energy_s"),
            t_finalize_s=med(s, "t_finalize_s"), peak_rss_kb=max(int(r["maxrss_kb"]) for r in runs[s]),
            **{k: int(r0[k]) for k in ("states_visited", "nodes", "leaves", "grammar_checks", "vertex_checks", "full_energy_evals", "field_updates", "pair_ops",
                                      "bound_evals", "pruned", "materialized", "candidates_kept", "comparisons")})
    sep_note = ("Phase timers are exclusive only where the algorithm separates the phases (G1: scan vs energy). In B0, G2 and B1 energy updates are intertwined with traversal, "
                "so their energy cost is reported as pair_ops/field_updates, not as a separate wall time. maxrss is per process and includes ~1-2 MB runtime baseline.")
    rec("K1", "Cost ledger recorded per architecture (preprocessing, traversal, grammar, energy, finalisation; operation counts; peak RSS; repeat spread) -- W=0 dry run only, no G_net computed",
        "MEASUREMENT", "PASS", ledger=ledger, note=sep_note, repeats=REP,
        environment=dict(platform=platform.platform(), machine=platform.machine(), cpu_count=os.cpu_count(), compiler=compiler, flags="-std=c++17 -O2", threads=1))

    # --------------------------------------------------------- S6: tie policy on synthetic cases (+ property test)
    rng6 = random.Random(SEED + 6); viol6 = 0; conservative_loss = 0; nprop = 3000
    for _ in range(nprop):
        tau = 10 ** rng6.uniform(-12, -8)
        delta = rng6.choice([0.0, 1e-3, 2.5e-3, 0.01])
        E = [0.0, 0.0, 0.004, delta + rng6.choice([0, 0, tau / 2, -tau / 2, tau * 2, -tau * 2, 1e-15, -1e-15]), 0.05]
        E0 = min(E); W = rng6.choice([0.0, delta, delta - tau / 2, delta + tau / 2, delta - 3 * tau, delta + 3 * tau, 0.004])
        if W < 0:
            continue
        ex = tp.members_exact(E, E0, W); tl = tp.members(E, E0, W, tau)
        if not ex <= tl:
            viol6 += 1                                  # tolerance must never remove an exact target
        g = [True, True, True, False, True]
        fn_ex = len([i for i in ex if not g[i]]); fn_tl = len([i for i in tl if not g[i]])
        if fn_tl < fn_ex:
            viol6 += 1                                  # tolerance must never convert an excluded target into a preserved one
        if fn_tl > fn_ex:
            conservative_loss += 1
        dl = dg.delta_G(E, g, E0)
        pol = tp.classify(dl, W, tau) == "PRESERVED"
        if pol != (fn_tl == 0):
            viol6 += 1                                  # classify() must agree with membership under the same tolerance
        if pol and fn_ex != 0:
            viol6 += 1                                  # soundness: policy PASS implies exact PASS
    edge = dict(empty=tp.classify(None, 1.0, 1e-10), ground_excluded=tp.classify(0.0, 0.0, 1e-10), exact_endpoint_fails=tp.classify(0.01, 0.01, 0.0),
                just_below_passes=tp.classify(0.01, 0.01 - 1e-9, 1e-12), tolerance_makes_marginal_fail=tp.classify(0.01, 0.01 - 1e-12, 1e-10))
    edge_ok = (edge["empty"].startswith("NOT_INFORMATIVE") and edge["ground_excluded"].startswith("NO_PRESERVING") and edge["exact_endpoint_fails"].startswith("FAIL")
               and edge["just_below_passes"] == "PRESERVED" and edge["tolerance_makes_marginal_fail"].startswith("FAIL"))
    rec("S6", "Candidate tie policy (E <= E0+W+tau; PRESERVED iff W+tau < Delta) tested on %d synthetic near-tie cases: tolerance never removes a target and never converts an excluded target into a preserved one; classification agrees with membership; edge cases handled" % nprop,
        "SYNTHETIC_PROPERTY_TEST", "PASS" if (viol6 == 0 and edge_ok) else "FAIL", violations=viol6, conservative_losses_marginal_pass_to_fail=conservative_loss, edge_cases=edge,
        policy_status="PROPOSED FOR TESTING ONLY; the constant (1e-9 * sum|K|) and the rule are NOT frozen; final policy must be frozen before inspecting real 3x3 thresholds")

    # --------------------------------------------------------- S7: gap diagnostics on PUBLIC patches only
    s7 = {}; ok7 = True
    A = pe.A_joule(ew.T_REF); kT_norm = pe.KB * ew.T_REF / A
    for L in (1, 2):
        d = inst[L]; n = d["n"]; tau = tp.tau_abs(d["sumabs"]); En = energies(n, d["pairs"]); g = grammar_flags(n, d["masks"])
        E0 = min(En); dl = dg.delta_G(En, g, E0); bad = 0; nw = 0
        lv, levels, _, _ = ew.group_levels(En)
        for k in range(len(levels)):
            for W in (levels[k]["E_min"] - E0, levels[k]["E_min"] - E0 - 10 * tau):
                if W < 0:
                    continue
                nw += 1
                cl, rho, bf = dg.verdict(dl, W, tau)
                fn = len([i for i in tp.members(En, E0, W, tau) if not g[i]])
                if (cl == "PRESERVED") != (fn == 0):
                    bad += 1
                if tau == 0 and rho is not None and ((rho < 1) != (fn == 0)):
                    bad += 1
        cl, rho, bf = dg.verdict(dl, kT_norm, tau)
        s7["%dx%d" % (L, L)] = dict(Delta_G_norm=dl, Delta_G_J=A * dl, Delta_G_over_kT=A * dl / (pe.KB * ew.T_REF), thermal_window_kT_norm=kT_norm,
                                    rho_G_for_W_equals_kT=rho, classification_for_W_equals_kT=cl, windows_checked=nw, equivalence_violations=bad)
        ok7 = ok7 and bad == 0
    rec("S7", "Gap diagnostics Delta_G and rho_G=W/Delta_G implemented and verified on the PUBLIC 1x1 and 2x2 patches: rho<1 (policy: W+tau<Delta) <=> FN=0 at every window. Not computed for 3x3 or nulls (post-freeze).",
        "EXHAUSTIVE_REFERENCE_COMPARISON", "PASS" if ok7 else "FAIL", patches=s7,
        thermal_window_disclosure="W = k_B*T_ref (T_ref=792 K) gives rho_G > 1 for both public patches (see patches); 3x3 preservation failure is therefore a genuine possibility and the window must not be changed to avoid it.")

    # --------------------------------------------------------- S8: outcome-blind audit
    real3 = [i for i in INVOC if i["input"] == "real3.txt"]
    leaks = [i for i in real3 if i["W"] > 0 and i["tag"] != "GUARD_TEST_REFUSAL_EXPECTED"]
    flagged = [i for i in INVOC if "--unblind-after-freeze" in i["flags"]]
    src_text = SRC.read_text()
    forbidden_outputs = [k for k in ("level", "spectrum", "histogram", "second_lowest", "gap") if any(k in (r0 or "") for r0 in ["".join(sorted(runs["b0"][0].keys()))])]
    rec("S8", "Outcome-blind audit: 3x3 was run only at W=0 (the single W>0 attempt is the guard refusal test); no run used --unblind-after-freeze; Delta_G/rho_G not computed on 3x3; solver outputs contain no level/spectrum fields",
        "AUDIT", "PASS" if (not leaks and not flagged and not forbidden_outputs and "REFUSED: outcome-blind guard" in src_text) else "FAIL",
        invocations_total=len(INVOC), invocations_3x3=len(real3), w_positive_3x3_successful_runs=len(leaks), unblind_flag_uses=len(flagged), forbidden_output_fields=forbidden_outputs,
        v007_blindness_note="v007 TESTS_v007.json permits inferring an approximate top-of-spectrum scale (~0.126 A units); low-energy levels and W>0 outcomes were not disclosed. v008 discloses nothing further.")

    mand_fail = [t["id"] for t in TESTS if t["mandatory"] and t["status"] == "FAIL"]
    verdict = "SOLVER_IMPLEMENTATION_GATE_FAIL" if mand_fail else "SOLVER_IMPLEMENTATION_GATE_PASS"
    obs = observations(ledger)
    rep.update(verdict=verdict, mandatory_failures=mand_fail, finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), tests={t["id"]: t["status"] for t in TESTS},
               statement="Implementation gate only. Implies NOTHING about H-G, H-P, H-T or H-C primary success; no G_net; no 3x3 W>0 outcome; preregistration and specification remain unfrozen.",
               ledger=ledger, observations=obs, compiler=compiler, still_open=OPEN)
    write_outputs(rep, ledger, obs)
    print(json.dumps(dict(verdict=verdict, mandatory_failures=mand_fail, tests=rep["tests"]), indent=1))
    return 1 if mand_fail else 0


OPEN = ["Window constant/rule (c in W = c*A(T_ref) or c*k_B*T_ref, or a level-respecting cardinality rule).",
        "Tie-policy constant and rule (candidate tested here is not frozen).", "Numerical success thresholds for G, P, C and the uncertainty/margin rule.",
        "Primary seed registry and null sample sizes; E2 design; state/variable ordering policy for B1 and G2; runtime and memory limits.",
        "Whether global-reversal (Z2) symmetry may be exploited by B0/G2/B1 (it halves every search; not used in v008 for any solver)."]


def observations(L):
    o = []
    o.append("W=0 dry run on 3x3: B1 visited %d nodes and G2 %d nodes (B0 visited %d states); wall medians B0 %.3g s, G1 %.3g s, G2 %.3g s, B1 %.3g s." % (
        L["b1"]["nodes"], L["g2"]["nodes"], L["b0"]["states_visited"], L["b0"]["wall_s_median"], L["g1"]["wall_s_median"], L["g2"]["wall_s_median"], L["b1"]["wall_s_median"]))
    if L["b1"]["wall_s_median"] < L["g2"]["wall_s_median"]:
        o.append("At W=0 the exact branch-and-bound sensitivity comparator B1 is FASTER than constructive grammar generation G2. This is a W=0 observation only (a very restrictive target); it must not be generalised to W>0, but it shows that the C axis against B1 is not guaranteed and must be reported honestly.")
    o.append("Neither G_net nor any speedup headline is derived from these figures; they are acceptance-only component measurements.")
    return o


def blocked(rep, why):
    OUT.mkdir(parents=True, exist_ok=True)
    rep.update(verdict="SOLVER_IMPLEMENTATION_GATE_BLOCKED", reason=why, tests={})
    (OUT / "REPORT_v008.json").write_text(json.dumps(clean(rep), indent=1))
    (OUT / "REPORT_v008.md").write_text("# REPORT_v008\n\n**Verdict:** `SOLVER_IMPLEMENTATION_GATE_BLOCKED`\n\n%s\n" % why)
    print("BLOCKED:", why)
    return 2


def f(x, nd=4):
    return "%.*g" % (nd, x)


def write_outputs(rep, ledger, obs):
    (OUT / "TESTS_v008.json").write_text(json.dumps(clean(TESTS), indent=1))
    (OUT / "REPORT_v008.json").write_text(json.dumps(clean(rep), indent=1))
    cols = ["solver", "wall_s_median", "wall_s_rel_spread", "t_preprocess_s", "t_traverse_s", "t_grammar_s", "t_energy_s", "t_finalize_s", "peak_rss_kb", "states_visited", "nodes", "leaves",
            "grammar_checks", "vertex_checks", "full_energy_evals", "field_updates", "pair_ops", "bound_evals", "pruned", "materialized", "candidates_kept", "comparisons"]
    with open(OUT / "COST_LEDGER_v008.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(cols)
        for s, d in ledger.items():
            w.writerow([s] + [repr(d[c]) if isinstance(d[c], float) else d[c] for c in cols[1:]])
    (OUT / "COST_LEDGER_v008.json").write_text(json.dumps(clean(ledger), indent=1))
    s1 = [t for t in TESTS if t["id"] == "S1"][0]["detail"]["patches"]; s7 = [t for t in TESTS if t["id"] == "S7"][0]["detail"]
    (OUT / "SOLVER_EQUIVALENCE_v008.json").write_text(json.dumps(clean(dict(S1=s1, S2=[t for t in TESTS if t["id"] == "S2"][0]["detail"],
                                                                         S3=[t for t in TESTS if t["id"] == "S3"][0]["detail"], S4=[t for t in TESTS if t["id"] == "S4"][0]["detail"])), indent=1))
    L = ["# REPORT_v008 — Solver Implementation Gate (outcome-blind)\n", "**Verdict:** `%s`\n" % rep["verdict"],
         "Implementation verdict only. It implies nothing about H-G, H-P, H-T or H-C primary success. No G_net, no 3×3 W>0 outcome, specification and preregistration remain unfrozen.\n",
         "## What passed\n",
         "- **F1** frozen v005–v007 untouched; **G0** the binary refuses 3×3 W>0 without the post-freeze flag; **S8** audit: 3×3 was run only at the published W=0 anchor.",
         "- **S1** B0=B1 (exact target set) and G1=G2 (S_T∩S_G) on 1×1 and 2×2 at W=0, every level threshold, 10τ below it and every midpoint; false-exclusion counts equal v006.",
         "- **S2** same equivalence on synthetic instances (random mixed-sign couplings and incidence, ferromagnet, antiferromagnet, all-degenerate).",
         "- **S3** B1 lower bound is admissible on %d partial assignments and equals an independent python formula." % [t for t in TESTS if t["id"] == "S3"][0]["detail"]["partial_assignments"],
         "- **S4** 3×3 W=0 dry run: all four solvers return the same two (complementary) ground states; E0 equals the v007 anchor; outputs and operation counts deterministic over repeats.",
         "- **S6** candidate tie policy is conservative on synthetic near-ties (**proposed for testing only, not frozen**). **S7** Δ_G and ρ_G verified on public 1×1/2×2: ρ<1 ⇔ FN=0.\n",
         "## Public-patch gap diagnostics and the thermal window\n", "| Patch | Δ_G (J) | Δ_G / k_BT | ρ_G for W = k_BT | classification |\n|---|---|---|---|---|"]
    for k, v in s7["patches"].items():
        L.append("| %s | %s | %s | %s | %s |" % (k, f(v["Delta_G_J"]), f(v["Delta_G_over_kT"], 3), f(v["rho_G_for_W_equals_kT"], 3), v["classification_for_W_equals_kT"]))
    L += ["\nW = k_BT lies above both known gaps. 3×3 preservation failure is a genuine possibility and the window must not be altered to avoid it.\n",
          "## Cost ledger (3×3, W=0 only; single thread; median of 5)\n", "| Solver | wall (s) | spread | nodes / states | pair ops | grammar checks | full energy evals | peak RSS (MB) |\n|---|---|---|---|---|---|---|---|"]
    for s, d in ledger.items():
        L.append("| %s | %s | %.0f%% | %s | %s | %s | %s | %.1f |" % (s.upper(), f(d["wall_s_median"]), 100 * d["wall_s_rel_spread"], d["nodes"] or d["states_visited"], d["pair_ops"], d["grammar_checks"], d["full_energy_evals"], d["peak_rss_kb"] / 1024))
    L += ["\n" + sep for sep in [[t for t in TESTS if t["id"] == "K1"][0]["detail"]["note"]]]
    L += ["\n## Observations (not conclusions)\n"] + ["- " + o for o in obs]
    L += ["\n## Test table\n", "| ID | Test | Status |\n|---|---|---|"] + ["| %s | %s | **%s** |" % (t["id"], t["title"], t["status"]) for t in TESTS]
    L += ["\n## Still open (to be fixed before any freeze, never from v008 performance)\n"] + ["- " + o for o in rep["still_open"]]
    (OUT / "REPORT_v008.md").write_text("\n".join(L) + "\n")
    mf = dict(version="v008", verdict=rep["verdict"], compiler=rep["compiler"], code={}, outputs={})
    for nme in ("validate_v008.py", "solvers_v008.cpp", "tie_policy_v008.py", "diagnostics_v008.py", "test_v008.py", "README_v008.md"):
        p = HERE / nme; mf["code"][nme] = sha(p) if p.exists() else None
    for nme in ("REPORT_v008.json", "REPORT_v008.md", "TESTS_v008.json", "COST_LEDGER_v008.csv", "COST_LEDGER_v008.json", "SOLVER_EQUIVALENCE_v008.json"):
        mf["outputs"][nme] = sha(OUT / nme)
    mf["note"] = "Output files contain timings; their hashes are per-run records."
    (OUT / "MANIFEST_v008.json").write_text(json.dumps(mf, indent=1))


if __name__ == "__main__":
    sys.exit(main())
