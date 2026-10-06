# YM3B_RESULT.md

## UNNS Yang-Mills Gap / Vacuum Boundary Non-Crossability
### YM-3B Class B measured-data refinement result

**Source:** Sakai & Sasaki (2023)  
**Evidence class:** B - published effective-mass reconstructions  
**Frozen chamber:** CORR-I v0.1.2  
**Chamber SHA-256:** `f972c9d460cebc19ef165e66c03f971411062eba093876406ed2efe614e2deb2`  
**Hash matches preregistration:** **True**  
**Frozen-rule verdict:** **DATA-INDETERMINATE**

## 1. Primary four-beta result

| beta | R_B | R_p8 matched | S_B=log10(R_p8/R_B) | PCHIP S_B |
|---:|---:|---:|---:|---:|
| 6.20 | 0.088575860 | 0.092825100 | 0.020350 | 0.019648 |
| 6.40 | 0.082775197 | 0.089901538 | 0.035867 | 0.036198 |
| 6.71 | 0.092699571 | 0.091977820 | -0.003395 | -0.003948 |
| 6.93 | 0.082333274 | 0.092774114 | 0.051851 | 0.052060 |

The matched Gamma ordering test uses `p = 0.5, 1, 2, 4, 8` at every beta.
Full matched ordering passes at every beta: **False**.

## 2. R3 nested-ladder sensitivity

| beta | L5 S_B | L6 S_B | L7 S_B |
|---:|---:|---:|---:|
| 6.20 | 0.010186 | 0.014667 | 0.020350 |
| 6.40 | 0.019249 | 0.027185 | 0.035867 |
| 6.71 | -0.007663 | -0.006666 | -0.003395 |
| 6.93 | 0.037860 | 0.046615 | 0.051851 |

## 3. 2,000-draw no-covariance sensitivity

| beta | 2.5% | median S_B | 97.5% | fraction S_B>0 |
|---:|---:|---:|---:|---:|
| 6.20 | 0.004053 | 0.020325 | 0.035659 | 0.9955 |
| 6.40 | 0.017167 | 0.035606 | 0.053094 | 1.0000 |
| 6.71 | -0.027454 | -0.003285 | 0.019320 | 0.3935 |
| 6.93 | 0.024726 | 0.052621 | 0.081194 | 1.0000 |

## 4. Frozen-rule interpretation

The central primary analysis produces a small negative boundary coordinate at beta = 6.71, while beta = 6.20, 6.40, and 6.93 remain positive.
The beta = 6.71 sign is unchanged by the preregistered PCHIP interpolation and is also negative at R3-L5, R3-L6, and R3-L7.
However, the preregistered 2,000-draw pointwise-no-covariance sensitivity ensemble spans both signs at beta = 6.71. Its 95% central interval crosses zero.

Under the frozen `DATA-INDETERMINATE` clause, digitization/statistical uncertainty therefore dominates the sign of the only central crossing.

> **DATA-INDETERMINATE**

This does not erase the central crossing. It means that the available published-figure precision is insufficient to classify that crossing as a stable data-refinement failure.

## 5. Claim boundary

This is a Class B published-effective-mass reconstruction test. It is stronger than the completed Class C model-refinement test, but it is not based on raw author correlator matrices or full covariance and it does not prove or disprove the Yang-Mills mass gap.
