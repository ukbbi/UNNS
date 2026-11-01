"""GEO_HD_BRIDGE v005 -- A5-T4/T7: census of ALL D-events (not only step activations) on FIELD-I orbits, with the transition calculus.
Same regime as the v004 scan: modulus l in {5,7,11,13}, S<1500 in the modular class, 24 steps from x = S^2/l."""
import _paths, json, sys, time
from fractions import Fraction as Fr
from collective_regimes import in_class
from geo1lib import fibre_q, Lof, Gof
from transition_calculus import analyse_transition, event_type

def run(ls=(5, 7, 11, 13), Smax=1500, nsteps=24, budget=3000):
    t0 = time.time(); rows = []
    for l in ls:
        for S in range(2, Smax):
            if time.time() - t0 > budget: break
            if not in_class(S, l): continue
            cur = Fr(S * S, l); Ds = []
            for n in range(nsteps + 1):
                D = fibre_q(cur); Ds.append(frozenset(D))
                if not D: break
                cur = cur + Fr(Lof(D) ** 2, Gof(D))
            for n in range(len(Ds) - 1):
                if Ds[n] != Ds[n + 1]:
                    t = analyse_transition(sorted(Ds[n]), sorted(Ds[n + 1]))
                    rows.append({'l': l, 'S': S, 'n': n, 'nD': len(Ds[n]), 'nD2': len(Ds[n + 1]), 'nnew': len(t['newv']),
                                 'betti': t['betti'], 'betti2': t['betti2'], 'delta': t['delta'], 'f': t['f'], 'f2': t['f2'],
                                 'dead': t['dead'], 'new': t['new'], 'surv': t['surv'], 'type': event_type(t),
                                 'formula_ok': t['formula_ok'], 'recK_ok': t['recK_ok'] and t['recK2_ok'],
                                 'lemmas_ok': all(t['lemmas'].values()), 'nec_ok': all(t['nec'].values()), 'comp': list(t['comp'])})
    return rows

if __name__ == '__main__':
    out = sys.argv[1]; rows = run(budget=int(sys.argv[2]) if len(sys.argv) > 2 else 3000)
    json.dump(rows, open(out, 'w')); print(len(rows))
