"""Independent distance checker (sympy factorint, plain BFS balls, no code shared with exact_lib)."""
from sympy import factorint, divisors

def nbrs(n):
    out=set()
    f=factorint(n)
    for N in divisors(n):            # forward  n -> n/N*(N+1)^2
        out.add(n//N*(N+1)**2)
    for q in divisors(n):            # backward q^2 | n :  n -> n/q^2*(q-1), q>=2
        if q>=2 and n % (q*q)==0:
            out.add(n//(q*q)*(q-1))
    out.discard(n)
    return out

def ball(n, r):
    layers=[{n}]; seen={n}
    for _ in range(r):
        nxt=set()
        for x in layers[-1]:
            for y in nbrs(x):
                if y not in seen: seen.add(y); nxt.add(y)
        layers.append(nxt)
    return layers, seen

def check_path(p):
    for a,b in zip(p,p[1:]):
        assert b in nbrs(a) , (a,b)
    return len(p)-1

def certify_distance(u, v, d, path):
    """Certify d(u,v)=d : path of length d is valid and balls of radii (ceil((d-1)/2), floor((d-1)/2)) are disjoint."""
    assert path[0]==u and path[-1]==v and check_path(path)==d
    r=(d)//2; s=d-1-r             # r+s = d-1 -> disjoint balls imply distance > d-1
    _,Bu=ball(u,r); _,Bv=ball(v,s)
    assert not (Bu & Bv), "balls intersect: distance <= d-1"
    return (r, s, len(Bu), len(Bv))
