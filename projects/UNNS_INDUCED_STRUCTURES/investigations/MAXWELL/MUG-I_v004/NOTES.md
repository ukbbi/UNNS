# MUG-I v004 — Dispersion-resolved nesting (research note)

Status: research release. Suite `verification/verify_v004.py` (4 checks, all pass, standard library). Units c = 1.
Two operations are kept separate throughout:
- Operation A (index nesting): n -> r_N n (N | n), then assign the on-shell eigenfrequency of the medium to the new index.
- Operation B (spacetime dilation): (k, w) -> (alpha k, alpha w).
Vacuum: A and B coincide (control). In a dispersive medium B is a field map only if w(alpha k) = alpha w(k); A is always defined (the new index has its own eigenmode). The question is how A relates to B.

## 1. Scope corrections to v003 (applied to the v003 notes)
- Content ratios are not cell-independent. Two waves with indices (1,0,0) and (0,1,0) on a cubic cell have contents 1 and 1; on a cell doubled only in x their indices are (2,0,0) and (0,1,0), contents 2 and 1. Index-space shape is invariant under change of basis of one lattice and under isotropic cell multiples only. What is cell-independent is the physical wavevectors (and hence ratios of |k|), polarisation and commensurability class. (Y1)
- Whole-field versus component. The content of a multimode field is the gcd of all its indices; each Fourier component has its own content. A field with harmonics 1 and 2 has whole-field content 1, while its second harmonic has content 2, so T_2 is admissible on that component but not on the field. v001's gcd statement and v003's translation-stabiliser statement are whole-field; componentwise nesting is a different (weaker) operation.
- v003 §2.3 is restated in the two-operation form above. It does not claim that no T_N is admissible in a dispersive medium: operation A is always available; what fails is B.

## 2. The cold plasma (Drude) identity — exact
For w^2 = k^2 + wp^2:  w(alpha k)^2 − alpha^2 w(k)^2 = (1 − alpha^2) wp^2,   independent of k.
Verified exactly on 2000 rational cases; vacuum (wp = 0) gives 0. (Y2)
Example T_2(2) = 9, wp = 1: w_2^2 = 5, w_9^2 = 82, both on-shell. Dilation would require w_9 = (9/2) w_2, i.e. w_9^2 = 101.25; the actual value is 82, defect −77/4 = (1 − 81/4) wp^2. So the nested pair (2, 9) is a valid correspondence of Maxwell modes while the scale relation fails by an amount fixed by alpha alone.
Consequence: for this medium the defect depends on the UNNS step only through r_N, not on the mode. It is not UNNS-specific (any alpha gives the same form).

## 3. Histories add no field-level structure in linear media
Let Phi(k) = w(k)^2 and Delta(alpha; k) = Phi(alpha k) − alpha^2 Phi(k). Then exactly
  Delta(beta alpha; k) = Delta(beta; alpha k) + beta^2 Delta(alpha; k),
the coboundary of Phi. Hence the final on-shell mode and the total defect depend only on the endpoint index (equivalently on the product of multipliers), for any linear time-invariant medium whose eigenfrequency is a function of (index, branch, polarisation). Verified exactly for the plasma (500 cases) and numerically for the Lorentz medium (60 cases). (Y3)
The stepwise defects DO depend on the order: for n = 3 with steps (N=1 then N=3) the stepwise defects are (−15, −247/9); with (N=3 then N=1) they are (−247/9, −15); the weighted totals agree: −4087/9 = 1 − (64/3)^2.
Reading: different UNNS histories reaching the same mode give the same electromagnetic field and the same total defect; the history survives only as the sequence of stepwise defects, which is bookkeeping of the path through intermediate modes. A genuine history-dependent field structure would need memory (nonlinearity, hysteresis, time-dependent media), not studied.

## 4. Polarisation enters through gyrotropy
Magnetised cold plasma, parallel propagation (wp = 1, Omega_c = 1, upper branches): the R and L circular waves have different dispersion, so index nesting produces different defects for the same indices:
(N,n) = (1,1): R −34.64, L −8.08; (1,3): −22.08, −11.20; (2,2): −33.68, −12.95; (2,6): −23.18, −16.42; (3,3): −40.12, −20.61; (3,9): −30.95, −24.63.
The R-branch defect for N = 1 varies with n (−34.64, −26.36, −22.08, −19.99 for n = 1..4). Limits behave as required: Omega_c → 0 gives the plasma value (1 − alpha^2) wp^2 for both branches; wp → 0 gives 0. (Y4)
So in a gyrotropic medium the nesting correspondence distinguishes configurations with the same index and different polarisation, and the defect depends on both the index and the polarisation branch. This is the first place where Maxwell's vector structure enters the induced construction, and it enters through the constitutive relation, as predicted by the symmetry argument of v003.

## 5. Where this leaves the UNNS contribution
- Arithmetic nesting (UNNS): which index pairs (n, r_N n) are related, the history graph.
- Solution correspondence (Maxwell + medium): operation A, always defined; the on-shell field at the endpoint.
- Dynamical symmetry: operation B, defined only when the defect vanishes.
The defect is a measurable property of the medium and of the chosen index pair; it is not produced by UNNS (any pair of integer indices has one). UNNS supplies the pairs and their history structure. No finding yet shows that the UNNS pairs are preferred by a physical process.

## 6. Limits and next
- Y4 uses numerically solved upper branches; only parallel propagation and cold plasma.
- No amplitude rule is proposed for operation A; the field-level relation is stated at the level of eigenfrequency, E–B ratio, polarisation branch. E–B amplitude ratio B/E = k/w could be tabulated along nesting (not done).
- Next candidates: (i) B/E, phase and group velocity along nesting edges in plasma and gyrotropic media; (ii) fixed resonators with walls plus dispersion (rectangular waveguide TE/TM branches with cutoffs); (iii) memory media for history-dependence; (iv) comparison with FUG-I v005 merger structure on the nesting graph, where this note predicts no extra field-level content for linear media.
