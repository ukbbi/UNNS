"""E36 (v006-4) -- ROLE-MAP CORRECTION.  Stage 3 (E30) tested whether the six-smallest-label sub-content of a lifted-hole content admits the Stage-1 H_2 survival regime using the IDENTITY role map only.
Here the anchor class (cycle z, prefix requirement P, minimal families) is transported by all |S_6|/stabiliser distinct images (E23.images, 180 of them) and each image is tested on the two sub6 contents
(2,9,15,20,26,27) and (8,9,15,20,26,27).  Survival of an image at content C: K = lcm_{I in P} D(I), and no family of the image is contained in A(K) (same law as Stage 1/AT-2).
Corrected statement:  absence of lower-dimensional survival holds for the identity role map only."""
import json, os, sys
from math import lcm
import _path
sys.path.insert(0, os.path.join(_path._vpath.V005S2, "EXPERIMENTS"))
import atlas as A, hole_survival as H
import E23_families as E23
import block_factor as bf

zb = sum(1 << g for g in H.Z)
P = A.pz(zb)
fams, _ = A.minimal_families(zb)
imgs = E23.images({"P": P, "fams": fams})
out = {"n_images": len(imgs), "contents": []}
for C in ([2, 9, 15, 20, 26, 27], [8, 9, 15, 20, 26, 27]):
    D = bf.denominators(C)
    idx = []
    for k, (Pm, fs) in enumerate(imgs):
        Pl = [s for s in range(1, 64) if Pm >> s & 1]
        K = lcm(*[D[s] for s in Pl])
        Af = sum(1 << s for s in range(1, 64) if K % D[s] == 0)
        if A.survives(Pm, fs, Af):
            idx.append(k)
    out["contents"].append({"content": C, "images_with_H2_regime": len(idx), "image_indices": idx, "identity_image_has_regime": 0 in idx})
    print(C, len(idx), "of", len(imgs), "identity:", 0 in idx)
json.dump(out, open(os.path.join(_path.ROOT, "RESULTS", "E36_role_map_correction.json"), "w"), indent=1)
