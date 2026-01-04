# UNNS-ADM — Admissibility Framework (Standards)

This directory contains the **normative methodological standards** governing
admissibility, registry handling, enforcement, and failure preservation in UNNS
research.

These documents define **infrastructure and constraints**.  
They are **not analytical results** and **not part of the chamber system**.

All UNNS analyses and chambers implicitly assume compliance with UNNS-ADM.

---

## Canonical UNNS-ADM Stack

┌───────────────────────────────────────────────┐
│ UNNS-ADM-C │
│ Negative Space Catalog │
│ │
│ • All inadmissible structures │
│ • Failure modes are classified & preserved │
│ • No deletion, no reinterpretation │
│ • Boundary of analyzability │
└───────────────────────────────────────────────┘

┌───────────────────────────────────────────────┐
│ UNNS-ADM │
│ Admissibility Theory (Axioms A1–A7) │
│ │
│ • Defines admissibility │
│ • Separates admissibility from observables │
│ • No execution, no registry, no analysis │
└───────────────────────────┬───────────────────┘
│ governs
▼
┌───────────────────────────────────────────────┐
│ UNNS-ADM-B │
│ Empirical Candidate Registry │
│ (Specification) │
│ │
│ • Records admissibility verdicts │
│ • Stores justifications & protocols │
│ • Immutable, versioned, auditable │
│ • Contains BOTH admissible and inadmissible │
└───────────────────────────┬───────────────────┘
│ realized by
▼
┌───────────────────────────────────────────────┐
│ UNNS-ADM-A │
│ Technical Realization Layer │
│ │
│ A.1 Identifier & Persistence │
│ A.2 Compliance Validation Interface │
│ A.3 Query & Audit Interface │
│ │
│ • No theory │
│ • No admissibility decisions │
│ • Mechanical enforcement only │
└───────────────────────────┬───────────────────┘
│ gates
▼
┌───────────────────────────────────────────────┐
│ Instrumental Analysis Layer │
│ (Chambers XII–XXXII and beyond) │
│ │
│ • Operators, simulations, measurements │
│ • Must reference ADM-B entry IDs │
│ • Cannot redefine admissibility │
│ • Rejected if ADM-A.2 non-compliant │
└───────────────────────────────────────────────┘


---

## Contents

- **UNNS-ADM**  
  *Admissibility of Recursive Structures in the UNNS Substrate*  
  Foundational theory defining admissibility axioms A1–A7.

- **UNNS-ADM-B**  
  *Empirical Candidate Registry*  
  Normative specification for recording admissibility determinations.

- **UNNS-ADM-A**  
  *Technical Realization of the UNNS Admissibility Framework*  
  Mechanical enforcement layer.
  - A.1 Identifier & Persistence  
  - A.2 Compliance Validation Interface  
  - A.3 Query & Audit Interface  

- **UNNS-ADM-C**  
  *Negative Space Catalog*  
  Normative treatment of inadmissible structures and failure preservation.

- **Methodological Guarantees of the UNNS Admissibility Framework**  
  External-facing summary of the guarantees provided by UNNS-ADM.

- **BRIDGE.md**  
  Orientation and chamber consolidation document linking ADM to the UNNS chamber ecosystem.

---

## Scope and Usage

- UNNS-ADM documents **do not execute**, **do not analyze**, and **do not evaluate results**.
- Chambers and analytical tools must operate **downstream** of UNNS-ADM.
- These standards are intended to be **stable, citable, and auditable**.

Revisions occur only through explicit versioned updates.

---

## Status

Current status: **Frozen (v1.0)**  
Any future changes will result in a new version series.

