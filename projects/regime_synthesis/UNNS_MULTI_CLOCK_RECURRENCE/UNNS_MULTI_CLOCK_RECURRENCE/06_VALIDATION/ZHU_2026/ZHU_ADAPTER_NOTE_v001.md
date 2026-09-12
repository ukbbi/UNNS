# Zhu adapter note

Source records:
- 数据/fig1/fig1(c1).xlsx
- 数据/fig1/fig1(c3).xlsx

The two XLSX columns are ingested as:
- first column -> `time_ms`
- second column -> `response`

Source drive:
- f1 = 88 kHz
- f2 = 54.387 kHz
- torus ratio used by locked v002 = golden ratio from the pre-analysis lock

Coordinate:
`x = f2[kHz] * time_ms`

No publisher Fourier spectrum is used as metric input.
