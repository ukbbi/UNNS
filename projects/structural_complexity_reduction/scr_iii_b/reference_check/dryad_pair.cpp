// Independent deterministic harness transcribing SPMMC-SSI-Unix-v1.00.cpp
// compute_charge_pair_normalized_displacement_ratio and
// compute_dipole_pair_normalized_coupling_factor (original lines ~1599-1624).
// No GSL/Monte Carlo needed; uses original geometry orientations and nm units.
#include <cmath>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <vector>
#include <array>
using E=std::array<double,4>;
double dot(double x,double y,double X,double Y){return x*X+y*Y;}
double charge(int a,int b,const E&i,const E&j,double len,double distance,double rx,double ry){
 const double l=len, m=len;
 double c=1.+(l/(3*distance))*(l/(3*distance))+(m/(3*distance))*(m/(3*distance))
 +(2./3)*b*m*dot(rx,ry,j[2],j[3])/(distance*distance)
 -(2./3)*a*l*dot(rx,ry,i[2],i[3])/(distance*distance)
 -(2./9)*a*b*l*m*dot(j[2],j[3],i[2],i[3])/(distance*distance);
 return sqrt(c);
}
double K(const E&i,const E&j,double len=160.,double wid=60.,double ht=16.){
 const double rx=j[0]-i[0],ry=j[1]-i[1],r=hypot(rx,ry);
 return (3./16)*wid*ht/(len*r)*(1/charge(1,1,i,j,len,r,rx,ry)+1/charge(-1,-1,i,j,len,r,rx,ry)-1/charge(1,-1,i,j,len,r,rx,ry)-1/charge(-1,1,i,j,len,r,rx,ry));
}
std::vector<E> geometry(int L,double a){
 std::vector<E> e;
 // matches Dryad initializer: each vertex (x+.5,-y) horizontal then (x,-y-.5) vertical, then boundary links
 for(int y=0;y<L;y++) for(int x=0;x<L;x++){
   e.push_back({(x+.5)*a,-y*a,1.,0.});
   e.push_back({x*a,-(y+.5)*a,0.,-1.});
 }
 for(int y=0;y<L;y++) e.push_back({-.5*a,-y*a,1.,0.});
 for(int x=0;x<L;x++) e.push_back({x*a,.5*a,0.,-1.});
 return e;
}
int main(int argc,char**argv){
 int L= argc>1?atoi(argv[1]):2;
 auto e=geometry(L,260.);std::cout<<std::setprecision(17);
 std::cout<<"N "<<e.size()<<"\n";
 for(size_t i=0;i<e.size();i++){
  std::cout<<"E "<<i;
  for(double v:e[i])std::cout<<" "<<v;
  std::cout<<"\n";
 }
 for(size_t i=0;i<e.size();i++)for(size_t j=i+1;j<e.size();j++)std::cout<<"K "<<i<<" "<<j<<" "<<K(e[i],e[j])<<"\n";
}
