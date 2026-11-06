"""A25 -- numerical check of the star-intersection lemma used in T-NERVE:
for any T of proper nonempty subsets of [6], Q_T = {x proper nonempty: x comparable to every t in T} is empty or Delta(Q_T) is contractible (here: acyclic over GF(2), all dimensions).
Exhaustive for |T|<=2, random for larger T (the proof is in THEORY/THEOREMS.md)."""
import itertools, json, os, random, time
import _path, nerve, forbidden as fb

def order_complex_sim(Q):
    Q = sorted(Q, key=lambda x: (bin(x).count("1"), x))
    sim = {}
    def rec(chain, cands):
        for i, x in enumerate(cands):
            c = chain + [x]
            sim.setdefault(len(c) - 1, []).append(tuple(c))
            rec(c, [y for y in cands[i + 1:] if (x & y) == x and x != y])
    rec([], Q)
    return sim

def acyclic(Q):
    sim = order_complex_sim(Q)
    return all(b == 0 for b in fb.reduced_betti(sim, 4))

def Q_of(T):
    Q = set(nerve.SUBS)
    for t in T: Q &= nerve.COMP[t]
    return Q

if __name__ == "__main__":
    t0 = time.time(); rng = random.Random(20261123)
    res = {"tested": 0, "empty": 0, "nonempty_acyclic": 0, "nonempty_not_acyclic": 0, "hard_case_tested": 0}
    def test(T):
        Q = Q_of(T)
        res["tested"] += 1
        if not Q: res["empty"] += 1; return
        if acyclic(Q): res["nonempty_acyclic"] += 1
        else: res["nonempty_not_acyclic"] += 1
        U = 0; V = 63
        for t in T: U |= t; V &= t
        if V == 0 and U == 63: res["hard_case_tested"] += 1
    for r in (1, 2):
        for T in itertools.combinations(nerve.SUBS, r): test(T)
    for _ in range(2500):
        r = rng.choice([3, 4, 5, 6, 8]); test(rng.sample(nerve.SUBS, r))
    # biased towards hard case (V empty, U full, Q nonempty): grow T around a random x0
    for _ in range(1500):
        x0 = rng.choice(nerve.SUBS); T = []
        for _ in range(rng.randint(3, 8)):
            t = rng.choice(sorted(nerve.COMP[x0])); T.append(t)
        test(sorted(set(T)))
    res["seconds"] = round(time.time() - t0)
    json.dump(res, open(os.path.join(_path.ROOT, "RESULTS", "A25_star_intersection_lemma.json"), "w"), indent=1); print(res)
