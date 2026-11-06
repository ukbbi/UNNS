"""E01 -- exact information-recovery profile of an arithmetic hole across the observation hierarchy O0 < O1 < O2 < O2c < O3 (see ENGINE/obs.py).
For each anchor: (a) the 60-source experiment m = m0*t, t=1..60, uniform; (b) the complete system lattice (all sources, grouped by capped prime valuations: A(m) depends only on these);
(c) exact tables, H(Y), H(Y|O_i), I(Y;O_i); equal-signature/different-state pair search with first-distinguishing level; (d) additivity of the history count over prime indicators;
(e) divisibility-arrow transitions m -> m p with exact (Y, N) changes; (f) explicit certificates (cochain for survival, filling chain for filled), independently verified."""
import itertools, json, os, sys, time
from collections import Counter, defaultdict
from fractions import Fraction
from math import gcd
import _path
import obs
from information import fmt

ANCHORS = [("A1", (2, 3, 4, 5, 8, 9), 288), ("A2", (2, 3, 6, 7, 8, 9), 432)]
LEVELS = ["O0", "O1", "O2", "O2c", "O3"]
PRIMES = (2, 3, 5, 7, 11, 13)


def run_anchor(tag, C, m0):
    t0 = time.time()
    D = obs.denominators(list(C))
    caps = {p: max(obs.vp(D[s], p) for s in range(1, 64)) for p in PRIMES}
    primes = [p for p in PRIMES if caps[p] > 0]
    anchor = obs.Anchor(C, m0)
    assert anchor.beta2 == 1
    cap_sig = lambda m: tuple(min(obs.vp(m, p), caps[p]) for p in primes)
    reps = {}
    for sig in itertools.product(*[range(caps[p] + 1) for p in primes]):
        reps[sig] = 1
        for p, e in zip(primes, sig):
            reps[sig] *= p ** e
    sigs = sorted(reps)
    systems = [obs.System(C, reps[s]) for s in sigs]
    sidx = {s: i for i, s in enumerate(sigs)}
    iso = obs.iso_classes(systems)
    state = [anchor.state(s) for s in systems]
    # signatures per level
    def sig_of(i, lev):
        s = systems[i]
        if lev == "O0": return s.O0
        if lev == "O1": return s.O1
        if lev == "O2": return (iso[i],)
        if lev == "O2c": return (iso[i], s.betti, s.fvec)
        return (s.key3,)
    out = {"tag": tag, "content": list(C), "m0": m0, "primes": primes, "caps": caps, "lattice_classes": len(sigs), "beta2_at_m0": anchor.beta2, "classes": []}
    for i, sg_ in enumerate(sigs):
        s = systems[i]
        out["classes"].append({"cap_valuations": dict(zip(primes, sg_)), "m_rep": reps[sg_], "N": s.N, "H_hist_bits": (fmt(obs.hartley_dec(s.N), 20) if s.N else None), "betti": list(s.betti), "fvec": list(s.fvec),
                               "iso_class": iso[i], "state": state[i], "h1": [list(x) for x in s.h1], "h2": [list(x) for x in s.h2], "A_sha256": s.key3})
    out["distinct_iso_classes"] = len(set(iso.values()))
    out["distinct_N"] = len({s.N for s in systems})
    # ---- ensembles
    def profile(samples, label):
        res = {"ensemble": label, "size": len(samples), "levels": {}}
        for lev in LEVELS:
            HY, HYO, I, nclass, HO = obs.cond_entropy([(y, sg(lev)) for y, sg in samples])
            res["levels"][lev] = {"observation_classes": nclass, "H(O)": fmt(HO, 30), "H(Y)": fmt(HY, 30), "H(Y|O)": fmt(HYO, 30), "I(Y;O)": fmt(I, 30)}
        return res
    ens = {}
    # (a) 60 sources, binary Y = survives
    samp60 = []
    survivors = 0
    for t in range(1, 61):
        m = m0 * t
        i = sidx[cap_sig(m)]
        y = 1 if state[i] == 1 else 0
        survivors += y
        samp60.append((y, (lambda i: (lambda lev: sig_of(i, lev)))(i)))
    ens["sources_60_binaryY"] = profile(samp60, "m=m0*t, t=1..60, uniform; Y=1 iff the anchored hole survives")
    ens["sources_60_binaryY"]["survivors"] = survivors
    ens["sources_60_binaryY"]["distinct_systems_among_60"] = len({cap_sig(m0 * t) for t in range(1, 61)})
    # (b) lattice, binary and three-valued
    sampL2 = [((1 if state[i] == 1 else 0), (lambda i: (lambda lev: sig_of(i, lev)))(i)) for i in range(len(sigs))]
    sampL3 = [(str(state[i]), (lambda i: (lambda lev: sig_of(i, lev)))(i)) for i in range(len(sigs))]
    ens["lattice_binaryY"] = profile(sampL2, "uniform over all system classes; Y=1 iff survives")
    ens["lattice_threevalued"] = profile(sampL3, "uniform over all system classes; Y3 in {NA, 0, 1}")
    out["ensembles"] = ens
    # ---- pair search: equal signature at level, different state
    pairs = {}
    for yname, ys in (("binaryY", [1 if s == 1 else 0 for s in state]), ("threevalued", [str(s) for s in state])):
        pairs[yname] = {}
        for lev in LEVELS:
            found = [(i, j) for i, j in itertools.combinations(range(len(sigs)), 2) if sig_of(i, lev) == sig_of(j, lev) and ys[i] != ys[j]]
            pairs[yname][lev] = [{"a": dict(zip(primes, sigs[i])), "b": dict(zip(primes, sigs[j])), "m_a": reps[sigs[i]], "m_b": reps[sigs[j]], "Y_a": ys[i], "Y_b": ys[j],
                                  "first_level_separating": next(l for l in LEVELS if sig_of(i, l) != sig_of(j, l))} for i, j in found]
    out["separating_pairs"] = pairs
    # ---- additivity of N over prime indicators on the comparable (survival-capable) sub-lattice
    comp = [i for i in range(len(sigs)) if state[i] != "NA"]
    base = [i for i in comp if all(sigs[i][k] == min(sigs[j][k] for j in comp) for k in range(len(primes)))]
    out["comparable_classes"] = len(comp)
    if base:
        b = base[0]
        lows = {k: min(sigs[j][k] for j in comp) for k in range(len(primes))}
        highs = {k: max(sigs[j][k] for j in comp) for k in range(len(primes))}
        deltas = {}
        for k, p in enumerate(primes):
            if highs[k] > lows[k]:
                s = list(sigs[b]); s[k] = highs[k]
                deltas[p] = systems[sidx[tuple(s)]].N - systems[b].N
        add_ok = True
        for j in comp:
            pred = systems[b].N + sum(deltas[p] for k, p in enumerate(primes) if p in deltas and sigs[j][k] > lows[k])
            add_ok &= pred == systems[j].N
        out["additivity"] = {"N_at_minimal_survivor": systems[b].N, "delta_N_by_prime_indicator": deltas, "N_equals_N0_plus_sum_delta_over_indicators": add_ok,
                             "comparable_valuation_window": {p: [lows[k], highs[k]] for k, p in enumerate(primes)}}
    # ---- divisibility arrows
    trans = []
    for i in comp:
        for p in primes:
            k = primes.index(p)
            s = list(sigs[i]); s[k] = min(s[k] + 1, caps[p])
            j = sidx[tuple(s)]
            trans.append({"from": dict(zip(primes, sigs[i])), "p": p, "Y_from": state[i], "Y_to": state[j], "N_from": systems[i].N, "N_to": systems[j].N, "dN": systems[j].N - systems[i].N,
                          "A_unchanged": systems[i].key3 == systems[j].key3})
    out["arrows"] = trans
    law = defaultdict(set)
    for tr in trans:
        law[tr["p"]].add((tr["Y_from"], tr["Y_to"]))
    out["arrow_Y_transitions_by_prime"] = {str(p): sorted(map(list, v), key=str) for p, v in law.items()}
    # ---- certificates for every comparable class
    out["certificates"] = [{"cap_valuations": dict(zip(primes, sigs[i])), "m_rep": reps[sigs[i]], **anchor.certificate(systems[i])} for i in comp]
    out["certificates_all_verified"] = all(c.get("verified", True) for c in out["certificates"])
    # ---- survival law check on the 60 sources: Y=1 iff t is coprime to every prime of the lattice that can still divide a multiplier (gcd(t, prod primes)=1)
    prod = 1
    for p in primes:
        if obs.vp(m0, p) < caps[p]:
            prod *= p
    out["law_check"] = {"gcd_modulus": prod, "survives_iff_gcd(t,modulus)=1_for_all_60": all((state[sidx[cap_sig(m0 * t)]] == 1) == (gcd(t, prod) == 1) for t in range(1, 61))}
    out["seconds"] = round(time.time() - t0, 1)
    return out


if __name__ == "__main__":
    allr = {}
    for tag, C, m0 in ANCHORS:
        r = run_anchor(tag, C, m0)
        allr[tag] = r
        print(tag, "classes", r["lattice_classes"], "iso", r["distinct_iso_classes"], "N", r["distinct_N"], r["seconds"], "s", flush=True)
        for en, e in r["ensembles"].items():
            print(" ", en, {l: (v["H(Y|O)"][:10], v["observation_classes"]) for l, v in e["levels"].items()}, "H(Y)", e["levels"]["O0"]["H(Y)"][:10])
        print("  sep binary:", {l: len(v) for l, v in r["separating_pairs"]["binaryY"].items()}, " sep 3-valued:", {l: len(v) for l, v in r["separating_pairs"]["threevalued"].items()})
        print("  additivity:", r.get("additivity"))
        print("  certs verified:", r["certificates_all_verified"])
    json.dump(allr, open(os.path.join(_path.ROOT, "RESULTS", "E01_information_recovery.json"), "w"), indent=1)
