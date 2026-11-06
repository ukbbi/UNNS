"""Read-only access to the frozen GIG-INFO v002 modules under explicit aliases (its module names `census`, `ent`, `pair_cert` collide with older releases)."""
import importlib.util, os
import _vpath


def _load(alias, fname):
    p = os.path.join(_vpath.PATHS["INFO002"], "ENGINE", fname)
    spec = importlib.util.spec_from_file_location(alias, p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m

census = _load("v2_census", "census.py")
ent = _load("v2_ent", "ent.py")
pair_cert = _load("v2_pair_cert", "pair_cert.py")
