"""GIG-I v004 -- parametric hole-survival machinery for the common combinatorial 2-cycle z of the v003 anchors.
Everything combinatorial (z, phi, the obstructed 3-faces) is content-independent; the arithmetic enters only through D(I)."""
import json
import os
from itertools import permutations
from math import lcm
import _v3path  # noqa: F401
import history_complex as hc
import face_threshold as ft
import block_factor as bf

_CERT = os.path.join(_v3path.V003, "CERTIFICATES", "H2_anchor_A.json")


def _tf(f):
    return tuple(tuple(b) for b in f)


_FS, _VM, _DIM, _BND = hc._complex_data(6)
_IDX = {f: i for i, f in enumerate(_FS)}


def pattern():
    """(z faces, phi faces) as global face indices of P_6, loaded from the frozen v003 certificate (rank coordinates)."""
    d = json.load(open(_CERT))
    return [_IDX[_tf(f)] for f in d["z_faces"]], [_IDX[_tf(f)] for f in d["phi_support_faces"]]


Z, PHI = pattern()


def check_cycle_and_cochain():
    """combinatorial facts used by the theorem (no arithmetic): d2 z = 0 ; phi(z)=1 ; list of 3-faces F of P_6 with phi(dF) odd."""
    # d2 z = 0 over GF(2): every edge lies in an even number of z-faces
    cnt = {}
    for g in Z:
        for e in _BND[g]:
            cnt[e] = cnt.get(e, 0) ^ 1
    cyc = not any(cnt.values())
    phiS = set(PHI)
    obstructed = [i for i in range(len(_FS)) if _DIM[i] == 3 and sum(1 for b in _BND[i] if b in phiS) % 2]
    return {"z_is_cycle": cyc, "phi_of_z": len(phiS & set(Z)) % 2, "obstructed_3faces": [ _FS[i] for i in obstructed]}


def _pref_sets(face):
    return ft.pref_sets(face)


def pattern_prefix_family():
    """P_z = union of Pref(F) over faces F of supp z ; P_T[i] = Pref(T_i) for the six obstructed truncated octahedra (rank bitmasks)."""
    pz = set()
    for g in Z:
        pz |= _pref_sets(_FS[g])
    obs = check_cycle_and_cochain()["obstructed_3faces"]
    return sorted(pz), obs, [sorted(_pref_sets(t)) for t in obs]


PZ, OBS, PT = pattern_prefix_family()


def thresholds(labels, sigma=None):
    """K_z and [K_T1..K_T6] for the content `labels` (sorted list of 6) with the role->rank bijection sigma (tuple, role r -> rank sigma[r])."""
    D = bf.denominators(labels)
    if sigma is None:
        mp = lambda I: I
    else:
        def mp(I):
            J = 0
            for r in range(6):
                if I >> r & 1:
                    J |= 1 << sigma[r]
            return J
    Kz = lcm(*[D[mp(I)] for I in PZ])
    KT = [lcm(*[D[mp(I)] for I in P]) for P in PT]
    return Kz, KT


def survives(labels, m, sigma=None):
    """sufficient condition of the Parametric Survival Theorem: K_z | m and no K_T | m."""
    Kz, KT = thresholds(labels, sigma)
    return m % Kz == 0 and all(m % K for K in KT)


def hole_regime_exists(labels, sigma=None):
    """exists m with K_z | m and all K_T not dividing m  <=>  no K_T divides K_z  (take m = K_z; any multiple of K_z is only larger)."""
    Kz, KT = thresholds(labels, sigma)
    return all(Kz % K for K in KT), Kz, KT


# ---------------------------------------------------------------------------------------------- universal filling certificates
GATES = {0: [0, 1], 1: [2, 3], 3: [4, 5]}      # role a -> indices of the two obstructed truncated octahedra T_a (orderings of the last two blocks)


def guaranteed_faces(a, dim=3):
    """faces F of P_6 (given dimension) whose Pref(F) is inside P_z U Pref(T_a): they are present in X_lambda(m) for EVERY content and every m
    with K_z | m and K_{T_a} | m."""
    base = set(PZ) | set(PT[GATES[a][0]])
    return [i for i in range(len(_FS)) if _DIM[i] == dim and _pref_sets(_FS[i]) <= base]


def universal_filling(a):
    """a 3-chain c supported on guaranteed faces with boundary exactly z (over GF(2)); returns the list of face indices, or None."""
    gf = guaranteed_faces(a)
    zmask = 0
    for g in Z:
        zmask |= 1 << g
    piv = {}
    for j, fi in enumerate(gf):
        x, comb = 0, 1 << j
        for b in _BND[fi]:
            x |= 1 << b
        while x:
            h = x.bit_length() - 1
            if h in piv:
                px, pc = piv[h]
                x ^= px
                comb ^= pc
            else:
                piv[h] = (x, comb)
                break
    x, comb = zmask, 0
    while x:
        h = x.bit_length() - 1
        if h not in piv:
            return None
        px, pc = piv[h]
        x ^= px
        comb ^= pc
    chain = [gf[j] for j in range(len(gf)) if comb >> j & 1]
    # independent verification: boundary of the chain equals z
    acc = 0
    for fi in chain:
        for b in _BND[fi]:
            acc ^= 1 << b
    assert acc == zmask
    return chain


def gate_sets():
    """the 'new' prefix sets that decide each gate: P_{T_a} \\ P_z (rank bitmasks)."""
    return {a: sorted(set(PT[GATES[a][0]]) - set(PZ)) for a in GATES}


def survives_gates(labels, m, sigma=None):
    """exact form of the criterion: K_z | m and for every a in {0,1,3} some set of gate_sets()[a] has D(I) not dividing m."""
    D = bf.denominators(labels)
    if sigma is not None:
        def mp(I):
            J = 0
            for r in range(6):
                if I >> r & 1:
                    J |= 1 << sigma[r]
            return J
    else:
        mp = lambda I: I
    Kz = lcm(*[D[mp(I)] for I in PZ])
    if m % Kz:
        return False
    return all(any(m % D[mp(I)] for I in S) for S in gate_sets().values())
