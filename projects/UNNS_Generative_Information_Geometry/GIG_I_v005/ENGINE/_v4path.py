"""locate frozen v001-v004 packages (siblings, or env GIG_V001..GIG_V004) and put their ENGINE folders on sys.path."""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARENT = os.path.dirname(ROOT)
def _loc(n, env):
    p = os.environ.get(env) or os.path.join(PARENT, "GIG_I_v00%d" % n)
    if not os.path.isdir(p):
        for alt in ("/home/claude/GIG_I_v00%d" % n,):
            if os.path.isdir(alt): p = alt
    return p
V001, V002, V003, V004 = (_loc(i, "GIG_V00%d" % i) for i in (1, 2, 3, 4))
for p in (V004, V003, V002, V001):
    e = os.path.join(p, "ENGINE")
    if e not in sys.path: sys.path.insert(0, e)
sys.path.insert(0, os.path.join(ROOT, "ENGINE"))
