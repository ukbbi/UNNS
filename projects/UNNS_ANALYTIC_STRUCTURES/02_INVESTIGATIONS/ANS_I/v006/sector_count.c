/* Words of the nesting grammar with E(w) <= X, split by the class phi(Q(w)) in Z/7,
   phi(2)=2, phi(3)=1, phi(p)=2 phi(p+1). Usage: sector_count X   (X <= 1e12). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef uint64_t u64;
static u64 X,cnt[7],R; static int *letter;
static u64 gcd(u64 a,u64 b){while(b){u64 t=a%b;a=b;b=t;}return a;}
static void rec(u64 E,int h){
  cnt[h]++;
  u64 B=X/E; if(B>R)B=R;
  for(u64 N=1;N<=B;N++){
    u64 E2=(N+1)*(N+1)*(E/gcd(E,N));
    if(E2<=X) rec(E2,(h+letter[N])%7);
  }
}
int main(int c,char**v){
  X=strtoull(v[1],0,10); R=1; while((R+1)*(R+1)<=X)R++;
  u64 n=R+2; int *phi=calloc(n+1,sizeof(int)),*spf=calloc(n+1,sizeof(int));
  for(u64 i=2;i<=n;i++) if(!spf[i]) for(u64 j=i;j<=n;j+=i) if(!spf[j]) spf[j]=i;
  phi[1]=0;
  /* primes need the next integer, whose prime factors are smaller */
  for(u64 m=2;m<=n;m++){
    if(spf[m]!=(int)m){phi[m]=(phi[spf[m]]+phi[m/spf[m]])%7;continue;}
    if(m==2){phi[m]=2;continue;}
    if(m==3){phi[m]=1;continue;}
    u64 k=m+1; int s=0; while(k>1){int p=spf[k]?spf[k]:(int)k; s=(s+phi[p])%7; k/=p;}
    phi[m]=2*s%7;
  }
  letter=calloc(R+1,sizeof(int));
  for(u64 N=1;N<=R;N++) letter[N]=((2*phi[N+1]-phi[N])%7+7)%7;
  rec(1,0);
  for(int h=0;h<7;h++)printf("%llu ",(unsigned long long)cnt[h]); printf("\n");return 0;
}
