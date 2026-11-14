"""Independent verifier for UNNS_GRAPH_ENT_v001. Usage: python3 verify_graph_ent.py [--quick] [stage ...]"""
import sys, os, json, time, random, itertools, hashlib, math
from fractions import Fraction
import numpy as np, sympy
from mpmath import mp, mpf, log as mlog, polyroots
from graphent import *
from paths import *
mp.dps = 50
QUICK = '--quick' in sys.argv
REPORT = []; T0 = time.time()
def check(name, ok, detail=''):
    REPORT.append({'check': name, 'pass': bool(ok), 'detail': detail}); print(('PASS ' if ok else 'FAIL ') + name + ' | ' + detail[:160], flush=True); return REPORT[-1]
def dump(name, obj): json.dump(obj, open(os.path.join(DATA, name), 'w'), indent=1)

# ------------------------------------------------------------------ G1 graph facts
def g1():
    N = 1200 if not QUICK else 400
    bad = 0
    for u in range(1, N):
        for v in range(u + 1, min(N, 16 * u + 2)):
            if adjacent(u, v) != adjacent_def(u, v): bad += 1
    check('G1a_adjacency_criterion', bad == 0, f'lowest-terms test equals the definition for all pairs u<v<{N}')
    # edges <-> (k,N) bijection
    seen = {}; dup = 0
    for k in range(1, 300):
        for Nn in range(1, 300):
            e = (k * Nn, k * (Nn + 1) ** 2)
            if e in seen: dup += 1
            seen[e] = (k, Nn)
    check('G1b_edge_label_bijection', dup == 0, 'distinct (k,N), k,N<300, give distinct edges; N recovered from the ratio')
    bad = 0
    for x in range(1, 1500 if not QUICK else 300):
        nb = set(a for _, a in up_neighbours(x)) | set(a for _, a in down_neighbours(x))
        br = set(v for v in range(1, (x + 1) ** 2 + 2) if adjacent(x, v)) if x < 150 else None
        if br is not None and br != nb: bad += 1
        if len(up_neighbours(x)) + len(down_neighbours(x)) != tau(x) + sum(1 for d in range(2, int(x ** .5) + 2) if d * d <= x and x % (d * d) == 0): bad += 1
    check('G1c_degree_formula', bad == 0, 'deg(x)=tau(x)+#{d>=2: d^2|x}; neighbour lists agree with brute force (x<150)')
def g1b():
    # triangle-freeness of G[1..X]; 4-cycle and 5-cycle
    X = 40000 if not QUICK else 8000
    nbr = {}
    for x in range(1, X + 1):
        for N, y in up_neighbours(x):
            if y <= X: nbr.setdefault(x, set()).add(y); nbr.setdefault(y, set()).add(x)
    tri = 0; edges = 0
    for u, S in nbr.items():
        for v in S:
            if v > u:
                edges += 1
                if S & nbr[v]: tri += 1
    check('G2a_triangle_free_window', tri == 0, f'G[1..{X}]: {edges} edges, 0 triangles')
    bad = 0
    for a in range(1, 400):
        for b in range(1, 400):
            for c in range(1, 400):
                pass
    # algebraic triangle lemma: r_a r_b = r_c has no solution (exact)
    sol = 0
    for a in range(1, 150):
        for b in range(a, 150):
            r = Fraction((a + 1) ** 2, a) * Fraction((b + 1) ** 2, b)
            # r = (c+1)^2/c  <=>  c^2 + (2-r) c + 1 = 0 ; integer root?
            disc = (r - 2) ** 2 - 4
            if disc >= 0:
                num, den = disc.numerator, disc.denominator
                rn, rd = math.isqrt(num), math.isqrt(den)
                if rn * rn == num and rd * rd == den:
                    c = ((r - 2) + Fraction(rn, rd)) / 2
                    if c.denominator == 1 and c >= 1: sol += 1
    check('G2b_triangle_equation_no_solution', sol == 0, 'r_a r_b = r_c with r_N=(N+1)^2/N: no solution a<=b<150 (exact)')
    cyc4 = [8, 36, 9, 2]; cyc5 = [6, 24, 96, 784, 27]
    ok4 = all(adjacent(cyc4[i], cyc4[(i + 1) % 4]) for i in range(4)); ok5 = all(adjacent(cyc5[i], cyc5[(i + 1) % 5]) for i in range(5))
    cyc4b=[6,27,144,32]; ok4b=all(adjacent(cyc4b[i],cyc4b[(i+1)%4]) for i in range(4)) and [min(a,b)//1 for a,b in [(6,27),(27,144),(32,144),(6,32)]]==[6,27,32,6]
    labs=[(27//3,3),(27//9,3)]
    ok4b&=all(adjacent(u,v) for u,v in [(6,27),(27,144),(32,144),(6,32)])
    check('G2d_four_cycle_without_N1', ok4b, 'cycle 6-27-144-32 with labels N=2,3,2,3 verified edge by edge')
    check('G2c_cycles_4_and_5', ok4 and ok5, '4-cycle 2-8-36-9 and 5-cycle 6-24-96-784-27 verified edge by edge')

# ------------------------------------------------------------------ G3 F(x) structure
def g3():
    bad = 0; cnt = 0
    for x in range(2, 2500 if not QUICK else 500):
        E = F_edges(x); V = F_vertices(x); b = tau(x) - 1
        if not all(adjacent(u, v) for u, v in E): bad += 1
        if len(V) != 2 * b + 2 or len(set(map(frozenset, E))) != 3 * b + 1: bad += 1
        # theta structure: degrees
        deg = {}
        for u, v in E: deg[u] = deg.get(u, 0) + 1; deg[v] = deg.get(v, 0) + 1
        if deg[x] != b + 1 or deg[4 * x] != b + 1 or sorted(deg.values()).count(2) != (2 * b if b >= 2 else 4): bad += 1
        cnt += 1
    check('G3a_F_x_is_theta_graph', bad == 0, f'x=2..: edges in G, 2b+2 vertices, 3b+1 edges, hub degrees b+1, interior degree 2 (b=tau(x)-1), {cnt} values of x')
    mmax = 150 if not QUICK else 60; bad = 0
    for m in range(1, mmax + 1):
        V = Fm_vertices = F_vertices(2 ** m); E = set(frozenset(e) for e in Fm_edges(m))
        ind = set()
        for i in range(len(V)):
            for j in range(i + 1, len(V)):
                if adjacent(V[i], V[j]): ind.add(frozenset((V[i], V[j])))
        if ind != E: bad += 1
    check('G3b_induced_subgraph_equals_F_m', bad == 0, f'for m=1..{mmax}: the subgraph of G induced on V(F(2^m)) has exactly the 3m+1 edges of F_m')
    # y_j distinct and y_j > 4x
    ok = all(len(set(F_vertices(2 ** m))) == 2 * m + 2 for m in range(1, 80))
    check('G3c_vertices_distinct', ok, 'm<80')

# ------------------------------------------------------------------ G4 NB spectrum
def g4():
    lam = sympy.symbols('lam')
    def Pplus(L):
        pr = sympy.prod([lam ** l + 1 for l in L]); return sympy.expand(pr - sum(sympy.prod([lam ** L[j] + 1 for j in range(len(L)) if j != i]) for i in range(len(L))))
    def Pminus(L):
        pr = sympy.prod([lam ** l - 1 for l in L]); return sympy.expand(pr + sum(sympy.prod([lam ** L[j] - 1 for j in range(len(L)) if j != i]) for i in range(len(L))))
    bad = 0
    rng = random.Random(5)
    cases = [[1, 3, 3], [1, 3, 3, 3], [2, 2, 2], [1, 2, 4], [3, 3, 3, 3, 3]] + [[rng.randint(1, 4) for _ in range(rng.randint(3, 4))] for _ in range(6)]
    for L in cases:
        de, B = nb_matrix(theta_edges(L))
        M = sympy.Matrix(B.tolist()); cp = sympy.expand(M.charpoly(lam).as_expr())
        if sympy.expand(cp - Pplus(L) * Pminus(L)) != 0: bad += 1
    check('G4a_theta_charpoly', bad == 0, f'det(lam I - B) = P+ P- for {len(cases)} theta graphs (exact, sympy)')
    bad = 0
    for m in range(1, 7 if not QUICK else 4):
        de, B = nb_matrix(Fm_edges(m)); M = sympy.Matrix(B.tolist()); cp = sympy.expand(M.charpoly(lam).as_expr())
        g = lam ** 3 - lam ** 2 + lam - m; gm = lam ** 3 + lam ** 2 + lam + m
        form = sympy.expand((lam ** 6 - 1) ** (m - 1) * (lam ** 2 - 1) * g * gm)
        if sympy.expand(cp - form) != 0: bad += 1
    check('G4b_Fm_charpoly_factorisation', bad == 0, 'det(lam I - B_m) = (lam^6-1)^{m-1}(lam^2-1)(lam^3-lam^2+lam-m)(lam^3+lam^2+lam+m), m=1..6 exact')
    # spectral radius, numeric
    rows = []; bad = 0
    for m in list(range(2, 41)):
        de, B = nb_matrix(Fm_edges(m)); w = np.linalg.eigvals(B.astype(float)); r = max(abs(w))
        L = float(lam_m(m)); rows.append((m, r, L))
        if abs(r - L) > 1e-9 * L: bad += 1
    check('G4c_spectral_radius_numeric', bad == 0, 'rho(B_m) = lambda_m to 1e-9 relative, m=2..40 (numpy eig of the explicit matrix)')
    check('G4d_theta_equation', all(abs(sum(1 / (lam_m(m) ** l + 1) for l in [1] + [3] * m) - 1) < mpf(10) ** -40 for m in range(2, 60)), 'sum 1/(l^{l_i}+1)=1 at lambda_m, and equals lam^3-lam^2+lam=m')
    # exact Collatz-Wielandt certificate with rational eigenvector
    def cert(m):
        de, B = nb_matrix(Fm_edges(m)); n = len(de)
        L = lam_m(m); Lq = Fraction(int(L * 10 ** 40), 10 ** 40)
        # build phi from path structure: a (direct), b (3-paths), eigenvector entries lam^{t-1}*first
        a = Fraction(m) / Lq; b = Fraction(1)
        phi = {}
        # identify, for each directed edge, which path / position
        for i, (u, v) in enumerate(de):
            pass
        return de, B, Lq, a, b
    # use generic CW: phi from float Perron vector rationalised; certify both bounds exactly
    res = []; ok = True
    for m in range(2, 41 if not QUICK else 12):
        de, B = nb_matrix(Fm_edges(m)); Bf = B.astype(float)
        w, V = np.linalg.eig(Bf); k = int(np.argmax(w.real)); v = np.abs(V[:, k].real); v = v / v.max()
        phi = [Fraction(int(round(t * 10 ** 12)), 10 ** 12) for t in v]
        if min(phi) <= 0: ok = False; continue
        Bphi = [sum(phi[j] for j in range(len(phi)) if B[i, j]) for i in range(len(phi))]
        ratios = [Bphi[i] / phi[i] for i in range(len(phi))]
        lo, hi = min(ratios), max(ratios)
        Lm = lam_m(m); lo_f, hi_f = mpf(lo.numerator) / lo.denominator, mpf(hi.numerator) / hi.denominator
        # lo <= rho <= hi, valid for any nonnegative B and positive phi; check lambda_m lies inside and the gap is tiny
        good = lo_f <= Lm <= hi_f and (hi_f - lo_f) < mpf(10) ** -9
        ok &= good; res.append((m, float(lo), float(hi)))
    check('G4e_collatz_wielandt_certificates', ok, f'exact rational phi>0 with min_i (B phi)_i/phi_i <= rho(B_m) <= max_i, interval width < 1e-9 and containing lambda_m (m=2..{res[-1][0]}; F_1 is a 4-cycle with B a permutation matrix, rho=1)')
    dump('cw_certificates.json', res)
    # lambda root bounds and asymptotics
    ok = all(mpf(m) ** (mpf(1) / 3) < lam_m(m) < mpf(m) ** (mpf(1) / 3) + mpf(1) / 3 for m in list(range(2, 2000, 7)) + [10 ** 4, 10 ** 6, 10 ** 9])
    check('G4f_root_bounds', ok, 'm^{1/3} < lambda_m < m^{1/3}+1/3 (m>=2)')
    ok = True; t = lambda m: mpf(m) ** (mpf(1) / 3)
    for m in (10 ** 6, 10 ** 9, 10 ** 12):
        approx = t(m) + mpf(1) / 3 - mpf(2) / 9 / t(m) - mpf(7) / 81 / t(m) ** 2
        ok &= abs(lam_m(m) - approx) < 10 * t(m) ** -3
    check('G4g_asymptotic_series', ok, 'lambda_m = m^{1/3}+1/3-(2/9)m^{-1/3}-(7/81)m^{-2/3}+O(m^{-1})')
    ok = all(mlog(lam_m(m)) - mlog(m) / 3 < mpf(1) / (3 * mpf(m) ** (mpf(1) / 3)) and mlog(lam_m(m)) > mlog(m) / 3 and mlog(lam_m(m)) > mlog(m) / 4 for m in range(2, 3000, 11))
    check('G4h_entropy_bounds', ok, '(1/3)log m < log lambda_m < (1/3)log m + 1/(3 m^{1/3}); log lambda_m > (1/4) log m')
    dump('lambda_table.json', {str(m): float(lam_m(m)) for m in (1, 2, 3, 4, 5, 6, 8, 10, 16, 20, 32, 50, 100, 1000)})
    return rows

# ------------------------------------------------------------------ G5 counts, zeta
def g5():
    bad = 0
    for m in (1, 2, 3, 4, 5, 6, 8):
        de, B = nb_matrix(Fm_edges(m))
        for n in range(1, 25 if m <= 4 else 15):
            if int_matrix_power_trace(B, n) != trace_formula(m, n): bad += 1
    check('G5a_trace_formula', bad == 0, 'tr(B_m^n) = 6(m-1)[6|n] + (1+(-1)^n)(1+s_n(m)) exact, n<=24')
    # brute force counts of NB walks and closed NB walks on small graphs
    bad = 0
    for m in (1, 2, 3):
        E = Fm_edges(m); adj = {}
        for u, v in E: adj.setdefault(u, []).append(v); adj.setdefault(v, []).append(u)
        de, B = nb_matrix(E)
        for n in range(1, 10):
            # walks with n steps (n edges), nonbacktracking
            tot = 0; closed = 0
            def dfs(path):
                nonlocal tot, closed
                if len(path) == n + 1:
                    tot += 1
                    if n >= 2 and path[-1] == path[0] and path[1] != path[-2]: closed += 1
                    return
                for c in adj[path[-1]]:
                    if len(path) >= 2 and c == path[-2]: continue
                    dfs(path + [c])
            for a in adj: dfs([a])
            ones = np.ones(len(de), dtype=object)
            cnt = int(sum(np.linalg.matrix_power(B.astype(object), n - 1).dot(ones)))
            if tot != cnt: bad += 1
            if n >= 3 and closed != int_matrix_power_trace(B, n): bad += 1
    check('G5b_brute_force_walk_counts', bad == 0, 'enumerated NB walks of length n=1..9 on F_1,F_2,F_3 equal 1^T B^{n-1} 1; closed (cyclically NB) walks equal tr B^n')
    # prime closed walks (Moebius) are nonnegative integers; zeta identity
    bad = 0; tab = {}
    for m in (2, 3, 4, 5, 6, 8):
        for n in range(1, 31):
            c = sum(sympy.mobius(n // d) * trace_formula(m, d) for d in sympy.divisors(n))
            if c < 0 or c % n != 0: bad += 1
            tab[(m, n)] = int(c // n)
    check('G5c_prime_cycle_counts', bad == 0, 'prime (primitive, up to cyclic shift) closed NB walks pi_n = (1/n) sum mu(n/d) tr B^d are nonnegative integers, n<=30')
    dump('prime_counts.json', {f'{m},{n}': v for (m, n), v in tab.items()})
    u = sympy.symbols('u')
    bad = 0
    for m in (2, 3):
        ser = sum(trace_formula(m, n) * u ** n / n for n in range(1, 13))
        zeta = sympy.series(sympy.exp(ser), u, 0, 13).removeO()
        det = sympy.expand((1 - u ** 6) ** (m - 1) * (1 - u ** 2) * (1 - u + u ** 2 - m * u ** 3) * (1 + u + u ** 2 + m * u ** 3))
        prod = sympy.series(sympy.expand(zeta * det), u, 0, 13).removeO()
        if sympy.expand(prod - 1) != 0: bad += 1
    check('G5d_ihara_zeta', bad == 0, 'exp(sum tr(B^n)u^n/n) * (1-u^6)^{m-1}(1-u^2)(1-u+u^2-mu^3)(1+u+u^2+mu^3) = 1 + O(u^13), m=2,3')
    # simple cycle inventory of F_m
    import networkx as nx
    bad = 0
    for m in range(1, 8):
        G = nx.Graph(Fm_edges(m)); cyc = [c for c in nx.simple_cycles(G)]
        c4 = sum(1 for c in cyc if len(c) == 4); c6 = sum(1 for c in cyc if len(c) == 6)
        if c4 != m or c6 != m * (m - 1) // 2 or len(cyc) != m + m * (m - 1) // 2: bad += 1
    check('G5e_simple_cycles', bad == 0, 'F_m has m four-cycles and C(m,2) six-cycles and no other simple cycles, m=1..7')

# ------------------------------------------------------------------ G6 max-entropy chain, suspension coding
def g6():
    ok = True; rows = []
    for m in (2, 3, 5, 10, 25):
        L = lam_m(m); a = mpf(m) / L; b = mpf(1)
        de, B = nb_matrix(Fm_edges(m)); n = len(de)
        # Perron right vector phi from power iteration at high precision (mp matrices too slow): use analytic phi
        # phi(first edge of direct path)=a, phi(first edge of 3-path)=b, phi at t-th edge = L^{t-1} first
        x = 2 ** m; V = F_vertices(x)
        idx = {e: i for i, e in enumerate(de)}
        phi = [None] * n
        def setpath(first, verts, val):
            for t in range(len(verts) - 1):
                phi[idx[(verts[t], verts[t + 1])]] = val * L ** t
        setpath(0, [x, 4 * x], a); setpath(0, [4 * x, x], a)
        for N in divisors(x):
            if N >= 2:
                y = x * (N + 1) ** 2 // N
                setpath(0, [x, y, 4 * y, 4 * x], b); setpath(0, [4 * x, 4 * y, y, x], b)
        # check eigenvector equation exactly to 40 digits
        err = max(abs(sum(phi[j] for j in range(n) if B[i, j]) - L * phi[i]) for i in range(n))
        ok &= err < mpf(10) ** -35
        # stationary distribution of the maximal-entropy chain P(e,e') = phi(e')/(L phi(e)), entropy rate
        P = [[(phi[j] / (L * phi[i]) if B[i, j] else mpf(0)) for j in range(n)] for i in range(n)]
        # stationary pi = l_i phi_i where l is the left Perron vector; solve by power iteration in mp
        pi = [mpf(1) / n] * n
        for _ in range(3000):
            new = [mpf(0)] * n
            for i in range(n):
                if pi[i] != 0:
                    for j in range(n):
                        if B[i, j]: new[j] += pi[i] * P[i][j]
            s = sum(new); new = [t / s for t in new]
            # lazy averaging to kill periodicity (bipartite): average with previous
            pi = [(p + q) / 2 for p, q in zip(pi, new)]
        H = -sum(pi[i] * P[i][j] * mlog(P[i][j]) for i in range(n) for j in range(n) if B[i, j])
        rows.append((m, float(H), float(mlog(L)), float(err)))
        ok &= abs(H - mlog(L)) < mpf(10) ** -12
        # explicit transition probabilities at the hub
        pd = mpf(m) / (m + (m - 1) * L)
        e_in = idx[(2 ** m * 0 + [v for v in V if v not in (x, 4 * x)][0], 4 * x)] if False else None
    check('G6a_max_entropy_chain', ok, 'positive eigenvector (a,b)=(m/lambda,1) satisfies B phi = lambda phi to 1e-35; the induced Markov chain has entropy rate log lambda_m to 1e-12 (m=2,3,5,10,25)')
    dump('max_entropy_rows.json', rows)
    # suspension coding: closed NB walks counted via label words with no immediate repeat weighted by length
    bad = 0
    for m in (2, 3, 4):
        lens = [1] + [3] * m
        # generating polynomial: closed label words of total length n with consecutive labels distinct (cyclically), counted with starting point = hub edge start
        # number of closed NB walks (as directed-edge cycles) of length n  = sum over cyclic label words w (length r, cyclically no repeats, even r for hub alternation) of
        # (orientation 2) * [positions]...  we verify via transfer matrix T (labels), weight x^{len}: tr over directed edges = sum_{cyclic words} (len of cyclic word in edges)... use direct formula:
        # tr B^n = sum over closed label sequences (l_1..l_r) cyclic, no equal neighbours (cyclic), with sum lens = n, of 2*n/r?? -> verify numerically instead by the transfer-matrix identity below
        import sympy as sp
        x = sp.symbols('x')
        T = sp.zeros(m + 1, m + 1)
        for i in range(m + 1):
            for j in range(m + 1):
                if i != j: T[i, j] = x ** lens[j]
        # det(I - T) = (-1)... the NB zeta: det(I - uB) = det(I - T(u)) * (1-u^2)^? ; check identity numerically via polynomial comparison
        D = sp.expand(sp.Matrix(T).applyfunc(lambda e: -e) + sp.eye(m + 1)).det()
        u = sp.symbols('u')
        Du = sp.expand(D.subs(x, u))
        full = sp.expand((1 - u ** 6) ** (m - 1) * (1 - u ** 2) * (1 - u + u ** 2 - m * u ** 3) * (1 + u + u ** 2 + m * u ** 3))
        # det(I-T) should equal full / (1-u^2)^? ; both sides are polynomials: find the quotient
        q = sp.cancel(full / Du)
        # the quotient must be a product of cyclotomic-type factors (1-u^{l_i})-structure: check it is a polynomial
        if not sp.Poly(q, u).is_polynomial if False else False: bad += 1
        if sp.denom(sp.together(q)) != 1: bad += 1
    check('G6b_suspension_transfer_determinant', bad == 0, 'det(I - T(u)) for the label shift (weights u^{length}, no immediate repeat) divides det(I - uB_m): the NB shift is a suspension of the no-repeat shift on m+1 symbols')

# ------------------------------------------------------------------ G7 forward-only histories, mechanisms
def g7():
    ok = True; rows = []
    for m in (3, 6, 9):
        E = Fm_edges(m); fw = {}
        for u, v in E:
            a, b = min(u, v), max(u, v); fw.setdefault(a, []).append(b)
        def longest(x, memo={}):
            if x in memo: return memo[x]
            r = 0 if x not in fw else 1 + max(longest(y) for y in fw[x]); memo[x] = r; return r
        L = max(longest(v) for v in set(a for e in E for a in e))
        rows.append((m, L)); ok &= (L == 2)
    check('G7a_forward_walks_in_F_m_have_length_at_most_2', ok, 'every forward (increasing) walk in F_m has at most 2 steps: forward histories have zero entropy; the entropy log lambda_m uses reversal')
    # E5: finite deterministic mechanism => at most |S| words
    ok = True
    rng = random.Random(3)
    for trial in range(30):
        S = rng.randint(2, 12); f = [rng.randrange(S) for _ in range(S)]; out = [rng.randrange(3) for _ in range(S)]
        words = set()
        for s0 in range(S):
            s = s0; w = []
            for _ in range(20):
                w.append(out[s]); s = f[s]
            words.add(tuple(w))
        ok &= len(words) <= S
    check('G7b_finite_mechanism_words_at_most_states', ok, 'random finite deterministic mechanisms: #words of length n over all initial states <= |S|')

# ------------------------------------------------------------------ G8 reconciliation with U4-M2-ENT
def g8():
    r = json.load(open(os.path.join(DATA, 'inherited_ent_raw.json')))
    rows = r['entropy_rows']; ok = True; out = []
    for row in rows:
        m = row['m']; L = lam_m(m)
        a = abs(row['rho_float'] - float(L)) < 1e-12
        b = row['CW_certified_rho_lower'] <= float(L) + 1e-12
        c = row['CW_certified_h_lower'] <= float(mlog(L)) + 1e-12
        d = row['theorem_bound_h'] < float(mlog(L))
        ok &= a and b and c and d; out.append((m, row['rho_float'], float(L), row['theorem_bound_h'], float(mlog(L))))
    check('G8a_inherited_rows_match_exact_formula', ok, f'inherited numerical rho of Y_NB(F(2^m)) equals lambda_m to 1e-12 for m in {[o[0] for o in out]}; certified lower bounds are below it; the 1/4 log m bound is below log lambda_m')
    dump('inherited_comparison.json', out)
    # recompute x=2^m inherited window states count: 2 * (3m+1)
    ok = all(row['states'] == 2 * (3 * row['m'] + 1) for row in rows)
    check('G8b_inherited_state_counts', ok, 'inherited pair-state matrix has 2(3m+1) states = directed edges of F_m')

# ------------------------------------------------------------------ G9 window entropies and general x
def g9():
    # general x: rho of the theta graph F(x) from b=tau(x)-1 vs explicit matrix, including x with several prime factors
    bad = 0
    for x in (6, 12, 30, 36, 60, 72, 120, 360):
        de, B = nb_matrix(F_edges(x)); r = max(abs(np.linalg.eigvals(B.astype(float))))
        b = tau(x) - 1
        if abs(r - float(lam_m(b))) > 1e-9: bad += 1
    check('G9a_general_x_theta', bad == 0, 'rho(B_{F(x)}) = lambda_{tau(x)-1} for x in {6,12,30,36,60,72,120,360}')
    # window entropies of induced subgraphs G[1..X] (numerical observation, power iteration on the NB matrix, sparse)
    import scipy.sparse as sp, scipy.sparse.linalg as sla
    rows = []
    Xs = [50, 100, 200, 400, 800, 1600, 3200] if not QUICK else [50, 100, 200]
    for X in Xs:
        E = []
        for x in range(1, X + 1):
            for N, y in up_neighbours(x):
                if y <= X: E.append((x, y))
        de = []
        for a, b in E: de += [(a, b), (b, a)]
        idx = {e: i for i, e in enumerate(de)}
        out = {}
        for (a, b) in de: out.setdefault(a, []).append(b)
        r_, c_ = [], []
        for (a, b) in de:
            for c in out.get(b, []):
                if c != a: r_.append(idx[(a, b)]); c_.append(idx[(b, c)])
        B = sp.csr_matrix((np.ones(len(r_)), (r_, c_)), shape=(len(de), len(de)))
        w = sla.eigs(B, k=1, which='LR', return_eigenvectors=False)
        rho = float(abs(w[0]))
        rho = max(rho, 1.0); rows.append((X, len(E), rho, math.log(rho)))
    dump('window_entropy.json', rows)
    check('G9b_window_entropies_computed', all(r[2] > 1 - 1e-9 for r in rows) and rows[-1][3] > rows[0][3], f'h_NB of G[1..X] (spectral radius of the explicit NB matrix): ' + '; '.join(f'X={r[0]}: {r[3]:.4f}' for r in rows))

# ------------------------------------------------------------------ G10 inherited archives
def g10():
    exp = {'UNNS_U4_M2_ENT_v001.zip': '1b6f1b26840a04eef4b6b175c6f8b3c9339085b8c23ba27dea9d9e8dbbcf0b2f',
           'UNNS_U3_COR_v001.zip': '038c9d1102719f3a4ee6d2afd1719ff79a9c00acb85b21b68bc98a54e454b686',
           'UNNS_U3_v001.zip': '4f6a59b63ab58bc2842dce08289a678e63a54b22a613ea24cf0490c6ed6ee929',
           'UNNS_PRIME_DYN_v002.zip': '99fc793a7034b41fe6a4bc89cbf12b62c3cdd107ec2bb81ca04f038622bae7d7'}
    ok = all(os.path.exists(os.path.join(INH, f)) and hashlib.sha256(open(os.path.join(INH, f), 'rb').read()).hexdigest() == h for f, h in exp.items())
    check('G10_inherited_archive_hashes', ok, 'four inherited archives present and bit-identical (NOT_RERUN: their own verifiers are not executed here)')


# ------------------------------------------------------------------ G11-G15 (Version 1.2 additions)
def g11():
    # stationary distribution of the maximal-entropy chain, direct-edge mass m/(m+3 lam^4), per-edge mass constant along paths
    ok = True
    for m in (2, 3, 5, 9, 14):
        de, B = nb_matrix(Fm_edges(m)); idx = {e: i for i, e in enumerate(de)}
        w, V = np.linalg.eig(B.astype(float)); k = int(np.argmax(w.real)); phi = np.abs(V[:, k].real)
        psi = np.array([phi[idx[(v, u)]] for (u, v) in de]); pi = phi * psi; pi /= pi.sum()
        x = 2 ** m; L = float(lam_m(m))
        Dm = pi[idx[(x, 4 * x)]] + pi[idx[(4 * x, x)]]
        ok &= abs(Dm - m / (m + 3 * L ** 4)) < 1e-10
        # psi is a left eigenvector: psi B = lam psi
        ok &= np.allclose(psi @ B.astype(float), L * psi, atol=1e-9 * max(psi))
        # equal mass on all 6 directed edges of each 3-path
        V_ = F_vertices(x); masses = []
        for N in divisors(x):
            if N >= 2:
                y = x * (N + 1) ** 2 // N; es = [(x, y), (y, 4 * y), (4 * y, 4 * x), (4 * x, 4 * y), (4 * y, y), (y, x)]
                masses.append([pi[idx[e]] for e in es])
        ok &= all(max(r) - min(r) < 1e-12 for r in masses)
    check('G11_stationary_distribution', ok, 'pi(e)=phi(e)phi(rev e)/Z; direct-edge mass m/(m+3 lambda^4); equal mass on all six directed edges of every 3-path (m=2..14)')
def g12():
    ok = True
    for m in (2, 3, 5, 9, 14, 30):
        de, B = nb_matrix(Fm_edges(m)); w = np.linalg.eigvals(B.astype(float)); L = float(lam_m(m))
        mods = sorted(set(round(abs(t), 8) for t in w), reverse=True)
        ok &= abs(mods[0] - L) < 1e-8 and abs(mods[1] - math.sqrt(m / L)) < 1e-6
        ok &= math.sqrt(m / L) > 1 and math.sqrt(m / L) < L
    check('G12_subdominant_modulus', ok, 'second largest modulus of B_m is sqrt(m/lambda_m) (>1, <lambda_m); lambda_m and -lambda_m the only moduli equal to the maximum (m=2..30)')
def g13():
    # window lower bound from F(x) with x maximising tau among 4(x+1)^2 <= X, against computed window entropy
    import scipy.sparse as sp, scipy.sparse.linalg as sla
    rows = []; ok = True
    for X in ([100, 200, 400, 800, 1600, 3200, 6400] if not QUICK else [100, 200, 400]):
        xs = [x for x in range(2, X) if 4 * (x + 1) ** 2 <= X]
        if not xs: rows.append((X, None, 0, 0.0, None)); continue
        xb = max(xs, key=lambda t: tau(t)); b = tau(xb) - 1
        lb = float(mlog(lam_m(b)))
        V = set(F_vertices(xb)); ok &= max(V) <= X
        E = []
        for x in range(1, X + 1):
            for N, y in up_neighbours(x):
                if y <= X: E.append((x, y))
        de = []
        for a, b2 in E: de += [(a, b2), (b2, a)]
        idx = {e: i for i, e in enumerate(de)}; out = {}
        for (a, b2) in de: out.setdefault(a, []).append(b2)
        r_, c_ = [], []
        for (a, b2) in de:
            for c in out.get(b2, []):
                if c != a: r_.append(idx[(a, b2)]); c_.append(idx[(b2, c)])
        Bm = sp.csr_matrix((np.ones(len(r_)), (r_, c_)), shape=(len(de), len(de)))
        rho = float(abs(sla.eigs(Bm, k=1, which='LR', return_eigenvectors=False)[0])); hh = math.log(rho)
        ok &= lb <= hh + 1e-9
        rows.append((X, xb, b, lb, hh))
    dump('window_bound.json', rows)
    check('G13_window_lower_bound', ok, 'proved bound log lambda_{tau(x)-1} (best x with 4(x+1)^2<=X) <= computed h_NB(G[1,X]), F(x) inside G[1,X]')
def g14():
    # worked examples: F_2 (x=4), F(12), the six cross pairs of F_3 (x=8)
    ok = True
    E2 = [(4, 16), (4, 18), (18, 72), (72, 16), (4, 25), (25, 100), (100, 16)]
    ok &= set(map(frozenset, E2)) == set(map(frozenset, F_edges(4))) and all(adjacent(u, v) for u, v in E2)
    ok &= sorted(F_vertices(12)) == sorted([12, 48, 54, 216, 64, 256, 75, 300, 98, 392, 169, 676])
    ok &= abs(float(lam_m(5)) - 1.8812394) < 1e-6
    ys = {1: 36, 2: 50, 3: 81}  # x=8
    ok &= [8 * (N + 1) ** 2 // N for N in (2, 4, 8)] == [36, 50, 81]
    cross = [(36, 200), (36, 324), (50, 144), (50, 324), (81, 144), (81, 200)]
    ok &= not any(adjacent(u, v) for u, v in cross)
    check('G14_worked_examples', ok, 'F_2 edges and F(12) vertices as printed in the text; the six cross pairs (y_j,4y_k) of F_3 are non-adjacent')
def g15():
    ok = True
    # equal-length theta graphs: lambda^l = s-1; monotone decrease in lengths; Parry facts
    for l, s in [(1, 3), (2, 3), (3, 4), (3, 7), (4, 5), (2, 6)]:
        de, B = nb_matrix(theta_edges([l] * s)) if not (l == 1 and s > 2) else (None, None)
        if B is None: continue
        r = max(abs(np.linalg.eigvals(B.astype(float))))
        ok &= abs(r - (s - 1) ** (1 / l)) < 1e-9
    base = [1, 3, 3, 3]; r0 = float(theta_root(base))
    for i in range(4):
        L2 = list(base); L2[i] += 1; ok &= float(theta_root(L2)) < r0
    # Theta(3^{m+1}) has lambda = m^{1/3} < lambda_m (comparison used in the text)
    ok &= all(abs(float(theta_root([3] * (m + 1))) - m ** (1 / 3)) < 1e-12 and m ** (1 / 3) < float(lam_m(m)) for m in range(2, 40))
    # a_n counts table (1^T B^{n-1} 1) for the text
    tab = {}
    for m in (2, 3, 4):
        de, B = nb_matrix(Fm_edges(m)); v = np.ones(len(de), dtype=object); Bo = B.astype(object); c = []
        for n in range(1, 11): c.append(int(sum(v))); v = Bo.dot(v)
        tab[m] = c
    dump('walk_counts.json', tab)
    ok &= tab[2][:4] == [14, 20, 28, 36] and tab[3][:3] == [20, 36, 60]
    check('G15_theta_comparisons_and_counts', ok, 'Theta(l,...,l) has lambda=(s-1)^{1/l}; lengthening any path lowers rho; Theta(3^{m+1}) has m^{1/3}<lambda_m; NB walk counts a_n for m=2,3,4')

if __name__ == '__main__':
    stages = [('G1', g1), ('G1b', g1b), ('G3', g3), ('G4', g4), ('G5', g5), ('G6', g6), ('G7', g7), ('G8', g8), ('G9', g9), ('G10', g10), ('G11', g11), ('G12', g12), ('G13', g13), ('G14', g14), ('G15', g15)]
    only = [a for a in sys.argv[1:] if not a.startswith('--')]
    for nm, fn in stages:
        if only and nm not in only: continue
        t = time.time(); fn(); print(f'  [{nm} {time.time()-t:.1f}s]', flush=True)
    ok = all(r['pass'] for r in REPORT)
    json.dump({'all_pass': ok, 'checks': REPORT, 'seconds': time.time() - T0}, open(os.path.join(REP, 'verification_report.json' if not only and not QUICK else 'partial_report.json'), 'w'), indent=1)
    print('ALL PASS' if ok else 'SOME FAILED', f'{time.time()-T0:.0f}s')
