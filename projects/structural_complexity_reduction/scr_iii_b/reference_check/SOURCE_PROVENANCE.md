# Original Dryad source probe v004

Original archive: `scr_iii_b/references/public_code/SPMMC_Code.zip` (not included or modified in this patch).
SHA-256 archive: `77c82d83ea20eff5abcab8323b061edf759809cdd4366e86042147f6ea60a5dd`
Original entry: `SPMMC Code/SPMMC-SSI-Unix-v1.00.cpp`
SHA-256 original C++: `f7ffe5ff3bdff923e1281c3ed7431dfece5ce0c596ffe3f60a5b037908ab750a`

Verbatim source function bodies, extracted (no manual formula rewriting):
- `compute_scalar_product`: original lines 669–679
- `compute_charge_pair_normalized_displacement_ratio`: original lines 1602–1609
- `compute_dipole_pair_normalized_coupling_factor`: original lines 1612–1626

Probe main, includes and `using namespace std` are independently added to drive the extracted functions on fixed small-patch coordinates. These are not a full simulation run. Do not imply original Monte Carlo outputs or full physical Hamiltonian validation.
