import sys,json,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from engine import *
from swaps import *
from itertools import combinations as C, permutations
R={}
def hub_exists(c):
    arr=arrangements(c); Ks={w:K(w) for w in arr}
    def adj(w):
        for i in range(len(w)-1):
            if w[i]!=w[i+1]: yield w[:i]+(w[i+1],w[i])+w[i+2:]
    for h in arr:
        if all(Ks[w]%Ks[h]==0 for w in arr):
            # descent paths: reachability to h along edges with K(next)|K(cur)
            ok=True
            for w in arr:
                seen={w};st=[w]
                while st:
                    u=st.pop()
                    for v in adj(u):
                        if v not in seen and Ks[u]%Ks[v]==0: seen.add(v);st.append(v)
                if h not in seen: ok=False;break
            if ok: return True
    return False
def census(labs,k):
    hub=nohub_nosplit=split=both=0
    for c in C(labs,k):
        sp=any(v>=2 for v in class_count_all_sources(c).values())
        h=hub_exists(c)
        if sp and h: both+=1
        elif sp: split+=1
        elif h: hub+=1
        else: nohub_nosplit+=1
    return {'hub_no_split':hub,'both':both,'neither':nohub_nosplit,'split':split}
R['hub_census_3_le30']=census(range(1,31),3)
R['hub_census_4_le14']=census(range(1,15),4)
# strongly connected but never split examples
ex={}
for c in [(2,4,15),(2,5,9),(2,6,7)]:
    ex[str(c)]={'scc_blocks':sccs(c),'max_classes':max(class_count_all_sources(c).values())}
R['scc_never_split']=ex
print(R)
json.dump(R,open('../results/RESULTS_II_part6.json','w'),indent=1)
