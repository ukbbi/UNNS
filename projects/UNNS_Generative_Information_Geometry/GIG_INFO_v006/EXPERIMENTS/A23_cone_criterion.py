"""A23 -- local criterion test: a hollow triangle of N[D] is 'coned' if some d in D\\{a,b,c} makes {a,b,d},{a,c,d},{b,c,d} faces of N.  A coned triangle bounds.  Does 'not coned' <=> 'non-bounding'?
Also: the positives with no non-bounding hollow triangle -- shortest non-bounding cycle (fundamental cycles of a BFS forest)."""
import itertools, json, os, random
from collections import Counter, deque
import _path, v2, nerve
import A21_motifs as M
from A20_load_positives import load_positives

def face(S):
    return any(all(x in nerve.COMP[z] for x in S) for z in nerve.SUBS)

def coned(t, D):
    a, b, c = t
    return any(d not in t and face((a, b, d)) and face((a, c, d)) and face((b, c, d)) for d in D)

def shortest_nonbounding(D):
    Dl, edges, tris = nerve.nerve_complex(D)
    B = nerve.Bounder(D)
    adj = {v: [] for v in Dl}
    for a, b in edges: adj[a].append(b); adj[b].append(a)
    best = None
    for root in Dl:
        par = {root: None}; dep = {root: 0}; q = deque([root])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if v not in par: par[v] = u; dep[v] = dep[u] + 1; q.append(v)
        tree = {(min(v, p), max(v, p)) for v, p in par.items() if p is not None}
        for a, b in edges:
            if (a, b) in tree or a not in par or b not in par: continue
            pa, pb = [a], [b]
            while pa[-1] != root: pa.append(par[pa[-1]])
            while pb[-1] != root: pb.append(par[pb[-1]])
            # remove common suffix
            while len(pa) > 1 and len(pb) > 1 and pa[-2] == pb[-2]: pa.pop(); pb.pop()
            cyc = pa + pb[-2::-1]
            if len(set(cyc)) != len(cyc) or len(cyc) < 3: continue
            if best is not None and len(cyc) >= len(best): continue
            if not B.bounds(cyc): best = cyc
    return best

if __name__ == "__main__":
    P, F, REGS = load_positives()
    rng = random.Random(20261122)
    neg = rng.sample([i for i in range(len(REGS)) if F["beta2"][i] == 0 and REGS[i][3] != (1 << 720) - 1], 400)
    out = {}
    for tag, items in (("positives", P), ("negatives", [{"mask": REGS[i][3], "src": "D", "idx": i, "content": tuple(REGS[i][0])} for i in neg])):
        c = Counter()
        exceptional = []
        for p in items:
            D = nerve.dead_sets(p["mask"]); B = nerve.Bounder(D)
            ht = M.hollow_triangles(D)
            anynb = False
            for t in ht:
                nb = not B.bounds(t); cn = coned(t, D)
                c[("nonbounding" if nb else "bounding", "coned" if cn else "uncone")] += 1
                anynb |= nb
            c["systems"] += 1
            if tag == "positives" and not anynb:
                cyc = shortest_nonbounding(D)
                exceptional.append({"src": p["src"], "idx": p["idx"], "content": list(p["content"]), "L": p.get("L"), "N": p.get("N"), "D": [nerve.label_set(x, p["content"]) for x in sorted(D)], "shortest_nonbounding_cycle_len": None if cyc is None else len(cyc), "cycle": None if cyc is None else [nerve.label_set(x, p["content"]) for x in cyc]})
        out[tag] = {"counts": {f"{k[0]}|{k[1]}" if isinstance(k, tuple) else k: v for k, v in c.items()}, "exceptional_positives_without_hollow_triangle_nonbounding": exceptional}
        print(tag, out[tag], flush=True)
    json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "A23_cone_criterion.json"), "w"), indent=1)
