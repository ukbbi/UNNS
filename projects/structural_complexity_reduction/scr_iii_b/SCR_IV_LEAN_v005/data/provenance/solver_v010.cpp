// SCR-III 4x4 additive solver v010. Double-precision bounds expanded outward.
// Usage: solver_v010 instance.txt seconds
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
using namespace std;
struct Solver {
 int n=0, nv=0; vector<vector<double>> k; vector<uint64_t> vertex, plusin;
 vector<int> spin; uint64_t bestid=0; double best= numeric_limits<double>::infinity();
 uint64_t nodes=0; bool timed=false; bool want_violation=false; double root_lower=0, scale=0;
 chrono::steady_clock::time_point deadline;
 double bound(int d, double acc){
   double l=acc;
   for(int j=d;j<n;j++){
     double field=0;
     for(int i=0;i<d;i++)field+=k[i][j]*spin[i];
     l-=fabs(field);
     for(int h=j+1;h<n;h++)l-=fabs(k[j][h]);
   }
   // outward guard: pessimistic accumulated round-off (never claim exact real arithmetic)
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
 void dfs(int d,double acc,uint64_t bits){
   if((++nodes&4095ULL)==0 && chrono::steady_clock::now()>=deadline){timed=true;return;}
   if(bound(d,acc)>=best) return;
   if(!possible_violation(d))return;
   if(d==n){if((!want_violation||violates())&&acc<best){best=acc;bestid=bits;}return;}
   double field=0;for(int i=0;i<d;i++)field+=k[i][d]*spin[i];
   int first=field>=0 ? -1:1;
   for(int t=0;t<2;t++){
     int s=t==0?first:-first;spin[d]=s;
     dfs(d+1,acc+s*field,bits|(s>0?(1ULL<<d):0));
     if(timed)return;
   }
 }
 void run(bool viol,int seconds){
  want_violation=viol;best=numeric_limits<double>::infinity();nodes=0;timed=false;
  root_lower=bound(0,0);deadline=chrono::steady_clock::now()+chrono::seconds(seconds);
  dfs(0,0,0);
  cout<<"{\"objective\":\""<<(viol?"non_grammar":"ground")<<"\",\"n\":"<<n
      <<",\"completed\":"<<(timed?"false":"true")<<",\"nodes\":"<<nodes
      <<",\"witness_id\":"<<bestid<<",\"upper\":";
  if(isfinite(best))cout<<setprecision(17)<<best;else cout<<"null";
  cout<<",\"lower\":"<<(timed?root_lower:best)<<"}\n";
 }
};
int main(int argc,char**argv){
 if(argc!=3){cerr<<"usage: solver_v010 INSTANCE seconds\n";return 2;}
 Solver s;int seconds=stoi(argv[2]); if(seconds<1||seconds>1800){cerr<<"time must be 1..1800 seconds\n";return 2;}
 ifstream f(argv[1]);if(!f){cerr<<"cannot read instance\n";return 2;}
 f>>s.n>>s.nv; if(s.n<1||s.n>63||s.nv<0||s.nv>100){cerr<<"unsafe instance sizes\n";return 2;}
 s.k.assign(s.n,vector<double>(s.n,0));s.spin.assign(s.n,-1);
 for(int i=0;i<s.n;i++)for(int j=i+1;j<s.n;j++){
  double v; if(!(f>>v)||!isfinite(v)){cerr<<"invalid K\n";return 2;}
  s.k[i][j]=s.k[j][i]=v; s.scale+=fabs(v);
 }
 for(int v=0;v<s.nv;v++){
  uint64_t m,p;if(!(f>>m>>p)|| (m>>s.n)!=0 || (p & ~m)!=0 || __builtin_popcountll(m)!=4){cerr<<"invalid vertex mask\n";return 2;}s.vertex.push_back(m);s.plusin.push_back(p);
 }
 string extra;if(f>>extra){cerr<<"trailing instance data\n";return 2;}
 s.run(false,seconds);s.run(true,seconds);return 0;
}
