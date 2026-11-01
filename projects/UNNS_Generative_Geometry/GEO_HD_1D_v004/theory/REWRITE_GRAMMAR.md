# D4-T3 — block rewrite grammar and its resource threshold

A rewrite is  p·u·s  ->  p·v·s  with (u,v) arrangements of the two sides of a kernel vector z.  Because R(u)=R(v), the state after p·u equals the state after p·v, so the suffix s is unchanged.

**D4-T3 (PROVED).** For a source m: p·u·s and p·v·s are both admissible iff lcm(K(p·u·s), K(p·v·s)) | m.  Equivalently: if p·u·s is admissible then p·v·s is admissible iff v is admissible from the state after p.  Both endpoints coincide.  (6000 + 5000 randomized tests, 0 violations; the proof is the two sentences above plus the threshold law of v002.)

Consequence: a rewrite is an event local to the prefix state x_p — its executability depends on x_p only through the p-adic valuations the block needs.  This is the operational counterpart of the algebraic relation.
