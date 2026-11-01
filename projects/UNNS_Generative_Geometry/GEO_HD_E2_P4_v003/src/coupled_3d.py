"""E2-P4 Track B (P4-E4) -- NOT STARTED beyond the P4-F110 preflight.  Provides the nonrectangularity predicate required to admit a transition to the
future coupled-target census; the broad census itself is deliberately not run (spec section 14)."""
import _boot  # noqa: F401

cl = _boot.p4("coupled_lattices")
STATUS = "NOT_STARTED"


def admissible_for_census(P, b, b2):
    """Spec 3.4: same prime set, nonrectangular source AND target lattices, distinct lattices."""
    return cl.describe(P, b)["nonrectangular"] and cl.describe(P, b2)["nonrectangular"] and cl.relation(P, b, b2) != "EQUAL"
