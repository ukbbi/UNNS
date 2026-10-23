"""Analytic *reference* models. NOT a UNNS entanglement theory."""
from math import cos
OUTCOMES=(-1,1)
def quantum_reference(a,b):
    """Polarization Bell-state reference distribution."""
    return {(x,y):(1-x*y*cos(2*(a-b)))/4 for x in OUTCOMES for y in OUTCOMES}
def bell_local_shared_sign(a,b):
    """Bell-local null: shared unbiased sign; settings ignored by design."""
    return {(x,y):(0.5 if x==y else 0.0) for x in OUTCOMES for y in OUTCOMES}
def independent_null(a,b):
    return {(x,y):0.25 for x in OUTCOMES for y in OUTCOMES}
