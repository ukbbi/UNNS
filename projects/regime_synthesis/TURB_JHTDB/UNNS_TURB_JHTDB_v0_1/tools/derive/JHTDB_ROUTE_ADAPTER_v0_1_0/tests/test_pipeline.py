from pathlib import Path
import json
import numpy as np
import h5py

from jhtdb_adapter.pipeline import run_adapter


def _make_vortex_h5(path: Path):
    n = 32
    L = 2.0
    coords = np.linspace(0, L, n, dtype=np.float32)
    z,y,x = np.meshgrid(coords,coords,coords,indexing="ij")

    with h5py.File(path, "w") as f:
        f["xcoor"] = coords
        f["ycoor"] = coords
        f["zcoor"] = coords
        f.attrs["t_start"] = 1
        f.attrs["t_end"] = 3
        f.attrs["t_step"] = 1
        for ti in range(3):
            shift = 0.02*ti
            xc, yc = 1.0+shift, 1.0
            xx=x-xc; yy=y-yc; zz=z-1.0
            r2=xx*xx+yy*yy
            # Localize the synthetic vortex in z as well so it does not touch
            # the retained-interior z faces and get correctly rejected as a
            # boundary-truncated structure.
            g=np.exp(-r2/0.12 - zz*zz/0.20).astype(np.float32)
            v=np.zeros((n,n,n,3),dtype=np.float32)
            v[...,0]=(-yy*g).astype(np.float32)
            v[...,1]=( xx*g).astype(np.float32)
            f[f"Velocity_{ti+1:04d}"] = v


def test_small_end_to_end(tmp_path):
    project=tmp_path/"project"
    src=project/"data/raw/jhtdb/isotropic1024coarse/cutouts"
    src.mkdir(parents=True)
    h5=src/"isotropic1024-coarse-velocity.h5"
    _make_vortex_h5(h5)

    cfg={
      "adapter":{"name":"TEST","version":"0","pilot":"testpilot"},
      "source":{
        "relative_path":"data/raw/jhtdb/isotropic1024coarse/cutouts/isotropic1024-coarse-velocity.h5",
        "dataset":"synthetic","expected_sha256":None,"validate_sha256":False,
        "axis_order":"zyxc","velocity_components":["u_x","u_y","u_z"],
        "stored_dt":0.002,"cutout_time_index_origin":1,"viscosity":0.000185
      },
      "scales":{"block_factors":[1,2,4],"method":"exact_nonoverlapping_block_mean"},
      "boundary":{"margin_native_cells":4,"discard_touching_objects":True},
      "segmentation":{"field":"Q","mode":"q_rms","q_rms_multiplier":0.5,
                      "connectivity":26,"min_native_voxels":4,"min_coarse_voxels":1},
      "relations":{"candidate_rule":"positive_voxel_overlap_only","confidence":"overlap_src",
                   "eligibility":{"mode":"any","conditions":[
                       {"column":"overlap_src","op":">=","value":0.05}
                   ]}},
      "route_i":{"edge_weight_column":"confidence","object_weight_column":"weight",
                 "nulls":{"count":20,"seed":1,"swaps_per_edge":3,
                          "mobility":{"min_mean_fraction":0.01,
                                      "min_unique_graph_fraction":0.1,
                                      "max_real_match_fraction":0.9}},
                 "inference":{"alpha":0.05,"min_nulls":20}},
      "reference":{"energy_history_relative_path":"data/source/ener_Re_time.txt"}
    }
    cfgp=tmp_path/"cfg.json"
    cfgp.write_text(json.dumps(cfg),encoding="utf-8")

    report=run_adapter(cfgp,project_root=project,skip_hash=True,progress=lambda x:None)
    assert report["status"]=="COMPLETE"
    assert report["result"]["objects"]>0
    assert report["result"]["relation_candidates"]>0
    assert (project/"outputs/records/JHTDB_PILOT_A_ROUTE.zip").exists()
    derived = project/"data/derived/objects/testpilot"
    assert (derived/"objects.parquet").exists() or (derived/"objects.csv").exists()
    assert (derived/"relations.parquet").exists() or (derived/"relations.csv").exists()
