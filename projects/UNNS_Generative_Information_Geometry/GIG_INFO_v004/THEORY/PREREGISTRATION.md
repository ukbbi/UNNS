# GIG-INFO v004 — pre-registration for the symbolic-transfer extension SYM-6 (written BEFORE any SYM-6 system was generated)
Already generated and therefore NOT part of this registration: SYM-3 (512 rule sets, categories S,S,S,R,R,N) and SYM-28 (all 28 size-6 category multisets over {S,R,N}). Result known at registration time: no system in SYM-3 or SYM-28 has beta2>0, so the primary beta2 target is untestable there.
SYM-6: six distinguishable symbols (each event its own category); a rule set is an arbitrary directed graph (transition relation) on the six symbols; histories = Hamiltonian orderings (admissible iff every consecutive transition is an arc). 60,000 digraphs drawn with numpy default_rng(20261111), each arc present independently with probability p, p drawn uniformly from {0.45,0.55,0.65,0.75,0.85}; distinct non-empty admissible arrangement masks kept.
Predictions transferred from the arithmetic census (not tuned on SYM-6):
 T1. (Q,S2), (N,SB22) and (N,h1,h2) have zero mixed classes for Y2=1[beta2>0] in SYM-6 provided SYM-6 contains >=50 positive systems; otherwise T1 is untestable.
 T2. (N,h1) leaves at least one positive in a mixed class (radius 1 insufficient).
 T3. (N) alone leaves every positive in a mixed class.
A prediction is FALSIFIED by any contrary class. Outcomes are reported whatever they are.
