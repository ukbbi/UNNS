"""Exact rational linear programming (Bland's rule, two-phase tableau).  No floating point.
Problem form used throughout GEO-I v003:   maximize c.z   subject to   A z = b,   0 <= z <= 1.
"""
try:
    from gmpy2 import mpq as Fr          # exact rationals, much faster than fractions.Fraction (same results)
except Exception:                         # pragma: no cover
    from fractions import Fraction as Fr


def lp_box(A, b, c, n):
    """returns ('infeasible', None, None) or ('optimal', value, z).  A: list of rows (len n), b: rhs list, c: objective (len n)."""
    m = len(A)
    N = 2 * n                       # z_1..z_n, slack w_i = 1 - z_i
    rows, rhs = [], []
    for i in range(m):
        rows.append([Fr(v) for v in A[i]] + [Fr(0)] * n); rhs.append(Fr(b[i]))
    for i in range(n):
        r = [Fr(0)] * N; r[i] = Fr(1); r[n + i] = Fr(1); rows.append(r); rhs.append(Fr(1))
    M = len(rows)
    for i in range(M):
        if rhs[i] < 0: rows[i] = [-v for v in rows[i]]; rhs[i] = -rhs[i]
    W = N + M
    T = [rows[i] + [Fr(1) if j == i else Fr(0) for j in range(M)] + [rhs[i]] for i in range(M)]
    basis = [N + i for i in range(M)]

    def pivot(r, col):
        pv = T[r][col]
        T[r] = [v / pv for v in T[r]]
        for i in range(M):
            if i != r and T[i][col] != 0:
                f = T[i][col]; Ti, Tr = T[i], T[r]
                T[i] = [a - f * bb for a, bb in zip(Ti, Tr)]
        basis[r] = col

    def run(cost, allowed):
        """maximize cost.x over the current tableau; returns value or None if unbounded (cannot happen: bounded box)."""
        while True:
            # reduced costs: cost_j - sum_i cost_basis[i]*T[i][j]
            cb = [cost[basis[i]] if basis[i] < len(cost) else Fr(0) for i in range(M)]
            enter = None
            for j in range(allowed):
                if j in basis: continue
                rc = (cost[j] if j < len(cost) else Fr(0)) - sum(cb[i] * T[i][j] for i in range(M) if cb[i] != 0)
                if rc > 0: enter = j; break
            if enter is None: break
            best = None
            for i in range(M):
                if T[i][enter] > 0:
                    ratio = T[i][W] / T[i][enter]
                    if best is None or ratio < best[0] or (ratio == best[0] and basis[i] < basis[best[1]]): best = (ratio, i)
            if best is None: return None
            pivot(best[1], enter)
        return sum((cost[basis[i]] if basis[i] < len(cost) else Fr(0)) * T[i][W] for i in range(M))

    cost1 = [Fr(0)] * N + [Fr(-1)] * M
    v1 = run(cost1, W)
    if v1 != 0: return ('infeasible', None, None)
    # drive artificials out of the basis
    keep = list(range(M))
    for i in range(M):
        if basis[i] >= N:
            col = next((j for j in range(N) if T[i][j] != 0), None)
            if col is not None: pivot(i, col)
    cost2 = [Fr(v) for v in c] + [Fr(0)] * (N - n)
    # forbid artificials entering: allowed = N columns
    val = run(cost2, N)
    z = [Fr(0)] * N
    for i in range(M):
        if basis[i] < N: z[basis[i]] = T[i][W]
    return ('optimal', val, z[:n])


def feasible_box(A, b, n):
    return lp_box(A, b, [0] * n, n)[0] == 'optimal'
