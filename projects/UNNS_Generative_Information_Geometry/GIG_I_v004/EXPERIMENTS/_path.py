import os
import sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
RESULTS = os.path.join(ROOT, "RESULTS")
CERTS = os.path.join(ROOT, "CERTIFICATES")
sys.path.insert(0, os.path.join(ROOT, "ENGINE"))
import _v3path  # noqa: E402,F401
sys.path.insert(0, os.path.join(_v3path.V003, "EXPERIMENTS"))
