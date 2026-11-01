"""HD-1D v001 builder: writes data/*.json and results/ROUTE_INVARIANTS.json, COUNTEREXAMPLES.json. Usage: python build_data.py [stage]
stages: b1 b2 b3 b4 b5 census r4"""
import sys, os, json, time
from math import comb
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); sys.path.insert(0, HERE)
from select_history import *
from predecessor_count import H, H_from
from diamond_criterion import *
from route_complex import *
from history_events import *
from merge_obstructions import *


def dump(rel, obj):
    with open(os.path.join(ROOT, rel), 'w') as f:
        json.dump(obj, f, indent=1, default=lambda x: list(x) if isinstance(x, (set, tuple)) else str(x))


def hist_record(h):
    m0, L = h; st = run(m0, L)
    return dict(source=m0, labels=list(L), states=st, fibres=[list(fibre(m)) for m in st], events=birth_loss(h), content=list(content(h)))


def stage_b1():
    m = 6
    succ = successors(m)
    pairs = {}
    divs = admissible_labels(m)
    for i, A in enumerate(divs):
        for B in divs[i + 1:]:
            pairs["%d,%d" % (A, B)] = classify(m, A, B)
    bound = 10 ** 6
    reach = {t: reach_plus(t, bound) for _, t in succ}
    cf = {}
    ts = [t for _, t in succ]
    for i, a in enumerate(ts):
        for b in ts[i + 1:]:
            c = sorted(reach[a] & reach[b])
            cf["%d,%d" % (a, b)] = dict(count_in_bound=len(c), smallest=c[:5], bound=bound, note="BOUNDED enumeration; states <= bound only")
    cont = {str(t): [dict(label=N, state=u) for N, u in successors(t)] for _, t in succ}
    dump('data/D_B1_6.json', dict(state=6, immediate=[dict(label=N, state=t) for N, t in succ], label_pairs_at_6=pairs, continuations=cont, pairwise_common_futures_of_successors=cf,
                                   verified_transitions=[24, 27, 32, 49]))


def stage_b2():
    hs = sorted(complete_histories(72)); cl = swap_classes(hs)
    cls = {h: i for i, c in enumerate(cl) for h in c}
    rec = []
    for h in hs:
        r = hist_record(h); r['swap_class'] = cls[h]; r['rho'] = {str(d): list(v) for d, v in signature_table(h).items()}
        rec.append(r)
    dump('data/D_B2_72.json', dict(endpoint=72, H=H(72), histories=rec, swap_classes=[[list(map(str, h)) for h in c] for c in cl],
                                   note="h1,h2 (source 1) are swap-equivalent at state 4 (2 | 4); h3,h4 have other sources and other contents"))


def stage_b3():
    rows = []
    for r in range(1, 7):
        t = 72 ** r
        rows.append(dict(r=r, H=H(t), H_from_root_1=H_from(t, 1), binom_2r_r=comb(2 * r, r), lower_bound_holds=H(t) >= comb(2 * r, r), binomial_family_all_admissible=all(is_admissible(*h) and endpoint(*h) == t for h in binomial_family(r)) if r <= 8 else None))
    detail = {}
    for r in (1, 2, 3):
        hs = list(complete_histories(72 ** r)); cl = swap_classes(hs)
        cd = Counter(cube_dim(h) for h in hs)
        grp = defaultdict(int)
        for c in cl: grp[(c[0][0], content(c[0]))] += 1
        detail[str(r)] = dict(histories=len(hs), swap_classes=len(cl), source_content_groups=len(grp), split_groups=sum(1 for v in grp.values() if v > 1),
                              cube_dim_distribution=dict(sorted(cd.items())), max_cube_dim=max(cd), class_sizes=dict(sorted(Counter(len(c) for c in cl).items())))
    fam = []
    for r in range(1, 9):
        base, pos = route_cube_family(r)
        fam.append(dict(r=r, base=[base[0], list(base[1])], positions=pos, cube_verified=verify_cube(base, pos), endpoint_is_72_pow_r=endpoint(*base) == 72 ** r, vertices=2 ** r))
    dump('data/D_B3_72_POWERS.json', dict(table=rows, detail=detail, route_cube_family=fam,
          note="H(72^r) from the predecessor recurrence; r>=4 not enumerated explicitly except via census stage r4"))


def stage_b4():
    cnt = Counter(); ex = {}
    for m in range(1, 121):
        for A in range(1, 41):
            for B in range(A + 1, 41):
                c = classify(m, A, B); cnt[c] += 1
                assert (c == 'DIAMOND') == diamond_direct(m, A, B)
                ex.setdefault(c, []).append((m, A, B)) if len(ex.get(c, [])) < 4 else None
    # pairwise vs product
    pw = []
    for m in range(1, 400):
        ds = admissible_labels(m)
        for i, A in enumerate(ds):
            for B in ds[i + 1:]:
                if not diamond(m, A, B): continue
                for C in ds:
                    if C > B and diamond(m, A, C) and diamond(m, B, C) and not all_arrangements_ok(m, (A, B, C)):
                        pw.append((m, A, B, C))
    hexa = []
    for m in range(2, 40):
        for a in admissible_labels(m):
            m1 = T(a, m)
            for b in admissible_labels(m1):
                if b == a: continue
                m2 = T(b, m1)
                for c in admissible_labels(m2):
                    if c in (a, b): continue
                    ok = hexagon_failures(m, (a, b, c))
                    if ok is not None and len(ok) < 6:
                        hexa.append(dict(source=m, history=[a, b, c], admissible_arrangements=[list(p) for p in ok]))
                        break
                else: continue
                break
            if len(hexa) > 12: break
    dump('data/D_B4_DIAMONDS.json', dict(classification_counts=dict(cnt), examples={k: v for k, v in ex.items()}, scope="m<=120, A<B<=40",
         pairwise_diamonds_without_triple_cell=dict(count=len(pw), first=pw[:10], scope="m<400"), overlapping_swap_hexagon_failures=hexa[:12],
         disjoint_swaps_always_complete="proved (Independence Lemma); see THEOREMS.md D-T3"))


def stage_b5():
    bound = 20000
    states = list(range(1, 41))
    R = {a: reach_plus(a, bound) for a in states}
    none = []
    for i, a in enumerate(states):
        for b in states[i + 1:]:
            if not (R[a] & R[b]) and a not in R[b] and b not in R[a]:
                none.append((a, b))
    dump('data/D_B5_FUTURES.json', dict(bound=bound, states=[1, 40], pairs_without_common_future_in_bound=none, n_pairs=len(none),
         note="BOUNDED: reach sets truncated at the bound; absence in bound is NOT an obstruction theorem. Retained as regression data only."))


def stage_census():
    rows = []; split_ex = []; tot = 0; t0 = time.time()
    maxH = 4000
    for t in range(4, 6001):
        if is_squarefree(t): continue
        h = H(t)
        if h > maxH: continue
        hs = list(complete_histories(t)); cl = swap_classes(hs)
        grp = defaultdict(int)
        for c in cl: grp[(c[0][0], content(c[0]))] += 1
        sp = [k for k, v in grp.items() if v > 1]
        tot += 1
        rows.append((t, h, len(cl), len(grp), len(sp), max(cube_dim(x) for x in hs)))
        if sp and len(split_ex) < 40: split_ex.append(dict(endpoint=t, source=sp[0][0], content=list(sp[0][1])))
    dump('results/ROUTE_INVARIANTS.json', dict(scope="non-squarefree t in [4,6000] with H(t)<=%d" % maxH, endpoints=tot,
         with_split_content=sum(1 for r in rows if r[4]), split_endpoints=[r[0] for r in rows if r[4]], split_examples=split_ex,
         max_cube_dim_over_endpoints=max(r[5] for r in rows), max_cube_dim_endpoint=[r[0] for r in rows if r[5] == max(x[5] for x in rows)][:10],
         table_columns=["t", "H", "swap_classes", "source_content_groups", "split_groups", "max_cube_dim"], table=rows, seconds=round(time.time() - t0)))


def stage_r4():
    t0 = time.time(); t = 72 ** 4
    hs = list(complete_histories(t))
    cd = Counter(cube_dim(h) for h in hs)
    dump('results/R4_CUBE_DIMENSIONS.json', dict(endpoint=t, histories=len(hs), cube_dim_distribution=dict(sorted(cd.items())), max_cube_dim=max(cd), seconds=round(time.time() - t0)))


if __name__ == '__main__':
    stages = sys.argv[1:] or ['b1', 'b2', 'b3', 'b4', 'b5']
    for s in stages:
        t = time.time(); globals()['stage_' + s](); print('stage', s, 'done', round(time.time() - t, 1), flush=True)
