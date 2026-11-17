// v012: exact length-height Pareto frontier for pairs (Bn,B(n+1)) inside G_Cmax.
// f_l(v) = min over walks of <= l steps from a to v of the maximum vertex (bottleneck DP, Jacobi iteration over ALL edges of G_Cmax).
// H_l(n) = f_l(B(n+1)).  tau_n(C) = min{ l : H_l(n) <= C }.  Output: n  then "l:H" at every l where H_l strictly decreases (first finite l included).
// usage: tau_exact B Cmax n1 n2 step out [STOPM]   (optional STOPM: stop iterating once H_l <= STOPM*(n+1); flag "#")
//    (n = n1, n1+step, ... <= n2)   [threads via OMP_NUM_THREADS]
#include <bits/stdc++.h>
#include <omp.h>
using namespace std; typedef unsigned long long u64; typedef uint32_t u32;
int main(int argc,char**argv){ u64 B=atoll(argv[1]); u64 Cmax=atoll(argv[2]); u64 n1=atoll(argv[3]),n2=atoll(argv[4]),st=atoll(argv[5]); const char*out=argv[6]; u64 STOPM=(argc>7)?strtoull(argv[7],0,10):0;
  vector<u32> eu,ev; eu.reserve((size_t)(0.66*Cmax)); ev.reserve((size_t)(0.66*Cmax)); for(u64 t=2;t*t<=Cmax;t++) for(u64 k=1;k*t*t<=Cmax;k++){ eu.push_back(k*(t-1)); ev.push_back(k*t*t); }
  size_t E=eu.size();  vector<u64> ns; for(u64 n=n1;n<=n2;n+=st) if(B*(n+1)<=Cmax) ns.push_back(n);
  vector<string> res(ns.size()); const u32 INF=0xFFFFFFFFu;
  #pragma omp parallel
  { vector<u32> cur(Cmax+1),nxt(Cmax+1);
    #pragma omp for schedule(dynamic,1)
    for(long i=0;i<(long)ns.size();i++){ u64 n=ns[i],a=B*n,b=B*(n+1); fill(cur.begin(),cur.end(),INF); cur[a]=a; u32 last=INF; string s=to_string(n); int l=0; bool conv=false;
      for(l=1;l<=400;l++){ nxt=cur;
        for(size_t e=0;e<E;e++){ u32 u=eu[e],v=ev[e]; u32 cu=cur[u],cv=cur[v]; if(cu!=INF){ u32 h=max(cu,v); if(h<nxt[v]) nxt[v]=h; } if(cv!=INF){ u32 h=max(cv,u); if(h<nxt[u]) nxt[u]=h; } }
        bool ch=(nxt!=cur); cur.swap(nxt); if(cur[b]<last){ last=cur[b]; s+=" "+to_string(l)+":"+to_string(last); } if(last==b) {conv=true;break;} if(STOPM && (u64)last<=STOPM*(n+1)) {conv=true;break;} if(!ch){conv=true;break;} }
      if(last==b) s+=" *"; else if(STOPM && (u64)last<=STOPM*(n+1)) s+=" #"; else if(last==INF) s+=" inf"; else s+=" ~"; // * reached the minimum possible ceiling B(n+1); ~ stalled above; inf unreachable within Cmax
      res[i]=s; } }
  FILE*fo=fopen(out,"w"); for(auto&s:res) fprintf(fo,"%s\n",s.c_str()); fclose(fo); }
