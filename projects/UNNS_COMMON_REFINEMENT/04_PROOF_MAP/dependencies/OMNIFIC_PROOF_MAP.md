# Conway Proof Architecture — UNNS Extraction Map

## Source basis

This map is based on the public `gaearon/conway-refinement` proof guide and README.
The repository itself states that it is a candidate proof and that specialist review of the
formal statement correspondence remains important.

This file therefore distinguishes:
- **documented proof nodes** — named in the public proof map;
- **UNNS role** — our interpretation of what structural function that node serves.

---

## A. Independence layer

### Proof phases
- Cantor–Bendixson ranks of supports
- Algebraic independence in graded rings
- Principal RV-elements
- Polynomial presentations

### Structural role
Replace the finite affine requirement that primitive factor directions be independent.

### UNNS role
**I — Local Independence**

The finite invariant `ARD=0` is replaced by a local/graded statement:
the relevant leading structural classes can be treated as independent coordinates.

---

## B. Prime-traceability layer

### Documented nodes
- (180) Primality for finitely many Archimedean classes
- (181) Primality of reduced omnific integers outside Z
- (182) Irreducible omnific integers are prime

### Structural role
Ensure that an irreducible structural component cannot be absorbed invisibly by a product.

### UNNS role
**P — Prime Traceability**

This is the closest direct continuation of the affine theorem.

---

## C. Descent layer

### Documented nodes
- (152) Strict decrease of support-class order type
- (153) Factorisation at a quotient Archimedean class
- (157) Refinement at a quotient Archimedean class
- (158) Transfinite extension of finite-class primality

### Structural role
Replace finite termination by a well-founded transfinite complexity decrease.

### UNNS role
**D — Well-Founded Descent**

The proof can recurse through support classes without an infinite uncontrolled regress.

---

## D. Limit-closure layer

### Documented nodes
- (176) Cofinality of common surreal Archimedean tails
- (177) Fraction fields of surreal common-tail integer parts
- (184) A coinitial family of positive elements in surreal common-tail quotients
- (185) Cauchy completeness of surreal common-tail quotients

### Structural role
Keep the factor/refinement construction closed when infinitely many lower stages accumulate.

### UNNS role
**L — Limit Closure**

This is genuinely absent from the finite affine theorem.

---

## E. Reconstruction / global closure

### Documented nodes
- (179) Signed normal-form isomorphism for omnific integers
- (186) Primality of the surreal Hahn integer part
- (187) Refinement property of Oz_u
- (188) Conway's refinement theorem for omnific integers

### Structural role
Transfer the series-level structure back into the omnific integer object and obtain the
headline four-factor refinement.

### UNNS role
**R — Reconstruction**

---

# Condensed dependency picture

```text
SUPPORT / CB RANK
        |
        v
GRADED INDEPENDENCE
        |
        v
POLYNOMIAL PRESENTATION
        |
        v
FINITE-CLASS PRIMALITY
        |
        v
IRREDUCIBLE -> PRIME
        |
        +-------------------+
        |                   |
        v                   v
STRICT ORDER-TYPE       COMMON-TAIL
DESCENT                 COMPLETENESS
        |                   |
        +---------+---------+
                  |
                  v
       HAHN INTEGER-PART
            PRIMALITY
                  |
                  v
          Oz REFINEMENT
                  |
                  v
      CONWAY FOUR-FACTOR
           THEOREM
```

This is not a replacement for the Lean dependency graph. It is the smallest structural map
needed for the UNNS comparison.
