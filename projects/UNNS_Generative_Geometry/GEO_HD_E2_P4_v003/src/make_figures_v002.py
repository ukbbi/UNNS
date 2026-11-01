"""v002 figures: slab mechanism (planar gap x thin slab) and the verdict cross-tab by free coordinate."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import _boot  # noqa: E402
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fractions import Fraction as Fr
a = _boot.p4("audit_v002")
S = json.load(open(os.path.join(ROOT, "results/P4_SLAB.json")))
fig, ax = plt.subplots(1, 2, figsize=(11, 4.6))
F, cells = a.cells_from_member(lambda v: (v[0] + v[1]) % 2 == 0, (2, 2))
A = ax[0]
A.fill([0, 2, 2, 0], [2, 2, 0, 2][:4] if False else [2, 2, 0, 2], color="#dfe9f7", alpha=0.9, label="hull H' = {x+y>=2}")
for base, gens in cells:
    vs = [tuple(map(float, v)) for v in a.cc._verts(base, [list(g) for g in gens])]
    if len(vs) == 4:
        order = [vs[0], vs[1], vs[3], vs[2]]
        A.fill(*zip(*order), color="#2b6cb0", alpha=0.35)
    elif len(vs) == 2:
        A.plot(*zip(*vs), color="#2b6cb0", lw=2)
pts = [tuple(float(Fr(x)) for x in r["slab"]["planar_point"]) for r in S["lattice_level"]["records"] + S["fieldI"]["records"] if r["slab"]["planar_box"] == [2, 2]]
A.scatter(*zip(*pts), color="#c53030", s=14, zorder=5, label="planar part of %d recorded witnesses" % len(pts))
A.scatter(*zip(*[(float(x), float(y)) for x, y, in [(p[0], p[1]) for p in F]]), color="k", s=25, zorder=6, label="F(E2)")
A.set_xlim(-0.1, 2.1); A.set_ylim(-0.1, 2.1); A.set_aspect("equal"); A.set_title("Planar target E2, box (2,2): U'_2 = blue segments only;\ngap = H'_2 minus U'_2 (witness planar parts in red)", fontsize=9)
A.legend(fontsize=7, loc="lower left")
B = ax[1]
t = S["free_coordinate_crosstab_fieldI_nonrect_target"]
cats = ["CONTAINED", "PROVED_BY_P4Z1", "NOT_CONTAINED", "UNAVAILABLE_COST"]
fr = [t.get("free_coordinate|" + c, 0) for c in cats]; nf = [t.get("no_free_coordinate|" + c, 0) for c in cats]
import numpy as np
xs = np.arange(len(cats))
B.bar(xs - 0.2, nf, 0.4, label="no free coordinate (2,427)", color="#718096"); B.bar(xs + 0.2, fr, 0.4, label="free coordinate (1,418)", color="#c53030")
B.set_yscale("symlog"); B.set_xticks(xs); B.set_xticklabels([c.replace("_", "\n") for c in cats], fontsize=7); B.legend(fontsize=8)
B.set_title("Spatial FIELD-I rows with nonrectangular target (3,845)")
for i, v in enumerate(fr): B.text(i + 0.2, v, str(v), ha="center", va="bottom", fontsize=7)
for i, v in enumerate(nf): B.text(i - 0.2, v, str(v), ha="center", va="bottom", fontsize=7)
plt.tight_layout(); plt.savefig(os.path.join(ROOT, "figures/slab_mechanism.png"), dpi=130)
print("ok", len(pts))
