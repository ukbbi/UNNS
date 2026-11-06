"""locate the frozen v001-v005 packages (siblings, or env GIG_V001..GIG_V005) and put their ENGINE folders on sys.path; the S2 ENGINE comes first."""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARENT = os.path.dirname(ROOT)
def _loc(n):
    p = os.environ.get("GIG_V00%d" % n) or os.path.join(PARENT, "GIG_I_v00%d" % n)
    if not os.path.isdir(p) and os.path.isdir("/home/claude/GIG_I_v00%d" % n):
        p = "/home/claude/GIG_I_v00%d" % n
    return p
V001, V002, V003, V004, V005 = (_loc(i) for i in (1, 2, 3, 4, 5))
for p in (V005, V004, V003, V002, V001):
    e = os.path.join(p, "ENGINE")
    if e not in sys.path:
        sys.path.insert(0, e)
sys.path.insert(0, os.path.join(ROOT, "ENGINE"))
