# Original user-provided verification scripts

`geo_hd_1_check.py` and `geo_hd_1_check_factorization.py` are copied **without alteration** from the conversation uploads. They require `sympy` (`python -m pip install sympy`) and were reported to verify, respectively, the initial arithmetic and 43,376 edges with source m<=5000.

The new `RUN_CHECKS.py` uses its own standard-library tests so it can work without installing SymPy. Execute the original full sweep separately for stronger computational coverage.
