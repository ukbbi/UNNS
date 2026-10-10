#!/usr/bin/env python3
"""SCR-III-B PREFLIGHT_v006 -- Energy-Window Feasibility and Non-Tautology Gate (orchestrator).

Run from the project root:   python3 scr_iii_b/feasibility/validate_v006.py
Reads (never writes) the frozen v005 code and outputs. Writes only scr_iii_b/output/validation/v006/.
No primary transfer experiment is run; no verdict beyond FEASIBILITY_* is issued.
"""
import sys
sys.dont_write_bytecode = True
import csv, datetime, hashlib, json, math, os, pathlib, platform, resource, time, tracemalloc

HERE = pathlib.Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import energy_windows_v006 as ew
import grammar_nulls_v006 as gn

OUT = PROJECT / "scr_iii_b" / "output" / "validation" / "v006"
V005_OUT = PROJECT / "scr_iii_b" / "output" / "validation" / "v005"
V005_CODE = PROJECT / "scr_iii_b" / "reference_check"
N_NULLS = 1000
TESTS = []


class Blocked(Exception):
    pass


def rec(tid, title, level, status, mandatory=True, **detail):
    TESTS.append(dict(id=tid, title=title, evidence_level=level, status=status, mandatory=mandatory, detail=detail))


def sha_file(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def clean(o):
    if isinstance(o, float) and (math.isnan(o) or math.isinf(o)):
        return None
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    return o


def s2str(sid, n):
    return "".join("+" if (sid >> i) & 1 else "-" for i in range(n))


# ------------------------------------------------------------------ frozen v005 record
def check_frozen():
    mf = V005_OUT / "MANIFEST_v005.json"
    if not mf.exists():
        raise Blocked("MANIFEST_v005.json not found: " + str(mf))
    m = json.loads(mf.read_text())
    rows, bad = [], []
    for grp, base in (("code", V005_CODE), ("outputs", V005_OUT)):
        for name, h in m[grp].items():
            p = base / name
            got = sha_file(p) if p.exists() else None
            rows.append(dict(group=grp, file=name, expected=h, actual=got, match=(got == h)))
            if got != h:
                bad.append(name)
    rec("F1", "Frozen v005 code and outputs equal the hashes recorded in the local MANIFEST_v005.json (read-only comparison)",
        "STATIC_FILE_HASH", "PASS" if not bad else "FAIL", mismatches=bad, files_checked=len(rows),
        v005_verdict=m.get("verdict"), rows=rows)
    if m.get("verdict") != "PHYSICAL_HAMILTONIAN_LOCK_PASS":
        raise Blocked("v005 verdict is not PHYSICAL_HAMILTONIAN_LOCK_PASS")
    return m, rows


# ------------------------------------------------------------------ per-patch analysis
def analyze_patch(pe, L, v005rep, v005_ground_rows):
    out = dict(L=L)
    tracemalloc.start()
    t0 = time.perf_counter()
    isl, pairs, vpos = ew.build_patch(pe, L)
    n = len(isl); N0 = 1 << n
    inc, roles = ew.build_incidence(pe, isl, vpos)
    masks = ew.compile_masks(inc)
    t_setup = time.perf_counter() - t0

    t0 = time.perf_counter(); states = [pe.decode(s, n) for s in range(N0)]; t_enum = time.perf_counter() - t0
    t0 = time.perf_counter(); surv = ew.grammar_set(n, masks); t_gram = time.perf_counter() - t0
    t0 = time.perf_counter(); En = [pe.energy_norm(st, pairs) for st in states]; t_en = time.perf_counter() - t0
    cur, peak = tracemalloc.get_traced_memory(); tracemalloc.stop()

    A = pe.A_joule(ew.T_REF)
    EJ = [A * e for e in En]
    level_of, levels, min_gap_rel, scale = ew.group_levels(En)
    E0 = levels[0]["E_min"]
    nl = len(levels)
    ice_geo = [pe.ice_ok_geometric(st, isl, vpos) for st in states]
    types_all = [ew.vertex_types(s, inc, roles) for s in range(N0)]
    type_ice = [all(t in (1, 2) for t in ts) for ts in types_all]
    incnt = [ew.in_counts(s, masks) for s in range(N0)]
    viol = [sum(1 for c in ic if c != 2) for ic in incnt]

    # first level containing a non-ice state; mixed levels
    lev_ice = [sum(1 for s in l["members"] if surv[s]) for l in levels]
    mixed = [k for k, l in enumerate(levels) if 0 < lev_ice[k] < len(l["members"])]
    k_nonice = next((k for k in range(nl) if lev_ice[k] < len(levels[k]["members"])), None)
    delta_norm = (levels[k_nonice]["E_min"] - E0) if k_nonice is not None else None

    # windows
    wins = []
    for k in range(nl):
        m = ew.window_metrics(n, level_of, nl, surv, k)
        Wn = levels[k]["E_min"] - E0
        Wn_next = (levels[k + 1]["E_min"] - E0) if k + 1 < nl else None
        if k_nonice is None or k < k_nonice:
            cls = "GROUND_ONLY_TRIVIAL" if k == 0 else "ICE_EXCITED_PRESERVED_BELOW_FIRST_NONICE"
        elif k == k_nonice:
            cls = "FIRST_NONICE_THRESHOLD_EXPECTED_FAILURE"
        else:
            cls = "DEFECT_ACCESSIBLE_FAILURE"
        tgt_ids = [s for s in range(N0) if level_of[s] <= k]
        eq_grammar = (m["false_exclusions"] == 0 and m["target"] == m["grammar"])
        wins.append(dict(patch="%dx%d" % (L, L), level=k, W_norm=Wn, W_J=A * Wn, W_over_kT_ref=A * Wn / (pe.KB * ew.T_REF),
                         interval_upper_norm=Wn_next, level_energy_J=A * levels[k]["E_min"], level_members=len(levels[k]["members"]),
                         level_ice_members=lev_ice[k], classification=cls, target_equals_grammar_set=eq_grammar,
                         grammar_states_not_in_target=m["grammar"] - m["surviving_targets"], **m))

    # regime C record
    reg = None
    if k_nonice is not None:
        before = [s for s in range(N0) if level_of[s] <= k_nonice - 1]
        after = [s for s in range(N0) if level_of[s] <= k_nonice]
        excl = [s for s in after if not surv[s]]
        first = min(excl)
        kept = [s for s in after if surv[s]]
        reg = dict(threshold_level=k_nonice, W_norm=delta_norm, W_J=A * delta_norm, target_before_ids=before, target_after_ids=after,
                   kept_after_filter_ids=kept, false_excluded_ids=excl, false_exclusion_count=len(excl),
                   first_excluded=dict(id=first, state=s2str(first, n), energy_J=EJ[first], energy_above_E0_J=A * (En[first] - E0),
                                       violated_vertices=ew.violated_vertices(first, masks), in_counts=incnt[first],
                                       vertex_types=types_all[first]))

    # bookkeeping rows
    rows = []
    for s in range(N0):
        tc = [types_all[s].count(t) for t in (1, 2, 3, 4)]
        rows.append([("%dx%d" % (L, L)), s, s2str(s, n), EJ[s], A * (En[s] - E0), En[s] - E0, level_of[s], int(surv[s]), viol[s],
                     ";".join(map(str, incnt[s])), ";".join(map(str, tc))])

    out.update(n=n, N0=N0, pairs=len(pairs), A_J=A, inc=inc, roles=roles, masks=masks, En=En, EJ=EJ, surv=surv, level_of=level_of,
               levels=levels, E0_norm=E0, E0_J=A * E0, min_gap_rel=min_gap_rel, scale=scale, ice_geo=ice_geo, type_ice=type_ice,
               windows=wins, regimeC=reg, k_nonice=k_nonice, delta_norm=delta_norm, mixed_levels=mixed, rows=rows, lev_ice=lev_ice,
               timing=dict(setup_s=t_setup, enumerate_states_s=t_enum, grammar_eval_s=t_gram, energy_eval_s=t_en,
                           grammar_per_state_us=1e6 * t_gram / N0, energy_per_state_us=1e6 * t_en / N0),
               memory=dict(tracemalloc_peak_bytes=peak, note="python allocation peak for setup+decode+grammar+energy lists"))
    return out


def null_summaries(P, family, nulls, inc_real):
    """Summaries per null; Hamiltonian/targets untouched (level_of is read-only here)."""
    n, N0 = P["n"], P["N0"]; level_of = P["level_of"]; nl = len(P["levels"]); surv_real = P["surv"]
    SGr = sum(surv_real)
    k0, kn = 0, P["k_nonice"]
    ks = [("W0_ground", 0)]
    if kn is not None:
        if kn - 1 >= 1:
            ks.append(("W_last_ice_below_gap", kn - 1))
        ks.append(("W_first_nonice", kn))
    rows = []
    for nl_ in nulls:
        surv = nl_["surv"]; SG = sum(surv)
        symdiff = sum(1 for a, b in zip(surv, surv_real) if a != b)
        ns_by_level = [0] * nl
        for s in range(N0):
            if not surv[s]:
                ns_by_level[level_of[s]] += 1
        cum, c = [], 0
        for x in ns_by_level:
            c += x; cum.append(c)
        tsize = [0] * nl
        for s in range(N0):
            tsize[level_of[s]] += 1
        tcum, c = [], 0
        for x in tsize:
            c += x; tcum.append(c)
        ff = next((k for k in range(nl) if cum[k] > 0), None)
        r = dict(family=family, idx=nl_["idx"], seed=nl_["seed"], patch="%dx%d" % (P["L"], P["L"]), grammar=SG,
                 contraction=1 - SG / N0, grammar_ratio_to_real=SG / SGr, capacity_comparable=(0.5 <= SG / SGr <= 2.0),
                 same_survivor_set_as_real=(symdiff == 0), survivor_symdiff_with_real=symdiff, first_failure_level=ff)
        for name, k in ks:
            r["FN_" + name] = cum[k]
            r["pres_" + name] = 1 - cum[k] / tcum[k]
        r["real_first_failure_level"] = kn
        r["preserves_at_least_as_far_as_real"] = (ff is None) or (kn is not None and ff >= kn)
        rows.append(r)
    return rows


# ------------------------------------------------------------------ main
def main():
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    OUT.mkdir(parents=True, exist_ok=True)
    rep = dict(version="v006", started_utc=started, platform=platform.platform(), python=sys.version.split()[0])
    try:
        manifest5, frozen_rows = check_frozen()
        try:
            pe = ew.load_v005()
        except Exception as exc:
            raise Blocked("cannot import frozen v005 evaluator: %r" % exc)
        v5 = json.loads((V005_OUT / "REPORT_v005.json").read_text())
        v5_ground = {}
        with open(V005_OUT / "GROUND_STATES_v005.csv") as f:
            for r in csv.DictReader(f):
                if r["model"].startswith("SPMMC_v1.00_all_pair_verified_sign"):
                    v5_ground.setdefault(int(r["L"]), []).append((int(r["state_id"]), float(r["E_J"]), r["state_string(+/-,spin0 first)"]))
    except Blocked as exc:
        return finish_blocked(rep, str(exc))

    P = {}
    for L in (1, 2):
        P[L] = analyze_patch(pe, L, v5, v5_ground)

    # ---- C1/C2/C3 consistency with frozen v005 -------------------------------------------------
    c1 = {}
    ok1 = True
    for L, p in P.items():
        key = "%dx%d" % (L, L)
        v5p = v5["patches"][key]
        n_ice = sum(p["surv"])
        gids = [s for s in p["levels"][0]["members"]]
        gJ = p["E0_J"]
        v5g = sorted(v5_ground[L])
        match_ids = [g[0] for g in v5g] == gids
        match_E = all(abs(g[1] - gJ) <= 1e-12 * abs(gJ) for g in v5g)
        match = (n_ice == v5p["ice_states_python_geometric"] and match_ids and match_E and len(gids) == v5p["degeneracy"]
                 and abs(gJ - v5p["ground_E_J"]) <= 1e-12 * abs(gJ) and p["ice_geo"] == p["surv"])
        c1[key] = dict(ice_states=n_ice, v005_ice_states=v5p["ice_states_python_geometric"], ground_ids=gids,
                       v005_ground_ids=[g[0] for g in v5g], ground_E_J=gJ, v005_ground_E_J=v5p["ground_E_J"], degeneracy=len(gids), match=match)
        ok1 = ok1 and match
    rec("C1", "Exhaustive 1x1/2x2 enumeration reproduces frozen v005: ice-state counts, ground ids, ground energy (J), degeneracy; incidence grammar == v005 geometric ice rule on every state",
        "FROZEN_V005_EVALUATOR_PYTHON", "PASS" if ok1 else "FAIL", patches=c1)
    ok2 = all(p["type_ice"] == p["surv"] for p in P.values())
    rec("C2", "Independent vertex typing (source ENWS table re-implemented) agrees with the incidence grammar on every state (Types I,II <=> 2-in/2-out)",
        "SOURCE_DERIVED_INDEPENDENT_PYTHON", "PASS" if ok2 else "FAIL")
    tolok = all(p["min_gap_rel"] is None or p["min_gap_rel"] > 1e3 * ew.LEVEL_TOL_REL for p in P.values())
    mixed = {("%dx%d" % (L, L)): p["mixed_levels"] for L, p in P.items()}
    rec("C3", "Level grouping: degeneracy tolerance (relative 1e-9 of max|E|) is far below the smallest genuine level spacing; no level mixes ice and non-ice states",
        "SOURCE_DERIVED_INDEPENDENT_PYTHON", "PASS" if (tolok and not any(mixed.values())) else "FAIL",
        tolerance_relative=ew.LEVEL_TOL_REL, min_level_spacing_relative={("%dx%d" % (L, L)): p["min_gap_rel"] for L, p in P.items()},
        number_of_levels={("%dx%d" % (L, L)): len(p["levels"]) for L, p in P.items()}, mixed_levels=mixed)

    # ---- windows --------------------------------------------------------------------------------
    allw = [w for p in P.values() for w in p["windows"]]
    # direct-threshold cross-check of level-based targets
    ok_dir = True
    for L, p in P.items():
        sc = p["scale"]; tol = ew.LEVEL_TOL_REL * sc
        for k, l in enumerate(p["levels"]):
            W = l["E_min"] - p["E0_norm"]
            direct = {s for s, e in enumerate(p["En"]) if e <= p["E0_norm"] + W + tol}
            lvl = {s for s in range(p["N0"]) if p["level_of"][s] <= k}
            ok_dir = ok_dir and direct == lvl
            if k > 0:
                below = {s for s, e in enumerate(p["En"]) if e <= p["E0_norm"] + W - 10 * tol}
                ok_dir = ok_dir and below == {s for s in range(p["N0"]) if p["level_of"][s] <= k - 1}
    rec("W1", "Every unique energy-level transition evaluated; level-based target sets equal direct threshold H<=E0+W on both sides of every transition",
        "EXHAUSTIVE_ENUMERATION", "PASS" if ok_dir else "FAIL", windows_evaluated={("%dx%d" % (L, L)): len(p["levels"]) for L, p in P.items()})
    # monotone, formulas
    okm = True
    for p in P.values():
        fn = [w["false_exclusions"] for w in p["windows"]]
        okm = okm and all(a <= b for a, b in zip(fn, fn[1:])) and p["windows"][0]["false_exclusions"] == 0 \
            and all(abs(w["preservation"] - (1 - w["false_exclusions"] / w["target"])) < 1e-15 for w in p["windows"]) \
            and all(w["surviving_targets"] + w["false_exclusions"] == w["target"] for w in p["windows"])
    rec("W2", "Window metrics are internally consistent (|S_T∩S_G|+FN=|S_T|, FN non-decreasing with W, ground window preserved)", "EXHAUSTIVE_ENUMERATION",
        "PASS" if okm else "FAIL")
    okc = True; cap_rows = []
    for p in P.values():
        for w in p["windows"]:
            if w["false_exclusions"] == 0:
                okc = okc and w["capacity_L_over_m"] >= 1.0
                cap_rows.append((w["patch"], w["level"], w["capacity_L_over_m"]))
    rec("W3", "Capacity L/m >= 1 for every exactly preserved nonempty window", "EXHAUSTIVE_ENUMERATION", "PASS" if okc else "FAIL", preserved_windows=len(cap_rows))
    okfirst = True; firsts = {}
    for L, p in P.items():
        kn = p["k_nonice"]
        key = "%dx%d" % (L, L)
        if kn is None:
            firsts[key] = None; continue
        first_fail = next(w["level"] for w in p["windows"] if w["false_exclusions"] > 0)
        okfirst = okfirst and first_fail == kn and p["regimeC"]["false_exclusion_count"] > 0
        firsts[key] = dict(first_failure_level=first_fail, Delta_nonice_W_norm=p["delta_norm"], Delta_nonice_W_J=p["regimeC"]["W_J"],
                           false_exclusions=p["regimeC"]["false_exclusion_count"], first_excluded=p["regimeC"]["first_excluded"])
    rec("W4", "Regime C expected-failure control: preservation first fails exactly at the first window admitting a non-ice state (control success, not a preflight failure)",
        "EXHAUSTIVE_ENUMERATION", "PASS" if okfirst else "FAIL", patches=firsts)

    # ---- constructive enumeration ---------------------------------------------------------------
    cons = {}
    okcons = True
    for L in (1, 2, 3):
        isl = pe.source_geometry(L); vpos = pe.vertex_positions(L)
        inc, _ = ew.build_incidence(pe, isl, vpos)
        t0 = time.perf_counter()
        S1, nodes1 = ew.constructive_enumerate(inc, len(isl))
        t1 = time.perf_counter() - t0
        S2, nodes2 = ew.constructive_enumerate(inc, len(isl), vertex_order=list(reversed(range(len(inc)))))
        entry = dict(spins=len(isl), nominal=1 << len(isl), grammar_states=len(S1), nodes_visited=nodes1, nodes_visited_reverse_order=nodes2,
                     runtime_s=t1, two_orders_agree=(S1 == S2))
        if L in P:
            entry["equals_bruteforce_grammar_set"] = (S1 == {s for s in range(P[L]["N0"]) if P[L]["surv"][s]})
            okcons = okcons and entry["equals_bruteforce_grammar_set"]
        okcons = okcons and entry["two_orders_agree"]
        cons["%dx%d" % (L, L)] = entry
    rec("X1", "Constructive (backtracking) generation of S_G equals brute-force S_G (1x1, 2x2) and is order-independent (also 3x3 count; no energies computed for 3x3)",
        "EXHAUSTIVE_ENUMERATION", "PASS" if okcons else "FAIL", patches=cons)

    # ---- nulls ----------------------------------------------------------------------------------
    null_rows, null_agg, null_logs, ctrl = [], {}, {}, {}
    H_hash_before = hashlib.sha256(repr([P[L]["En"] for L in (1, 2)]).encode()).hexdigest()
    T_hash_before = hashlib.sha256(repr([P[L]["level_of"] for L in (1, 2)]).encode()).hexdigest()
    ok_unch = ok_pert = True
    for L, p in P.items():
        key = "%dx%d" % (L, L)
        inc, n = p["inc"], p["n"]
        u = gn.survivors(n, gn.unchanged_control(inc))
        pt = gn.survivors(n, gn.perturbed_control(inc))
        ctrl[key] = dict(unchanged_equals_real=(u == p["surv"]), perturbed_differs_from_real=(pt != p["surv"]),
                         perturbed_grammar=sum(pt), real_grammar=sum(p["surv"]),
                         perturbed_symdiff=sum(1 for a, b in zip(pt, p["surv"]) if a != b))
        ok_unch = ok_unch and ctrl[key]["unchanged_equals_real"]
        ok_pert = ok_pert and ctrl[key]["perturbed_differs_from_real"]
        for fam in ("DEGREE_PRESERVING_SWAP", "FREE_RANDOM_4SET"):
            nulls, log = gn.generate(fam, inc, n, N_NULLS)
            null_logs["%s|%s" % (key, fam)] = dict(log, valid_null_acceptance_rate=(log["accepted"] / log["tries"] if log["tries"] else None),
                                                    master_seed=gn.MASTER_SEED, requested=N_NULLS)
            rows = null_summaries(p, fam, nulls, inc)
            null_rows += rows
            if rows:
                ncomp = [r for r in rows if r["capacity_comparable"]]
                agg = dict(valid_nulls=len(rows), capacity_comparable=len(ncomp),
                           mean_contraction=sum(r["contraction"] for r in rows) / len(rows), real_contraction=1 - sum(p["surv"]) / p["N0"],
                           frac_same_survivor_set=sum(r["same_survivor_set_as_real"] for r in rows) / len(rows),
                           frac_preserve_ground=sum(r["FN_W0_ground"] == 0 for r in rows) / len(rows),
                           frac_as_far_as_real=sum(r["preserves_at_least_as_far_as_real"] for r in rows) / len(rows))
                if ncomp:
                    agg["comparable_frac_preserve_ground"] = sum(r["FN_W0_ground"] == 0 for r in ncomp) / len(ncomp)
                    agg["comparable_frac_as_far_as_real"] = sum(r["preserves_at_least_as_far_as_real"] for r in ncomp) / len(ncomp)
                if p["k_nonice"] is not None and p["k_nonice"] - 1 >= 1:
                    agg["frac_preserve_last_ice_window"] = sum(r["FN_W_last_ice_below_gap"] == 0 for r in rows) / len(rows)
                    if ncomp:
                        agg["comparable_frac_preserve_last_ice_window"] = sum(r["FN_W_last_ice_below_gap"] == 0 for r in ncomp) / len(ncomp)
            else:
                agg = dict(valid_nulls=0, note="no valid rewiring exists / all attempts rejected (see log)")
            null_agg["%s|%s" % (key, fam)] = agg
    H_hash_after = hashlib.sha256(repr([P[L]["En"] for L in (1, 2)]).encode()).hexdigest()
    T_hash_after = hashlib.sha256(repr([P[L]["level_of"] for L in (1, 2)]).encode()).hexdigest()
    rec("N1", "Unchanged-incidence control reproduces the real grammar exactly (null implementation check)", "STRUCTURAL_NULL_MONTE_CARLO",
        "PASS" if ok_unch else "FAIL", controls=ctrl)
    rec("N2", "Deliberately perturbed-incidence control changes the surviving set (null implementation check)", "STRUCTURAL_NULL_MONTE_CARLO",
        "PASS" if ok_pert else "FAIL", controls=ctrl)
    rec("N3", "Hamiltonian energies and physical target sets are bit-identical before and after null generation", "STRUCTURAL_NULL_MONTE_CARLO",
        "PASS" if (H_hash_before == H_hash_after and T_hash_before == T_hash_after) else "FAIL", H_sha_before=H_hash_before, H_sha_after=H_hash_after,
        targets_sha_before=T_hash_before, targets_sha_after=T_hash_after)
    p2fam = null_logs.get("2x2|DEGREE_PRESERVING_SWAP", {})
    have_nulls = null_agg.get("2x2|DEGREE_PRESERVING_SWAP", {}).get("valid_nulls", 0) > 0 and null_agg.get("2x2|FREE_RANDOM_4SET", {}).get("valid_nulls", 0) > 0
    rec("N4", "Valid structural nulls generated for 2x2 in both families with seeds, rejection reasons and acceptance rates logged (1x1 is structurally degenerate: see logs)",
        "STRUCTURAL_NULL_MONTE_CARLO", "PASS" if have_nulls else "FAIL", logs=null_logs, aggregates=null_agg)

    # ---- costs and comparators ------------------------------------------------------------------
    costs = {}
    for L, p in P.items():
        key = "%dx%d" % (L, L)
        # grammar-first accounting: filter the nominal space, energy would then be needed only for survivors
        t0 = time.perf_counter()
        surv_ids = [s_ for s_ in range(p["N0"]) if all(((s_ ^ nm) & im).bit_count() == 2 for im, nm in p["masks"])]
        t_filter = time.perf_counter() - t0
        costs[key] = dict(spins=p["n"], evaluated_configurations=p["N0"], pair_interactions_per_energy_evaluation=p["pairs"],
                          pair_interactions_nominal_space=p["N0"] * p["pairs"], pair_interactions_grammar_first_survivors_only=len(surv_ids) * p["pairs"],
                          **p["timing"], grammar_filter_over_nominal_space_s=t_filter, memory=p["memory"],
                          grammar_can_precede_energy=True,
                          caveat="Filtering by testing every nominal state costs O(|S0|) grammar checks; contraction translates into saved work only with constructive generation of S_G (see X1 nodes_visited) or a downstream solver whose cost scales with candidates.")
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # C1 oracle
    oracle = {}
    for L, p in P.items():
        key = "%dx%d" % (L, L)
        oracle[key] = dict(definition="survivors = {s : H(s) <= E0 + W} computed from the full Hamiltonian (target-aware; NOT a structural filter)",
                           false_exclusions=0, cost_energy_evaluations=p["N0"], cost_pair_interactions=p["N0"] * p["pairs"],
                           measured_full_energy_pass_s=p["timing"]["energy_eval_s"])
    comparators = dict(
        C1_exact_energy_oracle=dict(implemented=True, per_patch=oracle,
                                    statement="Best-case target-aware reference; reported only as a bound and never as a structural discovery."),
        E2_charged_local_estimator=dict(implemented=False, status="REQUIREMENTS_ONLY",
            requirements=["a precisely specified Hamiltonian-informed local estimator (e.g. truncated-interaction energy bound) fixed BEFORE primary comparison",
                          "charged costs: pair evaluations, any preprocessing or fitting, and every rejection decision",
                          "same downstream solver and same candidate universe as the grammar arm",
                          "no frozen SCR-III-B source defines this estimator; it is not invented in v006"]))
    rec("K1", "Computational feasibility measurements recorded separately from structural contraction (runtime, memory, evaluations, pair interactions, environment)",
        "MEASUREMENT", "PASS", costs=costs, ru_maxrss_kb=rss, environment=dict(platform=platform.platform(), python=sys.version.split()[0], machine=platform.machine(),
                                                                                  cpu_count=os.cpu_count()))

    # ---- non-tautology ----------------------------------------------------------------------------
    nt = {}
    nontrivial_windows = []
    for L, p in P.items():
        key = "%dx%d" % (L, L)
        kn = p["k_nonice"]
        pres_below = [w for w in p["windows"] if kn is not None and 0 < w["level"] < kn and w["false_exclusions"] == 0]
        nontriv = [w for w in pres_below if not w["target_equals_grammar_set"] and w["grammar_states_not_in_target"] > 0
                   and w["target"] > len(p["levels"][0]["members"])]
        taut = [w["level"] for w in pres_below if w["target_equals_grammar_set"]]
        for w in nontriv:
            nontrivial_windows.append((key, w["level"]))
        agg_s = null_agg.get("%s|DEGREE_PRESERVING_SWAP" % key, {}); agg_f = null_agg.get("%s|FREE_RANDOM_4SET" % key, {})
        if kn is None:
            cls = "INCONCLUSIVE"
        elif not nontriv:
            cls = "NO_NONTRIVIAL_WINDOW"
        else:
            cls = "NONTRIVIAL_PRESERVATION_CANDIDATE"
        nt[key] = dict(
            classification=cls, also_applicable=["GUARANTEED_ALIGNMENT (all windows below the first non-ice level)"],
            item1_preservation_follows_from_energy_bound=dict(answer=True, detail="For W < Delta_nonice every target state is ice-admissible by the definition of Delta_nonice, so preservation is a spectral fact of the frozen Hamiltonian, established here by exhaustive enumeration; no analytic bound for larger patches is derived in v006."),
            item2_requires_configuration_level_evaluation=dict(answer=True, detail="Delta_nonice is obtained only by evaluating H on configurations; the grammar never sees energies."),
            item3_grammar_tuned_to_target=dict(answer=False, detail="Grammar built from vertex incidence and orientation only (C1/C2 show it equals the geometric ice rule); energy_windows grammar functions take no energy input; windows were enumerated afterwards."),
            item4_target_differs_from_grammar=dict(answer=bool(nontriv), windows_where_target_equals_grammar_set=taut,
                                                  detail="A window whose target set equals S_G exactly is flagged as TAUTOLOGY_RISK and excluded from the nontrivial count."),
            item5_preservation_interval_beyond_ground=dict(answer=bool(nontriv), windows=[dict(level=w["level"], W_norm=w["W_norm"], W_J=w["W_J"], interval_upper_norm=w["interval_upper_norm"],
                                                                                              target=w["target"], grammar=w["grammar"], capacity=w["capacity_L_over_m"],
                                                                                              grammar_states_not_in_target=w["grammar_states_not_in_target"]) for w in nontriv]),
            item6_structural_nulls=dict(degree_preserving=agg_s, free_random=agg_f,
                                        reading="Exploratory. Compare frac_preserve_ground / frac_as_far_as_real of nulls with the real grammar (which preserves through the last ice-only window by construction of the enumeration)."))
    rec("T1", "Non-tautology assessment completed for every tested patch (six mandated questions answered with evidence)", "ANALYSIS", "PASS", assessment=nt)

    # ---- verdict ---------------------------------------------------------------------------------
    mand_fail = [t["id"] for t in TESTS if t["mandatory"] and t["status"] == "FAIL"]
    mand_unres = [t["id"] for t in TESTS if t["mandatory"] and t["status"] == "UNRESOLVED"]
    if mand_fail:
        verdict = "FEASIBILITY_FAIL"
    elif mand_unres:
        verdict = "FEASIBILITY_LIMITED"
    elif nontrivial_windows:
        verdict = "FEASIBILITY_PASS"
    else:
        verdict = "FEASIBILITY_LIMITED"

    unresolved = [
        "No downstream solver is defined; C_downstream and any net work saving are unmeasured (contraction is not a computational gain).",
        "E2 charged local estimator not implemented (requirements only): no frozen source defines it.",
        "Only 1x1 and 2x2 are exhaustively evaluated; 3x3 has a grammar count only (no energy windows).",
        "Single reference temperature 792 K (energy ordering is T-invariant by v005; windows scale with A(T)).",
        "Window boundaries here are exploratory, discovered by enumeration; primary windows must be frozen separately before any primary comparison.",
        "Nothing here extends to the published 24x24 arrays, v1.01 geometry-specific parameters, size disorder or the unmodified simulator.",
        "Null comparisons are exploratory; 1x1 admits no degree-preserving rewiring.",
    ]
    finished = datetime.datetime.now(datetime.timezone.utc).isoformat()
    rep.update(verdict=verdict, mandatory_failures=mand_fail, mandatory_unresolved=mand_unres, nontrivial_preservation_windows=nontrivial_windows,
               unresolved=unresolved, finished_utc=finished, v005_frozen_verdict=manifest5.get("verdict"),
               statement="Feasibility gate only. Not a physical-transfer result; no primary SCR verdict is issued; nothing is preregistered.",
               tests={t["id"]: t["status"] for t in TESTS})
    write_outputs(rep, P, allw, null_rows, null_logs, null_agg, costs, cons, comparators, nt, frozen_rows)
    print(json.dumps(dict(verdict=verdict, mandatory_failures=mand_fail, nontrivial=nontrivial_windows, tests=rep["tests"]), indent=1))
    return {"FEASIBILITY_PASS": 0, "FEASIBILITY_LIMITED": 0, "FEASIBILITY_FAIL": 1, "FEASIBILITY_BLOCKED": 2}[verdict]


def finish_blocked(rep, why):
    rep.update(verdict="FEASIBILITY_BLOCKED", reason=why, tests={}, unresolved=[why])
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "REPORT_v006.json").write_text(json.dumps(clean(rep), indent=1))
    (OUT / "REPORT_v006.md").write_text("# REPORT_v006\n\n**Verdict:** `FEASIBILITY_BLOCKED`\n\n%s\n" % why)
    print("FEASIBILITY_BLOCKED:", why)
    return 2


def fmt(x, nd=4):
    return "%.*g" % (nd, x) if isinstance(x, float) else str(x)


def write_outputs(rep, P, allw, null_rows, null_logs, null_agg, costs, cons, comparators, nt, frozen_rows):
    # WINDOWS csv
    cols = ["patch", "level", "W_norm", "W_J", "W_over_kT_ref", "interval_upper_norm", "level_energy_J", "level_members", "level_ice_members",
            "classification", "nominal", "grammar", "target", "surviving_targets", "false_exclusions", "preservation", "contraction", "target_density",
            "grammar_target_density", "capacity_L_over_m", "capacity_ok", "target_equals_grammar_set", "grammar_states_not_in_target"]
    with open(OUT / "WINDOWS_v006.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(cols)
        for r in allw:
            w.writerow([repr(r[c]) if isinstance(r[c], float) else r[c] for c in cols])
    with open(OUT / "TARGET_STATES_v006.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["patch", "state_id", "state_string(+/-,spin0 first)", "E_J", "E_minus_E0_J", "E_minus_E0_norm", "level_index (target if level<=k)",
                    "ice_rule_member", "violated_vertex_count", "in_counts_per_vertex", "vertex_type_counts_I;II;III;IV"])
        for p in P.values():
            for r in p["rows"]:
                w.writerow([repr(x) if isinstance(x, float) else x for x in r])
    ncols = ["family", "idx", "seed", "patch", "grammar", "contraction", "grammar_ratio_to_real", "capacity_comparable", "same_survivor_set_as_real",
             "survivor_symdiff_with_real", "first_failure_level", "real_first_failure_level", "preserves_at_least_as_far_as_real",
             "FN_W0_ground", "pres_W0_ground", "FN_W_last_ice_below_gap", "pres_W_last_ice_below_gap", "FN_W_first_nonice", "pres_W_first_nonice"]
    with open(OUT / "NULLS_v006.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(ncols)
        for r in null_rows:
            w.writerow([r.get(c, "") for c in ncols])
    P2 = P[2]
    feas = dict(costs=costs, constructive_enumeration=cons, comparators=comparators,
                cost_accounting_plan=dict(formula="C_total = C_filter + C_downstream",
                                          rules=["measure C_downstream for the SAME solver on the SAME candidate universe without the grammar filter",
                                                 "C_filter counts grammar evaluation (or constructive generation) plus any enumeration needed to apply it",
                                                 "report net gain G = 1 - C_total(SCR)/C_baseline only after a preregistered primary comparison",
                                                 "never equate structural contraction with solver work saved"]),
                null_logs=null_logs, null_aggregates=null_agg)
    (OUT / "FEASIBILITY_v006.json").write_text(json.dumps(clean(feas), indent=1))
    (OUT / "TESTS_v006.json").write_text(json.dumps(clean(TESTS), indent=1))
    detail = dict(rep)
    detail["patches"] = {("%dx%d" % (L, L)): dict(spins=p["n"], nominal=p["N0"], grammar=sum(p["surv"]), contraction=1 - sum(p["surv"]) / p["N0"],
                                                   A_J_at_792K=p["A_J"], E0_J=p["E0_J"], levels=len(p["levels"]), Delta_nonice_W_norm=p["delta_norm"],
                                                   Delta_nonice_W_J=None if p["delta_norm"] is None else p["A_J"] * p["delta_norm"],
                                                   first_nonice_level=p["k_nonice"], regimeC=p["regimeC"], windows=p["windows"][:p["k_nonice"] + 3] if p["k_nonice"] is not None else p["windows"][:5])
                         for L, p in P.items()}
    detail["non_tautology"] = nt
    (OUT / "REPORT_v006.json").write_text(json.dumps(clean(detail), indent=1))

    # markdown
    L_ = []
    L_.append("# REPORT_v006 — Energy-Window Feasibility and Non-Tautology Gate\n")
    L_.append("**Verdict:** `%s`\n" % rep["verdict"])
    L_.append("This is a feasibility preflight. It is **not** a physical-transfer result, issues no primary SCR verdict, and preregisters nothing. Frozen v005 hashes: test F1 = %s.\n" % rep["tests"].get("F1"))
    L_.append("## Combinatorial contraction (not computational gain)\n")
    L_.append("| Patch | Spins | Nominal | Grammar | Contraction | Levels | Δ_nonice (J) | first non-ice level |\n|---|---|---|---|---|---|---|---|")
    for L, p in P.items():
        L_.append("| %dx%d | %d | %d | %d | %.5f | %d | %s | %s |" % (L, L, p["n"], p["N0"], sum(p["surv"]), 1 - sum(p["surv"]) / p["N0"], len(p["levels"]),
                                                                fmt(p["A_J"] * p["delta_norm"]) if p["delta_norm"] is not None else "-", p["k_nonice"]))
    for L, p in P.items():
        L_.append("\n## %dx%d windows (first levels up to first failure +1)\n" % (L, L))
        L_.append("| k | W (J) | W / A | level size | ice in level | |S_T| | FN | preservation | capacity L/m | class |\n|---|---|---|---|---|---|---|---|---|---|")
        lim = (p["k_nonice"] + 2) if p["k_nonice"] is not None else 6
        for w in p["windows"][:lim]:
            L_.append("| %d | %s | %s | %d | %d | %d | %d | %.4f | %.3f | %s%s |" % (w["level"], fmt(w["W_J"]), fmt(w["W_norm"]), w["level_members"], w["level_ice_members"],
                                                                                   w["target"], w["false_exclusions"], w["preservation"], w["capacity_L_over_m"],
                                                                                   w["classification"], " (target == S_G: TAUTOLOGY_RISK)" if w["target_equals_grammar_set"] else ""))
        r = p["regimeC"]
        if r:
            fe = r["first_excluded"]
            L_.append("\n**Regime C (expected-failure control), %dx%d:** at level %d (W = %s J) the target gains %d non-ice states, all excluded by the grammar (false exclusions = %d). "
                      "First excluded: id %d `%s`, E = %s J, E−E0 = %s J, violated vertices %s." % (L, L, r["threshold_level"], fmt(r["W_J"]), r["false_exclusion_count"], r["false_exclusion_count"],
                                                                                             fe["id"], fe["state"], fmt(fe["energy_J"]), fmt(fe["energy_above_E0_J"]), fe["violated_vertices"]))
            L_.append("Target before: %d states; after: %d; kept by grammar: %d (ids in `REPORT_v006.json`)." % (len(r["target_before_ids"]), len(r["target_after_ids"]), len(r["kept_after_filter_ids"])))
    L_.append("\n## Non-tautology assessment\n")
    for key, a in nt.items():
        L_.append("- **%s: %s.** %s Windows beyond ground: %s." % (key, a["classification"], a["item1_preservation_follows_from_energy_bound"]["detail"],
                                                                 [(w["level"], w["target"], w["grammar"]) for w in a["item5_preservation_interval_beyond_ground"]["windows"]] or "none"))
    L_.append("\nPreservation below Δ_nonice is a *spectral fact of the frozen Hamiltonian* established by enumeration; it is guaranteed-aligned, not an independent proof of transfer. Windows whose target set equals S_G are flagged and excluded from the nontrivial count.")
    L_.append("\n## Structural nulls (2×2, exploratory)\n")
    for k, a in null_agg.items():
        if k.startswith("2x2"):
            L_.append("- %s: %s" % (k, json.dumps(clean(a))))
    L_.append("\nControls: unchanged-incidence reproduces the real grammar (N1); perturbed-incidence differs (N2); energies and targets unchanged (N3). Seeds are `%d|family|index`; acceptance rates in `FEASIBILITY_v006.json`." % gn.MASTER_SEED)
    L_.append("\n## Computational cost (separate from contraction)\n")
    for k, c in costs.items():
        L_.append("- %s: %d configs, %d pair interactions per evaluation; grammar pass %.2e s vs energy pass %.2e s (%.2f µs vs %.2f µs per state); grammar can precede energy: %s." % (
            k, c["evaluated_configurations"], c["pair_interactions_per_energy_evaluation"], c["grammar_eval_s"], c["energy_eval_s"], c["grammar_per_state_us"], c["energy_per_state_us"], c["grammar_can_precede_energy"]))
    for k, c in cons.items():
        L_.append("- constructive S_G generation %s: %d grammar states, %d search nodes vs %d nominal states." % (k, c["grammar_states"], c["nodes_visited"], c["nominal"]))
    L_.append("\n## Test summary\n\n| ID | Test | Evidence | Status |\n|---|---|---|---|")
    for t in TESTS:
        L_.append("| %s | %s | %s | **%s** |" % (t["id"], t["title"], t["evidence_level"], t["status"]))
    L_.append("\n## Unresolved / out of scope\n")
    for u in rep["unresolved"]:
        L_.append("- " + u)
    L_.append("\n## Next step\n\nIf the verdict is FEASIBILITY_PASS: draft `SCR_III_B_SPEC_v001.md` and a separately frozen primary preregistration (windows frozen *before* any primary comparison). Nothing is frozen by this package.")
    (OUT / "REPORT_v006.md").write_text("\n".join(L_) + "\n")

    # manifest
    mf = dict(version="v006", verdict=rep["verdict"], code={}, outputs={}, frozen_v005_check=dict(files=len(frozen_rows), mismatches=[r["file"] for r in frozen_rows if not r["match"]]))
    for name in ("validate_v006.py", "energy_windows_v006.py", "grammar_nulls_v006.py", "test_v006.py", "README_v006.md"):
        p = HERE / name
        mf["code"][name] = sha_file(p) if p.exists() else None
    for name in ("REPORT_v006.json", "REPORT_v006.md", "WINDOWS_v006.csv", "TARGET_STATES_v006.csv", "NULLS_v006.csv", "FEASIBILITY_v006.json", "TESTS_v006.json"):
        mf["outputs"][name] = sha_file(OUT / name)
    mf["note"] = "Outputs contain timing and timestamps; their hashes are per-run records, not cross-machine invariants."
    (OUT / "MANIFEST_v006.json").write_text(json.dumps(mf, indent=1))


if __name__ == "__main__":
    sys.exit(main())
