// source_probe_v005.cpp  --  SCR-III-B PREFLIGHT_v005 physical-reference probe
// Evidence level: VERBATIM original-source functions (Dryad SPMMC-SSI-Unix-v1.00.cpp) driven by
// NEW non-verbatim driver code. This is NOT the unmodified simulator.
// Original archive : SPMMC_Code.zip  sha256 77c82d83ea20eff5abcab8323b061edf759809cdd4366e86042147f6ea60a5dd
// Original C++     : SPMMC Code/SPMMC-SSI-Unix-v1.00.cpp  sha256 f7ffe5ff3bdff923e1281c3ed7431dfece5ce0c596ffe3f60a5b037908ab750a
// Every block between "BEGIN VERBATIM" / "END VERBATIM" markers is a byte-exact copy of the original line range
// (sha256 of the block text recorded in the marker). validate_v005.py re-checks every block against the original.
// NON-verbatim parts (explicitly): the #include list (GSL headers omitted), update_simulation_log_file() stub,
// generate_random_gaussian_distribution() stand-in (original uses GSL; with stdev=0 it returns the mean),
// constant Delta-N stand-in (original uses GSL elliptic integrals; Delta-N cancels in flip differences),
// and main().
#include <cstdlib>
#include <cstdio>
#include <iostream>
#include <vector>
#include <cmath>
#include <climits>
#include <cfloat>
#include <string>
#include <sstream>
#include <iomanip>
using namespace std;

// BEGIN VERBATIM declaration double pi original_lines=45-45 sha256=7f7f8fefef9f5207d0c097247f8e169adfbe9439b1be3adcc2a447f9ddb84b3e
double pi = 3.1415926535897932384626433832795028841971693993751; // pi
// END VERBATIM double pi
// BEGIN VERBATIM declaration double error original_lines=46-46 sha256=042c8d27407ba2d5b7f1b7bfced1665039d89a11073886dc4469f1ab66a3e829
double error = pow(10.0, -12.0); // machine error, typically used for comparison of double variables
// END VERBATIM double error
// BEGIN VERBATIM declaration unsigned int lattice_linear_size original_lines=55-55 sha256=27295b177a0ed3b8f514b5b3afba9c70d703c173268c59b92803d82df4992269
unsigned int lattice_linear_size = 24; // number of repeats per dimensions
// END VERBATIM unsigned int lattice_linear_size
// BEGIN VERBATIM declaration double lattice_parameter original_lines=56-56 sha256=b41068d35114ca6623f08146ededf9ea019dfb2883938b2da8e3a532255fb916
double lattice_parameter = 260.0; // lattice parameter [nm]
// END VERBATIM double lattice_parameter
// BEGIN VERBATIM declaration double island_length_mean original_lines=58-58 sha256=4f8c537d5bf157c8a29e1a8087fd0be8aec960ac30e35f0a07b0facfe1a0df09
double island_length_mean = 160.0; // mean island length [nm]
// END VERBATIM double island_length_mean
// BEGIN VERBATIM declaration double island_length_stdev original_lines=59-59 sha256=d1d9e379ccd1f2be4b29eca587bbf8224f366067b4261db2c85564d172eb3992
double island_length_stdev = 0.0; // standard deviation of the island length distribution [nm]
// END VERBATIM double island_length_stdev
// BEGIN VERBATIM declaration double island_width_mean original_lines=60-60 sha256=a02c54fb4dd1e7d11993223a2617a04781c4c81cfd1ef82d77aefd4d19191459
double island_width_mean = 60.0; // mean island width [nm]
// END VERBATIM double island_width_mean
// BEGIN VERBATIM declaration double island_width_stdev original_lines=61-61 sha256=b7b0baa2eaf80dff0bb815fb6baf8ee65f6fc893dea044c6f5e3f101e2fe764a
double island_width_stdev = 0.0; // standard deviation of the island width distribution [nm]
// END VERBATIM double island_width_stdev
// BEGIN VERBATIM declaration double island_height original_lines=62-62 sha256=a44f0eeca783b180b6a31aa879f993c8fc4358ce81e86175128c577631b9e5cb
double island_height = 15.0; // island height [nm] - assumed to be the same for all islands
// END VERBATIM double island_height
// BEGIN VERBATIM declaration double Curie_temperature = original_lines=70-70 sha256=f9cc9c8cfb80151fb11a5e16e81d2c5230bba0dcfa1a249bdff06ba0d900798b
double Curie_temperature = 820.0; // Curie temperature of the islands [K]
// END VERBATIM double Curie_temperature =
// BEGIN VERBATIM declaration bool enable_Curie_temperature_height_dependence original_lines=72-72 sha256=9c6e01ced4d63260ec0598c027c40a8505cb1a9a06a9e68601ef8595369524b6
bool enable_Curie_temperature_height_dependence = true; // if enabled, the Curie temperature of the system islands is defined according to the empirical expression from Zhang et al. APL Materials (2019)
// END VERBATIM bool enable_Curie_temperature_height_dependence
// BEGIN VERBATIM declaration double Curie_temperature_bulk original_lines=73-73 sha256=d87d07d986fae49968a2065449b14f08ae29064fea43bf418929653c35135e86
double Curie_temperature_bulk = 820.0; // Curie temperature of the bulk magnetic material [K]
// END VERBATIM double Curie_temperature_bulk
// BEGIN VERBATIM declaration double Curie_temperature_characteristic_height original_lines=74-74 sha256=804bce1dce6b6790a6714aae848f18dfcbb92a660c7d4e2340a397278322c3dd
double Curie_temperature_characteristic_height = 0.0; // specific height used for computing the Curie temperature dependence on the height of the islands [nm]
// END VERBATIM double Curie_temperature_characteristic_height
// BEGIN VERBATIM declaration double Curie_temperature_characteristic_exponent original_lines=75-75 sha256=0642d397ae3070578fac26c3abef5d7f96ee40e22aa6879fbb1ec518b660fed2
double Curie_temperature_characteristic_exponent = 1.2; // exponent of the height ratios for computing the Curie temperature dependence 
// END VERBATIM double Curie_temperature_characteristic_exponent
// BEGIN VERBATIM declaration bool periodic_boundary_conditions_enabled original_lines=83-83 sha256=9d86891cd9009acfa958eb60714ffdb61fe36caf3f493d50a3f7f4c4bd988158
bool periodic_boundary_conditions_enabled = false;
// END VERBATIM bool periodic_boundary_conditions_enabled
// BEGIN VERBATIM declaration bool vertex_interaction_model_enabled original_lines=84-84 sha256=75190582589a2f8b2afc5ab856b04e2283e176ce1de377831374ae42239afdca
bool vertex_interaction_model_enabled = false;
// END VERBATIM bool vertex_interaction_model_enabled
// BEGIN VERBATIM declaration double interaction_range_cutoff_radius original_lines=86-86 sha256=394fcf6b56f441d7e086a894e19092d0c545538257826e17b37d2e0bc5b4a642
double interaction_range_cutoff_radius = 10000000; // the span of the interaction range [nm]
// END VERBATIM double interaction_range_cutoff_radius
// BEGIN VERBATIM declaration double spontaneous_magnetization0 original_lines=87-87 sha256=e6141f60ccb45ca6ee7ceee6f21f3bbe3718d10696381f27dc16a060a66cda7d
double spontaneous_magnetization0 = 7.9; // spontaneous magnetization at 0K [10^5 A/m]
// END VERBATIM double spontaneous_magnetization0
// BEGIN VERBATIM declaration double magnetization_critical_exponent original_lines=88-88 sha256=21bac21f31f7d35f5ec7f40854090c3ef64d079b82e93ea958c5fa96ba119ef6
double magnetization_critical_exponent = 0.5; // thermal dependence magnetization exponent (beta exponent)
// END VERBATIM double magnetization_critical_exponent
// BEGIN VERBATIM declaration double barrier_adjustment_ratio original_lines=89-89 sha256=3db6ffaec5ed50e2af8c1daf83606c20868fb2a32eb67e71d5e8d0055763e8c8
double barrier_adjustment_ratio = 1.0; // a global, athermal ratio that effectively reduces the energy barrier of the dipole islands
// END VERBATIM double barrier_adjustment_ratio
// BEGIN VERBATIM declaration double interaction_adjustment_ratio original_lines=90-90 sha256=017b617b7e30f336a3b8155adb065e3a14ed9a007919b01e5e24d1e6cccc9e64
double interaction_adjustment_ratio = 1.0; // a global, athermal ratio that effectively reduces the interaction energy of the dipole islands
// END VERBATIM double interaction_adjustment_ratio
// BEGIN VERBATIM declaration double tau0 original_lines=98-98 sha256=7d3b9206884d2e7c8865aaca659254dccabb4d7388d4674d2d099019df81c1a3
double tau0 = pow(10.0, -9.0); // inverse basic attempt frequency [s]
// END VERBATIM double tau0
// BEGIN VERBATIM declaration double maximum_allowed_exponent original_lines=106-106 sha256=c98a9bd61fd2f661f554e8f09a29bf85f9b22fa12757edb186c17daf7fe6ddba
double maximum_allowed_exponent = log(DBL_MAX) + log(tau0); // the argument of the exponential defining the maximum allowed reversal time, a precautionary measure for limiting/preventing floating point errors.
// END VERBATIM double maximum_allowed_exponent
// BEGIN VERBATIM declaration string main_folder_path original_lines=137-137 sha256=69ad82fb7c7aac6324a43b79cfa8d5fd4b4bb931d00ae38dcdc728fc50990ef7
string main_folder_path; // the path to the folder containing the code/solution
// END VERBATIM string main_folder_path
// BEGIN VERBATIM declaration unsigned int number_of_dipoles original_lines=139-139 sha256=684ca997946d4ef4f2e1952c1f1ff6e44c0591874ca4b87c799c045e15cc4908
unsigned int number_of_dipoles; // the number of dipoles - updated after the system definition
// END VERBATIM unsigned int number_of_dipoles
// BEGIN VERBATIM declaration unsigned int number_of_vertices original_lines=140-140 sha256=f625412e2afab5924da5cfb7c8d2e43ce58ceccd264e32a23e5afacb5c973f72
unsigned int number_of_vertices; // the number of vertices - updated after the system definition
// END VERBATIM unsigned int number_of_vertices
// BEGIN VERBATIM declaration unsigned int number_of_spin_vertex_neighborhood_configurations original_lines=141-141 sha256=8dabe90ddb48699f4d7f57cb21a30bb825f0e62c4fea209bde9ad54f9bb3c3d0
unsigned int number_of_spin_vertex_neighborhood_configurations; // the number of valid spin vertex neighborhood configurations - updated after the system definition
// END VERBATIM unsigned int number_of_spin_vertex_neighborhood_configurations
// BEGIN VERBATIM declaration unsigned int number_of_temperatures original_lines=142-142 sha256=0bf57262e51ae1c4d18595d43d4de227f228376a43c9ce6a7061fe22e87b126c
unsigned int number_of_temperatures; // the number of temperatures - updated after initializing the temperature vector
// END VERBATIM unsigned int number_of_temperatures

// ---------------- NON-VERBATIM stand-ins (documented) ----------------
static int g_log_counts[4] = {0,0,0,0};
void update_simulation_log_file(int log_code, unsigned int index_temperature, unsigned int index_acquisition, unsigned int index_sweep)
{ (void)index_temperature; (void)index_acquisition; (void)index_sweep; if (log_code>=1 && log_code<=3) g_log_counts[log_code]++; }
void generate_random_gaussian_distribution(double mean_value, double stdev_value, int number_of_elements, vector<double>& value_vector)
{ // STAND-IN: original draws mean + gsl_ran_gaussian(.,stdev). Valid only for stdev == 0 (all SPMMC v1.00 defaults here).
  if (stdev_value != 0.0) { cerr << "stand-in supports stdev==0 only\n"; exit(3); }
  value_vector.assign(number_of_elements, mean_value); }

// BEGIN VERBATIM function compute_scalar_product original_lines=669-679 sha256=4e9dff5bc7bd0936c647a792111a81f852a42c8ffc2e459d12678bbea87b50fa
double compute_scalar_product(vector<double>& vector1, vector<double>& vector2)
{//---------------------------------------------------------------------------------------------------------------------------------------------------

    double scalar_product = 0.0;

    for (unsigned int index = 0; index < vector1.size(); index++)
        scalar_product += vector1[index] * vector2[index];

    return scalar_product;

}//---------------------------------------------------------------------------------------------------------------------------------------------------
// END VERBATIM compute_scalar_product
// BEGIN VERBATIM function initialize_Curie_temperature original_lines=980-986 sha256=3b528199b01e986d1e76e0815b89ddd4bebfea39c12aae1aa6dd18e52e78d87c
void initialize_Curie_temperature()
{//---------------------------------------------------------------------------------------------------------------------------------------------------

    if (enable_Curie_temperature_height_dependence)
        Curie_temperature = Curie_temperature_bulk * (1.0 - pow((Curie_temperature_characteristic_height / island_height), Curie_temperature_characteristic_exponent));
    
}//---------------------------------------------------------------------------------------------------------------------------------------------------
// END VERBATIM initialize_Curie_temperature
// BEGIN VERBATIM function initialize_dipole_system original_lines=992-1126 sha256=9ba29f7fb905b16877d4e3feb9be8e4ffc8762f9742c0d63c4665447d93d446c
void initialize_dipole_system(vector<unsigned int>& dipole_direct_sequence_vector, vector< vector<double> >& dipole_coordinates_vector, vector< vector<double> >& dipole_unit_vectors_vector, vector<double>& dipole_island_lengths_vector, vector<double>& dipole_island_widths_vector)
{//---------------------------------------------------------------------------------------------------------------------------------------------------

    //--------------------------------------------------------------------------------------------------
    //-------------------------------------------------------------------------
    // Square spin ice - Lattice Vectors

    vector<double> square_ice_lattice_vector1;
    vector<double> square_ice_lattice_vector2;

    square_ice_lattice_vector1.clear();
    square_ice_lattice_vector1.push_back(1.0);
    square_ice_lattice_vector1.push_back(0.0);

    square_ice_lattice_vector2.clear();
    square_ice_lattice_vector2.push_back(0.0);
    square_ice_lattice_vector2.push_back(-1.0);

    //-------------------------------------------------------------------------
    // Square spin ice - Dipole Base Positions

    vector<double> square_spin_ice_dipole_base_position;
    vector< vector<double> > square_spin_ice_dipole_base_positions;

    square_spin_ice_dipole_base_position.clear();
    square_spin_ice_dipole_base_position.push_back(0.5);
    square_spin_ice_dipole_base_position.push_back(0.0);
    square_spin_ice_dipole_base_positions.push_back(square_spin_ice_dipole_base_position);

    square_spin_ice_dipole_base_position.clear();
    square_spin_ice_dipole_base_position.push_back(0.0);
    square_spin_ice_dipole_base_position.push_back(-0.5);
    square_spin_ice_dipole_base_positions.push_back(square_spin_ice_dipole_base_position);

    //-------------------------------------------------------------------------
    // Square spin ice - Dipole Unit Vectors

    vector<double> square_spin_ice_dipole_unit_vector;
    vector< vector<double> > square_spin_ice_dipole_unit_vectors;
    
    square_spin_ice_dipole_unit_vector.clear();
    square_spin_ice_dipole_unit_vector.push_back(1.0);
    square_spin_ice_dipole_unit_vector.push_back(0.0);
    square_spin_ice_dipole_unit_vectors.push_back(square_spin_ice_dipole_unit_vector);

    square_spin_ice_dipole_unit_vector.clear();
    square_spin_ice_dipole_unit_vector.push_back(0.0);
    square_spin_ice_dipole_unit_vector.push_back(-1.0);
    square_spin_ice_dipole_unit_vectors.push_back(square_spin_ice_dipole_unit_vector);

    //-------------------------------------------------------------------------
    //--------------------------------------------------------------------------------------------------

    int index_row;
    int index_column;    
    int index_base;
    double coordinate_x;
    double coordinate_y;
    vector<double> dipole_coordinates;
    vector<double> dipole_unit_vector;


    dipole_coordinates_vector.clear();
    dipole_unit_vectors_vector.clear();

    for (unsigned int index_row = 0; index_row < lattice_linear_size; index_row++)
    {
        for (unsigned int index_column = 0; index_column < lattice_linear_size; index_column++)
        {
            for (unsigned int index_base = 0; index_base < square_spin_ice_dipole_base_positions.size(); index_base++)
            {
                coordinate_x = index_row * square_ice_lattice_vector2[0] + index_column * square_ice_lattice_vector1[0] + square_spin_ice_dipole_base_positions[index_base][0];
                coordinate_y = index_row * square_ice_lattice_vector2[1] + index_column * square_ice_lattice_vector1[1] + square_spin_ice_dipole_base_positions[index_base][1];

                dipole_coordinates.clear();
                dipole_coordinates.push_back(lattice_parameter * coordinate_x);
                dipole_coordinates.push_back(lattice_parameter * coordinate_y);
                dipole_coordinates_vector.push_back(dipole_coordinates);

                dipole_unit_vectors_vector.push_back(square_spin_ice_dipole_unit_vectors[index_base]);
            }
        }
    }

    //--------------------------------------------------------------------------------------------------
    // Row of dipoles to ensure the top row of vertices have 4 dipoles

    for (unsigned int index_row = 0; index_row < lattice_linear_size; index_row++)
    {
        index_column = -1;
        index_base = 0;

        coordinate_x = index_row * square_ice_lattice_vector2[0] + index_column * square_ice_lattice_vector1[0] + square_spin_ice_dipole_base_positions[index_base][0];
        coordinate_y = index_row * square_ice_lattice_vector2[1] + index_column * square_ice_lattice_vector1[1] + square_spin_ice_dipole_base_positions[index_base][1];

        dipole_coordinates.clear();
        dipole_coordinates.push_back(lattice_parameter * coordinate_x);
        dipole_coordinates.push_back(lattice_parameter * coordinate_y);
        dipole_coordinates_vector.push_back(dipole_coordinates);

        dipole_unit_vectors_vector.push_back(square_spin_ice_dipole_unit_vectors[index_base]);
    }

    //--------------------------------------------------------------------------------------------------
    // Column of dipoles to ensure the left column of vertices have 4 dipoles

    for (unsigned int index_column = 0; index_column < lattice_linear_size; index_column++)
    {
        index_row = -1;
        index_base = 1;

        coordinate_x = index_row * square_ice_lattice_vector2[0] + index_column * square_ice_lattice_vector1[0] + square_spin_ice_dipole_base_positions[index_base][0];
        coordinate_y = index_row * square_ice_lattice_vector2[1] + index_column * square_ice_lattice_vector1[1] + square_spin_ice_dipole_base_positions[index_base][1];

        dipole_coordinates.clear();
        dipole_coordinates.push_back(lattice_parameter * coordinate_x);
        dipole_coordinates.push_back(lattice_parameter * coordinate_y);
        dipole_coordinates_vector.push_back(dipole_coordinates);

        dipole_unit_vectors_vector.push_back(square_spin_ice_dipole_unit_vectors[index_base]);
    }

    number_of_dipoles = dipole_coordinates_vector.size();


    for (unsigned int index_dipole = 0; index_dipole < number_of_dipoles; index_dipole++)
        dipole_direct_sequence_vector.push_back(index_dipole);

    //--------------------------------------------------------------------------------------------------
    // Generating the distribution of island lengths, widths and heights

    generate_random_gaussian_distribution(island_length_mean, island_length_stdev, number_of_dipoles, dipole_island_lengths_vector);
    generate_random_gaussian_distribution(island_width_mean, island_width_stdev, number_of_dipoles, dipole_island_widths_vector);

}//---------------------------------------------------------------------------------------------------------------------------------------------------
// END VERBATIM initialize_dipole_system
// BEGIN VERBATIM function initialize_vertex_system original_lines=1158-1337 sha256=394b067f891792b7a7c86cce5280aa31533e150c9102214b1d8a5922b00a46fa
void initialize_vertex_system(vector< vector<double> >& dipole_coordinates_vector, vector< vector<double> >& dipole_unit_vectors_vector, vector< vector<double> >& vertex_coordinates_vector, vector< vector<int> >& dipole_to_vertex_array, vector< vector<int> >& vertex_to_dipole_array)
{//---------------------------------------------------------------------------------------------------------------------------------------------------

    //--------------------------------------------------------------------------------------------------
    //-------------------------------------------------------------------------
    // Square spin ice - Lattice Vectors

    vector<double> square_ice_lattice_vector1;
    vector<double> square_ice_lattice_vector2;

    square_ice_lattice_vector1.clear();
    square_ice_lattice_vector1.push_back(1.0);
    square_ice_lattice_vector1.push_back(0.0);

    square_ice_lattice_vector2.clear();
    square_ice_lattice_vector2.push_back(0.0);
    square_ice_lattice_vector2.push_back(-1.0);

    //-------------------------------------------------------------------------

    double coordinate_x;
    double coordinate_y;

    vector<double> vertex_coordinates;

    //--------------------------------------------------------------------------------------------------


    vertex_coordinates_vector.clear();

    for (unsigned int index_row = 0; index_row < lattice_linear_size; index_row++)
    {
        for (unsigned int index_column = 0; index_column < lattice_linear_size; index_column++)
        {
            coordinate_x = index_row * square_ice_lattice_vector2[0] + index_column * square_ice_lattice_vector1[0];
            coordinate_y = index_row * square_ice_lattice_vector2[1] + index_column * square_ice_lattice_vector1[1];

            vertex_coordinates.clear();
            vertex_coordinates.push_back(lattice_parameter * coordinate_x);
            vertex_coordinates.push_back(lattice_parameter * coordinate_y);
            vertex_coordinates_vector.push_back(vertex_coordinates);
        }
    }

    number_of_vertices = vertex_coordinates_vector.size();

    //--------------------------------------------------------------------------------------------------
    //-------------------------------------------------------------------------
    // NOTE: The auxiliary sorting vector is used to ensure the ENWS storage order of the dipoles for each vertex.
    // This is achieved by computing the cosine and sine for the relative dipole position with respect to the vertex center during the search for the associated dipoles.
    // By using the abs(2 * cosine + sine + 1) function, this yields the values of 3,2,1,0 for E,N,W,S, respectively, making it easy to sort the dipoles afterwards.


    double current_relative_position_x;
    double current_relative_position_y;
    double current_relative_displacement;

    int cosine_value, sine_value;

    vector< vector<int> > vertex_to_dipole_array_aux;
    vector< vector<int> > vertex_to_dipole_sorting_array_aux;    

    vector<int> vertex_to_dipole_vector_aux;
    vector<int> vertex_to_dipole_sorting_vector_aux;


    vertex_to_dipole_array_aux.clear();
    vertex_to_dipole_sorting_array_aux.clear();

    for (unsigned int index_vertex = 0; index_vertex < number_of_vertices; index_vertex++)
    {
        vertex_to_dipole_vector_aux.clear();
        vertex_to_dipole_sorting_vector_aux.clear();

        for (unsigned int index_dipole = 0; index_dipole < number_of_dipoles; index_dipole++)
        {
            current_relative_position_x = dipole_coordinates_vector[index_dipole][0] - vertex_coordinates_vector[index_vertex][0];
            current_relative_position_y = dipole_coordinates_vector[index_dipole][1] - vertex_coordinates_vector[index_vertex][1];
            current_relative_displacement = sqrt(current_relative_position_x * current_relative_position_x + current_relative_position_y * current_relative_position_y);

            if ((current_relative_displacement > error) && (current_relative_displacement < 0.5 * lattice_parameter + error))
            {
                vertex_to_dipole_vector_aux.push_back(index_dipole);

                cosine_value = (int)(current_relative_position_x / current_relative_displacement);
                sine_value = (int)(current_relative_position_y / current_relative_displacement);
                vertex_to_dipole_sorting_vector_aux.push_back(abs(2 * cosine_value + sine_value + 1));                
            }
        }

        vertex_to_dipole_array_aux.push_back(vertex_to_dipole_vector_aux);
        vertex_to_dipole_sorting_array_aux.push_back(vertex_to_dipole_sorting_vector_aux);
    }

    //-------------------------------------------------------------------------
    // Sorting the dipole sequence in counter-clocwise order (starting from the Ox axis) for each vertex
    // Building the vertex-to-dipole array
   
    int aux_int, aux_int2;;


    vertex_to_dipole_array.clear();

    for (unsigned int index_vertex = 0; index_vertex < number_of_vertices; index_vertex++)
    {        
        vertex_to_dipole_vector_aux = vertex_to_dipole_array_aux[index_vertex];
        vertex_to_dipole_sorting_vector_aux = vertex_to_dipole_sorting_array_aux[index_vertex];

        for (unsigned int index_internal = 0; index_internal < vertex_to_dipole_vector_aux.size()-1; index_internal++)
        {
            for (unsigned int index_internal2 = index_internal + 1; index_internal2 < vertex_to_dipole_vector_aux.size(); index_internal2++)
            {
                if (vertex_to_dipole_sorting_vector_aux[index_internal] < vertex_to_dipole_sorting_vector_aux[index_internal2])
                {
                    aux_int = vertex_to_dipole_sorting_vector_aux[index_internal];
                    aux_int2 = vertex_to_dipole_vector_aux[index_internal];

                    vertex_to_dipole_sorting_vector_aux[index_internal] = vertex_to_dipole_sorting_vector_aux[index_internal2];
                    vertex_to_dipole_vector_aux[index_internal] = vertex_to_dipole_vector_aux[index_internal2];

                    vertex_to_dipole_sorting_vector_aux[index_internal2] = aux_int;
                    vertex_to_dipole_vector_aux[index_internal2] = aux_int2;
                }
            }           
        }

        vertex_to_dipole_array.push_back(vertex_to_dipole_vector_aux);
    }

    //--------------------------------------------------------------------------------------------------
    // Building the dipole-to-vertex array

    vector<int> dipole_to_vertex_vector;


    dipole_to_vertex_array.clear();

    for (unsigned int index_dipole = 0; index_dipole < number_of_dipoles; index_dipole++)
    {
        dipole_to_vertex_vector.clear();

        for (unsigned int index_vertex = 0; index_vertex < number_of_vertices; index_vertex++)
        {
            for (unsigned int index_internal = 0; index_internal < vertex_to_dipole_array[index_vertex].size(); index_internal++)
            {
                if ((unsigned int)(vertex_to_dipole_array[index_vertex][index_internal]) == index_dipole)
                    dipole_to_vertex_vector.push_back(index_vertex);
            }
        }

        while (dipole_to_vertex_vector.size() < 2)
            dipole_to_vertex_vector.push_back(-1);

        dipole_to_vertex_array.push_back(dipole_to_vertex_vector);
    }


    for (unsigned int index_dipole = 0; index_dipole < number_of_dipoles; index_dipole++)
    {
        if (dipole_unit_vectors_vector[index_dipole][0] > 0.5)
        {            
            if ((dipole_coordinates_vector[index_dipole][0] - vertex_coordinates_vector[dipole_to_vertex_array[index_dipole][0]][0]) < error)
            {         
                aux_int = dipole_to_vertex_array[index_dipole][0];
                dipole_to_vertex_array[index_dipole][0] = dipole_to_vertex_array[index_dipole][1];
                dipole_to_vertex_array[index_dipole][1] = aux_int;
            }
        }
        else
        {                        
            if ((dipole_coordinates_vector[index_dipole][1] - vertex_coordinates_vector[dipole_to_vertex_array[index_dipole][0]][1]) > error)
            {                
                aux_int = dipole_to_vertex_array[index_dipole][0];
                dipole_to_vertex_array[index_dipole][0] = dipole_to_vertex_array[index_dipole][1];
                dipole_to_vertex_array[index_dipole][1] = aux_int;
            }
        }        
    }

}//---------------------------------------------------------------------------------------------------------------------------------------------------
// END VERBATIM initialize_vertex_system
// BEGIN VERBATIM function initialize_spin_vertex_neighborhood_indices_array original_lines=1340-1471 sha256=4effe6bb34bac3281eeb733fbcf1f538ccd07be3cddbc584818c63c8ba257e8f
void initialize_spin_vertex_neighborhood_indices_array(vector< vector<double> >& dipole_coordinates_vector, vector< vector<double> >& dipole_unit_vectors_vector, vector< vector<int> >& spin_vertex_neighborhood_indices_array)
{//---------------------------------------------------------------------------------------------------------------------------------------------------
    
    //-------------------------------------------------------------------------
    // Local variables

    bool valid_spin_vertex_neighborhood;
    
    double reference_dipole_coordinate_x, reference_dipole_coordinate_y;
    double neighbor_dipole_coordinate_x, neighbor_dipole_coordinate_y;

    int reference_dipole_type;
    
    double current_relative_displacement;
    vector<double> current_relative_position_unit_vector;
    
    vector<int> spin_vertex_neighborhood_indices_vector;
    
    //-------------------------------------------------------------------------
    
    
    spin_vertex_neighborhood_indices_array.clear();
    
    for (unsigned int index_reference_dipole = 0; index_reference_dipole < number_of_dipoles; index_reference_dipole++)
    {
        reference_dipole_coordinate_x = dipole_coordinates_vector[index_reference_dipole][0];
        reference_dipole_coordinate_y = dipole_coordinates_vector[index_reference_dipole][1];
        
        reference_dipole_type = (int)(dipole_unit_vectors_vector[index_reference_dipole][1]);
    

        spin_vertex_neighborhood_indices_vector.clear();
        spin_vertex_neighborhood_indices_vector.push_back(index_reference_dipole);
        for (unsigned int index = 0; index < 6; index++)
            spin_vertex_neighborhood_indices_vector.push_back(-1);
        
        for (unsigned int index_neighbor_dipole = 0; index_neighbor_dipole < number_of_dipoles; index_neighbor_dipole++)
        {
            
            if (index_neighbor_dipole != index_reference_dipole)
            {
                neighbor_dipole_coordinate_x = dipole_coordinates_vector[index_neighbor_dipole][0];
                neighbor_dipole_coordinate_y = dipole_coordinates_vector[index_neighbor_dipole][1];

                current_relative_displacement = sqrt((neighbor_dipole_coordinate_x - reference_dipole_coordinate_x) * (neighbor_dipole_coordinate_x - reference_dipole_coordinate_x) + (neighbor_dipole_coordinate_y - reference_dipole_coordinate_y) * (neighbor_dipole_coordinate_y - reference_dipole_coordinate_y));

                if (current_relative_displacement < lattice_parameter + error)
                {
                    
                    current_relative_position_unit_vector.clear();
                    current_relative_position_unit_vector.push_back((neighbor_dipole_coordinate_x - reference_dipole_coordinate_x) / current_relative_displacement);
                    current_relative_position_unit_vector.push_back((neighbor_dipole_coordinate_y - reference_dipole_coordinate_y) / current_relative_displacement);
                    
                    if (reference_dipole_type == 0)
                    {
                        if (current_relative_displacement < (lattice_parameter - error))
                        {
                            if ( (current_relative_position_unit_vector[0] > 0.0) && (current_relative_position_unit_vector[1] > 0.0) )
                                spin_vertex_neighborhood_indices_vector[2] = (int)(index_neighbor_dipole);
                            
                            if ( (current_relative_position_unit_vector[0] < 0.0) && (current_relative_position_unit_vector[1] > 0.0) )
                                spin_vertex_neighborhood_indices_vector[3] = (int)(index_neighbor_dipole);
                            
                            if ( (current_relative_position_unit_vector[0] < 0.0) && (current_relative_position_unit_vector[1] < 0.0) )
                                spin_vertex_neighborhood_indices_vector[5] = (int)(index_neighbor_dipole);
                            
                            if ( (current_relative_position_unit_vector[0] > 0.0) && (current_relative_position_unit_vector[1] < 0.0) )
                                spin_vertex_neighborhood_indices_vector[6] = (int)(index_neighbor_dipole);
                        }
                        else
                        {
                            if (current_relative_position_unit_vector[0] > 0.0)
                                spin_vertex_neighborhood_indices_vector[1] = (int)(index_neighbor_dipole);
                            
                            if (current_relative_position_unit_vector[0] < 0.0)
                                spin_vertex_neighborhood_indices_vector[4] = (int)(index_neighbor_dipole);
                        }
                    }
                    else
                    {
                        if (current_relative_displacement < (lattice_parameter - error))
                        {
                            if ( (current_relative_position_unit_vector[0] > 0.0) && (current_relative_position_unit_vector[1] < 0.0) )
                                spin_vertex_neighborhood_indices_vector[2] = (int)(index_neighbor_dipole);
                            
                            if ( (current_relative_position_unit_vector[0] > 0.0) && (current_relative_position_unit_vector[1] > 0.0) )
                                spin_vertex_neighborhood_indices_vector[3] = (int)(index_neighbor_dipole);
                            
                            if ( (current_relative_position_unit_vector[0] < 0.0) && (current_relative_position_unit_vector[1] > 0.0) )
                                spin_vertex_neighborhood_indices_vector[5] = (int)(index_neighbor_dipole);
                            
                            if ( (current_relative_position_unit_vector[0] < 0.0) && (current_relative_position_unit_vector[1] < 0.0) )
                                spin_vertex_neighborhood_indices_vector[6] = (int)(index_neighbor_dipole);
                        }
                        else
                        {
                            if (current_relative_position_unit_vector[1] < 0.0)
                                spin_vertex_neighborhood_indices_vector[1] = (int)(index_neighbor_dipole);
                            
                            if (current_relative_position_unit_vector[1] > 0.0)
                                spin_vertex_neighborhood_indices_vector[4] = (int)(index_neighbor_dipole);
                        }
                    }
                }
            }
        }

        spin_vertex_neighborhood_indices_array.push_back(spin_vertex_neighborhood_indices_vector);
    }
    
    //-------------------------------------------------------------------------
    
    number_of_spin_vertex_neighborhood_configurations = 0;
    
    for (unsigned int index_dipole = 0; index_dipole < number_of_dipoles; index_dipole++)
    {
        spin_vertex_neighborhood_indices_vector = spin_vertex_neighborhood_indices_array[index_dipole];
        
        
        valid_spin_vertex_neighborhood = true;
        
        for (unsigned int index_internal = 0; index_internal < spin_vertex_neighborhood_indices_vector.size(); index_internal++)
            if (spin_vertex_neighborhood_indices_vector[index_internal] < 0)
                valid_spin_vertex_neighborhood = false;
     
        if (valid_spin_vertex_neighborhood)
            number_of_spin_vertex_neighborhood_configurations++;
    }
    
    //-------------------------------------------------------------------------
    
}//---------------------------------------------------------------------------------------------------------------------------------------------------
// END VERBATIM initialize_spin_vertex_neighborhood_indices_array
// BEGIN VERBATIM function initialize_dipole_island_volumes original_lines=1491-1508 sha256=10a123944fc8f8522a85d3c9aa172a616660d66060eebc4b27978ca12c32e67e
void initialize_dipole_island_volumes(vector<double>& dipole_island_lengths_vector, vector<double>& dipole_island_widths_vector, vector<double>& dipole_island_volumes_vector)
{//---------------------------------------------------------------------------------------------------------------------------------------------------

    double dipole_island_volume;

    //-------------------------------------------------------------------------

    
    dipole_island_volumes_vector.clear();

    for (unsigned int index_dipole = 0; index_dipole < number_of_dipoles; index_dipole++)
    {
        dipole_island_volume = (pi / 6.0) * dipole_island_lengths_vector[index_dipole] * dipole_island_widths_vector[index_dipole] * island_height;
        dipole_island_volumes_vector.push_back(dipole_island_volume);
    }

    
}//---------------------------------------------------------------------------------------------------------------------------------------------------
// END VERBATIM initialize_dipole_island_volumes
// BEGIN VERBATIM function initialize_reduced_temperature_prefactors_vector original_lines=1511-1531 sha256=4703ed880674b3bd068e94e4a56bc53b6273e471e9a87433b091cc65e2d9e2a4
void initialize_reduced_temperature_prefactors_vector(vector<double>& dipole_island_volumes_vector, vector<double>& reduced_temperature_prefactors_vector)
{//---------------------------------------------------------------------------------------------------------------------------------------------------

    //-------------------------------------------------------------------------
    // The constant 0.910179 is expressed in K and correponds to the a ratio between the magnetic permeability and the Boltzmann constant multiplied by the square of the reference magnetization (10^5 A/m) and the reference volume (10^-27m^3).
    // This effectively cancels the large exponents needed to express these constants, yielding a value that is closer to unity, thus avoiding floating-point errors.

    double current_reduced_temperature_prefactor;

    //-------------------------------------------------------------------------
    
    
    reduced_temperature_prefactors_vector.clear();

    for (unsigned int index_dipole = 0; index_dipole < number_of_dipoles; index_dipole++)
    {
        current_reduced_temperature_prefactor = 0.910179 * spontaneous_magnetization0 * spontaneous_magnetization0 * dipole_island_volumes_vector[index_dipole] / 2.0 / Curie_temperature;
        reduced_temperature_prefactors_vector.push_back(current_reduced_temperature_prefactor);
    }

}//---------------------------------------------------------------------------------------------------------------------------------------------------
// END VERBATIM initialize_reduced_temperature_prefactors_vector
// BEGIN VERBATIM function compute_charge_pair_normalized_displacement_ratio original_lines=1602-1609 sha256=a6df9a2bf42b380ab7ceb86fc0a075daeebb45a4a323898dfaf1681b4beb765e
double compute_charge_pair_normalized_displacement_ratio(int reference_dipole_sign, int neighbor_dipole_sign, double reference_dipole_island_length, double neighbor_dipole_island_length, vector<double>& reference_dipole_unit_vector, vector<double>& neighbor_dipole_unit_vector, double dipole_pair_relative_displacement, vector<double>& dipole_pair_relative_position )
{//---------------------------------------------------------------------------------------------------------------------------------------------------    

    double charge_pair_normalized_displacement_ratio = 1.0 + (reference_dipole_island_length / (3.0 * dipole_pair_relative_displacement)) * (reference_dipole_island_length / (3.0 * dipole_pair_relative_displacement)) + (neighbor_dipole_island_length / (3.0 * dipole_pair_relative_displacement)) * (neighbor_dipole_island_length / (3.0 * dipole_pair_relative_displacement)) + (2.0) / (3.0) * neighbor_dipole_sign * neighbor_dipole_island_length * compute_scalar_product(dipole_pair_relative_position, neighbor_dipole_unit_vector) / (dipole_pair_relative_displacement * dipole_pair_relative_displacement) - (2.0) / (3.0) * reference_dipole_sign * reference_dipole_island_length * compute_scalar_product(dipole_pair_relative_position, reference_dipole_unit_vector) / (dipole_pair_relative_displacement * dipole_pair_relative_displacement) - (2.0) / (9.0) * reference_dipole_sign * neighbor_dipole_sign * reference_dipole_island_length * neighbor_dipole_island_length * compute_scalar_product(neighbor_dipole_unit_vector, reference_dipole_unit_vector) / (dipole_pair_relative_displacement * dipole_pair_relative_displacement);

    return sqrt(charge_pair_normalized_displacement_ratio);

}//---------------------------------------------------------------------------------------------------------------------------------------------------
// END VERBATIM compute_charge_pair_normalized_displacement_ratio
// BEGIN VERBATIM function compute_dipole_pair_normalized_coupling_factor original_lines=1612-1626 sha256=f4ba9642f4c247b2cc883e50079ae3e96b276dfe01f75bb343921db3e68d4805
double compute_dipole_pair_normalized_coupling_factor(double reference_dipole_island_length, double neighbor_dipole_island_length, double neighbor_dipole_island_width, double neighbor_dipole_island_height, vector<double>& reference_dipole_unit_vector, vector<double>& neighbor_dipole_unit_vector, double dipole_pair_relative_displacement, vector<double>& dipole_pair_relative_position )
{//---------------------------------------------------------------------------------------------------------------------------------------------------

    double charge_pair_normalized_displacement_ratio_plus_plus = compute_charge_pair_normalized_displacement_ratio(+1, +1, reference_dipole_island_length, neighbor_dipole_island_length, reference_dipole_unit_vector, neighbor_dipole_unit_vector, dipole_pair_relative_displacement, dipole_pair_relative_position);
    double charge_pair_normalized_displacement_ratio_plus_minus = compute_charge_pair_normalized_displacement_ratio(+1, -1, reference_dipole_island_length, neighbor_dipole_island_length, reference_dipole_unit_vector, neighbor_dipole_unit_vector, dipole_pair_relative_displacement, dipole_pair_relative_position);
    double charge_pair_normalized_displacement_ratio_minus_plus = compute_charge_pair_normalized_displacement_ratio(-1, +1, reference_dipole_island_length, neighbor_dipole_island_length, reference_dipole_unit_vector, neighbor_dipole_unit_vector, dipole_pair_relative_displacement, dipole_pair_relative_position);
    double charge_pair_normalized_displacement_ratio_minus_minus = compute_charge_pair_normalized_displacement_ratio(-1, -1, reference_dipole_island_length, neighbor_dipole_island_length, reference_dipole_unit_vector, neighbor_dipole_unit_vector, dipole_pair_relative_displacement, dipole_pair_relative_position);

    double charge_pair_normalized_displacement_inverse_ratio = ((1.0 / charge_pair_normalized_displacement_ratio_plus_plus) + (1.0 / charge_pair_normalized_displacement_ratio_minus_minus) - (1.0 / charge_pair_normalized_displacement_ratio_plus_minus) - (1.0 / charge_pair_normalized_displacement_ratio_minus_plus));   

    double dipole_pair_normalized_coupling_factor = (3.0 / 16.0) * (neighbor_dipole_island_width * neighbor_dipole_island_height) / (reference_dipole_island_length * dipole_pair_relative_displacement) * charge_pair_normalized_displacement_inverse_ratio;

    return dipole_pair_normalized_coupling_factor;

}//---------------------------------------------------------------------------------------------------------------------------------------------------
// END VERBATIM compute_dipole_pair_normalized_coupling_factor
// BEGIN VERBATIM function initialize_dipole_interaction_web_arrays original_lines=1629-1772 sha256=4b307c1902aaa8846af3b171c62e5c0d775ee2eda7a331ed0840e1068e9107f3
void initialize_dipole_interaction_web_arrays(vector< vector<double> >& dipole_coordinates_vector, vector< vector<double> >& dipole_unit_vectors_vector, vector<double>& dipole_island_lengths_vector, vector<double>& dipole_island_widths_vector, vector< vector<int> >& spin_vertex_neighborhood_indices_array, vector< vector<int> >& dipole_interaction_web_indices_array, vector< vector<double> >& dipole_interaction_web_normalized_coupling_factors_array)
{//---------------------------------------------------------------------------------------------------------------------------------------------------

    //-------------------------------------------------------------------------
    // Local variables

    int neighbor_dipole_index;
    
    double reference_dipole_coordinate_x, reference_dipole_coordinate_y;
    double neighbor_dipole_coordinate_x, neighbor_dipole_coordinate_y;

    double current_relative_displacement;
    vector<double> current_relative_position;

    vector<double> reference_dipole_unit_vector;
    vector<double> neighbor_dipole_unit_vector;

    double reference_dipole_island_length;
    double neighbor_dipole_island_length;

    double neighbor_dipole_island_width;
    double neighbor_dipole_island_height;

    double normalized_coupling_factor;


    vector<int> dipole_interaction_web_indices_vector;
    vector<double> dipole_interaction_web_normalized_coupling_factors_vector;

    //-------------------------------------------------------------------------
    
    
    dipole_interaction_web_indices_array.clear();
    dipole_interaction_web_normalized_coupling_factors_array.clear();

    if (periodic_boundary_conditions_enabled)
    {

    }
    else
    {
        if (vertex_interaction_model_enabled)
        {
            for (unsigned int index_reference_dipole = 0; index_reference_dipole < number_of_dipoles; index_reference_dipole++)
            {
                reference_dipole_coordinate_x = dipole_coordinates_vector[index_reference_dipole][0];
                reference_dipole_coordinate_y = dipole_coordinates_vector[index_reference_dipole][1];
                
                reference_dipole_unit_vector = dipole_unit_vectors_vector[index_reference_dipole];
                
                reference_dipole_island_length = dipole_island_lengths_vector[index_reference_dipole];
                

                dipole_interaction_web_indices_vector.clear();
                dipole_interaction_web_normalized_coupling_factors_vector.clear();
                                                                
                for (unsigned int index_internal = 0; index_internal < spin_vertex_neighborhood_indices_array[index_reference_dipole].size(); index_internal++ )
                {
                    neighbor_dipole_index = spin_vertex_neighborhood_indices_array[index_reference_dipole][index_internal];
                 
                    
                    if ( (neighbor_dipole_index != -1) && (neighbor_dipole_index != (int)(index_reference_dipole)) )
                    {
                        neighbor_dipole_coordinate_x = dipole_coordinates_vector[neighbor_dipole_index][0];
                        neighbor_dipole_coordinate_y = dipole_coordinates_vector[neighbor_dipole_index][1];
                        
                        current_relative_displacement = sqrt((neighbor_dipole_coordinate_x - reference_dipole_coordinate_x) * (neighbor_dipole_coordinate_x - reference_dipole_coordinate_x) + (neighbor_dipole_coordinate_y - reference_dipole_coordinate_y) * (neighbor_dipole_coordinate_y - reference_dipole_coordinate_y));
                        
                        
                        current_relative_position.clear();
                        current_relative_position.push_back(neighbor_dipole_coordinate_x - reference_dipole_coordinate_x);
                        current_relative_position.push_back(neighbor_dipole_coordinate_y - reference_dipole_coordinate_y);
                        
                        neighbor_dipole_unit_vector = dipole_unit_vectors_vector[neighbor_dipole_index];
                        
                        neighbor_dipole_island_length = dipole_island_lengths_vector[neighbor_dipole_index];
                        neighbor_dipole_island_width = dipole_island_widths_vector[neighbor_dipole_index];
                        neighbor_dipole_island_height = island_height;
                        
                        
                        normalized_coupling_factor = compute_dipole_pair_normalized_coupling_factor(reference_dipole_island_length, neighbor_dipole_island_length, neighbor_dipole_island_width, neighbor_dipole_island_height, reference_dipole_unit_vector, neighbor_dipole_unit_vector, current_relative_displacement, current_relative_position);
                        
                        dipole_interaction_web_indices_vector.push_back(neighbor_dipole_index);
                        dipole_interaction_web_normalized_coupling_factors_vector.push_back(normalized_coupling_factor);
                    }
                }
                
                dipole_interaction_web_indices_array.push_back(dipole_interaction_web_indices_vector);
                dipole_interaction_web_normalized_coupling_factors_array.push_back(dipole_interaction_web_normalized_coupling_factors_vector);
            }
        }
        else
        {
            for (unsigned int index_reference_dipole = 0; index_reference_dipole < number_of_dipoles; index_reference_dipole++)
            {
                reference_dipole_coordinate_x = dipole_coordinates_vector[index_reference_dipole][0];
                reference_dipole_coordinate_y = dipole_coordinates_vector[index_reference_dipole][1];
                
                reference_dipole_unit_vector = dipole_unit_vectors_vector[index_reference_dipole];
                
                reference_dipole_island_length = dipole_island_lengths_vector[index_reference_dipole];
                
                
                dipole_interaction_web_indices_vector.clear();
                dipole_interaction_web_normalized_coupling_factors_vector.clear();
                
                for (unsigned int index_neighbor_dipole = 0; index_neighbor_dipole < number_of_dipoles; index_neighbor_dipole++)
                {
                    if (index_neighbor_dipole != index_reference_dipole)
                    {
                        neighbor_dipole_coordinate_x = dipole_coordinates_vector[index_neighbor_dipole][0];
                        neighbor_dipole_coordinate_y = dipole_coordinates_vector[index_neighbor_dipole][1];
                        
                        current_relative_displacement = sqrt((neighbor_dipole_coordinate_x - reference_dipole_coordinate_x) * (neighbor_dipole_coordinate_x - reference_dipole_coordinate_x) + (neighbor_dipole_coordinate_y - reference_dipole_coordinate_y) * (neighbor_dipole_coordinate_y - reference_dipole_coordinate_y));
                        
                        
                        if (current_relative_displacement < interaction_range_cutoff_radius + error)
                        {
                            current_relative_position.clear();
                            current_relative_position.push_back(neighbor_dipole_coordinate_x - reference_dipole_coordinate_x);
                            current_relative_position.push_back(neighbor_dipole_coordinate_y - reference_dipole_coordinate_y);
                            
                            neighbor_dipole_unit_vector = dipole_unit_vectors_vector[index_neighbor_dipole];
                            
                            neighbor_dipole_island_length = dipole_island_lengths_vector[index_neighbor_dipole];
                            neighbor_dipole_island_width = dipole_island_widths_vector[index_neighbor_dipole];
                            neighbor_dipole_island_height = island_height;
                            
                            normalized_coupling_factor = compute_dipole_pair_normalized_coupling_factor(reference_dipole_island_length, neighbor_dipole_island_length, neighbor_dipole_island_width, neighbor_dipole_island_height, reference_dipole_unit_vector, neighbor_dipole_unit_vector, current_relative_displacement, current_relative_position);
                            
                            dipole_interaction_web_indices_vector.push_back(index_neighbor_dipole);
                            dipole_interaction_web_normalized_coupling_factors_vector.push_back(normalized_coupling_factor);
                            
                        }
                    }
                }
                
                dipole_interaction_web_indices_array.push_back(dipole_interaction_web_indices_vector);
                dipole_interaction_web_normalized_coupling_factors_array.push_back(dipole_interaction_web_normalized_coupling_factors_vector);
            }
        }
    }

}//---------------------------------------------------------------------------------------------------------------------------------------------------
// END VERBATIM initialize_dipole_interaction_web_arrays
// BEGIN VERBATIM function initialize_dipole_athermal_interaction_fields original_lines=1775-1806 sha256=72dd66c8206b8fff69584bb300f3e1dd6fde1eec9a1594f0911572d0b2461938
void initialize_dipole_athermal_interaction_fields(vector<int>& dipole_states_vector, vector< vector<int> >& dipole_interaction_web_indices_array, vector< vector<double> >& dipole_interaction_web_normalized_coupling_factors_array, vector<double>& dipole_athermal_interaction_fields_vector, vector<double>& dipole_athermal_maximum_interaction_fields_vector)
{//---------------------------------------------------------------------------------------------------------------------------------------------------

    int neighbor_dipole_index, neighbor_dipole_state;   
    double current_dipole_athermal_interaction_field;
    double current_dipole_athermal_maximum_interaction_field;

    //-------------------------------------------------------------------------
    

    dipole_athermal_interaction_fields_vector.clear();
    dipole_athermal_maximum_interaction_fields_vector.clear();

    for (unsigned int index_reference_dipole = 0; index_reference_dipole < number_of_dipoles; index_reference_dipole++)
    {
        current_dipole_athermal_interaction_field = 0.0;
        current_dipole_athermal_maximum_interaction_field = 0.0;

        for (unsigned int index_internal = 0; index_internal < dipole_interaction_web_indices_array[index_reference_dipole].size(); index_internal++)
        {
            neighbor_dipole_index = dipole_interaction_web_indices_array[index_reference_dipole][index_internal];
            neighbor_dipole_state = dipole_states_vector[neighbor_dipole_index];
             
            current_dipole_athermal_interaction_field += dipole_interaction_web_normalized_coupling_factors_array[index_reference_dipole][index_internal] * neighbor_dipole_state;
            current_dipole_athermal_maximum_interaction_field += abs(dipole_interaction_web_normalized_coupling_factors_array[index_reference_dipole][index_internal]);         
        }
                    
        dipole_athermal_interaction_fields_vector.push_back(current_dipole_athermal_interaction_field);
        dipole_athermal_maximum_interaction_fields_vector.push_back(current_dipole_athermal_maximum_interaction_field);
    }

}//---------------------------------------------------------------------------------------------------------------------------------------------------
// END VERBATIM initialize_dipole_athermal_interaction_fields
// BEGIN VERBATIM function initialize_reduced_temperature_factors_array original_lines=1895-1925 sha256=a14c91eb80521853e7cbe977d374fddffccc159b764800541817faf5cb1f6bda
void initialize_reduced_temperature_factors_array(vector<double>& reduced_temperature_prefactors_vector, vector<double>& temperature_vector, vector< vector<double> >& reduced_temperature_factors_array)
{//---------------------------------------------------------------------------------------------------------------------------------------------------

    double current_reduced_temperature;
    double current_reduced_temperature_prefactor;
    double current_reduced_temperature_factor;

    vector<double> reduced_temperature_factors_vector;
    
    //-------------------------------------------------------------------------


    reduced_temperature_factors_array.clear();

    for (unsigned int index_temperature = 0; index_temperature < temperature_vector.size(); index_temperature++)
    {        
        reduced_temperature_factors_vector.clear();

        for (unsigned int index_reference_dipole = 0; index_reference_dipole < number_of_dipoles; index_reference_dipole++)
        {
            current_reduced_temperature = temperature_vector[index_temperature] / Curie_temperature;
            current_reduced_temperature_prefactor = reduced_temperature_prefactors_vector[index_reference_dipole];
            
            current_reduced_temperature_factor = current_reduced_temperature_prefactor * pow((1.0 - current_reduced_temperature), 2.0 * magnetization_critical_exponent) / current_reduced_temperature;
            reduced_temperature_factors_vector.push_back(current_reduced_temperature_factor);
        }

        reduced_temperature_factors_array.push_back(reduced_temperature_factors_vector);
    }

}//---------------------------------------------------------------------------------------------------------------------------------------------------
// END VERBATIM initialize_reduced_temperature_factors_array
// BEGIN VERBATIM function reinitialize_reversal_times original_lines=2256-2299 sha256=0074e4c661ddb121fcd3e3acfa6c58ad1dbe7a45887841c6534053e54269f868
void reinitialize_reversal_times (unsigned int index_temperature, vector< vector<double> >& reduced_temperature_factors_array, vector<double>& dipole_island_demagnetization_factors_difference_vector, vector<double>& dipole_athermal_interaction_fields_vector, vector<int>& dipole_states_vector, vector<double>& reversal_times_vector)
{//---------------------------------------------------------------------------------------------------------------------------------------------------

    int current_dipole_state;
    double current_reduced_temperature_factor;
    double current_dipole_island_demagnetization_factors_difference;
    double current_dipole_athermal_interaction_field;    
    double current_reversal_time_exponent;

    double current_reversal_time;
    
    //-------------------------------------------------------------------------

    
    reversal_times_vector.clear();

    for (unsigned int index_dipole = 0; index_dipole < number_of_dipoles; index_dipole++)
    {
        current_dipole_state = dipole_states_vector[index_dipole];

        current_reduced_temperature_factor = reduced_temperature_factors_array[index_temperature][index_dipole];
        current_dipole_island_demagnetization_factors_difference = dipole_island_demagnetization_factors_difference_vector[index_dipole];
        current_dipole_athermal_interaction_field = dipole_athermal_interaction_fields_vector[index_dipole];

        current_reversal_time_exponent = current_reduced_temperature_factor * (barrier_adjustment_ratio * current_dipole_island_demagnetization_factors_difference - interaction_adjustment_ratio * current_dipole_athermal_interaction_field * current_dipole_state);

        // such events should be stored in a simulation log
        if (current_reversal_time_exponent < error)
        {
            current_reversal_time_exponent = 0.0;
            update_simulation_log_file(1, index_temperature, -1, -1);
        }

        if (current_reversal_time_exponent > maximum_allowed_exponent - error)
        {
            current_reversal_time_exponent = maximum_allowed_exponent;
            update_simulation_log_file(2, index_temperature, -1, -1);
        }

        current_reversal_time = tau0 * exp(current_reversal_time_exponent);
        reversal_times_vector.push_back(current_reversal_time);
    }

}//---------------------------------------------------------------------------------------------------------------------------------------------------
// END VERBATIM reinitialize_reversal_times
// BEGIN VERBATIM function update_reference_dipole_reversal_time original_lines=2428-2462 sha256=4582a9fa228b23e22d82e8b7a77ebd5f7f3fc6d436ac970ea2904161a5711f41
void update_reference_dipole_reversal_time (unsigned int index_temperature, unsigned int index_acquisition, unsigned int index_sweep, unsigned int reference_dipole_index, vector< vector<double> >& reduced_temperature_factors_array, vector<double>& dipole_athermal_interaction_fields_vector, vector<int>& dipole_states_vector, vector<double>& reversal_times_vector)
{//---------------------------------------------------------------------------------------------------------------------------------------------------

    double previous_reversal_time;
    double previous_reversal_time_exponent;
    double new_reversal_time;
    double new_reversal_time_exponent;

    previous_reversal_time = reversal_times_vector[reference_dipole_index];
    previous_reversal_time_exponent = log(previous_reversal_time);

    //-------------------------------------------------------------------------

    new_reversal_time_exponent = previous_reversal_time_exponent + 2.0 * interaction_adjustment_ratio * reduced_temperature_factors_array[index_temperature][reference_dipole_index] * dipole_states_vector[reference_dipole_index] * dipole_athermal_interaction_fields_vector[reference_dipole_index];
    

    if (new_reversal_time_exponent > maximum_allowed_exponent - error)
    {
        new_reversal_time_exponent = maximum_allowed_exponent;
        update_simulation_log_file(2, index_temperature, index_acquisition, index_sweep);
    }

    if (new_reversal_time_exponent < -maximum_allowed_exponent + error)
    {
        new_reversal_time_exponent = -maximum_allowed_exponent;
        update_simulation_log_file(3, index_temperature, index_acquisition, index_sweep);
    }

    //-------------------------------------------------------------------------

    new_reversal_time = exp(new_reversal_time_exponent);

    reversal_times_vector[reference_dipole_index] = new_reversal_time;

}//---------------------------------------------------------------------------------------------------------------------------------------------------
// END VERBATIM update_reference_dipole_reversal_time
// BEGIN VERBATIM function update_neighbor_dipole_reversal_time original_lines=2465-2499 sha256=64594e27b29d248fa588dd32b25774e52d8c8e6d6f0d5118f624befbf1f3ec76
void update_neighbor_dipole_reversal_time(unsigned int index_temperature, unsigned int index_acquisition, unsigned int index_sweep, unsigned int reference_dipole_index, unsigned int neighbor_dipole_index, vector< vector<double> >& reduced_temperature_factors_array, double normalized_coupling_factor, vector<int>& dipole_states_vector, vector<double>& reversal_times_vector)
{//---------------------------------------------------------------------------------------------------------------------------------------------------

    double previous_reversal_time;
    double previous_reversal_time_exponent;
    double new_reversal_time;
    double new_reversal_time_exponent;

    previous_reversal_time = reversal_times_vector[neighbor_dipole_index];
    previous_reversal_time_exponent = log(previous_reversal_time);

    //-------------------------------------------------------------------------

    new_reversal_time_exponent = previous_reversal_time_exponent + (2.0) * interaction_adjustment_ratio * reduced_temperature_factors_array[index_temperature][neighbor_dipole_index] * normalized_coupling_factor * dipole_states_vector[neighbor_dipole_index] * dipole_states_vector[reference_dipole_index];


    if (new_reversal_time_exponent > maximum_allowed_exponent - error)
    {
        new_reversal_time_exponent = maximum_allowed_exponent;
        update_simulation_log_file(2, index_temperature, index_acquisition, index_sweep);
    }

    if (new_reversal_time_exponent < -maximum_allowed_exponent + error)
    {
        new_reversal_time_exponent = -maximum_allowed_exponent;
        update_simulation_log_file(3, index_temperature, index_acquisition, index_sweep);
    }

    //-------------------------------------------------------------------------

    new_reversal_time = exp(new_reversal_time_exponent);

    reversal_times_vector[neighbor_dipole_index] = new_reversal_time;

}//---------------------------------------------------------------------------------------------------------------------------------------------------
// END VERBATIM update_neighbor_dipole_reversal_time
// BEGIN VERBATIM function update_interaction_fields original_lines=2502-2518 sha256=09e86854c2f2f17e425ca242bc63120cabe2149f86a879bcc5059b093b8d5c9f
void update_interaction_fields (unsigned int index_temperature, unsigned int index_acquisition, unsigned int index_sweep, unsigned int reference_dipole_index, vector< vector<double> >& reduced_temperature_factors_array, vector< vector<int> >& dipole_interaction_web_indices_array, vector< vector<double> >& dipole_interaction_web_normalized_coupling_factors_array, vector<double>& dipole_athermal_interaction_fields_vector, vector<int>& dipole_states_vector, vector<double>& reversal_times_vector)
{//---------------------------------------------------------------------------------------------------------------------------------------------------

    unsigned int neighbor_dipole_index;
    double normalized_coupling_factor;

    for (unsigned int index_neighbor = 0; index_neighbor < dipole_interaction_web_indices_array[reference_dipole_index].size(); index_neighbor++)
    {        
        neighbor_dipole_index = dipole_interaction_web_indices_array[reference_dipole_index][index_neighbor];
        normalized_coupling_factor = dipole_interaction_web_normalized_coupling_factors_array[reference_dipole_index][index_neighbor];
        
        dipole_athermal_interaction_fields_vector[neighbor_dipole_index] += (- 2.0) * normalized_coupling_factor * dipole_states_vector[reference_dipole_index];        

        update_neighbor_dipole_reversal_time(index_temperature, index_acquisition, index_sweep, reference_dipole_index, neighbor_dipole_index, reduced_temperature_factors_array, normalized_coupling_factor, dipole_states_vector, reversal_times_vector);
    }
        
}//---------------------------------------------------------------------------------------------------------------------------------------------------
// END VERBATIM update_interaction_fields
// BEGIN VERBATIM function compute_vertex_statistics original_lines=2691-2791 sha256=cbc1c7171e67612f44b7fe09e89e4028e1be1186828ddc27c10d5c4f0225e4b2
void compute_vertex_statistics(vector<int>& current_dipole_states_vector, vector< vector<int> >& vertex_to_dipole_array, vector< vector<int> >& dipole_to_vertex_array, vector<double>& vertex_types_percentages_vector, double& order_parameter)
{//---------------------------------------------------------------------------------------------------------------------------------------------------

    //-------------------------------------------------------------------------
    // Local variables
    
    unsigned int index_row, index_column;
    int current_sign, order_parameter_count;

    int vertex_state, vertex_type;
    int current_dipole_state;

    vector<int> vertex_states_vector;
    vector<int> vertex_types_vector;
    vector<int> vertex_types_count_vector;

    //-------------------------------------------------------------------------
    // Building the vertex states vector

    vertex_states_vector.clear();

    for (unsigned int index_vertex = 0; index_vertex < number_of_vertices; index_vertex++)
    {
        vertex_state = 0;

        for (unsigned int index_internal = 0; index_internal < vertex_to_dipole_array[index_vertex].size(); index_internal++)
        {
            current_dipole_state = current_dipole_states_vector[vertex_to_dipole_array[index_vertex][index_internal]];
            vertex_state += (int)(pow(2.0, index_internal) * ((double)(current_dipole_state + 1)) / 2.0);
        }

        vertex_states_vector.push_back(vertex_state);
    }
    
    //-------------------------------------------------------------------------
    // Identifying the vertex types

    vertex_types_vector.clear();

    for (unsigned int index_vertex = 0; index_vertex < number_of_vertices; index_vertex++)
    {
        vertex_state = vertex_states_vector[index_vertex];

        if ((vertex_state == 3) || (vertex_state == 12))
            vertex_type = 1;

        if ((vertex_state == 0) || (vertex_state == 5) || (vertex_state == 10) || (vertex_state == 15))
            vertex_type = 2;

        if ((vertex_state == 1) || (vertex_state == 2) || (vertex_state == 4) || (vertex_state == 7) || (vertex_state == 8) || (vertex_state == 11) || (vertex_state == 13) || (vertex_state == 14))
            vertex_type = 3;

        if ((vertex_state == 6) || (vertex_state == 9))
            vertex_type = 4;

        vertex_types_vector.push_back(vertex_type);
    }
    
    //-------------------------------------------------------------------------
    // Vertex type percentages & order parameter

    vertex_types_count_vector.clear();
    vertex_types_count_vector.push_back(0);
    vertex_types_count_vector.push_back(0);
    vertex_types_count_vector.push_back(0);
    vertex_types_count_vector.push_back(0);

    order_parameter_count = 0;

    for (unsigned int index_vertex = 0; index_vertex < number_of_vertices; index_vertex++)
    {
        vertex_types_count_vector[vertex_types_vector[index_vertex] - 1]++;

        index_row = (unsigned int)(index_vertex / lattice_linear_size);
        index_column = (unsigned int)(index_vertex % lattice_linear_size);

        if ((index_row + index_column) % 2 == 0)
            current_sign = 1;
        else current_sign = -1;
            
        if (vertex_states_vector[index_vertex] == 3)
            order_parameter_count += (+1) * current_sign;
        if (vertex_states_vector[index_vertex] == 12)
            order_parameter_count += (-1) * current_sign;
    }

    vertex_types_percentages_vector.clear();

    for (unsigned int index_vertex_type = 0; index_vertex_type < vertex_types_count_vector.size(); index_vertex_type++)
        vertex_types_percentages_vector.push_back((double)(vertex_types_count_vector[index_vertex_type]) / (double)(number_of_vertices));
    


    order_parameter = (double)(order_parameter_count) / (double)(number_of_vertices);

    //!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11
    //!  change from original code
    //! 
    order_parameter = abs(order_parameter);

}//---------------------------------------------------------------------------------------------------------------------------------------------------
// END VERBATIM compute_vertex_statistics

// ---------------- NON-VERBATIM driver ----------------
static void pv(const char* k, const vector<double>& v){ cout<<k; for(double x: v) cout<<' '<<setprecision(17)<<x; cout<<"\n"; }
int main(int argc, char** argv)
{
    (void)argc; (void)argv;
    cout<<setprecision(17);
    int L, vertex_flag, nconf; double cutoff, length_scale, T, kappa, lat;
    if(!(cin>>L>>vertex_flag>>cutoff>>length_scale>>T>>kappa>>lat>>nconf)) return 2;
    lattice_linear_size = (unsigned int)L;
    vertex_interaction_model_enabled = (vertex_flag!=0);
    if (cutoff>0) interaction_range_cutoff_radius = cutoff;
    if (lat>0) lattice_parameter = lat;
    lattice_parameter *= length_scale; island_length_mean *= length_scale; island_width_mean *= length_scale; island_height *= length_scale;
    interaction_adjustment_ratio = kappa;
    initialize_Curie_temperature();
    vector<unsigned int> seq; vector< vector<double> > coords, units; vector<double> lengths, widths;
    initialize_dipole_system(seq, coords, units, lengths, widths);
    vector<double> volumes; initialize_dipole_island_volumes(lengths, widths, volumes);
    vector<double> prefs; initialize_reduced_temperature_prefactors_vector(volumes, prefs);
    vector<double> temps(1, T); vector< vector<double> > rtf; initialize_reduced_temperature_factors_array(prefs, temps, rtf);
    vector< vector<double> > vcoords; vector< vector<int> > d2v, v2d;
    initialize_vertex_system(coords, units, vcoords, d2v, v2d);
    vector< vector<int> > svn; initialize_spin_vertex_neighborhood_indices_array(coords, units, svn);
    vector< vector<int> > web_idx; vector< vector<double> > web_k;
    initialize_dipole_interaction_web_arrays(coords, units, lengths, widths, svn, web_idx, web_k);
    cout<<"META "<<number_of_dipoles<<" "<<number_of_vertices<<" "<<Curie_temperature<<" "<<spontaneous_magnetization0<<" "<<magnetization_critical_exponent<<" "<<island_height<<" "<<lattice_parameter<<" "<<kappa<<"\n";
    for(unsigned i=0;i<number_of_dipoles;i++) cout<<"DIPOLE "<<i<<" "<<coords[i][0]<<" "<<coords[i][1]<<" "<<units[i][0]<<" "<<units[i][1]<<" "<<lengths[i]<<" "<<widths[i]<<" "<<volumes[i]<<" "<<rtf[0][i]<<"\n";
    for(unsigned v=0;v<number_of_vertices;v++){ cout<<"VERTEX "<<v<<" "<<vcoords[v][0]<<" "<<vcoords[v][1]; for(int d: v2d[v]) cout<<" "<<d; cout<<"\n"; }
    for(unsigned i=0;i<number_of_dipoles;i++) for(unsigned k=0;k<web_idx[i].size();k++) cout<<"WEB "<<i<<" "<<web_idx[i][k]<<" "<<web_k[i][k]<<"\n";
    const double DELTA_N_STANDIN = 1.0; // arbitrary positive stand-in; cancels in every difference used
    vector<double> dN(number_of_dipoles, DELTA_N_STANDIN);
    for(int c=0;c<nconf;c++){
        string s; cin>>s; vector<int> st(number_of_dipoles); for(unsigned i=0;i<number_of_dipoles;i++) st[i]=(s[i]=='+')?1:-1;
        vector<double> h, hmax; initialize_dipole_athermal_interaction_fields(st, web_idx, web_k, h, hmax);
        vector<double> rt; reinitialize_reversal_times(0, rtf, dN, h, st, rt);
        vector<double> tp; double op; compute_vertex_statistics(st, v2d, d2v, tp, op);
        cout<<"CONF "<<s<<" TYPES "<<tp[0]<<" "<<tp[1]<<" "<<tp[2]<<" "<<tp[3]<<"\n";
        pv("H", h);
        vector<double> dx(number_of_dipoles), hinc(number_of_dipoles), rtinc(number_of_dipoles);
        for(unsigned k=0;k<number_of_dipoles;k++){
            vector<int> st2=st; vector<double> h2=h; vector<double> rt2=rt;
            double before=log(rt2[k]);
            update_reference_dipole_reversal_time(0,0,0,k,rtf,h2,st2,rt2);
            dx[k]=log(rt2[k])-before;
            update_interaction_fields(0,0,0,k,rtf,web_idx,web_k,h2,st2,rt2);
            st2[k]*=-1;
            vector<double> hfull, hmax2; initialize_dipole_athermal_interaction_fields(st2, web_idx, web_k, hfull, hmax2);
            vector<double> rtfull; reinitialize_reversal_times(0, rtf, dN, hfull, st2, rtfull);
            double mh=0, mr=0;
            for(unsigned n=0;n<number_of_dipoles;n++){ mh=fmax(mh,fabs(h2[n]-hfull[n])); if(n!=k) mr=fmax(mr,fabs(log(rt2[n])-log(rtfull[n]))); }
            hinc[k]=mh; rtinc[k]=mr;
        }
        pv("DX", dx); pv("HINC", hinc); pv("RTINC", rtinc);
    }
    cout<<"LOGCOUNTS "<<g_log_counts[1]<<" "<<g_log_counts[2]<<" "<<g_log_counts[3]<<"\n";
    return 0;
}

