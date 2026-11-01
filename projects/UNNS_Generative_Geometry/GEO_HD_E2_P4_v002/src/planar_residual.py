"""E2-P4 Track A (P4-E3) -- NOT STARTED.  This module only exposes the spec-6.4 reclassification of the completed E2-P3 corpus
(data/E2P3_PLANAR_REFERENCE.json, provenance-hashed).  The search for a proof or counterexample of CP3-A on hollow-box / sub-threshold targets
is a later release; finite evidence so far (E2-P3): 846 ENLARGE rows of those two classes in the expanded corpus, all CONTAINED."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATUS = "NOT_STARTED"


def reference():
    with open(os.path.join(ROOT, "data", "E2P3_PLANAR_REFERENCE.json"), encoding="utf-8") as fh:
        return json.load(fh)


def partition():
    return reference()["partition"]


def residual_open_targets():
    """Rows (x -> x') of the two classes for which CP3-A is open: RESIDUAL_EXCEPTIONAL_HOLLOW_BOX, RESIDUAL_SUBTHRESHOLD_BOX."""
    return reference()["residual_open"]["rows"]
