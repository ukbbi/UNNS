/* GEO-I v010: Burnside count of AGL(m,2) orbits on subsets of F_2^m (all sizes incl. empty). usage: burnside_affine m */
#include <stdio.h>
#include <stdlib.h>
typedef unsigned long long u64;
int main(int argc,char**argv){
  int m=atoi(argv[1]); int N=1<<m; int img[8]; int cand[8]; int sp[8][256]; int spn[8];
  u64 grp=0; unsigned __int128 sum=0; spn[0]=1; sp[0][0]=0; int depth=0; cand[0]=0;
  while(depth>=0){
    cand[depth]++; if(cand[depth]>=N){depth--;continue;}
    int v=cand[depth],in=0; for(int j=0;j<spn[depth];j++) if(sp[depth][j]==v){in=1;break;} if(in)continue;
    img[depth]=v;
    if(depth==m-1){
      for(int t=0;t<N;t++){ int perm[256]; for(int x=0;x<N;x++){int y=t; for(int b=0;b<m;b++) if((x>>b)&1) y^=img[b]; perm[x]=y;}
        int seen[256]={0},cyc=0; for(int x=0;x<N;x++) if(!seen[x]){cyc++;int y=x;while(!seen[y]){seen[y]=1;y=perm[y];}}
        sum+=((unsigned __int128)1)<<cyc; grp++; }
    } else { int n=spn[depth]; for(int j=0;j<n;j++){sp[depth+1][j]=sp[depth][j];sp[depth+1][j+n]=sp[depth][j]^v;} spn[depth+1]=2*n; depth++; cand[depth]=0; }
  }
  printf("m=%d |AGL|=%llu orbits_incl_empty=%llu rem=%llu\n",m,grp,(u64)(sum/grp),(u64)(sum%grp)); return 0; }
