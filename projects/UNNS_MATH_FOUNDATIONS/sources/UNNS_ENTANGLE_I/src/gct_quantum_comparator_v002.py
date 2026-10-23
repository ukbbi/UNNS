"""QUARANTINED COMPARATOR: imports the singlet correlation, not a derived UNNS rule."""
import math

def singlet_reference(a:float,b:float)->float:
    return -math.cos(a-b)
