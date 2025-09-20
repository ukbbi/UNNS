import numpy as np
import matplotlib.pyplot as plt
from diagnostics import residues, upi
from repair_operators import proofreading, excision_refit, global_renormalization

def generate_fibonacci(n):
    u = [0,1]
    for _ in range(2,n):
        u.append(u[-1] + u[-2])
    return np.array(u, dtype=float)

# Build corrupted Fibonacci
u = generate_fibonacci(40)
coeffs = [1.0, 1.0]
u[20] += 50   # inject corruption

print("Initial UPI:", upi(1.2,1.1,0.9,0.8))
print("Max residue before repair:", np.max(np.abs(residues(u, coeffs))))

# Repair with proofreading on flagged indices
for i in range(len(u)):
    if abs(residues(u, coeffs)[i]) > 1e-6:
        u = proofreading(u, coeffs, i, eta=0.8)

# Optional global renormalization
u = global_renormalization(u)

print("Max residue after repair:", np.max(np.abs(residues(u, coeffs))))

# Plot
plt.plot(u, 'o-', label="Repaired UNNS")
plt.legend()
plt.title("UNNS Repair Demo (Proofreading + Renormalization)")
plt.show()
