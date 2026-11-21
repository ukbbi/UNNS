#!/usr/bin/env python3
"""MUG-I v007 verification: eigenmode-resolved induced geometry of the periodic Maxwell system.

System: -E'' = w^2 eps(z) E on the torus R/2piZ, eps = 1 + 2 delta cos(q z)  (scalar Hill problem: k || z, E transverse).
Fourier index m; Bloch class kappa = m mod q; blocks decouple.  Eigenvectors are eps-weighted (B-) orthonormal.
Exact state = eigenvector.  Label g = dominant |m|.  Content d(s) = gcd of the Fourier support of s = gcd(kappa, q).
Induction rule E (eigenstate-resolved, fixed medium): a step N acts on a field x by
   (i) keeping only components in Bloch classes whose support content is divisible by N   [whole-field admissibility, P_N]
  (ii) dilating the surviving Fourier indices m -> r_N m (r_N = (N+1)^2/N)                [D_N, exact isometry of l2]
Needs numpy, scipy.
"""
import json, hashlib, math, random, itertools
from math import gcd
import numpy as np
from scipy.linalg import eigh

random.seed(7)
results = {}
def rec(name, ok, **kw):
    results[name] = dict(ok=bool(ok), **kw)
    print(("PASS " if ok else "FAIL ") + name, {k: v for k, v in kw.items() if not isinstance(v, (list, dict))})

DELTA = 0.1

def build(q, delta=DELTA, M=480):
    blocks = {}
    for kap in range(q):
        ms = np.array([m for m in range(-M, M + 1) if m % q == kap])
        n = len(ms)
        A = np.diag((ms.astype(float)) ** 2)
        B = np.eye(n)
        for i in range(n - 1): B[i, i + 1] = B[i + 1, i] = delta
        w2, V = eigh(A, B)
        blocks[kap] = dict(ms=ms, w2=w2, V=V, B=B)
    return blocks

def labelled_states(q, blocks, Gmax):
    st = []
    for kap, b in blocks.items():
        ms = b['ms']
        for n in range(len(ms)):
            v = b['V'][:, n]
            wt = {}
            for m, c in zip(ms, v): wt[abs(int(m))] = wt.get(abs(int(m)), 0.0) + c * c
            g = max(wt, key=wt.get)
            if g <= Gmax and g >= 1:
                st.append(dict(kappa=kap, n=n, g=g, w2=b['w2'][n], dom=wt[g] / sum(wt.values()), v=v, ms=ms,
                               parity=None))
    return st

def sparse(st, tol=1e-14):
    return {int(m): float(c) for m, c in zip(st['ms'], st['v']) if abs(c) > tol}
def parity_of(x):
    """parity of the field: E(-z) = +/- E(z)  <=> c_{-m} = +/- c_m (compare after sign alignment)."""
    s = 0.0; a = 0.0
    for m, c in x.items():
        if -m in x:
            s += abs(c + x[-m]); a += abs(c - x[-m])
    return +1 if s > a else -1

# ---------------------------------------------------------------- Y1: exact states, labels, bijection
Q = 4; GMAX = 24
blk = build(Q); sts = labelled_states(Q, blk, GMAX)
by_g = {}
for s in sts: by_g.setdefault(s['g'], []).append(s)
ok = all(len(by_g.get(g, [])) == 2 for g in range(1, GMAX + 1))
mindom = min(s['dom'] for s in sts)
rec("Y1_two_exact_states_per_Fourier_label_g", ok, labels_checked=GMAX, min_dominant_weight=round(mindom, 4),
    note="eigenstate <-> (|m|, parity) bijection by dominant |m|; exact states are mixed (dominant weight < 1)")


# Y1b: validity window of the Fourier label: dominant weight collapses when phase-modulation index beta = delta*g/q ~ 1 (WKB regime)
win = {}
for d_ in (0.04, 0.06, 0.1, 0.2):
    bl_ = build(4, d_, M=480); ss_ = labelled_states(4, bl_, 120)
    byg = {}
    for s_ in ss_: byg.setdefault(s_['g'], []).append(s_)
    gstar = None
    for g_ in range(1, 121):
        v_ = byg.get(g_, [])
        if len(v_) != 2 or min(t['dom'] for t in v_) < 0.5:
            gstar = g_; break
    win[d_] = dict(first_failure_g=gstar, beta_at_failure=None if gstar is None else round(d_ * gstar / 4, 3))
rec("Y1b_label_validity_window_beta_about_1", all(w['first_failure_g'] is not None and 0.9 < w['beta_at_failure'] < 1.4 for w in win.values()),
    windows=win, note="WKB: field ~ exp(i w delta/q sin qz) so the dominant harmonic is J_0(beta); label fails near beta~1, g ~ q/delta")

# ---------------------------------------------------------------- Y2: parity degeneracy law
a = Q // 2
off_ok = True; on_ok = True; rows = []
for g in range(1, GMAX + 1):
    w = sorted(s['w2'] for s in by_g[g]); rel = abs(w[1] - w[0]) / w[0]
    if g % a:
        off_ok &= rel < 1e-9
    elif g <= 14:
        on_ok &= rel > 1e-12
    if g % a == 0 and g <= 12: rows.append((g, 2 * g // Q, float(rel)))
rec("Y2_even_odd_splitting_iff_g_in_(q/2)Z", off_ok and on_ok, delta=DELTA, q=Q,
    off_resonance="degenerate to <1e-9 (float eigensolver level) (P maps Bloch class k to -k)", on_resonance_gap_vs_order_j=rows,
    note="on-resonance check limited to g<=14 (j<=7) by double precision (gap ~ delta^j)")

# parities of the two states at a resonant label
par = {g: sorted(parity_of(sparse(s)) for s in by_g[g]) for g in (2, 4, 6, 8)}
rec("Y2b_resonant_pair_has_both_parities", all(v == [-1, 1] for v in par.values()), parities=par)

# ---------------------------------------------------------------- Y3: whole-field admissibility restricts the step vocabulary
def content_support(s, thr=1e-12, jmax=2):
    ms = s['ms']; v = s['v']
    idx0 = int(np.argmax(np.abs(v)))
    ok = True
    for t in range(-jmax, jmax + 1):
        j = idx0 + t
        if 0 <= j < len(v) and ms[j] != 0: ok &= abs(v[j]) > thr     # m=0 coefficient vanishes for odd states and does not affect the gcd
    return ok
rec("Y3a_exact_states_have_full_Bloch_support", all(content_support(s) for s in sts if s['g'] <= 20), note="harmonics g+-q, g+-2q nonzero (>1e-12), so content(state)=gcd(kappa,q); general nonvanishing is leading-order perturbative, not proved")
cnt = {}
for q in (4, 6, 12):
    lab = 0; ex = 0; Ns = set()
    for g in range(1, 3000):
        for N in range(1, g + 1):
            if g % N == 0:
                lab += 1
                if N <= q and q % N == 0 and gcd(g, q) % N == 0: ex += 1; Ns.add(N)
    cnt[q] = dict(label_edges=lab, exact_state_edges=ex, removed_fraction=round(1 - ex / lab, 4), step_alphabet=sorted(Ns))
okalpha = all(cnt[q]['step_alphabet'] == [d for d in range(1, q + 1) if q % d == 0] for q in cnt)
rec("Y3b_exact_state_admissibility_is_N_divides_gcd(g,q)", okalpha, counts=cnt,
    note="steps restricted to divisors of the period q; fraction of label edges removed shown")

# ---------------------------------------------------------------- Y4: Bloch class splitting law
def dilate(x, N):
    return {(m * (N + 1) ** 2) // N: c for m, c in x.items()} if all(m % N == 0 for m in x) else None
ok = True; n = 0; mainw = {}
for q in (4, 6, 12):
    bl = build(q) if q != Q else blk
    ss = labelled_states(q, bl, 24)
    for s in ss:
        x = sparse(s); d = gcd(s['kappa'], q)
        for N in range(1, q + 1):
            if q % N or d % N: continue
            y = dilate(x, N)
            ok &= y is not None
            cls = {}
            for m, c in y.items(): cls[m % q] = cls.get(m % q, 0.0) + c * c
            cls = {k: v for k, v in cls.items() if v > 1e-18}
            kap = s['kappa']
            pred = {((N + 1) ** 2 * (kap // N) + i * (q // N)) % q for i in range(N)}
            ok &= set(cls) <= pred and len(cls) >= 1
            n += 1
            tot = sum(cls.values())
            if N >= 2: mainw.setdefault((q, N), []).append(max(cls.values()) / tot)
rec("Y4_image_lands_in_predicted_N_Bloch_classes", ok, states_checked=n,
    main_class_weight_min={str(k): round(min(v), 4) for k, v in mainw.items()},
    note="image support is r_N(kappa+qZ): N classes kappa' = (N+1)^2 kappa/N + i q/N; most weight in one class")

# ---------------------------------------------------------------- Y5: induced relation on exact states = weighted relation
def expand(y, bl, q, Gmax=200):
    """expand a Fourier vector y in exact eigenstates of all blocks; return list of (weight, label, parity, kappa)."""
    out = []; norm = 0.0
    for kap in range(q):
        b = bl[kap]; ms = b['ms']; pos = {int(m): i for i, m in enumerate(ms)}
        vec = np.zeros(len(ms)); lost = 0.0
        for m, c in y.items():
            if m % q == kap:
                if m in pos: vec[pos[m]] = c
                else: lost += c * c
        if not vec.any(): continue
        alpha = b['V'].T @ (b['B'] @ vec)
        for n_, al in enumerate(alpha):
            out.append((al * al, kap, n_))
        norm += float(vec @ b['B'] @ vec)
    return out, norm
q = Q; bl = build(Q, 0.03); sts5 = labelled_states(Q, bl, 16)
fid_rows = []; min_fid = 1.0; n = 0
lab_all = {(s['kappa'], s['n']): s['g'] for s in labelled_states(q, bl, 10 ** 6)}
sts = sts5
par_all = {}
for s in sts:
    if s['g'] <= 16: par_all[(s['kappa'], s['n'])] = parity_of(sparse(s))
for s in sts:
    if s['g'] > 16: continue
    x = sparse(s); d = gcd(s['kappa'], q)
    for N in range(1, q + 1):
        if q % N or d % N: continue
        y = dilate(x, N)
        comps, nrm = expand(y, bl, q)
        gt = s['g'] * (N + 1) ** 2 // N
        w_target = sum(w for w, kap, n_ in comps if lab_all.get((kap, n_)) == gt) / nrm
        n += 1; min_fid = min(min_fid, w_target)
        fid_rows.append((s['g'], N, round(w_target, 4)))
rec("Y5_T_N_on_exact_states_is_a_weighted_relation_with_leakage", min_fid > 0.5 and min_fid < 1.0, edges=n, delta=0.03,
    min_weight_on_label_target=round(min_fid, 4), sample=fid_rows[:12],
    note="weight on the two exact states labelled r_N g; remainder leaks to other eigenstates")

# ---------------------------------------------------------------- Y6: history dependence by blocking
def step(x, N, q):
    """rule E on a Fourier vector x: keep classes whose content is divisible by N, then dilate."""
    keep = {m: c for m, c in x.items() if q % N == 0 and gcd(m % q, q) % N == 0}
    if not keep: return {}
    return {(m * (N + 1) ** 2) // N: c for m, c in keep.items()}
def run(x0, Ns, q):
    x = dict(x0); surv = 1.0; n0 = sum(c * c for c in x.values())
    for N in Ns:
        before = sum(c * c for c in x.values())
        x = step(x, N, q)
        after = sum(c * c for c in x.values())
        surv *= (after / before) if before > 0 else 0.0
        if not x: return {}, 0.0
    return x, surv
def label_histories(g0, g1, maxlen=8):
    out = []
    def dfs(g, ns):
        if g == g1: out.append(tuple(ns)); return
        if len(ns) >= maxlen: return
        for N in range(1, g + 1):
            if g % N == 0:
                g2 = g * (N + 1) ** 2 // N
                if g2 <= g1: dfs(g2, ns + [N])
    dfs(g0, []); return out
summary = {}; examples = []
for q in (6, 12):
    bl = build(q, M=300)
    ss = [s for s in labelled_states(q, bl, 40) if parity_of(sparse(s)) == 1]
    for s in ss:
        g0 = s['g']
        if g0 > 24: continue
        x0 = sparse(s)
        seen = {}
        # endpoints reachable by >= 2 label histories
        ends = {}
        def dfs2(g, ns):
            for N in range(1, g + 1):
                if g % N == 0 and len(ns) < 4:
                    g2 = g * (N + 1) ** 2 // N
                    if g2 <= 3000:
                        ends.setdefault(g2, []).append(tuple(ns + [N])); dfs2(g2, ns + [N])
        dfs2(g0, [])
        for g1, hs in ends.items():
            if len(hs) < 2: continue
            res = [(h,) + run(x0, h, q)[::-1] for h in hs]       # (h, surv, x)
            surv = [r[1] for r in res]
            summary.setdefault(q, dict(groups=0, E_all_blocked=0, E_survival_differs=0, E_all_equal_full=0, mixed=0))
            S = summary[q]; S['groups'] += 1
            if max(surv) < 1e-12: S['E_all_blocked'] += 1
            elif max(surv) - min(surv) > 1e-9:
                S['E_survival_differs'] += 1
                if len(examples) < 6: examples.append(dict(q=q, g0=g0, g1=g1, histories=[list(h) for h in hs], survivals=[round(v, 6) for v in surv]))
            elif min(surv) > 1 - 1e-12: S['E_all_equal_full'] += 1
            else: S['mixed'] += 1
rec("Y6_equal_endpoint_histories_differ_by_blocking", any(v['E_survival_differs'] > 0 for v in summary.values()),
    summary=summary, examples=examples)

# no-blocking composition law: when every step passes completely, the final field is D_{prod r} x (path independent)
ok = True; n = 0
for q in (4, 6, 12):
    bl = build(q, M=200)
    for s in labelled_states(q, bl, 12):
        if parity_of(sparse(s)) != 1: continue
        x0 = sparse(s)
        for h1 in itertools.product([N for N in range(1, q + 1) if q % N == 0], repeat=2):
            for h2 in (h1, h1[::-1]):
                pass
            xa, sa = run(x0, h1, q); xb, sb = run(x0, h1[::-1], q)
            if sa > 1 - 1e-12 and sb > 1 - 1e-12:
                n += 1
                ok &= set(xa) == set(xb) and all(abs(xa[m] - xb[m]) < 1e-12 for m in xa)
rec("Y7_unblocked_histories_are_path_independent_exactly", ok, pairs_checked=n,
    note="when no component is blocked, F = D_{prod r} x for every ordering (multiplier group is abelian)")

blob = json.dumps(results, sort_keys=True, default=str, indent=1)
open('verification_results_v007.json', 'w').write(blob)
print("sha256", hashlib.sha256(blob.encode()).hexdigest())
print("ALL PASS" if all(v['ok'] for v in results.values()) else "SOME FAIL")
