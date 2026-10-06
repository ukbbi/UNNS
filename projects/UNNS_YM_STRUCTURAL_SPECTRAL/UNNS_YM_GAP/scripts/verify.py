"""Independent numerical/source/manifest verification; exits nonzero on failure."""
from pathlib import Path
from decimal import Decimal
from collections import Counter
import csv
import hashlib
import json
import re
import sys
import pypdf

ROOT = Path(__file__).resolve().parents[1]

def read(name):
    with (ROOT/name).open(encoding='utf-8',newline='') as f:
        return list(csv.DictReader(f))

def check(cond,msg):
    if not cond:
        raise AssertionError(msg)

def main():
    source = json.loads((ROOT/'source.json').read_text(encoding='utf-8'))
    pdfpath = ROOT/source['local_file']
    check(hashlib.sha256(pdfpath.read_bytes()).hexdigest()==source['sha256'],'source hash')
    counts = json.loads((ROOT/'counts.json').read_text(encoding='utf-8'))
    for name,expected in counts['csv_rows'].items():
        check(len(read(name))==expected,f'row count: {name}')
    raw1 = read('data/raw/at_t01.csv')
    rawm = read('data/raw/at_t07_13.csv')
    rawc = read('data/raw/at_t14.csv')
    masses = read('data/derived/at_mass.csv')
    cont = read('data/derived/at_cont.csv')
    flux = read('data/derived/at_flux.csv')
    lat = read('data/derived/at_lat.csv')
    aux = read('data/derived/at_aux.csv')
    cov = read('data/derived/at_cov.csv')
    expected_counts = {'5.6924':5,'5.80':10,'5.8941':40,'5.99':62,'6.0625':71,'6.235':80,'6.3380':85,'6.50':90}
    check(Counter(r['beta'] for r in masses)==expected_counts,'mass counts by beta')
    check((len(masses),len(cont),len(flux),len(lat),len(aux),len(cov))==(443,59,8,8,10,160),'fixed totals')
    check(sum(r['status']=='blank' for r in rawm)==113,'mass blanks')
    check(sum(r['status']=='blank' for r in rawc)==17,'continuum blanks')

    # Independent PDF engine: full source-token stream, with only spaces
    # introduced by pypdf after the decimal separator removed.
    pdf = pypdf.PdfReader(pdfpath)
    pattern = re.compile(r'\d+[.,]\s*\d+\(\d+\)?\*?')
    per_table = {}
    for table,page in [(1,34),(7,37),(8,38),(9,39),(10,40),(11,41),(12,42),(13,43),(14,44)]:
        text = pdf.pages[page-1].extract_text().split(f'Table {table}:')[0]
        if table==7:
            text = text.rsplit('aM',1)[1]
        tokens = [re.sub(r'\s+','',m.group()) for m in pattern.finditer(text)]
        if table==1:
            expected = [r[k] for r in raw1 for k in ['plaquette_raw','a_sqrt_sigma_raw','am_gap_raw']]
        else:
            expected = [r['raw'] for r in (rawc if table==14 else rawm)
                        if int(r['source_table'])==table and r['status']=='reported']
        check(tokens==expected,f'pypdf ordered tokens Table {table}: {len(tokens)} vs {len(expected)}')
        per_table[str(table)] = len(tokens)

    bybeta = {r['beta']:r for r in lat}
    for rows in [masses,cont,flux]:
        check(len(rows)==len({r['record_id'] for r in rows}),'unique measurement keys')
        for r in rows:
            token = r['raw'].rstrip('*').replace(',','.')
            central,error_digits = token.split('(')
            places = len(central.split('.')[1])
            error = Decimal(error_digits.rstrip(')'))/(Decimal(10)**places)
            check(r['value']==central and Decimal(r['uncertainty'])==error,'numeric normalization')
            check(Decimal(r['value'])>0 and error>0,'positive values/errors')
            check(int(r['poor_fit'])==int(r['raw'].endswith('*')),'star preserved')
            check(int(r['state_index'])==int(r['slot'])-1,'slot identity')
            if 'beta' in r:
                check(all(r[k]==bybeta[r['beta']][k] for k in ['ensemble_id','lattice','nx','ny','nz','nt']),'ensemble join')
    for r in lat:
        for col in ['plaquette','a_sqrt_sigma','am_gap']:
            central,err = r[col+'_raw'].rstrip(')').split('(')
            check(r[col]==central and Decimal(r[col+'_err'])==Decimal(err).scaleb(-len(central.split('.')[1])),'Table 1 errors')
    def key(r):
        return tuple(r.get(k,'') for k in ['source_table','beta','R','P','C','slot','quantity'])
    rawdict = {key(r):r for r in rawm+rawc if r['status']=='reported'}
    check(len(rawdict)==len(masses)+len(cont)+len(flux),'raw keys unique')
    for r in masses+cont+flux:
        check(rawdict[key(r)]['raw']==r['raw'],'raw/derived identity')
    check(sum(r['poor_fit']=='1' for r in cont)==4,'four continuum stars')
    starred = {(r['channel'],r['slot']) for r in cont if r['poor_fit']=='1'}
    check(starred=={('T1--','2'),('T2++','3'),('T2-+','3'),('T2--','2')},'star locations')
    repairs = {(r['source_table'],r['channel'],r['slot'],r['raw']) for r in masses if 'N01' in r['note_ids'] or 'N02' in r['note_ids']}
    check(repairs=={('11','T2++','2','1,0247(52)'),('8','A2--','1','2.10(12'),('12','T2++','5','0.974(12')},'editorial repair locations')
    gs = {r['beta']:r for r in masses if r['channel']=='A1++' and r['slot']=='1'}
    check(len(gs)==8,'eight scalar ground states')
    mismatch = [beta for beta,r in gs.items() if r['raw']!=bybeta[beta]['am_gap_raw']]
    check(mismatch==['5.8941'],'Table 1/Table 8 discrepancy preserved')
    check(gs['5.8941']['raw']=='0.799(10)' and bybeta['5.8941']['am_gap_raw']=='0.7991(92)','both discrepant values')
    for r in cov:
        n = sum(m['beta']==r['beta'] and m['channel']==r['channel'] for m in masses)
        check(n==int(r['n_reported']),'coverage count')
    check(sum(int(r['n_reported']) for r in cov)==443,'coverage total')

    if '--record' in sys.argv:
        report = dict(status='passed',source_sha256=source['sha256'],
                      pdfplumber_version='0.11.9',pypdf_version=pypdf.__version__,
                      independent_ordered_tokens_by_table=per_table,
                      independent_numeric_tokens=sum(per_table.values()),
                      visual_review=dict(status='completed',pdf_pages=[34,37,38,39,40,41,42,43,44],
                                         scope='Column/channel identities, lattice exponents, printed numerical tokens, malformed tokens, stars, and table captions'),
                      checks=['fixed row and ensemble counts','raw/derived identity','all source numeric tokens in source order via second PDF reader',
                              'unique keys','positive errors','ensemble joins','parenthetical error expansion','coverage counts',
                              'four poor-fit locations','three editorial repairs','Table 1/Table 8 scalar discrepancy'],
                      limitations=['Missing uploaded PDFs not compared','Publisher PDF not compared',
                                   'No original simulation data, covariance, correlators or continuum refits checked'])
        (ROOT/'qa.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    else:
        manifest = json.loads((ROOT/'manifest.json').read_text(encoding='utf-8'))
        for entry in manifest['files']:
            path = ROOT/entry['path']
            check(path.is_file(),f'missing file: {path}')
            check(path.stat().st_size==entry['bytes'],f'size mismatch: {path}')
            check(hashlib.sha256(path.read_bytes()).hexdigest()==entry['sha256'],f'hash mismatch: {path}')
        print(f"Verified {len(manifest['files'])} manifest entries.")
    print(f'PASS: 443 lattice masses, 59 continuum ratios, 8 flux energies; {sum(per_table.values())} independently matched numeric tokens.')

if __name__=='__main__':
    main()
