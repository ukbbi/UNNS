"""Finite searches for failures of observable congruence; not an exhaustive proof."""
from collections import defaultdict
from collections.abc import Callable, Iterable
from .anchor_routes import Anchor

def quotient_witness(routes: Iterable[Anchor], operation: Callable[[Anchor, Anchor], Anchor]):
    """Find (r,r',s,outputs) with equal input values but differing observed outputs."""
    groups = defaultdict(list)
    for route in routes:
        groups[route.value].append(route)
    all_routes = [r for group in groups.values() for r in group]
    for group in groups.values():
        if len(group) < 2:
            continue
        for i, r in enumerate(group):
            for rr in group[i+1:]:
                for s in all_routes:
                    a,b=operation(r,s).value,operation(rr,s).value
                    if a != b:
                        return {"r":(r.k,r.d),"r_prime":(rr.k,rr.d),"probe":(s.k,s.d),"outputs":(a,b)}
    return None
