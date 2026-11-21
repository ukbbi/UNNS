# MUG-I v009 — Exact mathematical research record

Research notes, **not a manuscript**. Status labels: PROVED (within stated model), VERIFIED COMPUTATIONAL, OPEN. Original UNNS self-substitution law is not modified.

## Model and non-negotiable distinction

On the 2π-periodic line, consider the one-dimensional transverse Maxwell reduction in normalized units µ=1:

    ∂_t D = −∂_z B;       ∂_t B = −∂_z E;       D = ε(z,t) E.

Choose an *externally driven*, real, positive, time-dependent dielectric

    ε(z,t) = 1+2η [f_1(t) cos(q_1(z−t))+f_2(t) cos(q_2(z−t))],

where 0<η<1/4, q_1,q_2>0 integers, and nonoverlapping pulses

    f_1(t) = sin²(πt/T)          for 0<t<T, zero otherwise,
    f_2(t) = sin²(π(t−T)/T)      for T<t<2T, zero otherwise.

Thus ε≥1−4η>0. At t=0,T,2T the pump is off, so incoming and outgoing harmonic decompositions are *actual free-medium Maxwell eigenmode components*. During the pump, the field is a superposition and is **not** assumed to be a fixed-medium stationary eigenstate. A real Maxwell solution is the real part of the complex Fourier calculation. The external pump can exchange energy with the field; energy of the electromagnetic subsystem need not remain constant.

The pre-declared **UNNS** law on *individual positive integer modal indices* is

    T_N(m) = m (N+1)²/N,     N|m,   N≥1.

A Maxwell field scattered into mode m′ does **not** imply that the physical time evolution implemented the whole-field pullback D_N E(z)=E(r_N z). A matching mode-index edge is an *overlay/intersection* between two independently defined structures, not identity of their dynamical operators.

## T1 [PROVED] — Exact Maxwell Fourier congruence selection

Let d=gcd(q_j : nonzero pump harmonics). Since ε(z+2π/d,t)=ε(z,t), the Maxwell Cauchy evolution commutes with translation by 2π/d. Any initial field whose Fourier indices lie in one congruence class m₀ mod d remains in that class for all t, including all orders in η. This also follows directly by Fourier convolution by ε and ε⁻¹. Therefore:

* For the two-harmonic protocol (q₁,q₂)=(6,28), d=2. Starting at m=2, odd indices, including m=9, have **exact zero amplitude**.
* With q=6 alone, only indices 2 mod 6 are populated; 36 is forbidden since 36−2=34 is not divisible by 6.
* With q=28 alone, only indices 2 mod 28 are populated; 36 is forbidden since 34 is not divisible by 28.
* With the two pumps together, 36 is not forbidden by congruence because 34 is divisible by gcd(6,28)=2.

The congruence statement is a direct *Maxwell and material-symmetry* selection law, not a new consequence of UNNS.

## T2 [PROVED PERTURBATIVELY] — Nonzero two-pulse Maxwell mode coupling

Let the incoming field be one right-moving vacuum mode at integer m>0, initialized by D_m=B_m=1, other components zero. Let p=m+q₁ and s=m+q₁+q₂. Assume q₁+q₂ is not divisible by either q₁ or q₂ so neither single-pump spatial sublattice can reach s from m. Introduce free-mode outgoing variables a_k=(D_k+B_k)/2 and b_k=(D_k−B_k)/2 (for positive k). To first order, E=ε⁻¹D = D−2η[f₁ cos q₁(z−t)+f₂ cos q₂(z−t)]D+O(η²).

At the end of pulse one, in the free interaction frame:

    a_p^I = +i (pη/2) I₁ + O(η²),
    b_p^I = −i (pη/2) J₁ + O(η²),

where

    I₁=∫₀ᵀ f₁(t)dt,     J₁=∫₀ᵀ f₁(t)e^(−2ipt)dt.

The only order-η² spatial route into s after pulse two passes through index p. Accounting also for the intermediate *counterpropagating* mode b_p gives

    a_s^I = −η² (ps/4)(I₁ I₂−J₁ K₂)+O(η³),
    I₂=∫ᵀ²ᵀ f₂(t)dt,    K₂=∫ᵀ²ᵀ f₂(t)e^(+2ipt)dt.

For the stated sin² pulse, I₁=I₂=T/2>0. Since f_j is strictly positive on an interval and p>0, the strict triangle inequality implies |J₁|<I₁ and |K₂|<I₂. Hence I₁I₂−J₁K₂ ≠0. So the target mode s has **nonzero outgoing positive-frequency amplitude for all sufficiently small nonzero η**, in this idealized Maxwell model.

This is a *Maxwell-derived* prediction independent of the UNNS nesting graph. The more familiar resonant contribution, −η²(ps/4)I₁I₂, is a useful approximation, not the entire coefficient. Analytic finite-time perturbation theory for the smooth positive dielectric justifies the expansion; this is not a statement about arbitrary η or laboratory realization.

## T3 [PROVED] — Intersection with the two-step UNNS diamond

Exactly under the integer self-substitution law:

    A: 2 --T₁--> 8 --T₂--> 36;
    B: 2 --T₂--> 9 --T₁--> 36.

For the *same fixed two-harmonic q=6,28 pump protocol*, the Maxwell coupling has an order-η² route 2→8→36 (T2) and cannot populate m=9 at any order (T1). Thus the Maxwell mode-conversion graph intersects one UNNS index path but excludes the other **for this particular imposed dielectric**.

The pump harmonics 6 and 28 were intentionally engineered from the mode differences 8−2 and 36−8. This proves an exact *conditional induced-structure selection* in the toy model. It is **not** blind prediction of an unknown material, and it does not implement the full-field T_N map as time evolution.

Reversing temporal pulse order to q=28 first, q=6 second yields a non-UNNS positive mode route 2→30→36. These are *different externally imposed Maxwell protocols*, not two histories evolved by an identical, autonomous medium; their different amplitudes do not establish UNNS physical memory.

## T4 [PROVED] — Infinite Maxwell-accessible, UNNS-forbidden counterfamily

For **every integer m≥12**, the two-harmonic pump (6 then 28) has nonzero perturbative outgoing mode-conversion coefficient m→m+34 (T2), since the proof applies with p=m+6 and s=m+34. But

    (m+34)/m = 1+34/m <4,

whereas every nonempty forward UNNS history multiplies the input by at least 4, because r_N=N+2+1/N≥4. Thus **no positive-length UNNS nesting history connects m to m+34 for any m≥12**, although Maxwell excitation is allowed and has nonzero amplitude at sufficiently small η.

This is a mathematically exact infinite counterfamily to any claim that these Maxwell couplings select only UNNS histories. Three finite numerical examples (m=12,13,20) are recorded as additional illustrations, not part of the 13 locked predictions.

For the held-out m=4→38 control, the ratio 38/4=19/2<16 excludes depth≥2 and direct checks N|4 (N=1,2,4) exclude a one-step UNNS history. Yet the same Maxwell pumping process populates mode 38.

## T5 [PROVED] — Why v008's fixed-medium no-go does not apply to these driven interactions

The v008 no-go concerns direct coordinate dilation E(z)→E(rz) mapping a stationary eigenstate to another stationary eigenstate of **one fixed nonuniform medium**. Here ε(z,t) changes according to an independently prescribed pump. A generic intermediate field is not stationary; at t=0 and 2T the pump vanishes, and incoming/outgoing modes are defined with respect to the common vacuum reference. Therefore the setups are not logically contradictory.

## T6 [VERIFIED NUMERICAL] — Held-out computed Maxwell predictions and independent solver

The predictions were locked after a *disclosed pilot* at η=.012,T=2. Held-out parameters η=.009,T=1.7 were frozen in `protocol/PREDICTIONS_LOCK.json` (SHA-256 stored separately) **before their solver runs**. Six cases/13 inequality predictions all pass. Independent staggered-grid Yee finite differences reproduce three principal Fourier/RK4 results to better than 3.5% (typically much better); a resolution-doubling check changes principal amplitudes by less than 0.5%; exact analytic order-η² Maxwell coupling coefficients agree with finite-η amplitudes within 3% for all four two-pulse cases.

These are prospective **computational** checks, not blinded physical experiments or evidence of UNNS-specific advantage over standard Maxwell analysis.

## Research verdict

PROVED: T1–T5 under explicitly declared equations and assumptions. VERIFIED COMPUTATIONAL: T6, including exact lock check, finite-difference independent solver, and Born coefficient comparisons. OPEN: whether independent empirical material data reveal useful UNNS-specific discrimination beyond the Maxwell/Fourier baseline; whether any physical device implements the whole-field T_N operator; general vector dispersive Maxwell; experimental confirmation.

The strongest demonstrated finding is a **conditional Maxwell-selection geometry on top of the UNNS nesting graph**, accompanied by a rigorous infinite counterfamily proving that Maxwell coupling is not in general restricted to UNNS-admissible index routes.
