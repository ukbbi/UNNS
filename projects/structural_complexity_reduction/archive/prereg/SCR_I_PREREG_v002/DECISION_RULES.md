# Frozen decision rules

Cell verdicts are evaluated in this order:

1. `INDETERMINATE_NO_TARGETS` if the baseline target count is zero.
2. `TARGET_LOSS` if target recall is not exactly 1.0.
3. `NO_WORK_REDUCTION` if downstream evaluation reduction is not positive.
4. `NET_SLOWDOWN` if neither measured time gain nor the preregistered operation proxy exceeds 1.
5. `SCR_CALIBRATION_SUPPORTED` only if all previous failures are absent.

Project-level support requires all 15 primary cells to avoid target loss and to preserve exact identity. A large pruning fraction never compensates for a lost target.
