"""GIG-I v004 -- parametric survival machinery for the combinatorial 3-cycles z3 of the k=7 beta_3 regimes (certificates H3_*.json of this release).
z3 and phi3 are combinatorial objects of P_7; the arithmetic enters only through D(I)."""
import json
import os
from math import lcm
import _v3path  # noqa: F401
import history_complex as hc
import face_threshold as ft
import block_factor as bf

_FS, _VM, _DIM, _BND = hc._complex_data(7)
_IDX = {f: i for i, f in enumerate(_FS)}
_CERTS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "CERTIFICATES")


def _tf(f):
    return tuple(tuple(b) for b in f)


class Pattern:
    def __init__(self, case):
        d = json.load(open(os.path.join(_CERTS, "H3_%s.json" % case)))
        self.case = case
        self.Z = [_IDX[_tf(f)] for f in d["z3_faces"]]
        self.PHI = [_IDX[_tf(f)] for f in d["phi3_faces"]]
        phiS = set(self.PHI)
        cnt = {}
        for g in self.Z:
            for e in _BND[g]:
                cnt[e] = cnt.get(e, 0) ^ 1
        self.z_is_cycle = not any(cnt.values())
        self.phi_of_z = len(phiS & set(self.Z)) % 2
        self.obstructed = [i for i in range(len(_FS)) if _DIM[i] == 4 and sum(1 for b in _BND[i] if b in phiS) % 2]
        self.PZ = set()
        for g in self.Z:
            self.PZ |= ft.pref_sets(_FS[g])
        self.PT = [ft.pref_sets(_FS[i]) for i in self.obstructed]
        # the two orderings of the last blocks give the same 'new' sets: group the 6 obstructed faces by their first block
        self.gate_sets = {}
        for i, P in zip(self.obstructed, self.PT):
            self.gate_sets.setdefault(tuple(_FS[i][0]), sorted(P - self.PZ))

    def thresholds(self, labels):
        D = bf.denominators(labels)
        Kz = lcm(*[D[I] for I in self.PZ])
        return Kz, D

    def hole_regime_exists(self, labels):
        """exists m (take m = K_z3) with K_z3 | m and every gate closed (some new set I with D(I) not dividing m)."""
        Kz, D = self.thresholds(labels)
        return all(any(Kz % D[I] for I in S) for S in self.gate_sets.values()), Kz

    def survives(self, labels, m):
        Kz, D = self.thresholds(labels)
        return m % Kz == 0 and all(any(m % D[I] for I in S) for S in self.gate_sets.values())
