"""Locate the frozen, read-only GIG_I_v001 and GIG_I_v002 packages (siblings, or $GIG_V001 / $GIG_V002) and put their
ENGINE folders (and this one) on sys.path.  v003 never modifies them."""
import os
import sys

_here = os.path.dirname(os.path.abspath(__file__))


def _find(env, name):
    for c in (os.environ.get(env, ""), os.path.join(_here, "..", "..", name)):
        if c and os.path.isdir(os.path.join(c, "ENGINE")):
            return os.path.abspath(c)
    raise ImportError("%s not found next to GIG_I_v003 (set %s)" % (name, env))


V001 = _find("GIG_V001", "GIG_I_v001")
V002 = _find("GIG_V002", "GIG_I_v002")
for p in (os.path.join(V002, "ENGINE"), os.path.join(V001, "ENGINE"), _here):
    if p not in sys.path:
        sys.path.insert(0, p)
import _v1path  # noqa: E402,F401  (v002's locator; same v001)
