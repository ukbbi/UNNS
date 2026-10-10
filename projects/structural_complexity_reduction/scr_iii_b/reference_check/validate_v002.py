"""Execute a deterministic source-formula C++ ↔ independent Python comparison.
C++ is a small, auditable extraction of the Dryad SPMMC v1.00 formula, NOT an
execution of the full original GSL simulator. Do not mistake this for full reference validation.
"""
from __future__ import annotations
import hashlib, json, math, pathlib, subprocess, sys, time
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'models'))
from physical_energy import pair_coupling, ice_ok, energy, enumerate_patch
HERE=pathlib.Path(__file__).resolve().parent
DEST=ROOT/'output'/'validation'/'v002'
DEST.mkdir(parents=True,exist_ok=True)

def geometry(L,a=260):
    # Original SPMMC index/orientation convention, independent of v001 patch().
    e=[]
    for y in range(L):
        for x in range(L):
            e.extend([((x+.5)*a,-y*a,1.,0.),(x*a,-(y+.5)*a,0.,-1.)])
    e.extend([(-.5*a,-y*a,1.,0.) for y in range(L)])
    e.extend([(x*a,.5*a,0.,-1.) for x in range(L)])
    return e

def vertices(L):
    # input state signs are the original Dryad vectors (right, downward).
    es=geometry(L); vs=[]
    for y in range(L):
        for x in range(L):
            v=[]
            for idx,(ex,ey,ux,uy) in enumerate(es):
                # midpoint on a ray of length a/2 from vertex
                dx=ex-260*x; dy=ey+260*y
                if math.isclose(math.hypot(dx,dy),130.,abs_tol=1e-8):
                    # dot spin direction with displacement towards vertex
                    sig=1 if ux*(-dx)+uy*(-dy)>0 else -1
                    v.append((idx,sig))
            assert len(v)==4,(L,x,y,v)
            vs.append(tuple(v))
    return vs

def run():
    cpp=HERE/'dryad_pair.cpp'
    exe=HERE/('dryad_pair.exe' if sys.platform=='win32' else 'dryad_pair.bin')
    subprocess.run(['g++','-std=c++17','-O2',str(cpp),'-o',str(exe)],check=True,capture_output=True,text=True)
    cases=[]
    for L in (1,2,3):
        process=subprocess.run([str(exe),str(L)],check=True,capture_output=True,text=True)
        ref_edges={};ks={}
        for line in process.stdout.splitlines():
            row=line.split()
            if row[0]=='E':ref_edges[int(row[1])]=tuple(map(float,row[2:]))
            if row[0]=='K':ks[int(row[1]),int(row[2])]=float(row[3])
        edges=geometry(L)
        assert len(edges)==len(ref_edges)
        geom_err=max(abs(a-b) for i,e in enumerate(edges) for a,b in zip(e,ref_edges[i]))
        max_err=max(abs(pair_coupling(edges[i],edges[j])-k) for (i,j),k in ks.items())
        pairs=[(i,j,k) for (i,j),k in ks.items()]
        # Numerical spin-flip identity for reproducible deterministic patterns, source field h= sum(K*s).
        flip_err=0.
        for t in range(8):
            state=[1 if ((i*17+t*31+L*7)%11)<5 else -1 for i in range(len(edges))]
            baseline=energy(state,pairs)
            for i in range(len(edges)):
                flipped=state.copy();flipped[i]*=-1
                h=sum(k*state[j] if ii==i else k*state[ii] for ii,j,k in pairs if ii==i or j==i)
                flip_err=max(flip_err,abs(energy(flipped,pairs)-baseline-2*state[i]*h))
        rec={'L':L,'spins':len(edges),'pairs':len(ks),'geometry_max_abs_error':geom_err,'coupling_max_abs_error':max_err,'spin_flip_max_abs_error':flip_err}
        if L<=2:
            vs=vertices(L)
            best=math.inf; ground=[]; bestice=math.inf; bestnonice=math.inf; n_ice=0
            for k in range(1<<len(edges)):
                s=tuple(1 if k>>i&1 else -1 for i in range(len(edges)))
                en=energy(s,pairs); ice=ice_ok(s,vs);n_ice+=ice
                if ice:bestice=min(bestice,en)
                else:bestnonice=min(bestnonice,en)
                if en<best-1e-13:best=en;ground=[s]
                elif abs(en-best)<1e-13:ground.append(s)
            rec.update({'states':2**len(edges),'ice_states':n_ice,'ground_count':len(ground),'ground_all_ice':all(ice_ok(s,vs) for s in ground),'ground_energy':best,'minimum_ice_energy':bestice,'minimum_nonice_energy':bestnonice})
        cases.append(rec)
    threshold=1e-12
    cross_pass=all(r['geometry_max_abs_error']<threshold and r['coupling_max_abs_error']<threshold and r['spin_flip_max_abs_error']<threshold for r in cases)
    verdict='FORMULA_CROSSCHECK_PASS_FULL_REFERENCE_PENDING' if cross_pass else 'FORMULA_CROSSCHECK_FAIL'
    result={'verdict':verdict,'reference':'Dryad SPMMC-SSI-Unix-v1.00.cpp pair/field equations manually transcribed into independent C++ harness','caveat':'C++ harness is transcribed, not original GSL simulation; Hamiltonian physical scaling and reference simulator energy comparison are not established.','temperature':'athermal pair couplings; no T-dependent magnetization scaling','pair_interaction':'all pair (SPMMC; cut-off effectively unlimited)','model_dimensions_nm':{'a':260,'l':160,'w':60,'h':16},'tolerance':threshold,'cases':cases,'source_cpp_sha256':hashlib.sha256(cpp.read_bytes()).hexdigest()}
    (DEST/'ENERGY_REFERENCE_v002.json').write_text(json.dumps(result,indent=2)+'\n')
    lines=['# SCR-III-B Energy Reference Preflight v002','',f'**Verdict:** `{verdict}`','', '## Cross-language deterministic checks','', '| L | Spins | Pair coefficients | Max C++/Python coupling difference | Flip identity error | Ice ground? |','|---:|---:|---:|---:|---:|---|']
    for r in cases:lines.append(f"| {r['L']} | {r['spins']} | {r['pairs']} | {r['coupling_max_abs_error']:.3g} | {r['spin_flip_max_abs_error']:.3g} | {r.get('ground_all_ice','not enumerated')} |")
    lines+=['','## Scope and limitations','','- This is a deterministic, auditable C++ transcription of the original Dryad pair-coupling equation, compared with the independently written Python v001 expression. It is **not a comparison to energy output from the unmodified Dryad simulation**.','- The v001 non-ice ground states were reproduced using the Dryad coordinate orientation and sign convention in this harness, but physical identification of the normalized energy remains provisional.','- Direct full-reference validation, temperature normalization, H_full selection, interaction ranges, and 3×3 exact target solution remain open.','- No preregistration or physical-transfer outcome is claimed.']
    (DEST/'ENERGY_REFERENCE_v002.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps(result,indent=2))
    if not cross_pass:sys.exit(1)
if __name__=='__main__':run()
