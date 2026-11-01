"""HD-1D v004 builder: the integer kernel L_A = ker_Z V_A (exact, via unimodular column reduction), primitive vectors, Graver candidates."""
from math import gcd
from itertools import product
from functools import reduce
from valuation_matrix import matrix


def int_kernel(M):
    """Z-basis of {x in Z^s : M x = 0} by column-style integer elimination (unimodular transform U with M U = [H | 0])."""
    r = len(M); s = len(M[0]) if M else 0
    cols = [[M[i][j] for i in range(r)] for j in range(s)]          # column vectors of M
    U = [[1 if i == j else 0 for i in range(s)] for j in range(s)]  # U[j] = j-th column of the transform
    piv = 0
    for i in range(r):
        while True:
            nz = [j for j in range(piv, s) if cols[j][i] != 0]
            if len(nz) <= 1: break
            j0 = min(nz, key=lambda j: abs(cols[j][i]))
            for j in nz:
                if j == j0: continue
                q = cols[j][i] // cols[j0][i]
                cols[j] = [a - q * b for a, b in zip(cols[j], cols[j0])]
                U[j] = [a - q * b for a, b in zip(U[j], U[j0])]
        nz = [j for j in range(piv, s) if cols[j][i] != 0]
        if nz:
            j0 = nz[0]; cols[piv], cols[j0] = cols[j0], cols[piv]; U[piv], U[j0] = U[j0], U[piv]; piv += 1
    return [tuple(U[j]) for j in range(piv, s)]


def rank(M):
    return len(M[0]) - len(int_kernel(M)) if M else 0


def kernel_of_alphabet(A):
    ps, V = matrix(A); return int_kernel(V)


def is_primitive(z): return reduce(gcd, [abs(x) for x in z]) == 1


def conformal_le(y, z):
    """y is conformally <= z : same sign pattern and |y_i| <= |z_i|"""
    return all(a * b >= 0 and abs(a) <= abs(b) for a, b in zip(y, z))


def graver_candidates(A, bound):
    """conformally minimal nonzero kernel vectors with |z_i| <= bound (box search; EXACT inside the box: a vector of the box is Graver
    iff no other nonzero kernel vector of the box is conformally below it, since a conformally smaller vector lies in the same box)"""
    ps, V = matrix(A); s = len(A)
    ker = []
    for z in product(range(-bound, bound + 1), repeat=s):
        if any(z) and all(sum(V[i][j] * z[j] for j in range(s)) == 0 for i in range(len(ps))): ker.append(z)
    return [z for z in ker if not any(y != z and conformal_le(y, z) for y in ker)]
