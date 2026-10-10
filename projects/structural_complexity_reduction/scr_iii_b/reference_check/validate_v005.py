#!/usr/bin/env python3
"""SCR-III-B PREFLIGHT_v005 -- physical energy and Hamiltonian convention lock.

Run from the project root (Ubuntu/WSL):   python3 scr_iii_b/reference_check/validate_v005.py

Exit status: 0 = PHYSICAL_HAMILTONIAN_LOCK_PASS or _PARTIAL (a PARTIAL verdict is a valid scientific outcome),
             1 = PHYSICAL_HAMILTONIAN_LOCK_FAIL, 2 = PREFLIGHT_EXECUTION_BLOCKED.
Never modifies originals, v001-v004 outputs, SCR-III-A, or GitHub. Writes only scr_iii_b/output/validation/v005/
and a compiled probe binary inside that directory.
"""
import hashlib, json, os, pathlib, re, subprocess, sys, tempfile, zipfile, csv, datetime, random, platform

HERE = pathlib.Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
SCR = PROJECT / "scr_iii_b"
sys.path.insert(0, str(HERE))
import physical_energy_v005 as pe  # noqa: E402

OUT = SCR / "output" / "validation" / "v005"
SPMMC_ZIP = SCR / "references" / "public_code" / "SPMMC_Code.zip"
MMC_ZIP = SCR / "references" / "public_code" / "MMC_Code.zip"
README = SCR / "references" / "square_ice_model" / "Dryad_README.md"
PROBE_SRC = HERE / "source_probe_v005.cpp"
BIN = OUT / "source_probe_v005.bin"
EXPECTED = {
    "SPMMC_Code.zip": "77c82d83ea20eff5abcab8323b061edf759809cdd4366e86042147f6ea60a5dd",
    "Dryad_README.md": "b0f39ada4049248934db140fca396d3f3824e31094543c8b1c60d3a66e336f64",
    "SPMMC-SSI-Unix-v1.00.cpp": "f7ffe5ff3bdff923e1281c3ed7431dfece5ce0c596ffe3f60a5b037908ab750a",
    "MMC-SSI-Unix-v1.00.cpp": "bd4f2e7a139817f7cee71d413d01f8296dcc31b5649bca086c26970d70b8cbc0",
}
TEMPS = [760.0, 780.0, 792.0, 805.0, 815.0]   # all inside 0<T<Tc; 760-792 K is the source default window
T_REF = 792.0
LEVEL = {"U": "UNMODIFIED_SIMULATOR_EXECUTION", "V": "VERBATIM_ORIGINAL_SOURCE_FUNCTIONS_IN_PROBE",
         "P": "SOURCE_DERIVED_INDEPENDENT_PYTHON", "T": "PREVIOUSLY_TRANSCRIBED_V002_V004_FORMULAS",
         "S": "STATIC_SOURCE_TEXT_ANALYSIS"}
TESTS = []


def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""):
            h.update(ch)
    return h.hexdigest()


def sha_text(t):
    return hashlib.sha256(t.encode()).hexdigest()


def rec(tid, title, level, status, mandatory=True, applies=True, challenges="", **detail):
    """status: PASS | FAIL | UNRESOLVED | INFO | FINDING | NOT_APPLICABLE"""
    TESTS.append(dict(id=tid, title=title, evidence_level=LEVEL[level], status=status, mandatory=mandatory,
                      invariant_applies=applies, challenged_assumption=challenges, detail=detail))
    return status


class Blocked(Exception):
    pass


# ----------------------------------------------------------------- provenance / sources
def load_sources(tmp):
    for p in (SPMMC_ZIP, MMC_ZIP, README):
        if not p.exists():
            raise Blocked("required original source missing: %s" % p)
    got = {"SPMMC_Code.zip": sha_file(SPMMC_ZIP), "MMC_Code.zip": sha_file(MMC_ZIP), "Dryad_README.md": sha_file(README)}
    texts = {}
    for name, z in (("SPMMC-SSI-Unix-v1.00.cpp", SPMMC_ZIP), ("MMC-SSI-Unix-v1.00.cpp", MMC_ZIP)):
        with zipfile.ZipFile(z) as zf:
            member = [m for m in zf.namelist() if m.endswith(name)]
            if not member:
                raise Blocked("%s not found inside %s" % (name, z))
            data = zf.read(member[0])
        (tmp / name).write_bytes(data)
        got[name] = hashlib.sha256(data).hexdigest()
        texts[name] = data.decode("utf-8", errors="replace").split("\n")
    return got, texts


def func_block(lines, name):
    for i, l in enumerate(lines):
        if re.match(r"^(double|void|int|unsigned int)\s+" + re.escape(name) + r"\s*\(", l):
            j = i
            while not lines[j].startswith("}//"):
                j += 1
            return i + 1, j + 1, "\n".join(lines[i:j + 1])
    return None


def find_line(lines, pattern, start=0):
    rx = re.compile(pattern)
    for i in range(start, len(lines)):
        if rx.search(lines[i]):
            return i + 1
    return None


def norm_ws(t):
    return re.sub(r"\s+", "", t)


def check_provenance(got, texts):
    # MMC_Code.zip has no v004 hash record: it is hashed here for the first time (reported, not compared).
    ok = all(got[k] == v for k, v in EXPECTED.items()) and "MMC_Code.zip" in got and len(got["MMC_Code.zip"]) == 64
    rec("P1", "Original-source files present; SHA-256 equals the v004 provenance record", "S",
        "PASS" if ok else "FAIL", sha256=got, expected_from_v004_record=EXPECTED,
        first_recorded_in_v005=["MMC_Code.zip"])
    # verbatim blocks in probe vs original
    probe = PROBE_SRC.read_text().split("\n")
    sp = texts["SPMMC-SSI-Unix-v1.00.cpp"]
    bad, n = [], 0
    for i, l in enumerate(probe):
        m = re.match(r"^// BEGIN VERBATIM (\w+) (\S+) original_lines=(\d+)-(\d+) sha256=([0-9a-f]{64})$", l)
        if not m:
            continue
        n += 1
        kind, name, a, b, h = m.group(1), m.group(2), int(m.group(3)), int(m.group(4)), m.group(5)
        j = i + 1
        body = []
        while not probe[j].startswith("// END VERBATIM"):
            body.append(probe[j]); j += 1
        text = "\n".join(body)
        orig = "\n".join(sp[a - 1:b])
        if sha_text(text) != h or text != orig:
            bad.append(name)
    rec("P2", "Every VERBATIM block in the probe is byte-identical to the original line range", "S",
        "PASS" if (n > 0 and not bad) else "FAIL", blocks_checked=n, mismatches=bad)


# ----------------------------------------------------------------- probe I/O
def build_probe():
    if not PROBE_SRC.exists():
        raise Blocked("probe source missing")
    OUT.mkdir(parents=True, exist_ok=True)
    cc = os.environ.get("CXX", "g++")
    try:
        p = subprocess.run([cc, "-std=c++17", "-O2", str(PROBE_SRC), "-o", str(BIN)], capture_output=True, text=True)
    except FileNotFoundError:
        raise Blocked("C++ compiler '%s' not found" % cc)
    if p.returncode:
        raise Blocked("probe compile failed:\n" + p.stderr[-3000:])
    return cc


def run_probe(L, T, confs=(), vertex=0, cutoff=-1.0, scale=1.0, kappa=1.0, lat=-1.0):
    stdin = "%d %d %r %r %r %r %r %d\n" % (L, vertex, cutoff, scale, T, kappa, lat, len(confs))
    stdin += "".join(c + "\n" for c in confs)
    p = subprocess.run([str(BIN)], input=stdin, capture_output=True, text=True)
    if p.returncode:
        raise Blocked("probe run failed (rc=%d): %s" % (p.returncode, p.stderr[-500:]))
    d = dict(dipoles=[], vertices=[], web={}, confs=[], logcounts=None)
    cur = None
    for line in p.stdout.split("\n"):
        t = line.split()
        if not t:
            continue
        k = t[0]
        if k == "META":
            d["meta"] = dict(N=int(t[1]), V=int(t[2]), Tc=float(t[3]), M0=float(t[4]), beta=float(t[5]),
                             h=float(t[6]), a=float(t[7]), kappa=float(t[8]))
        elif k == "DIPOLE":
            d["dipoles"].append(dict(x=float(t[2]), y=float(t[3]), ux=float(t[4]), uy=float(t[5]),
                                     l=float(t[6]), w=float(t[7]), V=float(t[8]), f=float(t[9])))
        elif k == "VERTEX":
            d["vertices"].append(dict(x=float(t[2]), y=float(t[3]), islands=[int(v) for v in t[4:]]))
        elif k == "WEB":
            d["web"][(int(t[1]), int(t[2]))] = float(t[3])
        elif k == "CONF":
            cur = dict(s=t[1], types=[float(v) for v in t[3:7]])
            d["confs"].append(cur)
        elif k in ("H", "DX", "HINC", "RTINC"):
            cur[k] = [float(v) for v in t[1:]]
        elif k == "LOGCOUNTS":
            d["logcounts"] = [int(v) for v in t[1:]]
    return d


def s2str(sid, n):
    return "".join("+" if (sid >> i) & 1 else "-" for i in range(n))


def mask_state(sid, n):
    return pe.decode(sid, n)


# ----------------------------------------------------------------- numerical policy
def policy(K_scale):
    return dict(
        normalized_dimensionless=dict(rtol=1e-11, atol=1e-13 * max(K_scale, 1e-3),
                                      note="pure double-precision math; atol scaled to the largest |K|"),
        joule_python_only=dict(rtol=1e-12, atol_J=1e-12 * pe.A_joule(T_REF) * max(K_scale, 1e-3)),
        joule_vs_source_constant=dict(rtol=2e-6, note="source hard-codes mu0/kB-derived constant 0.910179 K "
                                      "(exact value %.9f): expected systematic relative offset %.3e"
                                      % (pe.MU0 * 1e10 * 1e-27 / pe.KB, 0.910179 / (pe.MU0 * 1e10 * 1e-27 / pe.KB) - 1)),
        zero_handling="errors are |a-b|/max(|a|,|b|,atol); quantities below atol are treated as zero (ratios skipped)",
        v004_normalized_abs_tol_not_applied_to_joules=True)


# ----------------------------------------------------------------- tests
def test_geometry_and_coupling():
    res = {}
    allok = True
    for L in (1, 2, 3):
        d = run_probe(L, T_REF)
        isl = pe.source_geometry(L)
        gd = max(max(abs(p["x"] - q.x), abs(p["y"] - q.y), abs(p["ux"] - q.ux), abs(p["uy"] - q.uy))
                 for p, q in zip(d["dipoles"], isl))
        inc = pe.incident_islands(isl, pe.vertex_positions(L))
        vset = all(set(v["islands"]) == set(i) for v, i in zip(d["vertices"], inc))
        n = len(isl)
        kerr, sym = 0.0, 0.0
        for (i, j), k in d["web"].items():
            kp = pe.K_pair(isl[i], isl[j])
            kerr = max(kerr, abs(k - kp))
            sym = max(sym, abs(k - d["web"][(j, i)]))
        pol = (len(d["dipoles"]) == 2 * L * (L + 1)) and (len(d["web"]) == n * (n - 1))
        ok = gd < 1e-9 and vset and kerr < 1e-13 and sym < 1e-13 and pol
        allok = allok and ok
        res[L] = dict(spins=n, vertices=len(d["vertices"]), ordered_pairs=len(d["web"]), geometry_max_abs_nm=gd,
                      vertex_incidence_match=vset, max_abs_K_python_vs_verbatim=kerr, max_abs_K_asymmetry=sym,
                      spins_equals_2L_L_plus_1=len(d["dipoles"]) == 2 * L * (L + 1))
    rec("E1", "Geometry (coordinates, unit vectors, free-boundary vertex incidence): python vs verbatim initialize_dipole_system/initialize_vertex_system",
        "V", "PASS" if allok else "FAIL", challenges="lattice spacing, orientation, endpoints, free boundary", per_L=res)
    rec("E2", "Pair coupling K_ij and all-pair web (no cutoff, no self-term): python vs verbatim; symmetry for identical islands",
        "V", "PASS" if allok else "FAIL", challenges="included pairs, self-terms, formula prefactors", per_L=res)
    return allok


def test_charge_model():
    isl = pe.source_geometry(2)
    worst, worst_m = 0.0, 0.0
    for T in (760.0, 792.0, 815.0):
        A = pe.A_joule(T)
        M = pe.moment_M(T)
        q = (pe.pi / 4) * M * 60e-9 * 15e-9
        worst_m = max(worst_m, abs(q * (2 * 160e-9 / 3) - M * pe.island_volume_m3()) / (M * pe.island_volume_m3()))
        for i in range(len(isl)):
            for j in range(i + 1, len(isl)):
                u = pe.pair_energy_charge_model_J(isl[i], isl[j], T)
                v = A * pe.K_pair(isl[i], isl[j])
                worst = max(worst, abs(u - v) / max(abs(u), abs(v), 1e-40))
    rec("E3", "Physical Coulomb dumbbell energy (explicit charges, SI) equals A(T)*K_ij (fixes 3/16 normalisation, q=(pi/4)Mwh, moment=MV)",
        "P", "PASS" if (worst < 1e-9 and worst_m < 1e-12) else "FAIL",
        challenges="magnetic moment, charge magnitude and placement, units, prefactors",
        max_rel_err_pair_energy=worst, max_rel_err_dumbbell_moment_vs_MV=worst_m)


def conf_ids(L):
    n = 2 * L * (L + 1)
    if L <= 2:
        return list(range(1 << n)), n
    rng = random.Random(20261009)
    return [rng.getrandbits(n) for _ in range(48)], n


def test_fields_and_flips():
    out = {}
    allok = True
    c_exact = pe.MU0 * 1e10 * 1e-27 / pe.KB
    ratio_expected = 0.910179 / c_exact
    for L in (1, 2, 3):
        ids, n = conf_ids(L)
        isl = pe.source_geometry(L)
        pairs = pe.K_pairs(isl)
        Kmax = max(abs(k) for _, _, k in pairs)
        for T in ([T_REF] if L == 3 else TEMPS):
            d = run_probe(L, T, [s2str(s, n) for s in ids])
            f = [p["f"] for p in d["dipoles"]]
            herr = nerr = jerr = ratio_dev = hinc = rtinc = 0.0
            for sid, c in zip(ids, d["confs"]):
                st = pe.decode(sid, n)
                hp = pe.local_fields(st, pairs, n)
                herr = max(herr, max(abs(a - b) for a, b in zip(hp, c["H"])))
                e0n = pe.energy_norm(st, pairs)
                for k in range(n):
                    st2 = list(st); st2[k] = -st2[k]
                    direct_n = pe.energy_norm(st2, pairs) - e0n
                    via_h = pe.flip_delta_norm(st, k, hp)
                    src_n = -c["DX"][k] / f[k]            # kappa=1: dE/A = -DX/(kappa f)
                    nerr = max(nerr, abs(direct_n - via_h), abs(direct_n - src_n))
                    dJ_py = pe.A_joule(T) * direct_n
                    dJ_src = -pe.KB * T * c["DX"][k]
                    atol = 1e-12 * pe.A_joule(T) * Kmax
                    if abs(dJ_py) > 1e-6 * pe.A_joule(T) * Kmax:
                        jerr = max(jerr, abs(dJ_src - dJ_py) / abs(dJ_py))
                        ratio_dev = max(ratio_dev, abs(dJ_src / dJ_py - ratio_expected))
                hinc = max(hinc, max(c["HINC"])); rtinc = max(rtinc, max(c["RTINC"]))
            clip = d["logcounts"]
            good = (herr < 1e-12 and nerr < 1e-11 and jerr < 2e-6 and ratio_dev < 1e-9 and hinc < 1e-14 and rtinc < 1e-9
                    and not any(clip))
            allok = allok and good
            out["L%d_T%g" % (L, T)] = dict(configs=len(ids), max_abs_H_python_vs_verbatim=herr,
                                          max_abs_dEnorm_direct_vs_fieldformula_vs_source=nerr,
                                          max_rel_dEJ_source_vs_python=jerr,
                                          max_dev_of_observed_over_expected_constant_ratio=ratio_dev,
                                          expected_source_over_exact_constant_ratio=ratio_expected,
                                          max_abs_incremental_vs_full_field_update=hinc,
                                          max_abs_incremental_vs_fresh_log_reversal_time=rtinc,
                                          exponent_clip_events=clip, pass_=good)
    rec("E4", "Local interaction field h_i = sum_j K_ij s_j: python vs verbatim initialize_dipole_athermal_interaction_fields",
        "V", "PASS" if allok else "FAIL", challenges="field expression and its relation to energy", cases=out)
    rec("E5", "Single-spin-flip dE = -2 A s_i h_i: verbatim update_reference_dipole_reversal_time vs python direct subtraction (normalised and joules)",
        "V", "PASS" if allok else "FAIL",
        challenges="dE definition, sign and factor; double counting; joule scale",
        note="Joule agreement is tested against the predicted systematic offset caused by the source's rounded constant 0.910179 (not by a tolerance fudge).",
        cases=out)
    rec("E6", "Incremental field / reversal-time updates (verbatim update_interaction_fields) agree with fresh recomputation (identical islands)",
        "V", "PASS" if allok else "FAIL", challenges="consistency of ΔE update bookkeeping", cases=out)
    return allok


def enumerate_patch(L):
    isl = pe.source_geometry(L)
    pairs = pe.K_pairs(isl)
    n = len(isl)
    vpos = pe.vertex_positions(L)
    En = [pe.energy_norm(pe.decode(s, n), pairs) for s in range(1 << n)]
    ice = [pe.ice_ok_geometric(pe.decode(s, n), isl, vpos) for s in range(1 << n)]
    return isl, pairs, n, En, ice


def canon_order(vals, digits=11):
    """Tie-robust ordering: values equal to ~1e-11 relative are one level (exact-degenerate states differ by roundoff)."""
    sc = max(abs(v) for v in vals) or 1.0
    return sorted(range(len(vals)), key=lambda i: (round(vals[i] / sc, digits), i))


def summarise(En, ice, T, n, tol=1e-14):
    A = pe.A_joule(T)
    emin = min(En)
    ground = [s for s, e in enumerate(En) if abs(e - emin) <= tol * max(1.0, abs(emin))]
    ei = min((e for e, g in zip(En, ice) if g), default=None)
    en_ = min((e for e, g in zip(En, ice) if not g), default=None)
    return dict(T=T, A_J=A, ground_E_J=A * emin, ground_E_norm=emin, degeneracy=len(ground), ground_ids=ground,
                ground_all_ice=all(ice[s] for s in ground), min_ice_E_J=None if ei is None else A * ei,
                min_nonice_E_J=None if en_ is None else A * en_,
                gap_nonice_minus_ice_J=None if (ei is None or en_ is None) else A * (en_ - ei),
                gap_minimum_ice_above_ground_J=None if ei is None else A * (ei - emin),
                gap_minimum_nonice_above_ground_J=None if en_ is None else A * (en_ - emin))


def test_enumeration_and_temperature(src_texts):
    res = dict(patches={})
    csv_ground, csv_temp = [], []
    ok_all = True
    for L in (1, 2):
        isl, pairs, n, En, ice = enumerate_patch(L)
        d = run_probe(L, T_REF, [s2str(s, n) for s in range(1 << n)])
        # ice classification: python geometric vs verbatim vertex statistics
        mism = 0
        for s, c in enumerate(d["confs"]):
            ice_src = abs(c["types"][0] + c["types"][1] - 1.0) < 1e-9
            mism += (ice_src != ice[s])
        n_ice = sum(ice)
        base = summarise(En, ice, T_REF, n)
        gtypes = []
        for s in base["ground_ids"]:
            gtypes.append(d["confs"][s]["types"])
        # temperature
        tinfo = []
        rank_ok = True
        ref_rank = canon_order(En)
        for T in TEMPS:
            sm = summarise(En, ice, T, n)
            ET = [pe.A_joule(T) * e for e in En]
            sp = pe.spearman(En, ET)
            same_rank = canon_order(ET) == ref_rank
            rank_ok = rank_ok and same_rank and sm["ground_ids"] == base["ground_ids"] and sm["degeneracy"] == base["degeneracy"]
            ratio = pe.A_joule(T) / pe.A_joule(T_REF)
            tinfo.append(dict(T=T, M_A_per_m=pe.moment_M(T), A_J=sm["A_J"], A_over_Aref=ratio,
                              analytic_ratio=((1 - T / 820.0) / (1 - T_REF / 820.0)), spearman_vs_ref=sp,
                              identical_rank_order=same_rank, ground_ids=sm["ground_ids"], degeneracy=sm["degeneracy"],
                              ground_E_J=sm["ground_E_J"], min_ice_E_J=sm["min_ice_E_J"],
                              min_nonice_E_J=sm["min_nonice_E_J"], gap_nonice_minus_ice_J=sm["gap_nonice_minus_ice_J"]))
            csv_temp.append([L, T, pe.moment_M(T), sm["A_J"], ratio, ((1 - T / 820.0) / (1 - T_REF / 820.0)), sp, same_rank,
                             sm["degeneracy"], ";".join(map(str, sm["ground_ids"])), sm["ground_E_J"], sm["min_ice_E_J"],
                             sm["min_nonice_E_J"], sm["gap_nonice_minus_ice_J"]])
        # legacy regression
        Eleg = [pe.energy_norm_legacy_v004(pe.decode(s, n), pairs) for s in range(1 << n)]
        # v004 used height 16 -> uniform K scale 16/15: ordering unchanged; reproduce v004 numbers
        pairs16 = pe.K_pairs(isl, h=16.0)
        Eleg16 = [-pe.energy_norm(pe.decode(s, n), pairs16) for s in range(1 << n)]
        leg = summarise(Eleg16, ice, T_REF, n)
        res["patches"]["%dx%d" % (L, L)] = dict(
            spins=n, configurations=1 << n, ice_states_python_geometric=n_ice,
            ice_states_verbatim_vertex_statistics=sum(1 for c in d["confs"] if abs(c["types"][0] + c["types"][1] - 1.0) < 1e-9),
            ice_classification_mismatches_python_vs_verbatim=mism, **{k: v for k, v in base.items() if k != "T"},
            ground_vertex_type_fractions_verbatim=gtypes,
            ground_states_all_type1_vertices=all(abs(t[0] - 1.0) < 1e-9 for t in gtypes),
            physical_vs_normalized_rank_identical=True,
            temperature_series=tinfo, temperature_order_invariant=rank_ok,
            legacy_v004_regression=dict(convention="E=-sum K s s with h=16 nm (v001-v004)", ground_E_norm=leg["ground_E_norm"],
                                        degeneracy=leg["degeneracy"], ground_all_ice=leg["ground_all_ice"],
                                        min_ice_E_norm=leg["min_ice_E_J"] / leg["A_J"], min_nonice_E_norm=leg["min_nonice_E_J"] / leg["A_J"]),
            legacy_energy_is_exact_negative_of_source_derived=all(abs(a + b) < 1e-14 for a, b in zip(Eleg, En)))
        for s in base["ground_ids"]:
            csv_ground.append([L, "SPMMC_v1.00_all_pair_verified_sign(+)", T_REF, s, s2str(s, n), base["ground_E_J"], base["ground_E_norm"], ice[s], d["confs"][s]["types"]])
        for s in leg["ground_ids"]:
            csv_ground.append([L, "legacy_v001-v004_sign(-)_REGRESSION_ONLY", T_REF, s, s2str(s, n), None, leg["ground_E_norm"], ice[s], None])
        ok_all = ok_all and mism == 0 and rank_ok
    # records
    p1, p2 = res["patches"]["1x1"], res["patches"]["2x2"]
    rec("E7", "Ice-rule classification (2-in/2-out at every vertex): independent geometric rule vs verbatim compute_vertex_statistics (all 16 and 4096 states)",
        "V", "PASS" if (p1["ice_classification_mismatches_python_vs_verbatim"] == 0 and p2["ice_classification_mismatches_python_vs_verbatim"] == 0
                        and p1["ice_states_python_geometric"] == 6 and p2["ice_states_python_geometric"] == 82) else "FAIL",
        challenges="spin orientation, charge placement, vertex incidence", ice_1x1=p1["ice_states_python_geometric"], ice_2x2=p2["ice_states_python_geometric"])
    rec("E10", "Exact 1x1 and 2x2 enumeration under the verified model: ground states, ice verdict, gaps, degeneracy",
        "P", "PASS" if ok_all else "FAIL", challenges="whether the v001-v004 non-ice minima survive the verified conventions", summary=res)
    return res, csv_ground, csv_temp, ok_all


def reconstruct_landscape_and_scaling():
    """Source-derived energy landscape (from verbatim flip energies) vs python; temperature scaling of source flips."""
    L = 2
    isl, pairs, n, En, ice = enumerate_patch(L)
    ids = list(range(1 << n))
    per_T = {}
    dE_by_T = {}
    ok = True
    c_exact = pe.MU0 * 1e10 * 1e-27 / pe.KB
    for T in TEMPS:
        d = run_probe(L, T, [s2str(s, n) for s in ids])
        dE = [[-pe.KB * T * x for x in c["DX"]] for c in d["confs"]]
        dE_by_T[T] = dE
        # antisymmetry (edge s->s^k and back) and BFS potential
        asym = 0.0
        for s in ids:
            for k in range(n):
                asym = max(asym, abs(dE[s][k] + dE[s ^ (1 << k)][k]))
        E = {0: 0.0}
        queue = [0]
        for s in queue:
            for k in range(n):
                t = s ^ (1 << k)
                if t not in E:
                    E[t] = E[s] + dE[s][k]; queue.append(t)
        closure = 0.0
        for s in ids:
            for k in range(n):
                closure = max(closure, abs((E[s ^ (1 << k)] - E[s]) - dE[s][k]))
        A = pe.A_joule(T)
        span = A * (max(En) - min(En))
        diff = max(abs((E[s] - E[0]) - A * (En[s] - En[0])) for s in ids) * (0.910179 / c_exact) ** 0  # absolute J
        # allowed difference: systematic constant ratio only
        pred = max(abs((E[s] - E[0]) - (0.910179 / c_exact) * A * (En[s] - En[0])) for s in ids)
        per_T[T] = dict(antisymmetry_max_abs_J=asym, potential_closure_max_abs_J=closure, energy_range_J=span,
                        max_abs_J_diff_vs_python=diff, max_abs_J_diff_vs_python_after_known_constant_ratio=pred,
                        ground_id_from_source_landscape=min(ids, key=lambda s: (E[s], s)))
        ok = ok and asym < 1e-9 * span and closure < 1e-9 * span and pred < 1e-9 * span and diff < 2e-6 * span * 1.0000001 + 1e-30
    ref = dE_by_T[T_REF]
    scal = {}
    worst = 0.0
    for T in TEMPS:
        r = pe.A_joule(T) / pe.A_joule(T_REF)
        w = 0.0; cnt = 0
        thr = 1e-6 * pe.A_joule(T_REF) * max(abs(k) for _, _, k in pairs)
        for s in ids:
            for k in range(n):
                if abs(ref[s][k]) > thr:
                    w = max(w, abs(dE_by_T[T][s][k] / ref[s][k] - r) / r); cnt += 1
        scal[T] = dict(expected_ratio=r, max_rel_deviation_of_source_flip_ratio=w, flips_compared=cnt,
                       zero_flips_skipped=len(ids) * n - cnt)
        worst = max(worst, w)
    rec("E8", "Source-derived energy landscape from verbatim flip energies is a single-valued potential equal to python H up to the known constant ratio",
        "V", "PASS" if ok else "FAIL", challenges="direct subtraction vs ΔE consistency; absolute energy convention", per_T=per_T)
    # E(s,T) = A(T) E_ref(s) + B(T)
    Tm = [T for T in TEMPS]
    resid = 0.0
    for T in Tm:
        A_ratio = pe.A_joule(T) / pe.A_joule(T_REF)
        for s in ids[::37]:
            resid = max(resid, abs(pe.A_joule(T) * En[s] - A_ratio * pe.A_joule(T_REF) * En[s]))
    dom_ok = False
    try:
        pe.moment_M(820.0)
    except ValueError:
        dom_ok = True
    tcheck = dict(analytic="E(s,T)=A(T)E_ref(s)+B(T), A(T)=kappa mu0 M0^2 V (1-T/Tc)^(2 beta)/2 >0 for T<Tc, B(T)=0",
                  flip_ratio_scaling=scal, worst_rel_dev=worst, curie_domain_guard_raises_at_Tc=dom_ok,
                  uniform_scaling_established=worst < 1e-9 and dom_ok,
                  ordering_vs_thermal_sampling=("Hamiltonian ordering is T-invariant; Boltzmann probabilities exp(-E/kT) and the "
                                                "fixed-timestep SPMMC kinetics are NOT: ratio A/kT varies with T."))
    rec("E9", "Temperature-dependent magnetization: E(s,T)=A(T)E_ref(s) with A>0, B=0; ordering, ground set, degeneracy, flip-ΔE scaling at 5 temperatures",
        "V", "PASS" if tcheck["uniform_scaling_established"] else "FAIL", challenges="temperature-dependent magnetization and energy scaling",
        no_extrapolation="T >= Tc rejected by the evaluator; supported domain tested: 760-815 K (<Tc=820 K)", **tcheck)
    # analytic f*T ratio from verbatim factors (L=1 quick)
    d = {T: run_probe(1, T)["dipoles"][0]["f"] for T in TEMPS}
    fr = max(abs((d[T] * T) / (d[T_REF] * T_REF) - ((1 - T / 820.0) / (1 - T_REF / 820.0)) ** 1.0) for T in TEMPS)
    rec("E9b", "Verbatim reduced-temperature factor: f(T)*T ∝ (1-T/Tc)^(2 beta) (beta=0.5) exactly", "V",
        "PASS" if fr < 1e-12 else "FAIL", challenges="magnetization exponent", max_abs_dev=fr)
    return per_T, scal, ok and tcheck["uniform_scaling_established"]


def test_adversarial(src_texts):
    sp = src_texts["SPMMC-SSI-Unix-v1.00.cpp"]; mm = src_texts["MMC-SSI-Unix-v1.00.cpp"]
    L = 2
    isl, pairs, n, En, ice = enumerate_patch(L)
    # A1 global reversal
    worst = max(abs(En[s] - En[(~s) & ((1 << n) - 1)]) for s in range(1 << n))
    d = run_probe(L, T_REF, [s2str(s, n) for s in range(0, 1 << n, 17)] + [s2str((~s) & ((1 << n) - 1), n) for s in range(0, 1 << n, 17)])
    m = len(d["confs"]) // 2
    hs = max(max(abs(a + b) for a, b in zip(d["confs"][i]["H"], d["confs"][i + m]["H"])) for i in range(m))
    dxs = max(max(abs(a - b) for a, b in zip(d["confs"][i]["DX"], d["confs"][i + m]["DX"])) for i in range(m))
    rec("A1", "Reverse every spin: H(-s)=H(s); verbatim h(-s)=-h(s); flip exponent unchanged", "V",
        "PASS" if (worst < 1e-13 and hs < 1e-13 and dxs < 1e-10) else "FAIL", challenges="time-reversal symmetry of the Hamiltonian",
        max_abs_dH_norm=worst, max_abs_h_antisymmetry=hs, max_abs_flip_exponent_change=dxs)
    # A2 flip one (random)
    rng = random.Random(7); mx = 0.0
    hh = lambda st: pe.local_fields(st, pairs, n)
    for _ in range(300):
        st = [rng.choice((-1, 1)) for _ in range(n)]; k = rng.randrange(n); h = hh(st)
        st2 = list(st); st2[k] = -st2[k]
        mx = max(mx, abs(pe.energy_norm(st2, pairs) - pe.energy_norm(st, pairs) - pe.flip_delta_norm(st, k, h)))
    rec("A2", "Flip one selected spin: direct subtraction equals -2 s_k h_k", "P", "PASS" if mx < 1e-12 else "FAIL",
        challenges="single-count energy and ΔE factor", max_abs_err=mx, trials=300)
    # A3 geometry conventions
    isl_up = pe.source_geometry(L, y_down=False)
    pairs_up = pe.K_pairs(isl_up)
    e_mirror = max(abs(a[2] - b[2]) for a, b in zip(pairs, pairs_up))
    # gauge: flip vertical unit vectors and relabel vertical states
    isl_g = [pe.Island(p.x, p.y, p.ux, -p.uy) if p.uy != 0 else pe.Island(p.x, p.y, p.ux, p.uy) for p in isl]
    pairs_g = pe.K_pairs(isl_g)
    vert = [i for i, p in enumerate(isl) if p.uy != 0]
    gauge_err = 0.0; naive_diff = 0
    for s in range(0, 1 << n, 13):
        st = pe.decode(s, n)
        stg = list(st)
        for i in vert:
            stg[i] = -stg[i]
        gauge_err = max(gauge_err, abs(pe.energy_norm(st, pairs) - pe.energy_norm(stg, pairs_g)))
        naive_diff = max(naive_diff, abs(pe.energy_norm(st, pairs) - pe.energy_norm(st, pairs_g)))
    En_g = [pe.energy_norm(pe.decode(s, n), pairs_g) for s in range(1 << n)]
    emin = min(En_g); gg = [s for s, e in enumerate(En_g) if abs(e - emin) < 1e-14]
    rec("A3a", "Physically equivalent convention: y-mirror of the whole patch (positions and unit vectors)", "P",
        "PASS" if e_mirror < 1e-14 else "FAIL", challenges="geometric orientation convention", max_abs_K_difference=e_mirror)
    rec("A3b", "Equivalent gauge: flip vertical unit vectors AND relabel vertical states", "P",
        "PASS" if gauge_err < 1e-13 else "FAIL", challenges="spin orientation convention", max_abs_dH=gauge_err)
    rec("A3c", "Convention-mismatch detector: flip vertical unit vectors WITHOUT relabelling states (a modelling error, not a symmetry)", "P",
        "INFO", mandatory=False, applies=False, challenges="spin-orientation bookkeeping",
        max_abs_dH_naive=naive_diff, ground_states_under_mismatch_all_ice=all(ice[s] for s in gg),
        note="Shows that orientation-bookkeeping errors alter energies; not used in the selected model.")
    # A4 normalisation change (python and verbatim probe kappa)
    sc = 3.7
    order_same = canon_order(En) == canon_order([sc * e for e in En])
    d1 = run_probe(L, T_REF, [s2str(s, n) for s in range(0, 1 << n, 41)], kappa=1.0)
    d2 = run_probe(L, T_REF, [s2str(s, n) for s in range(0, 1 << n, 41)], kappa=0.5)
    kr = max(abs(b - 0.5 * a) / max(abs(a), 1e-300) for c1, c2 in zip(d1["confs"], d2["confs"]) for a, b in zip(c1["DX"], c2["DX"]) if abs(a) > 1e-9)
    rec("A4", "Change normalisation (python K scale 3.7; verbatim interaction_adjustment_ratio 0.5) without moving coordinates: ordering invariant, flip exponent scales linearly",
        "V", "PASS" if (order_same and kr < 1e-9) else "FAIL", challenges="normalisation / energy scale",
        python_ordering_invariant=order_same, max_rel_dev_flip_exponent_scaling=kr)
    # A5 double counting
    n_test = 40
    dc = 0.0; ok_ratio = True
    for _ in range(n_test):
        st = [rng.choice((-1, 1)) for _ in range(n)]; k = rng.randrange(n); h = hh(st)
        full = lambda s_: sum(kk * s_[i] * s_[j] for i, j, kk in pairs) * 2.0
        st2 = list(st); st2[k] = -st2[k]
        corr = pe.energy_norm(st2, pairs) - pe.energy_norm(st, pairs)
        dcnt = full(st2) - full(st)
        ok_ratio = ok_ratio and abs(dcnt - 2 * corr) < 1e-12 and abs(corr - pe.flip_delta_norm(st, k, h)) < 1e-12
    rec("A5", "Double-counting detector: counting every ordered pair doubles ΔE relative to the source; single-counted H matches the source", "V",
        "PASS" if ok_ratio else "FAIL", challenges="double-counting convention", trials=n_test)
    # A6 sign detector against source
    d = run_probe(L, T_REF, [s2str(s, n) for s in range(0, 1 << n, 101)])
    f = [p["f"] for p in d["dipoles"]]
    agree = legacy_agree = 0; tot = 0
    for s, c in zip(range(0, 1 << n, 101), d["confs"]):
        st = pe.decode(s, n)
        for k in range(n):
            st2 = list(st); st2[k] = -st2[k]
            src = -c["DX"][k] / f[k]
            new = pe.energy_norm(st2, pairs) - pe.energy_norm(st, pairs)
            old = pe.energy_norm_legacy_v004(st2, pairs) - pe.energy_norm_legacy_v004(st, pairs)
            if abs(src) > 1e-9:
                tot += 1; agree += abs(src - new) < 1e-9; legacy_agree += abs(src - old) < 1e-9
    rec("A6", "ΔE sign detector against verbatim source: verified H agrees, legacy v001-v004 sign (E=-sum K s s) contradicts the source", "V",
        "PASS" if (agree == tot and legacy_agree == 0 and tot > 0) else "FAIL", challenges="incorrect ΔE sign",
        flips_compared=tot, verified_sign_agrees=agree, legacy_sign_agrees=legacy_agree)
    rec("F1", "FINDING: v001-v004 energy sign was inverted relative to the original source; the non-ice minima are its consequence (see E10)", "V",
        "FINDING", mandatory=False, challenges="sign of the interaction energy",
        cause="models/physical_energy.py energy(): E=-sum K s s with comment 'sign chosen to match local field' — but the source flip update gives dE=-2A s h, i.e. E=+sum K s s.",
        corroboration=["verbatim update_reference_dipole_reversal_time: exponent += +2*kappa*f*s*h (barrier up => state energy down by that amount)",
                       "MMC acceptance flip_probability = exp(+2*f*kappa*s*h) => dE/kT = -2 f kappa s h",
                       "Dryad README: Type 1 vertex is the ground-state vertex (checked in E10 for the verified sign)",
                       "independent Coulomb dumbbell energy (E3): like charges repel, head-to-tail aligned dipoles attract"])
    # A7 omitted long-range
    cuts = {}
    for cut in (200.0, 270.0, 400.0, -1.0):
        d = run_probe(L, T_REF, [], cutoff=cut)
        web = d["web"]
        pr = [(i, j, k) for (i, j), k in web.items() if i < j]
        E = [pe.energy_norm(pe.decode(s, n), pr) for s in range(1 << n)]
        emin = min(E); gr = [s for s, e in enumerate(E) if abs(e - emin) < 1e-14]
        cuts[str(cut)] = dict(pairs=len(pr), ground_degeneracy=len(gr), ground_all_ice=all(ice[s] for s in gr),
                              same_ground_ids_as_all_pair=(gr == summarise(En, ice, T_REF, n)["ground_ids"]))
    rec("A7", "Omitted long-range interactions (verbatim web builder with cutoff 200/270/400 nm vs all-pair): sensitivity of ground states", "V",
        "INFO", mandatory=False, applies=False, challenges="all-pair vs truncated interactions",
        results=cuts, note="Sensitivity measurement. Truncation changes the Hamiltonian; no invariant is expected.")
    # A8 units
    ok8 = True; u8 = {}
    for sc_ in (0.5, 2.0):
        d = run_probe(1, T_REF, [], scale=sc_)
        K_ok = max(abs(k - pe.K_pair(pe.source_geometry(1, a=260.0 * sc_)[i], pe.source_geometry(1, a=260.0 * sc_)[j], l=160 * sc_, w=60 * sc_, h=15 * sc_)) for (i, j), k in d["web"].items())
        base_f = run_probe(1, T_REF, [])["dipoles"][0]["f"]
        fr_ = d["dipoles"][0]["f"] / base_f
        Aj = pe.A_joule(T_REF, l=160 * sc_, w=60 * sc_, h=15 * sc_) / pe.A_joule(T_REF)
        u8[str(sc_)] = dict(K_max_err_vs_scaled_geometry=K_ok, source_f_ratio=fr_, python_A_ratio=Aj, expected=sc_ ** 3)
        ok8 = ok8 and K_ok < 1e-13 and abs(fr_ - sc_ ** 3) < 1e-9 * sc_ ** 3 and abs(Aj - sc_ ** 3) < 1e-9 * sc_ ** 3
    k_base = run_probe(1, T_REF, [])["web"]
    k_up = run_probe(1, T_REF, [], scale=2.0)["web"]
    scale_inv = max(abs(k_base[key] - k_up[key]) for key in k_base)
    rec("A8", "Unit consistency: uniform length scaling leaves K invariant and scales source f and python A(T) by scale^3 (volume)", "V",
        "PASS" if (ok8 and scale_inv < 1e-13) else "FAIL", challenges="nm vs m, volume units, conversion constants",
        K_invariance_max_abs=scale_inv, cases=u8,
        constants=dict(mu0=pe.MU0, kB=pe.KB, source_constant_K=0.910179, exact_constant_K=pe.MU0 * 1e10 * 1e-27 / pe.KB))
    # A9 boundary
    pbc_line = find_line(sp, r"if \(periodic_boundary_conditions_enabled\)")
    pbc_empty = False
    if pbc_line:
        pbc_empty = sp[pbc_line].strip() == "{" and sp[pbc_line + 1].strip() == "" and sp[pbc_line + 2].strip() == "}"
    ep1 = enumerate_patch(1)
    ep2 = (isl, pairs, n, En, ice)
    gr2 = summarise(En, ice, T_REF, n)["ground_ids"]
    sub = [0, 1, 2, 3]  # not geometrically the central vertex; compute properly below
    inc = pe.incident_islands(isl, pe.vertex_positions(2))
    central = inc[0]
    emb = []
    for g in gr2:
        emb.append(pe.ice_ok_geometric([pe.decode(g, n)[i] for i in central] + [0] * 0, [isl[i] for i in central], [pe.vertex_positions(2)[0]]))
    rec("A9", "Free boundary: source offers no alternative (periodic branch empty in v1.00); embedded-vertex check of the 2x2 ground states", "S",
        "INFO", mandatory=False, applies=False, challenges="free-boundary treatment; omitted exterior spins",
        periodic_branch_line=pbc_line, periodic_branch_is_empty=pbc_empty,
        ground_states_corner_vertex_ice=emb,
        note="No periodic treatment is implemented in the original v1.00 source, so no boundary alternative can be compared against it. The published geometry is free-boundary with dangling islands (README).")
    # A10 MMC vs SPMMC
    names = ["compute_scalar_product", "compute_charge_pair_normalized_displacement_ratio",
             "compute_dipole_pair_normalized_coupling_factor", "initialize_dipole_island_volumes",
             "initialize_reduced_temperature_prefactors_vector", "initialize_reduced_temperature_factors_array"]
    same = {}
    for nm in names:
        a, b = func_block(sp, nm), func_block(mm, nm)
        same[nm] = dict(spmmc_lines="%d-%d" % (a[0], a[1]), mmc_lines="%d-%d" % (b[0], b[1]), whitespace_normalised_identical=norm_ws(a[2]) == norm_ws(b[2]))
    sp_lat = find_line(sp, r"^double lattice_parameter"); mm_lat = find_line(mm, r"^double lattice_parameter")
    sp_vm = find_line(sp, r"^bool vertex_interaction_model_enabled"); mm_vm = find_line(mm, r"^bool vertex_interaction_model_enabled")
    mm_acc = find_line(mm, r"flip_probability = exp\(reduced_temperature_factors_array")
    sp_exp = find_line(sp, r"new_reversal_time_exponent = previous_reversal_time_exponent \+ 2\.0 \* interaction_adjustment_ratio")
    dm = run_probe(2, T_REF, [s2str(s, n) for s in range(1 << n)], vertex=1, lat=220.0)
    pr = [(i, j, k) for (i, j), k in dm["web"].items() if i < j]
    pr_all = len(pr)
    Ev = [pe.energy_norm(pe.decode(s, n), pr) for s in range(1 << n)]
    ev0 = min(Ev); gv = [s for s, e in enumerate(Ev) if abs(e - ev0) < 1e-14]
    all_same = all(v["whitespace_normalised_identical"] for v in same.values())
    rec("A10", "MMC vs SPMMC kept distinct: shared pair functions identical; defaults and interaction sets differ; MMC acceptance uses the same sign", "S",
        "PASS" if (all_same and sp_lat and mm_lat and mm_acc and sp_exp) else "FAIL", challenges="conflating MMC and SPMMC",
        shared_functions=same,
        spmmc_default=dict(lattice_parameter_line=sp[sp_lat - 1].strip(), vertex_interaction_model_line=sp[sp_vm - 1].strip()),
        mmc_default=dict(lattice_parameter_line=mm[mm_lat - 1].strip(), vertex_interaction_model_line=mm[mm_vm - 1].strip()),
        mmc_acceptance_line=(mm_acc, mm[mm_acc - 1].strip()[:200]), spmmc_exponent_update_line=(sp_exp, sp[sp_exp - 1].strip()[:200]),
        vertex_model_2x2_with_MMC_defaults=dict(unordered_pairs=pr_all, ground_degeneracy=len(gv), ground_all_ice=all(ice[s] for s in gv)),
        verdict_statement="MMC (vertex-neighbour six-pair model, a=220 nm default, Metropolis) and SPMMC (all-pair model, a=260 nm, kinetic) share the pair-coupling function but are different Hamiltonians; SPMMC all-pair is the selected model.")
    # regression vs transcribed v002-v004 formula if available
    try:
        sys.path.insert(0, str(SCR / "models"))
        import physical_energy as legacy  # noqa
        e_old = legacy.patch(2)[0]
        # legacy island ORDER and y orientation differ, so compare the multisets of pair couplings (orientation-gauge-free)
        old_k = sorted(legacy.pair_coupling(e_old[i], e_old[j], height=15.0)
                       for i in range(len(e_old)) for j in range(i + 1, len(e_old)))
        new_k = sorted(k for _, _, k in pairs)
        mx = max(abs(a - b) for a, b in zip(old_k, new_k)) if len(old_k) == len(new_k) else float("inf")
        rec("A11", "Regression: previously transcribed v002-v004 pair formula (models/physical_energy.py, y-up geometry) pair-coupling multiset equals v005 K at h=15 nm (index/orientation-independent)", "T",
            "PASS" if mx < 1e-13 else "FAIL", mandatory=False, challenges="geometry/formula transcription",
            max_abs_K_difference=mx, note="v004 default height was 16 nm vs source template 15 nm: a uniform K scale 16/15 (does not change any ordering).")
    except Exception as exc:  # noqa
        rec("A11", "Regression against previously transcribed formula", "T", "UNRESOLVED", mandatory=False,
            reason="legacy module not importable: %r" % (exc,))


# ----------------------------------------------------------------- source audit text
def source_audit_md(texts, got):
    sp = texts["SPMMC-SSI-Unix-v1.00.cpp"]; mm = texts["MMC-SSI-Unix-v1.00.cpp"]
    S, M = "SPMMC-SSI-Unix-v1.00.cpp", "MMC-SSI-Unix-v1.00.cpp"

    def fb(lines, name):
        b = func_block(lines, name)
        return "%d-%d" % (b[0], b[1])

    def ln(lines, pat):
        v = find_line(lines, pat)
        return str(v)
    R = []
    R.append("# SOURCE_AUDIT_v005 — Hamiltonian convention audit\n")
    R.append("Generated by `validate_v005.py` from the original files (line numbers are computed, not typed). Evidence labels: **[V]** verbatim function executed in probe; **[P]** independent Python; **[S]** static source text.\n")
    R.append("## Sources and hashes\n")
    for k, v in got.items():
        R.append("- `%s` sha256 `%s`" % (k, v))
    R.append("\nHierarchy used: (1) original SPMMC v1.00 C++; (2) original MMC v1.00 C++ for differentiation only; (3) Dryad README; (4) paper/supplement — **not available in this package**, so SM equation numbers are cited only via the README's own wording; (5) v001–v004 files for regression only.\n")
    R.append("Published geometry-specific v1.01 sources live in the (not acquired) data archives. README states v1.01 differs from v1.00 for SPMMC **only** in `island_width_mean` and `island_height` (set per geometry folder). Those per-folder values are **UNRESOLVED** here; the template defaults (w=60 nm, h=15 nm) are used and recorded, never presented as the published settings.\n")
    R.append("## Component table\n")
    R.append("| Component | Convention established | SPMMC v1.00 (file:lines) | MMC v1.00 | Tested by |")
    R.append("|---|---|---|---|---|")
    R.append("| Magnetic moment | m_i = M(T)·V_i, V_i=(π/6)·l·w·h (ellipsoid), M0=7.9×10^5 A/m (source units 10^5 A/m), direction s_i·u_i, s=+1 along u (README `Dipole_Unit_Vector`) | `%s:%s` volumes; `:%s` M0 | same function, lines `%s` | E3, A8 |" % (S, fb(sp, "initialize_dipole_island_volumes"), ln(sp, r"^double spontaneous_magnetization0"), fb(mm, "initialize_dipole_island_volumes")))
    R.append("| Dumbbell | charges ±q·s at r ± (l/3)u (the (l/3d)² terms of the displacement ratio); q=(π/4)·M·w·h (derived from the 3/16 prefactor; verified by independent Coulomb evaluation); dumbbell moment q·2l/3 = M·V | `%s:%s`, `%s` | `%s:%s` (identical after whitespace) | E3 |" % (S, fb(sp, "compute_charge_pair_normalized_displacement_ratio"), fb(sp, "compute_dipole_pair_normalized_coupling_factor"), M, fb(mm, "compute_dipole_pair_normalized_coupling_factor")))
    R.append("| Geometry | horizontal islands unit (1,0) at (col+½, −row)·a; vertical unit **(0,−1)** at (col, −row−½)·a; plus dangling left horizontals and top verticals so every vertex has 4 islands; N=2L(L+1); a=260 nm, l=160, w=60, h=15 nm (template) | `%s:%s`, vertices `%s` | defaults: lattice parameter %s | E1, A3 |" % (S, fb(sp, "initialize_dipole_system"), fb(sp, "initialize_vertex_system"), mm[find_line(mm, r"^double lattice_parameter") - 1].split("//")[0].strip()))
    R.append("| Interactions | SPMMC default: all pairs i≠j within cutoff 10^7 nm (no self term); `vertex_interaction_model_enabled=false`. MMC default: six-neighbour shared-vertex model (`true`) | `%s:%s`; flags line %s | flags line %s | E2, A7, A10 |" % (S, fb(sp, "initialize_dipole_interaction_web_arrays"), ln(sp, r"^bool vertex_interaction_model_enabled"), ln(mm, r"^bool vertex_interaction_model_enabled")))
    R.append("| Energy | **No total-energy routine exists in either source.** Reconstructed as H = Σ_{i<j} U_ij s_i s_j = A(T) Σ_{i<j} K_ij s_i s_j, single-counted, no additive offset; proven consistent with the source's own ΔE (E5, E8) and independent Coulomb physics (E3) | pair factor `%s:%s` | same | E3, E5, E8, A5 |" % (S, fb(sp, "compute_dipole_pair_normalized_coupling_factor")))
    R.append("| Magnetic field | h_i = Σ_j K_ij s_j (source `initialize_dipole_athermal_interaction_fields`); README: H_i normalised dumbbell field | `%s:%s` | `%s:%s` | E4 |" % (S, fb(sp, "initialize_dipole_athermal_interaction_fields"), M, fb(mm, "initialize_dipole_athermal_interaction_fields")))
    R.append("| Spin flips | SPMMC: reversal exponent x_i=f(T)(κ_b ΔN − κ h_i s_i) (README Eq.3); flip of i changes it by +2κ f s_i h_i ⇒ **ΔE_i = −2 A s_i h_i** (state energy falls when s_i h_i>0); acceptance convention: fixed-time-step rate Δτ/τ_i. MMC: Metropolis probability exp(+2 f κ s h) ⇒ same ΔE sign | `%s:%s` (exponent), `%s:%s` (update), line %s | line %s (`flip_probability`) | E5, A6, F1 |" % (S, fb(sp, "reinitialize_reversal_times"), S, fb(sp, "update_reference_dipole_reversal_time"), ln(sp, r"new_reversal_time_exponent = previous_reversal_time_exponent \+ 2\.0 \* interaction_adjustment_ratio"), ln(mm, r"flip_probability = exp\(reduced_temperature_factors_array")))
    R.append("| Boundary | free boundary, 24×24 vertices published; finite patches embed L×L vertices with dangling boundary islands; `periodic_boundary_conditions_enabled=false` and the periodic branch of the web builder is empty in v1.00 | `%s` flag line %s; branch line %s | similar | A9 |" % (S, ln(sp, r"^bool periodic_boundary_conditions_enabled"), ln(sp, r"if \(periodic_boundary_conditions_enabled\)")))
    R.append("| Temperature | M(T)=M0(1−T/Tc)^β (β=0.5); f(T)=0.910179·M0²·V/(2Tc)·(1−t)^{2β}/t ⇒ f·kB·T = κ μ0 M(T)² V/2 = A(T); all pair energies share the same T-dependence, so E(s,T)=A(T)E_ref(s), B=0; Tc=820 K (height-dependent Tc disabled in effect: characteristic height 0) | `%s:%s`, `%s:%s`; Tc line %s | identical functions | E9, E9b |" % (S, fb(sp, "initialize_reduced_temperature_prefactors_vector"), S, fb(sp, "initialize_reduced_temperature_factors_array"), ln(sp, r"^double Curie_temperature =")))
    R.append("| Units | length: nm in source; M0: 10^5 A/m in source; volume: nm³ (=10^-27 m³); constant 0.910179 K = μ0·(10^5)²·10^-27/kB **rounded** (exact 0.9101785…, relative offset +5.2×10⁻⁷); ΔE in joules = −kB·T·Δ(exponent) | `%s` line %s | same | A8, E5 |" % (S, ln(sp, r"0\.910179 \* spontaneous_magnetization0")))
    R.append("\n## Unresolved / out of scope (declared, not silently substituted)\n")
    R.append("- Published v1.01 per-folder island width and height: UNRESOLVED (data archives not acquired).")
    R.append("- Unmodified full-simulator execution: **not run** (needs GSL, produces no total energy; flip/field relations are exercised through verbatim functions instead).")
    R.append("- Paper/supplement equations: not in package; README text used for Eq. 3 and t0.")
    R.append("- Size-disorder (stdev>0) runs: probe stand-in supports stdev=0 only (all template defaults).")
    return "\n".join(R) + "\n"


# ----------------------------------------------------------------- reporting
def md_report(rep):
    L = []
    L.append("# REPORT_v005 — Physical Energy and Hamiltonian Convention Lock\n")
    L.append("**Verdict:** `%s`\n" % rep["verdict"])
    L.append("This verdict concerns the selected finite-patch SPMMC v1.00 all-pair model with template parameters. It is **not** a transfer result and does not generalise to artificial square spin ice in general or to the published 24×24 arrays.\n")
    L.append("## Headline\n")
    for k in ("headline_1x1", "headline_2x2"):
        L.append("- " + rep[k])
    L.append("- " + rep["headline_sign"])
    L.append("\n## Test summary\n")
    L.append("| ID | Test | Evidence level | Status | Mandatory |")
    L.append("|---|---|---|---|---|")
    for t in rep["tests"]:
        L.append("| %s | %s | %s | **%s** | %s |" % (t["id"], t["title"], t["evidence_level"], t["status"], "yes" if t["mandatory"] else "no"))
    L.append("\n## Unresolved items\n")
    for u in rep["unresolved"]:
        L.append("- " + u)
    L.append("\n## Evidence levels\n")
    for k, v in LEVEL.items():
        L.append("- %s" % v)
    L.append("\n## Scope\n")
    L.append(rep["scope"])
    return "\n".join(L) + "\n"


def main():
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    OUT.mkdir(parents=True, exist_ok=True)
    rep = dict(version="v005", started_utc=started, platform=platform.platform(), python=sys.version.split()[0])
    try:
        with tempfile.TemporaryDirectory() as td:
            got, texts = load_sources(pathlib.Path(td))
            rep["source_hashes"] = got
            check_provenance(got, texts)
            rep["compiler"] = build_probe()
            test_geometry_and_coupling()
            test_charge_model()
            test_fields_and_flips()
            res, csv_ground, csv_temp, _ = test_enumeration_and_temperature(texts)
            reconstruct_landscape_and_scaling()
            test_adversarial(texts)
            (OUT / "SOURCE_AUDIT_v005.md").write_text(source_audit_md(texts, got))
    except Blocked as exc:
        rep["verdict"] = "PREFLIGHT_EXECUTION_BLOCKED"; rep["blocked_reason"] = str(exc); rep["tests"] = TESTS
        rep["unresolved"] = [str(exc)]
        (OUT / "REPORT_v005.json").write_text(json.dumps(rep, indent=2, default=str) + "\n")
        (OUT / "REPORT_v005.md").write_text("# REPORT_v005\n\nVerdict: `PREFLIGHT_EXECUTION_BLOCKED`\n\nReason: %s\n" % exc)
        print("PREFLIGHT_EXECUTION_BLOCKED:", exc)
        return 2

    mand_fail = [t["id"] for t in TESTS if t["mandatory"] and t["status"] == "FAIL"]
    mand_unres = [t["id"] for t in TESTS if t["mandatory"] and t["status"] == "UNRESOLVED"]
    verdict = ("PHYSICAL_HAMILTONIAN_LOCK_FAIL" if mand_fail else
               "PHYSICAL_HAMILTONIAN_LOCK_PARTIAL" if mand_unres else "PHYSICAL_HAMILTONIAN_LOCK_PASS")
    p1, p2 = res["patches"]["1x1"], res["patches"]["2x2"]

    def head(p, name):
        return ("%s: %d configs, %d 2-in/2-out, ground energy %.6e J at %g K (A(T)=%.6e J), degeneracy %d, all ground states ice-rule=%s, "
                "min ice %.6e J, min non-ice %.6e J, non-ice-minus-ice gap %.3e J; ground vertices all Type 1 = %s"
                % (name, p["configurations"], p["ice_states_python_geometric"], p["ground_E_J"], T_REF, p["A_J"], p["degeneracy"],
                   p["ground_all_ice"], p["min_ice_E_J"], p["min_nonice_E_J"], p["gap_nonice_minus_ice_J"], p["ground_states_all_type1_vertices"]))
    rep.update(
        verdict=verdict, mandatory_failures=mand_fail, mandatory_unresolved=mand_unres,
        headline_1x1=head(p1, "1×1 (4 spins)"), headline_2x2=head(p2, "2×2 (12 spins)"),
        headline_sign=("v001–v004 non-ice ground states reproduced ONLY with the legacy sign E=−ΣKss (regression, exact negative of the verified "
                       "energy). The source's own flip update gives ΔE=−2A s h, i.e. E=+ΣKss; under it the 1×1 and 2×2 ground states are ice-rule "
                       "(Type 1) states. Cause: energy sign convention, not geometry, units, boundary or temperature."),
        unresolved=["v1.01 production island width/height per geometry folder (data archives not acquired).",
                    "Unmodified simulator execution not performed (GSL not required by the probe; the simulator exposes no total energy).",
                    "Paper/supplement not in package; README used for Eq. 3.",
                    "Boundary alternatives cannot be compared: periodic branch is empty in v1.00.",
                    "Gaussian size disorder (stdev>0) untested; probe stand-in supports stdev=0."],
        scope=("Selected model: SPMMC-SSI-Unix-v1.00 all-pair dumbbell interaction, free-boundary finite patches 1×1 (4 spins) and 2×2 (12 spins), "
               "template parameters a=260, l=160, w=60, h=15 nm, M0=7.9e5 A/m, β=0.5, Tc=820 K, κ=1, supported domain 0<T<Tc (tested 760–815 K). "
               "3×3 (24 spins, 16,777,216 configurations) used for targeted field/energy/flip tests only (48 random configurations); no exhaustive run."),
        tolerance_policy=policy(max(abs(k) for _, _, k in pe.K_pairs(pe.source_geometry(2)))),
        finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), tests=TESTS, patches=res["patches"])
    (OUT / "REPORT_v005.json").write_text(json.dumps(rep, indent=2, default=str) + "\n")
    (OUT / "REPORT_v005.md").write_text(md_report(rep))
    (OUT / "TESTS_v005.json").write_text(json.dumps(TESTS, indent=2, default=str) + "\n")
    (OUT / "PARAMETERS_v005.json").write_text(json.dumps(dict(
        model="SPMMC-SSI-Unix-v1.00 (all-pair dumbbell), template parameters", template=pe.TEMPLATE,
        units=dict(lengths="nm", M0="A/m", T="K", energy="J"), constants=dict(mu0_H_per_m=pe.MU0, kB_J_per_K=pe.KB,
                                                                           source_constant_K=0.910179, exact_constant_K=pe.MU0 * 1e10 * 1e-27 / pe.KB),
        temperatures_K=TEMPS, reference_temperature_K=T_REF, v101_production_parameters="UNRESOLVED",
        tolerance_policy=rep["tolerance_policy"]), indent=2, default=str) + "\n")
    with open(OUT / "GROUND_STATES_v005.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["L", "model", "T_K", "state_id", "state_string(+/-,spin0 first)", "E_J", "E_norm", "ice_rule", "vertex_type_fractions_I..IV"]); w.writerows(csv_ground)
    with open(OUT / "TEMPERATURE_v005.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["L", "T_K", "M_A_per_m", "A_J", "A_over_Aref", "analytic_(1-T/Tc)/(1-Tref/Tc)", "spearman_vs_ref", "identical_rank_order", "ground_degeneracy", "ground_ids", "ground_E_J", "min_ice_E_J", "min_nonice_E_J", "gap_nonice_minus_ice_J"]); w.writerows(csv_temp)
    files = ["REPORT_v005.json", "REPORT_v005.md", "SOURCE_AUDIT_v005.md", "PARAMETERS_v005.json", "GROUND_STATES_v005.csv", "TEMPERATURE_v005.csv", "TESTS_v005.json"]
    code = [HERE / "validate_v005.py", HERE / "physical_energy_v005.py", PROBE_SRC, HERE / "test_v005.py", HERE / "README_v005.md"]
    (OUT / "MANIFEST_v005.json").write_text(json.dumps(dict(
        outputs={k: sha_file(OUT / k) for k in files}, code={c.name: sha_file(c) for c in code if c.exists()},
        inputs=rep["source_hashes"], verdict=verdict), indent=2) + "\n")
    print(json.dumps(dict(verdict=verdict, mandatory_failures=mand_fail, tests={t["id"]: t["status"] for t in TESTS}), indent=1))
    print(rep["headline_1x1"]); print(rep["headline_2x2"])
    return 1 if mand_fail else 0


if __name__ == "__main__":
    sys.exit(main())
