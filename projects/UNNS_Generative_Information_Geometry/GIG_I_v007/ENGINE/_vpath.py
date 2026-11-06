"""GIG-I v007: locate the frozen parent packages (siblings, or env GIG_V001..GIG_V006 etc.) and put their ENGINE folders on sys.path (v006 ENGINE first). Parents are read-only."""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARENT = os.path.dirname(ROOT)
def _loc(name, env):
    p = os.environ.get(env) or os.path.join(PARENT, name)
    if not os.path.isdir(p) and os.path.isdir("/home/claude/" + name):
        p = "/home/claude/" + name
    return p
V001, V002, V003, V004, V005 = (_loc("GIG_I_v00%d" % i, "GIG_V00%d" % i) for i in (1, 2, 3, 4, 5))
V005S2 = _loc("GIG_I_v005_S2", "GIG_V005_S2")
V005S3 = _loc("GIG_I_v005_S3", "GIG_V005_S3")
V006 = _loc("GIG_I_v006", "GIG_V006")
for p in (V006, V005S3, V005S2, V005, V004, V003, V002, V001):
    e = os.path.join(p, "ENGINE")
    if e not in sys.path:
        sys.path.insert(0, e)
sys.path.insert(0, os.path.join(ROOT, "ENGINE"))
