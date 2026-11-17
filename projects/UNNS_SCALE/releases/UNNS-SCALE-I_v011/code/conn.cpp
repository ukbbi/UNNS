// v011: window connectivity certificate for the million-spaced pairs (B=1e6, C=1e12).
//  Reduction lemma: B m --(backward q=1000)--> 999 m.      Hub: component of vertex 1 in G_{Cs}, Cs=1e9 (exact union-find).
//  Hard vertices (999 m not in hub): m = m' p with p>25000 prime: p-multiples subgraph ~ G_{C/p} (scaling lemma);
//  flip gadget: s p -- s (p+1)^2 -- s d (p+1-d) for d | p+1 (backward q=(p+1)/d).  Certificate = exact union-find data + explicit (s,d).
#include <bits/stdc++.h>
using namespace std; typedef unsigned long long u64; typedef uint32_t u32;
static vector<u32> par;
static inline u32 find(u32 x){ while(par[x]!=x){ par[x]=par[par[x]]; x=par[x]; } return x; }
// Kruskal with optional queries; returns kappa per query (0 if unanswered); par holds the final union-find
static vector<u64> kruskal(u64 Cmax, const vector<pair<u32,u32>>&Q){
  par.assign(Cmax+1,0); for(u64 i=0;i<=Cmax;i++) par[i]=i; vector<u64> kap(Q.size(),0); vector<char> done(Q.size(),0);
  unordered_map<u32,vector<u32>> L; for(u32 i=0;i<Q.size();i++){ L[Q[i].first].push_back(i); L[Q[i].second].push_back(i); }
  const u64 BLK=1ULL<<24; vector<pair<u32,u32>> E;
  for(u64 lo=1; lo<=Cmax; lo+=BLK){ u64 hi=min(lo+BLK,Cmax+1); E.clear();
    for(u64 t=2;t*t<hi;t++){ u64 t2=t*t; for(u64 k=(lo+t2-1)/t2;k*t2<hi;k++) E.push_back({(u32)(k*t2),(u32)(k*(t-1))}); }
    sort(E.begin(),E.end());
    for(auto&e:E){ u32 ra=find(e.first), rb=find(e.second); if(ra==rb) continue;
      auto ia=L.find(ra), ib=L.find(rb); size_t sa=ia==L.end()?0:ia->second.size(), sb=ib==L.end()?0:ib->second.size();
      u32 big=ra, small=rb; if(sa<sb){ big=rb; small=ra; }
      auto is=L.find(small); par[small]=big;
      if(is!=L.end()){ vector<u32> lst=move(is->second); L.erase(is); auto&dst=L[big];
        for(u32 i:lst){ if(!done[i]){ if(find(Q[i].first)==find(Q[i].second)){ done[i]=1; kap[i]=e.first; continue; } } dst.push_back(i); } } } }
  return kap; }
int main(int argc,char**argv){ const u64 C=1000000000000ULL, Cs=1000000000ULL; const int MP=40, SMAX=2000; u64 NM=999999+1; // m = 1..1e6
  // sieve to 1e6+1
  vector<u32> spf(1000002,0); for(u32 i=2;i<=1000001;i++) if(!spf[i]) for(u32 j=i;j<=1000001;j+=i) if(!spf[j]) spf[j]=i;
  // phase-1 kappa(s0=999 m', s), m'=1..MP, s=1..SMAX in G_{5e7}
  vector<pair<u32,u32>> Q; for(int mp=1;mp<=MP;mp++) for(int s=1;s<=SMAX;s++) Q.push_back({(u32)(999*mp),(u32)s});
  vector<u64> kap=kruskal(50000000ULL,Q); fprintf(stderr,"phase1 done\n");
  auto K=[&](int mp,int s)->u64{ return kap[(mp-1)*SMAX+(s-1)]; };
  kruskal(Cs,{}); u32 g=find(1); fprintf(stderr,"hub built, root %u\n",g);
  u64 nok=0, nflip=0, nfail=0, nother=0; vector<u64> failed; FILE*fo=fopen(argv[1],"w");
  vector<char> linked(NM+1,0);
  for(u64 m=1;m<=1000000;m++){ u64 v=999*m; if(find(v)==g){ linked[m]=1; nok++; continue; }
    // largest prime factor of m
    u64 mm=m, p=1; while(mm>1){ p=spf[mm]; while(mm%p==0) mm/=p; }
    u64 mp=m; while(mp%p==0) mp/=p; // m' (p exactly once if p>1000)
    if(p<25000 || mp>MP || (m/mp)!=p){ nother++; fprintf(fo,"%llu other\n",(unsigned long long)m); continue; }
    u64 T=C/p; bool ok=false; u64 bs=0,bd=0;
    // divisors of p+1
    vector<u64> ds; { u64 a=p+1; vector<pair<u64,int>> f; while(a>1){ u64 q=spf[a]; int e=0; while(a%q==0){a/=q;e++;} f.push_back({q,e}); } ds={1}; for(auto&pe:f){ size_t sz=ds.size(); u64 pw=1; for(int e=1;e<=pe.second;e++){ pw*=pe.first; for(size_t i=0;i<sz;i++) ds.push_back(ds[i]*pw); } } }
    for(u64 s=1;s<=SMAX && s*(p+1)*(p+1)<=C && !ok;s++){ u64 kk=K((int)mp,(int)s); if(!kk||kk>T) continue;
      for(u64 d:ds){ if(d>=p+1) continue; u64 q=(p+1)/d; if(q<2) continue; u64 t=s*d*(p+1-d); if(t<=Cs && find(t)==g){ ok=true; bs=s; bd=d; break; } } }
    if(ok){ linked[m]=1; nflip++; fprintf(fo,"%llu flip p=%llu mprime=%llu s=%llu d=%llu\n",(unsigned long long)m,(unsigned long long)p,(unsigned long long)mp,(unsigned long long)bs,(unsigned long long)bd); }
    else { nfail++; failed.push_back(m); fprintf(fo,"%llu fail p=%llu mprime=%llu\n",(unsigned long long)m,(unsigned long long)p,(unsigned long long)mp); } }
  fclose(fo);
  u64 allpairs=0, bad=0; for(u64 n=1;n<=999999;n++){ if(linked[n]&&linked[n+1]) allpairs++; else bad++; }
  printf("vertices m=1..1e6: hub-direct %llu, flip-linked %llu, fail %llu, other %llu\npairs connected (both endpoints linked to hub): %llu of 999999 ; not shown connected: %llu\n",(unsigned long long)nok,(unsigned long long)nflip,(unsigned long long)nfail,(unsigned long long)nother,(unsigned long long)allpairs,(unsigned long long)bad); }
