# FIELD-I v007 — Results: Persistent-G Growth and Collapse

field7.py: 13 PASS, 16 DATA, 3 OPEN, 0 FAIL, 16 DATA, 3 OPEN, 0 FAIL (`output/field7_output.txt`); predecessors rerun unchanged.

## Headline
**Universal G-collapse is false.** There are collective orbits with G(x_n) = 5 for every n, and more generally G = g for every g >= 5 coprime to 6 (T38, T38a). This is a second infinite asymptotic regime: P_g, the g-twisted version of regime I.

- Explicit orbit: x_0 = 254016/5 = 504^2/5. Then x_1 = 508032/5, x_2 = 762048/5, x_3 = 1016064/5 = 4 x_0, ... ; D = {d | s_n : d = 1 mod 5}, lcm D = s_n, G = 5 at every step; s doubles every three steps. Checked by direct iteration of the collective map for 150 steps (K10.1) and for 14 values of g (K10.3, g up to 77).
- The first sighting was not designed: the natural seed 45828/5 stays at G = 5 for 400 steps (K10.2) and enters the family at step 3. Of 557 natural seeds with G = 5 (a<25000) 10 persist (K10.5), all of them eventually in the form x = s^2 t/5 with x_(n+3) = 4 x_n (K10.5b).
- v005's evidence for G-collapse (all 290 sampled orbits collapsed) was a sampling artefact: designed seeds are needed. The v005 conjecture K3.6 was wrong.

## K8 — growth classification (T35)
The criterion d^2 | Y and g/gcd(g,d-1) | Y/d^2 is verified against occurrence integrality and brute force (1715 states, K8.2). Transition identity G(x') = gcd(g, new d-1) verified (K8.3). Witnesses (K8.5, exact, reproducible): preserving — G=2: 1170 -> 2349/2 adds 9; G=3: 1264/3 -> 1280/3 adds 16; G=4: 1225/4 -> 625/2 adds 25; G=5: 6912/5 -> 9216/5 adds 96; G=12: 2366 -> 28561/12 adds 169. Reducing — G=5: 2124/5 -> 432 (5 -> 1); G=6: 2303/6 -> 392 (6 -> 1); G=4: 1325/4 -> 675/2 (4 -> 2); G=12: 6253/6 -> 4225/4 (12 -> 4).

## K9 — arithmetic anatomy (T36)
A preserving event always introduces a fresh prime (-y a square mod q^2) or a carried prime power; it never merely rearranges the current fibre, and its new moduli are coprime to g and divisor-closed mod g. Of 116 new moduli in preserving events, 67 are carries, 49 fresh (K9.4). In P_g every event is a carry of the prime 2 (the forced doubling of s).

## K10 — persistent regimes
G=5: persistent regime found and proved. G=4 and G=12: no proof either way (K10.6 OPEN); longest natural survival 28 and 60 steps, followed by collapse.

## K11 — global collapse
Settled negatively for the statement as posed. New open problems (K11.3, K11.4): does every orbit end in the form x = s^2 t/g (t in {1,2,3})? which g occur beyond gcd(g,6)=1? The reviewer's alternative — 'a genuinely different infinite dynamical regime' — is what happened.

## Corrections to earlier statements
- v005 K3.6 (G-collapse conjecture) is refuted; v005 T34 and v006 L2 stay valid (they exclude only G=2,3,6).
- v006 L5's bound 'upper density <= 1/g' is not sharp in P_g: density 0, O(log X) (T40).
- v005 T33 non-universality holds in every known regime.

## Caveats
T38 is a proof schema plus finite hypotheses (H1)-(H3); T38a proves them for all g coprime to 6 using the existence of a prime q = 2 mod g (Dirichlet). The numerical rows are finite checks of identities whose general proofs are written out. Regimes for 2|g or 3|g are not classified.
