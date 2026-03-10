from astropy.io import fits
import csv
import random

fits_file = "BGS_BRIGHT_full.dat.fits"
out_file = "desi_sample_ra_dec_z.csv"

MAX_ROWS = 2000000   # 2 million galaxies

with fits.open(fits_file, memmap=True) as hdul:
    data = hdul[1].data
    
    ra = data['RA']
    dec = data['DEC']
    z = data['Z_not4clus']

    N = len(ra)
    indices = random.sample(range(N), min(MAX_ROWS, N))

    with open(out_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["RA","DEC","Z"])

        for i in indices:
            writer.writerow([ra[i], dec[i], z[i]])

print("DESI sample extraction finished.")