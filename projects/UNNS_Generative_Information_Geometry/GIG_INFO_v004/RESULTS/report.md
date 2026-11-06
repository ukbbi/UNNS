# GIG-INFO v004 report

## B. exact information profiles (bits) for Y=1[beta2>0]

### D, natural ensemble (H(Y)=0.0057133)

| observation | H(Y|O) | I(Y;O) | classes | mixed |
|---|---|---|---|---|
| none | 0.0057133 | 0.0000000 | 1 | 1 |
| N | 0.0044674 | 0.0012458 | 488 | 59 |
| (N,h1) | 0.0006191 | 0.0050941 | 54921 | 26 |
| (N,h1,hq) | 0.0001836 | 0.0055297 | 60088 | 14 |
| (N,h1,Q) | 0.0002033 | 0.0055099 | 59135 | 16 |
| (Q,S2) | 0.0000000 | 0.0057133 | 55277 | 0 |
| (N,h1,Q,S2) | 0.0000000 | 0.0057133 | 62403 | 0 |
| (N,h1,h2) | 0.0000000 | 0.0057133 | 62531 | 0 |
| (N,E,Q,hx)=f0..f2 | 0.0002971 | 0.0054161 | 49439 | 19 |

### D, balanced ensemble (H(Y)=1.0000000)

| observation | H(Y|O) | I(Y;O) | classes | mixed |
|---|---|---|---|---|
| none | 1.0000000 | 0.0000000 | 1 | 1 |
| N | 0.3913509 | 0.6086490 | 488 | 59 |
| (N,h1) | 0.0116951 | 0.9883048 | 54921 | 26 |
| (N,h1,hq) | 0.0012947 | 0.9987052 | 60088 | 14 |
| (N,h1,Q) | 0.0014030 | 0.9985969 | 59135 | 16 |
| (Q,S2) | 0.0000000 | 1.0000000 | 55277 | 0 |
| (N,h1,Q,S2) | 0.0000000 | 1.0000000 | 62403 | 0 |
| (N,h1,h2) | 0.0000000 | 1.0000000 | 62531 | 0 |
| (N,E,Q,hx)=f0..f2 | 0.0021297 | 0.9978702 | 49439 | 19 |

### D_union_H6, natural ensemble (H(Y)=0.0059336)

| observation | H(Y|O) | I(Y;O) | classes | mixed |
|---|---|---|---|---|
| none | 0.0059336 | 0.0000000 | 1 | 1 |
| N | 0.0048159 | 0.0011177 | 493 | 84 |
| (N,h1) | 0.0006967 | 0.0052369 | 91858 | 48 |
| (N,h1,hq) | 0.0002721 | 0.0056615 | 104147 | 28 |
| (N,h1,Q) | 0.0002848 | 0.0056488 | 101780 | 30 |
| (Q,S2) | 0.0000000 | 0.0059336 | 91644 | 0 |
| (N,h1,Q,S2) | 0.0000000 | 0.0059336 | 109706 | 0 |
| (N,h1,h2) | 0.0000000 | 0.0059336 | 109971 | 0 |
| (N,E,Q,hx)=f0..f2 | 0.0003502 | 0.0055834 | 79486 | 34 |

### D_union_H6, balanced ensemble (H(Y)=1.0000000)

| observation | H(Y|O) | I(Y;O) | classes | mixed |
|---|---|---|---|---|
| none | 1.0000000 | 0.0000000 | 1 | 1 |
| N | 0.4552170 | 0.5447829 | 493 | 84 |
| (N,h1) | 0.0125861 | 0.9874138 | 91858 | 48 |
| (N,h1,hq) | 0.0015940 | 0.9984059 | 104147 | 28 |
| (N,h1,Q) | 0.0016771 | 0.9983228 | 101780 | 30 |
| (Q,S2) | 0.0000000 | 1.0000000 | 91644 | 0 |
| (N,h1,Q,S2) | 0.0000000 | 1.0000000 | 109706 | 0 |
| (N,h1,h2) | 0.0000000 | 1.0000000 | 109971 | 0 |
| (N,E,Q,hx)=f0..f2 | 0.0023014 | 0.9976985 | 79486 | 34 |

## B. out-of-sample (balanced test ensemble)

### train D -> test H6

| model | recovered bits | balanced acc | AUC |
|---|---|---|---|
| N | 0.3065 | 0.7482 | 0.8423 |
| radius1 scalars | 0.2772 | 0.808 | 0.9139 |
| radius1 + squares | 0.4376 | 0.8575 | 0.9604 |
| radius2 scalars | 0.436 | 0.7928 | 0.9613 |
| (Q,S2) only | 0.2894 | 0.8374 | 0.9159 |
| exact lookup | -1.0537 | 0.5731 | - |

### train H6 -> test D

| model | recovered bits | balanced acc | AUC |
|---|---|---|---|
| N | 0.3825 | 0.7971 | 0.8633 |
| radius1 scalars | 0.5159 | 0.8474 | 0.9399 |
| radius1 + squares | 0.6561 | 0.9091 | 0.9758 |
| radius2 scalars | 0.676 | 0.9166 | 0.9787 |
| (Q,S2) only | 0.4474 | 0.8322 | 0.9232 |
| exact lookup | -1.1881 | 0.578 | - |

## A. scope of (Q,S2) sufficiency

| class | systems | positives | (Q,S2) mixed/hidden | (N,h1,Q,S2) mixed/hidden | (N,h1,h2) mixed |
|---|---|---|---|---|---|
| PF | 109906 | 4796 | 60/89 | 24/48 | 0 |
| VS | 30000 | 11373 | 15/15 | 0/0 | 0 |
| arithmetic (D u H6) | 609983 | 290 | 0/0 | 0/0 | 0 |

## C. symbolic grammar

primary: 71 systems, beta2 positives 0
beta1 transfer:
- symbolic SYM-6 stress: N mixed 123 (hidden 10009), (N,h1) mixed 5 (hidden 34), (N,h1,Q) mixed 4 (hidden 27), (Q,S2) mixed 49 (hidden 258), (N,h1,Q,S2) mixed 0 (hidden 0), (N,h1,h2) mixed 0 (hidden 0)
- arithmetic census D: N mixed 262 (hidden 2807), (N,h1) mixed 120 (hidden 233), (N,h1,Q) mixed 13 (hidden 40), (Q,S2) mixed 132 (hidden 207), (N,h1,Q,S2) mixed 0 (hidden 0), (N,h1,h2) mixed 0 (hidden 0)
