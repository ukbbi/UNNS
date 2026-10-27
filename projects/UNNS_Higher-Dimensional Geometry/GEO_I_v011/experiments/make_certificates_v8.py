"""GEO-I v008: build the shipped certificates (certificates/C1_cover.json, C2_gap.json, C3_homology.json, C4_rank.json) and verify them with certificates/checker8.py.
Deterministic; no randomness."""
import os, sys, json, itertools
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..')
for d_ in ('geometry', 'topology', 'frozen', 'theory', 'certificates'): sys.path.insert(0, os.path.join(ROOT, d_))
import cell_cover as CCv, binary_min as BM, binary_01 as B, centre_collisions as CC, rank_reduction as RR, small_box as SB
import checker8 as K


def cover_set():
    out = []
    spec = [(7, 3, (7, 9)), (7, 3, (9, 7)), (7, 3, (9, 10)), (7, 2, (8, 8)), (8, 3, (10, 11)), (9, 2, (9, 12)), (9, 4, (12, 9)), (9, 5, (11, 11)), (11, 4, (12, 13)),
            (11, 3, (14, 11)), (13, 5, (13, 14)), (13, 2, (17, 16)), (10, 3, (10, 11)), (10, 7, (11, 10))]
    for d, s, Q in spec:
        c, left = CCv.cover_certificate(d, s, Q)
        assert c is not None, ('COUNTEREXAMPLE?', d, s, Q)
        c['region'] = SB.region(d, s, Q); c['squareless'] = SB.squareless(d, s, Q); out.append(c)
    return out


def gap_set():
    out = []
    for d, s in [(5, 2), (5, 3), (6, 5), (7, 3), (8, 3), (9, 2), (10, 3), (11, 4), (12, 5), (13, 6)]:
        g = CCv.gap_certificate(d, s, (d, d), K.check_GAP); assert g is not None, (d, s); g['claim'] = 'hollow box: z in conv(F) and in no cell (G7-T3 / G8-T2 region)'; out.append(g)
    return out


def homology_set():
    return [CCv.homology_certificate(d, s, Q) for d, s, Q in [(5, 2, (5, 5)), (5, 3, (5, 5)), (5, 4, (5, 5)), (7, 3, (7, 7)), (5, 2, (5, 6)), (5, 2, (6, 5)), (7, 3, (7, 8)), (7, 3, (8, 7))]]


def rank_set():
    res = []; cls = {k: BM.classify_nullity(k) for k in (3, 4)}
    for k in (3, 4):
        for o in cls[k]['minimal_reduced_orbits']:
            sig = o['support']; p = len(sig)
            for extra in ([1] * p, [2] + [1] * (p - 1)):
                cols = BM.blowup_parity_columns(sig, extra); n = len(cols)
                if n > 10: continue
                mr = min(RR.witness_rank(n, a, b)[0] for cen, a, b in CC.collisions(cols))
                res.append({'kind': 'RANK', 'claim': 'minimal non-embedded box, minimum witness rank = min_rank; B-SERIES data', 'columns': cols, 'min_rank': mr, 'nullity': k,
                            'series_classes': p, 'reduced_support': sig, 'multiplicities': extra})
    return res


if __name__ == '__main__':
    out = os.path.join(ROOT, 'certificates')
    for name, fn in [('C1_cover.json', cover_set), ('C2_gap.json', gap_set), ('C3_homology.json', homology_set), ('C4_rank.json', rank_set)]:
        items = fn(); json.dump(items, open(os.path.join(out, name), 'w'))
        bad = [(i, K.KINDS[c['kind']](c)) for i, c in enumerate(items) if not K.KINDS[c['kind']](c)[0]]
        print(name, len(items), 'invalid:', bad)
