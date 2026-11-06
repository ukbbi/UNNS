"""GIG-I v005 -- exact bounding lattice for the common 2-cycle z in P_6.
Faces of X(m) are those F of P_6 with Pref(F) inside the admissible family A(m) (T16/T17). With K_z | m the family contains P_z, so
the only freedom is S = A \\ P_z, a subset of the 20 remaining prefix sets. z bounds in X(m) iff z is in the GF(2) span of d3 of the present 3-faces."""
import _v4path  # noqa: F401
import hole_survival as H

PZ = set(H.PZ)
EXTRA = sorted(set(s for f in H._FS for s in H._pref_sets(f)) - PZ)     # 20 sets
BIT = {s: i for i, s in enumerate(EXTRA)}
ZMASK = 0
for g in H.Z:
    ZMASK |= 1 << g
FACES3 = []                                                              # (requirement mask over EXTRA, boundary bitmask)
for i, f in enumerate(H._FS):
    if H._DIM[i] != 3:
        continue
    P = set(H._pref_sets(f))
    if not P <= PZ | set(EXTRA):
        raise RuntimeError
    r = 0
    for s in P - PZ:
        r |= 1 << BIT[s]
    b = 0
    for e in H._BND[i]:
        b |= 1 << e
    FACES3.append((r, b))


def bounds(S):
    """S: bitmask over EXTRA of admissible extra prefix sets (P_z assumed admissible). True iff z is a boundary of present 3-faces."""
    piv = {}
    for r, b in FACES3:
        if r & ~S:
            continue
        x = b
        while x:
            h = x.bit_length() - 1
            if h in piv:
                x ^= piv[h]
            else:
                piv[h] = x
                break
    x = ZMASK
    while x:
        h = x.bit_length() - 1
        if h not in piv:
            return False
        x ^= piv[h]
    return True
