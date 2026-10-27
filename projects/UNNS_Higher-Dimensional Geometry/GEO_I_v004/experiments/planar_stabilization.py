"""Programme A (G4-C1).  For every k=2 relation lattice Lambda(o1,o2,d,s) with o_i <= OMAX and every box in a window around q_i = o_i,
compute beta_*(U) exactly.  usage: planar_stabilization.py OMIN OMAX DQ_LO DQ_HI OUT   (boxes q_i in [o_i+DQ_LO, o_i+DQ_HI])"""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'theory'))
from lattice_model import *

def run(omin, omax, lo, hi, out, only_new=True):
    t0 = time.time(); n = 0
    with open(out, 'w') as f:
        for L in lattices(omax, 1):
            if L.o2 < omin and L.o1 < omin: continue
            if max(L.o1, L.o2) < omin: continue
            for q1 in range(max(1, L.o1 + lo), L.o1 + hi + 1):
                for q2 in range(max(1, L.o2 + lo), L.o2 + hi + 1):
                    t = time.time(); b, info = U_betti(L, (q1, q2))
                    if b is None: continue
                    n += 1
                    f.write(json.dumps({'o': [L.o1, L.o2], 'd': L.d, 's': L.s, 'q': [q1, q2], 'betti_U': b, 'R': info['R'], 'cover': info['cover'], 't': round(time.time() - t, 2)}) + '\n')
            f.flush()
    return n, time.time() - t0

if __name__ == '__main__':
    omin, omax, lo, hi, out = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    print(run(omin, omax, lo, hi, out))


def run_window(omax, mult_hi, out, shard=0, nshard=1, dmin=2, lo_off=1, omin=1):
    """strict window  o_i + lo_off <= q_i <= mult_hi*o_i + 1, lattices with d >= dmin, o2 in [omin, omax]; shard by lattice index."""
    t0 = time.time(); n = 0
    Ls = [L for L in lattices(omax, 1) if L.d >= dmin and L.o2 >= omin]
    with open(out, 'w') as f:
        for i, L in enumerate(Ls):
            if i % nshard != shard: continue
            for q1 in range(L.o1 + lo_off, mult_hi * L.o1 + 2):
                for q2 in range(L.o2 + lo_off, mult_hi * L.o2 + 2):
                    t = time.time(); b, info = U_betti(L, (q1, q2))
                    if b is None: continue
                    n += 1
                    f.write(json.dumps({'o': [L.o1, L.o2], 'd': L.d, 's': L.s, 'q': [q1, q2], 'betti_U': b, 'R': info['R'], 'cover': info['cover'], 't': round(time.time() - t, 2)}) + '\n')
            f.flush()
    return n, time.time() - t0


def offsets_for(a):
    return sorted(set(list(range(1, a + 2)) + [2 * a, 2 * a + 1]))


def run_targeted(omin, omax, out, shard=0, nshard=1):
    """boxes q_i = o_i + e_i with e_i in {1..a_i+1} u {2a_i, 2a_i+1}  (a_i = o_i/d): tests the stabilization threshold law."""
    n = 0; t0 = time.time()
    Ls = [L for L in lattices(omax, 1) if L.d >= 2 and L.o2 >= omin]
    with open(out, 'w') as f:
        for i, L in enumerate(Ls):
            if i % nshard != shard: continue
            for e1 in offsets_for(L.a):
                for e2 in offsets_for(L.c):
                    q = (L.o1 + e1, L.o2 + e2)
                    t = time.time(); b, info = U_betti(L, q)
                    if b is None: continue
                    n += 1
                    f.write(json.dumps({'o': [L.o1, L.o2], 'd': L.d, 's': L.s, 'a': L.a, 'c': L.c, 'e': [e1, e2], 'q': list(q), 'betti_U': b, 'R': info['R'], 'cover': info['cover'], 't': round(time.time() - t, 2)}) + '\n')
            f.flush()
    return n, time.time() - t0
