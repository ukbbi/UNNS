#!/usr/bin/env python3
"""Differential test (NOT a proof). Compares the Lean definitions (evaluated with `lean`) against two independent Python implementations:
  (a) the geometric 2-in/2-out rule and exact Fraction energies of the frozen v005 module (data/provenance/physical_energy_v005.py),
  (b) the exact integer Hamiltonian from data/real_4x4.txt.
usage: diff_test.py ROOT   (run from ROOT with `lake` on PATH)"""
import sys, random, subprocess, pathlib, re, ast
from fractions import Fraction
ROOT = pathlib.Path(sys.argv[1]); sys.dont_write_bytecode = True; sys.path.insert(0, str(ROOT/"data/provenance"))
import physical_energy_v005 as P
t = (ROOT/"data/real_4x4.txt").read_text().split(); n = 40; c = 2
K = [[Fraction(0)]*n for _ in range(n)]
for i in range(n):
    for j in range(i+1, n): K[i][j] = Fraction(float(t[c])); c += 1
vs = [(int(t[c+2*v]), int(t[c+2*v+1])) for v in range(16)]
isl = P.source_geometry(4); vp = P.vertex_positions(4); inc = P.incident_islands(isl, vp)
geo_sets = [frozenset(x) for x in inc]; file_sets = [frozenset(i for i in range(n) if (m >> i) & 1) for m, _ in vs]
assert sorted(map(sorted, geo_sets)) == sorted(map(sorted, file_sets))
rng = random.Random(20261010); ids = [rng.getrandbits(40) for _ in range(300)]
# bias: include near-grammar states (random single/double flips of the ground witness) so violations of size 1-2 are exercised
g = 711243241830
for _ in range(100): ids.append(g ^ (1 << rng.randrange(n)))
for _ in range(100): ids.append(g ^ (1 << rng.randrange(n)) ^ (1 << rng.randrange(n)))
ids += [g, 161487427942, 0, (1 << 40)-1]
(ROOT/"tests/_Diff.lean").write_text("import SCR_IV_Witness\nopen SCR_IV\n#eval [%s].map (fun id => (id, violatingVertices id, hScaled id))\n" % ", ".join(map(str, ids)))
out = subprocess.run(["lake", "env", "lean", "tests/_Diff.lean"], cwd=ROOT, capture_output=True, text=True).stdout
res = ast.literal_eval(re.sub(r"\)", ")", out.strip().replace("[", "[").replace("]", "]")))
assert len(res) == len(ids), (len(res), len(ids), out[:200])
bad_g = bad_h = 0; viol_hist = {}
for (idv, vv, hs) in res:
    s = P.decode(idv, n); ch = P.vertex_charges_geometric(s, isl, vp)
    geo_viol = sorted(sorted(inc[v]) for v in range(16) if ch[v] != 0)
    lean_viol = sorted(sorted(file_sets[k]) for k in vv)
    if geo_viol != lean_viol: bad_g += 1
    H = sum(K[i][j]*s[i]*s[j] for i in range(n) for j in range(i+1, n))
    if Fraction(hs, 1 << 70) != H: bad_h += 1
    viol_hist[len(vv)] = viol_hist.get(len(vv), 0)+1
print("ids tested:", len(ids), " violating-vertex-set mismatches vs geometric rule:", bad_g, " energy mismatches vs exact Python:", bad_h, " violation-count histogram:", dict(sorted(viol_hist.items())))
sys.exit(0 if bad_g == 0 and bad_h == 0 else 1)
