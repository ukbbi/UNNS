# FIELD-I — conversation handoff

Project: `UNNS_ENTANGLE_I/FIELD-I`, release `FIELD1_v001.zip`.

Motivation: Original 2017 UNNS post fixes the nest `N` and varies modulus `M` in `S_N(M)=M(N+1)^2/N`. The October 2026 RGG manuscript treats integer anchors `M=kN`, value `k(N+1)^2`; field/non-anchor rational outputs were not analyzed. SELECT-II feeds integer outputs back into modulus and is a distinct, explicitly introduced self-iteration model, not the founding rule.

Goals: F1 full rational fibres; F2 intersections of whole rational fixed-nest sequences; F3 non-anchor multiplicities and restrictions; F4 leak-controlled observability; F5 binary-operation nonselection; F6 adversarial/reproducibility.

Principal theorem: For x=a/b reduced, positive integer occurrences correspond to d>=2 with d^2|a and d≡1 (mod b), with N=d-1, M=(a/d^2)((d-1)/b). Same nest `N` outputs `M*(N+1)^2/N`. Entire rational intersection of nests N1 and N2 consists of positive multiples of lcm(N1+1,N2+1)^2/gcd(N1,N2).

Status: arithmetic exact and proved; two-point successor chart is injective, but this is label leakage, not relational selection. Two distinct commutative/associative/idempotent binary operations are covariant under simultaneous fixed-nest successor and agree on same-nest pairs, demonstrating insufficiency of that constraint. No intrinsic binary operation or physical entanglement is derived.

Run `python field1.py` from project root (standard library). Tests and deterministic CSV/JSON reports included. `MANIFEST.json` records file SHA-256. Preserve everything from earlier RGG, SELECT-I/II, and the manuscript. Do not silently replace these constructions or claim canonical binary interactions.
