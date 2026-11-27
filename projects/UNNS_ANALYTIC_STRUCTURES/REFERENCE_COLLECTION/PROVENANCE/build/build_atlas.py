# loaded at the end of build_out.py: assembles the Atlas from atlas/*.md and the catalogue
AD = HERE / 'atlas'
atl = {}
for f in sorted(AD.glob('ATL-*.md')):
    head, body = f.read_text(encoding='utf-8').split('\n---\n', 1)
    meta = dict((l.split(':', 1)[0], l.split(':', 1)[1].strip()) for l in head.split('\n'))
    atl[f.stem] = dict(title=meta['title'].strip('"'), principal=[full(x) for x in meta['principal'].split()],
        entries=[full(x) for x in meta['entries'].split()], open=meta.get('open', '').split(), body=body.strip())
home = {}
for k, a in atl.items():
    for i in a['entries']:
        assert i in byid and i not in home, ('atlas assignment', k, i); home[i] = k
    assert set(a['principal']) <= set(a['entries']), (k, set(a['principal']) - set(a['entries']))
assert set(home) == set(ids), ('not in atlas', sorted(set(ids) - set(home)))
opn = {x['id']: x['text'] for x in opens}
assert set(opn) <= {o for a in atl.values() for o in a['open']}, ('open question not placed', sorted(set(opn) - {o for a in atl.values() for o in a['open']}))
known_ids = set(ids) | set(opn)
def mention_ok(a, tok):
    return any(c in known_ids for c in (tok, 'ANS-' + tok, 'ANS2-' + tok if a in ('ATL-10',) else tok, 'ANS2N-' + tok if a == 'ATL-11' else tok))
for k, a in atl.items():
    for tok in re.findall(r'(?<![\w-])((?:ANS2N-|ANS2-|ANS-|AS-)?(?:T\d+[a-z]?(?:-i)?|C\d+|L\d|O\d)|ANS-LIM)(?![\w])', a['body']):
        if tok.startswith('O') and k in ('ATL-10', 'ATL-11'): continue
        assert mention_ok(k, tok), ('unknown identifier in atlas text', k, tok)
front = (AD / '00_front.md').read_text(encoding='utf-8').strip()
out = [front, '']; conn = []
for k, a in atl.items():
    mine = set(a['entries'])
    o = ['## Principal results', '', '| ID | Result | Status | Review |', '|---------------|--------------------------------------|---------------------|---------|'] + [
         f"| {i} | {byid[i]['title']} | {byid[i]['status']} | {byid[i]['review_code']} |" for i in a['principal']]
    if a['open']:
        o += ['', '## Recorded open questions', ''] + [f"- **{q}:** {opn[q]}" for q in a['open']]
    uses, usedby = collections.defaultdict(set), collections.defaultdict(set)
    for e in edges:
        r, u = e['result'], e['uses']
        if r in mine and u not in mine: uses[home[u]].add(u)
        if u in mine and r not in mine: usedby[home[r]].add(r)
    o += ['', '## Connected entries (cited dependencies)', '']
    o += [f"- **Uses {j}** ({atl[j]['title']}): {', '.join(sorted(v))}." for j, v in sorted(uses.items())]
    o += [f"- **Used by {j}** ({atl[j]['title']}): {', '.join(sorted(v))}." for j, v in sorted(usedby.items())]
    if not uses and not usedby: o += ['No citation in either direction is recorded.']
    bound = [f"{i} ({byid[i]['review_code']})" for i in a['entries'] if byid[i]['review_code'] not in ('V', 'VQ')]
    quals = [f"{i}: {byid[i]['qualification']}" for i in a['entries'] if byid[i]['review_code'] == 'VQ']
    o += ['', '## Review boundary', '', ('Without a review verdict: ' + ', '.join(bound) + '.') if bound else 'Every result in this entry has a review verdict.']
    if quals: o += ['', 'Qualified verdicts:', ''] + [f'- {q}' for q in quals]
    src = collections.OrderedDict()
    for i in a['entries']: src.setdefault(byid[i]['release'], []).append(i)
    o += ['', '## All results and proof sources', ''] + [f"- **{r}:** {', '.join(v)}." for r, v in src.items()]
    text = f"# {k}: {a['title']}\n\n{a['body']}\n\n" + '\n'.join(o) + '\n'
    put(f'ATLAS/entries/{k}.md', text); out += [text]
    conn.append(dict(id=k, title=a['title'], results=a['entries'], principal=a['principal'], open_questions=a['open'],
        uses={j: sorted(v) for j, v in sorted(uses.items())}, used_by={j: sorted(v) for j, v in sorted(usedby.items())}))
put('ATLAS/ATLAS.md', '\n'.join(out))
put('ATLAS/atlas.json', json.dumps(dict(atlas='Analytic Atlas of the UNNS Substrate', date='2026-11-27', entries=conn), indent=1))
put('ATLAS/README.md', '# Analytic Atlas of the UNNS Substrate\n\nRead `ATLAS.pdf` (or `ATLAS.md`). Each entry is also a separate file under `entries/`, and `atlas.json` holds the entry structure. The text sources are in `../PROVENANCE/build/atlas/`; a new theorem is added to the catalogue and to one entry, then the collection is rebuilt.\n\n| Entry | Phenomenon | Results |\n|--|--|--|\n' + '\n'.join(f"| [{c['id']}](entries/{c['id']}.md) | {c['title']} | {len(c['results'])} |" for c in conn) + '\n\nEntries are labelled ATL to avoid confusion with the baseline identifiers AS-001 and AS-002.')
print('atlas entries', len(conn), 'results placed', len(home))
