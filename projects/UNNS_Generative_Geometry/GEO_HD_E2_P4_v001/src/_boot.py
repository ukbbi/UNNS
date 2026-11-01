"""Path bootstrap.  The inherited exact engine (src/engine/, byte-identical E2-P3 copies, hash-pinned in RUN_VERIFY.py) uses flat module
names.  New E2-P4 modules in src/ reuse some of those names (exact_containment, planar_residual, coupled_3d), so src/ is NEVER put on
sys.path; P4 modules are loaded through p4('name') under the alias 'p4_<name>'."""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.join(HERE, "engine")
for pth in (os.path.join(ENGINE, "p2", "inherited"), os.path.join(ENGINE, "p2"), ENGINE):
    if pth not in sys.path:
        sys.path.insert(0, pth)


def p4(name):
    key = "p4_" + name
    if key in sys.modules:
        return sys.modules[key]
    spec = importlib.util.spec_from_file_location(key, os.path.join(HERE, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[key] = mod
    spec.loader.exec_module(mod)
    return mod
