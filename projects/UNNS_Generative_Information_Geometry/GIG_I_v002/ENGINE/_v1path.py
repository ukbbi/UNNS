"""Locate the frozen, read-only GIG_I_v001 ENGINE (sibling folder, or $GIG_V001) and put it on sys.path.
v002 never modifies v001; it only imports from it."""
import os
import sys

_here = os.path.dirname(os.path.abspath(__file__))
_cands = [os.environ.get("GIG_V001", ""), os.path.join(_here, "..", "..", "GIG_I_v001")]
V001 = None
for c in _cands:
    if c and os.path.isdir(os.path.join(c, "ENGINE")):
        V001 = os.path.abspath(c)
        break
if V001 is None:
    raise ImportError("GIG_I_v001 not found next to GIG_I_v002 (set GIG_V001 to its folder)")
for p in (os.path.join(V001, "ENGINE"), _here):
    if p not in sys.path:
        sys.path.insert(0, p)
