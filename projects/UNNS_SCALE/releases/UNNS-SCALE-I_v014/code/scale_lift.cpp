// v014 scale_lift: exact d_{G_W}(A n, A(n+1)) for W = M*(n+1), provided d <= 2*R (R=3 by default); else reports 9 (">2R").
// Balls of radius R computed exactly inside G_W (all vertices <= W). Layers < R carry factorizations; the last layer is values only.
// usage: scale_lift A M nlo nhi out [R=3] [threads]   (list mode: env NLIST=file of n values, nlo/nhi ignored except for the sieve bound; output lines "n d")
// (v014 range mode and list mode share the same core)   -> out: one digit per n (distance 0..2R, or 9 if > 2R), plus lines with n for d>=lim in out.list
#include <bits/stdc++.h>
#include <omp.h>
using namespace std;
typedef unsigned long long u64; typedef unsigned __int128 u128; typedef vector<pair<u64,int>> Fac;
static vector<uint32_t> spf;
static Fac factor_small(u64 n){ Fac f; while(n>1){ u64 p=spf[n]; int e=0; while(n%p==0){n/=p;e++;} f.push_back({p,e}); } return f; }
static Fac comb(const Fac&a,const Fac&b,int sa,int sb){ Fac r; size_t i=0,j=0; while(i<a.size()||j<b.size()){
  int e; u64 p; if(j==b.size()||(i<a.size()&&a[i].first<b[j].first)){ p=a[i].first; e=a[i].second*sa; i++; }
  else if(i==a.size()||b[j].first<a[i].first){ p=b[j].first; e=b[j].second*sb; j++; } else { p=a[i].first; e=a[i].second*sa+b[j].second*sb; i++; j++; }
  if(e) r.push_back({p,e}); } return r; }
static void divs(const Fac&f,int halve,u64 lim,size_t k,u64 cur,vector<u64>&out){
  if(k==f.size()){ out.push_back(cur); return; }
  int e=f[k].second; if(halve) e/=2; u64 v=cur;
  for(int a=0;a<=e;a++){ if(v>lim) break; divs(f,halve,lim,k+1,v,out); if(a<e){ if((u128)v*f[k].first>lim) break; v*=f[k].first; } } }
struct V{ u64 y; Fac f; };
// neighbours of y inside G_C; withfac=false -> values only
static void nbrs(u64 y,const Fac&f,u64 C,bool withfac,vector<V>&out){
  vector<u64> d; divs(f,0,C/y,0,1,d);
  for(u64 N:d){ u128 z=(u128)(y/N)*(N+1)*(N+1); if(z>C) continue; V v; v.y=(u64)z; if(withfac){ Fac g=comb(f,factor_small(N),1,-1); v.f=comb(g,factor_small(N+1),1,2);} out.push_back(move(v)); }
  vector<u64> qs; divs(f,1,~0ULL,0,1,qs);
  for(u64 q:qs){ if(q<2) continue; V v; v.y=y/q/q*(q-1); if(withfac){ Fac g=comb(f,factor_small(q),1,-2); v.f=comb(g,factor_small(q-1),1,1);} out.push_back(move(v)); } }
// ball of radius R from (x,fx): returns sorted vector of (value,dist) with minimal dist
static void ball(u64 x,const Fac&fx,u64 C,int R,vector<pair<u64,int>>&res,unordered_map<u64,u64>*par=nullptr){
  res.clear(); res.push_back({x,0}); vector<V> cur; cur.push_back({x,fx}); unordered_set<u64> seen; seen.insert(x);
  for(int r=1;r<=R;r++){ bool wf=(r<R); vector<V> nxt; for(auto&v:cur){ vector<V> o; nbrs(v.y,v.f,C,wf,o); for(auto&w:o) if(seen.insert(w.y).second){ if(par) (*par)[w.y]=v.y; nxt.push_back(move(w)); } }
    for(auto&w:nxt) res.push_back({w.y,r}); cur.swap(nxt); }
  sort(res.begin(),res.end()); }
static Fac fxm(const Fac&FB,u64 m){ return comb(FB,factor_small(m),1,1); }
int main(int argc,char**argv){ u64 A=atoll(argv[1]),M=atoll(argv[2]),nlo=atoll(argv[3]),nhi=atoll(argv[4]); const char*out=argv[5]; int R=argc>6?atoi(argv[6]):3; int th=argc>7?atoi(argv[7]):2;
  u64 L=(u64)sqrtl((long double)M*(nhi+1))+5; L=max<u64>(L,nhi+2); spf.assign(L+1,0); for(u64 i=2;i<=L;i++) if(!spf[i]) for(u64 j=i;j<=L;j+=i) if(!spf[j]) spf[j]=i;
  Fac FA=factor_small(A); omp_set_num_threads(th); const char*nl=getenv("NLIST");
  auto solve=[&](u64 n)->int{ u64 W=M*(n+1); u64 x=A*n,y=A*(n+1); vector<pair<u64,int>> a,b; ball(x,fxm(FA,n),W,R,a); ball(y,fxm(FA,n+1),W,R,b);
    int best=99; size_t i=0,j=0; while(i<a.size()&&j<b.size()){ if(a[i].first<b[j].first) i++; else if(b[j].first<a[i].first) j++; else { best=min(best,a[i].second+b[j].second); i++; j++; } }
    return best<=2*R?best:9999; };
  if(nl&&getenv("PATHS")){ vector<u64> ns; { FILE*f=fopen(nl,"r"); unsigned long long v; while(fscanf(f,"%llu",&v)==1) ns.push_back(v); fclose(f); } vector<string> lines(ns.size());
    #pragma omp parallel for schedule(dynamic,1)
    for(long long i=0;i<(long long)ns.size();i++){ u64 n=ns[i],W=M*(n+1),x=A*n,y=A*(n+1); vector<pair<u64,int>> a,b; unordered_map<u64,u64> pa,pb; ball(x,fxm(FA,n),W,R,a,&pa); ball(y,fxm(FA,n+1),W,R,b,&pb);
      int best=99; u64 z=0; size_t p=0,q=0; while(p<a.size()&&q<b.size()){ if(a[p].first<b[q].first) p++; else if(b[q].first<a[p].first) q++; else { if(a[p].second+b[q].second<best){ best=a[p].second+b[q].second; z=a[p].first; } p++; q++; } }
      string s=to_string(n)+" "+to_string(best<=2*R?best:9999); if(best<=2*R){ vector<u64> L; for(u64 v=z;v!=x;v=pa[v]) L.push_back(v); L.push_back(x); reverse(L.begin(),L.end()); for(u64 v=z;v!=y;){ v=pb[v]; L.push_back(v); } for(u64 v:L) s+=" "+to_string(v); } lines[i]=s; }
    FILE*fo=fopen(out,"w"); for(auto&l:lines) fprintf(fo,"%s\n",l.c_str()); fclose(fo); return 0; }
  if(nl){ vector<u64> ns; { FILE*f=fopen(nl,"r"); unsigned long long v; while(fscanf(f,"%llu",&v)==1) ns.push_back(v); fclose(f); } vector<int> d(ns.size());
    #pragma omp parallel for schedule(dynamic,4)
    for(long long i=0;i<(long long)ns.size();i++) d[i]=solve(ns[i]);
    FILE*fo=fopen(out,"w"); for(size_t i=0;i<ns.size();i++) fprintf(fo,"%llu %d\n",(unsigned long long)ns[i],d[i]); fclose(fo); return 0; }
  vector<char> dist(nhi-nlo,'9');
  #pragma omp parallel for schedule(dynamic,64)
  for(long long n=nlo;n<(long long)nhi;n++){ int best=solve(n); if(best<=2*R) dist[n-nlo]='0'+best; }
  FILE*fo=fopen(out,"w"); fwrite(dist.data(),1,dist.size(),fo); fclose(fo); return 0; }
