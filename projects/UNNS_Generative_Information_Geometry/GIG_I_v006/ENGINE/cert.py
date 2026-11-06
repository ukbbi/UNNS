"""GIG-I v006 -- explicit cycle/cochain certificates over GF(2).
cochain_certificate(pk, allowed, d, zbits): a d-cochain phi (set of d-face ids) with  phi(z) = 1  and  phi(boundary f) = 0  for EVERY (d+1)-face f whose prefix sets lie in `allowed`.  Returns None iff z bounds in K(allowed).
verify_certificate(pk, allowed, d, zbits, phi): independent check (no elimination): z is a d-cycle, its faces lie in K(allowed), phi(z) odd, and every admitted (d+1)-face has even phi-boundary."""
import _vpath  # noqa: F401




def solve(pk, allowed, d, zbits):
    rows = [b for pm, b in pk.rows(d + 1) if not pm & ~allowed]
    # compact variable set: d-faces occurring in an admitted boundary or in z
    var = {}
    def comp(x):
        out = 0
        while x:
            l = x & -x
            g = l.bit_length() - 1
            if g not in var:
                var[g] = len(var)
            out |= 1 << var[g]
            x ^= l
        return out
    eqs = [(comp(b), 0) for b in rows] + [(comp(zbits), 1)]
    piv = {}
    for m, r in eqs:
        while m:
            h = m.bit_length() - 1
            if h in piv:
                pm, pr = piv[h]
                m ^= pm
                r ^= pr
            else:
                piv[h] = (m, r)
                break
        if m == 0 and r == 1:
            return None
    phi = 0
    for h in sorted(piv):
        m, r = piv[h]
        rest = m ^ (1 << h)
        val = r ^ (bin(rest & phi).count("1") & 1)
        if val:
            phi |= 1 << h
    inv = {v: g for g, v in var.items()}
    ids, x = [], phi
    while x:
        l = x & -x
        ids.append(inv[l.bit_length() - 1])
        x ^= l
    return sorted(ids)


def verify_certificate(pk, allowed, d, zbits, phi_ids):
    phi = set(phi_ids)
    if not pk.is_cycle(zbits):
        return False, "not a cycle"
    if pk.pz(zbits) & ~allowed:
        return False, "cycle has a face outside K(allowed)"
    zi = [g for g in range(len(pk.FS)) if zbits >> g & 1] if len(pk.FS) < 10**6 else None
    if sum(1 for g in zi if g in phi) % 2 != 1:
        return False, "phi(z) is even"
    for i in range(len(pk.FS)):
        if pk.DIM[i] == d + 1 and not pk.PM[i] & ~allowed:
            if sum(1 for b in pk.BND[i] if b in phi) % 2:
                return False, "admitted face %d has odd phi-boundary" % i
    return True, "ok"
