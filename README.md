 UNNS Many-Faces Theorem: Interactive Visualization & Formal Framework

A mathematical framework and interactive visualization tool for exploring the Unbounded Nested Number Sequences (UNNS) system and its Many-Faces Theorem, demonstrating how diverse mathematical sequences emerge from a unified computational substrate.

 🌟 Overview

The UNNS (Unbounded Nested Number Sequences / Universal Network Nexus System) framework provides a unified approach to understanding linear recurrence sequences, their geometric attractors, modular properties, and cross-domain mappings. This repository contains:

- Interactive HTML5 visualization tool with 2D/3D graphics
- Formal theorem statements and proof sketches (PDF documents)
- Python verification scripts for numerical analysis
- Constructive embeddings for classic sequences (Fibonacci, Pell, Tribonacci, etc.)

 📚 The Many-Faces Theorem

The core theoretical result shows that a single UNNS system can simultaneously exhibit multiple mathematical "faces":

 Theorem Statement
Let U = (S, C, G, {μ_D}) be a UNNS system where:
- **S** = set of nests (symbolic tokens or integers)
- **C** = finite set of combinators (bounded-lookback operators)
- **G** = finite seed set
- **μ_D** = computable domain mappings

Then the system exhibits:

1. **Linear Recurrence Embedding**: Any linear recurrence a_n = c₁a_{n-1} + ... + c_r a_{n-r} can be exactly embedded
2. **Dominant-Root Attractor**: Convergence to the characteristic polynomial's dominant eigenvalue
3. **Modular Domain Partition**: Residue classes mod m create finite-state subsystems
4. **Cross-Domain Homomorphism**: Constructive mappings between different encodings
5. **Computational Completeness**: With appropriate combinators, Turing completeness is achievable

 🚀 Quick Start

 Interactive Visualization
1. Download `unns_many_faces.html`
2. Open in any modern web browser (Chrome, Firefox, Safari, Edge)
3. No server or installation required!

 Features
- 13 pre-programmed sequences (Fibonacci, Lucas, Pell, Jacobsthal, Tribonacci, etc.)
- Custom sequence builder
- Real-time 2D spiral and 3D helical visualizations
- Modular arithmetic analysis
- Ratio convergence tracking
- JSON/CSV export for data analysis

 🔬 Mathematical Sequences Included

| Sequence | Recurrence | Dominant Root | Special Property |
|----------|------------|---------------|------------------|
| Fibonacci | F(n) = F(n-1) + F(n-2) | φ ≈ 1.618 | Golden ratio |
| Lucas | L(n) = L(n-1) + L(n-2) | φ ≈ 1.618 | Fibonacci companion |
| Pell | P(n) = 2P(n-1) + P(n-2) | 1+√2 ≈ 2.414 | Silver ratio |
| Jacobsthal | J(n) = J(n-1) + 2J(n-2) | 2 | Binary connections |
| Tribonacci | T(n) = T(n-1) + T(n-2) + T(n-3) | ≈ 1.839 | 3D spiral |
| Padovan | P(n) = P(n-2) + P(n-3) | ≈ 1.324 | Plastic constant |
| ... | ... | ... | ... |

<img width="516" height="369" alt="image" src="https://github.com/user-attachments/assets/d92cb387-0e50-4490-8431-f625ef5cb14d" />


 💻 Python Verification

```python
 Example: Verify Fibonacci convergence
import json
from verify_convergence import verify_unns_convergence

with open('unns_fibonacci_50.json', 'r') as f:
    data = json.load(f)
    results = verify_unns_convergence(data)
    print(f"Convergence error: {results['final_error']:.2e}")
    print(f"Dominant root: {results['dominant_root']:.10f}")
🔧

🔧 Technical Implementation
UNNS Combinator Example (Fibonacci)
S = ℤ (integers)
G = {0, 1} (seeds)
C = {★} where ★(x,y) = x + y
μ_Z: S → ℤ (identity mapping)

Sequence generation:
s₀ = 0, s₁ = 1
s_{n+1} = ★(s_{n-1}, s_n) = s_{n-1} + s_n
Technologies Used

Frontend: HTML5, Canvas API, Three.js for 3D
Computation: Pure JavaScript for sequence generation
Visualization: 2D Canvas for charts, WebGL for 3D spiral
Export: JSON for data, CSV for spreadsheets

🤝 Contributing
Contributions are welcome! Areas of interest:

New Sequences: Add more recurrence relations
Proof Formalization: Lean 4 or Coq implementations
Performance: Optimize for very large terms
Visualizations: Additional geometric embeddings
Documentation: Improve mathematical explanations

Please see CONTRIBUTING.md for guidelines.
📊 Research Applications
This framework has potential applications in:

Number theory and combinatorics
Dynamical systems analysis
Cryptographic sequence generation
Pattern recognition in biological systems
Architectural proportion analysis
Educational tools for discrete mathematics

🎓 Educational Use
Perfect for:

Undergraduate discrete mathematics courses
Graduate seminars on recurrence relations
Research into sequence properties
Interactive demonstrations of convergence
Exploring modular arithmetic patterns

📖 References

Original UNNS Framework: [Initial formulation and proofs]
Binet's Formula: Closed-form expression for Fibonacci numbers
Characteristic Polynomials: Eigenvalue analysis of recurrence relations
Pisano Periods: Modular repetition in Fibonacci sequences

🚧 Future Work

 Formal proof verification in Lean 4
 WebAssembly optimization for large sequences
 Machine learning pattern detection
 Non-linear recurrence support
 Symbolic computation integration
 Mobile app version

📝 License
MIT License - See LICENSE file for details
🙏 Acknowledgments
Thanks to the mathematical community, which has explored sequences for centuries, from Fibonacci (1202) to modern computational approaches.
📧 Contact
For questions, suggestions, or collaboration:

Open an issue on GitHub
Contribute to discussions
Submit pull requests


"Many faces, one framework" - The beauty of mathematical unity in diversity

This README provides:
- Clear project overview
- Mathematical context without overwhelming detail
- Practical usage instructions
- Technical implementation details
- Contribution guidelines
- Future research directions
- Professional presentation suitable for academic or developer audiences
