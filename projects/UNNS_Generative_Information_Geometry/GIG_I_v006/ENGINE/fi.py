"""GIG-I v006 -- exact GF(2) tools for filling-independence.
Bounder(pk, allowed, d): pivot table of the boundaries of (d+1)-faces F of pk with Pref(F) <= allowed; .contains(zbits) tests z in span, .express(zbits) returns the 4-chain (face ids) or None.
cycle_basis(pk, allowed, d): basis (list of bitmasks over global face ids) of the d-cycles of the complex K(allowed) = faces with Pref <= allowed.
chain helpers: first_bits / last_bits / lam_bits embed a P_6 chain (bitmask over P6 ids) into P_7 (new rank 6)."""
import _vpath  # noqa: F401
import lift as Lf


class Bounder:
    def __init__(self, pk, allowed, d):
        self.pk, self.faces = pk, []
        self.piv = {}
        for fid, (pm, b) in zip([i for i in range(len(pk.FS)) if pk.DIM[i] == d + 1], pk.rows(d + 1)):
            if pm & ~allowed:
                continue
            j = len(self.faces)
            self.faces.append(fid)
            x, comb = b, 1 << j
            while x:
                h = x.bit_length() - 1
                if h in self.piv:
                    px, pc = self.piv[h]
                    x ^= px
                    comb ^= pc
                else:
                    self.piv[h] = (x, comb)
                    break

    def express(self, zbits):
        x, comb = zbits, 0
        while x:
            h = x.bit_length() - 1
            if h not in self.piv:
                return None
            px, pc = self.piv[h]
            x ^= px
            comb ^= pc
        return [self.faces[j] for j in range(len(self.faces)) if comb >> j & 1]

    def contains(self, zbits):
        return self.express(zbits) is not None


def cycle_basis(pk, allowed, d):
    """kernel of the boundary map on d-faces with Pref <= allowed (GF(2))."""
    ids = [i for i in range(len(pk.FS)) if pk.DIM[i] == d and not pk.PM[i] & ~allowed]
    piv, basis = {}, []
    for i in ids:
        x = 0
        for b in pk.BND[i]:
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


def ids_of(bits):
    out, i = [], 0
    while bits:
        l = bits & -bits
        out.append(l.bit_length() - 1)
        bits ^= l
    return out


def embed(P6, P7, bits6, kind, r=6):
    fs = [P6.FS[g] for g in ids_of(bits6)]
    if kind == "first":
        s = Lf.first(fs, r)
    elif kind == "last":
        s = Lf.last(fs, r)
    elif kind == "lam":
        s = Lf.lam_faces(fs, r)
    else:
        raise ValueError(kind)
    return P7.bits([P7.IDX[f] for f in s])


def prefix_union(pk, bits):
    return pk.pz(bits)
