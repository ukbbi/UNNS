"""Extract the pinned AT2020 PDF. Run from any directory: python extract.py.

Source files are never modified. All coordinates are PDF points, top-origin.
Requires pdfplumber==0.11.9. No network access occurs during a rebuild.
"""
from pathlib import Path
from decimal import Decimal
from collections import Counter
import csv
import hashlib
import json
import re
import sys
import pdfplumber

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw'
OUT = ROOT / 'data' / 'derived'
SOURCE = 'at20v2'
SHA = 'f0eb6406bf49a00d376c0be25917173426c826050046a1bf0f32987895de23d0'
BETAS = ['5.6924', '5.80', '5.8941', '5.99', '6.0625', '6.235', '6.3380', '6.50']
SIZES = [(10,16),(12,16),(14,16),(18,18),(20,20),(26,26),(30,30),(38,38)]
PCS = [('+','+'),('-','+'),('+','-'),('-','-')]
REPS = ['A1','A2','E','T1','T2']
DIM = {'A1':1,'A2':1,'E':2,'T1':3,'T2':3}
PAT = re.compile(r'^(\d+[.,]\d+)\((\d+)\)?(\*)?$')
COUNTS = {}

def write_csv(path, rows):
    assert rows, path
    with path.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n')
        w.writeheader()
        w.writerows(rows)
    COUNTS[path.relative_to(ROOT).as_posix()] = len(rows)

def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

def parse(token):
    m = PAT.fullmatch(token)
    assert m, token
    value, digits, star = m.groups()
    value = value.replace(',', '.')
    err = Decimal(digits).scaleb(-len(value.split('.')[1]))
    note = []
    if ',' in token:
        note.append('N01')
    if ')' not in token:
        note.append('N02')
    return value, format(err, 'f'), int(bool(star)), ';'.join(note)

def src(table):
    printed = 33 if table == 1 else table + 29
    return dict(source_id=SOURCE, source_table=table, pdf_page=printed+1, printed_page=printed)

def ens(beta):
    ns, nt = SIZES[BETAS.index(beta)]
    return dict(ensemble_id='b'+beta.replace('.','p'), beta=beta,
                lattice=f'{ns}^3x{nt}', nx=ns, ny=ns, nz=ns, nt=nt)

def bbox(w):
    return '|'.join(f'{w[k]:.3f}' for k in ['x0','top','x1','bottom']) if w else ''

def record(table, beta, rep, p, c, slot, word, quantity='aM'):
    return dict(**src(table), beta=beta, R=rep, P=p, C=c,
                slot=slot, quantity=quantity, raw=word['text'] if word else '',
                status='reported' if word else 'blank', bbox_pt=bbox(word))

def same_line(words, y, tol=4):
    return sorted([w for w in words if abs(w['top']-y)<tol], key=lambda w:w['x0'])

def extract_t1(page):
    words = page.extract_words()
    beta_words = [w for w in words if w['text'] in BETAS and w['x0']<160 and w['top']<220]
    assert [w['text'] for w in beta_words] == BETAS
    rows = []
    for bw in beta_words:
        ws = same_line(words, bw['top'])
        assert len(ws) == 6, ws
        rows.append(dict(**src(1), beta=ws[0]['text'], lattice_pdf=ws[1]['text'],
                         plaquette_raw=ws[2]['text'], a_sqrt_sigma_raw=ws[3]['text'],
                         am_gap_raw=ws[4]['text'], aux_pdf=ws[5]['text']))
    return rows

def extract_t7(page):
    # Table 6 shares this page; its numbers are explicitly excluded.
    words = page.extract_words()
    values = [w for w in words if 460<w['top']<625 and PAT.fullmatch(w['text'])]
    ys = sorted({round(w['top'],2) for w in values})
    # Manually reviewed row labels resolve superscript/subscript extraction.
    labels = [('A1','+','+',1),('A1','+','+',2),('A1','+','+',3),
              ('E','+','+',1),('E','+','+',2),('T2','+','+',1),
              ('A1','-','+',1),('E','-','+',1),('T2','-','+',1),
              ('T1','+','-',1),('','','',1)]
    assert len(ys)==len(labels), ys
    result = []
    for y, (rep,p,c,slot) in zip(ys, labels):
        ws = same_line(values,y,0.5)
        for col,beta in enumerate(BETAS[:2]):
            found = [w for w in ws if (w['x0']>=325)==bool(col)]
            assert len(found)<=1
            result.append(record(7,beta,rep,p,c,slot,found[0] if found else None,
                                 'aM' if rep else 'aE_l'))
    assert sum(r['status']=='reported' for r in result)==17
    return result

def extract_grid(page, table):
    words = page.extract_words()
    headers = [w for w in words if re.fullmatch(r'P=[+-],C=[+-]',w['text'])]
    assert [w['text'] for w in headers] == ['P=+,C=+','P=-,C=+','P=+,C=-','P=-,C=-']
    hy = headers[0]['top']
    end = min(w['top'] for w in words if w['text']=='Table' and w['top']>hy)
    flux = [w for w in words if w['text']=='aE' and hy<w['top']<end]
    if flux:
        end = flux[0]['top']
    labels = [w for w in words if w['x0']<195 and hy<w['top']<end
              and w['text'] in ['A','A1','A2','E','T1','T2']]
    assert len(labels)==5, labels
    vals = [w for w in words if hy<w['top']<end and PAT.fullmatch(w['text'])]
    centers = [(w['x0']+w['x1'])/2 for w in headers]
    beta = '' if table==14 else BETAS[table-6]
    result = []
    consumed = 0
    for i,label in enumerate(labels):
        low = label['top']-0.5
        high = labels[i+1]['top']-0.5 if i<4 else end
        group = [w for w in vals if low<=w['top']<high]
        ys = sorted({round(w['top'],2) for w in group})
        for slot,y in enumerate(ys,1):
            ws = same_line(group,y,0.5)
            for col,(p,c) in enumerate(PCS):
                found = [w for w in ws if min(range(4),key=lambda j:abs((w['x0']+w['x1'])/2-centers[j]))==col]
                assert len(found)<=1, found
                consumed += len(found)
                result.append(record(table,beta,REPS[i],p,c,slot,found[0] if found else None,
                                     'M_over_sqrt_sigma' if table==14 else 'aM'))
    assert consumed==len(vals)
    if flux:
        fw = [w for w in same_line(words,flux[0]['top'],1) if PAT.fullmatch(w['text'])]
        assert len(fw)==1
        result.append(record(table,beta,'','','',1,fw[0],'aE_l'))
    return result

def normalized(r):
    v,e,star,note = parse(r['raw'])
    if star:
        note = ';'.join(filter(None,[note,'N05']))
    if r['source_table']==8 and r['R']=='A1' and r['P']==r['C']=='+' and r['slot']==1:
        note = ';'.join(filter(None,[note,'N03']))
    return dict(**src(r['source_table']), R=r['R'], P=r['P'], C=r['C'],
                channel=r['R']+r['P']+r['C'], irrep_dim=DIM.get(r['R'],''),
                slot=r['slot'], state_index=r['slot']-1, quantity=r['quantity'],
                value=v, uncertainty=e, raw=r['raw'], poor_fit=star, note_ids=note)

def decode_size(token):
    # PDF text loses exponent formatting. Explicit grammar after visual check.
    m = re.fullmatch(r'(\d+)3(\d{2})',token)
    if m:
        return tuple(map(int,m.groups()))
    assert token.endswith('4'), token
    n = int(token[:-1])
    return n,n

def main():
    pdf = RAW/'at20.pdf'
    assert hashlib.sha256(pdf.read_bytes()).hexdigest()==SHA, 'Unexpected PDF: do not apply pinned coordinates to a different version.'
    OUT.mkdir(parents=True,exist_ok=True)
    with pdfplumber.open(pdf) as doc:
        assert len(doc.pages)==75
        lattice_raw = extract_t1(doc.pages[33])
        mass_raw = extract_t7(doc.pages[36])
        for table in range(8,14):
            mass_raw.extend(extract_grid(doc.pages[table+29],table))
        cont_raw = extract_grid(doc.pages[43],14)
    write_csv(RAW/'at_t01.csv',lattice_raw)
    write_csv(RAW/'at_t07_13.csv',mass_raw)
    write_csv(RAW/'at_t14.csv',cont_raw)
    lattices,aux = [],[]
    for r in lattice_raw:
        row = dict(**src(1),**ens(r['beta']))
        assert decode_size(r['lattice_pdf'])==(row['nx'],row['nt'])
        row['lattice_printed'] = f"{row['nx']}^4" if row['nx']==row['nt'] else f"{row['nx']}^3x{row['nt']}"
        for col in ['plaquette','a_sqrt_sigma','am_gap']:
            v,e,_,_ = parse(r[col+'_raw'])
            row.update({col:v,col+'_err':e,col+'_raw':r[col+'_raw']})
        row['note_ids'] = 'N03' if r['beta']=='5.8941' else ''
        lattices.append(row)
        for i,size in enumerate(r['aux_pdf'].split(','),1):
            ns,nt = decode_size(size)
            aux.append(dict(**src(1),parent_ensemble_id=row['ensemble_id'],beta=r['beta'],
                            aux_id=row['ensemble_id']+f'_aux{i}',lattice=f'{ns}^3x{nt}',
                            nx=ns,ny=ns,nz=ns,nt=nt,source_token=size,
                            use='finite_volume_or_topology',note_ids='N04'))
    masses,flux = [],[]
    for r in mass_raw:
        if r['status']=='blank':
            continue
        base = dict(**ens(r['beta']),**normalized(r))
        if r['quantity']=='aM':
            base['record_id'] = base['ensemble_id']+'_'+base['channel']+f"_s{r['slot']:02}"
            masses.append(base)
        else:
            base['record_id'] = base['ensemble_id']+'_flux'
            flux.append(base)
    continuum = []
    for r in cont_raw:
        if r['status']=='reported':
            base = normalized(r)
            base['record_id'] = 'cont_'+base['channel']+f"_s{r['slot']:02}"
            continuum.append(base)
    coverage = []
    for beta in BETAS:
        for rep in REPS:
            for p,c in PCS:
                rr = [r for r in mass_raw if (r['beta'],r['R'],r['P'],r['C'])==(beta,rep,p,c)]
                n = sum(r['status']=='reported' for r in rr)
                coverage.append(dict(**ens(beta),R=rep,P=p,C=c,channel=rep+p+c,
                                     n_reported=n,coverage='reported' if n else 'not_reported'))
    for name,rows in [('at_lat',lattices),('at_aux',aux),('at_mass',masses),
                      ('at_cont',continuum),('at_flux',flux),('at_cov',coverage)]:
        write_csv(OUT/(name+'.csv'),rows)
    for rows in [masses,continuum,flux]:
        assert len({r['record_id'] for r in rows})==len(rows)
        assert all(Decimal(r['value'])>0 and Decimal(r['uncertainty'])>0 for r in rows)
    assert len(lattices)==8 and len(aux)==10 and len(flux)==8 and len(coverage)==160
    assert sum(r['poor_fit'] for r in continuum)==4
    assert sum('N01' in r['note_ids'] for r in masses)==1
    assert sum('N02' in r['note_ids'] for r in masses)==2
    assert sum(r['n_reported'] for r in coverage)==len(masses)
    assert sum(r['P']==r['C']=='+' and r['R']=='A1' and r['slot']==1 for r in masses)==8
    write_json(ROOT/'counts.json',dict(csv_rows=COUNTS,
        masses_by_beta=dict(Counter(r['beta'] for r in masses)),
        continuum_by_channel=dict(Counter(r['channel'] for r in continuum)),
        blank_mass_cells=sum(r['status']=='blank' for r in mass_raw),
        blank_continuum_cells=sum(r['status']=='blank' for r in cont_raw),
        poor_fit_entries=4,normalization_repairs=3))
    print(json.dumps({'csv_rows':COUNTS,'masses_by_beta':dict(Counter(r['beta'] for r in masses))},indent=2))

if __name__=='__main__':
    main()
