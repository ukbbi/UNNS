# UPI for Developers — API & Integration Guide

This document is a **developer-oriented guide** for working with the  
**UNNS Paradox Index (UPI)** outside the interactive chambers.

It explains a reference API shape you can use when:

- embedding UPI logic into your own tools
- generating JSON logs compatible with Chamber XXIII
- scripting batch experiments
- integrating UPI with other numerical engines

> Note: the exact internal implementation may differ per chamber.
> This guide describes the *intended* public interface and data
> contracts that other code should rely on.

---

## 1. Core Idea

At the code level, UPI is:

- a function that accepts a **numeric sequence** and a **configuration**
- an engine that returns a **structured diagnostics object**

Conceptually:

```text
sequence: number[]  +  config: UPIConfig
           ↓
     UPI Diagnostics Engine
           ↓
     UPIRunResult (JSON-serializable)
You can implement this pattern in any language.
Below we use TypeScript-style pseudocode for clarity.

2. Reference Types
2.1 UPIConfig
ts

type ZoneMode = "standard";  // future: "experimental", etc.

interface UPIConfig {
  maxSteps?: number;            // hard cutoff, default: sequence length
  sobtraSensitivity?: number;   // [0, 1] slider value
  noiseAmplitude?: number;      // ε term for robustness
  zoneMode?: ZoneMode;          // α/β/γ/δ mode profile
  enableOperators?: boolean;    // toggle XIII–XXI metrics
  strictValidation?: boolean;   // throw on NaN / infinities
}
2.2 PSC & Zone Types
ts

type PSCClass = "A" | "B" | "C" | "D" | "E" | "F";

type ZoneLabel = "ALPHA" | "BETA" | "GAMMA" | "DELTA";
type CollapseChannel = "NONE" | "SOBRA" | "SOBTRA";
2.3 Operator Metrics (XIII–XXI)
ts

interface OperatorMetrics {
  XIII_phaseSpikes?: {
    count: number;
    warning: boolean;
    threshold: number;
  };
  XIV_phiCompatibility?: {
    matches: number;
    totalPairs: number;
    compatibilityPct: number;   // 0–100
  };
  XVI_closureEvents?: {
    count: number;
  };
  XVII_semanticLevel?: {
    level: "Weak" | "Moderate" | "Strong";
    motifs: number;
  };
  XXI_tauCurvature?: {
    peaks: number;
    meanTau: number;
  };
}
2.4 Main Result: UPIRunResult
ts

interface UPIRunResult {
  // 1) Basic run info
  meta: {
    version: string;          // e.g. "UPI-1.3.0"
    system: string;           // "CustomData", "Collatz_3n+1", etc.
    maxSteps: number;
    sobtraSensitivity: number;
    noiseAmplitude: number;
    timestamp: string;        // ISO8601
  };

  // 2) Core sequence & UPI
  sequence: number[];         // original x(n)
  upiTimeline: number[];      // UPI(n) per step (length <= sequence.length)

  // 3) Phase & collapse diagnostics
  zones: ZoneLabel[];         // α/β/γ/δ labels per step
  collapseChannels: CollapseChannel[];  // Sobra/Sobtra/None

  // 4) Summary statistics
  summary: {
    pscClass: PSCClass;
    currentStep: number;
    maxUPI: number;
    alphaSteps: number;
    betaSteps: number;
    gammaSteps: number;
    deltaSteps: number;
    sobraCollapses: number;
    sobtraCollapses: number;
    firstParadoxStep?: number | null;
  };

  // 5) Advanced operator diagnostics
  operators?: OperatorMetrics;

  // 6) Export-friendly block
  advancedMetrics?: any;   // reserved for chamber-specific extras
}
3. Reference API Shape
3.1 Engine Class
ts

class UPIDiagnosticsEngine {
  constructor(config?: UPIConfig);

  run(sequence: number[]): UPIRunResult;

  // Optional: convenience helpers:
  runFromCSV(csvText: string): UPIRunResult;
  toJSON(result: UPIRunResult): string;
}
3.2 Minimal Usage Example (JS/TS)
ts

import { UPIDiagnosticsEngine } from "./upi_engine";

const engine = new UPIDiagnosticsEngine({
  sobtraSensitivity: 0.70,
  maxSteps: 200,
  enableOperators: true
});

const seq = [1, 2, 4, 8, 16, 32, 64, 128];
const result = engine.run(seq);

console.log("PSC:", result.summary.pscClass);
console.log("Max UPI:", result.summary.maxUPI);
console.log("Zones:", result.zones.join(","));
4. JSON Export Contract
When integrating with Chamber XXIII or other UNNS tools,
stick to this JSON structure:

json

{
  "meta": { ... },
  "sequence": [ ... ],
  "upiTimeline": [ ... ],
  "zones": [ "ALPHA", "BETA", "GAMMA", "DELTA" ],
  "collapseChannels": [ "SOBRA", "SOBTRA", "NONE" ],
  "summary": {
    "pscClass": "C",
    "currentStep": 99,
    "maxUPI": 1274,
    "alphaSteps": 2,
    "betaSteps": 3,
    "gammaSteps": 3,
    "deltaSteps": 92,
    "sobraCollapses": 0,
    "sobtraCollapses": 85,
    "firstParadoxStep": 3
  },
  "operators": {
    "XIII_phaseSpikes": { "count": 88, "warning": true, "threshold": 1.5 },
    "XIV_phiCompatibility": {
      "matches": 0,
      "totalPairs": 98,
      "compatibilityPct": 0.0
    },
    "XVI_closureEvents": { "count": 8 },
    "XVII_semanticLevel": { "level": "Moderate", "motifs": 8 },
    "XXI_tauCurvature": { "peaks": 22, "meanTau": 3.8776 }
  },
  "advancedMetrics": { }
}
If you keep this schema:

Chamber XXIII can import your logs in the future

other scripts can process runs in a uniform way

you can compare results across languages and engines

5. Data Preparation Rules
To keep the engine stable:

Numeric only

Input must be finite numbers

Non-numeric tokens should be dropped or cause an error if strictValidation = true

Length constraints

Minimum: 3 values (need curvature)

Recommended upper bound: ~10,000 points for interactive tools

CSV ingestion
A simple pre-parser is enough:

ts

function parseCSVToSequence(csvText: string): number[] {
  return csvText
    .split(/[\s,;]+/)
    .map(t => t.trim())
    .filter(t => t.length > 0)
    .map(Number)
    .filter(v => Number.isFinite(v));
}
Determinism
For reproducible experiments, avoid random perturbations unless
you control the seed in your own code.

6. Mapping to Chamber XXIII Panels
If your engine returns UPIRunResult, the fields map naturally:

Field	Chamber XXIII Panel / Feature
upiTimeline[]	UPI Timeline (log/linear)
zones[]	Colored phase bands (α/β/γ/δ)
collapseChannels[]	Collapse Strip & CCM
summary.pscClass	PSC badge in Diagnostics Summary
summary.*Steps	Zone counts in summary cards
summary.sobraCollapses	Sobra counter
summary.sobtraCollapses	Sobtra counter
operators.XIII_*	Operator XIII box in Advanced Diagnostics
operators.XIV_*	Operator XIV box
operators.XVI_*	Operator XVI box
operators.XVII_*	Operator XVII box
operators.XXI_*	Operator XXI box

As long as you populate these fields, the UI side can be decoupled from the
numeric implementation.

7. Extending the API
You can safely extend the engine with:

additional experimental operator metrics

alternative zone models

extra per-step diagnostics

Recommended pattern:

ts

interface UPIRunResult {
  ...
  experimental?: {
    [key: string]: any;
  };
}
This keeps the core schema stable while allowing new research features.

8. Example: Batch Experiment Script (Node / Deno)
ts

import { readFileSync, writeFileSync } from "fs";
import { UPIDiagnosticsEngine } from "./upi_engine";

const engine = new UPIDiagnosticsEngine({
  sobtraSensitivity: 0.65,
  enableOperators: true,
  strictValidation: true
});

function runCSV(path: string) {
  const raw = readFileSync(path, "utf8");
  const seq = raw
    .split(/[\s,;]+/)
    .map(t => t.trim())
    .filter(t => t.length > 0)
    .map(Number)
    .filter(v => Number.isFinite(v));

  const result = engine.run(seq);
  const outPath = path.replace(/\.csv$/i, "_upi.json");
  writeFileSync(outPath, JSON.stringify(result, null, 2), "utf8");
  console.log("Written:", outPath, "PSC =", result.summary.pscClass);
}

// Example: process all macro CSVs
["us_inflation.csv", "eu_inflation.csv", "japan_inflation.csv"].forEach(runCSV);
This kind of script makes it easy to feed UPI results into other tools or
visualization frameworks.

9. Implementation Notes & Recommendations
Keep the public interface stable; evolve internals freely.

Always include a meta.version string for compatibility.

Use unit tests on:

PSC classification

zone counts

collapse counts

operator metrics on known test sequences

Make sure your engine behaves well on:

monotone sequences

random noise

oscillatory sequences

mixed-regime synthetic data

10. Roadmap Ideas
Some future developer-facing extensions:

Typed UPI SDK (@unns/upi-core)

WASM builds for high-performance environments

Python wrapper (pip install unns-upi)

Rust/Julia bindings for numerical work

Direct integration with macro CSV sources (FRED / OECD / World Bank)