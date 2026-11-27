/* Exact census of words of the nesting grammar with E(w) <= 2*10^8, reported at thresholds
   T = 10^3..10^8 and 2T. Integer arithmetic except for the sum of log Q. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
typedef uint64_t u64;
#define NT 12
static u64 th[NT],TOP,R; static int *cls; static double *lr;
static u64 A[NT],A1[NT],C[NT],sec[NT][7],depth[NT],ones[NT],letters[NT];
static double lq[NT],le[NT];
static u64 gcd(u64 a,u64 b){while(b){u64 t=a%b;a=b;b=t;}return a;}
static void rec(u64 E,u64 K,int h,int k,int n1,double logQ){
  double logE=log((double)E);
  for(int i=NT-1;i>=0;i--){
    if(E>th[i])break;              /* thresholds are increasing */
    A[i]++; sec[i][h]++; if(K==1)A1[i]++; C[i]+=th[i]/E;
    depth[i]+=k; ones[i]+=n1; lq[i]+=logQ; le[i]+=logE;
  }
  u64 B=TOP/E; if(B>R)B=R;
  for(u64 N=1;N<=B;N++){
    u64 g=gcd(E,N),E2=(N+1)*(N+1)*(E/g);
    if(E2<=TOP) rec(E2,N*(K)/g,(h+cls[N])%7,k+1,n1+(N==1),logQ+lr[N]);
  }
}
int main(int argc,char**argv){
  int m=0; for(u64 T=1000;T<=100000000ULL;T*=10){th[m++]=T;th[m++]=2*T;}
  TOP=th[NT-1]; R=1; while((R+1)*(R+1)<=TOP)R++;
  u64 n=R+2; int *phi=calloc(n+1,sizeof(int)),*spf=calloc(n+1,sizeof(int));
  for(u64 i=2;i<=n;i++) if(!spf[i]) for(u64 j=i;j<=n;j+=i) if(!spf[j]) spf[j]=i;
  for(u64 q=2;q<=n;q++){
    if(spf[q]!=(int)q){phi[q]=(phi[spf[q]]+phi[q/spf[q]])%7;continue;}
    if(q==2){phi[q]=2;continue;} if(q==3){phi[q]=1;continue;}
    u64 k=q+1;int s=0;while(k>1){int p=spf[k];s=(s+phi[p])%7;k/=p;} phi[q]=2*s%7;
  }
  cls=calloc(R+1,sizeof(int)); lr=calloc(R+1,sizeof(double));
  for(u64 N=1;N<=R;N++){cls[N]=((2*phi[N+1]-phi[N])%7+7)%7; lr[N]=2*log((double)N+1)-log((double)N);}
  rec(1,1,0,0,0,0.0);
  printf("[\n");
  for(int i=0;i<NT;i++){
    printf("{\"X\":%llu,\"A\":%llu,\"N1\":%llu,\"C\":%llu,\"sectors\":[",(unsigned long long)th[i],(unsigned long long)A[i],(unsigned long long)A1[i],(unsigned long long)C[i]);
    for(int h=0;h<7;h++)printf("%llu%s",(unsigned long long)sec[i][h],h<6?",":"");
    printf("],\"mean_depth\":%.10f,\"letter1_share\":%.10f,\"mean_logQ\":%.10f,\"mean_logE\":%.10f}%s\n",
      (double)depth[i]/A[i],(double)ones[i]/depth[i],lq[i]/A[i],le[i]/A[i],i<NT-1?",":"");
  }
  printf("]\n");return 0;
}
