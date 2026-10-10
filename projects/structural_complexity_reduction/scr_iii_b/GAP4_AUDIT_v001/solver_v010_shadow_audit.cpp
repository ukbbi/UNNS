// AUDIT-ONLY shadow variant of solver_v010.cpp (does NOT replace it). Identical double-precision traversal;
// additionally re-evaluates every pruning decision in IEEE binary128 (__float128, unit roundoff ~9.6e-35) and independently
// re-implements the violation-filter prune. Usage: shadow INSTANCE seconds
#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <string>
#include <vector>
#include <quadmath.h>
using namespace std;
typedef __float128 Q;
static inline double qd(Q x){return (double)x;}
struct Solver {
 int n=0, nv=0; vector<vector<double>> k; vector<uint64_t> vertex, plusin;
 vector<int> spin; uint64_t bestid=0; double best= numeric_limits<double>::infinity();
 uint64_t nodes=0; bool timed=false; bool want_violation=false; double root_lower=0, scale=0;
 chrono::steady_clock::time_point deadline;
 // shadow
 vector<vector<Q>> kq; vector<Q> TT; Q bestq=0; Q Sq=0;
 uint64_t prune_bound=0, prune_viol=0, viol_prune_mismatch=0, bound_violations=0, leaf_updates=0;
 double min_slack_over_S=1e300, max_dbl_bound_err_over_S=0, max_leaf_err_over_S=0, min_slack_prune_ratio=1e300;
 double bound(int d, double acc){
   double l=acc;
   for(int j=d;j<n;j++){
     double field=0;
     for(int i=0;i<d;i++)field+=k[i][j]*spin[i];
     l-=fabs(field);
     for(int h=j+1;h<n;h++)l-=fabs(k[j][h]);
   }
   return l-1e-11*max(1.0,scale);
 }
 bool possible_violation(int d){
   if(!want_violation) return true;
   for(size_t v=0;v<vertex.size();v++){
     uint64_t mask=vertex[v];
     int count=0, left=0;
     for(int i=0;i<n;i++)if((mask>>i)&1ULL){if(i<d)count+=(spin[i]>0)==(((plusin[v]>>i)&1ULL)!=0);else left++;}
     if(count>2 || count+left<2) return true;
     if(left>0) return true;
   }
   return false;
 }
 bool violates(){
   for(size_t v=0;v<vertex.size();v++){auto m=vertex[v];int c=0;for(int i=0;i<n;i++) if((m>>i)&1ULL)c+=((spin[i]>0)==(((plusin[v]>>i)&1ULL)!=0)); if(c!=2)return true;}
   return false;
 }
 // independent popcount re-implementation of "no violation possible": every vertex fully assigned and exactly 2 'in'
 bool independent_no_violation_possible(int d){
   uint64_t S=0; for(int i=0;i<d;i++) if(spin[i]>0) S|=1ULL<<i;
   for(size_t v=0;v<vertex.size();v++){
     uint64_t m=vertex[v]; if((m>>d)!=0 && d<64) return false;      // some island unassigned
     uint64_t same=(~(S^plusin[v]))&m; if(__builtin_popcountll(same)!=2) return false;
   }
   return true;
 }
 Q energy_q(uint64_t bits){ Q e=0; for(int i=0;i<n;i++)for(int j=i+1;j<n;j++){int si=((bits>>i)&1)?1:-1, sj=((bits>>j)&1)?1:-1; e+=kq[i][j]*(si*sj);} return e;}
 Q bound_q(int d, Q accq){
   Q l=accq;
   for(int j=d;j<n;j++){ Q f=0; for(int i=0;i<d;i++) f+=kq[i][j]*spin[i]; l-=fabsq(f);} 
   l-=TT[d]; return l; }
 void dfs(int d,double acc,uint64_t bits,Q accq){
   if((++nodes&4095ULL)==0 && chrono::steady_clock::now()>=deadline){timed=true;return;}
   double bd=bound(d,acc);
   if(bd>=best){
     ++prune_bound;
     Q Bq=bound_q(d,accq);
     Q slack=Bq-bestq;
     if(slack<0) ++bound_violations;
     min_slack_over_S=min(min_slack_over_S,qd(slack/Sq));
     max_dbl_bound_err_over_S=max(max_dbl_bound_err_over_S,qd(fabsq((Q)(bd+1e-11*max(1.0,scale))-Bq)/Sq));
     return;
   }
   if(!possible_violation(d)){
     ++prune_viol; if(!independent_no_violation_possible(d)) ++viol_prune_mismatch; return; }
   if(d==n){
     if((!want_violation||violates())&&acc<best){best=acc;bestid=bits;bestq=energy_q(bits);++leaf_updates;
        max_leaf_err_over_S=max(max_leaf_err_over_S,qd(fabsq((Q)acc-bestq)/Sq));}
     return;}
   double field=0;for(int i=0;i<d;i++)field+=k[i][d]*spin[i];
   Q fieldq=0; for(int i=0;i<d;i++) fieldq+=kq[i][d]*spin[i];
   int first=field>=0 ? -1:1;
   for(int t=0;t<2;t++){
     int s=t==0?first:-first;spin[d]=s;
     dfs(d+1,acc+s*field,bits|(s>0?(1ULL<<d):0),accq+fieldq*s);
     if(timed)return;
   }
 }
 void run(bool viol,int seconds){
  want_violation=viol;best=numeric_limits<double>::infinity();bestq=0;nodes=0;timed=false;
  prune_bound=prune_viol=viol_prune_mismatch=bound_violations=leaf_updates=0; min_slack_over_S=1e300; max_dbl_bound_err_over_S=0; max_leaf_err_over_S=0;
  root_lower=bound(0,0);deadline=chrono::steady_clock::now()+chrono::seconds(seconds);
  dfs(0,0,0,(Q)0);
  cout<<setprecision(17)<<"{\"objective\":\""<<(viol?"non_grammar":"ground")<<"\",\"n\":"<<n
      <<",\"completed\":"<<(timed?"false":"true")<<",\"nodes\":"<<nodes<<",\"witness_id\":"<<bestid<<",\"upper\":"<<best
      <<",\"shadow\":{\"scale_S\":"<<scale<<",\"guard_abs\":"<<1e-11*max(1.0,scale)<<",\"prune_bound_events\":"<<prune_bound
      <<",\"bound_prunes_unsafe_in_binary128\":"<<bound_violations<<",\"min_slack_over_S\":"<<min_slack_over_S
      <<",\"max_double_bound_error_over_S\":"<<max_dbl_bound_err_over_S<<",\"max_incumbent_error_over_S\":"<<max_leaf_err_over_S
      <<",\"violation_filter_prunes\":"<<prune_viol<<",\"violation_filter_prune_mismatch_vs_independent\":"<<viol_prune_mismatch
      <<",\"incumbent_updates\":"<<leaf_updates<<"}}\n";
 }
};
int main(int argc,char**argv){
 if(argc!=3){cerr<<"usage\n";return 2;}
 Solver s;int seconds=stoi(argv[2]);
 ifstream f(argv[1]);if(!f){cerr<<"cannot read instance\n";return 2;}
 f>>s.n>>s.nv; s.k.assign(s.n,vector<double>(s.n,0));s.spin.assign(s.n,-1);
 for(int i=0;i<s.n;i++)for(int j=i+1;j<s.n;j++){double v; f>>v; s.k[i][j]=s.k[j][i]=v; s.scale+=fabs(v);}
 for(int v=0;v<s.nv;v++){uint64_t m,p;f>>m>>p;s.vertex.push_back(m);s.plusin.push_back(p);}
 s.kq.assign(s.n,vector<Q>(s.n,0)); for(int i=0;i<s.n;i++)for(int j=0;j<s.n;j++)s.kq[i][j]=(Q)s.k[i][j];
 s.Sq=0; for(int i=0;i<s.n;i++)for(int j=i+1;j<s.n;j++)s.Sq+=fabsq(s.kq[i][j]);
 // TT[d] = sum_{j>=d} sum_{h>j} |K_jh|
 s.TT.assign(s.n+1,0); for(int d=s.n-1;d>=0;d--){Q t=0; for(int h=d+1;h<s.n;h++)t+=fabsq(s.kq[d][h]); s.TT[d]=s.TT[d+1]+t;}
 string o=argv[0]; if(argc>=3 && string(argv[2])=="0"){return 2;}
 // objective selection via env
 const char* ob=getenv("SHADOW_OBJ");
 if(!ob||string(ob)=="ground") s.run(false,seconds); else s.run(true,seconds);
 return 0;
}
