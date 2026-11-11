"""Independent definition-level neighbour engine (no factorization): used only to cross-check rn_core for x<=~20000."""
def nbrs(x):
    F=sorted(x*(d+1)**2//d for d in range(1,x+1) if x%d==0)
    I=[]; q=2
    while q*q<=x:
        if x%(q*q)==0: I.append(x*(q-1)//(q*q))
        q+=1
    return F,sorted(I,reverse=True)
def edge_graph(B):
    """all edges {kN,k(N+1)^2} with both ends<=B (brute force from the grammar itself)."""
    adj={}
    N=1
    while (N+1)**2<=B:
        k=1
        while k*(N+1)**2<=B:
            a,b=k*N,k*(N+1)**2
            adj.setdefault(a,set()).add(b);adj.setdefault(b,set()).add(a);k+=1
        N+=1
    return adj
