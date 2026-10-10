#include <cmath>
#include <vector>
#include <iostream>
#include <iomanip>
using namespace std;
double compute_scalar_product(vector<double>& vector1, vector<double>& vector2)
{//---------------------------------------------------------------------------------------------------------------------------------------------------

    double scalar_product = 0.0;

    for (unsigned int index = 0; index < vector1.size(); index++)
        scalar_product += vector1[index] * vector2[index];

    return scalar_product;

}

double compute_charge_pair_normalized_displacement_ratio(int reference_dipole_sign, int neighbor_dipole_sign, double reference_dipole_island_length, double neighbor_dipole_island_length, vector<double>& reference_dipole_unit_vector, vector<double>& neighbor_dipole_unit_vector, double dipole_pair_relative_displacement, vector<double>& dipole_pair_relative_position )
{//---------------------------------------------------------------------------------------------------------------------------------------------------    

    double charge_pair_normalized_displacement_ratio = 1.0 + (reference_dipole_island_length / (3.0 * dipole_pair_relative_displacement)) * (reference_dipole_island_length / (3.0 * dipole_pair_relative_displacement)) + (neighbor_dipole_island_length / (3.0 * dipole_pair_relative_displacement)) * (neighbor_dipole_island_length / (3.0 * dipole_pair_relative_displacement)) + (2.0) / (3.0) * neighbor_dipole_sign * neighbor_dipole_island_length * compute_scalar_product(dipole_pair_relative_position, neighbor_dipole_unit_vector) / (dipole_pair_relative_displacement * dipole_pair_relative_displacement) - (2.0) / (3.0) * reference_dipole_sign * reference_dipole_island_length * compute_scalar_product(dipole_pair_relative_position, reference_dipole_unit_vector) / (dipole_pair_relative_displacement * dipole_pair_relative_displacement) - (2.0) / (9.0) * reference_dipole_sign * neighbor_dipole_sign * reference_dipole_island_length * neighbor_dipole_island_length * compute_scalar_product(neighbor_dipole_unit_vector, reference_dipole_unit_vector) / (dipole_pair_relative_displacement * dipole_pair_relative_displacement);

    return sqrt(charge_pair_normalized_displacement_ratio);

}

double compute_dipole_pair_normalized_coupling_factor(double reference_dipole_island_length, double neighbor_dipole_island_length, double neighbor_dipole_island_width, double neighbor_dipole_island_height, vector<double>& reference_dipole_unit_vector, vector<double>& neighbor_dipole_unit_vector, double dipole_pair_relative_displacement, vector<double>& dipole_pair_relative_position )
{//---------------------------------------------------------------------------------------------------------------------------------------------------

    double charge_pair_normalized_displacement_ratio_plus_plus = compute_charge_pair_normalized_displacement_ratio(+1, +1, reference_dipole_island_length, neighbor_dipole_island_length, reference_dipole_unit_vector, neighbor_dipole_unit_vector, dipole_pair_relative_displacement, dipole_pair_relative_position);
    double charge_pair_normalized_displacement_ratio_plus_minus = compute_charge_pair_normalized_displacement_ratio(+1, -1, reference_dipole_island_length, neighbor_dipole_island_length, reference_dipole_unit_vector, neighbor_dipole_unit_vector, dipole_pair_relative_displacement, dipole_pair_relative_position);
    double charge_pair_normalized_displacement_ratio_minus_plus = compute_charge_pair_normalized_displacement_ratio(-1, +1, reference_dipole_island_length, neighbor_dipole_island_length, reference_dipole_unit_vector, neighbor_dipole_unit_vector, dipole_pair_relative_displacement, dipole_pair_relative_position);
    double charge_pair_normalized_displacement_ratio_minus_minus = compute_charge_pair_normalized_displacement_ratio(-1, -1, reference_dipole_island_length, neighbor_dipole_island_length, reference_dipole_unit_vector, neighbor_dipole_unit_vector, dipole_pair_relative_displacement, dipole_pair_relative_position);

    double charge_pair_normalized_displacement_inverse_ratio = ((1.0 / charge_pair_normalized_displacement_ratio_plus_plus) + (1.0 / charge_pair_normalized_displacement_ratio_minus_minus) - (1.0 / charge_pair_normalized_displacement_ratio_plus_minus) - (1.0 / charge_pair_normalized_displacement_ratio_minus_plus));   

    double dipole_pair_normalized_coupling_factor = (3.0 / 16.0) * (neighbor_dipole_island_width * neighbor_dipole_island_height) / (reference_dipole_island_length * dipole_pair_relative_displacement) * charge_pair_normalized_displacement_inverse_ratio;

    return dipole_pair_normalized_coupling_factor;

}
int main(int argc,char**argv){
 int L=argc>1?atoi(argv[1]):2; double a=260.;
 vector<vector<double>> e,u;
 for(int y=0;y<L;y++) for(int x=0;x<L;x++){
 e.push_back({(x+.5)*a,-y*a});u.push_back({1.,0.});
 e.push_back({x*a,-(y+.5)*a});u.push_back({0.,-1.});
 }
 for(int y=0;y<L;y++){e.push_back({-.5*a,-y*a});u.push_back({1.,0.});}
 for(int x=0;x<L;x++){e.push_back({x*a,.5*a});u.push_back({0.,-1.});}
 cout<<setprecision(17);
 for(size_t i=0;i<e.size();i++)for(size_t j=i+1;j<e.size();j++){
  vector<double> r={e[j][0]-e[i][0],e[j][1]-e[i][1]};double d=hypot(r[0],r[1]);
  double k=compute_dipole_pair_normalized_coupling_factor(160.,160.,60.,16.,u[i],u[j],d,r);
  cout<<i<<" "<<j<<" "<<k<<"\n";
 }
}
