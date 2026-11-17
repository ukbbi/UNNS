// v011: exact connection ceilings kappa(x,y) = min over ALL paths (any length) of the maximum vertex, for query pairs (B n, B (n+1)),
// via Kruskal on the SELECT-II edges {kN, k(N+1)^2} processed in increasing order of the larger endpoint m = k (N+1)^2 <= Cmax.
// usage: kruskal B Cmax nmax out.txt     (queries n=1..nmax with B(n+1) <= Cmax). Output lines: n kappa (0 if > Cmax)
#include <bits/stdc++.h>
using namespace std; typedef unsigned long long u64; typedef uint32_t u32;
static vector<u32> par;
static inline u32 find(u32 x){ while(par[x]!=x){ par[x]=par[par[x]]; x=par[x]; } return x; }
int main(int argc,char**argv){ u64 B=atoll(argv[1]), Cmax=atoll(argv[2]), nmax=atoll(argv[3]); const char*out=argv[4];
  par.resize(Cmax+1); for(u64 i=0;i<=Cmax;i++) par[i]=i;
  vector<u64> kap(nmax+2,0); vector<char> done(nmax+2,0);
  unordered_map<u32,vector<u32>> L; L.reserve(nmax*2); // root -> list of query ids (query id n)
  u64 qn=0; for(u64 n=1;n<=nmax;n++){ if(B*(n+1)>Cmax) break; qn=n; L[B*n].push_back(n); L[B*(n+1)].push_back(n); }
  auto ends=[&](u32 n,u32&a,u32&b){ a=B*n; b=B*(n+1); };
  const u64 BLK=1ULL<<24; vector<pair<u32,u32>> E; u64 answered=0;
  for(u64 lo=1; lo<=Cmax; lo+=BLK){ u64 hi=min(lo+BLK,Cmax+1); E.clear();
    for(u64 t=2;t*t<hi;t++){ u64 t2=t*t; u64 k0=(lo+t2-1)/t2; for(u64 k=k0;k*t2<hi;k++) E.push_back({(u32)(k*t2),(u32)(k*(t-1))}); }
    sort(E.begin(),E.end());
    for(auto&e:E){ u32 ra=find(e.first), rb=find(e.second); if(ra==rb) continue;
      auto ia=L.find(ra), ib=L.find(rb); size_t sa=ia==L.end()?0:ia->second.size(), sb=ib==L.end()?0:ib->second.size();
      u32 big=ra, small=rb; if(sa<sb){ big=rb; small=ra; }
      auto is=L.find(small); par[small]=big;   // merge into the root holding the larger query list
      if(is!=L.end()){ vector<u32> lst=move(is->second); L.erase(is); auto& dst=L[big];
        for(u32 n:lst){ if(!done[n]){ u32 a,b; ends(n,a,b); if(find(a)==find(b)){ done[n]=1; kap[n]=e.first; answered++; continue; } } dst.push_back(n); } } }
    if(((lo-1)/BLK)%8==0) fprintf(stderr,"lo=%llu answered %llu/%llu\n",(unsigned long long)lo,(unsigned long long)answered,(unsigned long long)qn); }
  FILE*fo=fopen(out,"w"); for(u64 n=1;n<=qn;n++) fprintf(fo,"%llu %llu\n",(unsigned long long)n,(unsigned long long)kap[n]); fclose(fo);
  fprintf(stderr,"done answered %llu of %llu\n",(unsigned long long)answered,(unsigned long long)qn); }
