"""GEO-III.A/E  audits: classify every pair of cells of a fibre complex; decide whether the straight-line realization is a valid
embedded polyhedral complex (common-face property) and record exact witnesses."""
import time
from fractions import Fraction as Fr
from realization import maximal_cells, edges_of, edge_endpoints
import intersections as X


def edge_level_audit(cells, example_cap=5):
    """all pairs of edges (not only maximal ones) via exact segment relations."""
    E = [edge_endpoints(e) for e in edges_of(cells)]
    cnt = {}; examples = {}; pts = {}; pairs = set()
    order = sorted(range(len(E)), key=lambda i: min(E[i][0][0], E[i][1][0]))
    n = len(E)
    for ii in range(n):
        i = order[ii]; a = E[i]; amax = max(a[0][0], a[1][0])
        for jj in range(ii + 1, n):
            j = order[jj]; bq = E[j]
            if min(bq[0][0], bq[1][0]) > amax: break
            kind, p = X.seg_relation(a[0], a[1], bq[0], bq[1])
            if kind == 'disjoint': continue
            cnt[kind] = cnt.get(kind, 0) + 1
            if kind == 'interior_cross':
                pairs.add(frozenset((tuple(map(tuple, a)), tuple(map(tuple, bq)))))
                pts.setdefault(p, []).append((a, bq))
                if len(examples.get(kind, [])) < example_cap: examples.setdefault(kind, []).append({'edges': [a, bq], 'point': [str(c) for c in p]})
    return {'n_edges': n, 'relations': cnt, 'crossing_points': {tuple(str(c) for c in p): len(v) for p, v in pts.items()}, 'crossing_pairs': pairs, 'examples': examples}


def cell_level_audit(cells, lp_budget=30000, example_cap=5, stop_at_first=False):
    """pairs of abstract-maximal cells: disjoint / common_face / non_face.  Sufficient and necessary for embeddedness (see MATHEMATICS)."""
    mx = maximal_cells(cells)
    n = len(mx)
    boxes = [X.cell_bbox(*c) for c in mx]
    cnt = {'disjoint': 0, 'common_face': 0, 'non_face': 0}; why = {}; ex = []; dims = {}; involved = set()
    calls = 0; limited = False
    for i in range(n):
        for j in range(i + 1, n):
            bi, bj = boxes[i], boxes[j]
            if any(max(bi[0][t], bj[0][t]) > min(bi[1][t], bj[1][t]) for t in range(len(bi[0]))):
                cnt['disjoint'] += 1; continue
            A, B = mx[i], mx[j]
            if len(A[1]) == 1 and len(B[1]) == 1:
                u, (g,) = A; r, (h,) = B
                kind, p = X.seg_relation(u, X.add(u, g), r, X.add(r, h))
                if kind == 'disjoint': cnt['disjoint'] += 1
                elif kind in ('shared_endpoint', 'collinear_touch'): cnt['common_face'] += 1
                else:
                    cnt['non_face'] += 1; why[kind] = why.get(kind, 0) + 1; dims['1-1'] = dims.get('1-1', 0) + 1; involved.update((i, j))
                    if len(ex) < example_cap: ex.append({'cells': [A, B], 'why': kind})
                    if stop_at_first: return _finish(n, cnt, why, dims, ex, calls, False, True, involved, mx)
                continue
            calls += 1
            if calls > lp_budget: limited = True; break
            kind, info = X.cell_relation(A, B)
            cnt[kind] += 1
            if kind == 'non_face':
                dk = '%d-%d' % tuple(sorted((len(A[1]), len(B[1])))); dims[dk] = dims.get(dk, 0) + 1; involved.update((i, j))
                w = info.get('why', '?'); why[w] = why.get(w, 0) + 1
                if len(ex) < example_cap: ex.append({'cells': [A, B], 'why': w, 'dims': [len(A[1]), len(B[1])]})
                if stop_at_first: return _finish(n, cnt, why, dims, ex, calls, False, True, involved, mx)
        if limited: break
    return _finish(n, cnt, why, dims, ex, calls, limited, False, involved, mx)


def _finish(n, cnt, why, dims, ex, calls, limited, early, involved=None, mx=None):
    status = 'non_embedded' if cnt['non_face'] > 0 else ('resource_limited' if limited else 'embedded')
    return {'n_maximal': n, 'pairs': cnt, 'why': why, 'non_face_by_dims': dims, 'status': status, 'lp_calls': calls, 'examples': ex, 'early_exit': early,
            'maximal_by_dim': _by_dim(mx), 'involved_by_dim': _by_dim([mx[i] for i in sorted(involved)] if involved is not None else None)}


def _by_dim(cs):
    if cs is None: return None
    out = {}
    for c in cs: out[len(c[1])] = out.get(len(c[1]), 0) + 1
    return out


def audit(fc, lp_budget=30000, stop_at_first=False):
    t = time.time()
    e = edge_level_audit(fc['cells'])
    c = cell_level_audit(fc['cells'], lp_budget, stop_at_first=stop_at_first)
    return {'edge': e, 'cell': c, 'status': c['status'], 'seconds': round(time.time() - t, 2)}
