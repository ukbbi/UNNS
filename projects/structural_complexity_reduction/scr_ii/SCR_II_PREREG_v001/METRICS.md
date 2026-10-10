# Metrics

For each instance:

## Exact preservation

\[
P_{preserve}=\mathbf{1}[S_{SCR}=S_{baseline}].
\]

This is binary and mandatory.

## Candidate-leaf reduction

\[
R_{leaf}=1-rac{L_{SCR}}{L_{baseline}}.
\]

## Node-expansion reduction

\[
R_{node}=1-rac{N_{SCR}}{N_{baseline}}.
\]

`R_node` is the primary search-reduction metric.

## End-to-end time gain

\[
G_{time}=rac{T_{baseline}}{T_{filter}+T_{downstream,SCR}}.
\]

Implementation must measure the combined SCR arm directly; filter overhead cannot be hidden.

## Memory

Peak resident memory of baseline and SCR arms, measured at process level when available.

## Effective branching factor

For depth `d` and expanded nodes `N`:

\[
b_{eff}=\exp(\log(\max(N,1))/d).
\]

Reported for baseline and SCR.

## Scaling fit

Fit

\[
\log_2 N = a+lpha d
\]

separately for median baseline and median SCR node counts across primary depths.

`Δα = α_baseline-α_SCR` is exploratory, not required for primary confirmation.
