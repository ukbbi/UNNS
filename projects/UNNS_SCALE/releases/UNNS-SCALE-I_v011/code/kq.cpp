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
int main(int argc,char**argv){ u64 Cmax=atoll(argv[1]); vector<pair<u32,u32>> Q; unsigned long long a,b; FILE*f=fopen(argv[2],"r"); while(fscanf(f,"%llu %llu",&a,&b)==2) Q.push_back({(u32)a,(u32)b}); fclose(f);
  auto k=kruskal(Cmax,Q); for(size_t i=0;i<Q.size();i++) printf("%u %u %llu\n",Q[i].first,Q[i].second,(unsigned long long)k[i]); }
