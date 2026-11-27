import collections
REGIONS = collections.OrderedDict([
 ('A', 'Generation: recurrences, composition and factorization'), ('B', 'Convergence and growth in depth'),
 ('C', 'The critical exponent'), ('D', 'Counting, equidistribution and typical histories'),
 ('E', 'Fixed depth: continuation and counting'), ('F', 'Depth two'), ('G', 'Depth three'),
 ('H', 'Arbitrary depth at one third'), ('I', 'Collective growth at and below s = 1'),
 ('J', 'Extended generation: torsion multipliers'), ('K', 'Negative drift: entropy and attainment')])
REVIEW = {'V': 'UNNS Research Collective review: valid', 'VQ': 'UNNS Research Collective review: valid, with a recorded qualification',
 'A': 'Reciprocal review: proposal checked internally; no UNNS Research Collective verdict recorded', 'P': 'No review verdict recorded',
 'B': 'Baseline note, not separately reviewed', 'N': 'Not a proved result'}
AUDIT_IDS = ['T%02d' % i for i in range(1, 16)] + ['T16', 'T17', 'T18', 'T19', 'T20', 'T21', 'T23a', 'T28a']
V003_IDS = ['T49', 'T50', 'T48a', 'T48b', 'ANS2N-T12a', 'ANS2N-T12', 'ANS2N-C12', 'ANS2N-T13', 'ANS2N-T14', 'ANS2N-T15']
QUAL = {
 'T50': 'Fixed real tau as k tends to infinity; no uniform statement for tau = tau(k).',
 'T48b': 'The bounding constants satisfy 0 < c_- <= c_+ < infinity.',
 'ANS2N-C12': 'Valid under its hypotheses.',
 'ANS2N-T14': 'Proof-writing clarification: in the final Fatou step use a limit superior for the drift difference, or a further convergent subsequence. The theorem is unaffected; the release file is not edited.',
 'T01': 'Absolute-convergence region as stated.', 'T02': 'Exact depth-resolved Moebius inversion.',
 'T04': 'Prime-coordinate recurrence and maximum formula.', 'T06': 'Ordinary Euler-product obstruction.', 'T07': 'A sufficient convergence criterion.',
 'T08': 'Unit-denominator grammar.', 'T11': 'The saturation criterion only; the general classification remains open.',
 'T13': 'Uses the classical Delange theorem.', 'T14': 'The stated convergence regions; not a complete classification for negative source weights.',
 'T28a': 'Preventing harmful first introductions does not prevent depletion of primes met earlier, so this does not settle T28.',
 'T27': 'Valid for the infimal Gevrey order; membership at exactly that order is open.',
 'T32': 'Valid after a correction to the limiting step, which has been applied.',
 'T46h-i': 'A normal-convergence clarification was requested and added in ANS-I v013.',
 'T46j': 'Two scope clarifications were requested and made in ANS-I v013.',
 'ANS2-T04': 'Valid for the infimal Gevrey order.', 'ANS2-T07': 'Valid with the precise event definition, now in the text.',
 'ANS2-T15': 'Bounded only when the norm is finite (in the text).', 'ANS2N-T03': 'Convergence valid; attainment is open.',
 'ANS2N-T06': 'Method valid and stored result reviewed; no independent rerun.',
 'ANS2N-T07': 'Valid; its hypothesis is superseded by ANS2N-T10.', 'ANS2N-T09': 'Valid; a proof clarification is recorded in ANS-II-ND v003.',
 'T46b': 'k = 2, 3 proved and reviewed (T45, T46k); k >= 4 conjecture.'}
RELATIONS = [('T09','T07','extends'), ('T23a','T23','sharpens'), ('T24a','T24','sharpens'), ('T24b','T24a','gives a second proof of one inequality of'),
 ('T23','T19','quantifies'), ('T24','T21','quantifies'), ('T22','T20','strengthens'), ('T37','T37a','strengthens'),
 ('T34a','T32','refines'), ('T45','T05','continues further than'), ('T45a','T45','extends'), ('T34b','T34','completes the exactness of'),
 ('T38d','T38a','generalizes'), ('T38d','T38b','generalizes'), ('T46k-i','T46k','widens the margin of'),
 ('T46e','T46e-i','discharges the hypothesis of'), ('T48a','T48','sharpens the upper constant of'),
 ('T49','T48','raises the lower constant of'), ('T50','T48','extends to a window the setting of'), ('ANS2-T16','ANS2-T05','gives the exact value bounded in'),
 ('ANS2-T16','ANS2-T02','treats the abscissa for any drift signs, beyond'), ('ANS2N-T06','ANS2-C16','certifies'),
 ('ANS2N-T10','ANS2N-T07','supersedes the hypothesis of'), ('ANS2N-T14','ANS2N-T10','contains, by a second argument, part of')]
NOTES = {'T46h': "Consolidation note: the releases record the factorisation behind this result as the UNNS Research Collective's and declare it valid without writing out a derivation. A derivation is in `PROVENANCE/AUDIT_v001.md`, section 5; the foundational audit of 27 November 2026 accepted it.",
 'ANS2-C16': 'Floating-point evaluation. The interval is certified by ANS2N-T06.', 'T46c': 'A model series, not the depth-three function.',
 'T46f': 'A model series, not the depth-three function.', 'T46o': 'A model series, not G_k.',
 'T46p': 'An implication; its hypotheses are not established for any k >= 4.',
 'T45d': 'Corollary 2 (the non-real poles) assumes the Riemann hypothesis; the theorem itself does not.',
 'AS-001': 'Elementary baseline deduction; classical in content.', 'AS-002': 'Elementary baseline deduction; classical in content.'}
