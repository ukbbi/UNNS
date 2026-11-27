/* Exact A_k(X) = number of words of length k with least endpoint E <= X, k = 2,3,4.
   Usage: depth_count k X   */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
typedef uint64_t u64;
static u64 X; static int *spf;
typedef struct { int n; u64 p[24]; int e[24]; } F;
static u64 gcd(u64 a,u64 b){while(b){u64 t=a%b;a=b;b=t;}return a;}
static u64 isq(u64 v){u64 r=(u64)sqrtl((long double)v);while(r*r>v)r--;while((r+1)*(r+1)<=v)r++;return r;}
static void mul(F*f,u64 m,int sign){ /* multiply (sign>0) or divide exponents by those of m */
  while(m>1){u64 p=spf[m];int c=0;while(m%p==0){m/=p;c++;}
    int i;for(i=0;i<f->n;i++)if(f->p[i]==p)break;
    if(i==f->n){f->p[i]=p;f->e[i]=0;f->n++;}
    f->e[i]+=sign*c;}
}
/* last letter: sum over g | E and squarefree e | E/g of mu(e) floor(B(g)/(g e)) */
static u64 last(u64 E,const F*f){
  long long total=0;
  u64 g[8192];int ng=1;g[0]=1;
  for(int i=0;i<f->n;i++){int m=ng;u64 q=1;for(int j=1;j<=f->e[i];j++){q*=f->p[i];for(int t=0;t<m;t++)g[ng++]=g[t]*q;}}
  for(int t=0;t<ng;t++){
    u64 d=g[t]; u64 B=isq((u64)(((unsigned __int128)X*d)/E)); if(B<d+1)continue; B-=1;
    u64 M=E/d; u64 es[4096];int sg[4096];int ne=1;es[0]=d;sg[0]=1;
    for(int i=0;i<f->n;i++)if(M%f->p[i]==0){int m=ne;for(int u=0;u<m;u++){u64 v=es[u]*f->p[i];if(v<=B){es[ne]=v;sg[ne]=-sg[u];ne++;}}}
    for(int u=0;u<ne;u++)total+=sg[u]*(long long)(B/es[u]);
  }
  return (u64)total;
}
static u64 rec(u64 E,const F*f,int left){
  if(left==1)return last(E,f);
  u64 Y=X; for(int i=1;i<left;i++)Y/=4;
  u64 total=0;
  u64 g[8192];int ng=1;g[0]=1;
  for(int i=0;i<f->n;i++){int m=ng;u64 q=1;for(int j=1;j<=f->e[i];j++){q*=f->p[i];for(int t=0;t<m;t++)g[ng++]=g[t]*q;}}
  for(int t=0;t<ng;t++){
    u64 d=g[t]; u64 B=isq((u64)(((unsigned __int128)Y*d)/E)); if(B<d+1)continue; B-=1;
    for(u64 N=d;N<=B;N+=d){
      if(gcd(E,N)!=d)continue;
      u64 E2=(E/d)*(N+1)*(N+1);
      F h=*f; mul(&h,N+1,1); mul(&h,N+1,1); mul(&h,d,-1);
      total+=rec(E2,&h,left-1);
    }
  }
  return total;
}
int main(int argc,char**argv){
  int k=atoi(argv[1]); X=strtoull(argv[2],0,10);
  u64 S=isq(X)+3; spf=calloc(S+1,sizeof(int));
  for(u64 i=2;i<=S;i++)if(!spf[i])for(u64 j=i;j<=S;j+=i)if(!spf[j])spf[j]=i;
  F f; f.n=0; printf("%llu\n",(unsigned long long)rec(1,&f,k)); return 0;
}
