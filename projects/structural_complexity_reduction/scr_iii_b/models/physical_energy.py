"""Independent finite free-boundary square-ice dumbbell coupling evaluator.
Non-normative preflight, adapted from mathematical formula in Dryad SPMMC v1.00.
Coordinates and dimensions are in nanometers. Energy units are normalized coupling units.
"""
from math import sqrt
from itertools import product

def patch(L, spacing=260.0):
    """Returns edge spins (center x,y, unit x,y) and vertex incident (spin index, incoming sign)."""
    if L < 1: raise ValueError('L >= 1')
    edges=[]
    # Every degree-four vertex includes boundary dangling edges.
    for y in range(L):
        for x in range(L+1):
            edges.append(((x-0.5)*spacing,y*spacing,1.,0.))
    for y in range(L+1):
        for x in range(L):
            edges.append((x*spacing,(y-0.5)*spacing,0.,1.))
    verts=[]; nh=(L+1)*L
    for y in range(L):
        for x in range(L):
            # Incoming along orientation corresponds right/bottom, outgoing left/top
            verts.append(((y*(L+1)+x,1),(y*(L+1)+x+1,-1),(nh+y*L+x,1),(nh+(y+1)*L+x,-1)))
    return edges,verts

def pair_coupling(e1,e2,length=160.,width=60.,height=16.):
    x,y,ux,uy=e1; X,Y,vx,vy=e2
    rx=X-x;ry=Y-y;r=sqrt(rx*rx+ry*ry)
    if r == 0:raise ValueError('coincident centers')
    def inv(a,c):
        squared=(1.+(length/(3*r))**2*2 + (2/3)*c*length*(rx*vx+ry*vy)/r**2 - (2/3)*a*length*(rx*ux+ry*uy)/r**2-(2/9)*a*c*length**2*(ux*vx+uy*vy)/r**2)
        return 1/sqrt(squared)
    return (3/16)*(width*height)/(length*r)*(inv(1,1)+inv(-1,-1)-inv(1,-1)-inv(-1,1))

def couplings(edges, length=160.,width=60.,height=16.):
    return [(i,j,pair_coupling(edges[i],edges[j],length,width,height)) for i in range(len(edges)) for j in range(i+1,len(edges))]

def energy(state, pairs):
    # sign chosen to match local field h_i = sum_j K_ij s_j, deltaE_flip = 2*s_i*h_i
    return -sum(k*state[i]*state[j] for i,j,k in pairs)

def ice_ok(state, vertices):
    return all(sum(sign*state[idx] for idx,sign in v)==0 for v in vertices)

def enumerate_patch(L,limit=12):
    edges,vertices=patch(L);N=len(edges)
    if N>limit:raise ValueError('explicit enumeration cap')
    pairs=couplings(edges)
    best=float('inf');counts=0;ice=0;ground=[];energy_records=[]
    for s in product((-1,1),repeat=N):
        e=energy(s,pairs); g=ice_ok(s,vertices);counts+=1;ice+=g
        energy_records.append((e,g))
        if e<best-1e-14:best=e;ground=[s]
        elif abs(e-best)<=1e-14:ground.append(s)
    return {'L':L,'N':N,'states':counts,'ice_states':ice,'ice_fraction':ice/counts,'ground_energy_normalized':best,'ground_count':len(ground),'ground_all_ice':all(ice_ok(s,vertices) for s in ground),'ground_non_ice_count':sum(not ice_ok(s,vertices) for s in ground),'energy_min_ice':min(e for e,g in energy_records if g),'energy_min_non_ice':min(e for e,g in energy_records if not g)}
