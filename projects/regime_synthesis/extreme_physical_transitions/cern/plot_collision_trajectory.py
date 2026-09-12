import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("unns_collision_trajectory.csv")

plt.figure(figsize=(10,5))
plt.plot(df["t"], df["signal"], linewidth=1)

plt.title("Collision Trajectory (UNNS Form)")
plt.xlabel("t (event index)")
plt.ylabel("signal (energy / mass)")
plt.grid(True)

plt.show()