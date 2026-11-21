# FUG-I v004 — Frozen mathematical specification

## Fixed substrate and selected continuation

The founding UNNS arithmetic is **unchanged**:

`M ⟂ N = M*(N+1)^2/N`, for positive integer `M,N`, including rational non-anchor outputs.

This particular investigation uses the **explicitly selected** integer self-substitution continuation grammar:

`T_N(x) = x*(N+1)^2/N`, legal when `x,N` are positive integers and `N | x`.

This grammar (SELECT-II) is a chosen way to form legal histories; it is not a replacement for the complete rational occurrence domain.

## Histories

A **word** `w=(N_1,...,N_k)` is an ordered list of positive labels; `()` is empty. It is admissible from source `x` when every intermediate `T_N` operation is legal. Its multiplier is `Q(w)=prod_j ((N_j+1)^2/N_j)`. Let `W(y)` denote all admissible finite words (including empty) that end at `y` from at least one positive integer source. The source is unique for a fixed word and endpoint, because every multiplier is strictly positive.

Every nonempty forward step multiplies a positive integer by at least four. Consequently, `W(y)` is finite for every fixed positive integer `y`.

For a word `w` let `K(w)` be the minimum positive legal source, characterized by the divisibility threshold of the prefixes, and `E(w)=K(w)*Q(w)` its minimum positive integer endpoint. Then `w in W(y)` precisely when `E(w) | y`.

## Fibonacci overlay

`F_0=0, F_1=F_2=1`, `F_(n+2)=F_(n+1)+F_n`. The index is retained, even when two early values are equal. For integer `q>=1`, let the **Fibonacci rank of apparition** `z(q)` be the least positive `n` satisfying `q | F_n`; set `z(1)=1`.

Define `W_F(n)=W(F_n)` and `P_n(t)=sum_{w in W_F(n)} t^length(w)`.

The rank activation of a word is `z(E(w))`. The first index of joint admissibility of several specified words (not necessarily sharing a source) is the lcm of their individual ranks.

## Source-locked merger

Two distinct words `w,v` form a **source-locked merger** at `y` if both are admissible from the same source `x` and their outputs equal `y`. This is stronger than both words occurring separately in `W(y)`.

## Finite alphabet restriction

For the infinite delayed-activation result, the chosen finite alphabet is

`A={1,2,3,5,7,11}`.

`W_A(y)` consists of admissible words using only labels from A, and `D_A(y)={N in A:(N+1)^2|y}` gives the one-step incoming labels. The infinite first-new-depth-two theorem applies to this **explicit restricted grammar**, not automatically to all possible N.

## Evidence status

- **PROVED:** Theorems 4.1–4.6 in THEOREMS.md, elementary deductions from the fixed substrate and classical Fibonacci properties.
- **VERIFIED-EXACT:** All enumerations and local Python checks for indices 1–84, modulo-64 residue checks, and explicit representatives.
- **NOT ESTABLISHED:** Global novelty or universality; infinite unchanged *unrestricted* immediate label sets; a physical mechanism; a complete classification of all Fibonacci merger words.
