"""G6-C1 / E1: general-s stabilization beyond d = 21.
For every type (d,s) (s <= s^-1 mod d, i.e. up to the transposition symmetry) with DMIN <= d <= DMAX:
  (a) SMALL BOXES (the only boxes not covered by the proved theorems G6-T1a/b): every Q = (d+r1,d+r2), 0<=r_i<d, Q != (d,d)
      certified by the exact sufficient-family test (theory/small_boxes.py), with the generic v005 test as fallback;
  (b) PROOF-CELL AUDIT of the theorems: NSAMPLE deterministic boxes with max(Q1,Q2) >= 2d are checked by the cell list of the proof
      (theory/modular_layers.py), exact;
  (c) GENERIC AUDIT (independent implementation = v005 test over *all* cells): NGENERIC deterministic boxes per type, only for d <= GENERIC_DMAX.
Output: one JSON row per finished type; resumable.  A box that cannot be decided is recorded as 'unresolved' (never counted as passed).
usage: general_s.py DMIN DMAX OUT.jsonl [SHARD NSHARD] [--nsample N] [--ngeneric N] [--generic-dmax D]"""
import os, sys, json, time, random
HERE = os.path.dirname(os.path.abspath(__file__))
for d_ in ('geometry', 'topology', 'frozen', 'theory'): sys.path.insert(0, os.path.join(HERE, '..', d_))
from math import gcd
from small_boxes import certify_box
import modular_layers as ML


def inv(s, d): return next(t for t in range(1, d + 1) if (s * t) % d == 1 % d)


def types(dmin, dmax):
    for d in range(dmin, dmax + 1):
        for s in range(1, d):
            if gcd(s, d) == 1 and inv(s, d) >= s: yield d, s


def run_type(d, s, nsample, ngeneric, gdmax):
    t0 = time.time(); row = {'d': d, 's': s, 't': inv(s, d)}
    ok = 0; fb = 0; bad = []
    sym = inv(s, d) == s
    for r1 in range(d):
        for r2 in range(d):
            if (r1, r2) == (0, 0) or (sym and r2 < r1): continue
            res = certify_box(d, s, (d + r1, d + r2))
            if res['ok']: ok += 1; fb += res['method'] != 'family'
            else: bad.append(res)
    row.update({'small_boxes_certified': ok, 'small_boxes_via_fallback': fb, 'small_boxes_unresolved_or_violated': bad[:5], 'n_bad': len(bad)})
    rng = random.Random(1000003 * d + s)
    pa = 0; pb = []
    for _ in range(nsample):
        reg = rng.choice(['thick', 'thin_x', 'thin_y'])
        if reg == 'thick': Q = (rng.randint(2 * d, 4 * d), rng.randint(2 * d, 4 * d))
        elif reg == 'thin_x': Q = (rng.randint(d, 2 * d - 1), rng.randint(2 * d, 4 * d))
        else: Q = (rng.randint(2 * d, 4 * d), rng.randint(d, 2 * d - 1))
        r = ML.verify_box(d, s, Q)
        if r['ok']: pa += 1
        else: pb.append(r)
    row.update({'proof_cell_audit_ok': pa, 'proof_cell_audit_bad': pb[:3], 'n_proof_audit': nsample})
    if d <= gdmax and ngeneric:
        import coverage as C
        from lattice_model import Lat
        L = Lat(d, d, d, s); ga = 0; gb = []
        for _ in range(ngeneric):
            Q = (rng.randint(d, 2 * d + 1), rng.randint(d, 2 * d + 1))
            if Q == (d, d): continue
            u = C.uncovered(L, Q)
            if u is not None and len(u) == 0: ga += 1
            else: gb.append(list(Q))
        row.update({'generic_audit_ok': ga, 'generic_audit_bad': gb, 'n_generic_audit': ngeneric})
    row['seconds'] = round(time.time() - t0, 1)
    return row


if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    opt = {}
    args = sys.argv[1:]
    for i, x in enumerate(args):
        if x.startswith('--') and i + 1 < len(args): opt[x] = args[i + 1]
    a = [x for i, x in enumerate(args) if not x.startswith('--') and not (i > 0 and args[i - 1].startswith('--'))]
    dmin, dmax, out = int(a[0]), int(a[1]), a[2]; sh, ns = (int(a[3]), int(a[4])) if len(a) > 4 else (0, 1)
    nsample = int(opt.get('--nsample', 30)); ngeneric = int(opt.get('--ngeneric', 6)); gdmax = int(opt.get('--generic-dmax', 24))
    done = set()
    if os.path.exists(out): done = {(json.loads(l)['d'], json.loads(l)['s']) for l in open(out)}
    with open(out, 'a') as f:
        for k, (d, s) in enumerate(types(dmin, dmax)):
            if k % ns != sh or (d, s) in done: continue
            f.write(json.dumps(run_type(d, s, nsample, ngeneric, gdmax)) + '\n'); f.flush()
