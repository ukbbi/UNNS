"""G10 -- assemble RESULTS/report.md from the result JSONs (mathematics first)."""
import json, os
import _path
R = os.path.join(_path.ROOT, "RESULTS")
J = lambda n: json.load(open(os.path.join(R, n)))
a20, a21, a22, a23, a24, a25, a26 = (J(x) for x in ("A20_nerve_model.json", "A21_motifs.json", "A22_pair_anatomy.json", "A23_cone_criterion.json", "A24_S2_vs_dead_sets.json", "A25_star_intersection_lemma.json", "A26_cocycle_certificates.json"))
b20, b21, b23, b24 = (J(x) for x in ("B20_adjacency_cover.json", "B21_locality_boundary.json", "B23_two_triple_mechanism.json", "B24_symbolic_theorem_check.json"))
c = json.load(open(os.path.join(_path.ROOT, "CERTIFICATES", "counterexample_triple_adjacency_beta2.json")))
L = ["# GIG-INFO v005 — Forbidden-History Topology and Information Recovery: report", ""]
L += ["## 1. Mathematics", "",
      "**Arithmetic.** For prefix-defined systems (all arithmetic regimes) the forbidden complex Y_A is homotopy equivalent to the dead-set nerve N[D_A] (T-NERVE, from the star-intersection lemma L1), so beta_2(K_A) = dim H_1(N[D_A]).",
      f"- Nerve model vs direct Y: {a20['model_agrees_b0_b1']}/{a20['tested']} agree (158 census positives, 132 held-out positives, 1000 sampled negatives); all {a20['prefix_defined']} prefix-defined.",
      f"- L1 numerical check: {a25['tested']} sets T, {a25['nonempty_acyclic']} nonempty and all acyclic, {a25['hard_case_tested']} in the hard case (cap T empty, cup T full); failures {a25['nonempty_not_acyclic']}.",
      f"- Non-bounding hollow triangle in N[D]: {a21['positives']['counts']['with_nonbounding_hollow_triangle']}/290 positives, {a21['negatives']['counts']['with_nonbounding_hollow_triangle']}/1000 negatives ({a21['negatives']['counts']['with_hollow_triangle']} negatives have hollow triangles, all bounding).",
      f"- The other {len(a23['positives']['exceptional_positives_without_hollow_triangle_nonbounding'])} positives carry a non-bounding 4-cycle formed by two complementary dead-set pairs.",
      f"- Cycle + cocycle certificates verified for {a26['counts']['certified']}/{a26['counts']['systems']} positives.",
      f"- 'No cone point' is not equivalent to non-bounding: {a23['positives']['counts']['bounding|uncone']} (positives) and {a23['negatives']['counts']['bounding|uncone']} (negatives) uncone hollow triangles bound.", "",
      "**Sharp pairs.**"]
for tag, r in a22.items():
    L.append(f"- {tag}, content {r['content']}, sources {r['positive_source']}/{r['negative_source']}: |D| = {r['|D|']}, H1(N[D]) ranks {[x[1] for x in r['nerve_betti']]}, dead sets only in the positive {r['dead_only_in_positive']}, only in the negative {r['dead_only_in_negative']}; non-bounding hollow triangles {r['nonbounding_hollow']}.")
L += ["", f"**S2.** In the {a24['mixed_classes']} census classes with equal (N,h1,Q,Sds) and mixed sign, S2 differences (positive minus negative): {a24['S2_difference_signs']}. No derivation from the nerve is offered.", "",
      "**Symbolic transition grammar.** Theorem T-ADJ: for every digraph G on six events, beta_2 of the Hamiltonian-path complex is 0.",
      f"- Finite hypotheses: single Z_p acyclic for all 30 pairs ({b20['single_pair_betti_distinct']}); all 435 Z_pq nonempty and connected; all 4060 Z_pqr nonempty ({b20['sizes']['3']['disconnected']} disconnected, harmless).",
      f"- All {b24['distinct_masks']} distinct S/R/N masks: beta_2 max {b24['beta2_max']}; (beta1,beta2,beta3) distribution {b24['beta_1_2_3_distribution']}.",
      f"- Random pair-adjacency systems: {b21['pair_adjacency_random']}.",
      f"- Sharpness: forbidding the consecutive triples {c['forbidden_triples']} gives Betti numbers {c['betti_hc_engine']} (beta_2 = 5); mechanism: Z1 and Z2 have trivial reduced H0,H1, their intersection has {b23['reduced_betti_intersection'][0] + 1} components (reduced b0 = {b23['reduced_betti_intersection'][0]}), union has reduced b1 = {b23['reduced_betti_union'][1]}.",
      f"- Exploratory: {c['recount_random_3adjacency']['beta2_positive']} of {c['recount_random_3adjacency']['tested']} random 3-adjacency systems have beta_2 > 0.", ""]
open(os.path.join(R, "report.md"), "w").write("\n".join(L)); print("\n".join(L)[:1500])
