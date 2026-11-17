// v011: exhaustive check of the barrier theorems on the finite graph G_C (all edges {kN,k(N+1)^2} with k(N+1)^2 <= C):
//  (a) large-prime invariance: p > sqrt(C)  => v_p constant on every connected component;
//  (b) parity invariance: (p+1)^2 > C       => v_p mod 2 constant on every component;
//  also prints number of components, #isolated vertices, size of the giant component.
#include <bits/stdc++.h>
using namespace std; typedef unsigned long long u64; typedef uint32_t u32;
int main(int argc,char**argv){ u64 C=atoll(argv[1]); vector<u32> par(C+1); iota(par.begin(),par.end(),0);
  function<u32(u32)> find=[&](u32 x){ while(par[x]!=x){ par[x]=par[par[x]]; x=par[x]; } return x; };
  for(u64 t=2;t*t<=C;t++) for(u64 k=1;k*t*t<=C;k++){ u32 a=find(k*t*t), b=find(k*(t-1)); if(a!=b) par[a]=b; }
  vector<u32> spf(C+1,0); for(u64 i=2;i<=C;i++) if(!spf[i]) for(u64 j=i;j<=C;j+=i) if(!spf[j]) spf[j]=i;
  u64 sq=(u64)sqrtl((long double)C); // v_p of x for p > sq (exact), and parity for p with (p+1)^2 > C
  auto big=[&](u64 x,bool parity){ vector<pair<u64,int>> r; while(x>1){ u64 p=spf[x]; int e=0; while(x%p==0){x/=p;e++;} bool cond= parity? ((p+1)*(p+1)>C) : (p>sq); if(cond && (!parity || (e&1))) r.push_back({p,parity?1:e}); } return r; };
  u64 bad1=0,bad2=0; vector<u32> rep(C+1,0); unordered_map<u32,u64> sz;
  for(u64 x=1;x<=C;x++){ u32 r=find(x); sz[r]++; if(!rep[r]){ rep[r]=x; continue; } auto a=big(x,false), b=big(rep[r],false); if(a!=b) bad1++; auto c=big(x,true), d=big(rep[r],true); if(c!=d) bad2++; }
  u64 iso=0,giant=0; for(auto&kv:sz){ if(kv.second==1) iso++; giant=max(giant,kv.second); }
  printf("C=%llu components=%zu isolated=%llu giant=%llu  violations: large-prime(v_p exact, p>sqrtC)=%llu parity((p+1)^2>C)=%llu\n",(unsigned long long)C,sz.size(),(unsigned long long)iso,(unsigned long long)giant,(unsigned long long)bad1,(unsigned long long)bad2); }
