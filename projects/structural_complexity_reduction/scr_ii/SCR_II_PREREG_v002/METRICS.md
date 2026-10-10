# SCR-II v002 Metrics

Primary metrics:

## Exact solution preservation

\[
P_{preserve}=\mathbf{1}[S_{SCR}=S_{baseline}].
\]

Mandatory per primary instance.

## Node reduction

\[
R_{node}=1-N_{SCR}/N_{baseline}.
\]

## Leaf reduction

\[
R_{leaf}=1-L_{SCR}/L_{baseline}.
\]

## End-to-end gain

\[
G_{time}=T_{baseline}/T_{SCR,total}.
\]

Structural-filter cost must be included in `T_SCR,total`.

## Solution density

\[
\rho_{solution}=|S_{baseline}|/2^d.
\]

Every accepted v002 instance must satisfy `0.02 <= rho_solution <= 0.04`.

## Candidate solution recall

\[
R_{solution}=|S_{SCR}|/|S_{baseline}|.
\]

This diagnostic is distinct from exact set preservation: the primary requirement remains `R_solution = 1` and exact hash equality.
