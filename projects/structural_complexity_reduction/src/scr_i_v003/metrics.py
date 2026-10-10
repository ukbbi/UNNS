from __future__ import annotations
import statistics

def median(xs):
    xs=list(xs); return float(statistics.median(xs)) if xs else 0.0

def mad(xs):
    xs=list(xs)
    if not xs:return 0.0
    m=statistics.median(xs); return float(statistics.median(abs(x-m) for x in xs))

def cell_verdict(target_count:int,preservation_ok:bool,r_candidate:float)->str:
    if target_count==0:return 'INDETERMINATE_NO_TARGETS'
    if not preservation_ok:return 'REPRESENTATION_LOSS'
    if r_candidate<=0:return 'NO_REDUCTION'
    return 'STRUCTURAL_COMPRESSION_PRESERVED'
