#!/usr/bin/env python3
"""SCR-III GAP-4x4 witness-and-certification audit v001.
Does NOT search the 4x4 space. Inputs: the preserved real_4x4.txt and GAP4_FIRST_RUN.jsonl. Evaluates the two reported witness states only,
validates the solver on the public 1x1-3x3 patches (frozen references), and tests the pruning bound. Usage: gap4_audit_v001.py ROOT SOLVER_FRESH PUB_DIR OUT_JSON"""
import sys, json, hashlib, math, random, pathlib, subprocess
from fractions import Fraction
import numpy as np
ROOT = pathlib.Path(sys.argv[1]); SV = sys.argv[2]; PUB = pathlib.Path(sys.argv[3]); OUT = sys.argv[4]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "scr_iii_b/reference_check"))
import physical_energy_v005 as P
G = ROOT / "scr_iii_b/GAP4_v010"
R = {}
sha = lambda p: hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
R["hashes"] = {str(p.relative_to(ROOT)): sha(p) for p in [G/"output/real_4x4.txt", G/"output/GAP4_FIRST_RUN.jsonl", G/"solver_v010.cpp", G/"solver_v010", G/"make_instance_v010.py", G/"physical_energy_v005.py", ROOT/"scr_iii_b/reference_check/physical_energy_v005.py"]}
R["v005_copy_identical_to_frozen"] = R["hashes"]["scr_iii_b/GAP4_v010/physical_energy_v005.py"] == R["hashes"]["scr_iii_b/reference_check/physical_energy_v005.py"]

def parse_inst(path):
    t = pathlib.Path(path).read_text().split()
    n, nv = int(t[0]), int(t[1]); m = n*(n-1)//2
    K = [[0.0]*n for _ in range(n)]; c = 2
    for i in range(n):
        for j in range(i+1, n):
            K[i][j] = K[j][i] = float(t[c]); c += 1
    vs = [(int(t[c+2*v]), int(t[c+2*v+1])) for v in range(nv)]
    assert c + 2*nv == len(t)
    return n, nv, K, vs

# ---------- 1. instance fidelity (geometry only; generator CLI not used) ----------
n, nv, K, vs = parse_inst(G/"output/real_4x4.txt")
isl = P.source_geometry(4); vp = P.vertex_positions(4); inc = P.incident_islands(isl, vp)
pairs = P.K_pairs(isl)
R["instance"] = dict(n=n, nv=nv, K_all_equal_geometry=all(K[i][j] == k for i, j, k in pairs), pair_count=len(pairs),
    masks_equal_geometry=sorted(m for m, _ in vs) == sorted(sum(1 << i for i in x) for x in inc))
scale = sum(abs(k) for _, _, k in pairs)
R["instance"]["scale_sum_abs_K"] = scale

# ---------- 2. witnesses ----------
runs = [json.loads(l) for l in open(G/"output/GAP4_FIRST_RUN.jsonl")]
gr, ng = runs[0], runs[1]
Pk = pairs
def en_fsum(s): return math.fsum(k*s[i]*s[j] for i, j, k in Pk)
def en_exact(s): return sum(Fraction(k)*s[i]*s[j] for i, j, k in Pk)
A792 = P.A_joule(792.0); kT = P.KB*792.0
def charge_J(s): return math.fsum(s[i]*s[j]*P.pair_energy_charge_model_J(isl[i], isl[j], 792.0) for i, j, _ in Pk)
def charges(s): return P.vertex_charges_geometric(s, isl, vp)
def mask_count_bad(s):
    bad = []
    for v, (m, p) in enumerate(vs):
        c = sum(1 for i in range(n) if (m >> i) & 1 and ((s[i] > 0) == bool((p >> i) & 1)))
        if c != 2: bad.append(v)
    return bad
W = {}
for name, r in (("ground", gr), ("non_grammar", ng)):
    s = P.decode(r["witness_id"], n); ex = en_exact(s)
    W[name] = dict(witness_id=r["witness_id"], completed=r["completed"], nodes=r["nodes"],
        reported_upper=r["upper"], reported_lower=r["lower"], E_fsum=en_fsum(s), E_exact_rational_of_stored_doubles=float(ex),
        abs_diff_reported_vs_exact=float(abs(Fraction(r["upper"]) - ex)), tau_1e9_scale=1e-9*scale,
        within_tau=float(abs(Fraction(r["upper"]) - ex)) <= 1e-9*scale,
        E_charge_model_J=charge_J(s), E_normA_times_A_J=en_exact(s).__float__()*A792,
        charge_vs_K_rel_diff=abs(charge_J(s) - float(ex)*A792)/abs(float(ex)*A792),
        ice_ok_geometric=P.ice_ok_geometric(s, isl, vp), vertex_charges=charges(s),
        violating_vertices_geometric=[i for i, q in enumerate(charges(s)) if q != 0],
        violating_vertices_instance_masks=mask_count_bad(s),
        z2_partner_id=(2**n-1) ^ r["witness_id"], z2_energy_equal=en_fsum([-x for x in s]) == en_fsum(s) or abs(en_fsum([-x for x in s]) - en_fsum(s)) < 1e-15)
    W[name]["_state"] = s
R["witnesses"] = {k: {a: b for a, b in v.items() if a != "_state"} for k, v in W.items()}
E0 = float(en_exact(W["ground"]["_state"])); EN = float(en_exact(W["non_grammar"]["_state"]))
d_A = EN - E0; delta = d_A*A792/kT
R["gap"] = dict(E0_A=E0, E_nonG_A=EN, delta_A=d_A, delta4=delta, delta4_from_reported=(ng["upper"]-gr["upper"])*A792/kT,
    I_R2=[0.790439676056526, 1.0333534753990623], inside_R2=0.790439676056526 <= delta <= 1.0333534753990623, below_1=delta < 1.0,
    margin_to_R2_lower=delta-0.790439676056526, margin_to_R2_upper=1.0333534753990623-delta, margin_to_1=1.0-delta,
    rounding_uncertainty_delta=(2*1e-11*scale)*A792/kT)

# ---------- 3. local optimality (consistency only, NOT a proof) ----------
def Kmat(): return np.array(K)
KM = Kmat()
def en_np(s): s = np.asarray(s, float); return 0.5*float(s @ KM @ s)
s0 = np.array(W["ground"]["_state"], float); e0 = en_np(s0)
lo1 = min(en_np(np.where(np.arange(n) == i, -s0, s0)) for i in range(n))
lo2 = min(en_np(np.where((np.arange(n) == i) | (np.arange(n) == j), -s0, s0)) for i in range(n) for j in range(i+1, n))
s1 = np.array(W["non_grammar"]["_state"], float); e1 = en_np(s1)
def viol(s): return bool(mask_count_bad(list(map(int, s))))
nb = []
for i in range(n):
    t = s1.copy(); t[i] *= -1; nb.append(t)
    for j in range(i+1, n):
        t = s1.copy(); t[i] *= -1; t[j] *= -1; nb.append(t)
nbv = [en_np(t) for t in nb if viol(t)]
R["local_optimality_consistency_only"] = dict(ground_min_1flip=lo1, ground_min_2flip=lo2, ground_E=e0, ground_is_1_2flip_min=(lo1 >= e0-1e-15 and lo2 >= e0-1e-15),
    nongrammar_min_violating_neighbour=min(nbv), nongrammar_E=e1, nongrammar_is_local_min_among_violating=(min(nbv) >= e1-1e-15))

# ---------- 4. solver validation on 1x1-3x3 vs frozen references and independent exhaustive scan ----------
REF = {1: 0.009438264173023073, 2: 0.010315265098625195, 3: 0.010212546058288613}
E0_3_J = -9.271994751803727e-20
val = {}
for L in (1, 2, 3):
    f = PUB/("pub%d.txt" % L)
    out = [json.loads(x) for x in subprocess.check_output([SV, str(f), "60"], text=True).splitlines()]
    nn, nvv, KK, vss = parse_inst(f)
    # independent exhaustive scan with geometric grammar (via instance masks AND v005 geometric rule)
    il = P.source_geometry(L); vpl = P.vertex_positions(L); prs = P.K_pairs(il)
    Km = np.zeros((nn, nn))
    for i, j, k in prs: Km[i, j] = Km[j, i] = k
    best = np.inf; bestv = np.inf; chunk = 1 << min(nn, 20)
    pw = (1 << np.arange(nn, dtype=np.int64))
    for base in range(0, 1 << nn, chunk):
        ids = np.arange(base, min(base+chunk, 1 << nn), dtype=np.int64)
        S = (((ids[:, None] >> np.arange(nn)) & 1)*2-1).astype(np.float64)
        e = 0.5*np.einsum('ij,jk,ik->i', S, Km, S)
        ok = np.ones(len(ids), bool)
        for m, p in vss:
            idx = [i for i in range(nn) if (m >> i) & 1]
            cnt = sum(((S[:, i] > 0) == bool((p >> i) & 1)).astype(int) for i in idx)
            ok &= (cnt == 2)
        best = min(best, e.min()); bestv = min(bestv, e[~ok].min()) if (~ok).any() else bestv
    # cross-check the grammar masks against the geometric rule on random states
    rnd = random.Random(7); agree = True
    for _ in range(300):
        s = [rnd.choice((-1, 1)) for _ in range(nn)]
        agree &= (P.ice_ok_geometric(s, il, vpl) == (not any(sum(1 for i in range(nn) if (m >> i) & 1 and ((s[i] > 0) == bool((p >> i) & 1))) != 2 for m, p in vss)))
    val[L] = dict(solver=out, exhaustive_E0=best, exhaustive_Enong=bestv, solver_E0=out[0]["upper"], solver_Enong=out[1]["upper"],
        E0_match=abs(best-out[0]["upper"]) < 1e-14, Enong_match=abs(bestv-out[1]["upper"]) < 1e-14,
        delta_solver=out[1]["upper"]-out[0]["upper"], delta_frozen_ref=REF[L], delta_diff=abs((out[1]["upper"]-out[0]["upper"])-REF[L]),
        masks_vs_geometric_rule_agree=bool(agree), completed=all(o["completed"] for o in out))
val[3]["E0_J_vs_frozen_primary"] = out[0]["upper"]*A792 if False else val[3]["solver_E0"]*A792
val[3]["E0_J_frozen"] = E0_3_J
R["solver_validation_public"] = val

# ---------- 5. python port of the solver: fidelity, bound admissibility, rounding ----------
GUARD = lambda sc: 1e-11*max(1.0, sc)
def make_port(K, vs, n):
    sc = sum(abs(K[i][j]) for i in range(n) for j in range(i+1, n))
    def bound(spin, d, acc):
        l = acc
        for j in range(d, n):
            field = 0.0
            for i in range(d): field += K[i][j]*spin[i]
            l -= abs(field)
            for h in range(j+1, n): l -= abs(K[j][h])
        return l - GUARD(sc)
    def possible(spin, d):
        for m, p in vs:
            cnt = left = 0
            for i in range(n):
                if (m >> i) & 1:
                    if i < d: cnt += int((spin[i] > 0) == bool((p >> i) & 1))
                    else: left += 1
            if cnt > 2 or cnt+left < 2: return True
            if left > 0: return True
        return False
    def violates(spin):
        for m, p in vs:
            c = sum(int((spin[i] > 0) == bool((p >> i) & 1)) for i in range(n) if (m >> i) & 1)
            if c != 2: return True
        return False
    def run(want):
        spin = [-1]*n; st = dict(best=math.inf, bid=0, nodes=0)
        def dfs(d, acc, bits):
            st["nodes"] += 1
            if bound(spin, d, acc) >= st["best"]: return
            if want and not possible(spin, d): return
            if d == n:
                if (not want or violates(spin)) and acc < st["best"]: st["best"] = acc; st["bid"] = bits
                return
            field = 0.0
            for i in range(d): field += K[i][d]*spin[i]
            first = -1 if field >= 0 else 1
            for t in range(2):
                s = first if t == 0 else -first; spin[d] = s
                dfs(d+1, acc+s*field, bits | ((1 << d) if s > 0 else 0))
        dfs(0, 0.0, 0); return st
    return sc, bound, possible, run
port = {}
for L in (1, 2, 3):
    nn, nvv, KK, vss = parse_inst(PUB/("pub%d.txt" % L))
    sc, bound, possible, run = make_port(KK, vss, nn)
    a = run(False); b = run(True); o = val[L]["solver"]
    port[L] = dict(nodes_port=[a["nodes"], b["nodes"]], nodes_cpp=[o[0]["nodes"], o[1]["nodes"]], witness_port=[a["bid"], b["bid"]], witness_cpp=[o[0]["witness_id"], o[1]["witness_id"]],
        upper_port=[a["best"], b["best"]], upper_cpp=[o[0]["upper"], o[1]["upper"]],
        identical=(a["nodes"] == o[0]["nodes"] and b["nodes"] == o[1]["nodes"] and a["bid"] == o[0]["witness_id"] and b["bid"] == o[1]["witness_id"]
                   and a["best"] == o[0]["upper"] and b["best"] == o[1]["upper"]))
R["port_fidelity_vs_cpp_binary_fresh"] = port
# admissibility on 3x3: exact minimum over ALL completions of random prefixes
nn, nvv, KK, vss = parse_inst(PUB/"pub3.txt"); sc3, bound3, possible3, _ = make_port(KK, vss, nn)
K3 = np.array(KK); rng = random.Random(20261010); slacks = []; viol_ok = True; viol_tests = 0
for _ in range(300):
    d = rng.randint(6, 18); pre = [rng.choice((-1, 1)) for _ in range(d)] + [-1]*(nn-d)
    acc = math.fsum(KK[i][j]*pre[i]*pre[j] for i in range(d) for j in range(i+1, d))
    b = bound3(pre, d, acc)
    ids = np.arange(1 << (nn-d), dtype=np.int64); T = ((ids[:, None] >> np.arange(nn-d)) & 1)*2-1
    S = np.hstack([np.tile(np.array(pre[:d], float), (len(ids), 1)), T.astype(float)])
    e = 0.5*np.einsum('ij,jk,ik->i', S, K3, S)
    slacks.append(float(e.min()-b))
for _ in range(300):
    d = rng.randint(16, 24); pre = [rng.choice((-1, 1)) for _ in range(d)] + [-1]*(nn-d)
    if not possible3(pre, d):
        viol_tests += 1
        ids = np.arange(1 << (nn-d), dtype=np.int64); T = ((ids[:, None] >> np.arange(nn-d)) & 1)*2-1
        for row in T:
            full = pre[:d] + [int(x) for x in row]
            if mask_count_bad(full) if False else any(sum(1 for i in range(nn) if (m >> i) & 1 and ((full[i] > 0) == bool((p >> i) & 1))) != 2 for m, p in vss): viol_ok = False
R["bound_admissibility_3x3_exact"] = dict(prefixes=len(slacks), min_slack_true_min_minus_bound=min(slacks), all_bound_le_true_completion_min=all(s >= 0 for s in slacks),
    possible_violation_false_cases_tested=viol_tests, possible_violation_prune_sound=viol_ok)
# 4x4: witnesses are never pruned along their own path; and float bound vs exact-rational bound
sc4, bound4, possible4, _ = make_port(K, vs, n)
def path_ok(name, best):
    s = W[name]["_state"]; spin = list(s); res = []
    for d in range(n+1):
        acc = math.fsum(K[i][j]*spin[i]*spin[j] for i in range(d) for j in range(i+1, d))
        res.append(bound4(spin, d, acc) < best)
        if name == "non_grammar": res.append(possible4(spin, d))
    return all(res)
R["witness_never_pruned_along_own_path_4x4"] = dict(ground=path_ok("ground", gr["upper"]+1e-300), non_grammar=path_ok("non_grammar", ng["upper"]+1e-300))
def bound_exact(spin, d):
    l = Fraction(0)
    l += sum(Fraction(K[i][j])*spin[i]*spin[j] for i in range(d) for j in range(i+1, d))
    for j in range(d, n):
        l -= abs(sum(Fraction(K[i][j])*spin[i] for i in range(d)))
        l -= sum(abs(Fraction(K[j][h])) for h in range(j+1, n))
    return l
errs = []
for _ in range(60):
    d = rng.randint(0, n); pre = [rng.choice((-1, 1)) for _ in range(d)] + [-1]*(n-d)
    acc = 0.0
    for i in range(d):          # accumulate as the solver does along a path
        field = 0.0
        for q in range(i): field += K[q][i]*pre[q]
        acc += pre[i]*field
    errs.append(float(abs(Fraction(bound4(pre, d, acc)+GUARD(sc4)) - bound_exact(pre, d))))
eps = 2.0**-53; m_ops = n*n*2
R["rounding"] = dict(guard=GUARD(sc4), guard_over_scale=GUARD(sc4)/sc4, empirical_max_abs_error_of_float_bound=max(errs), empirical_error_over_scale=max(errs)/sc4,
    gamma_m_model=dict(m=m_ops, gamma=m_ops*eps/(1-m_ops*eps), worst_abs_error_over_scale=m_ops*eps/(1-m_ops*eps)),
    two_error_terms_needed=2*m_ops*eps/(1-m_ops*eps), guard_covers_two_error_terms=GUARD(sc4)/sc4 > 2*m_ops*eps/(1-m_ops*eps),
    margin_factor=(GUARD(sc4)/sc4)/(2*m_ops*eps/(1-m_ops*eps)))
json.dump(R, open(OUT, "w"), indent=1, default=str)
print(json.dumps({k: R[k] for k in ("gap", "rounding", "witness_never_pruned_along_own_path_4x4", "bound_admissibility_3x3_exact", "local_optimality_consistency_only")}, indent=1, default=str))
