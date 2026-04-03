HD mu 17-point sweep pack
Construction: inferred Tier A-style vib/rot split from HITRAN .par records
Parsing: fixed-width wavenumber field [3:15], lower energy [45:55], local lower quanta [112:127]
Band inference: lower/upper energy manifolds ranked by J and J' to assign (upper_band, lower_band)
nu_vib = min(nu) within inferred band; nu_rot = nu - nu_vib
Deformation: nu_beta = nu_vib*beta^(-1/2) + nu_rot*beta^(-1)
CSV format: numeric only, one value per line, no headers
