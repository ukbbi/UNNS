"""E02 -- when are two systems with equal uncolored data the same system under a relabelling of the label ranks?  For every pair of lattice classes with identical O2c, search all 720 rank permutations sigma (sigma o p) for
A(m_b) = sigma(A(m_a)).  If so they are the same abstract complex placed on different labels; only the labelled data (O3, the anchor relation) tells them apart."""
import itertools, json, os
import _path
import obs
from E01_information_recovery import ANCHORS, PRIMES

if __name__ == "__main__":
    res = {}
    for tag, C, m0 in ANCHORS:
        D = obs.denominators(list(C))
        caps = {p: max(obs.vp(D[s], p) for s in range(1, 64)) for p in PRIMES}
        primes = [p for p in PRIMES if caps[p] > 0]
        reps = {}
        for sig in itertools.product(*[range(caps[p] + 1) for p in primes]):
            m = 1
            for p, e in zip(primes, sig):
                m *= p ** e
            reps[sig] = m
        sigs = sorted(reps)
        systems = [obs.System(C, reps[s]) for s in sigs]
        iso = obs.iso_classes(systems)
        anchor = obs.Anchor(C, m0)
        pairs = []
        for i, j in itertools.combinations(range(len(sigs)), 2):
            a, b = systems[i], systems[j]
            if iso[i] == iso[j] and a.betti == b.betti and a.fvec == b.fvec and a.key3 != b.key3:
                Aj = set(b.A)
                sigma = next((s for s in itertools.permutations(range(6)) if {tuple(s[x] for x in p) for p in a.A} == Aj), None)
                pairs.append({"m_a": reps[sigs[i]], "m_b": reps[sigs[j]], "N": a.N, "state_a": str(anchor.state(a)), "state_b": str(anchor.state(b)), "relabelling_sigma": None if sigma is None else list(sigma)})
        res[tag] = {"pairs_equal_O2c_different_labelled_set": pairs}
        print(tag, len(pairs), pairs[:5])
    json.dump(res, open(os.path.join(_path.ROOT, "RESULTS", "E02_relabeling.json"), "w"), indent=1)
