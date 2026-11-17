// v010: exact radius-2 balls inside the ceiling C (all vertices <= C) for x = B*m; meeting test between consecutive m.
// usage: ball B nlo nhi C outfile [witness_dump]
// For each n in [nlo,nhi): meet = min z in Ball2_C(Bn) ∩ Ball2_C(B(n+1)) (0 if none); also the sizes.
#include <bits/stdc++.h>
#include <thread>
#include <atomic>
using namespace std;
typedef unsigned long long u64; typedef unsigned __int128 u128; typedef uint32_t u32;
typedef vector<pair<u64,int>> Fac;
static vector<uint32_t> spf; static thread_local u64 C;
static Fac factor_small(u64 n){ Fac f; if(n<=1) return f; // n <= sieve limit
  while(n>1){ u64 p=spf[n]; int e=0; while(n%p==0){n/=p;e++;} f.push_back({p,e}); } return f; }
static Fac comb(const Fac&a,const Fac&b,int sa,int sb){ // sa*a + sb*b (exponents), drop zeros; both sorted
  Fac r; size_t i=0,j=0; while(i<a.size()||j<b.size()){
    if(j==b.size()||(i<a.size()&&a[i].first<b[j].first)){ r.push_back({a[i].first,a[i].second*sa}); i++; }
    else if(i==a.size()||b[j].first<a[i].first){ r.push_back({b[j].first,b[j].second*sb}); j++; }
    else { int e=a[i].second*sa+b[j].second*sb; if(e) r.push_back({a[i].first,e}); i++; j++; } }
  Fac q; for(auto&t:r) if(t.second) q.push_back(t); return q; }
static void divs(const Fac&f,int halve,u64 lim,size_t k,u64 cur,vector<u64>&out){
  if(k==f.size()){ out.push_back(cur); return; }
  int e=f[k].second; if(halve) e/=2; u64 v=cur;
  for(int a=0;a<=e;a++){ if(v>lim) break; divs(f,halve,lim,k+1,v,out); if(a<e){ if((u128)v*f[k].first>lim) break; v*=f[k].first; } } }
struct V{ u64 y; Fac f; };
static void nbrs(u64 y,const Fac&f,vector<V>&out){
  u64 lim=C/y; vector<u64> d; divs(f,0,lim,0,1,d);
  for(u64 N:d){ u128 z=(u128)(y/N)*(N+1)*(N+1); if(z<=C){ Fac fN=factor_small(N), fN1=factor_small(N+1); Fac g=comb(f,fN,1,-1); g=comb(g,fN1,1,2); out.push_back({(u64)z,g}); } }
  vector<u64> qs; divs(f,1,~0ULL,0,1,qs);
  for(u64 q:qs){ if(q<2) continue; u64 N=q-1; u64 z=y/q/q*N; Fac fq=factor_small(q), fN=factor_small(N); Fac g=comb(f,fq,1,-2); g=comb(g,fN,1,1); out.push_back({z,g}); } }
static void ball2(u64 x,const Fac&fx,vector<u64>&B,u64*s1=nullptr){
  B.clear(); B.push_back(x); vector<V> l1; nbrs(x,fx,l1); if(s1)*s1=l1.size();
  for(auto&v:l1){ B.push_back(v.y); vector<V> l2; nbrs(v.y,v.f,l2); for(auto&w:l2) B.push_back(w.y); }
  sort(B.begin(),B.end()); B.erase(unique(B.begin(),B.end()),B.end()); }

// conn2: link the remaining vertices B*m to the hub (component of 1 in G_{Cs}) by bounded BFS inside the window.
static vector<u32> par; static inline u32 find(u32 x){ while(par[x]!=x){ par[x]=par[par[x]]; x=par[x]; } return x; }
static void build_uf(u64 Cmax){ par.assign(Cmax+1,0); for(u64 i=0;i<=Cmax;i++) par[i]=i; const u64 BLK=1ULL<<24; vector<pair<u32,u32>> E;
  for(u64 lo=1; lo<=Cmax; lo+=BLK){ u64 hi=min(lo+BLK,Cmax+1); E.clear();
    for(u64 t=2;t*t<hi;t++){ u64 t2=t*t; for(u64 k=(lo+t2-1)/t2;k*t2<hi;k++) E.push_back({(u32)(k*t2),(u32)(k*(t-1))}); }
    sort(E.begin(),E.end()); for(auto&e:E){ u32 ra=find(e.first), rb=find(e.second); if(ra!=rb) par[ra]=rb; } } }
int main(int argc,char**argv){ C=1000000000000ULL; const u64 Cs=1000000000ULL; const char*inf=argv[1],*outf=argv[2]; u64 MULT=argc>5?strtoull(argv[5],0,10):1000000ULL; int RMAX=atoi(argv[3]); size_t CAP=(size_t)atoll(argv[4]);
  spf.assign(1000003,0); for(u64 i=2;i<=1000002;i++) if(!spf[i]) for(u64 j=i;j<=1000002;j+=i) if(!spf[j]) spf[j]=i;
  build_uf(Cs); u32 g=find(1); fprintf(stderr,"hub root %u\n",g);
  vector<u64> todo; { FILE*f=fopen(inf,"r"); unsigned long long m; char buf[256]; while(fscanf(f,"%llu %255[^\n]",&m,buf)==2) todo.push_back(m); fclose(f); }
  Fac fB; { u64 n=MULT; for(u64 p=2;p*p<=n;p++){ if(n%p==0){int e=0; while(n%p==0){n/=p;e++;} fB.push_back({p,e});} } if(n>1) fB.push_back({n,1}); }
  vector<string> res(todo.size()); atomic<size_t> next(0);
  auto work=[&](){ for(;;){ size_t i=next.fetch_add(1); if(i>=todo.size()) return; u64 m=todo[i]; C=(argc>6&&atoi(argv[6])==1)? MULT*m*(MULT==1?1000000ULL:1ULL) : 1000000000000ULL; Fac fm=factor_small(m); Fac fx=comb(fB,fm,1,1); u64 x=MULT*m;
      vector<unordered_map<u64,Fac>> layers; layers.push_back({{x,fx}}); unordered_set<u64> seen{x}; int found=-1; u64 fv=0; unordered_map<u64,u64> parent; parent[x]=0;
      auto chk=[&](u64 y){ return y<=Cs && find((u32)y)==g; };
      if(chk(x)) { found=0; fv=x; }
      for(int r=1;r<=RMAX&&found<0;r++){ unordered_map<u64,Fac> nxt; for(auto&kv:layers.back()){ vector<V> o; nbrs(kv.first,kv.second,o); for(auto&w:o){ if(seen.count(w.y)||nxt.count(w.y)) continue; nxt[w.y]=w.f; parent[w.y]=kv.first; if(chk(w.y)&&found<0){ found=r; fv=w.y; } } if(found>=0) break; }
        for(auto&kv:nxt) seen.insert(kv.first); layers.push_back(move(nxt)); if(seen.size()>CAP) break; }
      u64 pmax=0; string path; if(found>=0){ u64 v=fv; while(v){ pmax=max(pmax,v); path=to_string(v)+(path.empty()?"":">")+path; v=parent[v]; } } res[i]=to_string(m)+" "+to_string(found)+" "+to_string(fv)+" "+to_string(seen.size())+" "+to_string(pmax)+" "+path; } };
  thread t1(work), t2(work); t1.join(); t2.join();
  FILE*fo=fopen(outf,"w"); size_t ok=0; for(auto&s:res){ fprintf(fo,"%s\n",s.c_str()); if(s.find(" -1 ")==string::npos) ok++; } fclose(fo); printf("searched %zu, linked %zu\n",todo.size(),ok); }
