/* GEO-I v009: Burnside count of GL(k,2)-orbits on subsets of F_2^k \ {0}  (all sizes incl. empty).  independent check of theory/binary5.py orbit enumeration.
   usage: burnside5 k */
#include <stdio.h>
#include <stdlib.h>
typedef unsigned long long u64;
int k, N;
int main(int argc, char** argv){
  k = atoi(argv[1]); N = (1<<k) - 1;
  int img[8]; u64 group = 0; unsigned __int128 sum = 0;
  int span[256];
  /* recursive enumeration of ordered bases */
  int idx[8]; int depth = 0;
  /* iterative DFS */
  int cand[8]; for (int i=0;i<k;i++) cand[i]=0;
  int sp[8][256]; int spn[8];
  spn[0]=1; sp[0][0]=0;
  depth=0; cand[0]=0;
  while (depth>=0){
    cand[depth]++;
    if (cand[depth] > N){ depth--; continue; }
    int v = cand[depth]; int in=0;
    for (int j=0;j<spn[depth];j++) if (sp[depth][j]==v){in=1;break;}
    if (in) continue;
    img[depth]=v;
    if (depth==k-1){
      /* full basis: build permutation */
      int perm[256]; 
      for (int x=1;x<=N;x++){ int y=0; for (int b=0;b<k;b++) if ((x>>b)&1) y^=img[b]; perm[x]=y; }
      int seen[256]={0}; int cyc=0;
      for (int x=1;x<=N;x++) if(!seen[x]){ cyc++; int y=x; while(!seen[y]){seen[y]=1;y=perm[y];} }
      sum += ((unsigned __int128)1)<<cyc; group++;
    } else {
      int n=spn[depth]; for (int j=0;j<n;j++){ sp[depth+1][j]=sp[depth][j]; sp[depth+1][j+n]=sp[depth][j]^v; }
      spn[depth+1]=2*n; depth++; cand[depth]=0;
    }
  }
  printf("k=%d |GL|=%llu orbits_on_subsets_incl_empty=%llu remainder=%llu\n", k, group, (u64)(sum/group), (u64)(sum%group));
  return 0;
}
