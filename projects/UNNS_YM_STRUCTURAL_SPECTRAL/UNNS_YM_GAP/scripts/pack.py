"""Build CSV schema and SHA-256 manifest, then create ../at20.zip.

Use only after extract.py and verify.py --record have passed. This script
does not certify new data: review any changed source/extraction before packing.
"""
from pathlib import Path
import csv
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]

DESCRIPTIONS = {
    'source_id':('string','Key into source.json; exact source edition.'),
    'source_table':('integer','Published table number.'),
    'pdf_page':('integer','One-based PDF page index.'),
    'printed_page':('integer','Page number printed on the source page.'),
    'beta':('string','Bare lattice coupling beta, retained with printed trailing zeros. Empty for continuum.'),
    'ensemble_id':('string','Main ensemble key: b plus beta with decimal point replaced by p.'),
    'parent_ensemble_id':('string','Main ensemble at the same beta; foreign key to at_lat.csv.'),
    'aux_id':('string','Auxiliary lattice key, ordered as listed in Table 1.'),
    'lattice':('string','ASCII Ns^3xNt notation; isotropic spatial axes.'),
    'nx':('integer','Number of sites along spatial x.'),
    'ny':('integer','Number of sites along spatial y.'),
    'nz':('integer','Number of sites along spatial z.'),
    'nt':('integer','Number of sites along Euclidean time.'),
    'lattice_printed':('string','Visually resolved printed notation, using ^4 for a four-dimensional cube.'),
    'lattice_pdf':('string','Unmodified flattened PDF text for the main lattice; exponents lost by PDF text extraction.'),
    'aux_pdf':('string','Unmodified flattened PDF text for auxiliary lattices; comma-separated inside a quoted CSV field.'),
    'source_token':('string','Unmodified flattened PDF token for one auxiliary lattice.'),
    'use':('string','Collective Table 1 auxiliary purpose; exact per-lattice purpose not specified in Table 1.'),
    'plaquette':('number','Mean plaquette (1/3) Re Tr <U_p>, dimensionless.'),
    'plaquette_err':('number','Quoted absolute error on mean plaquette, dimensionless.'),
    'plaquette_raw':('string','Original mean plaquette value(error) token.'),
    'a_sqrt_sigma':('number','Lattice spacing times square root of string tension, dimensionless.'),
    'a_sqrt_sigma_err':('number','Quoted absolute error on a*sqrt(sigma), dimensionless.'),
    'a_sqrt_sigma_raw':('string','Original a*sqrt(sigma) value(error) token.'),
    'am_gap':('number','Table 1 lattice mass-gap estimate a*m_G, dimensionless; not overwritten by other tables.'),
    'am_gap_err':('number','Quoted absolute error on a*m_G, dimensionless.'),
    'am_gap_raw':('string','Original Table 1 mass-gap value(error) token.'),
    'R':('string','Cubic irrep A1, A2, E, T1 or T2; empty for flux energy.'),
    'P':('string','Parity sign + or -; empty for flux energy.'),
    'C':('string','Charge-conjugation sign + or -; empty for flux energy.'),
    'channel':('string','R concatenated with parity and charge-conjugation signs; empty for flux energy.'),
    'irrep_dim':('integer_or_empty','Known cubic irrep dimension, not a count of independent mass measurements; empty for flux.'),
    'slot':('integer','One-based printed row in each irrep/parity/charge block. Flux uses placeholder 1.'),
    'state_index':('integer','slot minus 1; printed-order index, not a globally matched excitation ID. Flux uses placeholder 0.'),
    'quantity':('string','aM, aE_l, or M_over_sqrt_sigma; all dimensionless.'),
    'value':('number','Central value after documented punctuation normalization only.'),
    'uncertainty':('number','Absolute error expanded from parenthetical last digits; same units as value.'),
    'raw':('string','Original numeric token with quoted error and any star, decimal comma or missing parenthesis; empty for a blank cell.'),
    'poor_fit':('integer','1 if Table 14 marks chi2/dof > 2.5, 0 if unmarked. No fit-quality inference for lattice/flux tables.'),
    'note_ids':('string','Semicolon-separated note IDs in notes.json; empty if no row-specific note.'),
    'record_id':('string','Unique measurement key; no cross-ensemble state correspondence asserted.'),
    'status':('string','reported or blank. Blank is not zero, and not an interpolated measurement.'),
    'bbox_pt':('string','x0|top|x1|bottom in PDF points (1/72 inch), origin top-left, for a numeric word; empty for blank cells.'),
    'n_reported':('integer','Number of reported mass measurements in this ensemble/channel.'),
    'coverage':('string','reported when n_reported > 0; otherwise not_reported. Does not assert channel absence in the theory.')
}
KEYS = {
    'at_t01.csv':['source_id','beta'],
    'at_t07_13.csv':['source_id','source_table','beta','R','P','C','slot','quantity'],
    'at_t14.csv':['source_id','R','P','C','slot'],
    'at_lat.csv':['ensemble_id'],
    'at_aux.csv':['aux_id'],
    'at_mass.csv':['record_id'],
    'at_cont.csv':['record_id'],
    'at_flux.csv':['record_id'],
    'at_cov.csv':['ensemble_id','channel']
}

def dump(path,obj):
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def files():
    return sorted(p for p in ROOT.rglob('*') if p.is_file()
                  and '__pycache__' not in p.parts and p.suffix!='.pyc'
                  and p.name!='manifest.json')

def main():
    tables = {}
    for p in sorted((ROOT/'data').rglob('*.csv')):
        with p.open(encoding='utf-8',newline='') as f:
            reader = csv.DictReader(f)
            columns = reader.fieldnames
            rows = list(reader)
        pk = KEYS[p.name]
        assert len(rows)==len({tuple(r[c] for c in pk) for r in rows}), p
        tables[p.relative_to(ROOT).as_posix()] = dict(
            rows=len(rows),primary_key=pk,
            columns=[dict(name=c,type=DESCRIPTIONS[c][0],description=DESCRIPTIONS[c][1]) for c in columns])
    dump(ROOT/'schema.json',dict(version=1,csv_encoding='UTF-8 without BOM',delimiter=',',
                                 newline='LF',decimal_separator='.',missing_value='empty string',
                                 numeric_units='dimensionless unless site counts or PDF points',
                                 uncertainties='absolute quoted errors; confidence level/covariance not inferred',
                                 tables=tables))
    entries = []
    for p in files():
        rel = p.relative_to(ROOT).as_posix()
        entry = dict(path=rel,bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
        if rel in tables:
            entry['rows']=tables[rel]['rows']
        entries.append(entry)
    dump(ROOT/'manifest.json',dict(package='at20',version='1.0.0',created_date='2026-09-29',
                                  algorithm='SHA-256',paths_relative_to='package root',
                                  excluded=['manifest.json itself','at20.zip archive','Python bytecode/cache'],
                                  source_origin='public arXiv v2 fallback; prior uploads unavailable',files=entries))
    # Fixed ZIP timestamp makes rebuilding the same bytes deterministic.
    target = ROOT.parent/'at20.zip'
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(files()+[ROOT/'manifest.json']):
            info = zipfile.ZipInfo('at20/'+p.relative_to(ROOT).as_posix(),date_time=(2026,9,29,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o644 << 16
            z.writestr(info,p.read_bytes())
    print(f'Packaged {len(entries)+1} files: {target.name} ({target.stat().st_size} bytes)')

if __name__=='__main__':
    main()
