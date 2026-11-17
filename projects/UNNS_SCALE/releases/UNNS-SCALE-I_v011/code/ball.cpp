// v010: exact radius-2 balls inside the ceiling C (all vertices <= C) for x = B*m; meeting test between consecutive m.
// usage: ball B nlo nhi C outfile [witness_dump]
// For each n in [nlo,nhi): meet = min z in Ball2_C(Bn) ∩ Ball2_C(B(n+1)) (0 if none); also the sizes.
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64; typedef unsigned __int128 u128;
typedef vector<pair<u64,int>> Fac;
static vector<uint32_t> spf; static u64 C;
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
int main(int argc,char**argv){ u64 Bs=atoll(argv[1]), lo=atoll(argv[2]), hi=atoll(argv[3]); C=strtoull(argv[4],0,10); const char*out=argv[5];
  u64 L=(u64)sqrtl((long double)C)+3; spf.assign(L+1,0); for(u64 i=2;i<=L;i++) if(!spf[i]) for(u64 j=i;j<=L;j+=i) if(!spf[j]) spf[j]=i;
  // factor B and m via trial division using spf (m <= L assumed for window runs; else trial)
  auto fac=[&](u64 n){ Fac f; for(u64 p=2;p*p<=n;p++){ if(n%p==0){int e=0; while(n%p==0){n/=p;e++;} f.push_back({p,e});} } if(n>1) f.push_back({n,1}); return f; };
  Fac fB=fac(Bs); auto fx=[&](u64 m){ Fac fm; if(m<=L) fm=factor_small(m); else fm=fac(m); return comb(fB,fm,1,1); };
  FILE*fo=fopen(out,"wb"); vector<u64> b0,b1; u64 s0,s1; ball2(Bs*lo,fx(lo),b0,&s0); u64 nfail=0,total=0; size_t maxball=0;
  for(u64 n=lo;n<hi;n++){ u64 x1=Bs*(n+1); if(x1>C){ fprintf(stderr,"endpoint above ceiling\n"); return 1; } ball2(x1,fx(n+1),b1,&s1);
    u64 z=0; size_t i=0,j=0; while(i<b0.size()&&j<b1.size()){ if(b0[i]<b1[j]) i++; else if(b1[j]<b0[i]) j++; else { z=b0[i]; break; } }
    u64 rec[4]={n,z,(u64)b0.size(),(u64)b1.size()}; fwrite(rec,8,4,fo); total++; if(!z) nfail++; maxball=max(maxball,max(b0.size(),b1.size()));
    b0.swap(b1); if(n%100000==0){ fprintf(stderr,"n=%llu fail so far %llu\n",(unsigned long long)n,(unsigned long long)nfail); } }
  fclose(fo); printf("pairs %llu  no-meet %llu  maxball %zu\n",(unsigned long long)total,(unsigned long long)nfail,maxball); }
