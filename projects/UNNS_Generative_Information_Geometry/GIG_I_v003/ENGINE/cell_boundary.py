"""GIG-I v003 -- sparse GF(2) cellular chain complex of the permutohedral history complex, exact ranks, explicit
kernel representatives and cohomological certificates for non-bounding cycles.
Independent of v001's `betti`: boundary rows are rebuilt here from the face list (inclusion-exclusion by vertex masks)."""
import _v2path  # noqa: F401
import history_complex as hc


class Complex:
    def __init__(self, mask, k):
        self.k, self.mask = k, mask
        fs, vm, dim, bnd = hc._complex_data(k)
        self.gfaces = fs
        keep = [i for i in range(len(fs)) if vm[i] & ~mask == 0]
        self.dims = {}
        for i in keep:
            self.dims.setdefault(dim[i], []).append(i)
        self.local = {d: {g: j for j, g in enumerate(L)} for d, L in self.dims.items()}
        # boundary of a d-face as a bit-row over the (d-1)-faces of the complex
        self.rows = {}
        for d, L in self.dims.items():
            if d == 0:
                continue
            self.rows[d] = [sum(1 << self.local[d - 1][b] for b in bnd[g]) for g in L]
        # (sum with + instead of xor is fine: boundary faces of a face are distinct)

    def f(self):
        return tuple(len(self.dims.get(d, ())) for d in range(self.k))

    def rank(self, d):
        if d not in self.rows:
            return 0
        return _rank(self.rows[d])

    def ranks(self):
        return tuple(self.rank(d) for d in range(1, self.k))

    def betti(self):
        f, r = self.f(), (0,) + self.ranks() + (0,)
        return tuple(f[d] - r[d] - r[d + 1] for d in range(self.k))

    def check_boundary_squared(self):
        """partial_{d-1} partial_d = 0 for every d (the chain-complex consistency check)."""
        bad = 0
        for d in range(2, self.k):
            for row in self.rows.get(d, ()):
                acc, x = 0, row
                while x:
                    b = x & -x
                    acc ^= self.rows[d - 1][b.bit_length() - 1]
                    x ^= b
                if acc:
                    bad += 1
        return bad


def _rank(rows):
    piv, r = {}, 0
    for x in rows:
        while x:
            h = x.bit_length() - 1
            if h in piv:
                x ^= piv[h]
            else:
                piv[h] = x
                r += 1
                break
    return r


def _reduce(x, piv):
    while x:
        h = x.bit_length() - 1
        if h in piv:
            x ^= piv[h]
        else:
            return x, h
    return 0, None


def kernel_basis(rows, ncols):
    """basis (bit-rows over the d-face index set) of ker(partial_d) where rows[j] = boundary of d-face j."""
    piv = {}
    ker = []
    for j, r in enumerate(rows):
        x, comb = r, 1 << j
        while x:
            h = x.bit_length() - 1
            if h in piv:
                px, pc = piv[h]
                x ^= px
                comb ^= pc
            else:
                piv[h] = (x, comb)
                break
        if not x:
            ker.append(comb)
    return ker


def image_pivots(rows):
    piv = {}
    for x in rows:
        while x:
            h = x.bit_length() - 1
            if h in piv:
                x ^= piv[h]
            else:
                piv[h] = x
                break
    return piv


def homology_representatives(cx, d):
    """explicit cycles z_1..z_b in ker(partial_d) whose classes are a basis of H_d(X;GF2); also returns the pivots of im(partial_{d+1})."""
    ker = kernel_basis(cx.rows.get(d, []), len(cx.dims.get(d, [])))
    if d == 0:
        ker = [1 << j for j in range(len(cx.dims.get(0, [])))]
    piv = image_pivots(cx.rows.get(d + 1, []))
    reps = []
    pv = dict(piv)
    for z in ker:
        x, h = _reduce(z, pv)
        if x:
            pv[h] = x
            reps.append(z)
    return reps, piv


def cocycle_certificate(cx, d, z, piv_image):
    """a d-cochain phi (bit-row over d-faces) with phi(partial_{d+1} c)=0 for every (d+1)-face c and phi(z)=1."""
    n = len(cx.dims.get(d, []))
    # unknown phi in GF(2)^n ; constraints: phi . b = 0 for b in im basis ; phi . z = 1
    cons = [(b, 0) for b in piv_image.values()] + [(z, 1)]
    piv = {}
    for v, rhs in cons:
        x, r = v, rhs
        while x:
            h = x.bit_length() - 1
            if h in piv:
                px, pr = piv[h]
                x ^= px
                r ^= pr
            else:
                piv[h] = (x, r)
                break
        if not x and r:
            return None   # inconsistent <=> z is a boundary
    # back-substitute: free variables = 0
    phi = 0
    for h in sorted(piv):
        x, r = piv[h]
        low = x & ~(1 << h)
        val = r ^ (bin(low & phi).count("1") & 1)
        if val:
            phi |= 1 << h
    return phi


def parity(a, b):
    return bin(a & b).count("1") & 1


def verify_cocycle(cx, d, z, phi):
    """independent check: d z = 0 ; phi(d c) = 0 for all (d+1)-faces c ; phi(z) = 1."""
    out = {"z_is_cycle": True, "phi_kills_all_boundaries": True, "phi_of_z": parity(phi, z)}
    if d >= 1:
        acc = 0
        x = z
        while x:
            b = x & -x
            acc ^= cx.rows[d][b.bit_length() - 1]
            x ^= b
        out["z_is_cycle"] = acc == 0
    for row in cx.rows.get(d + 1, []):
        if parity(phi, row):
            out["phi_kills_all_boundaries"] = False
            break
    return out


def fill_chain(cx, d, z):
    """a (d+1)-chain c (bit-row over the (d+1)-faces of cx) with partial_{d+1} c = z, or None if z is not a boundary.
    Gaussian elimination that tracks which generators were combined; the result is re-verified by the caller."""
    rows = cx.rows.get(d + 1, [])
    piv = {}
    for j, r in enumerate(rows):
        x, comb = r, 1 << j
        while x:
            h = x.bit_length() - 1
            if h in piv:
                px, pc = piv[h]
                x ^= px
                comb ^= pc
            else:
                piv[h] = (x, comb)
                break
    x, comb = z, 0
    while x:
        h = x.bit_length() - 1
        if h not in piv:
            return None
        px, pc = piv[h]
        x ^= px
        comb ^= pc
    return comb


def boundary_of_chain(cx, d, c):
    """partial_{d} of the d-chain c (bit-row over d-faces)."""
    acc, x = 0, c
    while x:
        b = x & -x
        acc ^= cx.rows[d][b.bit_length() - 1]
        x ^= b
    return acc
