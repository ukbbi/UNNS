import numpy as np
import pandas as pd

# Load DESI dataset
df = pd.read_csv("cw_desi_xyz_sample.csv")

x = df["x"].values
y = df["y"].values
z = df["z"].values

# Compute radius of each galaxy
r = np.sqrt(x*x + y*y + z*z)

N = len(r)

# Random angular positions
u = np.random.rand(N)
v = np.random.rand(N)

theta = np.arccos(2*u - 1)
phi = 2*np.pi*v

# Convert back to Cartesian coordinates
xs = r*np.sin(theta)*np.cos(phi)
ys = r*np.sin(theta)*np.sin(phi)
zs = r*np.cos(theta)

synthetic = pd.DataFrame({
    "x": xs,
    "y": ys,
    "z": zs
})

synthetic.to_csv("cw_desi_synthetic_xyz.csv", index=False)

print("Synthetic dataset created:")
print("cw_desi_synthetic_xyz.csv")