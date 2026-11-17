// (core of ball.cpp, reused; v012 ladder) v010: exact radius-2 balls inside the ceiling C (all vertices <= C) for x = B*m; meeting test between consecutive m.
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


// v012 ladder: exact bidirectional distance d_W(Bn,B(n+1)) inside G_W (all vertices <= W) for a ladder of ceilings W, with a node cap.
// usage: ladder B RMAX CAP outfile n W1 W2 ...  -> lines "n W dist" (dist>=0 exact) or "n W >r" (no meeting up to radius r each side / cap hit: tau > r_total_explored)
static Fac FB;
static Fac fxm(u64 m){ Fac fm; u64 n=m; for(u64 p=2;p*p<=n;p++){ if(n%p==0){int e=0; while(n%p==0){n/=p;e++;} fm.push_back({p,e});} } if(n>1) fm.push_back({n,1}); return comb(FB,fm,1,1); }
struct Lay{ vector<unordered_map<u64,Fac>> L; unordered_set<u64> seen; };
static void expand(Lay&A){ unordered_map<u64,Fac> nxt; for(auto&kv:A.L.back()){ vector<V> o; nbrs(kv.first,kv.second,o); for(auto&w:o) if(!A.seen.count(w.y)&&!nxt.count(w.y)) nxt[w.y]=w.f; } for(auto&kv:nxt) A.seen.insert(kv.first); A.L.push_back(move(nxt)); }
int main(int argc,char**argv){ u64 Bs=atoll(argv[1]); int RMAX=atoi(argv[2]); size_t CAP=strtoull(argv[3],0,10); const char*out=argv[4]; u64 n=strtoull(argv[5],0,10);
  vector<u64> Ws; u64 Wm=0; for(int i=6;i<argc;i++){ Ws.push_back(strtoull(argv[i],0,10)); Wm=max(Wm,Ws.back()); }
  u64 L=(u64)sqrtl((long double)Wm)+3; spf.assign(L+1,0); for(u64 i=2;i<=L;i++) if(!spf[i]) for(u64 j=i;j<=L;j+=i) if(!spf[j]) spf[j]=i;
  { u64 m=Bs; for(u64 p=2;p*p<=m;p++){ if(m%p==0){int e=0; while(m%p==0){m/=p;e++;} FB.push_back({p,e});} } if(m>1) FB.push_back({m,1}); }
  FILE*fo=fopen(out,"a"); u64 x=Bs*n,y=Bs*(n+1); Fac fx=fxm(n),fy=fxm(n+1);
  for(u64 W:Ws){ if(y>W){ fprintf(fo,"%llu %llu below\n",(unsigned long long)n,(unsigned long long)W); continue; }
    C=W; Lay A,Bb; A.L.push_back({{x,fx}}); A.seen.insert(x); Bb.L.push_back({{y,fy}}); Bb.seen.insert(y); int dW=-1; int ra=0,rb=0; bool capped=false;
    for(int tot=0;tot<=2*RMAX&&dW<0;tot++){ int a=(tot+1)/2,b=tot/2; if(A.seen.size()>CAP||Bb.seen.size()>CAP){capped=true;break;}
      while((int)A.L.size()<=a){ expand(A); } while((int)Bb.L.size()<=b){ expand(Bb); } ra=a; rb=b;
      for(auto&kv:A.L[a]) if(Bb.seen.count(kv.first)){ dW=tot; break; }
      if(dW<0) for(auto&kv:Bb.L[b]) if(A.seen.count(kv.first)){ dW=tot; break; } }
    if(dW>=0) fprintf(fo,"%llu %llu %d\n",(unsigned long long)n,(unsigned long long)W,dW); else fprintf(fo,"%llu %llu >%d%s\n",(unsigned long long)n,(unsigned long long)W,ra+rb,capped?"cap":""); fflush(fo); }
  fclose(fo); return 0; }
