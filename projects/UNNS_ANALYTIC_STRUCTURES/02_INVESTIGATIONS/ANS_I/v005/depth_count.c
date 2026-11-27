/* Exact count A_k(X) = #{words of length k of the nesting grammar with E(w) <= X}.
   Usage: depth_count k X   (2<=k<=6, X<=1e13). Integer arithmetic only. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
typedef uint64_t u64;
static u64 X; static int K;
static u64 gcd(u64 a,u64 b){while(b){u64 t=a%b;a=b;b=t;}return a;}
static u64 isq(u64 n){u64 r=(u64)sqrtl((long double)n);while(r*r>n)r--;while((r+1)*(r+1)<=n)r++;return r;}
/* last letter: sum over g = gcd(E,N), Moebius over squarefree h | E/g */
static u64 last(u64 E){
  u64 pr[64];int ex[64],n=0;u64 m=E;
  for(u64 p=2;p*p<=m;p+=(p==2?1:2)) if(m%p==0){pr[n]=p;ex[n]=0;while(m%p==0){m/=p;ex[n]++;}n++;}
  if(m>1){pr[n]=m;ex[n]=1;n++;}
  int a[64]={0};u64 total=0;
  for(;;){
    u64 g=1;for(int i=0;i<n;i++)for(int j=0;j<a[i];j++)g*=pr[i];
    unsigned __int128 t=(unsigned __int128)X*g/E;
    u64 r=isq((u64)t);               /* N+1 <= r */
    if(r>=2 && (r-1)>=g){
      u64 M=(r-1)/g;                 /* N=g*m, m<=M, gcd(m,E/g)=1 */
      u64 h[1<<12];int s[1<<12],c=1;h[0]=1;s[0]=1;
      for(int i=0;i<n;i++) if(a[i]<ex[i]){int c0=c;for(int j=0;j<c0;j++){if(h[j]<=M/pr[i]){h[c]=h[j]*pr[i];s[c]=-s[j];c++;}}}
      int64_t v=0;for(int j=0;j<c;j++)v+=s[j]*(int64_t)(M/h[j]);
      total+=(u64)v;
    }
    int i=0;while(i<n&&a[i]==ex[i]){a[i]=0;i++;}
    if(i==n)break;a[i]++;
  }
  return total;
}
static u64 rec(u64 E,int depth){
  if(depth==K-1) return last(E);
  u64 total=0,R=isq(X);               /* g | E gives E' >= (N+1)^2 */
  u64 B=X/E; if(B>R)B=R;              /* g | N gives E' > E*N */
  for(u64 N=1;N<=B;N++){
    unsigned __int128 E2=(unsigned __int128)(N+1)*(N+1)*(E/gcd(E,N));
    if(E2<=X) total+=rec((u64)E2,depth+1);
  }
  return total;
}
int main(int c,char**v){K=atoi(v[1]);X=strtoull(v[2],0,10);printf("%llu\n",(unsigned long long)rec(1,0));return 0;}
