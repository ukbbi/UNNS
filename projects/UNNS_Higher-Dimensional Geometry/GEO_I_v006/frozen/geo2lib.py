r"""GEO-I v002 exact engine. Integer / Fraction arithmetic only (no floating point).

Objects (from the v002 specification):
  x = a/b reduced; active primes p_i with q_i = floor(e_i/2) >= 1; box B = prod {0..q_i};
  modular relation lattice  Lambda_b = {alpha : prod p_i^alpha_i = 1 (mod b)}  (negative exponents by inverses);
  realized fibre F = (B ∩ Lambda_b) \ {0}.
Two adjacency structures:
  K_axis : cubical complex, moves = unit vectors +-e_i.
  K_move : cubical set, moves = region-restricted Graver basis of Lambda_b (conformally minimal lattice vectors
           whose coordinates satisfy |g_i| <= q_i, which are the only vectors that can join two points of B).
Cells are parallelotopes P(u; g_1..g_j): base u = lex-minimal vertex, generators lex-positive, sorted, linearly independent,
all 2^j vertices in F.  Homology is computed from explicit boundary matrices over GF(p).
"""
import itertools
from fractions import Fraction as Fr
from math import prod, gcd
from geo1lib import factor, val

# ---------------------------------------------------------------- coordinates
def coords(x):
    """x: int or Fraction.  returns (primes, q, b) with only primes whose q_i >= 1."""
    x = Fr(x); a, b = x.numerator, x.denominator
    f = factor(a) if a > 1 else {}
    ps = sorted(p for p, e in f.items() if e // 2 >= 1)
    return ps, [f[p] // 2 for p in ps], b

def chi_ok(ps, b, alpha):
    """alpha in Lambda_b ?  (b=1: Lambda = Z^k)."""
    if b == 1: return True
    r = 1
    for p, e in zip(ps, alpha): r = r * pow(p, e, b) % b      # pow handles negative e (modular inverse)
    return r == 1 % b

def fibre_points(ps, q, b):
    return [al for al in itertools.product(*[range(e + 1) for e in q]) if any(al) and chi_ok(ps, b, al)]

def d_value(ps, al): return prod(p ** e for p, e in zip(ps, al))

# ---------------------------------------------------------------- Graver moves
def lexpos(g):
    for c in g:
        if c: return c > 0
    return False

def graver_region(ps, q, b):
    """conformally minimal nonzero vectors of Lambda_b inside [-q,q]; returns all of them (both signs)."""
    k = len(q)
    cand = [g for g in itertools.product(*[range(-e, e + 1) for e in q]) if any(g) and chi_ok(ps, b, g)]
    cand.sort(key=lambda g: (sum(abs(c) for c in g), g))
    G = []
    for g in cand:
        dom = False
        for h in G:
            if all(hi * gi >= 0 and abs(hi) <= abs(gi) for hi, gi in zip(h, g)): dom = True; break
        if not dom: G.append(g)
    return G

def unit_moves(k):
    return [tuple(1 if i == j else 0 for i in range(k)) for j in range(k)] + \
           [tuple(-1 if i == j else 0 for i in range(k)) for j in range(k)]

# ---------------------------------------------------------------- linear algebra (exact)
def rank_Q(vecs):
    M = [[Fr(c) for c in v] for v in vecs]; r = 0
    if not M: return 0
    for c in range(len(M[0])):
        piv = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c] / M[r][c]; M[i] = [a - f * b2 for a, b2 in zip(M[i], M[r])]
        r += 1
    return r

def d_aff(F):
    if len(F) <= 1: return 0
    u0 = F[0]
    return rank_Q([tuple(a - b for a, b in zip(u, u0)) for u in F[1:]])

# ---------------------------------------------------------------- cells
def add(u, g): return tuple(a + b for a, b in zip(u, g))

def cell_vertices(u, gens):
    vs = [u]
    for g in gens: vs = vs + [add(v, g) for v in vs]
    return vs

def build_cells(F, moves, kmax):
    """returns list cells[j] of (base, gens) for j=0..; moves given as set of vectors (both signs allowed; only lex-positive used)."""
    Fs = set(F); pos = sorted(g for g in moves if lexpos(g))
    cells = [[(u, ()) for u in sorted(F)]]
    one = []
    for u in sorted(F):
        for g in pos:
            if add(u, g) in Fs: one.append((u, (g,)))
    cells.append(one)
    j = 1
    while cells[j] and j < kmax:
        nxt = []
        for (u, gens) in cells[j]:
            for g in pos:
                if g <= gens[-1]: continue
                if rank_Q(list(gens) + [g]) < j + 1: continue
                if all(add(v, g) in Fs for v in cell_vertices(u, gens)):
                    nxt.append((u, gens + (g,)))
        cells.append(nxt); j += 1
    while cells and not cells[-1]: cells.pop()
    return cells

def boundary(cell):
    u, gens = cell; out = {}
    for i, g in enumerate(gens):
        rest = gens[:i] + gens[i + 1:]
        s = 1 if i % 2 == 0 else -1
        for face, sg in (((add(u, g), rest), s), ((u, rest), -s)):
            out[face] = out.get(face, 0) + sg
    return out

def _rank_mod(cols, p):
    """cols: list of dict row->coeff. rank over GF(p) by sparse elimination."""
    pivots = {}; r = 0
    for col in cols:
        c = {k: v % p for k, v in col.items() if v % p}
        while c:
            piv = min(c)
            if piv in pivots:
                pc = pivots[piv]; f = c[piv] * pow(pc[piv], -1, p) % p
                for k, v in pc.items():
                    nv = (c.get(k, 0) - f * v) % p
                    if nv: c[k] = nv
                    else: c.pop(k, None)
            else:
                pivots[piv] = c; r += 1; break
    return r

def homology(cells, primes=(2, 2147483647)):
    """Betti numbers b_0..b_top over GF(p) for each p, plus check boundary-of-boundary = 0."""
    n = [len(c) for c in cells]
    # d^2 = 0 check
    d2 = True
    for j in range(2, len(cells)):
        for cell in cells[j]:
            acc = {}
            for f, s in boundary(cell).items():
                for f2, s2 in boundary(f).items(): acc[f2] = acc.get(f2, 0) + s * s2
            if any(acc.values()): d2 = False
    res = {}
    for p in primes:
        r = [0] * (len(cells) + 1)
        for j in range(1, len(cells)):
            r[j] = _rank_mod([boundary(c) for c in cells[j]], p)
        res[p] = [n[j] - r[j] - r[j + 1] for j in range(len(cells))]
    return res, d2

def components(F, cells):
    par = {u: u for u in F}
    def find(a):
        while par[a] != a: par[a] = par[par[a]]; a = par[a]
        return a
    if len(cells) > 1:
        for (u, gens) in cells[1]:
            a, b2 = find(u), find(add(u, gens[0]))
            if a != b2: par[a] = b2
    return len({find(u) for u in F})

def analyse(x, kmax=None, primes=(2, 2147483647), with_homology=True):
    """Full geometric profile of a state x (int or Fraction)."""
    ps, q, b = coords(x); k = len(ps)
    F = fibre_points(ps, q, b)
    out = {'x': str(Fr(x)), 'primes': ps, 'q': q, 'b': b, 'd_amb': k, 'R': len(F)}
    if not F:
        out.update({'d_aff': -1, 'axis': None, 'move': None}); return out
    out['d_aff'] = d_aff(F)
    kk = k if kmax is None else min(k, kmax)
    G = graver_region(ps, q, b)
    out['graver_region_size'] = len(G)
    for name, moves in (('axis', unit_moves(k)), ('move', G)):
        cells = build_cells(F, set(moves), kk)
        info = {'cells_per_dim': [len(c) for c in cells], 'd_cell': len(cells) - 1,
                'components': components(F, cells)}
        if with_homology:
            h, d2 = homology(cells, primes); info['betti'] = {str(p): v for p, v in h.items()}; info['d2_zero'] = d2
        out[name] = info
    out['graver_region'] = [list(g) for g in G if lexpos(g)]
    return out

# ---------------------------------------------------------------- flag (clique) complex of a move graph, for comparison only
def flag_cells(F, moves, maxdim=3):
    """simplices of the clique complex of the graph u~v iff v-u in moves (cells[j] = sorted vertex tuples, j+1 vertices)."""
    Fs = sorted(F); S = set(moves)
    adj = {u: set() for u in Fs}
    for i, u in enumerate(Fs):
        for v in Fs[i + 1:]:
            if tuple(a - b for a, b in zip(v, u)) in S: adj[u].add(v); adj[v].add(u)
    cells = [[(u,) for u in Fs]]
    cur = [(u, v) for u in Fs for v in sorted(adj[u]) if v > u]
    if cur: cells.append(cur)
    j = 1
    while cells[-1] and j < maxdim:
        nxt = []
        for s in cells[-1]:
            common = set.intersection(*[adj[v] for v in s])
            for w in sorted(common):
                if w > s[-1]: nxt.append(s + (w,))
        cells.append(nxt); j += 1
    while cells and not cells[-1]: cells.pop()
    return cells

def flag_betti(cells, primes=(2, 2147483647)):
    n = [len(c) for c in cells]; res = {}
    for p in primes:
        r = [0] * (len(cells) + 1)
        for j in range(1, len(cells)):
            cols = []
            for s in cells[j]:
                cols.append({s[:i] + s[i + 1:]: (1 if i % 2 == 0 else -1) for i in range(len(s))})
            r[j] = _rank_mod(cols, p)
        res[p] = [n[j] - r[j] - r[j + 1] for j in range(len(cells))]
    return res
