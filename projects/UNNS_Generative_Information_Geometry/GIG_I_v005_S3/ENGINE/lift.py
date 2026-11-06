"""GIG-I v005 Stage 3 -- the suspension lift  C_2(P_6) -> C_3(P_7)  (new rank r = k-1 appended as the largest label).
Ins_i(f): add r to block i of f (dimension +1);  first(g)=({r}|g), last(g)=(g|{r}).
Lam(z) = sum_f sum_i Ins_i(f).  For a 2-cycle z and a 3-chain c with boundary z:   L_c(z) = Lam(z) + first(c) + last(c)."""
import _vpath  # noqa: F401
from pk import PK


def ins(face, i, r):
    return tuple(tuple(sorted(B + (r,))) if j == i else B for j, B in enumerate(face))


def lam_faces(faces, r):
    from collections import Counter
    c = Counter()
    for f in faces:
        for i in range(len(f)):
            c[ins(f, i, r)] += 1
    return {g for g, n in c.items() if n & 1}


def first(faces, r):
    return {((r,),) + f for f in faces}


def last(faces, r):
    return {f + ((r,),) for f in faces}


def filling_chain(P6, zbits, allowed):
    """a 3-chain (set of 3-face ids of P_6) with boundary z using only 3-faces with Pref <= allowed; None if z does not bound there. Deterministic."""
    rows = [(i, b) for i, (pm, b) in zip([i for i in range(len(P6.FS)) if P6.DIM[i] == 3], P6.rows(3)) if not pm & ~allowed]
    piv = {}
    for j, (i, b) in enumerate(rows):
        x, comb = b, 1 << j
        while x:
            h = x.bit_length() - 1
            if h in piv:
                px, pc = piv[h]
                x ^= px
                comb ^= pc
            else:
                piv[h] = (x, comb)
                break
    x, comb = zbits, 0
    while x:
        h = x.bit_length() - 1
        if h not in piv:
            return None
        px, pc = piv[h]
        x ^= px
        comb ^= pc
    chain = [rows[j][0] for j in range(len(rows)) if comb >> j & 1]
    return chain


def lifted_cycle(P6, P7, z_ids, c_ids, r=None):
    r = P6.k if r is None else r
    zf = [P6.FS[g] for g in z_ids]
    cf = [P6.FS[g] for g in c_ids]
    faces = lam_faces(zf, r) ^ first(cf, r) ^ last(cf, r)
    return [P7.IDX[f] for f in faces]


def delete_rank(face, r):
    return tuple(b for b in (tuple(x for x in B if x != r) for B in face) if b)
