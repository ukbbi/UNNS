from engine import *
from itertools import permutations
from collections import Counter
def arrangements(content):
    return sorted(set(permutations(sorted(content))))
def adm_set(content,m):
    return [w for w in arrangements(content) if m%K(w)==0]
def swap_classes(content,m):
    A=set(adm_set(content,m)); seen=set(); comps=[]
    for w in sorted(A):
        if w in seen: continue
        st=[w]; seen.add(w); c=[w]
        while st:
            u=st.pop()
            for i in range(len(u)-1):
                if u[i]!=u[i+1]:
                    v=u[:i]+(u[i+1],u[i])+u[i+2:]
                    if v in A and v not in seen: seen.add(v); st.append(v); c.append(v)
        comps.append(sorted(c))
    return comps
def feeding(content):
    L=sorted(set(content))
    return {(a,b) for a in L for b in L if a!=b and gcd(a+1,b)>1}
def sccs(content):
    L=sorted(set(content)); E=feeding(content)
    reach={a:{a} for a in L}
    ch=True
    while ch:
        ch=False
        for (a,b) in E:
            n=reach[a]|reach[b]
            if n!=reach[a]: reach[a]=n; ch=True
    comps=[];seen=set()
    for a in L:
        if a in seen: continue
        c=sorted(b for b in L if b in reach[a] and a in reach[b]); seen|=set(c); comps.append(c)
    return comps
def class_count_all_sources(content, limit=None):
    """all sources in lcm-closure"""
    ks=sorted({K(w) for w in arrangements(content)})
    from math import lcm
    cl=set(); 
    # lcm closure of subsets via iterative closure
    cl=set(ks); ch=True
    while ch:
        ch=False
        for a in list(cl):
            for b in ks:
                l=lcm(a,b)
                if l not in cl: cl.add(l); ch=True
    return {m:len(swap_classes(content,m)) for m in sorted(cl)}
