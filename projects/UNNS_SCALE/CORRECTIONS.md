# Corrections, scope and superseded claims

The research releases are frozen historical records. Corrections are recorded in later releases, not silently applied to old files. **Consult these notes before citing earlier theorems.**

1. **v005 preliminary seed:** The excluded `v005 seed` folder predates the finished theorem and contained an incorrect preliminary count of 999,385 direct-identity cases. The verified v005 partition is **999,384 direct-identity pairs + n=1 separately + 614 certificate paths = 999,999**.
2. **v007 constant-ratio obstruction:** The claim that no finite collection of constant-ratio shapes covers all positive `n` was overbroad, because the shapes originally required `ρ>1` and omitted legitimate `0<ρ<1` shapes. The lcm obstruction only applies in its restricted `P>1` setting. See [v008 erratum](releases/UNNS-SCALE-I_v008/ERRATUM_v007.md).
3. **v008 shape / converse:** Both congruences are required for a valid constant-ratio route. The converse of the v008 integer-coordinate Theorem L′ also requires `B | Q²aN`. See [v009 erratum](releases/UNNS-SCALE-I_v009/ERRATUM_v008.md).
4. **v011 sample hub routes:** The existence proof used long paths through vertex 1, but v012 found much shorter confined routes; vertex 1 is not established as a necessary or optimal hub.
5. **v013 parity condition:** The correct necessary obstruction compares `v_r(B)` and `v_r(p+1)` modulo 2, not solely prime factors of `p+1`. The quoted finite maxima for `T(100)`, `T(1000)` are *sample maxima*, not infinite suprema. See [v014 theory §4](releases/UNNS-SCALE-I_v014/THEORY/UNNS_SCALE_I_THEORY_v014.md).
6. **v013 scale-4 bound:** The proposed universal `τ⁴≤6` within the large ceiling is false for 8,655 of the 999,999 pairs. v014 obtains a uniform confined bound of 18 by allowing alternative scale-transfer constructions.

## Essential scope

- `M_{10⁶}=4` is a **finite ambient** theorem for `1≤n<10⁶`; the universal `D_{10⁶}` remains `{4,5,6}`.
- The v010 forced excursions hold for routes **of at most four edges** inside the fixed trillion window. Longer endpoint-confined connections exist by v011.
- The prime-parity theorem supplies a separate infinite family of height barriers regardless of path length.
- Neither shorter graph paths nor smaller scale labels imply faster computation; Gate 4 has not been run.
- Nothing here is a demonstrated physical spacetime wormhole; the phrase *Arithmetic Wormhole Geometry* refers to a property of arithmetic graph routing.
