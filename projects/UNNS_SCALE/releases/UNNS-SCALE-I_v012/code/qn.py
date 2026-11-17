import sys
sys.dont_write_bytecode=True
def spf_sieve(N):
    s=list(range(N+1))
    for i in range(2,int(N**.5)+1):
        if s[i]==i:
            for j in range(i*i,N+1,i):
                if s[j]==j: s[j]=i
    return s
def qvec(N,spf=None):
    """q[n] = largest prime with odd exponent in n(n+1), n<=N"""
    spf=spf or spf_sieve(N+2); q=[0]*(N+2)
    def odd(m):
        r={}
        while m>1:
            p=spf[m]; e=0
            while m%p==0: m//=p; e+=1
            if e&1: r[p]=1
        return r
    for n in range(1,N+1):
        s=odd(n); t=odd(n+1); S=set(s)|set(t)   # coprime so no overlap
        q[n]=max(S) if S else 1
    return q
