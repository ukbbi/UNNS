# ROUTE_CSP_I v002 — Multiplicity-Controlled Benchmark

## Nominal candidates

A candidate is a binary route of depth `d`:

\[
x=(x_1,\ldots,x_d),\quad x_i\in\{0,1\}.
\]

Nominal complete-route count:

\[
|S_{nominal}|=2^d.
\]

## Structural layer

Each branch option has:

- route symbol in `{A,B,C,D}`;
- boundary phase in `{0,1,2}`;
- discontinuity marker;
- branch ID.

The structural skeleton retains the same frozen route grammar used by SCR-II v001.

One structurally valid route is embedded only to ensure that the structural search space itself is nonempty. It does **not** determine the arithmetic target in v002.

## Arithmetic layer

Each branch option independently receives:

- integer cost in `[1,1000]`;
- checksum weight modulo `5`.

A separate arithmetic RNG also generates an anchor bit string. The anchor determines:

- checksum target modulo 5;
- center of the cost interval;
- terminal seal bit.

The structural filter is never evaluated when choosing the anchor or arithmetic target.

## Exact downstream solution predicate

A route is an exact solution iff:

1. checksum modulo 5 equals the instance target;
2. total cost lies in the frozen cost interval;
3. final branch bit equals the terminal seal.

## Multiplicity acceptance

After arithmetic target construction, the exact **baseline** solver enumerates all `2^d` routes.

The arithmetic attempt is accepted only if:

\[
0.02 \le |S_{solution}|/2^d \le 0.04.
\]

No structural-filter result is consulted.

If the band is not reached, only the arithmetic layer is regenerated with the next deterministic attempt index, up to 64 attempts.

If no attempt succeeds, instance generation fails rather than changing the frozen band.
