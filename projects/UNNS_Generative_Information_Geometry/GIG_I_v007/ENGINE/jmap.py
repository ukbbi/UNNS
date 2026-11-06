"""GIG-I v007 -- the filling-dependence map J_X.
For an admissible set A (prefix-set mask in P_{k+1}) and base pk (P_k), lift index r=k:  V_X = { d in Z_j(P_k) : first(d) in C_j(K(A)) },  J_X(d) = [first(d)] in H_j(K(A)).
r_fill(X) = dim im J_X.  Everything is GF(2) linear algebra on python ints."""
import _vpath  # noqa: F401
import lift as Lf
import fi


def first_ok_faces(Pk, Pk1, d, A, kind="first"):
    """ids of d-faces f of Pk with Pref(first(f)) <= A (kind='last': Pref(last(f)) <= A)."""
    out = []
    for i in range(len(Pk.FS)):
        if Pk.DIM[i] != d:
            continue
        g = Pk1.IDX[((Pk.k,),) + Pk.FS[i]] if kind == "first" else Pk1.IDX[Pk.FS[i] + ((Pk.k,),)]
        if not Pk1.PM[g] & ~A:
            out.append(i)
    return out


def kernel(Pk, ids, d):
    piv, basis = {}, []
    for i in ids:
        x = 0
        for b in Pk.BND[i]:
            x ^= 1 << b
        comb = 1 << i
        while x:
            h = x.bit_length() - 1
            if h in piv:
                px, pc = piv[h]
                x ^= px
                comb ^= pc
            else:
                piv[h] = (x, comb)
                break
        if x == 0:
            basis.append(comb)
    return basis


def reduce_mod(B, x):
    """reduce x by the pivot table of fi.Bounder B (leading-bit reduction)."""
    while x:
        h = x.bit_length() - 1
        if h in B.piv:
            x ^= B.piv[h][0]
        else:
            break
    return x


def rank_mod_boundaries(B, vecs):
    """dim of span(vecs) modulo the boundary space held by Bounder B; also returns the indices of a maximal independent subfamily."""
    piv, keep = {}, []
    for k, v in enumerate(vecs):
        x = v
        while x:
            # full reduction by B then by piv
            h = x.bit_length() - 1
            if h in B.piv:
                x ^= B.piv[h][0]
            elif h in piv:
                x ^= piv[h]
            else:
                piv[h] = x
                keep.append(k)
                break
    return len(piv), keep


def J_rank(Pk, Pk1, A, d, kind="first"):
    ids = first_ok_faces(Pk, Pk1, d, A, kind)
    basis = kernel(Pk, ids, d)
    B = fi.Bounder(Pk1, A, d)
    vecs = [fi.embed(Pk, Pk1, b, kind, r=Pk.k) for b in basis]
    r, keep = rank_mod_boundaries(B, vecs)
    # beta_d of the facet complex F_X = span of the faces ids (cells of Pk whose first/last image is admitted): dim Z_d - rank d_{d+1}
    okset = set(ids)
    up = [i for i in range(len(Pk.FS)) if Pk.DIM[i] == d + 1 and (Pk1.PM[Pk1.IDX[((Pk.k,),) + Pk.FS[i]] if kind == "first" else Pk1.IDX[Pk.FS[i] + ((Pk.k,),)]] & ~A) == 0]
    piv = {}
    rk = 0
    for i in up:
        x = 0
        for b in Pk.BND[i]:
            x ^= 1 << b
        while x:
            h = x.bit_length() - 1
            if h in piv:
                x ^= piv[h]
            else:
                piv[h] = x
                rk += 1
                break
    return {"faces_ok": len(ids), "dim_V": len(basis), "r_fill": r, "dim_ker": len(basis) - r, "beta_facet": len(basis) - rk, "basis": basis, "keep": keep}
