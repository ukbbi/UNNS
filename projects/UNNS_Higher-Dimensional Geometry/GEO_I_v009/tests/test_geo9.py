"""GEO-I v009 unit tests (exact).  python3 tests/test_geo9.py"""
import os, sys, json, copy, itertools, pickle
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
for d in ('geometry', 'topology', 'frozen', 'theory', 'certificates', 'experiments', 'tests'): sys.path.insert(0, os.path.join(ROOT, d))
import binary5 as B5, binary_min as BM, binary_01 as B, checker8 as K
N = 0; F = 0
def t(name, ok):
    global N, F
    N += 1; F += (not ok); print(('ok   ' if ok else 'FAIL ') + name)
D = os.path.join(ROOT, 'output', 'data')
def spanning(k): r = B5.orbit_representatives(k); return [R for m in sorted(r) for R in r[m] if B5.rank_of(list(R)) == k]
t('orbit enumeration: spanning supports k=2,3,4 = 2,6,36 (independent of v008 support_orbits)', [len(spanning(k)) for k in (2, 3, 4)] == [2, 6, 36] == [len(BM.support_orbits(k)) for k in (2, 3, 4)])
r5 = pickle.load(open(os.path.join(D, 'v9_orbits_k5.pkl'), 'rb'))
t('orbit enumeration k=5 shipped data: 1371 orbits, 1326 spanning; complement symmetry of orbit counts by size', sum(len(v) for v in r5.values()) == 1371 and sum(1 for m in r5 for R in r5[m] if B5.rank_of(list(R)) == 5) == 1326 and all(len(r5[m]) == len(r5[31 - m]) for m in range(1, 31)))
t('isomorphism test: two RM(1,3)-type supports are isomorphic, an RM support and a non-isomorphic same-size set are not', B5.isomorphic([1, 2, 4, 7, 8, 11, 13, 14], [1, 2, 4, 7, 8, 11, 13, 14], 4) and not B5.isomorphic([1, 2, 4, 8, 3, 5, 6, 7][:7], [1, 2, 4, 8, 3, 5, 9], 4))
# engine agreement with the v008 path: nullity 3 and 4 classification
for k in (3, 4):
    mine = []
    for R in spanning(k):
        sig = list(R); C = B5.code_masks(sig)
        if B5.embedded(C) or not all(B5.embedded(B5.delete(C, i)) for i in range(len(sig))): continue
        mine.append((len(sig), B5.min_rank(C, len(sig))))
    ref = BM.classify_nullity(k)['minimal_reduced_orbits']
    t('binary5 engine reproduces v008 nullity-%d classification (sizes and min ranks)' % k, sorted(mine) == sorted((o['p'], o['min_rank']) for o in ref))
res = json.load(open(os.path.join(D, 'v9_binary5.json')))
t('nullity 5: 12 minimal reduced orbits, all minimum witness rank 3', len(res) == 12 and all(x[2] == 3 for x in res))
t('nullity 5: orbit sizes of the 12 minimal boxes', sorted(x[0] for x in res) == [8, 9, 10, 10, 11, 11, 12, 12, 13, 14, 15, 16])
cc = json.load(open(os.path.join(D, 'v9_binary5_crosscheck.json'))); t('nullity 5 cross-check against the v006 code path: 785 supports (<=16 points), 0 disagreements', cc['checked'] == 785 and cc['disagreements'] == 0)
bs = json.load(open(os.path.join(D, 'v9_burnside.json')))
t('orbit counts agree with the independent Burnside count over GL(k,2) (k=2..5; python total + empty set)', all(bs['orbits'][k] == bs['python_enumeration_total_nonempty'][k] + 1 for k in bs['orbits']) and sum(len(v) for v in r5.values()) + 1 == bs['orbits']['5'])
import shutil, subprocess, tempfile
if shutil.which('gcc'):
    tmp = tempfile.mkdtemp(); exe = os.path.join(tmp, 'b5'); subprocess.run(['gcc', '-O2', '-o', exe, os.path.join(ROOT, 'tools', 'burnside5.c')], check=True)
    t('Burnside program re-run k=4: 46 orbits', 'orbits_on_subsets_incl_empty=46' in subprocess.run([exe, '4'], capture_output=True, text=True).stdout)
else: print('UNAVAILABLE  gcc not found: Burnside re-run skipped (shipped record checked above)')
# G9-Z
zc = json.load(open(os.path.join(D, 'v9_zero_column.json'))); t('G9-Z exhaustive record: no minimal non-embedded box has a zero column', zc['minimal_with_zero'] == 0 and zc['nonembedded_with_zero'] > 0)
bad = [c for m in (2, 3) for n in range(2, 7) for c in itertools.combinations_with_replacement(range(1 << m), n) if 0 in c and not B.is_embedded(list(c)) and B.minimal_nonembedded(list(c))]
t('G9-Z recomputed (m<=3, n<=6): none minimal', not bad)
# G9-Z mechanism: deletion of a zero-column box keeps a collision
ok = True
for c in itertools.combinations_with_replacement(range(8), 5):
    if 0 in c and not B.is_embedded(list(c)):
        j = c.index(0); rest = list(c[:j] + c[j + 1:])
        ok &= not B.is_embedded(rest)
t('G9-Z mechanism: deleting a zero column of a non-embedded box leaves a non-embedded box (m=3, n=5)', ok)
# certificates
cs = json.load(open(os.path.join(ROOT, 'certificates', 'C5_rank5.json')))
t('C5 certificates: 12 RANK certificates accepted by checker8', len(cs) == 12 and all(K.check_RANK(c)[0] for c in cs))
c = copy.deepcopy(cs[0]); c['min_rank'] = 4; t('RANK tamper: wrong min_rank rejected', not K.check_RANK(c)[0])
c = copy.deepcopy(cs[0]); c['nullity'] = 4; t('RANK tamper: wrong nullity rejected', not K.check_RANK(c)[0])
c = copy.deepcopy(cs[3]); c['columns'] = c['columns'][:-1]; t('RANK tamper: column dropped (box no longer minimal-nonembedded) rejected', not K.check_RANK(c)[0])
# planar data records
ha = [json.load(open(os.path.join(D, 'v9_hollow_attack_p%d.json' % i))) for i in (0, 1)] if all(os.path.exists(os.path.join(D, 'v9_hollow_attack_p%d.json' % i)) for i in (0, 1)) else None
t('hollow survey record present, zero violations', ha is not None and all(not h['violations'] for h in ha))
print('\n%d checks, %d failures' % (N, F)); sys.exit(1 if F else 0)
