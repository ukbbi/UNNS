# Zhu unused-ratio inventory v001

The public Zhu archive does contain the two useful non-golden-ratio regimes identified in
the paper:

- `f2/f1 = 1/sqrt(5)` at `f1 = 40 sqrt(5) kHz`, `f2 = 40 kHz`;
- `f2/f1 = 3/(2 sqrt(5))` at `f1 = 40 sqrt(5) kHz`, `f2 = 60 kHz`.

However, the available Fig. 4 material is not time-domain trajectory data.

## Fig. 4(a)

- 201 CSV spectra
- f1 sweep 89.000--91.000 kHz in 0.010 kHz steps
- fixed f2 = 40 kHz
- CSV header: `Frequency(Hz),Transmission`

## Fig. 4(b)

- 201 CSV spectra
- f1 sweep 89.000--91.000 kHz in 0.010 kHz steps
- fixed f2 = 60 kHz
- CSV header: `Frequency(Hz),Transmission`

## Fig. 4(c)--(f)

Four two-column XLSX files, each 489 rows, containing the plotted frequency-domain spectra.

## Consequence

These records can support a descriptive frequency-lattice study at other irrational ratios,
but they cannot legitimately enter JPR or fractional-cover time-domain qualification.

No inverse FFT or synthetic reconstruction will be used.

Therefore the **different-irrational-ratio time-domain challenge remains unresolved**.
