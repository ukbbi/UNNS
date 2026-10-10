#!/usr/bin/env python3
"""SCR-III-B PREFLIGHT_v009 -- preregistration closure gate (outcome-blind).

Run from the project root (Ubuntu/WSL; g++ and Python 3 with numpy):   python3 scr_iii_b/prereg_gate/validate_v009.py
Reads (never writes) frozen v005-v008 code/outputs.  Writes only scr_iii_b/output/validation/v009/ (and drafts are shipped separately, unfrozen).

OUTCOME-BLIND RESTRICTIONS: the real 3x3 patch is only ever run at W=0 (the published anchor) and in grammar-only modes (no Hamiltonian).
Delta_nonG / rho_G are NOT computed for the real 3x3 grammar.  Real-3x3 W>0 and excitation-gap requests are only ever issued to prove that the
guard BLOCKS them.  Synthetic instances (random couplings) and the public 1x1 / 2x2 patches may be used at any window.
Nothing here freezes or authorises anything: every constant in PROPOSED is a recommendation awaiting ratification.
"""
import sys
sys.dont_write_bytecode = True
import csv, datetime, gzip, hashlib, json, math, os, pathlib, platform, random, re, shutil, statistics, subprocess, tempfile, time
from fractions import Fraction

HERE = pathlib.Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
SB = PROJECT / "scr_iii_b"
FEAS, EX3, V8SOL = SB / "feasibility", SB / "exact3", SB / "solvers"
V5C = SB / "reference_check"
OUTV = SB / "output" / "validation"
V5, V6, V7, V8, OUT = OUTV / "v005", OUTV / "v006", OUTV / "v007", OUTV / "v008", OUTV / "v009"
DRAFTS = SB / "drafts"
sys.path.insert(0, str(FEAS)); sys.path.insert(0, str(HERE))
import numpy as np
import energy_windows_v006 as ew
import tolerance_v009 as tol
import seeds_v009 as sd
import cost_audit_v009 as ca

PROPOSED = dict(master_seed=20261010, rel_tau=1e-9, rel_gray=1e-10, e2_frac=0.25, T_ref=792.0, kB=1.380649e-23,
                window_multipliers=dict(primary=1.0, sensitivity_A=0.5, sensitivity_B=2.0), n_nulls_per_family=1000,
                warmups=3, repeats=15, mem_limit_gib=2.0, time_limit_min=30.0, hg_contraction=0.99, hc_speedup=1.20, z2_in_primary=False,
                null_cap=50_000_000, tie_rule="E <= E0 + W + tau; PRESERVED iff W + tau < Delta_nonG")
TESTS, DIAG = [], {}
SOLVERS = ("b0", "g1", "g2", "b1", "e2")


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
    if isinstance(o, (list, tuple, set)):
        return [clean(v) for v in o]
    if isinstance(o, np.generic):
        return o.item()
    return o


def fnv64(b):
    h = 1469598103934665603
    for c in b:
        h ^= c; h = (h * 1099511628211) & 0xFFFFFFFFFFFFFFFF
    return h


def frozen(manifest, groups):
    if not manifest.exists():
        raise Blocked("%s missing" % manifest)
    m = json.loads(manifest.read_text()); bad = []; n = 0
    for grp, base in groups:
        for name, h in m.get(grp, {}).items():
            n += 1; p = base / name
            if not p.exists() or sha(p) != h:
                bad.append(name)
    return m, bad, n


# ---------------------------------------------------------------- instances and python oracles
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


def synth_instance(rng, n, nvmax=4, scale=0.01):
    pairs = [(i, j, rng.gauss(0, scale)) for i in range(n) for j in range(i + 1, n)]
    for _ in range(300):
        masks = []
        for _v in range(rng.randint(1, nvmax)):
            isl = rng.sample(range(n), 4)
            masks.append((sum(1 << i for i in isl), sum(1 << i for i in isl if rng.random() < 0.5)))
        g = grammar_flags(n, masks)
        if 2 <= sum(g) <= int(0.9 * (1 << n)):
            return pairs, masks, g
    raise Blocked("could not generate synthetic grammar")


class Env:
    """Holds compiled binaries, the audit log and the run helpers."""

    def __init__(self, tmp, pg, e2, audit, protected):
        self.tmp, self.pg, self.e2, self.audit, self.protected = tmp, pg, e2, audit, protected
        self.runs = 0

    def run(self, inp, mode, W, tau, e0=None, extra=(), tag="", synthetic=False, dump=None):
        binp = self.e2 if mode == "e2" else self.pg
        cmd = [str(binp), str(inp), mode, repr(float(W)), repr(float(tau))]
        if e0 is not None:
            cmd += ["--e0", repr(float(e0))]
        cmd += ["--audit", str(self.audit), "--tag", tag]
        if synthetic:
            cmd += ["--synthetic", "--protected", str(self.protected)]
        if dump:
            cmd += ["--dump", str(dump)]
        cmd += [str(x) for x in extra]
        self.runs += 1
        return subprocess.run(cmd, capture_output=True, text=True)

    def solve(self, inp, mode, W, tau, e0, extra=(), tag="", synthetic=False):
        d = self.tmp / "dump.txt"
        if d.exists():
            d.unlink()
        p = self.run(inp, mode, W, tau, e0, extra, tag, synthetic, dump=d)
        if p.returncode:
            raise Blocked("%s failed rc=%d: %s" % (mode, p.returncode, p.stderr[-300:]))
        kv = ca.parse_kv(p.stdout)
        ids = {int(x) for x in d.read_text().split()} if d.exists() else set()
        return ids, kv


def public_windows(En, tau):
    E0 = min(En); lv, levels, gap, sc = ew.group_levels(En)
    Ws = [("zero", 0.0)]
    for k in range(1, len(levels)):
        Wk = levels[k]["E_min"] - E0
        Ws.append(("level%d" % k, Wk)); Ws.append(("below%d" % k, Wk - 10 * tau))
        if k + 1 < len(levels):
            Ws.append(("mid%d" % k, 0.5 * (Wk + levels[k + 1]["E_min"] - E0)))
    return Ws, levels


# ================================================================ setup
def setup():
    X = {}
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="v009_")); X["tmp"] = tmp
    cc = os.environ.get("CXX", "g++")
    try:
        for src, name in (("prereg_gate_v009.cpp", "pg"), ("e2_v009.cpp", "e2")):
            pr = subprocess.run([cc, "-std=c++17", "-O2", "-Wall", "-Wextra", str(HERE / src), "-o", str(tmp / name)], capture_output=True, text=True)
            if pr.returncode:
                raise Blocked("compile of %s failed:\n%s" % (src, pr.stderr[-2000:]))
            X["warnings_" + name] = len(pr.stderr.strip().splitlines())
        X["compiler"] = subprocess.run([cc, "--version"], capture_output=True, text=True).stdout.splitlines()[0]
    except FileNotFoundError:
        raise Blocked("C++ compiler '%s' not found" % cc)
    X["pe"] = ew.load_v005()
    pe = X["pe"]
    inst, incs = {}, {}
    for L in (1, 2, 3):
        isl = pe.source_geometry(L); pairs = pe.K_pairs(isl); vpos = pe.vertex_positions(L)
        inc, _ = ew.build_incidence(pe, isl, vpos); masks = ew.compile_masks(inc)
        p = tmp / ("real%d.txt" % L); write_instance(p, len(isl), pairs, masks)
        inst[L] = dict(path=p, n=len(isl), pairs=pairs, masks=masks, inc=inc, Q=sum(abs(k) for _, _, k in pairs), fp="%016x" % fnv64(p.read_bytes()))
        inst[L]["tau"] = tol.REL_TAU * inst[L]["Q"]
    X["inst"] = inst
    prot = tmp / "protected_fingerprints.txt"; prot.write_text(inst[3]["fp"] + "\n")
    audit = tmp / "audit.jsonl"; audit.write_text("")
    X["env"] = Env(tmp, tmp / "pg", tmp / "e2", audit, prot)
    X["A_J"] = pe.A_joule(PROPOSED["T_ref"]); X["kT_J"] = PROPOSED["kB"] * PROPOSED["T_ref"]; X["kT_norm"] = X["kT_J"] / X["A_J"]
    X["anchor"] = json.loads((V7 / "REPORT_v007.json").read_text())["anchor_3x3"]
    X["E0f"] = X["anchor"]["E0_norm"]
    return X


# ================================================================ P0, F1
def test_P0_F1(X):
    m5, b5, n5 = frozen(V5 / "MANIFEST_v005.json", (("code", V5C), ("outputs", V5)))
    m6, b6, n6 = frozen(V6 / "MANIFEST_v006.json", (("code", FEAS), ("outputs", V6)))
    m7, b7, n7 = frozen(V7 / "MANIFEST_v007.json", (("code", EX3), ("outputs", V7)))
    m8, b8, n8 = frozen(V8 / "MANIFEST_v008.json", (("code", V8SOL), ("outputs", V8)))
    X["manifests"] = dict(v005=m5, v006=m6, v007=m7, v008=m8)
    rec("F1", "Frozen v005-v008 code/outputs equal the hashes in their local manifests (read-only)", "STATIC_FILE_HASH",
        "PASS" if not (b5 or b6 or b7 or b8) else "FAIL", mismatches=dict(v005=b5, v006=b6, v007=b7, v008=b8), files_checked=n5 + n6 + n7 + n8,
        verdicts={k: v.get("verdict") for k, v in X["manifests"].items()})
    inputs = m5.get("inputs", {})
    found = {nm: [str(p.relative_to(PROJECT)) for p in PROJECT.rglob(nm)] for nm in inputs}
    ok = len(inputs) >= 5 and all(len(h) == 64 for h in inputs.values())
    rec("P0", "Prerequisites and original-source provenance: compiler, numpy, frozen manifests present; Dryad source hashes recorded by v005", "PROVENANCE",
        "PASS" if ok and X["compiler"] else "FAIL", compiler=X["compiler"], python=sys.version.split()[0], numpy=np.__version__, compile_warnings=dict(pg=X["warnings_pg"], e2=X["warnings_e2"]),
        original_source_hashes_recorded_in_v005=inputs, original_files_present_in_this_tree=found,
        note="The Dryad archives themselves are not part of the additive tree: their SHA-256 are recorded in the frozen v005 manifest and are NOT re-verified here (provenance by record, not by re-hash).")


# ================================================================ R1, R2 : common E0
def reconcile_reference(frozen_E0, reported):
    """Harness-level reconciliation: every solver must report exactly the frozen reference (bitwise)."""
    bad = {k: v for k, v in reported.items() if float.fromhex(v) != frozen_E0}
    if bad:
        raise ValueError("inconsistent ground-energy reference(s): %s" % bad)
    return True


def test_R(X):
    env, I, tmp = X["env"], X["inst"], X["tmp"]; E0f = X["E0f"]; pe = X["pe"]
    m7 = X["manifests"]["v007"]
    rec_hash_ok = sha(V7 / "REPORT_v007.json") == m7["outputs"]["REPORT_v007.json"]
    canon = json.dumps(X["anchor"], sort_keys=True)
    # independent certification of the minimum (W=0 operations only)
    cert = {}
    for mode in ("cert_b0", "cert_b1"):
        p = env.run(I[3]["path"], mode, 0, I[3]["tau"], tag="E0_certification")
        kv = ca.parse_kv(p.stdout); cert[mode] = dict(E0=float(kv["E0_certified"]), ground_count=int(kv["ground_count_within_tau"]), ids=kv.get("ids"), rc=p.returncode)
    A_J = X["A_J"]; E0J = E0f * A_J
    units_ok = abs(E0J - X["anchor"]["E0_J"]) <= 1e-12 * abs(E0J) and abs(E0J - (-9.271994751803727e-20)) <= 1e-12 * abs(E0J)
    cert_ok = all(c["rc"] == 0 and abs(c["E0"] - E0f) <= I[3]["tau"] and c["ground_count"] == X["anchor"]["ground_states"] for c in cert.values())
    DIAG["E0_AUDIT"] = dict(frozen_source="output/validation/v007/REPORT_v007.json::anchor_3x3.E0_norm", E0_norm_repr=repr(E0f), E0_norm_hex=E0f.hex(), E0_J=X["anchor"]["E0_J"],
                            spec_literal_J=-9.271994751803727e-20, A_J_at_Tref=A_J, E0_norm_times_A_J=E0J, units_scaling_ok=units_ok,
                            report_v007_sha256=sha(V7 / "REPORT_v007.json"), manifest_v007_recorded_sha256=m7["outputs"]["REPORT_v007.json"], hash_matches_frozen_record=rec_hash_ok,
                            anchor_record_sha256=hashlib.sha256(canon.encode()).hexdigest(), independent_certification=cert,
                            certification_equal_to_frozen_bitwise={k: v["E0"] == E0f for k, v in cert.items()}, certification_within_tau=cert_ok)
    # the same reference to every solver, every patch
    echoes = {}; wrong = []; nrun = 0
    refs = {1: min(energies(I[1]["n"], I[1]["pairs"])), 2: min(energies(I[2]["n"], I[2]["pairs"])), 3: E0f}
    for L in (1, 2, 3):
        for mode in SOLVERS:
            ids, kv = env.solve(I[L]["path"], mode, 0.0, I[L]["tau"], refs[L], tag="R1_common_E0_%dx%d" % (L, L)); nrun += 1
            echoes[(L, mode)] = kv["E0_used_hex"]
            if float.fromhex(kv["E0_used_hex"]) != refs[L] or abs(float(kv["Ecut"]) - (refs[L] + I[L]["tau"])) > 4e-16 * I[L]["Q"] or kv["E0_source"] != "reference":
                wrong.append((L, mode))
            if mode in ("b0", "b1", "e2") and not (abs(float(kv["own_min"]) - refs[L]) <= I[L]["tau"] or mode == "e2"):
                wrong.append((L, mode, "own_min"))
    try:
        reconcile_reference(E0f, {m: echoes[(3, m)] for m in SOLVERS}); recon = True
    except ValueError:
        recon = False
    # accounting of the one-time cost is produced in the cost section (cert_b0 / cert_b1 rows)
    rec("R1", "Common physical E0: the frozen v007 anchor (hash-matched, unit-checked, independently re-certified by Gray-code and branch-and-bound minimisation) is passed to B0, G1, G2, B1 and E2; every solver echoes it bitwise and thresholds Ecut = E0+W+tau from it",
        "BEHAVIOURAL_AND_HASH", "PASS" if (rec_hash_ok and units_ok and cert_ok and not wrong and recon) else "FAIL",
        solver_runs=nrun, wrong=wrong, hash_matches_frozen_record=rec_hash_ok, units_scaling_ok=units_ok, certification_ok=cert_ok, harness_reconciliation=recon,
        certified_values=cert, frozen_E0_norm=repr(E0f))
    # ------------------------------------------------ R2
    d2, t2 = I[2], I[2]["tau"]; E02 = refs[2]; out = {}
    for name, ref in (("high_100tau", E02 + 100 * t2), ("low_100tau", E02 - 100 * t2), ("high_0.5tau", E02 + 0.5 * t2)):
        for mode in SOLVERS:
            p = env.run(d2["path"], mode, 0.0, t2, ref, tag="R2_" + name)
            out[(name, mode)] = p.returncode
    p_missing = env.run(d2["path"], "b0", 0.0, t2, None, tag="R2_missing_e0")
    must_reject = [("high_100tau", m) for m in ("b0", "b1", "g1", "g2")] + [("low_100tau", m) for m in ("b0", "b1", "e2")]
    rej_ok = all(out[k] == 4 for k in must_reject) and all(out[("high_0.5tau", m)] == 0 for m in SOLVERS)
    # tampered harness record and a different-estimate scenario
    try:
        reconcile_reference(E0f, {"g2": (E0f + 1e-6).hex()}); harness_ok = False
    except ValueError:
        harness_ok = True
    # grammar-restricted estimate must never replace E0: synthetic instance whose grammar EXCLUDES the true ground state
    rng = random.Random(PROPOSED["master_seed"] + 9); excl = None
    for t in range(400):
        n = rng.randint(8, 11); pairs, masks, g = synth_instance(rng, n)
        En = energies(n, pairs); E0 = min(En); idsG = [i for i in range(1 << n) if g[i]]
        E0G = min(En[i] for i in idsG)
        if E0G - E0 > 1e-6:
            excl = (n, pairs, masks, g, En, E0, E0G, idsG); break
    if excl is None:
        raise Blocked("no grammar-excludes-ground synthetic instance found")
    n, pairs, masks, g, En, E0, E0G, idsG = excl; ps = tmp / "excl.txt"; write_instance(ps, n, pairs, masks); Qs = sum(abs(k) for _, _, k in pairs); ts = tol.REL_TAU * Qs
    W = 0.5 * (E0G - E0); correct = {i for i in idsG if En[i] <= E0 + W + ts}; wrongset = {i for i in idsG if En[i] <= E0G + W + ts}
    sets = {}; flags = {}
    for mode in ("g1", "g2"):
        ids, kv = env.solve(ps, mode, W, ts, E0, tag="R2_grammar_excludes_ground"); sets[mode] = ids; flags[mode] = kv["ref_status"]
    no_replace = all(sets[m] == correct for m in sets) and correct != wrongset and all(f.startswith("GROUND_EXCLUDED") for f in flags.values())
    src = (HERE / "prereg_gate_v009.cpp").read_text() + (HERE / "gate_common_v009.hpp").read_text()
    static_ok = src.count("Eref = O.have_e0 ? O.e0 : 0.0; set_threshold();") == 1 and "Eref = own" not in src and "Eref = E0hat" not in src
    rec("R2", "Inconsistent ground-energy references are rejected (exit 4) or flagged; missing reference refused; harness reconciliation rejects a different estimate; a grammar-restricted minimum never replaces E0",
        "BEHAVIOURAL", "PASS" if (rej_ok and p_missing.returncode == 2 and harness_ok and no_replace and static_ok) else "FAIL",
        exit_codes={"%s/%s" % k: v for k, v in out.items()}, missing_reference_rc=p_missing.returncode, harness_rejects_tampered=harness_ok,
        grammar_excludes_ground_case=dict(n=n, E0_minus_E0G=E0 - E0G, W=W, correct_target_size=len(correct), restricted_estimate_target_size=len(wrongset), solver_sizes={m: len(s) for m, s in sets.items()}, flags=flags),
        static_check_threshold_only_from_reference=static_ok,
        documented_limits="Grammar-restricted solvers (G1/G2) and E2 cannot certify E0 from their own search; G1/G2 detect a reference ABOVE a grammar state, E2 detects an empty target or a state certified below the reference; a reference that is too LOW by a few tau is only caught by the harness hash/bitwise reconciliation (R1) against the frozen v007 record.")
    X["refs"] = refs


# ================================================================ E1..E4 : E2 comparator
def e2_model(pairs, frac):
    npairs = len(pairs)
    ordr = sorted(range(npairs), key=lambda p: (-abs(pairs[p][2]), p))
    r = max(0, min(npairs, math.ceil(frac * npairs - 1e-12)))
    ret = set(ordr[:r]); h = 1469598103934665603
    for p in ordr[:r]:
        h ^= p; h = (h * 1099511628211) & 0xFFFFFFFFFFFFFFFF
    BO = sum((Fraction(abs(pairs[p][2])) for p in range(npairs) if p not in ret), Fraction(0))
    return ordr, r, ret, BO, h


def test_E(X):
    env, I, tmp = X["env"], X["inst"], X["tmp"]; rng = random.Random(PROPOSED["master_seed"] + 21)
    FR = (0.0, 0.1, 0.25, 0.5, 0.9, 1.0)
    # ---- E1: remainder bound, implementation vs independent model, and the inequality itself in exact arithmetic
    e1_bad = []; ineq_checked = 0; cases = [("real1x1", 4, I[1]["pairs"], I[1]["masks"], I[1]["path"], I[1]["tau"]), ("real2x2", 12, I[2]["pairs"], I[2]["masks"], I[2]["path"], I[2]["tau"])]
    for t in range(4):
        n = rng.randint(7, 10); pairs, masks, _g = synth_instance(rng, n); pth = tmp / ("e1syn%d.txt" % t); write_instance(pth, n, pairs, masks)
        cases.append(("synthetic%d" % t, n, pairs, masks, pth, tol.REL_TAU * sum(abs(k) for _, _, k in pairs)))
    n_ = 6; pairs_mixed = [(i, j, (1 if (i + j) % 2 else -1) * 0.25 * ((i * j) % 3)) for i in range(n_) for j in range(i + 1, n_)]     # mixed sign with zero couplings
    pth = tmp / "e1mixed.txt"; write_instance(pth, n_, pairs_mixed, [(0b001111, 0)]); cases.append(("mixed_zero", n_, pairs_mixed, [(0b001111, 0)], pth, 1e-9 * sum(abs(k) for _, _, k in pairs_mixed)))
    pth = tmp / "e1degen.txt"; pairs_deg = [(i, j, 0.0) for i in range(n_) for j in range(i + 1, n_)]; write_instance(pth, n_, pairs_deg, [(0b001111, 0)]); cases.append(("all_degenerate_zero", n_, pairs_deg, [(0b001111, 0)], pth, 1e-9))
    for name, n, pairs, masks, pth, tau in cases:
        E0 = min(energies(n, pairs))
        for fr in FR:
            ordr, r, ret, BO, h = e2_model(pairs, fr)
            p = env.run(pth, "e2", 0.0, tau, E0, extra=["--frac", fr], tag="E1_bound"); kv = ca.parse_kv(p.stdout)
            if p.returncode:
                e1_bad.append((name, fr, "rc%d" % p.returncode)); continue
            cert = Fraction(float(kv["e2_B_O_certified"])); okc = cert >= BO and (BO == 0 or cert <= BO * Fraction(1 + 1e-12))
            if not okc or int(kv["e2_retained_pairs"]) != r or int(kv["e2_order_digest"]) != h:
                e1_bad.append((name, fr, "bound/order mismatch"))
            sample = range(1 << n) if n <= 8 else [rng.randrange(1 << n) for _ in range(150)]
            for s in sample:
                H = Fraction(0); HR = Fraction(0)
                for q, (i, j, k) in enumerate(pairs):
                    term = -Fraction(k) if ((s >> i) ^ (s >> j)) & 1 else Fraction(k)
                    H += term
                    if q in ret:
                        HR += term
                ineq_checked += 1
                if not (HR - BO <= H <= HR + BO):
                    e1_bad.append((name, fr, "inequality violated", s))
    rec("E1", "E2 omitted-interaction bound: H_R - B_O <= H <= H_R + B_O verified in exact rational arithmetic (%d state/fraction checks); the C++ certified B_O is >= the exact omitted weight (outward rounded); retained set and its ordering digest equal an independent re-implementation; mixed-sign, zero-coupling and all-degenerate instances included" % ineq_checked,
        "PROOF_PLUS_EXACT_ARITHMETIC", "PASS" if not e1_bad else "FAIL", inequality_checks=ineq_checked, mismatches=e1_bad[:10],
        proof="For every state s, |H_O(s)| = |sum_{(i,j) in O} K_ij s_i s_j| <= sum_O |K_ij| = B_O (triangle inequality, |s_i s_j| = 1), hence H_R - B_O <= H = H_R + H_O <= H_R + B_O. Rejecting a state needs H_R - B_O - eps > Ecut, accepting needs H_R + B_O + eps <= Ecut; eps (= eps_gray) bounds the rounding of the incrementally maintained H_R, so no actual target can be rejected and no non-target accepted.")
    # ---- E2: exact target-set equality with B0 and the oracle on public patches (all windows, several retained fractions) + 3x3 anchor
    res = {}; bad = []; nruns = 0
    for L in (1, 2):
        d = I[L]; En = energies(d["n"], d["pairs"]); E0 = min(En); Ws, levels = public_windows(En, d["tau"]); idsG = None
        for name, W in Ws:
            ref = {i for i, e in enumerate(En) if e <= E0 + W + d["tau"]}
            b0 = env.solve(d["path"], "b0", W, d["tau"], E0, tag="E2_public")[0]; nruns += 1
            for fr in FR:
                ids, kv = env.solve(d["path"], "e2", W, d["tau"], E0, extra=["--frac", fr], tag="E2_public"); nruns += 1
                if ids != ref or ids != b0:
                    bad.append((L, name, fr, len(ids), len(ref)))
            ids25, kv25 = env.solve(d["path"], "e2", W, d["tau"], E0, tag="E2_public_default"); nruns += 1
        res["%dx%d" % (L, L)] = dict(windows=len(Ws))
    ids3, kv3 = env.solve(I[3]["path"], "e2", 0.0, I[3]["tau"], X["E0f"], tag="E2_3x3_W0_anchor")
    b03, _ = env.solve(I[3]["path"], "b0", 0.0, I[3]["tau"], X["E0f"], tag="E2_3x3_W0_anchor")
    anchor_ok = ids3 == b03 and len(ids3) == X["anchor"]["ground_states"]
    # ---- degenerate / mixed-sign / zero-coupling instances: E2 and B0 against the exact oracle
    deg_bad = []; deg_runs = 0
    n_ = 6; pm = [(i, j, (1 if (i + j) % 2 else -1) * 0.25 * ((i * j) % 3)) for i in range(n_) for j in range(i + 1, n_)]; pz = [(i, j, 0.0) for i in range(n_) for j in range(i + 1, n_)]
    pu = [(i, j, 1.0 if (i + j) % 2 else -1.0) for i in range(n_) for j in range(i + 1, n_)]       # uniform magnitudes -> massive ties in |K| and in E
    for nm_, pr_ in (("mixed_zero", pm), ("all_zero", pz), ("uniform_mag", pu)):
        pth = tmp / ("deg_%s.txt" % nm_); write_instance(pth, n_, pr_, [(0b001111, 0)]); Qd_ = sum(abs(k) for _, _, k in pr_); td = max(1e-9 * Qd_, 1e-12)
        Ed = energies(n_, pr_); Ed0 = min(Ed); span = max(Ed) - Ed0
        for Wd in (0.0, 0.01 * span, 0.5 * span, 2 * span):
            refd = {i for i, e in enumerate(Ed) if e <= Ed0 + Wd + td}
            for md in ("b0", "e2", "g1", "g2", "b1"):
                for fr in ((0.0, 0.25, 0.5) if md == "e2" else (None,)):
                    ex = ["--frac", fr] if fr is not None else []
                    ids_d, _kv = env.solve(pth, md, Wd, td, Ed0, extra=ex, tag="E2_degenerate_instances"); deg_runs += 1
                    gramd = {i for i in refd if all(((i ^ nm2) & im2).bit_count() == 2 for im2, nm2 in [(0b001111, 0)])}
                    if ids_d != (gramd if md in ("g1", "g2") else refd):
                        deg_bad.append((nm_, md, Wd, fr))
    src_e2 = re.sub(r"//[^\n]*", "", (HERE / "e2_v009.cpp").read_text())
    gfree = not re.search(r"grammar_counted\s*\(|grammar_quiet\s*\(|\bNM\s*\[|\bIM\s*\[|\bnv\b", src_e2) and int(kv3["grammar_checks"]) == 0 and int(kv3["vertex_checks"]) == 0
    rec("E2", "E2 returns the complete target set equal to B0 and to the brute-force oracle on public 1x1 and 2x2 at W=0, every level threshold, 10*tau below it and every midpoint, for retained fractions %s; equals B0 at the disclosed 3x3 W=0 anchor; also equals the oracle on mixed-sign, zero-coupling, all-zero and tie-heavy instances (%d runs); the E2 source makes no grammar query and its grammar counters are zero" % (FR, deg_runs),
        "EXHAUSTIVE_REFERENCE_COMPARISON", "PASS" if (not bad and anchor_ok and not deg_bad and gfree) else "FAIL", runs=nruns, mismatches=bad[:10], degenerate_mismatches=deg_bad[:10], degenerate_runs=deg_runs, e2_source_grammar_free=gfree,
        per_patch=res, anchor_3x3_W0_equal_to_b0=anchor_ok, e2_default_fraction=PROPOSED["e2_frac"])
    # ---- E3: ambiguous cases fall back to the full exact evaluation; random synthetic instances/windows/fractions never lose or gain a state
    wrong = 0; nfb = 0; ncase = 0; amb = 0; hp_used = 0
    for t in range(150):
        n = rng.randint(6, 11); pairs, masks, _g = synth_instance(rng, n, scale=rng.choice((0.01, 1.0))); pth = tmp / "e3.txt"; write_instance(pth, n, pairs, masks)
        Qs = sum(abs(k) for _, _, k in pairs); ts = tol.REL_TAU * Qs; En = energies(n, pairs); E0 = min(En); span = max(En) - E0
        W = rng.choice((0.0, 0.01, 0.05, 0.2, 0.5, 1.5)) * span; fr = rng.choice((0.05, 0.1, 0.25, 0.5, 0.75))
        ref = {i for i, e in enumerate(En) if e <= E0 + W + ts}
        ids, kv = env.solve(pth, "e2", W, ts, E0, extra=["--frac", fr], tag="E3_random"); ncase += 1
        if ids != ref:
            wrong += 1
        nfb += int(kv["e2_fallbacks"]); amb += int(kv["e2_fallbacks"]) > 0; hp_used += int(kv["hp_evals"])
    # adversarial: very small retained fraction so almost every state is ambiguous -> all fall back, result still exact
    n = 10; pairs, masks, _g = synth_instance(rng, n); pth = tmp / "e3a.txt"; write_instance(pth, n, pairs, masks); En = energies(n, pairs); E0 = min(En); ts = 1e-9 * sum(abs(k) for _, _, k in pairs)
    idsA, kvA = env.solve(pth, "e2", 0.3 * (max(En) - E0), ts, E0, extra=["--frac", 0.0], tag="E3_all_fallback")
    refA = {i for i, e in enumerate(En) if e <= E0 + 0.3 * (max(En) - E0) + ts}
    all_fb = int(kvA["e2_fallbacks"]) + int(kvA["cert_rejects"]) + int(kvA["cert_accepts"]) == 1 << n and idsA == refA and int(kvA["cert_accepts"]) == 0
    rec("E3", "E2 ambiguous-case handling: %d random synthetic instances/windows/fractions (%d with fallbacks, %d fallback evaluations) all equal the oracle; with zero retained pairs every undecided state falls back to the full exact evaluation and the result is still exact" % (ncase, amb, nfb),
        "RANDOMISED_EXACT_COMPARISON", "PASS" if (wrong == 0 and all_fb and amb > 0) else "FAIL", wrong_sets=wrong, instances_with_fallback=amb, total_fallbacks=nfb, hp_evaluations=hp_used,
        all_fallback_case_exact=all_fb)
    # ---- E4: charged-cost completeness and exact accounting identities
    def expected_e2(n, pairs, frac, kv, z2=0):
        ordr, r, ret, BO, h = e2_model(pairs, frac); deg = [0] * n
        for p in ret:
            deg[pairs[p][0]] += 1; deg[pairs[p][1]] += 1
        N0 = 1 << (n - z2); t = np.arange(1, N0, dtype=np.int64); low = t & (-t); k = np.log2(low).astype(np.int64)
        inc = (t % 256) != 0; degarr = np.array(deg, dtype=np.int64)
        steps = int(np.sum(degarr[k[inc]] + 1)); nres = 1 + (N0 - 1) // 256
        return nres * 3 * r + steps + (int(kv["full_energy_evals"]) + int(kv["hp_evals"])) * len(pairs), nres
    def expected_b0(n, pairs, kv, z2=0):
        N0 = 1 << (n - z2); nres = 1 + (N0 - 1) // 256; incr = (N0 - 1) - (N0 - 1) // 256
        return nres * (n * n + len(pairs)) + incr * (n + 1) + (int(kv["full_energy_evals"]) + int(kv["hp_evals"])) * len(pairs), nres
    acct = {}; acct_bad = []
    for L, W in ((2, 0.0), (3, 0.0)):
        d = I[L]; E0 = X["refs"][L]
        for mode in ("e2", "b0"):
            ids, kv = env.solve(d["path"], mode, W, d["tau"], E0, tag="E4_accounting")
            exp, nres = (expected_e2(d["n"], d["pairs"], PROPOSED["e2_frac"], kv) if mode == "e2" else expected_b0(d["n"], d["pairs"], kv))
            N0 = 1 << d["n"]
            ok = int(kv["pair_ops"]) == exp and int(kv["resyncs"]) == nres and int(kv["states_visited"]) == N0
            if mode == "e2":
                ok = ok and int(kv["bound_evals"]) == N0 and int(kv["cert_rejects"]) + int(kv["cert_accepts"]) + int(kv["e2_fallbacks"]) == N0
            acct["%dx%d/%s" % (L, L, mode)] = dict(reported_pair_ops=int(kv["pair_ops"]), model_pair_ops=exp, ok=ok)
            if not ok:
                acct_bad.append((L, mode))
        ids, kv = env.solve(d["path"], "g1", W, d["tau"], E0, tag="E4_accounting")
        ok = int(kv["grammar_checks"]) == 1 << d["n"] and int(kv["full_energy_evals"]) == int(kv["materialized"])
        acct["%dx%d/g1" % (L, L)] = dict(grammar_checks=int(kv["grammar_checks"]), energy_evals=int(kv["full_energy_evals"]), survivors=int(kv["materialized"]), ok=ok)
        if not ok:
            acct_bad.append((L, "g1"))
    RULES = {"states_visited": "nominal states touched by a scan (B0, E2, G1, nullgap)", "nodes": "assignments tried in a search tree (G2, B1)", "leaves": "complete assignments reached (G2, B1)",
             "grammar_checks": "full-state grammar evaluations (G1); vertex_checks counts each vertex popcount test (G1, G2)", "pair_ops": "pair-term multiply-adds: direct/hp energies cost npairs; incremental field updates cost (n-1-pos)+1 (G2,B1), n+1 (B0), deg_R(k)+1 (E2); resync costs n*n+npairs (B0) or 3|R| (E2)",
             "field_updates": "incremental updates of the local fields/energy", "full_energy_evals": "direct double-precision energy evaluations of one state (npairs terms)", "hp_evals": "__float128 evaluations of one state (boundary cascade)",
             "bound_evals": "branch-and-bound lower-bound (B1) or certified interval (E2) evaluations", "cert_rejects/cert_accepts/e2_fallbacks": "E2 certified rejection / certified acceptance / exact fallback evaluation",
             "resyncs": "exact recomputation of the Gray-code state every 256 steps", "t_*": "monotonic wall-clock phase timers; t_serialize_s = writing the id list; t_read_input_s = parsing the instance", "cpu_s": "user+system CPU of the process", "maxrss_kb": "peak resident set (process)",
             "z2_expansions": "symmetry expansions (sensitivity mode only)", "E0 certification": "reported as separate cert_b0 / cert_b1 ledger rows"}
    rec("E4", "Charged-cost completeness: E2 and B0 pair-operation counters equal an independent analytic model EXACTLY (including Gray-code resynchronisation, certified decisions and fallback evaluations) on 2x2 and the 3x3 anchor; G1 counters equal their definitions; every counter has a defined accounting rule",
        "ANALYTIC_ACCOUNTING_IDENTITY", "PASS" if not acct_bad else "FAIL", checks=acct, mismatches=acct_bad, counting_rules=RULES)
    # ---- E2 retained-fraction sweep on SYNTHETIC inputs only (no real 3x3 target is examined)
    n = 24; rngs = random.Random(PROPOSED["master_seed"] + 5)
    pairs_g = [(i, j, rngs.gauss(0, 1.0)) for i in range(n) for j in range(i + 1, n)]
    sc = I[3]["Q"] / sum(abs(k) for _, _, k in pairs_g); pairs_g = [(i, j, k * sc) for i, j, k in pairs_g]
    # "realmag": the public real-3x3 coupling MAGNITUDES (a property of the frozen geometry, no Hamiltonian outcome) with independently randomised signs
    pairs_r = [(i, j, abs(k) * rngs.choice((-1.0, 1.0))) for i, j, k in I[3]["pairs"]]
    X["synth24"] = dict(pairs=pairs_g, masks=I[3]["masks"], name="gauss"); X["synth24r"] = dict(pairs=pairs_r, masks=I[3]["masks"], name="realmag")
    sweep = {}
    for key, nm in (("synth24", "gauss"), ("synth24r", "realmag")):
        sy = X[key]; pth = tmp / (key + ".txt"); write_instance(pth, 24, sy["pairs"], I[3]["masks"])
        sy.update(path=pth, Q=sum(abs(k) for _, _, k in sy["pairs"])); sy["tau"] = tol.REL_TAU * sy["Q"]
        assert pth.read_bytes() != I[3]["path"].read_bytes()
        pc = env.run(pth, "cert_b1", 0, sy["tau"], tag="synthetic_E0", synthetic=True)
        sy["E0"] = float(ca.parse_kv(pc.stdout)["E0_certified"])
        sw = {}
        for fr in (0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0):
            row = {}
            for wn, W in (("1kT", X["kT_norm"]), ("2kT", 2 * X["kT_norm"])):
                p = env.run(pth, "e2", W, sy["tau"], sy["E0"], extra=["--frac", fr], tag="E2_fraction_sweep_synthetic", synthetic=True)
                kv = ca.parse_kv(p.stdout); row[wn] = dict(wall_s=float(kv["wall_s"]), pair_ops=int(kv["pair_ops"]), fallbacks=int(kv["e2_fallbacks"]), cert_accepts=int(kv["cert_accepts"]), targets=int(kv["target_count"]), retained_weight=float(kv["e2_retained_weight_fraction"]))
            sw[str(fr)] = row
        sw["b0"] = {wn: dict(wall_s=float(ca.parse_kv(env.run(pth, "b0", W, sy["tau"], sy["E0"], tag="E2_fraction_sweep_synthetic", synthetic=True).stdout)["wall_s"])) for wn, W in (("1kT", X["kT_norm"]), ("2kT", 2 * X["kT_norm"]))}
        sweep[nm] = sw
    cand = [0.05, 0.1, 0.25, 0.5, 0.75, 0.9]
    worst_ops = {f: max(sweep[nm][str(f)][w]["pair_ops"] for nm in sweep for w in ("1kT", "2kT")) for f in cand}
    rec_frac = min(cand, key=lambda f: (worst_ops[f], f)); X["e2_recommended_fraction"] = rec_frac
    ratio25 = {nm: sweep[nm]["0.25"]["1kT"]["wall_s"] / max(sweep[nm]["b0"]["1kT"]["wall_s"], 1e-9) for nm in sweep}
    recommendation = ("The spec-proposed 25%% is exact (E1-E3) but, on flat-coupling synthetic 24-spin instances, its certified interval is rarely decisive, so E2 degenerates towards a full fallback scan (wall ratio E2(25%%)/B0 at 1 kT: %s). "
                      "Measured worst-case pair operations over {gauss, realmag} x {1 kT, 2 kT} are lowest at a retained fraction of %g%% (candidates 5-90%%; 100%% is B0 in disguise and is excluded). v009 therefore RECOMMENDS %g%% as the prospective E2 setting and keeps 25%% only as the spec's nominal value; neither is frozen. "
                      "The choice used synthetic data only, no 3x3 target. The real 3x3 W=0 anchor E2 cost is reported in the ledger." % (", ".join("%s %.1fx" % (k, v) for k, v in ratio25.items()), rec_frac * 100, rec_frac * 100))
    DIAG["E2_VALIDATION"] = dict(tests=["E1", "E2", "E3", "E4"], default_fraction=PROPOSED["e2_frac"], recommended_fraction=rec_frac, worst_pair_ops_by_fraction=worst_ops, ordering_rule="|K| descending, ties by smaller pair index (no target information)",
                                 synthetic_n24_fraction_sweep=sweep, accounting=acct, counting_rules=RULES, recommendation=recommendation,
                                 e2_allowed_slower_than_b0=True)


# ================================================================ W1 : thermal windows vs the PUBLIC small-patch gaps
def test_W(X):
    env, I = X["env"], X["inst"]; kT = X["kT_norm"]; rows = []; bad = []
    kT_ok = abs(X["kT_J"] - 1.09347e-20) < 5e-26 and abs(kT - 0.010831) < 2e-6
    spec_kT = 1.093473608e-20; kT_rel_diff = abs(X["kT_J"] - spec_kT) / X["kT_J"]
    for L, disclosed in ((1, 0.871), (2, 0.952)):
        d = I[L]; En = energies(d["n"], d["pairs"]); E0 = min(En)
        p = env.run(d["path"], "nullgap", 0.0, d["tau"], E0, tag="W1_public_gap_%dx%d" % (L, L))
        if p.returncode:
            raise Blocked("nullgap failed on public %dx%d: %s" % (L, L, p.stderr[-200:]))
        kv = ca.parse_kv(p.stdout); delta = float(kv["delta_nonG"]); nex = int(kv["n_excluded"])
        oracle = min(e - E0 for i, e in enumerate(En) if not all(((i ^ nm) & im).bit_count() == 2 for im, nm in d["masks"]))
        if abs(delta - oracle) > 1e-12 * d["Q"]:
            bad.append(("gap_vs_oracle", L, delta, oracle))
        gk = delta / kT
        if abs(gk - disclosed) > 0.002:
            bad.append(("gap_vs_disclosed", L, gk, disclosed))
        for nm, mult in (("sensitivity_A_0.5kT", 0.5), ("primary_1kT", 1.0), ("sensitivity_B_2kT", 2.0)):
            W = mult * kT; st, reason, flags = tol.preservation(delta, W, d["tau"], tol.hierarchy(d["Q"], len(d["pairs"]))["eps_input"], nex == 0)
            rows.append(dict(patch="%dx%d" % (L, L), window=nm, W_over_kT=mult, delta_over_kT=gk, rho=(W + d["tau"]) / delta, status=st, reason=reason))
    exp = {("1x1", "sensitivity_A_0.5kT"): "PASS", ("1x1", "primary_1kT"): "FAIL", ("2x2", "sensitivity_A_0.5kT"): "PASS", ("2x2", "primary_1kT"): "FAIL", ("2x2", "sensitivity_B_2kT"): "FAIL", ("1x1", "sensitivity_B_2kT"): "FAIL"}
    for r in rows:
        e = exp.get((r["patch"], r["window"]))
        if e and r["status"] != e:
            bad.append(("classification", r["patch"], r["window"], r["status"]))
    X["W1_rows"] = rows
    DIAG["TOLERANCE"]["W1_public_gap_table"] = rows
    rec("W1", "Thermal windows vs the PUBLIC small-patch gaps: k_BT_ref(792 K) = k_B*792 = %.9e J (the specification prints 1.093473608e-20 J, a 3.7e-7 relative typo vs the SI-exact product; 1.09347e-20 agrees) = %.6f (A units); C++ nullgap on the public 1x1 and 2x2 patches reproduces the disclosed gaps (~0.871 and ~0.952 k_BT) and the exact-oracle gap; the 0.5x/1x/2x classification table is generated. The 3x3 gap is withheld (not computed)" % (X["kT_J"], kT),
        "PUBLIC_PATCH_COMPARISON", "PASS" if (not bad and kT_ok) else "FAIL", kT_J=X["kT_J"], kT_norm=kT, kT_check=kT_ok, kT_spec_printed_J=spec_kT, kT_spec_relative_difference=kT_rel_diff, rows=rows, mismatches=bad,
        disclosure="At the primary window k_BT_ref the public 1x1 and 2x2 patches are already NOT preserved (W > gap); the primary window was proposed with this knowledge, so a 3x3 failure is not a surprise outcome and must not be interpreted as independent evidence.")


# ================================================================ T1, T2, T3 : tolerance, boundary, zero-gap, empty-excluded
def dyadic_instance(rng, n=8):
    for _ in range(2000):
        pairs = [(i, j, rng.choice((-0.5, -0.25, -0.125, 0.125, 0.25, 0.5))) for i in range(n) for j in range(i + 1, n)]
        masks = []
        for _v in range(rng.randint(1, 3)):
            isl = rng.sample(range(n), 4); masks.append((sum(1 << i for i in isl), sum(1 << i for i in isl if rng.random() < 0.5)))
        g = grammar_flags(n, masks)
        if not (4 <= sum(g) < (1 << n)):
            continue
        En = [tol.energy_exact(n, pairs, s) for s in range(1 << n)]
        E0 = min(En)
        if not g[En.index(E0)]:
            continue
        D = min(En[s] for s in range(1 << n) if not g[s]) - E0
        if D > 0:
            return n, pairs, masks, g, En, E0, D
    raise Blocked("no dyadic instance")


def test_T(X):
    env, I, tmp = X["env"], X["inst"], X["tmp"]; rng = random.Random(PROPOSED["master_seed"] + 31)
    # ---- T1
    table = [("gap > W+tau", tol.preservation(1.0, 0.5, 0.1), "PASS"), ("gap == W+tau", tol.preservation(1.0, 0.9, 0.1), "FAIL"), ("gap < W+tau", tol.preservation(1.0, 0.95, 0.1), "FAIL"),
             ("gap == 0", tol.preservation(0.0, 0.0, 0.1), "FAIL"), ("gap == 0, W>0", tol.preservation(0.0, 0.3, 0.1), "FAIL"), ("S_G == S_0 (empty excluded set)", tol.preservation(None, 0.3, 0.1, empty_excluded=True), "PASS")]
    tab_ok = all(r[0] == e for _, r, e in table) and "EMPTY_EXCLUDED_SET_NOT_INFORMATIVE" in table[-1][1][2]
    n, pairs, masks, g, En, E0, D = dyadic_instance(rng); pth = tmp / "dyadic.txt"; write_instance(pth, n, pairs, masks)
    Qd = sum(abs(k) for _, _, k in pairs); tau = 2.0 ** -27; hier = tol.hierarchy(Qd, len(pairs)); E0d = float(E0)
    offs = [2.0 ** -30, 2.0 ** -45, 2.0 ** -50, 0.0, -2.0 ** -50, -2.0 ** -45, -2.0 ** -30]; rows = []; bad = []
    for gcut in offs:
        W = float(D - Fraction(tau) - Fraction(gcut)); assert W >= 0 and Fraction(W) == D - Fraction(tau) - Fraction(gcut), "dyadic construction not exact"
        exp_status = tol.preservation(float(D), W, tau, eps_input=hier["eps_input"])[0]
        for mode in ("b0", "b1", "e2"):
            ids, kv = env.solve(pth, mode, W, tau, E0d, tag="T1_boundary")
            FN = len([s for s in ids if not g[s]]); got = "PASS" if FN == 0 else "FAIL"
            unres = int(kv["unresolved_boundary"])
            if got != exp_status or (abs(gcut) <= hier["eps_input"] and unres < 1) or (abs(gcut) > hier["eps_input"] and unres != 0):
                bad.append((gcut, mode, got, exp_status, unres))
            rows.append(dict(gap_minus_Wplustau=gcut, solver=mode, FN=FN, unresolved=unres, hp_evals=int(kv["hp_evals"]), expected=exp_status, got=got))
    rec("T1", "Threshold equality and near-boundary behaviour: classification table (gap > / = / < W+tau, zero gap, empty excluded set) and exact dyadic instances with gap-minus-(W+tau) in {+-2^-30, +-2^-45, +-2^-50, 0}: B0, B1 and E2 agree with the exact-rational oracle; equality and sub-resolution (|d| <= eps_input) cases are UNRESOLVED_BOUNDARY and conservatively FAIL",
        "EXACT_ARITHMETIC_CONSTRUCTION", "PASS" if (tab_ok and not bad) else "FAIL", classification_table=[dict(case=c, status=r[0], reason=r[1], flags=r[2], expected=e) for c, r, e in table],
        boundary_runs=rows, mismatches=bad, eps_input=hier["eps_input"], eps_direct=hier["eps_direct"], tau=tau, Q=Qd)
    # ---- T2 : zero gap, empty excluded set, nullgap equivalence
    zero_case = None
    for _ in range(400):
        nn = rng.randint(7, 10); pr, mk, gg = synth_instance(rng, nn); Ens = energies(nn, pr); E0s = min(Ens)
        if not gg[Ens.index(E0s)]:
            zero_case = (nn, pr, mk, gg, Ens, E0s); break
    nn, pr, mk, gg, Ens, E0s = zero_case; pz = tmp / "zerogap.txt"; write_instance(pz, nn, pr, mk); Qz = sum(abs(k) for _, _, k in pr); tz = tol.REL_TAU * Qz
    pn = env.run(pz, "nullgap", 0.0, tz, E0s, tag="T2_zero_gap"); kvn = ca.parse_kv(pn.stdout); dz = float(kvn["delta_nonG"])
    idsz, _ = env.solve(pz, "b0", 0.0, tz, E0s, tag="T2_zero_gap"); FNz = len([s for s in idsz if not gg[s]])
    zero_ok = abs(dz) <= 1e-12 * Qz and tol.preservation(dz if dz > tz else 0.0, 0.0, tz)[0] == "FAIL" and FNz >= 1
    n0 = 8; pe0 = [(i, j, rng.gauss(0, 0.1)) for i in range(n0) for j in range(i + 1, n0)]; pq = tmp / "emptyexcl.txt"; write_instance(pq, n0, pe0, [])
    E0e = min(energies(n0, pe0)); Qe = sum(abs(k) for _, _, k in pe0); te = tol.REL_TAU * Qe
    pn = env.run(pq, "nullgap", 0.0, te, E0e, tag="T2_empty_excluded"); kve = ca.parse_kv(pn.stdout)
    ids_e, _ = env.solve(pq, "b0", 0.5 * Qe, te, E0e, tag="T2_empty_excluded")
    st = tol.preservation(None if kve["delta_nonG"] in ("inf", "+inf") else float(kve["delta_nonG"]), 0.5 * Qe, te, empty_excluded=int(kve["empty_excluded_set"]) == 1)
    empty_ok = kve["delta_nonG"] in ("inf", "+inf") and int(kve["empty_excluded_set"]) == 1 and st[0] == "PASS" and "EMPTY_EXCLUDED_SET_NOT_INFORMATIVE" in st[2] and len(ids_e) > 0
    eq_bad = []; ncmp = 0
    cmp_cases = [(L, I[L]["n"], I[L]["pairs"], I[L]["masks"], I[L]["path"], I[L]["tau"], I[L]["Q"]) for L in (1, 2)]
    rng2 = random.Random(PROPOSED["master_seed"] + 32)
    for t in range(25):
        nn2 = rng2.randint(7, 12); pr2, mk2, _g2 = synth_instance(rng2, nn2)
        cmp_cases.append(("syn%d" % t, nn2, pr2, mk2, None, tol.REL_TAU * sum(abs(k) for _, _, k in pr2), sum(abs(k) for _, _, k in pr2)))
    pres_bad = []
    for name, nn2, pr2, mk2, p2, t2, Q2 in cmp_cases:
        if p2 is None:
            p2 = tmp / "t2cmp.txt"; write_instance(p2, nn2, pr2, mk2)
        Ens2 = energies(nn2, pr2); E02 = min(Ens2); g2 = grammar_flags(nn2, mk2)
        excl = [Ens2[s] - E02 for s in range(1 << nn2) if not g2[s]]
        dpy = min(excl) if excl else None
        kvn2 = ca.parse_kv(env.run(p2, "nullgap", 0.0, t2, E02, tag="T2_nullgap_vs_python").stdout); ncmp += 1
        dcp = float(kvn2["delta_nonG"]); okd = (dpy is None and dcp == math.inf) or (dpy is not None and abs(dcp - dpy) <= 1e-12 * Q2)
        if not okd or int(kvn2["n_grammar"]) != sum(g2):
            eq_bad.append((name, dpy, dcp)); continue
        if dpy is not None and dpy > 0:
            for fac in (0.5, 0.999, 1.0001, 1.5):
                W = fac * dpy; ids, _ = env.solve(p2, "b0", W, t2, E02, tag="T2_preservation_relation")
                FN = len([s for s in ids if not g2[s]]); pstat = tol.preservation(dcp, W, t2, eps_input=2.0 ** -52 * Q2)[0]
                if (FN == 0) != (pstat == "PASS"):
                    pres_bad.append((name, fac, FN, pstat))
    rec("T2", "Zero-gap and empty-excluded-set handling, and the gap/preservation equivalence: ground level excluded -> Delta = 0 and FAIL; S_G = S_0 -> Delta = +inf, PASS with the empty-excluded-set flag; C++ nullgap equals a Python brute force on %d instances (incl. public 1x1/2x2) and PRESERVED <=> FN = 0 across windows around Delta" % ncmp,
        "EXACT_COMPARISON", "PASS" if (zero_ok and empty_ok and not eq_bad and not pres_bad) else "FAIL", zero_gap_delta=dz, zero_gap_FN=FNz, empty_excluded_flag=kve.get("empty_excluded_set"), empty_excluded_status=st[0], nullgap_mismatches=eq_bad[:5],
        preservation_relation_mismatches=pres_bad[:5], compared=ncmp)
    # ---- T3 : conservative treatment of evaluation error (randomised near-tie property test against an exact-rational oracle)
    nprop = 700; viol = 0; cons_loss = 0; cats = {}; unres_total = 0; hp_total = 0; set_bad = []; excl_to_pres = 0; rr = random.Random(PROPOSED["master_seed"] + 33)
    for case in range(nprop):
        n = rr.randint(5, 7); pr = [(i, j, rr.gauss(0, rr.choice((0.01, 1.0)))) for i in range(n) for j in range(i + 1, n)]
        Qc = sum(abs(k) for _, _, k in pr); hier = tol.hierarchy(Qc, len(pr)); tauc = hier["tau"]
        masks = []
        for _v in range(rr.randint(1, 2)):
            isl = rr.sample(range(n), 4); masks.append((sum(1 << i for i in isl), sum(1 << i for i in isl if rr.random() < 0.5)))
        g = grammar_flags(n, masks)
        if sum(g) == 0:
            continue
        Ex = [tol.energy_exact(n, pr, s) for s in range(1 << n)]; Ed = energies(n, pr); E0d = min(Ed)
        t = rr.randrange(1 << n); catn = rr.choice(("eps_input*0.3", "eps_input*3", "eps_direct*0.5", "eps_direct*2", "eps_gray*0.5", "eps_gray*2", "tau*0.5", "tau*2", "zero", "wide"))
        base = {"eps_input": hier["eps_input"], "eps_direct": hier["eps_direct"], "eps_gray": hier["eps_gray"], "tau": tauc}.get(catn.split("*")[0], 0.0)
        mult = float(catn.split("*")[1]) if "*" in catn else 0.0
        off = rr.choice((-1, 1)) * (base * mult if catn != "wide" else rr.uniform(0.01, 1.0) * Qc)
        cut = Ex[t] + Fraction(off); W = float(cut - Fraction(E0d) - Fraction(tauc))
        if W < 0:
            continue
        cutr = Fraction(E0d) + Fraction(W) + Fraction(tauc)
        oracle = {s for s in range(1 << n) if tol.membership_oracle(Ex[s], E0d, W, tauc, hier["eps_input"]) in ("IN", "UNRESOLVED")}
        exact_strict = {s for s in range(1 << n) if Ex[s] <= Fraction(E0d) + Fraction(W)}
        p = tmp / "t3.txt"; write_instance(p, n, pr, masks); cats[catn] = cats.get(catn, 0) + 1
        for mode in ("b0", "b1", "e2", "g2"):
            ids, kv = env.solve(p, mode, W, tauc, E0d, extra=(["--frac", 0.25] if mode == "e2" else []), tag="T3_property")
            want = oracle if mode != "g2" else {s for s in oracle if g[s]}
            if ids != want:
                set_bad.append((case, mode, catn, len(ids), len(want)))
            if mode in ("b0", "e2"):
                if not exact_strict <= ids:
                    viol += 1
                unres_total += int(kv["unresolved_boundary"]); hp_total += int(kv["hp_evals"])
                fn_exact = len([s for s in exact_strict if not g[s]]); fn_solver = len([s for s in ids if not g[s]])
                if fn_exact > 0 and fn_solver == 0:
                    excl_to_pres += 1
                if fn_exact == 0 and fn_solver > 0:
                    cons_loss += 1
    rec("T3", "Conservative numerical error treatment (%d randomised near-threshold cases, offsets from 0.3 eps_input to 100 eps_gray and wide, across B0/B1/E2/G2): every solver set equals the exact-rational oracle (UNRESOLVED_BOUNDARY included conservatively); the tolerance never removes an exactly-inclusive target and never turns an excluded target into a preserved one" % sum(cats.values()),
        "EXACT_RATIONAL_ORACLE", "PASS" if (not set_bad and viol == 0 and excl_to_pres == 0) else "FAIL", cases=sum(cats.values()), categories=cats, set_mismatches=set_bad[:10], targets_lost=viol,
        excluded_target_converted_to_preserved=excl_to_pres, marginal_pass_turned_fail=cons_loss, unresolved_boundary_events=unres_total, higher_precision_evaluations=hp_total,
        three_tolerances=dict(note="level grouping (1e-9 * max|E|, reporting of degenerate levels only), evaluation error (eps_direct, eps_gray), and membership tolerance tau are distinct quantities; only tau enlarges the target, only eps_input defines UNRESOLVED_BOUNDARY"))
    DIAG["TOLERANCE"] = dict(policy=PROPOSED["tie_rule"], rel_tau=PROPOSED["rel_tau"], hierarchy_example_3x3_Q=tol.hierarchy(I[3]["Q"], len(I[3]["pairs"])), hierarchy_example_2x2_Q=tol.hierarchy(I[2]["Q"], len(I[2]["pairs"])),
                             gray_drift_rigorous_bound_over_Q=tol.drift_bound_rigorous(1.0), gray_margin_over_Q=PROPOSED["rel_gray"], status="PROPOSED -- final constant must be frozen before any W>0 unblinding",
                             T1_rows=rows, T3_categories=cats, T3_unresolved_events=unres_total)


# ================================================================ N1, N2, N3 : seeds and nulls (target-blind)
def make_survivors_fn(X, n, tag, cap=None):
    env, tmp = X["env"], X["tmp"]; path = tmp / ("gnull_%s.txt" % tag); stats = dict(calls=0, seconds=0.0)
    def fn(inc):
        write_instance(path, n, [], ew.compile_masks(inc)); t0 = time.perf_counter()
        p = env.run(path, "gcount", 0, 0, extra=["--cap", cap or PROPOSED["null_cap"]], tag="null_survivor_count_" + tag)
        stats["calls"] += 1; stats["seconds"] += time.perf_counter() - t0
        kv = ca.parse_kv(p.stdout)
        return None if int(kv["cap_hit"]) else int(kv["survivors"])
    fn.stats = stats
    return fn


def test_N(X):
    env, I, tmp = X["env"], X["inst"], X["tmp"]; v6 = sd.load_v006_nulls(FEAS); inc_real = I[3]["inc"]
    # ---- build the registry on the real 3x3 incidence (grammar-only; no Hamiltonian is evaluated)
    reg, acct, gstat = {}, {}, {}
    t0 = time.perf_counter()
    for key, fam in sd.FAMILIES.items():
        fn = make_survivors_fn(X, 24, key)
        nulls, acc = sd.generate(fam, inc_real, 24, PROPOSED["n_nulls_per_family"], fn, v6, max_tries=5 * PROPOSED["n_nulls_per_family"])
        reg[key] = nulls; acct[key] = acc; gstat[key] = dict(survivor_count_calls=fn.stats["calls"], seconds_total=fn.stats["seconds"])
    gen_seconds = time.perf_counter() - t0
    entries = [dict(family=k, idx=e["idx"], label=e["label"], seed_sha256=e["seed_sha256"], inc_sha256=e["inc_sha256"], survivors=e["survivors"]) for k in reg for e in reg[k]]
    X["null_registry"] = dict(entries=entries, accounting=acct, digest=sd.registry_digest(entries))
    # ---- N1 : deterministic regeneration
    bad = []
    for key, fam in sd.FAMILIES.items():
        for idx in range(200):
            if sd.label(fam, idx) != "%d|%s|%d" % (v6.MASTER_SEED, fam, idx) or sd.rng_for(fam, idx).random() != v6.rng_for(fam, idx).random():
                bad.append((fam, idx, "derivation differs from frozen v006"))
    v6csv = {}
    with open(V6 / "NULLS_v006.csv") as f:
        for r in csv.DictReader(f):
            v6csv[(r["family"], int(r["idx"]))] = r["seed"]
    for (fam, idx), seed in list(v6csv.items())[:200]:
        if sd.label(fam, idx) != seed:
            bad.append((fam, idx, "label differs from NULLS_v006.csv"))
    # second in-process regeneration of the first 100 accepted nulls per family
    fn2 = make_survivors_fn(X, 24, "regen")
    again = {}
    for key, fam in sd.FAMILIES.items():
        nl, _ = sd.generate(fam, inc_real, 24, 100, fn2, v6, max_tries=2000); again[key] = [dict(family=key, idx=e["idx"], seed_sha256=e["seed_sha256"], inc_sha256=e["inc_sha256"], survivors=e["survivors"]) for e in nl]
        first = [dict(family=key, idx=e["idx"], seed_sha256=e["seed_sha256"], inc_sha256=e["inc_sha256"], survivors=e["survivors"]) for e in reg[key][:100]]
        if sd.registry_digest(again[key]) != sd.registry_digest(first):
            bad.append((key, "in-process regeneration differs"))
    # cross-process regeneration of raw incidence draws
    probe = tmp / "probe.py"
    probe.write_text("import sys, json, hashlib\nsys.dont_write_bytecode=True\nsys.path.insert(0, %r)\nimport seeds_v009 as sd\nv6 = sd.load_v006_nulls(%r)\n" % (str(HERE), str(FEAS)) +
                     "import energy_windows_v006 as ew\npe = ew.load_v005(); isl = pe.source_geometry(3); inc, _ = ew.build_incidence(pe, isl, pe.vertex_positions(3))\n"
                     "out = {}\nfor fam in sd.FAMILIES.values():\n    h = hashlib.sha256()\n    for idx in range(150):\n        i2, a, r = sd.draw(fam, idx, inc, 24, v6); h.update(sd.inc_sha256(i2).encode())\n    out[fam] = h.hexdigest()\nprint(json.dumps(out))\n")
    sub = json.loads(subprocess.run([sys.executable, "-I", str(probe)], capture_output=True, text=True, cwd=str(tmp)).stdout)
    here = {}
    for fam in sd.FAMILIES.values():
        h = hashlib.sha256()
        for idx in range(150):
            i2, a, r = sd.draw(fam, idx, inc_real, 24, v6); h.update(sd.inc_sha256(i2).encode())
        here[fam] = h.hexdigest()
    if sub != here:
        bad.append("cross-process draw digests differ")
    rec("N1", "Deterministic seed regeneration: the domain-separated derivation '<master>|<family>|<idx>' equals the frozen v006 derivation (200 draws/family, NULLS_v006.csv labels), the first 100 accepted nulls per family regenerate bit-identically in-process and the first 150 raw draws regenerate identically in a fresh interpreter",
        "DETERMINISM", "PASS" if not bad else "FAIL", mismatches=bad[:10], registry_digest=X["null_registry"]["digest"], master_seed=PROPOSED["master_seed"])
    # ---- N2 : well-formedness, accounting, counter cross-check, controls, machinery on public patch
    wf_bad = []; acc_bad = []
    for key, fam in sd.FAMILIES.items():
        for e in reg[key]:
            ok, why = sd.well_formed(e["inc"], inc_real, 24, fam, v6)
            if not ok or e["survivors"] < 1:
                wf_bad.append((key, e["idx"], why))
        a = acct[key]; rej = sum(v for k, v in a.items() if k.startswith("rejected:"))
        if a["attempted"] != a["accepted"] + a.get("duplicate", 0) + rej or a["exhausted"] or a["accepted"] != PROPOSED["n_nulls_per_family"]:
            acc_bad.append((key, a))
    cc_bad = []; rr = random.Random(PROPOSED["master_seed"] + 41)
    for key in sd.FAMILIES:
        for e in rr.sample(reg[key], 8):
            pth = tmp / "ccheck.txt"; write_instance(pth, 24, [], ew.compile_masks(e["inc"]))
            a = ca.parse_kv(env.run(pth, "gcount", 0, 0, tag="null_crosscheck_gcount").stdout); b = ca.parse_kv(env.run(pth, "gscan", 0, 0, tag="null_crosscheck_gscan").stdout)
            if a["survivors"] != b["survivors"] or a["digest"] != b["digest"] or int(a["survivors"]) != e["survivors"]:
                cc_bad.append((key, e["idx"]))
    real_cnt = make_survivors_fn(X, 24, "ctl")(inc_real); pert = make_survivors_fn(X, 24, "ctl2")(v6.perturbed_control(inc_real))
    pw = tmp / "ctlp.txt"; write_instance(pw, 24, [], ew.compile_masks(v6.perturbed_control(inc_real))); dg_p = ca.parse_kv(env.run(pw, "gcount", 0, 0, tag="control").stdout)["digest"]
    pr_ = tmp / "ctlr.txt"; write_instance(pr_, 24, [], I[3]["masks"]); dg_r = ca.parse_kv(env.run(pr_, "gcount", 0, 0, tag="control").stdout)["digest"]
    ctl_ok = real_cnt == 2604 and dg_p != dg_r
    # public 2x2: C++ counter vs python brute force, and nullgap pipeline vs python for nulls of both families (machinery equivalence only; no preservation statistics are reported)
    pub_bad = []; pub_n = 0
    inc2 = I[2]["inc"]; fn2x2 = make_survivors_fn(X, 12, "pub")
    for key, fam in sd.FAMILIES.items():
        nl, _ = sd.generate(fam, inc2, 12, 30, fn2x2, v6, max_tries=2000)
        for e in nl:
            masks = ew.compile_masks(e["inc"]); g = grammar_flags(12, masks); pub_n += 1
            if sum(g) != e["survivors"]:
                pub_bad.append((key, e["idx"], "count")); continue
            pth = tmp / "pubnull.txt"; write_instance(pth, 12, I[2]["pairs"], masks)
            En = energies(12, I[2]["pairs"]); E0 = min(En); excl = [En[s] - E0 for s in range(4096) if not g[s]]
            kv = ca.parse_kv(env.run(pth, "nullgap", 0.0, I[2]["tau"], E0, tag="N2_public_machinery").stdout)
            dpy = min(excl) if excl else math.inf
            if abs(float(kv["delta_nonG"]) - dpy) > 1e-12 * I[2]["Q"] and not (dpy == math.inf and float(kv["delta_nonG"]) == math.inf):
                pub_bad.append((key, e["idx"], "delta"))
    rec("N2", "Null well-formedness and acceptance accounting: %d accepted nulls (N1 degree-preserving, N2 free incidence) are structurally valid; attempted = accepted + duplicates + rejections with reasons, none exhausted; constructive survivor counts equal an independent full scan; unchanged control reproduces 2604 and the perturbed control differs; null machinery (counts, Delta_null) equals Python on the public 2x2 patch" % len(entries),
        "STRUCTURAL_AND_COUNTING", "PASS" if not (wf_bad or acc_bad or cc_bad or pub_bad) and ctl_ok else "FAIL", malformed=wf_bad[:5], accounting_failures=acc_bad, accounting=acct, crosscheck_mismatches=cc_bad,
        controls=dict(unchanged_survivors=real_cnt, perturbed_survivors=pert, perturbed_set_differs=dg_p != dg_r), public_2x2_machinery_checked=pub_n, public_mismatches=pub_bad[:5],
        prohibition="Nulls are not ranked or selected by physical-target preservation; no null preservation statistics are computed in v009.")
    # ---- N3 / feasibility : can 2 x 1000 nulls fit the declared budget?
    sy = X["synth24"]; times = []
    for k in range(5):
        p = env.run(sy["path"], "nullgap", 0.0, sy["tau"], sy["E0"], tag="null_feasibility_synthetic_nullgap", synthetic=True); kv = ca.parse_kv(p.stdout)
        times.append(dict(wall_s=float(kv["wall_s"]), maxrss_kb=int(kv["maxrss_kb"]), excluded=int(kv["n_excluded"])))
    t_gap = statistics.median(t["wall_s"] for t in times); rss = max(t["maxrss_kb"] for t in times)
    surv_stats = {k: dict(min=min(e["survivors"] for e in reg[k]), median=statistics.median(e["survivors"] for e in reg[k]), max=max(e["survivors"] for e in reg[k])) for k in reg}
    per_family = {k: gstat[k]["seconds_total"] + len(reg[k]) * t_gap for k in reg}
    budget = PROPOSED["time_limit_min"] * 60
    feasible = all(v <= budget for v in per_family.values()) and rss / 1048576 < PROPOSED["mem_limit_gib"]
    alt = {str(m): dict(seconds_per_family=m * t_gap + (gstat["N1"]["seconds_total"] / len(reg["N1"])) * m, fits=(m * t_gap + (gstat["N1"]["seconds_total"] / len(reg["N1"])) * m) <= budget) for m in (500, 1000, 2000, 5000)}
    DIAG["NULL_FEASIBILITY"] = dict(proposed_per_family=PROPOSED["n_nulls_per_family"], acceptance_cap_draws=5 * PROPOSED["n_nulls_per_family"], accounting=acct, survivor_count_distribution=surv_stats,
                                    generation_seconds_total=gen_seconds, grammar_count_seconds=gstat, nullgap_synthetic_n24_runs=times, nullgap_median_s=t_gap, peak_rss_kb=rss,
                                    estimated_seconds_per_family_for_Delta_null=per_family, budget_seconds_per_arm=budget, fits_budget=feasible, alternative_sample_sizes=alt,
                                    method="Delta_null needs ONE Gray-code scan per null (all three windows follow from it); timing measured on a SYNTHETIC 24-spin instance with the real grammar masks and non-physical couplings (non-protected fingerprint), so no real 3x3 excitation is evaluated.",
                                    cap_policy=dict(survivor_count_cap=PROPOSED["null_cap"], note="draws whose constructive count exceeds the cap are rejected with a logged reason; the cap was not binding" if all(acct[k].get("rejected:survivor-count cap hit (more than the declared cap)", 0) == 0 for k in acct) else "cap rejections occurred"))
    rec("N3", "Null feasibility gate: 2 x %d valid nulls generated deterministically within the draw cap and the primary Delta_null evaluation (one Gray-code scan per null, timed on a synthetic 24-spin instance) fits the per-arm budget" % PROPOSED["n_nulls_per_family"],
        "FEASIBILITY_TIMING", "PASS" if feasible else "BOUNDED", mandatory=False, estimated_seconds_per_family=per_family, nullgap_median_s=t_gap, fits_budget=feasible)
    sy["nullgap_median_s"] = t_gap


# ================================================================ O1, Z1
def expected_g2_order(masks, n):
    seen, order = set(), []
    for im, nm in masks:
        for i in range(n):
            if im >> i & 1 and i not in seen:
                seen.add(i); order.append(i)
    return order + [i for i in range(n) if i not in seen]


def test_O_Z(X):
    env, I, tmp = X["env"], X["inst"], X["tmp"]; bad = []; detail = {}
    for L, W in ((2, 0.0), (2, X["kT_norm"]), (3, 0.0)):
        d = I[L]; E0 = X["refs"][L]
        for mode in SOLVERS:
            a_ids, a = env.solve(d["path"], mode, W, d["tau"], E0, tag="O1_run_a"); b_ids, b = env.solve(d["path"], mode, W, d["tau"], E0, tag="O1_run_b")
            keys = [k for k in a if k not in ("wall_s", "cpu_s", "maxrss_kb") and not k.startswith("t_")]
            if any(a[k] != b[k] for k in keys) or a_ids != b_ids:
                bad.append((L, W, mode, "run-to-run difference"))
            if mode == "g2":
                exp = expected_g2_order(d["masks"], d["n"])
                if [int(x) for x in a["g2_island_order"].split(",")] != exp:
                    bad.append((L, mode, "island order differs from the specification"))
    # tie handling: all-degenerate instance -> retained set must be the first r pair indices
    n = 6; pdeg = [(i, j, 0.0) for i in range(n) for j in range(i + 1, n)]; pth = tmp / "o1deg.txt"; write_instance(pth, n, pdeg, [(0b001111, 0)])
    kv = ca.parse_kv(env.run(pth, "e2", 0.0, 1e-9, 0.0, tag="O1_ties").stdout); ordr, r, ret, BO, h = e2_model(pdeg, 0.25)
    if ordr[:r] != list(range(r)) or int(kv["e2_order_digest"]) != h:
        bad.append("tie ordering of equal magnitudes is not by pair index")
    rec("O1", "Deterministic candidate ordering: every solver repeats counters/ids exactly across runs (2x2 at two windows, 3x3 at the W=0 anchor); G2 island order equals the specified first-appearance order; E2 breaks equal |K| by pair index; B0/E2 use the documented Gray-code bit ctz(t) order",
        "DETERMINISM", "PASS" if not bad else "FAIL", mismatches=bad[:10],
        ordering_policy=dict(B0="Gray code, flipping spin ctz(t) at step t=1..2^n-1 (spin 0..n-1 = state bits), exact resync every 256 steps", G1="ascending state id 0..2^n-1", G2="islands in order of first appearance in the vertex list; value 0 before 1; vertex checked as soon as complete",
                             B1="spin index order 0..n-1; the lower-energy value is tried first", E2="Gray code as B0; retained pairs by |K| descending, ties by smaller pair index", ordering_calibration="none: no heuristic was tuned, so no calibration data were needed"))
    # ---- Z1
    zbad = []; zrows = []
    for L in (1, 2):
        d = I[L]; En = energies(d["n"], d["pairs"]); N = 1 << d["n"]; full = (1 << d["n"]) - 1
        if any(En[s] != En[s ^ full] for s in range(N)):
            zbad.append((L, "H(-s) != H(s)"))
        g = grammar_flags(d["n"], d["masks"])
        if any(g[s] != g[s ^ full] for s in range(N)):
            zbad.append((L, "grammar not complement invariant"))
    p3 = tmp / "g3ids.txt"; env.run(I[3]["path"], "gcount", 0, 0, extra=["--dump", p3], tag="Z1_grammar_ids_3x3")
    ids3 = {int(x) for x in p3.read_text().split()}; full3 = (1 << 24) - 1
    if len(ids3) != 2604 or any((s ^ full3) not in ids3 for s in ids3):
        zbad.append((3, "3x3 grammar set is not complement closed"))
    # z2 sensitivity equivalence for every solver (same opportunity for all)
    rng = random.Random(PROPOSED["master_seed"] + 51); cases = []
    for L in (1, 2):
        d = I[L]; En = energies(d["n"], d["pairs"]); Ws, _ = public_windows(En, d["tau"])
        for name, W in Ws[:1] + Ws[1:12:3]:
            cases.append((d["path"], d["tau"], min(En), W, "public%dx%d_%s" % (L, L, name)))
    for t in range(8):
        n = rng.randint(8, 12); pr, mk, _g = synth_instance(rng, n); p = tmp / ("z1syn%d.txt" % t); write_instance(p, n, pr, mk); En = energies(n, pr)
        cases.append((p, tol.REL_TAU * sum(abs(k) for _, _, k in pr), min(En), rng.choice((0.0, 0.1, 0.4)) * (max(En) - min(En)), "synthetic%d" % t))
    for pth, tau, E0, W, name in cases:
        for mode in SOLVERS:
            full_ids, _ = env.solve(pth, mode, W, tau, E0, tag="Z1_full"); z_ids, kz = env.solve(pth, mode, W, tau, E0, extra=["--z2"], tag="Z1_z2_sensitivity")
            if full_ids != z_ids:
                zbad.append((name, mode, len(full_ids), len(z_ids)))
    for mode in SOLVERS:
        d = I[3]; ids_f, kf = env.solve(d["path"], mode, 0.0, d["tau"], X["E0f"], tag="Z1_3x3_W0_full"); ids_z, kz = env.solve(d["path"], mode, 0.0, d["tau"], X["E0f"], extra=["--z2"], tag="Z1_3x3_W0_z2")
        if ids_f != ids_z:
            zbad.append(("3x3", mode, "z2 set differs"))
        zrows.append(dict(solver=mode, full_work=int(kf["states_visited"]) + int(kf["nodes"]), z2_work=int(kz["states_visited"]) + int(kz["nodes"]), full_pair_ops=int(kf["pair_ops"]), z2_pair_ops=int(kz["pair_ops"]),
                          full_wall_s=float(kf["wall_s"]), z2_wall_s=float(kz["wall_s"]), z2_expansions=int(kz["z2_expansions"])))
    rec("Z1", "Global-reversal (Z2) symmetry: H(-s) = H(s) exactly on every public state; the ice grammar is complement-invariant (public patches and all 2604 3x3 survivors); the optional --z2 sensitivity mode gives identical target sets for ALL five solvers on %d cases and the 3x3 anchor, with the expansion charged. Policy: DISABLED in the primary experiment" % len(cases),
        "EXHAUSTIVE_AND_BEHAVIOURAL", "PASS" if not zbad else "FAIL", mismatches=zbad[:10], work_at_3x3_W0=zrows,
        policy="Primary solvers run on the full space. A symmetry-quotient sensitivity analysis is permitted only if every applicable solver receives the same opportunity (all five accept --z2) and every cost, including expansion, is charged; no one-sided symmetrisation.")


# ================================================================ C1, C2 : cost ledger, timing protocol, resource feasibility
def test_C(X):
    env, I, tmp = X["env"], X["inst"], X["tmp"]; d = I[3]; E0 = X["E0f"]; tau = d["tau"]
    def runner_factory(extra=()):
        def runner(mode):
            t = time.perf_counter()
            p = env.run(d["path"], mode, 0.0, tau, None if mode.startswith("cert") else E0, extra=list(extra), tag="C2_timing_protocol" + ("_z2" if extra else ""))
            ext = time.perf_counter() - t
            if p.returncode:
                raise Blocked("timing run failed: %s %s" % (mode, p.stderr[-200:]))
            return ca.parse_kv(p.stdout), ext
        return runner
    prim, order = ca.run_protocol(runner_factory(), list(SOLVERS), PROPOSED["warmups"], PROPOSED["repeats"])
    cert, order_c = ca.run_protocol(runner_factory(), ["cert_b0", "cert_b1"], PROPOSED["warmups"], PROPOSED["repeats"])
    z2, _ = ca.run_protocol(runner_factory(["--z2"]), list(SOLVERS), PROPOSED["warmups"], PROPOSED["repeats"])
    def ledger_row(solver, rows, label):
        keys = ca.NUMERIC_KEYS + ["external_wall_s"]; med = {}
        for k in keys:
            vals = [r[k] for r in rows if k in r]
            if vals:
                med[k] = statistics.median(vals)
        for k in ("maxrss_kb",):
            med[k] = max(r[k] for r in rows)
        b = ca.charged(solver, med); dsp = ca.disp([r["wall_s"] for r in rows]); dsp_ext = ca.disp([r["external_wall_s"] for r in rows])
        return dict(arm=label, solver=solver, median=med, buckets=b, wall_dispersion=dsp, external_wall_dispersion=dsp_ext)
    ledger = {s: ledger_row(s, prim[s], "primary") for s in SOLVERS}
    ledger_cert = {s: ledger_row(s, cert[s], "E0_certification") for s in ("cert_b0", "cert_b1")}
    ledger_z2 = {s: ledger_row(s, z2[s], "SENSITIVITY_z2") for s in SOLVERS}
    cheapest_cert = min(ledger_cert.values(), key=lambda r: r["buckets"]["total_charged"])
    scen = {s: dict(precertified_reference=ledger[s]["buckets"]["total_charged"], end_to_end_with_E0_certification=ledger[s]["buckets"]["total_charged"] + cheapest_cert["buckets"]["total_charged"],
                    certification_method=cheapest_cert["solver"]) for s in SOLVERS}
    # positional balance of the deterministic interleaving
    pos = {s: [0] * len(SOLVERS) for s in SOLVERS}
    for r_, ordr in enumerate(order):
        if r_ >= PROPOSED["warmups"]:
            for p_, s in enumerate(ordr):
                pos[s][p_] += 1
    balanced = all(len(set(v)) == 1 for v in pos.values())
    # ---- C1 : completeness against the required ledger items
    required = {"wall-clock": "wall_s", "CPU time": "cpu_s", "candidate states visited": "states_visited", "constructive nodes": "nodes", "grammar checks": "grammar_checks", "pair-interaction operations": "pair_ops",
                "incremental energy updates": "field_updates", "full-energy evaluations": "full_energy_evals", "branch-and-bound node expansions / bound evaluations": "bound_evals",
                "E2 certified rejections": "cert_rejects", "E2 fallback evaluations": "e2_fallbacks", "initialisation and preprocessing": "t_preprocess_s", "peak resident memory": "maxrss_kb",
                "output serialisation": "t_serialize_s", "ground-energy certification (separate rows)": "E0_certification"}
    missing = []
    for item, key in required.items():
        if key == "E0_certification":
            if not ledger_cert:
                missing.append(item)
        elif not all(key in ledger[s]["median"] for s in SOLVERS):
            missing.append(item)
    once = all(ledger[s]["buckets"]["total_charged"] >= 0.999 * ledger[s]["median"]["wall_s"] for s in SOLVERS)      # buckets + unattributed remainder cover the whole wall time exactly once
    rec("C1", "Complete operation-cost ledger: all %d required cost items are recorded for B0, G1, G2, B1 and E2 (and, separately, for the E0 certification); each operation belongs to exactly one bucket (setup / generation / filter / energy / other); both the precertified-reference and the end-to-end scenario are reported" % len(required),
        "INSTRUMENTATION", "PASS" if not missing and once else "FAIL", missing_items=missing, required_items=required, scenario_totals=scen, bucket_mapping={s: ca.BUCKETS[s] for s in ca.BUCKETS},
        note="W=0 component measurements on the disclosed anchor only: no speedup, no G_net and no C verdict follows from them.")
    # ---- worst-case resource projection on a SYNTHETIC 24-spin instance (non-protected fingerprint)
    worst = {s: dict(wall_s=0.0, rss_kb=0, W=None, instance=None) for s in SOLVERS}; synth_rows = []
    for inm, sy in (("gauss", X["synth24"]), ("realmag", X["synth24r"])):
        for wn, W in (("1kT", X["kT_norm"]), ("2kT", 2 * X["kT_norm"]), ("0.1Q", 0.1 * sy["Q"]), ("Q", sy["Q"]), ("3Q_all_states", 3 * sy["Q"])):
            for s in SOLVERS:
                t = time.perf_counter(); p = env.run(sy["path"], s, W, sy["tau"], sy["E0"], tag="C2_resource_worst_case_synthetic", synthetic=True, extra=(["--frac", X["e2_recommended_fraction"]] if s == "e2" else [])); ext = time.perf_counter() - t
                if p.returncode:
                    raise Blocked("synthetic worst-case run failed: %s %s %s" % (s, wn, p.stderr[-200:]))
                kv = ca.parse_kv(p.stdout); w = float(kv["wall_s"]); rss = int(kv["maxrss_kb"])
                synth_rows.append(dict(instance=inm, solver=s, window=wn, W=W, wall_s=w, external_wall_s=ext, maxrss_kb=rss, targets=int(kv["target_count"])))
                if ext > worst[s]["wall_s"]:
                    worst[s] = dict(wall_s=ext, rss_kb=rss, W=wn, instance=inm)
    max_rss = max([r["maxrss_kb"] for r in synth_rows] + [max(l["median"]["maxrss_kb"] for l in ledger.values())]) / 1048576.0
    arm_seconds = {s: (PROPOSED["warmups"] + PROPOSED["repeats"]) * worst[s]["wall_s"] for s in SOLVERS}
    total_primary_cpu = 3 * sum(arm_seconds.values())
    within = max(arm_seconds.values()) <= PROPOSED["time_limit_min"] * 60 and max_rss < PROPOSED["mem_limit_gib"]
    # ---- uncertainty rule for H-C (synthetic correlated timings only)
    cov = ca.coverage_simulation(sims=500, n_boot=1000)
    DIAG["HC_UNCERTAINTY"] = dict(rule="paired per-round ratios t_B0/t_arm; 95% percentile-bootstrap interval of the median ratio (rounds resampled as blocks, 10000 resamples, seed 20261010); decision: PASS if lower end >= 1.20 AND P passed AND output completeness independently certified; FAIL if upper end < 1.20; else INCONCLUSIVE",
                                  secondary="log-scale Student-t interval of the geometric-mean ratio reported alongside", simulation=cov,
                                  simulation_note="500 simulated 15-round experiments per true ratio with a common machine factor (sd 0.15, cancels in the paired ratio), AR(1)-correlated individual noise (phi=0.3, sd 0.05).")
    cover_ok = {k: v["coverage_bootstrap"] for k, v in cov.items()}
    false_pass = cov["1.00"]["decisions_bootstrap"]["CHARGED_GAIN_PASS"] + cov["1.10"]["decisions_bootstrap"]["CHARGED_GAIN_PASS"]
    power15 = cov["1.50"]["decisions_bootstrap"]["CHARGED_GAIN_PASS"]
    status = "PASS" if (within and balanced and false_pass <= 0.05 and power15 >= 0.9) else "BOUNDED"
    rec("C2", "Timing protocol and resource feasibility: single thread, %d warm-ups + %d timed rounds, deterministic balanced interleaving (position-balanced: %s), median and dispersion; worst-case synthetic 24-spin windows keep every arm under %g min and %g GiB; the paired-ratio uncertainty rule has low false-pass and high power on simulated correlated timings" % (PROPOSED["warmups"], PROPOSED["repeats"], balanced, PROPOSED["time_limit_min"], PROPOSED["mem_limit_gib"]),
        "TIMING_AND_SIMULATION", status, worst_case_per_solver=worst, projected_arm_seconds=arm_seconds, projected_total_primary_seconds=total_primary_cpu, max_rss_gib=max_rss, within_limits=within,
        position_counts=pos, bootstrap_coverage=cover_ok, false_pass_rate_when_true_ratio_le_1_1=false_pass, power_at_true_ratio_1_5=power15,
        caveat="Bootstrap coverage of a 15-round experiment is below the nominal 95% when timings are autocorrelated; the decision-rule error rates above are what matter and are reported, not hidden. Machine and load differences between this run and the user's WSL machine are not modelled.", synthetic_rows=synth_rows)
    X["ledger"], X["ledger_cert"], X["ledger_z2"], X["scenarios"] = ledger, ledger_cert, ledger_z2, scen


# ================================================================ B1 : guard,  (B2 evaluated at the end)
def test_guard(X):
    env, I, tmp = X["env"], X["inst"], X["tmp"]; r3 = I[3]; E0 = X["E0f"]; att = []; bad = []
    for mode in SOLVERS:
        for W in (1e-300, X["kT_norm"], 2 * X["kT_norm"]):
            p = env.run(r3["path"], mode, W, r3["tau"], E0, tag="GUARD_TEST_BLOCK_EXPECTED_real3x3")
            att.append(dict(mode=mode, W=W, rc=p.returncode, stdout_empty=not p.stdout.strip()))
            if p.returncode != 3 or p.stdout.strip() or "REFUSED" not in p.stderr:
                bad.append((mode, W, p.returncode))
    for label, extra, syn in (("nullgap_real3x3_excitation_gap", [], False), ("synthetic_flag_on_protected_instance", [], True)):
        mode = "nullgap" if label.startswith("nullgap") else "b0"
        p = env.run(r3["path"], mode, 0.0 if mode == "nullgap" else X["kT_norm"], r3["tau"], E0, extra=extra, tag="GUARD_TEST_BLOCK_EXPECTED_" + label, synthetic=syn)
        att.append(dict(mode=mode, label=label, rc=p.returncode, stdout_empty=not p.stdout.strip()))
        if p.returncode != 3 or p.stdout.strip():
            bad.append((label, p.returncode))
    cmd = [str(env.pg), str(r3["path"]), "b0", repr(X["kT_norm"]), repr(r3["tau"]), "--e0", repr(E0), "--synthetic", "--audit", str(env.audit), "--tag", "GUARD_TEST_BLOCK_EXPECTED_synthetic_without_protected_list"]
    p = subprocess.run(cmd, capture_output=True, text=True); att.append(dict(label="synthetic_flag_without_protected_list", rc=p.returncode))
    if p.returncode != 3 or p.stdout.strip():
        bad.append(("synthetic without list", p.returncode))
    p = env.run(r3["path"], "b0", -1.0, r3["tau"], E0, tag="GUARD_TEST_negative_W"); att.append(dict(label="negative_W", rc=p.returncode))
    if p.returncode != 2:
        bad.append(("negative W", p.returncode))
    allowed = {}
    for label, args in (("real3x3_W0_solver", (r3["path"], "g2", 0.0, r3["tau"], E0, False)), ("real3x3_W0_certification", (r3["path"], "cert_b1", 0.0, r3["tau"], None, False)),
                        ("real3x3_grammar_only", (r3["path"], "gcount", 0.0, 0.0, None, False)), ("public2x2_W_positive", (I[2]["path"], "b0", 0.5, I[2]["tau"], X["refs"][2], False)),
                        ("synthetic24_W_positive", (X["synth24"]["path"], "b0", X["kT_norm"], X["synth24"]["tau"], X["synth24"]["E0"], True))):
        p = env.run(args[0], args[1], args[2], args[3], args[4], tag="GUARD_TEST_allowed_" + label, synthetic=args[5]); allowed[label] = p.returncode
        if p.returncode != 0:
            bad.append(("allowed", label, p.returncode))
    src = (HERE / "gate_common_v009.hpp").read_text()
    guard_src = "REFUSED: outcome-blind guard" in src and "(n > 16) && (O.W > 0 || excitation_mode)" in src and (HERE / "e2_v009.cpp").read_text().count("guard(false)") == 1
    rec("B1", "3x3 W>0 guard: every attempt on the real 3x3 instance with W>0 (five solvers, three windows), the excitation-gap (nullgap) mode, the synthetic-flag bypass (with and without the protected list) is REFUSED with exit 3 and no result on stdout; negative W is rejected; W=0 anchor runs, grammar-only runs, public W>0 and non-protected synthetic W>0 are allowed; --unblind-after-freeze is never used by v009",
        "BEHAVIOURAL", "PASS" if (not bad and guard_src) else "FAIL", attempts=att, mismatches=bad, allowed_exit_codes=allowed, guard_in_source=guard_src,
        limits="The guard is a procedural safeguard (instance fingerprint + flags), not a cryptographic barrier: a deliberately modified copy of the code or of the input would bypass it.")
    X["guard_attempts"] = len(att)


# ================================================================ H1 : decision functions
def hg_verdict(membership_equal, survivors, nominal, leakage=False, thr=PROPOSED["hg_contraction"]):
    if not membership_equal or leakage:
        return "GENERATIVE_CONTRACTION_FAIL"
    return "GENERATIVE_CONTRACTION_PASS" if 1 - survivors / nominal >= thr else "GENERATIVE_CONTRACTION_FAIL"


def hp_verdict(FN, verifier_complete, window_prospective=True):
    if not verifier_complete or not window_prospective:
        return "TARGET_PRESERVATION_INCONCLUSIVE"
    return "TARGET_PRESERVATION_PASS" if FN == 0 else "TARGET_PRESERVATION_FAIL"


def ht_verdict():
    return "NOT_TESTED / PROTOCOL_UNFROZEN"


def test_H(X):
    I = X["inst"]; cases = []
    cases.append(("H-G exact membership, 3x3 survivors 2604 of 2^24", hg_verdict(True, 2604, 1 << 24), "GENERATIVE_CONTRACTION_PASS"))
    cases.append(("H-G membership mismatch", hg_verdict(False, 2604, 1 << 24), "GENERATIVE_CONTRACTION_FAIL"))
    cases.append(("H-G contraction 98% < 99%", hg_verdict(True, 82, 4096), "GENERATIVE_CONTRACTION_FAIL"))
    cases.append(("H-G target leakage", hg_verdict(True, 2604, 1 << 24, leakage=True), "GENERATIVE_CONTRACTION_FAIL"))
    cases.append(("H-P FN=0 certified", hp_verdict(0, True), "TARGET_PRESERVATION_PASS"))
    cases.append(("H-P FN=1", hp_verdict(1, True), "TARGET_PRESERVATION_FAIL"))
    cases.append(("H-P incomplete verifier", hp_verdict(0, False), "TARGET_PRESERVATION_INCONCLUSIVE"))
    cases.append(("H-T", ht_verdict(), "NOT_TESTED / PROTOCOL_UNFROZEN"))
    t_ref = [1.0 * (1 + 0.01 * (i % 3)) for i in range(15)]; t_fast = [x / 2.0 for x in t_ref]; t_slow = [x / 1.0 for x in t_ref]
    cases.append(("H-C P not passed", ca.hc_decision(ca.hc_intervals(t_ref, t_fast), 1.2, False, True), "NOT_ELIGIBLE_COMPLETE_TASK_NOT_CERTIFIED"))
    cases.append(("H-C completeness not certified", ca.hc_decision(ca.hc_intervals(t_ref, t_fast), 1.2, True, False), "NOT_ELIGIBLE_COMPLETE_TASK_NOT_CERTIFIED"))
    cases.append(("H-C 2.0x with P and completeness", ca.hc_decision(ca.hc_intervals(t_ref, t_fast), 1.2, True, True), "CHARGED_GAIN_PASS"))
    cases.append(("H-C 1.0x", ca.hc_decision(ca.hc_intervals(t_ref, t_slow), 1.2, True, True), "CHARGED_GAIN_FAIL"))
    noisy = [1.0, 2.5, 0.8, 1.9, 1.1, 2.2, 0.9, 1.6, 1.3, 2.0, 1.0, 1.4, 1.8, 0.7, 2.4]; cases.append(("H-C noisy straddling 1.2", ca.hc_decision(ca.hc_intervals(noisy, [1.0] * 15), 1.2, True, True), "CHARGED_GAIN_INCONCLUSIVE"))
    bad = [(c, got, exp) for c, got, exp in cases if got != exp]
    # replication figures on grammar-only counts (no Hamiltonian)
    rep = {}
    for L in (1, 2, 3):
        kv = ca.parse_kv(X["env"].run(I[L]["path"], "gcount", 0, 0, tag="H1_grammar_counts").stdout); s = int(kv["survivors"]); nom = 1 << I[L]["n"]
        rep["%dx%d" % (L, L)] = dict(survivors=s, nominal=nom, contraction=1 - s / nom, hg_at_99pct=hg_verdict(True, s, nom), nodes=int(kv["nodes"]), role="regression control" if L < 3 else "primary-scale replication of the v007 count (historical evidence, not a new discovery)")
    ok_counts = (rep["1x1"]["survivors"], rep["2x2"]["survivors"], rep["3x3"]["survivors"]) == (6, 82, 2604)
    rec("H1", "Decision functions implement the axis decision table (G exact membership + >=99% contraction; P FN=0 with a complete verifier; T NOT_TESTED; C needs P and certified completeness plus the paired lower-bound rule) and reproduce the historical counts 6/16, 82/4096, 2604/2^24 from the constructive counter", "SYNTHETIC_DECISION_TABLE",
        "PASS" if (not bad and ok_counts) else "FAIL", cases=[dict(case=c, got=g, expected=e) for c, g, e in cases], mismatches=bad, replication_counts=rep)
    X["hg_rep"] = rep


# ================================================================ decision register (PROPOSED values only) and D1
def register(X):
    I = X["inst"]; kT_J, kT_n = X["kT_J"], X["kT_norm"]; sw = PROPOSED["window_multipliers"]
    gap1, gap2 = 9.529e-21, 1.041e-20           # public v008 values (J), used only for the disclosure ratios
    R = []
    def add(decision, proposed, status, rationale, support, limits, informed, token):
        R.append(dict(decision=decision, proposed=proposed, required_status=status, rationale=rationale, support=support, limitations=limits, informed_by_disclosed_results=informed, token=token))
    add("Primary patch", "3×3 free-boundary square ice (24 spins, 2^24 states)", "Confirm", "Smallest patch at which exact exhaustive verification is non-trivial yet feasible on one thread (v007); 4×4 exact verification is not shown to be feasible.",
        "v007 EXACT3_VERIFIER_FEASIBLE; F1, E2, H1", "Single geometry; no claim about larger patches.", "Yes: the 2,604/2^24 count and the exact-verification feasibility were disclosed (v007).", "3×3")
    add("Primary window", "W = k_B T_ref, T_ref = 792 K  (= %.9e J = %.6f in A units)" % (kT_J, kT_n), "Ratify", "Physically interpretable thermal scale fixed from T_ref and k_B alone; no 3×3 excited-state information was used.",
        "R1 (units), T1/T3 (boundary policy), B1/B2 (blindness)", "Exceeds the known exclusion gaps of both public patches (1×1: Δ=0.871 k_BT, ρ_G≈1.15; 2×2: Δ=0.952 k_BT, ρ_G≈1.05), so a P FAIL at 3×3 is a genuine possibility. The window must not be changed after unblinding.",
        "Partly: the public small-patch gaps were known when the window was proposed (disclosed); the 3×3 gap was not.", "k_B T_ref")
    add("Sensitivity windows", "W = 0.5 k_B T_ref (%.5e J) and W = 2 k_B T_ref (%.5e J)" % (sw["sensitivity_A"] * kT_J, sw["sensitivity_B"] * kT_J), "Ratify", "Bracket the primary window by a factor of two on a logarithmic scale; reported separately, never to rescue a failed primary.",
        "T1/T3, H1", "0.5 k_BT lies below both public gaps (would pass on 1×1/2×2), 2 k_BT lies above them; neither is independent of the primary window.", "Partly (same as primary window).", "2 k_B T")
    add("Tolerance scale", "τ = 1e-9 · Σ|K_ij|, membership E ≤ E0 + W + τ, PRESERVED ⇔ W + τ < Δ_nonG; UNRESOLVED_BOUNDARY (|d| ≤ 2^-52 Q) is treated as target", "Validate and ratify",
        "Scale known before any scan; only enlarges the target, so it can never turn an excluded target into a preserved one; separated from evaluation error (eps_direct, eps_gray) and from level grouping.",
        "T1, T2, T3, E3, F1 (v007 V4 deviation preserved)", "τ is a convention, not derived from physics; ≈1e-9 relative matches the v006/v007 grouping tolerance only in magnitude (different normalisation); v007's drift threshold was revised post hoc and must not be cited as prospective.",
        "Partly: v007 V4 drift measurements (disclosed) motivated eps_gray; the final hierarchy was tested on synthetic and public data only.", "1e-9")
    add("Null seed", "20261010 (domain-separated '<seed>|<family>|<index>')", "Ratify", "Same master seed and derivation as the frozen v006 nulls, which makes the registry reproducible and auditable.", "N1, N2", "An arbitrary constant; no sensitivity analysis over seeds.", "No.", "20261010")
    add("Null sample size", "1,000 valid nulls per family (N1 degree-preserving, N2 free incidence), draw cap 5,000 per family", "Validate and ratify", "Large enough for a stable null distribution of Δ_null and survivor counts; the primary evaluation needs one Gray-code scan per null.",
        "N2, N3 (NULL_FEASIBILITY_v009.json)", "No power analysis for any null-separation threshold was performed (that threshold remains OPEN); timing is from a synthetic 24-spin instance.", "No.", "1,000")
    recf = X.get("e2_recommended_fraction", PROPOSED["e2_frac"]); rtxt = "%g%%" % (recf * 100)
    add("E2 retained interactions", "strongest 25%% of |K_ij| (spec nominal; ties by pair index); v009 RECOMMENDS %s on measured synthetic cost (exactness is independent of the fraction); certified remainder bound B_O" % rtxt, "Validate and ratify",
        "Fixed before any 3×3 target was examined; exactness does not depend on the fraction, only cost does. The recommended fraction minimises worst-case pair operations over two synthetic 24-spin instances (Gaussian and sign-randomised real magnitudes) at 1 and 2 k_BT.",
        "E1, E2, E3, E4; fraction sweep on synthetic n=24 (E2_VALIDATION_v009.json)",
        "Sweep on synthetic couplings only; on flat-coupling instances 25%% degenerates towards a full fallback scan and is slower than B0; cost on the real geometry may differ; E2 may be slower than B0 by design. Recommended fraction %s is not frozen." % rtxt,
        "No (geometry-only retained-weight fraction is a property of the frozen couplings).", "25%")
    add("Z₂ symmetry", "Disabled in the primary experiment; optional equal-opportunity sensitivity (--z2 for every solver)", "Ratify", "Keeps comparability with the frozen v005–v008 counts and avoids one-sided symmetrisation.", "Z1", "Halving of every search is forgone in the primary comparison.", "No.", "Z₂")
    add("Primary B0 baseline", "Optimised single-thread Gray-code exhaustive scan with periodic exact resynchronisation", "Confirm", "Competitive exact baseline for the complete-target task, not a slow direct evaluator.", "E2, E4, C1, C2", "A hand-optimised or vectorised B0 could be faster; only single-thread scalar code was built.", "Yes (v007/v008 timings of the Gray-code scan were disclosed).", "Gray-code")
    add("B1", "Exact branch-and-bound sensitivity comparator with the admissible bound LB = E_fixed − Σ|f_j| − Σ|K_jk| (decision form at the common threshold)", "Confirm", "Strong Hamiltonian-aware conventional comparator; reported honestly even if it beats G2.", "R1, E3, T1, T3, v008 S3 (bound admissibility, frozen)", "At the W=0 anchor B1 is faster than G2 (v008); its advantage at W>0 is unknown.", "Yes (v008 W=0 timings).", "branch-and-bound")
    add("H-G contraction", "exact constructive = independent membership, and ≥ 99% contraction of the nominal space", "Ratify", "Separates structural contraction from computational work (nodes and work are reported separately).", "H1, N2",
        "Non-discriminating: the 3×3 count 2,604/2^24 (99.985%) is already known, so the contraction condition cannot fail unless membership disagrees; the substantive test is exact membership and absence of target leakage.", "Yes: explicitly (v007 count).", "99%")
    add("H-P preservation", "FN = 0 at the prospectively declared window, exact verifier complete", "Confirm", "Direct restatement of S_T(W) ⊆ S_G, equivalent to W + τ < Δ_nonG.", "T1, T2, T3, H1", "Logically equivalent to a statement about the gap: a pass is not independent evidence of transfer.", "No.", "FN = 0")
    add("H-T", "NOT_TESTED / PROTOCOL_UNFROZEN", "Confirm", "The beyond-gap criterion is logically unsatisfiable for inclusive energy windows; a future target family needs its own protocol.", "H1; v008 amended drafts", "No transfer claim is possible from this study.", "No.", "NOT_TESTED")
    add("H-C performance", "≥ 1.20× charged median speedup against optimised B0; paired per-round ratios, 95% bootstrap lower bound ≥ 1.20; only if P passes and completeness is certified", "Ratify", "A modest margin above timing noise; conditional on a certified complete output.", "C2 (uncertainty simulation), H1, E4",
        "The disclosed W=0 timings (B0 ≈ 0.33 s, G2 ≈ 0.3 ms) suggest the margin will not bind against B0; B1 and E2 are sensitivity arms and may beat G2; W>0 costs are unknown.", "Yes (v008 W=0 timings).", "1.20")
    add("Timed repeats", "15 timed rounds after 3 warm-ups, deterministic balanced interleaving, single thread", "Validate and ratify", "Enough rounds for a paired median with a stable block bootstrap on this machine class; position-balanced across solvers.", "C2",
        "Simulated coverage of the nominal 95% interval is only about 0.78-0.87 with 15 rounds (more rounds or a wider margin would be needed for true 95%); load on the user's machine may differ.", "No.", "15")
    add("Resource limits", "30 min per arm, 2 GiB resident memory", "Validate and ratify", "Worst-case synthetic 24-spin windows and the null scans fit with large margin.", "C2, N3", "Based on this container's CPU; a slower machine scales times proportionally.", "No.", "2 GiB")
    add("E0", "Frozen v007 physical anchor E0 = %.17g (A units) = %.16e J, passed unchanged to every solver" % (X["E0f"], X["anchor"]["E0_J"]), "Confirm", "A single certified global minimum prevents a grammar-restricted estimate from silently shifting the target.", "R1, R2",
        "G1/G2/E2 cannot self-certify E0; certification is external and hash-checked.", "Yes (disclosed anchor).", "E0")
    add("3×3 W>0 unblinding", "Forbidden until a separate freeze and authorisation", "Confirm", "Protects the primary outcome from adaptive decisions.", "B1, B2", "Procedural guard, not cryptographic.", "No.", "unblinding")
    return R


def register_md(R, X):
    L = ["# DECISION_REGISTER_v009 — proposed settings awaiting scientific ratification\n",
         "**Nothing in this register is frozen.** Every entry is a recommendation with its evidence; a proposed value does not become frozen because v009 recommends it. "
         "Primary experiment: NOT AUTHORIZED. Date: 2026-10-10.\n", "| # | Decision | Proposed setting | Required status | Supporting tests / sources |", "|---|---|---|---|---|"]
    for i, r in enumerate(R, 1):
        L.append("| %d | %s | %s | %s | %s |" % (i, r["decision"], r["proposed"].replace("|", "/"), r["required_status"], r["support"]))
    L.append("\n## Detail per decision\n")
    for i, r in enumerate(R, 1):
        L += ["### %d. %s\n" % (i, r["decision"]), "- **Proposed:** %s" % r["proposed"], "- **Required status:** %s — *AWAITING RATIFICATION*" % r["required_status"], "- **Rationale:** %s" % r["rationale"],
              "- **Supporting test / source:** %s" % r["support"], "- **Unresolved limitations:** %s" % r["limitations"], "- **Informed by previously disclosed physical results:** %s\n" % r["informed_by_disclosed_results"]]
    L += ["## Axis decision table (implemented and tested as code, test H1)\n", "| Axis | PASS | FAIL | Other |", "|---|---|---|---|",
          "| G | exact constructive = independent membership, no target leakage, contraction ≥ 99% | any mismatch / leakage / contraction below threshold | INCONCLUSIVE if unverifiable |",
          "| P | FN = 0 with complete exact verifier at the prospective window | FN ≥ 1 | INCONCLUSIVE if verifier incomplete or window not prospective |",
          "| T | — | — | NOT_TESTED / PROTOCOL_UNFROZEN |",
          "| C | P passed, output completeness certified, paired lower 95% bound of the B0/G2 median ratio ≥ 1.20 | upper bound < 1.20 | INCONCLUSIVE if the interval straddles; NOT_ELIGIBLE if P/completeness not established |\n",
          "## Not decided by v009 (remain OPEN for the user)\n",
          "- Whether to keep W = k_B T_ref as the single primary window or declare a different rule (the register only recommends).",
          "- The null-separation success criterion and any numerical threshold for 'distinctive grammar' versus nulls (no power analysis was done).",
          "- Whether a margin above 1.20× is more appropriate given the disclosed W=0 timings, and whether B1 or E2 results should carry any pre-declared interpretation.",
          "- The final tolerance constant and whether UNRESOLVED_BOUNDARY should be reported as its own outcome class in addition to FAIL.",
          "- The dated freeze record, SHA-256 manifest of the final documents, and the separate authorisation to lift the W>0 guard.\n"]
    return "\n".join(L) + "\n"


def test_D(X):
    R = register(X); X["register"] = R
    spec, pre, am = (DRAFTS / "SCR_III_B_SPEC_v001.md"), (DRAFTS / "SCR_III_B_PREREG_v001.md"), (DRAFTS / "DRAFT_AMENDMENTS_v009.md")
    probs = []
    if not (spec.exists() and pre.exists() and am.exists()):
        raise Blocked("v009 drafts missing in " + str(DRAFTS))
    st, pt, at = spec.read_text(), pre.read_text(), am.read_text()
    for name, t in (("SPEC", st), ("PREREG", pt)):
        if "UNFROZEN" not in t or re.search(r"Status:\*\*\s*\**\s*FROZEN", t) or "RATIFIED" in t.replace("NOT RATIFIED", "").replace("awaiting ratification", ""):
            probs.append(name + ": status not clearly unfrozen")
        if "Δ_nonice" in t or "nonice" in t.replace("gap_nonice", ""):
            probs.append(name + ": inconsistent Δ_nonice wording")
        for must in ("Physical Sufficiency", "NOT_TESTED", "low-energy-outcome", "separately implemented", "1e−10"):
            if must not in t:
                probs.append("%s: missing '%s'" % (name, must))
    for tkn in ("0.871", "0.952", "1.15", "1.05", "Gray-code", "AWAITING RATIFICATION"):
        if tkn not in pt:
            probs.append("PREREG: missing '%s'" % tkn)
    rf = "%g%%" % (X["e2_recommended_fraction"] * 100)
    for name, t in (("PREREG", pt), ("AMENDMENTS", at)):
        if rf not in t:
            probs.append("%s: recommended E2 fraction %s not recorded" % (name, rf))
    for r in R:
        if r["token"] not in pt:
            probs.append("PREREG: decision '%s' (token %s) not recorded" % (r["decision"], r["token"]))
        if r["token"] not in at:
            probs.append("AMENDMENTS: decision '%s' not recorded" % r["decision"])
    if at.count("OPEN") < 3 or "does not freeze" not in at.lower() and "not frozen" not in at.lower():
        probs.append("AMENDMENTS: open items / non-freeze statement missing")
    md = register_md(R, X)
    for r in R:
        if r["decision"] not in md or not all(r[k] for k in ("rationale", "support", "limitations", "informed_by_disclosed_results")):
            probs.append("register entry incomplete: " + r["decision"])
    # proposed numeric values in the register equal those used by the code under test
    expect = {"20261010": PROPOSED["master_seed"], "1,000": PROPOSED["n_nulls_per_family"], "25%": int(PROPOSED["e2_frac"] * 100), "99%": int(PROPOSED["hg_contraction"] * 100), "1.20": PROPOSED["hc_speedup"], "15": PROPOSED["repeats"], "2 GiB": PROPOSED["mem_limit_gib"], "1e-9": PROPOSED["rel_tau"]}
    for tkn, val in expect.items():
        if tkn not in md:
            probs.append("register lacks value token " + tkn)
    X["register_md"] = md
    rec("D1", "Draft decisions and open items are faithfully recorded: the shipped SPEC/PREREG copies stay UNFROZEN, contain every one of the %d register decisions with their PROPOSED values marked AWAITING RATIFICATION, the thermal-window disclosure numbers, the Δ_nonG wording, the NOT_TESTED transfer status, the v007 blindness/verifier/V4 disclosures, and an explicit list of open items; the register has rationale, support, limitation and informed-by-disclosure fields for every entry" % len(R),
        "DOCUMENT_CONSISTENCY", "PASS" if not probs else "FAIL", problems=probs, entries=len(R), sha256=dict(spec=sha(spec), prereg=sha(pre), amendments=sha(am)))


# ================================================================ B2 : blindness audit
PERMIT = re.compile(r"withheld|not computed|NOT computed|prohibit|forbid|blocked|BLOCKED|must not|never|only after|guard|remain|unknown|not examined|not disclosed|no 3", re.I)
FORBID = re.compile(r"delta_nonG|Δ_nonG|Delta_nonG|rho_G|ρ_G|excitation level|excited[- ]state level|first non-grammar", re.I)
M33 = re.compile(r"3\s*[x×]\s*3|real3", re.I)


def scan_text(name, text):
    hits = []
    for ln in text.splitlines():
        if M33.search(ln) and FORBID.search(ln) and re.search(r"\d", ln) and not PERMIT.search(ln):
            hits.append((name, ln.strip()[:200]))
    return hits


def audit_log_entries(X):
    return [json.loads(l) for l in X["env"].audit.read_text().splitlines() if l.strip()]


def test_B2(X, extra_texts):
    I = X["inst"]; log = audit_log_entries(X); real_fp = I[3]["fp"]
    ALLOWED_3X3 = {"b0", "g1", "g2", "b1", "e2", "cert_b0", "cert_b1", "gcount", "gscan"}
    real = [e for e in log if e["instance_fp"] == real_fp]; viol = []
    for e in real:
        if e["status"] == "ALLOWED" and not (e["W"] == 0 and e["mode"] in ALLOWED_3X3):
            viol.append(e)
    wpos_allowed = [e for e in log if e["status"] == "ALLOWED" and e["n"] > 16 and e["W"] > 0]
    wpos_bad = [e for e in wpos_allowed if not e["synthetic_flag"] or e["instance_fp"] == real_fp]
    unblind = [e for e in log if e["unblind_flag"]]
    blocked = [e for e in log if e["status"] == "BLOCKED"]
    rejected = [e for e in log if e["status"] == "E0_REJECTED"]
    hits = []
    for name, text in extra_texts.items():
        hits += scan_text(name, text)
    modes = sorted({e["mode"] for e in log})
    summary_3x3 = {}
    for e in real:
        k = "%s|W=%g|%s" % (e["mode"], e["W"], e["status"]); summary_3x3[k] = summary_3x3.get(k, 0) + 1
    DIAG["BLINDNESS_AUDIT"] = dict(log_records=len(log), accepted_command_line_modes=modes, real3x3_fingerprint=real_fp, real3x3_invocation_summary=summary_3x3,
                                   blocked_attempts=[dict(mode=e["mode"], W=e["W"], tag=e["tag"], reason=e["reason"]) for e in blocked], blocked_count=len(blocked), e0_rejections=len(rejected),
                                   allowed_w_positive_runs_on_n_gt_16=dict(count=len(wpos_allowed), all_synthetic_nonprotected=not wpos_bad), unblind_flag_uses=len(unblind), real3x3_policy_violations=viol[:5],
                                   output_scan_hits=hits[:10], scanned_documents=list(extra_texts),
                                   statement="A blocked attempted unblinding is not a primary result but is recorded. Every real-3x3 execution that was ALLOWED is a W=0 anchor run or a grammar-only run; excitation-gap (nullgap) and W>0 requests on the real 3x3 instance were only issued to prove that they are refused.",
                                   disclosures=["Operation counters of W=0 3x3 runs (e.g. E2 fallback counts, B1 node counts) are published as costs; they are derived from the disclosed W=0 anchor only and identify no excited level or exclusion gap, but they are coarse functions of the near-ground spectrum.",
                                                "v007 TESTS_v007.json V4.relative_to_scale together with the drift value still permits inferring an approximate upper-spectrum scale (~0.126 in A units): the study is low-energy-outcome blinded, NOT spectrum-blind.",
                                                "The guard is a procedural safeguard, not a cryptographic one."],
                                   delta_nonG_for_real_3x3="NOT computed", W_positive_3x3_target_search="NOT performed")
    ok = not viol and not wpos_bad and not unblind and not hits and len(blocked) >= X["guard_attempts"] - 1
    rec("B2", "No primary-window outcome disclosure: the invocation audit shows only W=0 anchor and grammar-only executions of the real 3x3 instance (all W>0 / excitation-gap requests BLOCKED), every W>0 run on n>16 used a non-protected synthetic instance, no unblinding flag was used, and no produced document states a 3x3 exclusion gap, rho_G or excited level",
        "AUDIT", "PASS" if ok else "FAIL", log_records=len(log), real3x3_runs=len(real), blocked_attempts=len(blocked), policy_violations=len(viol), unsafe_wpos_runs=len(wpos_bad), unblind_uses=len(unblind), text_hits=hits[:5])


# ================================================================ outputs
ORDER = ["F1", "P0", "R1", "R2", "E1", "E2", "E3", "E4", "T1", "T2", "T3", "W1", "N1", "N2", "N3", "O1", "Z1", "C1", "C2", "B1", "B2", "H1", "D1"]
CODE_FILES = ["validate_v009.py", "test_v009.py", "prereg_gate_v009.cpp", "gate_common_v009.hpp", "e2_v009.cpp", "seeds_v009.py", "tolerance_v009.py", "cost_audit_v009.py", "README_v009.md"]


def f(x, nd=4):
    return "%.*g" % (nd, x)


def verdict_of(X):
    tests = sorted(TESTS, key=lambda t: ORDER.index(t["id"]) if t["id"] in ORDER else 99)
    mand_fail = [t["id"] for t in tests if t["mandatory"] and t["status"] == "FAIL"]
    partial = [t["id"] for t in tests if t["status"] not in ("PASS", "FAIL")]
    unsupported = [r["decision"] for r in X["register"] if r["required_status"].startswith("Validate") and any(
        next((t["status"] for t in tests if t["id"] == tid), "MISSING") != "PASS" for tid in re.findall(r"\b([A-Z]\d)\b", r["support"]) if tid in ORDER)]
    if mand_fail:
        v = "PREREG_CLOSURE_GATE_FAIL"
    elif partial or unsupported:
        v = "PREREG_CLOSURE_GATE_PARTIAL"
    else:
        v = "PREREG_CLOSURE_GATE_PASS"
    return v, mand_fail, partial, unsupported, tests


def csv_ledger(X, path):
    cols = ["arm", "solver", "wall_s_median", "wall_rel_mad", "external_wall_s_median", "cpu_s_median", "C_setup", "C_generation", "C_filter", "C_energy", "C_other", "C_unattributed", "C_total_charged",
            "end_to_end_total_with_E0_cert", "peak_rss_kb"] + [k for k in ca.NUMERIC_KEYS if k not in ("wall_s", "cpu_s", "maxrss_kb")]
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(cols)
        for led in (X["ledger"], X["ledger_cert"], X["ledger_z2"]):
            for s, d in led.items():
                m, b = d["median"], d["buckets"]; e2e = X["scenarios"][s]["end_to_end_with_E0_certification"] if s in X["scenarios"] and d["arm"] == "primary" else ""
                w.writerow([d["arm"], s, repr(m["wall_s"]), repr(d["wall_dispersion"]["rel_mad"]), repr(d["external_wall_dispersion"]["median"]), repr(m.get("cpu_s", "")), repr(b["setup"]), repr(b["generation"]), repr(b["filter"]), repr(b["energy"]),
                            repr(b["other"]), repr(b["unattributed"]), repr(b["total_charged"]), repr(e2e) if e2e != "" else "", int(m["maxrss_kb"])] + [repr(m[k]) if k in m else "" for k in cols[15:]])


def report_md(X, verdict, mand_fail, partial, unsupported, tests):
    I = X["inst"]; L = ["# REPORT_v009 — Preregistration Closure Gate (outcome-blind)\n", "**Verdict:** `%s`\n" % verdict,
         "This is a **technical-readiness** verdict. It does not freeze `SCR_III_B_SPEC_v001.md` or `SCR_III_B_PREREG_v001.md`, ratifies none of the proposed values, authorises no primary run and implies nothing about H-G, H-P, H-T or H-C primary success. "
         "Authorization remains `SCR-III-B / V008_LOCALLY_REPRODUCED / V009_SPECIFIED / PRIMARY_NOT_AUTHORIZED`.\n"]
    if verdict.endswith("PARTIAL"):
        L.append("**Why PARTIAL:** non-PASS tests %s; register entries whose supporting tests are not all PASS: %s.\n" % (partial or "none", unsupported or "none"))
    if verdict.endswith("FAIL"):
        L.append("**Mandatory failures:** %s\n" % mand_fail)
    L += ["## Test table\n", "| ID | Test | Status |\n|---|---|---|"] + ["| %s | %s | **%s** |" % (t["id"], t["title"][:230], t["status"]) for t in tests]
    e0 = DIAG["E0_AUDIT"]; tolh = DIAG["TOLERANCE"]["hierarchy_example_3x3_Q"]
    L += ["\n## Common ground-energy reference (R1/R2)\n", "- Frozen v007 anchor E0 = `%s` (A units) = %.16e J; hash of REPORT_v007.json matches the frozen record: **%s**; unit scaling E0·A(792 K) = %.16e J." % (e0["E0_norm_repr"], e0["E0_J"], e0["hash_matches_frozen_record"], e0["E0_norm_times_A_J"]),
          "- Independent re-certification (Gray-code minimisation and branch-and-bound minimisation) reproduces it within τ (bitwise: %s) with the two disclosed complementary ground states." % e0["certification_equal_to_frozen_bitwise"],
          "- Limit: G1/G2/E2 cannot certify E0 themselves; mismatches are caught by the exit-4 checks where possible and always by the harness bitwise reconciliation.\n",
          "## Tolerance hierarchy (proposed, not frozen)\n", "For the 3×3 coupling set Q = Σ|K| = %s: eps_input = %s < eps_direct = %s < eps_gray = %s < τ = %s." % tuple(f(tolh[k], 4) for k in ("Q", "eps_input", "eps_direct", "eps_gray", "tau")),
          "Membership: E ≤ E0 + W + τ; PRESERVED ⇔ W + τ < Δ_nonG; |d| ≤ eps_input is UNRESOLVED_BOUNDARY and counted as target (conservative).\n"]
    sw = DIAG["E2_VALIDATION"]["synthetic_n24_fraction_sweep"]; ev = DIAG["E2_VALIDATION"]
    L += ["## E2 comparator\n", "Exact for every tested retained fraction (public patches at all windows, mixed-sign / zero / tie-heavy instances, 150 random synthetic cases, 3×3 anchor). Synthetic n=24 fraction sweep (cost only; B0 wall at 1 k_BT shown for reference):\n",
          "| instance | retained fraction | wall @1 k_BT (s) | pair ops @1 k_BT | fallbacks @1 k_BT | wall @2 k_BT (s) |", "|---|---|---|---|---|---|"]
    for inm, rows_ in sw.items():
        for k, v in rows_.items():
            if k == "b0":
                L.append("| %s | B0 | %s | | | %s |" % (inm, f(v["1kT"]["wall_s"]), f(v["2kT"]["wall_s"])))
            else:
                L.append("| %s | %s | %s | %s | %s | %s |" % (inm, k, f(v["1kT"]["wall_s"]), v["1kT"]["pair_ops"], v["1kT"]["fallbacks"], f(v["2kT"]["wall_s"])))
    L += ["", ev["recommendation"], ""]
    L += ["## Thermal windows vs public gaps (W1)\n", "| patch | window | Δ/k_BT | (W+τ)/Δ | status |", "|---|---|---|---|---|"] + ["| %s | %s | %.4f | %.3f | %s |" % (r["patch"], r["window"], r["delta_over_kT"], r["rho"], r["status"]) for r in X["W1_rows"]] + [""]
    nf = DIAG["NULL_FEASIBILITY"]
    L += ["\n## Seeds and nulls\n", "Master seed %d; accounting per family: %s" % (PROPOSED["master_seed"], json.dumps(nf["accounting"])),
          "Primary Δ_null evaluation needs one Gray-code scan per null: median %s s on a synthetic 24-spin instance → estimated %s s per family (budget %d s). 2×1000 nulls fit: **%s**.\n" % (f(nf["nullgap_median_s"]), {k: round(v) for k, v in nf["estimated_seconds_per_family_for_Delta_null"].items()}, nf["budget_seconds_per_arm"], nf["fits_budget"])]
    L += ["## Cost ledger (3×3, W=0 anchor only; 1 thread; %d warm-ups + %d rounds; median)\n" % (PROPOSED["warmups"], PROPOSED["repeats"]), "| Solver | wall (s) | rel. MAD | charged total (s) | + E0 certification (s) | pair ops | nodes / states | peak RSS (MB) |", "|---|---|---|---|---|---|---|---|"]
    for s, d in X["ledger"].items():
        m = d["median"]; L.append("| %s | %s | %.1f%% | %s | %s | %s | %s | %.1f |" % (s.upper(), f(m["wall_s"]), 100 * (d["wall_dispersion"]["rel_mad"] or 0), f(d["buckets"]["total_charged"]), f(X["scenarios"][s]["end_to_end_with_E0_certification"]), int(m["pair_ops"]), int(m.get("nodes", 0)) or int(m["states_visited"]), m["maxrss_kb"] / 1024))
    L.append("\nOne-time E0 certification: " + "; ".join("%s %s s (charged)" % (k, f(v["buckets"]["total_charged"])) for k, v in X["ledger_cert"].items()) + ". **These are acceptance-only component measurements: no speedup, no G_net and no C verdict follows.**\n")
    hc = DIAG["HC_UNCERTAINTY"]["simulation"]
    L += ["## H-C uncertainty rule (simulation on synthetic correlated timings)\n", "| true ratio | bootstrap coverage | P(decision PASS) |\n|---|---|---|"] + ["| %s | %.2f | %.2f |" % (k, v["coverage_bootstrap"], v["decisions_bootstrap"]["CHARGED_GAIN_PASS"]) for k, v in hc.items()]
    cv = [v["coverage_bootstrap"] for v in hc.values()]
    L.append("\n**Honest limitation:** the nominal 95%% interval has simulated coverage of only %.2f-%.2f with 15 rounds (moving-block bootstrap, block 3); a log-scale t interval is similar. The rule is therefore anti-conservative as an interval; what the proposal relies on is the simulated decision error: false-pass rate for true ratio <= 1.1 and power at 1.5 (table above and C2).\n" % (min(cv), max(cv)))
    L += ["## Things you should know before ratifying\n",
          "1. **H-G ≥ 99% cannot discriminate**: 2,604/2^24 (99.985%) is already known, so the condition only fails if constructive membership disagrees with the independent count.",
          "2. **H-C ≥ 1.20× against B0 is unlikely to bind**: the disclosed W=0 timings differ by about three orders of magnitude; B1 (and possibly E2) are the informative sensitivity arms. B1 beat G2 at W=0 in v008.",
          "3. **The primary window k_BT exceeds the known exclusion gaps of 1×1 (0.871 k_BT) and 2×2 (0.952 k_BT)**; a P FAIL at 3×3 is a genuine possibility and must be reported, not repaired.",
          "4. The guard and audit are procedural. The v007 upper-spectrum leak means the study is low-energy-outcome blinded, not spectrum-blind. W=0 operation counters are published.",
          "5. The tolerance τ = 1e-9·Q is a convention validated for conservatism, not derived from physics; the v007 drift threshold revision (1e-12 → 1e-10) was post hoc and is not a precedent.\n",
          "## Readiness\n", "Technical readiness to freeze **without outcome-dependent modification**: " + ("the implementation, numerical and blindness prerequisites tested here are satisfied; the remaining steps are your ratification of the register, assembly of the final documents with source hashes, a separate freeze record and a separate authorization." if verdict.endswith("PASS") else "NOT yet — see the non-PASS items above."), ""]
    return "\n".join(L) + "\n"


def write_outputs(X, started):
    OUT.mkdir(parents=True, exist_ok=True)
    verdict, mand_fail, partial, unsupported, tests = verdict_of(X)
    rep = dict(version="v009", started_utc=started, finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), platform=platform.platform(), python=sys.version.split()[0], numpy=np.__version__,
               compiler=X["compiler"], verdict=verdict, mandatory_failures=mand_fail, non_pass=partial, unsupported_register_entries=unsupported, tests={t["id"]: t["status"] for t in tests},
               proposed_constants=PROPOSED, authorization="SCR-III-B / V008_LOCALLY_REPRODUCED / V009_SPECIFIED / PRIMARY_NOT_AUTHORIZED",
               statement="Technical-readiness verdict only; nothing is frozen, ratified or authorised; no 3x3 W>0 outcome and no 3x3 exclusion gap was computed.")
    md_pre = report_md(X, verdict, mand_fail, partial, unsupported, tests)
    texts = {"REPORT_v009.md": md_pre, "DECISION_REGISTER_v009.md": X["register_md"], "DIAG": json.dumps(clean(DIAG), indent=1, default=str), "TESTS": json.dumps(clean(TESTS), indent=1, default=str)}
    test_B2(X, texts)
    verdict, mand_fail, partial, unsupported, tests = verdict_of(X)
    rep.update(verdict=verdict, mandatory_failures=mand_fail, non_pass=partial, unsupported_register_entries=unsupported, tests={t["id"]: t["status"] for t in tests})
    md = report_md(X, verdict, mand_fail, partial, unsupported, tests)
    (OUT / "REPORT_v009.md").write_text(md); (OUT / "REPORT_v009.json").write_text(json.dumps(clean(rep), indent=1))
    (OUT / "TESTS_v009.json").write_text(json.dumps(clean(tests), indent=1, default=str))
    (OUT / "E2_VALIDATION_v009.json").write_text(json.dumps(clean(dict(DIAG["E2_VALIDATION"], tests={t["id"]: dict(status=t["status"], title=t["title"], detail=t["detail"]) for t in tests if t["id"] in ("E1", "E2", "E3", "E4")})), indent=1, default=str))
    (OUT / "E0_AUDIT_v009.json").write_text(json.dumps(clean(dict(DIAG["E0_AUDIT"], tests={t["id"]: dict(status=t["status"], detail=t["detail"]) for t in tests if t["id"] in ("R1", "R2")})), indent=1, default=str))
    (OUT / "TOLERANCE_v009.json").write_text(json.dumps(clean(dict(DIAG["TOLERANCE"], tests={t["id"]: dict(status=t["status"], detail=t["detail"]) for t in tests if t["id"] in ("T1", "T2", "T3")})), indent=1, default=str))
    reg = X["null_registry"]
    (OUT / "SEED_REGISTRY_v009.json").write_text(json.dumps(clean(dict(
        master_seed=PROPOSED["master_seed"], status="PROPOSED -- not frozen", derivation="label = '<master>|<family>|<idx>'; rng = random.Random(label); seed_sha256 = SHA-256(label); identical to frozen v006",
        families=sd.FAMILIES, real_3x3_instance_fingerprint_fnv1a64=X["inst"][3]["fp"], per_family_size=PROPOSED["n_nulls_per_family"], draw_cap_per_family=5 * PROPOSED["n_nulls_per_family"],
        accounting=reg["accounting"], registry_sha256=reg["digest"], entries=reg["entries"])), indent=0))
    (OUT / "NULL_FEASIBILITY_v009.json").write_text(json.dumps(clean(DIAG["NULL_FEASIBILITY"]), indent=1, default=str))
    csv_ledger(X, OUT / "COST_LEDGER_v009.csv")
    (OUT / "COST_LEDGER_v009.json").write_text(json.dumps(clean(dict(primary=X["ledger"], e0_certification=X["ledger_cert"], z2_sensitivity=X["ledger_z2"], scenarios=X["scenarios"], hc_uncertainty=DIAG["HC_UNCERTAINTY"],
                                                              note="W=0 anchor component measurements only; no speedup claim")), indent=1, default=str))
    log = audit_log_entries(X); gzp = OUT / "INVOCATION_LOG_v009.jsonl.gz"
    with gzip.GzipFile(filename="", mode="wb", fileobj=open(gzp, "wb"), mtime=0) as gz:
        gz.write(("\n".join(json.dumps(e, sort_keys=True) for e in log) + "\n").encode())
    agg = {}
    for e in log:
        k = "%s|%s|%s" % (e["mode"], e["status"], "real3x3" if e["instance_fp"] == X["inst"][3]["fp"] else ("synthetic" if e["synthetic_flag"] else "public_or_other")); agg[k] = agg.get(k, 0) + 1
    (OUT / "BLINDNESS_AUDIT_v009.json").write_text(json.dumps(clean(dict(DIAG["BLINDNESS_AUDIT"], aggregate_by_mode_status_instance=agg, blocked_records=[e for e in log if e["status"] == "BLOCKED"],
                                                                         invocation_log_file="INVOCATION_LOG_v009.jsonl.gz", invocation_log_records=len(log), invocation_log_sha256=sha(gzp),
                                                                         accepted_cli_modes_from_source=sorted(set(re.findall(r'mode == "(\w+)"', (HERE / "prereg_gate_v009.cpp").read_text())) | {"e2"}))), indent=1, default=str))
    (OUT / "DECISION_REGISTER_v009.md").write_text(X["register_md"])
    mf = dict(version="v009", verdict=verdict, compiler=X["compiler"], code={}, drafts={}, outputs={})
    for nme in CODE_FILES:
        p = HERE / nme; mf["code"][nme] = sha(p) if p.exists() else None
    for nme in ("SCR_III_B_SPEC_v001.md", "SCR_III_B_PREREG_v001.md", "DRAFT_AMENDMENTS_v009.md"):
        mf["drafts"][nme] = sha(DRAFTS / nme)
    for nme in ("REPORT_v009.md", "REPORT_v009.json", "E2_VALIDATION_v009.json", "E0_AUDIT_v009.json", "TOLERANCE_v009.json", "SEED_REGISTRY_v009.json", "NULL_FEASIBILITY_v009.json", "COST_LEDGER_v009.csv",
                "COST_LEDGER_v009.json", "BLINDNESS_AUDIT_v009.json", "INVOCATION_LOG_v009.jsonl.gz", "DECISION_REGISTER_v009.md", "TESTS_v009.json"):
        mf["outputs"][nme] = sha(OUT / nme)
    mf["note"] = "Output files contain timings; their hashes are per-run records. MANIFEST_v009.json itself is not hashed."
    (OUT / "MANIFEST_v009.json").write_text(json.dumps(mf, indent=1))
    return verdict, mand_fail, tests


def blocked(rep, why):
    OUT.mkdir(parents=True, exist_ok=True)
    rep.update(verdict="PREREG_CLOSURE_GATE_BLOCKED", reason=why, tests={})
    (OUT / "REPORT_v009.json").write_text(json.dumps(clean(rep), indent=1))
    (OUT / "REPORT_v009.md").write_text("# REPORT_v009\n\n**Verdict:** `PREREG_CLOSURE_GATE_BLOCKED`\n\n%s\n" % why)
    print("BLOCKED:", why)
    return 2


def main():
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    rep = dict(version="v009", started_utc=started, platform=platform.platform(), python=sys.version.split()[0])
    t0 = time.time()
    try:
        X = setup()
        steps = [test_P0_F1, test_R, test_E, test_T, test_W, test_N, test_O_Z, test_C, test_guard, test_H, test_D]
        for st in steps:
            ts = time.time(); st(X); print("  %-12s done in %.1fs" % (st.__name__, time.time() - ts), flush=True)
        verdict, mand_fail, tests = write_outputs(X, started)
    except Blocked as exc:
        return blocked(rep, str(exc))
    finally:
        pass
    print(json.dumps(dict(verdict=verdict, mandatory_failures=mand_fail, tests={t["id"]: t["status"] for t in tests}, seconds=round(time.time() - t0, 1)), indent=1))
    return 1 if verdict.endswith("FAIL") else 0


if __name__ == "__main__":
    sys.exit(main())
