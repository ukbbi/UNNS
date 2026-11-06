"""E23 -- minimal filling antichains for every canonical cycle of E22 (exact dualisation, no enumeration cut-off) and the coverage matrix:
cycle c covers regime r iff some S_6-image of c survives in A(r) (P <= A(r) and no minimal family <= A(r))."""
import json, os, time
from math import lcm
import _path
import atlas as A
import block_factor as bf
import _vpath


def adm_family(C, L):
    D = bf.denominators(list(C))
    f = 0
    for I in range(1, 64):
        if L % D[I] == 0:
            f |= 1 << I
    return f


def build():
    E = json.load(open(os.path.join(_path.ROOT, "RESULTS", "E22_extract.json")))
    regimes = E["records"]
    cyc = sorted({int(c) for r in regimes for c in r["classes"]})
    t0 = time.time()
    atlas = []
    for zb in cyc:
        P = A.pz(zb)
        fams, st = A.minimal_families(zb)
        atlas.append({"cycle": zb, "weight": zb.bit_count(), "P": P, "fams": fams, "stats": st})
    return regimes, atlas, round(time.time() - t0, 1)


def images(c):
    seen, out = set(), []
    for sig in A.SIGMAS:
        P = A.act_family(sig, c["P"])
        fams = tuple(sorted(A.act_family(sig, f) for f in c["fams"]))
        key = (P, fams)
        if key not in seen:
            seen.add(key)
            out.append((P, fams))
    return out


def covers(imgs, Afam):
    return any(A.survives(P, fams, Afam) for P, fams in imgs)


if __name__ == "__main__":
    regimes, atlas, sec = build()
    Afams = [adm_family(tuple(r["content"]), r["L"]) for r in regimes]
    imgs = [images(c) for c in atlas]
    cov = [[covers(imgs[i], Afams[j]) for j in range(len(regimes))] for i in range(len(atlas))]
    own = [[str(a["cycle"]) in r["classes"] for r in regimes] for a in atlas]
    assert all(cov[i][j] for i in range(len(atlas)) for j in range(len(regimes)) if own[i][j])        # each cycle covers the regime it came from
    # greedy set cover
    left = set(range(len(regimes)))
    chosen = []
    while left:
        i = max(range(len(atlas)), key=lambda i: len(left & {j for j in range(len(regimes)) if cov[i][j]}))
        chosen.append(i)
        left -= {j for j in range(len(regimes)) if cov[i][j]}
    ps1_idx = [j for j, r in enumerate(regimes) if r["ps1_explained"]]
    out = {"cycles": len(atlas), "seconds_families": sec,
           "q_hist": {}, "families_count_hist": {}, "covering_cycles": len(chosen), "cover_sizes": [sum(cov[i]) for i in chosen],
           "images_per_cycle": [len(x) for x in imgs],
           "regimes_covered_by_union_of_all_cycles": sum(any(cov[i][j] for i in range(len(atlas))) for j in range(len(regimes))),
           "cycles": [{"cycle_bits": str(a["cycle"]), "weight": a["weight"], "q": a["stats"]["q"], "n_min_families": len(a["fams"]),
                       "family_sizes": sorted(f.bit_count() for f in a["fams"]), "regimes_covered": sum(cov[i]), "own_regimes": sum(own[i])} for i, a in enumerate(atlas)]}
    for a in atlas:
        out["q_hist"][a["stats"]["q"]] = out["q_hist"].get(a["stats"]["q"], 0) + 1
        out["families_count_hist"][len(a["fams"])] = out["families_count_hist"].get(len(a["fams"]), 0) + 1
    json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "E23_families.json"), "w"), indent=1)
    json.dump([{"cycle_bits": str(a["cycle"]), "P": str(a["P"]), "families": [str(f) for f in a["fams"]]} for a in atlas],
              open(os.path.join(_path.ROOT, "CERTIFICATES", "atlas_cycles.json"), "w"))
    print({k: v for k, v in out.items() if k != "cycles"})
    print(sorted(((c["q"], c["n_min_families"], c["regimes_covered"]) for c in out["cycles"]))[:80])
