---
license: mit
dataset_creator:
- Johns Hopkins Turbulence Database (JHTDB) Team
annotations_creators:
- no-annotation
task_categories:
- other
size_categories:
- 1B<n<10B
source_datasets: >-
  Johns Hopkins Turbulence Database (full access at
  https://turbulence.idies.jhu.edu)
---

<!-- task_categories:
- scientific
- turbulence
- computational-fluid-dynamics -->

# Johns Hopkins Turbulence Database


👉 **Please visit:** https://turbulence.idies.jhu.edu

There you will find:

- **Homogeneous Turbulence**: Isotropic 1024³, 2048³, 4096³, 8192³ and 32768³
- **Wall-Bounded Turbulence**: Channel Flow & Transitional Boundary Layer
- **Geophysical**
- **Wind Farm Simulations**

**You will also be able to access these datasets in their full size, unlike the subset presented in this HuggingFace dataset**

## What is in this HuggingFace Dataset?

This repository hosts a *small* 3-D snapshot (256³ grid points) extracted from the publicly available **Johns Hopkins Turbulence Database (JHTDB)**, meant for quick experimentation, tutorials, benchmarking, and as a lightweight entry point before connecting to the full database.

* `DEMO_HF_Getdata_local.ipynb`  
  - Notebook used to generate the below data.
  - Example Use case of our JHTDB library, and testing token included


* `isotropic_1024_coarse_pressure.h5`  
  - shape: `(256, 256, 256, 1, 10)` - 256³ across 10 timesteps
  - fields: `p` - pressure
  - dtype: `float32`
  - data format: hdf5
  - size: 688 MB


* `isotropic_1024_coarse_velocity.h5`  
  - shape: `(256, 256, 256, 3, 10)` - 256³ across 10 timesteps, 3 fields
  - fields: `u,v,w` - three velocity direction components
  - dtype: `float32`
  - data format: hdf5
  - size: 2.02 GB


<!-- ## Dataset structure -->

<!-- Provide a quick summary of the dataset. -->

### Dataset Description


Direct numerical simulation (DNS) using 1,024³ nodes. Only 256³ is present in the HuggingFace files.

✪ Navier-Stokes is solved using pseudo-spectral method.

✪ Energy is injected by keeping constant the total energy in shells such that |k| is less or equal to 2.

✪ After the simulation has reached a statistical stationary state, 5,028 frames of data with 3 velocity components and pressure are stored in the database. Extra time frames at the beginning and at the end have been added to be used for temporal-interpolations.

✪ The Taylor-scale Reynolds number fluctuates around Rλ~ 433.

✪ There is one dataset ("coarse") with 5028 timesteps available, for time t between 0 and 10.056 (the frames are stored at every 10 time-steps of the DNS). Intermediate times can be queried using temporal-interpolation.

✪ There is another dataset ("fine") that stores every single time-step of the DNS, for testing purposes. Times available are for t between 0.0002 and 0.0198.

✪ A table with the time history of the total kinetic energy and Taylor-scale Reynolds number as function of time can be downloaded from this text file.

✪ Radial spectrum E(k) averaged over time can be downloaded from this text file.

<!-- Provide the basic links for the dataset. -->

- **[Direct Numerical Simulation Description](https://turbulence.idies.jhu.edu/datasets/homogeneousTurbulence/isotropic)**
- **[Paper](https://turbulence.idies.jhu.edu/docs/isotropic/README-isotropic.pdf)**

- **Curated by:** Johns Hopkins University
- **Funded by:** National Science Foundation

<!-- ## Uses -->

<!-- Address questions around how the dataset is intended to be used. -->



<!-- ### Direct Use

<!-- This section describes suitable use cases for the dataset. -->