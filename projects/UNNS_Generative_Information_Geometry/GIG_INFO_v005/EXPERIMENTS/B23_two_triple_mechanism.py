"""B23 -- mechanism of the smallest 3-adjacency counterexample: forbid exactly the two consecutive triples (1,2,0) and (5,4,3).
Mayer-Vietoris:  H1(Z1 u Z2) = H~0(Z1 n Z2) (both pieces have H~0=H~1=0).  Computed exactly."""
import itertools, json, os
import _path, forbidden as fb, B21_locality_boundary as B
import history_complex as hc
T3 = list(itertools.permutations(range(6), 3))
def Y(bad):
    return fb.y_simplices(B.triple_mask(set(T3) - set(bad)), 6)
if __name__ == "__main__":
    t1, t2 = (1, 2, 0), (5, 4, 3)
    Z1, Z2, Z12 = Y([t1]), Y([t2]), Y([t1, t2])
    inter = {d: sorted(set(Z1.get(d, [])) & set(Z2.get(d, []))) for d in range(5)}
    inter = {d: v for d, v in inter.items() if v}
    out = {"triples": [list(t1), list(t2)], "reduced_betti_Z1": fb.reduced_betti(Z1, 3), "reduced_betti_Z2": fb.reduced_betti(Z2, 3), "reduced_betti_union": fb.reduced_betti(Z12, 3), "reduced_betti_intersection": fb.reduced_betti(inter, 3),
           "betti_K_single_triple": list(hc.betti(B.triple_mask(set(T3) - {t1}), 6)), "betti_K_two_triples": list(hc.betti(B.triple_mask(set(T3) - {t1, t2}), 6))}
    json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "B23_two_triple_mechanism.json"), "w"), indent=1); print(out)
