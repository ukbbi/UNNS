┌───────────────────────────────────────────────┐
│               UNNS-ADM                        │
│   Admissibility Theory (Axioms A1–A7)         │
│                                               │
│   • Defines admissibility                     │
│   • Separates admissibility from observables  │
│   • No execution, no registry, no analysis    │
└───────────────────────────┬───────────────────┘
                            │ governs
                            ▼
┌───────────────────────────────────────────────┐
│               UNNS-ADM-B                      │
│   Empirical Candidate Registry (Specification)│
│                                               │
│   • Records admissibility verdicts            │
│   • Stores justifications & protocols         │
│   • Immutable, versioned, auditable           │
│   • Contains BOTH admissible and inadmissible │
└───────────────────────────┬───────────────────┘
                            │ realized by
                            ▼
┌───────────────────────────────────────────────┐
│               UNNS-ADM-A                      │
│   Technical Realization Layer                 │
│                                               │
│   A.1 Identifier & Persistence                │
│   A.2 Compliance Validation Interface         │
│   A.3 Query & Audit Interface                 │
│                                               │
│   • No theory                                 │
│   • No admissibility decisions                │
│   • Mechanical enforcement only               │
└───────────────────────────┬───────────────────┘
                            │ gates
                            ▼
┌───────────────────────────────────────────────┐
│         Instrumental Analysis Layer            │
│        (Chambers XII–XXXII and beyond)         │
│                                               │
│   • Operators, simulations, measurements      │
│   • Must reference ADM-B entry IDs             │
│   • Cannot redefine admissibility             │
│   • Rejected if ADM-A.2 non-compliant          │
└───────────────────────────────────────────────┘
