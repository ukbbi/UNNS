hashes = []
for a in ['B'] + list(REL):
    src = srcpath(a); dst = COL / 'PROOFS' / copyname(a); dst.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(src, dst)
    assert sha(src) == sha(dst); hashes.append((copyname(a), src.relative_to(W).as_posix(), sha(src)))
    if a != 'B':
        t = src.parent / 'THEOREMS.md'; d2 = dst.parent / 'THEOREMS.md'; shutil.copyfile(t, d2)
        hashes.append((copyname(a).replace('PROOFS', 'THEOREMS'), t.relative_to(W).as_posix(), sha(t)))
records = json.loads((HERE / 'archive_records.json').read_text(encoding='utf-8'))
matches = []
for a in REL:
    m = records['proof_matches'].get(REL[a] + '/PROOFS.md|' + sha(srcpath(a))); assert m, ('no archive match', a)
    own = [z for z in m if ('_' + REL[a].replace('/', '_') + '_') in z or z.endswith(REL[a].replace('/', '_') + '.zip')]
    matches.append((copyname(a), (own or m)[0], len(m)))
shutil.copyfile(W / '07_REFERENCES/SOURCES.md', COL / 'PROOFS/CLASSICAL_SOURCES.md')
put('PROOFS/README.md', '# Proof sources\n\nEach proof file is byte-identical to a file inside at least one release archive (table below). The archives are kept outside this repository.\n\nVerbatim copies of the release proof files and release tables. The originals under `02_INVESTIGATIONS` are the record; these copies were byte-identical to them when the collection was built. In the release tables of this edition, attribution wording is standardised; the archive match concerns the proof files. Line numbers in the compendium refer to these files. Each entry lists the classical inputs it uses. `CLASSICAL_SOURCES.md` is a copy of the workspace source list, which records external sources and how they were used.\n\n| copy | original | SHA-256 |\n|--|--|--|\n' + '\n'.join(f'| `{a}` | `{b}` | `{c}` |' for a, b, c in hashes) + '\n\n## Match with release archives\n\n| copy | an archive containing the identical file | archives containing it |\n|--|--|--|\n' + '\n'.join(f'| `{a}` | `{b}` | {c} |' for a, b, c in matches))

def where(e): return f"{e['release']}, lines {', '.join(f'{a}-{b}' for a, b in e['lines'])}"
def table(es):
    return '| ID | Result | Status | Review | Proof source |\n|----------|------------------------|----------|----|----------------|\n' + '\n'.join(
        f"| {e['id']} | {e['title']} | {e['status']} | {e['review_code']} | {where(e)} |" for e in es)
idx = ['# Theorem index', '', f'{len(E)} catalogued entries, grouped by mathematical phenomenon. Original identifiers are kept. Open questions are in `OPEN_PROBLEMS/`.', '',
       'Review codes: ' + '; '.join(f'**{k}** = {v}' for k, v in REVIEW.items()) + '.', '']
for k, v in REGIONS.items(): idx += [f'## {k}. {v}', '', table([e for e in E if e['region'] == k]), '']
put('THEOREM_INDEX.md', '\n'.join(idx))

DEFS = (HERE / 'definitions.md').read_text(encoding='utf-8')
def settings(a, s, e): return relabel('\n'.join(x for x in srcpath(a).read_text(encoding='utf-8').split('\n')[s-1:e] if not x.startswith('#')).strip())
def entry(e):
    o = [f"## {e['id']}: {e['title']}", '', f"**Proof status:** {e['status']}. **Review:** {e['review']}." + (f" {e['qualification']}" if e['qualification'] else ''), '',
         f"**Review record:** {e['review_record']}. **Release and computation:** {e['acceptance']}.", '',
         f"**Source:** {where(e)}. **Scope:** {e['scope']}. **Literature priority:** {e['literature_priority']}.", '']
    if e['release_summary']: o += [f"**Release table summary** ({e['release_summary_from'].replace('_', '-')}): {e['release_summary']}", '']
    o += ['**Statement as recorded:**', '', e['statement'], '']
    o += [f"**Depends on:** {', '.join(e['depends_on']) or 'no earlier result cited'}." + (f" **Used by:** {', '.join(e['used_by'])}." if e['used_by'] else '') + (f" **Classical inputs:** {e['classical_inputs']}." if e['classical_inputs'] else ''), '']
    if e['related']: o += ['**Relations:** ' + '; '.join(e['related']) + '.', '']
    if e['unreviewed_ancestors']: o += [f"**Rests on results without a review verdict:** {', '.join(e['unreviewed_ancestors'])}.", '']
    if e['note']: o += [e['note'], '']
    return '\n'.join(o)
comp = ['---', 'title: "ASUNNS Theorem Compendium, v003"', 'author: "UNNS Research Collective"', 'date: "27 November 2026"', '---', '',
 'Results of Analytic Structures of the UNNS Substrate through ANS-I v015, ANS-II v002 and ANS-II-ND v003. Statements are copied by program from the proof files; the proofs stay in those files. In this edition, review attribution inside quoted statements reads UNNS Research Collective. A statement may refer to a numbered display or section of its source. Three statuses are kept apart: proof status (PROVED means that a written argument exists in the releases), mathematical review, and release or computational acceptance. No literature novelty review of these results has been completed. Entries with status CONJECTURE are not theorems.', '',
 '# Standing definitions', '', DEFS, '']
for k, v in REGIONS.items():
    comp += [f'# {k}. {v}', '']
    if k == 'J': comp += ['**Setting (ANS-II v001).**', '', settings('II1', 6, 15), '']
    if k == 'K': comp += ['**Setting (ANS-II-ND v001).**', '', settings('N1', 6, 13), '']
    comp += [entry(e) for e in E if e['region'] == k]
put('THEOREMS/COMPENDIUM.md', '\n'.join(comp))
put('THEOREMS/compendium.json', json.dumps(dict(collection='ASUNNS reference collection v003', date='2026-11-27', regions=REGIONS, review_codes=REVIEW, entries=E, open_questions=opens), indent=1, ensure_ascii=False))

edges = [dict(result=e['id'], uses=d) for e in E for d in e['depends_on']]
put('DEPENDENCIES.json', json.dumps(dict(meaning='An edge records that the written proof or statement of the first result cites the second, by identifier, release section or named lemma. Edges were recorded by hand from a reading of the citations. Uses that are not cited are absent, so the graph is a lower bound on logical dependence.',
    nodes=[dict(id=e['id'], region=e['region'], status=e['status'], review=e['review_code'], classical_inputs=e['classical_inputs']) for e in E], edges=edges, relations=[dict(source=full(a), target=full(b), kind=k) for a, b, k in RELATIONS]), indent=1))
cross = collections.Counter((byid[x['result']]['region'], byid[x['uses']]['region']) for x in edges if byid[x['result']]['region'] != byid[x['uses']]['region'])
top = sorted(ids, key=lambda i: (-len(down[i]), i))[:12]
anc = collections.Counter(d for v in exposed.values() for d in v)
mer = ['```mermaid', 'flowchart LR'] + [f'  {k}["{k}. {v}"]' for k, v in REGIONS.items()] + [f'  {b} -->|{n}| {a}' for (a, b), n in sorted(cross.items())] + ['```']
dm = ['# Dependency architecture', '', f'{len(E)} nodes and {len(edges)} edges, recorded from explicit citations (exact meaning in `DEPENDENCIES.json`). The graph is a lower bound: an uncited use does not appear.', '',
 '## Most relied-upon results', '', '| Result | Title | Direct uses | All results resting on it | Review |', '|--|--|--|--|--|'] + [f"| {i} | {byid[i]['title']} | {len(used.get(i, []))} | {len(down[i])} | {byid[i]['review_code']} |" for i in top] + [
 '', '## Reviewed results resting on results without a review verdict', '', f'{len(exposed)} of {len(reviewed)} reviewed results have such an ancestor in the recorded graph. In v001, before the foundational audit, the count was 63 of 91. The graph records cited uses only.'] + ([] if not anc else ['', '| Ancestor without a verdict | Review code | Reviewed results above it |', '|--|--|--|']) + [
 f"| {d} | {byid[d]['review_code']} | {n} |" for d, n in sorted(anc.items(), key=lambda x: (-x[1], x[0]))] + [
 '', '## Links between regions', '', 'An arrow from X to Y means that results in region Y cite results in region X; the label counts the citations.', ''] + mer + [
 '', '## Entries citing no earlier result', '', ', '.join(i for i in ids if not byid[i]['depends_on']) + '.']
put('DEPENDENCIES.md', '\n'.join(dm))

op = ['# Open problems and conjectures', '', 'Recorded for preservation. Sequential ANS-I development is paused at v015.', '', '## Conjectures', '']
for e in E:
    if cat(e) == 'conjecture': op += [f"### {e['id']}: {e['title']}", '', f"**Status:** {e['status']}. Source: {e['release']}.", '', e['statement'], '']
op += ['## Open questions', '']
for k, v in REGIONS.items():
    o = [x for x in opens if x['region'] == k]
    if o: op += [f'### {k}. {v}', '', '| ID | Question |', '|----------|----------------------------------------|'] + [f"| {x['id']} | {x['text'].replace('|', chr(92) + '|')} |" for x in o] + ['']
op += ['## Where attempts stopped (recorded in the releases)', '', '- Depth four: no viable analytical route was found (ANS-I v014, section 4).', '- Growth at s = 1: a necessary condition, and an unproved heuristic against the upper constant e^gamma (ANS-I v015, section 5).', '- Attainment: reduced to weights at least 1/2 at depleting primes (ANS-II-ND v002 and v003).', '',
 'The earlier list `01_THEORY/OPEN.md` is the historical record; parts of it are superseded.']
put('OPEN_PROBLEMS/OPEN_PROBLEMS.md', '\n'.join(op))

base = ['# Frozen releases', '', 'Hashes taken when the collection was built. The collection does not replace these files.', '', '## Release archives (kept outside this repository)', '', '| file | bytes | SHA-256 |', '|--|--|--|']
for name, size, digest in records['releases']: base.append(f'| `{name}` | {size} | `{digest}` |')
base += ['', 'ANS-I v001 is not yet frozen: its Windows run is pending. ANS-I v004 has no archive of its own.', '', '`INVESTIGATION_FILES.sha256` lists every file under `02_INVESTIGATIONS`, relative to the project root, as published here.']
put('BASELINES/RELEASES.md', '\n'.join(base))
put('BASELINES/INVESTIGATION_FILES.sha256', '\n'.join(f"{sha(p)}  {p.relative_to(W).as_posix()}" for p in sorted(INV.rglob('*')) if p.is_file() and '__pycache__' not in p.parts))
comps = ['# Computational records', '', 'Finite computations support or test statements; they are not proofs, apart from the certified computation ANS2N-T06, whose conditions are stated with it. Run instructions are in the release READMEs.', '', '| release | programs | result files |', '|--|--|--|']
for t in tables:
    d = INV / t; pr = sorted(p.name for p in d.iterdir() if p.suffix in ('.py', '.c'))
    n = sum(p.is_file() for p in (d / 'results').rglob('*')) if (d / 'results').exists() else 0
    comps.append(f"| `{t}` | {', '.join(pr) or 'none'} | {n} |")
put('BASELINES/COMPUTATIONS.md', '\n'.join(comps))

rv = ['# Review status', '', 'Generated from the catalogue. The release tables copied under `PROOFS/` are the underlying records.', '']
for k, v in REVIEW.items():
    m = [e for e in E if e['review_code'] == k]
    if m: rv += [f'## {k}: {v} ({len(m)})', '', ', '.join(e['id'] for e in m) + '.', '']
rv += ['## Recorded qualifications', '', '| ID | Qualification |', '|--|--|'] + [f"| {e['id']} | {e['qualification']} |" for e in E if e['qualification']]
put('PROVENANCE/REVIEW_STATUS.md', '\n'.join(rv))
known = set(ids) | {x['id'] for x in opens}
stats = dict(entries=len(E), categories=dict(count), open_questions=len(opens), edges=len(edges), reviewed=len(reviewed), reviewed_with_unreviewed_ancestor=len(exposed),
    register_rows=len(reg), register_not_covered=sorted(set(reg) - known), covered_not_in_register=sorted(known - set(reg)), table_ids_not_covered=sorted(set(rows) - known),
    register_differs={i: [reg[i]['evidence'], byid[i]['status']] for i in ids if i in reg and byid[i]['status'].split()[0] != reg[i]['evidence'].split()[0]},
    by_category={c: [e['id'] for e in E if cat(e) == c] for c in count}, top=[(i, len(down[i])) for i in top], ancestors=anc.most_common())
put('PROVENANCE/build/stats.json', json.dumps(stats, indent=1))
print(json.dumps({k: v for k, v in stats.items() if k != 'by_category'}))
print({k: len(v) for k, v in stats['by_category'].items()}); print({k: v for k, v in stats['by_category'].items() if k != 'reviewed'})

exec((HERE / 'build_atlas.py').read_text(encoding='utf-8'), globals())
