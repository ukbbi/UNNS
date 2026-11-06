"""GIG-INFO v001: put the frozen, read-only parent ENGINE folders on sys.path (siblings, or env GIG_V001..GIG_V007, GIG_V005_S2, GIG_V005_S3). Nothing in the parents is modified."""
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARENT = os.path.dirname(ROOT)
def _loc(name, env):
    p = os.environ.get(env) or os.path.join(PARENT, name)
    if not os.path.isdir(p) and os.path.isdir("/home/claude/" + name):
        p = "/home/claude/" + name
    return p
NAMES = [("V001", "GIG_I_v001"), ("V002", "GIG_I_v002"), ("V003", "GIG_I_v003"), ("V004", "GIG_I_v004"), ("V005", "GIG_I_v005"), ("V005S2", "GIG_I_v005_S2"), ("V005S3", "GIG_I_v005_S3"), ("V006", "GIG_I_v006"), ("V007", "GIG_I_v007")]
PATHS = {}
for key, name in NAMES:
    PATHS[key] = _loc(name, "GIG_" + key.replace("V005S", "V005_S") if key.startswith("V005S") else "GIG_" + key)
for key in ("V007", "V006", "V005S3", "V005S2", "V005", "V004", "V003", "V002", "V001"):
    e = os.path.join(PATHS[key], "ENGINE")
    if e not in sys.path:
        sys.path.insert(0, e)
sys.path.insert(0, os.path.join(ROOT, "ENGINE"))
