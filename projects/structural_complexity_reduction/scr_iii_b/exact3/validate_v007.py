#!/usr/bin/env python3
"""SCR-III-B PREFLIGHT_v007 -- 3x3 exact-verification feasibility and solver-selection gate.

Run from the project root (Ubuntu/WSL, needs g++ and Python 3):   python3 scr_iii_b/exact3/validate_v007.py
Reads (never writes) frozen v005/v006 code and outputs. Writes only scr_iii_b/output/validation/v007/. No primary experiment is run.

Design rule (spec: do not tune on 3x3 target outcomes): the 3x3 space is scanned COMPLETELY (all 2^24 states), but the report
discloses only the prereg-neutral W=0 anchor and correctness/cost data -- not the 3x3 energy-level spectrum or any window outcome.
"""
import sys
sys.dont_write_bytecode = True
import datetime, hashlib, json, math, os, pathlib, platform, random, subprocess, tempfile, time

HERE = pathlib.Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
FEAS = PROJECT / "scr_iii_b" / "feasibility"
sys.path.insert(0, str(FEAS))
import energy_windows_v006 as ew            # frozen v006 module, imported read-only

OUT = PROJECT / "scr_iii_b" / "output" / "validation" / "v007"
V5_OUT = PROJECT / "scr_iii_b" / "output" / "validation" / "v005"
V5_CODE = PROJECT / "scr_iii_b" / "reference_check"
V6_OUT = PROJECT / "scr_iii_b" / "output" / "validation" / "v006"
SRC = HERE / "verify3_v007.cpp"
SEED = 20261010
TESTS = []


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


def frozen_check(tag, manifest, groups):
    if not manifest.exists():
        raise Blocked("%s not found" % manifest)
    m = json.loads(manifest.read_text())
    bad, n = [], 0
    for grp, base in groups:
        for name, h in m.get(grp, {}).items():
            n += 1
            p = base / name
            if not p.exists() or sha(p) != h:
                bad.append(name)
    return m, bad, n


def make_input(pe, L):
    isl = pe.source_geometry(L); pairs = pe.K_pairs(isl); vpos = pe.vertex_positions(L)
    inc, roles = ew.build_incidence(pe, isl, vpos); masks = ew.compile_masks(inc)
    lines = ["%d %d" % (len(isl), len(pairs))]
    lines += ["%d %d %.17g" % (i, j, k) for i, j, k in pairs]
    lines.append(str(len(masks)))
    lines += ["%d %d" % (im, nm) for im, nm in masks]
    return "\n".join(lines) + "\n", isl, pairs, inc, masks


def run(cmd, timeout=3000):
    t0 = time.perf_counter()
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    if p.returncode:
        raise Blocked("verifier failed: %s\n%s" % (cmd, p.stderr[-500:]))
    kv, wins = {}, []
    for ln in p.stdout.splitlines():
        if ln.startswith("window "):
            _, k, w, t, fn = ln.split()
            wins.append((int(k), float(w), int(t), int(fn)))
        elif "=" in ln:
            a, b = ln.split("=", 1); kv[a] = b
    return kv, wins, time.perf_counter() - t0, p.stdout


def main():
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    OUT.mkdir(parents=True, exist_ok=True)
    rep = dict(version="v007", started_utc=started, platform=platform.platform(), python=sys.version.split()[0])
    try:
        m5, bad5, n5 = frozen_check("v005", V5_OUT / "MANIFEST_v005.json", (("code", V5_CODE), ("outputs", V5_OUT)))
        m6, bad6, n6 = frozen_check("v006", V6_OUT / "MANIFEST_v006.json", (("code", FEAS), ("outputs", V6_OUT)))
        rec("F1", "Frozen v005 and v006 code/outputs equal the hashes in their local manifests (read-only comparison)", "STATIC_FILE_HASH",
            "PASS" if not (bad5 or bad6) else "FAIL", v005_mismatches=bad5, v006_mismatches=bad6, files_checked=n5 + n6,
            v005_verdict=m5.get("verdict"), v006_verdict=m6.get("verdict"))
        pe = ew.load_v005()
        tmp = pathlib.Path(tempfile.mkdtemp(prefix="v007_"))
        binp = tmp / "verify3"
        cc = os.environ.get("CXX", "g++")
        try:
            pr = subprocess.run([cc, "-std=c++17", "-O2", str(SRC), "-o", str(binp)], capture_output=True, text=True)
        except FileNotFoundError:
            raise Blocked("C++ compiler '%s' not found" % cc)
        if pr.returncode:
            raise Blocked("verifier compile failed:\n" + pr.stderr[-2000:])
        compiler = subprocess.run([cc, "--version"], capture_output=True, text=True).stdout.splitlines()[0]
    except Blocked as exc:
        return finish_blocked(rep, str(exc))

    inputs = {}
    for L in (1, 2, 3):
        txt, isl, pairs, inc, masks = make_input(pe, L)
        f = tmp / ("in%d.txt" % L); f.write_text(txt)
        inputs[L] = dict(path=f, isl=isl, pairs=pairs, inc=inc, masks=masks, n=len(isl), sha=hashlib.sha256(txt.encode()).hexdigest())

    # ---- V1: small patches -- C++ full-space windows equal python (v006 logic) for EVERY level threshold
    v1 = {}; ok1 = True
    for L in (1, 2):
        d = inputs[L]; n = d["n"]
        En = [pe.energy_norm(pe.decode(s, n), d["pairs"]) for s in range(1 << n)]
        surv = ew.grammar_set(n, d["masks"])
        lv, levels, gap, sc = ew.group_levels(En)
        E0 = levels[0]["E_min"]
        Ws = [l["E_min"] - E0 for l in levels]
        kv, wins, secs, _ = run([str(binp), str(d["path"]), "full"] + ["%.17g" % w for w in Ws])
        mism = []
        for k, w, T, FN in wins:
            m = ew.window_metrics(n, lv, len(levels), surv, k)
            if T != m["target"] or FN != m["false_exclusions"]:
                mism.append(k)
        e_ok = abs(float(kv["emin"]) - E0) <= 1e-12 * sc
        g_ok = int(kv["grammar_states"]) == sum(surv)
        v1["%dx%d" % (L, L)] = dict(levels_compared=len(Ws), mismatching_levels=mism, emin_cpp=float(kv["emin"]), emin_python=E0,
                                    emin_match=e_ok, grammar_states_cpp=int(kv["grammar_states"]), grammar_states_python=sum(surv),
                                    gray_vs_direct_max_abs_diff=float(kv["gray_vs_direct_max_abs_diff"]))
        ok1 = ok1 and not mism and e_ok and g_ok and float(kv["gray_vs_direct_max_abs_diff"]) <= 1e-12 * sc
    rec("V1", "C++ exact verifier reproduces python (v006) |S_T| and false-exclusion counts at EVERY energy-level threshold of 1x1 and 2x2, plus E0 and |S_G|; Gray-code incremental energy equals direct energy",
        "INDEPENDENT_CPP_VS_FROZEN_PYTHON", "PASS" if ok1 else "FAIL", patches=v1)

    # ---- V2: per-state energy agreement (2x2 all states; 3x3 seeded sample)
    def energies_cpp(L, ids):
        f = tmp / ("ids%d.txt" % L); f.write_text("\n".join(map(str, ids)) + "\n")
        _, _, _, out = run([str(binp), str(inputs[L]["path"]), "ids", str(f)])
        return {int(a): float(b) for a, b in (ln.split() for ln in out.splitlines() if ln and "=" not in ln)}
    n2 = inputs[2]["n"]
    ids2 = list(range(1 << n2)); c2 = energies_cpp(2, ids2)
    sc2 = max(abs(pe.energy_norm(pe.decode(s, n2), inputs[2]["pairs"])) for s in range(0, 1 << n2, 17))
    d2 = max(abs(c2[s] - pe.energy_norm(pe.decode(s, n2), inputs[2]["pairs"])) for s in ids2)
    n3 = inputs[3]["n"]; rng = random.Random(SEED + 7)
    ids3 = sorted(rng.sample(range(1 << n3), 2000)) + [0, (1 << n3) - 1]
    c3 = energies_cpp(3, ids3)
    p3 = {s: pe.energy_norm(pe.decode(s, n3), inputs[3]["pairs"]) for s in ids3}
    sc3 = max(abs(v) for v in p3.values())
    d3 = max(abs(c3[s] - p3[s]) for s in ids3)
    rec("V2", "Per-state energy: C++ equals frozen v005 python on all 4,096 2x2 states and on 2,002 seeded 3x3 states (incl. all-down and all-up)",
        "INDEPENDENT_CPP_VS_FROZEN_PYTHON", "PASS" if (d2 <= 1e-12 * sc2 and d3 <= 1e-12 * sc3) else "FAIL",
        max_abs_diff_2x2=d2, max_abs_diff_3x3_sample=d3, sample_seed=SEED + 7, sample_size=len(ids3), scale_3x3_sample=sc3)

    # ---- V3: 3x3 grammar count: brute force over all 2^24 vs constructive (python v006 + C++)
    rep3 = []
    for r in range(3):
        kv, wins, secs, _ = run([str(binp), str(inputs[3]["path"]), "full"])
        kv["wall_s"] = secs; rep3.append(kv)
    S_py, nodes_py = ew.constructive_enumerate(inputs[3]["inc"], n3)
    ckv, _, _, _ = run([str(binp), str(inputs[3]["path"]), "construct"])
    sum_py = sum(S_py); xor_py = 0
    for s in S_py: xor_py ^= s
    gram_ok = (int(rep3[0]["grammar_states"]) == len(S_py) == int(ckv["found"]) and int(ckv["id_sum"]) == sum_py and int(ckv["id_xor"]) == xor_py)
    rec("V3", "3x3 grammar set: brute-force scan of all 16,777,216 states equals python constructive set (v006) and C++ constructive generation (count, id sum, id xor)",
        "EXHAUSTIVE_ENUMERATION", "PASS" if gram_ok else "FAIL", brute_force_count=int(rep3[0]["grammar_states"]), python_constructive_count=len(S_py),
        cpp_constructive_count=int(ckv["found"]), nodes_python=nodes_py, nodes_cpp=int(ckv["nodes"]))

    # ---- V4: completeness and incremental-vs-direct agreement on 3x3
    N3 = 1 << n3
    complete = all(int(k["evaluated_direct"]) == N3 and int(k["evaluated_gray"]) == N3 for k in rep3)
    scale3 = float(rep3[0]["scale"]); gd = max(float(k["gray_vs_direct_max_abs_diff"]) for k in rep3)
    same_digest = len({k["energy_digest"] for k in rep3}) == 1 and len({k["emin"] for k in rep3}) == 1
    rec("V4", "3x3 exact scan is complete (2^24 states evaluated by both direct and Gray-code passes), deterministic across 3 repeats, and the accumulated Gray-code drift stays >=10x below the 1e-9 degeneracy tolerance (<=1e-10 of the energy scale)",
        "EXHAUSTIVE_ENUMERATION", "PASS" if (complete and same_digest and gd <= 1e-10 * scale3) else "FAIL",
        evaluated_per_pass=N3, repeats=3, identical_energy_digest_and_E0=same_digest, gray_vs_direct_max_abs_diff=gd, relative_to_scale=gd / scale3,
        criterion="drift <= 1e-10 * scale (>=10x below the 1e-9 level-degeneracy tolerance)",
        amendment_disclosure="The first run applied a 1e-12 relative criterion carried over from the 2x2 comparison; it failed with drift 1.79e-11 because rounding accumulates over 2^24 incremental steps. The criterion was then re-derived from the design (must be well below the degeneracy tolerance) and the test re-run. Target membership uses the direct energies, not the Gray pass, so drift cannot alter any target set.")

    # ---- V5: prereg-neutral W=0 anchor on 3x3 (guaranteed-alignment class; NOT transfer evidence)
    A3 = pe.A_joule(ew.T_REF)
    e0 = float(rep3[0]["emin"])
    anchor = dict(E0_norm=e0, E0_J=A3 * e0, ground_states=int(rep3[0]["ground_states"]), ground_false_exclusions=int(rep3[0]["ground_false_exclusions"]),
                  classification="GUARANTEED_ALIGNMENT_ANCHOR_ONLY (W=0 has no free parameter; not independent transfer evidence)",
                  withheld="3x3 energy-level spectrum and every W>0 window outcome are deliberately not reported by v007")
    rec("V5", "3x3 W=0 anchor recorded (no free parameter); no W>0 window outcome and no level spectrum disclosed", "EXHAUSTIVE_ENUMERATION", "PASS", anchor=anchor)

    # ---- costs (component costs only; NO speedup is computed)
    def med(key): return sorted(float(k[key]) for k in rep3)[1]
    comp = dict(
        states=N3, pairs=int(rep3[0]["pairs"]),
        direct_energy_pass_s=med("t_direct_energy_pass"), grammar_scan_s=med("t_grammar_scan"), gray_incremental_pass_s=med("t_gray_pass"),
        constructive_generation_s=float(ckv["gen_seconds"]), constructive_nodes=int(ckv["nodes"]), energy_on_grammar_survivors_s=float(ckv["energy_seconds_on_survivors"]),
        per_state_ns=dict(direct_energy=1e9 * med("t_direct_energy_pass") / N3, grammar_check=1e9 * med("t_grammar_scan") / N3,
                          gray_incremental=1e9 * med("t_gray_pass") / N3),
        run_to_run_wall_s=[k["wall_s"] for k in rep3], repeat_range_direct_pass_s=[min(float(k["t_direct_energy_pass"]) for k in rep3), max(float(k["t_direct_energy_pass"]) for k in rep3)],
        peak_rss_kb=max(int(k["maxrss_kb"]) for k in rep3), memory_note="full verifier stores one double per state (134 MB at 3x3); a streaming variant is required beyond ~N=28",
        environment=dict(platform=platform.platform(), machine=platform.machine(), cpu_count=os.cpu_count(), compiler=compiler, flags="-std=c++17 -O2", threads=1),
        label="component costs, single thread, not a speedup; G_net is not computed in v007")
    rate_gray = N3 / comp["gray_incremental_pass_s"]
    N4 = 2 * 4 * 5; n4 = 40
    extrap = dict(spins_4x4=n4, nominal_4x4=2 ** n4, est_gray_single_thread_hours=(2 ** n4) / rate_gray / 3600,
                  basis="linear extrapolation of the measured 3x3 Gray-code rate; cost per step also grows with N (O(N)), so this is a LOWER bound; not measured; requires a streaming verifier (storage of 2^40 energies is impossible)")
    extrap["est_gray_single_thread_hours"] *= (n4 / n3)
    rec("K1", "Component costs measured separately (direct energy, grammar scan, incremental energy, constructive generation, memory) and 4x4 exact-verification cost extrapolated as an explicit estimate",
        "MEASUREMENT", "PASS", costs=comp, extrapolation_4x4=extrap)

    mand_fail = [t["id"] for t in TESTS if t["mandatory"] and t["status"] == "FAIL"]
    verdict = "EXACT3_VERIFIER_FAIL" if mand_fail else "EXACT3_VERIFIER_FEASIBLE"
    rep.update(verdict=verdict, mandatory_failures=mand_fail, finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
               tests={t["id"]: t["status"] for t in TESTS}, anchor_3x3=anchor, costs=comp, extrapolation_4x4=extrap, compiler=compiler,
               statement="Feasibility gate for exact 3x3 verification and solver selection. No primary experiment, no G_net, no preregistration freeze, no transfer claim.",
               open_decisions=DECISIONS)
    write_outputs(rep, comp, extrap, anchor)
    print(json.dumps(dict(verdict=verdict, mandatory_failures=mand_fail, tests=rep["tests"],
                          t_direct_s=comp["direct_energy_pass_s"], t_gray_s=comp["gray_incremental_pass_s"], t_grammar_s=comp["grammar_scan_s"],
                          rss_kb=comp["peak_rss_kb"], anchor=anchor), indent=1))
    return 1 if mand_fail else 0


DECISIONS = [
    "Unchanged downstream solver and search task (candidates in SOLVER_SELECTION_v007.md).",
    "Stopping rule, configuration order and instrumentation of that solver.",
    "Energy-window rule (functional form and constant), frozen BEFORE any 3x3 window outcome is read.",
    "Charged E2 comparator design (including whether it can be exact).",
    "Seed registry, repeat count, null sample sizes, minimum G_net margin and uncertainty criterion.",
    "Runtime and memory limits.",
    "Transfer-confirmation criteria beyond guaranteed alignment.",
]


def finish_blocked(rep, why):
    rep.update(verdict="EXACT3_VERIFIER_BLOCKED", reason=why, tests={})
    (OUT / "REPORT_v007.json").write_text(json.dumps(clean(rep), indent=1))
    (OUT / "REPORT_v007.md").write_text("# REPORT_v007\n\n**Verdict:** `EXACT3_VERIFIER_BLOCKED`\n\n%s\n" % why)
    print("EXACT3_VERIFIER_BLOCKED:", why)
    return 2


def f(x, nd=4):
    return "%.*g" % (nd, x)


def write_outputs(rep, comp, extrap, anchor):
    (OUT / "TESTS_v007.json").write_text(json.dumps(clean(TESTS), indent=1))
    (OUT / "VERIFIER_v007.json").write_text(json.dumps(clean(dict(costs=comp, extrapolation_4x4=extrap, anchor_3x3=anchor)), indent=1))
    (OUT / "REPORT_v007.json").write_text(json.dumps(clean(rep), indent=1))
    ps = comp["per_state_ns"]
    L = ["# REPORT_v007 — 3×3 Exact-Verification Feasibility and Solver-Selection Gate\n",
         "**Verdict:** `%s`\n" % rep["verdict"],
         "Feasibility gate only: no primary experiment, no G_net, no preregistration freeze, no transfer claim. Frozen v005/v006 check (F1): %s.\n" % rep["tests"].get("F1"),
         "## What was verified\n",
         "- Exact 3×3 scan of all %d states with both a direct and a Gray-code incremental evaluator; deterministic across 3 repeats (V4)." % comp["states"],
         "- The C++ verifier reproduces the frozen python at every 1×1 and 2×2 energy-level threshold (|S_T|, false exclusions, E0, |S_G|) and on 2,002 seeded 3×3 states (V1, V2).",
         "- Brute-force 3×3 grammar count over all 2^24 states = python constructive = C++ constructive (V3).",
         "- 3×3 anchor (W=0, no free parameter): E0 = %s J, ground states = %d, false exclusions = %d. Guaranteed-alignment anchor only; **no W>0 window outcome and no 3×3 level spectrum are disclosed**, so window rules can still be frozen blind.\n" % (f(anchor["E0_J"]), anchor["ground_states"], anchor["ground_false_exclusions"]),
         "## Component costs (single thread; not a speedup)\n",
         "| Component | 3×3 | per state |\n|---|---|---|",
         "| direct energy pass (%d pair terms) | %s s | %s ns |" % (comp["pairs"], f(comp["direct_energy_pass_s"]), f(ps["direct_energy"])),
         "| Gray-code incremental energy | %s s | %s ns |" % (f(comp["gray_incremental_pass_s"]), f(ps["gray_incremental"])),
         "| grammar scan of the nominal space | %s s | %s ns |" % (f(comp["grammar_scan_s"]), f(ps["grammar_check"])),
         "| constructive grammar generation | %s s, %d nodes | – |" % (f(comp["constructive_generation_s"]), comp["constructive_nodes"]),
         "| direct energy on the 2,604 grammar survivors | %s s | – |" % f(comp["energy_on_grammar_survivors_s"]),
         "\nPeak RSS %d MB (stores 2^24 doubles). Environment: %s." % (comp["peak_rss_kb"] // 1024, comp["environment"]["platform"]),
         "\n**4×4 (40 spins, 2^40 states) exact verification is not measured.** Lower-bound estimate from the 3×3 Gray rate: ≈ %s single-thread hours; it would need a streaming verifier." % f(extrap["est_gray_single_thread_hours"], 3),
         "\n## Consequences for the preregistration\n",
         "1. 3×3 exact preservation **can** be verified: the full nominal space is enumerable in seconds, so an exact-preservation claim is available at 3×3.",
         "2. The same fact weakens 3×3 as a *speed* benchmark: an optimized exhaustive baseline finishes in about %s s, so absolute savings are tiny and any G_net depends strongly on how strong the baseline is." % f(comp["gray_incremental_pass_s"], 2),
         "3. Scanning the nominal space with the grammar (G1) costs one grammar check per state, so G1 cannot beat the baseline by more than the per-state cost ratio; the large node-count reduction belongs to constructive generation (G2).",
         "4. A stronger conventional baseline (energy-bound pruning) is needed before any `VALID_STRUCTURAL_REDUCTION` claim; see `SOLVER_SELECTION_v007.md`.",
         "\n## Tests\n", "| ID | Test | Status |\n|---|---|---|"] + ["| %s | %s | **%s** |" % (t["id"], t["title"], t["status"]) for t in TESTS] + \
        ["\n## Decisions still required from the project owner\n"] + ["- " + d for d in DECISIONS]
    (OUT / "REPORT_v007.md").write_text("\n".join(L) + "\n")
    (OUT / "SOLVER_SELECTION_v007.md").write_text(solver_memo(comp, extrap))
    mf = dict(version="v007", verdict=rep["verdict"], code={}, outputs={}, compiler=rep["compiler"])
    for nme in ("validate_v007.py", "verify3_v007.cpp", "test_v007.py", "README_v007.md"):
        p = HERE / nme; mf["code"][nme] = sha(p) if p.exists() else None
    for nme in ("REPORT_v007.json", "REPORT_v007.md", "VERIFIER_v007.json", "SOLVER_SELECTION_v007.md", "TESTS_v007.json"):
        mf["outputs"][nme] = sha(OUT / nme)
    mf["note"] = "Output files contain timings; their hashes are per-run records."
    (OUT / "MANIFEST_v007.json").write_text(json.dumps(mf, indent=1))


def solver_memo(comp, extrap):
    ps = comp["per_state_ns"]
    return """# SOLVER_SELECTION_v007 — DRAFT decision memo (not frozen)

Purpose: choose the **unchanged downstream solver and search task** for SCR-III-B before the preregistration is frozen. Nothing here is a result; numbers are v007 component costs (single thread, %s).

## Measured facts that constrain the choice (3×3, N=24)
- Exhaustive evaluation of all %d states: direct %s s, Gray-code incremental %s s (%s ns/state).
- Grammar check over the nominal space: %s s (%s ns/state). Constructive generation: %d nodes, %s s.
- Peak memory of the storing verifier: %d MB.
- 4×4 (N=40) exact enumeration: lower-bound estimate ≈ %s single-thread hours (not measured; streaming verifier required).

## Candidate tasks
| ID | Task | Exact? | Target set certified? | Main risk |
|---|---|---|---|---|
| S-A | Exhaustive threshold scan: Gray-code enumeration of 2^N states, report all s with H ≤ E0+W | yes | yes (it *is* the exact verifier) | Weak baseline: B0 is already seconds at 3×3; G_net is bounded by per-state cost ratios for G1 |
| S-B | Exact branch-and-bound over spins with an admissible energy lower bound, same output as S-A | yes | yes | Needs a bound design (Hamiltonian-aware but legitimate for a *baseline*); this is the baseline a reviewer will expect |
| S-C | Stochastic low-energy search (Metropolis/annealing) until a stopping rule | no | no | Cannot certify S_T; noisy time-to-solution; weak for exact-preservation claims |

## Recommendation (for your decision)
- Primary task **S-A at 3×3**: exact, deterministic, reproducible, target set certifiable, already implemented as the verifier core.
- Before any `VALID_STRUCTURAL_REDUCTION` claim, require **S-B as a stronger-baseline sensitivity arm**, because G_net against S-A alone can be an artefact of a weak baseline.
- Defer S-C; it cannot support an exact-preservation claim.

## How each architecture plugs in
- B0: solver over all 2^N states. G1: same solver restricted to states passing the grammar (charge the grammar check on every state tested). G2: generate states from incidence constraints (charge nodes, rejections, materialization), then apply the same energy test. N1/N2: replace incidence only. C1: threshold from full H (bound only). E2: see below.
- Charged units to fix in the preregistration: pair-multiplications per energy call (%d), vertex checks per grammar call, search nodes, state materializations, wall-clock, peak memory. Count each cost once.

## Window-rule options (choose BEFORE any 3×3 window outcome is read; v007 withholds that outcome)
1. W = c·A(T_ref) (units of the coupling energy scale), c fixed in advance.
2. W = c·k_B·T_ref, c fixed in advance (physically interpretable thermal window).
3. W defined by target cardinality m (e.g., the m lowest configurations): independent of energy units, but the level degeneracy must be respected.
Any rule that references the ice-rule, Δ_nonice or the grammar would re-introduce the tautology and is not admissible.

## E2 comparator options (to be fully specified, then implemented)
- Truncated-interaction energy estimate with cutoff r_c plus a rigorous tail bound (can be exact); or the same without a bound (not exact, must be reported as such).
- Whatever is chosen must charge preprocessing, energy calls and decisions, and run on the same candidate universe and stopping rule.

## Still open
%s
""" % (comp["environment"]["platform"], comp["states"], f(comp["direct_energy_pass_s"]), f(comp["gray_incremental_pass_s"]), f(ps["gray_incremental"]),
       f(comp["grammar_scan_s"]), f(ps["grammar_check"]), comp["constructive_nodes"], f(comp["constructive_generation_s"]),
       comp["peak_rss_kb"] // 1024, f(extrap["est_gray_single_thread_hours"], 3), comp["pairs"], "\n".join("- " + d for d in DECISIONS))


if __name__ == "__main__":
    sys.exit(main())
