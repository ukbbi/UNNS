#!/usr/bin/env python3
"""Direct SciServer/Ceph extraction for the preregistered high-Re branch.

Reads only the frozen central 256^3 velocity cubes from the mounted JHTDB Zarr
arrays and writes one HDF5 per snapshot. No JHTDB authorization token is used.
Snapshots are NOT treated as a temporal sequence.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, math, os, sys, time
import numpy as np
import h5py
import zarr

BASE = Path('/home/idies/workspace/turbulence-ceph/sciserver-turbulence')
SAMPLES = [
    {
      'dataset':'isotropic8192','grid_n':8192,
      'zarr':BASE/'isotropic8192'/'isotropic8192.zarr'/'velocity',
      'bounds':(3969,4224),
      'snapshots':[(0,'PRIMARY_HIGH_RE'),(1,'PRIMARY_HIGH_RE'),(2,'PRIMARY_HIGH_RE'),(3,'PRIMARY_HIGH_RE'),(4,'PRIMARY_HIGH_RE'),(5,'PRESPECIFIED_LOW_RE_CONTRAST')]
    },
    {
      'dataset':'isotropic32768','grid_n':32768,
      'zarr':BASE/'isotropic32768'/'isotropic32768.zarr'/'velocity',
      'bounds':(16257,16512),
      'snapshots':[(0,'PRIMARY_EXTREME_RE')]
    }
]


def sha256_file(p):
    h=hashlib.sha256()
    total=p.stat().st_size; done=0
    with p.open('rb') as f:
        for b in iter(lambda:f.read(16*1024*1024), b''):
            h.update(b); done += len(b)
            print(f'  hash {100*done/total:6.2f}%', end='\r', flush=True)
    print(' '*30, end='\r')
    return h.hexdigest()


def writable_volume():
    # Prefer scratch Temporary volume, then persistent Storage volume.
    roots=[Path('/home/idies/workspace/Temporary'), Path('/home/idies/workspace/Storage')]
    candidates=[]
    for root in roots:
        if not root.exists(): continue
        for depth in (2,1,3):
            pattern='/'.join(['*']*depth)
            for p in root.glob(pattern):
                if p.is_dir() and os.access(p, os.W_OK):
                    score=0
                    if p.name.lower()=='scratch': score += 100
                    if p.name.lower()=='persistent': score += 80
                    if 'Temporary' in p.parts: score += 20
                    candidates.append((score,p))
            if candidates: break
        if candidates: break
    if not candidates:
        raise RuntimeError('No writable SciServer Storage/Temporary volume auto-detected. Re-run with --output /home/idies/workspace/Temporary/<user>/<volume>/HIGH_RE_EXPORT')
    candidates.sort(key=lambda x:(-x[0],str(x[1])))
    return candidates[0][1]/'HIGH_RE_EXPORT'


def verify_array(a, sample):
    n=sample['grid_n']
    if len(a.shape)!=5 or a.shape[1:4]!=(n,n,n) or a.shape[-1]!=3:
        raise ValueError(f"Unexpected Zarr shape for {sample['dataset']}: {a.shape}")
    need=max(i for i,_ in sample['snapshots'])+1
    if a.shape[0] < need:
        raise ValueError(f"Not enough snapshots in {sample['dataset']}: {a.shape[0]} < {need}")


def write_one(sample, snap, role, out_root):
    name=sample['dataset']; n=sample['grid_n']; start1,end1=sample['bounds']
    a=zarr.open(str(sample['zarr']), mode='r')
    verify_array(a,sample)
    s0=start1-1; e0=end1  # Python stop is exclusive; 1-based inclusive -> [start-1:end]
    print(f'[{name} snapshot {snap}] reading central cube {start1}:{end1} on x/y/z...')
    t0=time.time()
    data=np.asarray(a[snap, s0:e0, s0:e0, s0:e0, :], dtype=np.float32)
    if data.shape!=(256,256,256,3):
        raise ValueError(f'Unexpected extracted shape: {data.shape}')
    if not np.isfinite(data).all():
        raise ValueError('Non-finite velocity values encountered.')
    print(f'  read complete in {time.time()-t0:.1f} s; {data.nbytes/1024**2:.1f} MiB')

    ddir=out_root/name
    ddir.mkdir(parents=True,exist_ok=True)
    stem=f'{name}-snap{snap:02d}-center256-velocity'
    h5=ddir/f'{stem}.h5'
    if h5.exists():
        raise FileExistsError(f'Refusing to overwrite existing frozen extraction: {h5}')

    dx=2*math.pi/n
    coords=(np.arange(start1-1,end1,dtype=np.float64)*dx).astype(np.float32)
    with h5py.File(h5,'w') as f:
        f.create_dataset('Velocity_0001', data=data, dtype='f4', chunks=(64,64,64,3))
        f.create_dataset('xcoor',data=coords,dtype='f4')
        f.create_dataset('ycoor',data=coords,dtype='f4')
        f.create_dataset('zcoor',data=coords,dtype='f4')
        f.attrs['dataset']=name
        f.attrs['source_snapshot_label']=snap
        f.attrs['source_zarr_index']=snap
        f.attrs['sample_role']=role
        f.attrs['x_start']=start1; f.attrs['x_end']=end1
        f.attrs['y_start']=start1; f.attrs['y_end']=end1
        f.attrs['z_start']=start1; f.attrs['z_end']=end1
        f.attrs['axis_order']='zyxc'
        f.attrs['domain']='2pi_periodic_parent_nonperiodic_cutout'
        f.attrs['extraction_method']='direct_sciserver_ceph_zarr_slice'
        f.attrs['temporal_sequence']=False
        f.attrs['created_utc']=datetime.now(timezone.utc).isoformat()
    del data

    print('  computing HDF5 SHA-256...')
    digest=sha256_file(h5)
    rec={
      'schema':'UNNS_JHTDB_HIGH_RE_SOURCE_RECORD_v0.1',
      'status':'ACQUIRED_HASHED_READY_FOR_SCALE_ADAPTER',
      'branch':'jhtdb_high_re',
      'dataset':name,
      'grid_n':n,
      'source_zarr_path':str(sample['zarr']),
      'source_snapshot_label':snap,
      'source_zarr_index':snap,
      'sample_role':role,
      'coords_1based_inclusive':{'x':[start1,end1],'y':[start1,end1],'z':[start1,end1]},
      'shape_zyxc':[256,256,256,3],
      'axis_order':'zyxc',
      'parent_domain_periodic':True,
      'cutout_analysis_periodic':False,
      'hdf5_file':h5.name,
      'sha256':digest,
      'hdf5_bytes':h5.stat().st_size,
      'created_utc':datetime.now(timezone.utc).isoformat(),
      'field_value_selection_rule':'frozen central native-grid 256^3 cube; no post-result reselection'
    }
    recp=ddir/f'{stem}_SOURCE_RECORD.json'
    recp.write_text(json.dumps(rec,indent=2)+'\n',encoding='utf-8')
    (ddir/f'{stem}_SHA256.txt').write_text(f'{digest}  {h5.name}\n',encoding='utf-8')
    print('  SHA-256:',digest)
    print('  wrote:',h5)
    return rec


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,default=None,help='Output HIGH_RE_EXPORT directory; auto-detects a writable SciServer volume when omitted.')
    ap.add_argument('--inspect-only',action='store_true',help='Metadata only; do not read selected field values.')
    args=ap.parse_args()
    print('UNNS JHTDB HIGH-RE SPATIAL GENERALIZATION — FROZEN EXTRACTION v0.1')
    print('Snapshots are independent; no time edges are implied.\n')
    for s in SAMPLES:
        a=zarr.open(str(s['zarr']),mode='r'); verify_array(a,s)
        print(s['dataset'], 'shape=',a.shape,'chunks=',getattr(a,'chunks',None),'dtype=',a.dtype)
    if args.inspect_only:
        print('\n[PASS] metadata only; no selected field values were read.')
        return
    out=(args.output or writable_volume()).resolve()
    out.mkdir(parents=True,exist_ok=True)
    print('\nOutput root:',out)
    manifest={'schema':'UNNS_JHTDB_HIGH_RE_EXPORT_v0.1','created_utc':datetime.now(timezone.utc).isoformat(),'records':[]}
    for s in SAMPLES:
        for snap,role in s['snapshots']:
            manifest['records'].append(write_one(s,snap,role,out))
    mp=out/'EXPORT_MANIFEST.json'; mp.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print('\n[COMPLETE] 7 frozen source samples extracted and hashed.')
    print('Export folder:',out)
    print('Download this folder; do not inspect/reselect samples before the frozen scale analysis.')

if __name__=='__main__': main()
