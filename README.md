# The Five-Bit Threshold for Universal Computation

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Abstract

We prove that under natural encodings, every universal computational system requires at least 5 bits of descriptive complexity. The proof proceeds by capability decomposition: we show that universal computation requires four independent capabilities—Logic (≥2 bits), Memory (≥1 bit), Control (≥1 bit), and State (≥1 bit)—and prove their mutual independence via explicit construction. The bound is tight: Tag(2,2), SK calculus, and Rule 110 each achieve exactly 5 bits under specification complexity.

We conjecture this bound reflects a deeper constraint: that universal computation inherently requires the descriptive complexity to encode **Control**—the capacity for conditional, context-dependent state transitions. We invite proof or refutation of this conjecture in alternative substrates.

## Key Result

**Theorem (Universal Computation Threshold):** Under natural encodings, no computational system with description length ≤ 4 bits is universal. The bound of 5 bits is tight, achieved by Tag(2,2), SK calculus, and Rule 110.

**Capability Decomposition:**
- Logic (L) ≥ 2 bits — Boolean completeness (Post 1941)
- Memory (M) ≥ 1 bit — Unbounded storage (Turing 1936)
- Control (K) ≥ 1 bit — Conditional branching (Böhm-Jacopini 1966)
- State (S) ≥ 1 bit — Halting capability (Minsky 1967)

**Total: 2 + 1 + 1 + 1 = 5 bits minimum**

## Repository Structure

```
UCT/
├── paper/
│   ├── five_bit_threshold.md           # Full paper (Markdown)
│   ├── five_bit_threshold.tex          # Full paper (LaTeX)
│   └── references.bib                  # Bibliography
├── figures/
│   ├── capability_decomposition.png    # Why 5 bits?
│   ├── complexity_landscape.png        # Complexity landscape showing universal systems
│   ├── two_peaks.png                   # Activity at 4 bits / computation at 5 bits
│   ├── rule110_dynamics.png            # Complex, non-periodic behavior
│   ├── rule110_vs_rule122.png          # Rule 110 vs Rule 122
│   ├── control_diagram.png             # Control capability
│   ├── threshold_summary.png           # Summary of the 5 bit threshold
│   └── substrate_comparison.png        # Complexity comparison across substrates
├── supplementary/
│   ├── proofs.md                       # Detailed proofs
│   ├── exhaustive_enumeration.md       # TM(2,2) results
│   └── structural_conditions.md        # Substrate-specific conditions
├── theory/
│   ├── INDEX.md                        # Theory file index
│   ├── CAPABILITY_CALCULUS.md          # Formal framework
│   ├── FOUR_BIT_IMPOSSIBILITY.md       # Formal impossibility proof
│   ├── UCT_COMPLETE_PROOF.md           # Complete proof structure
│   ├── UCT_FORMALIZATION.md            # Formal UCT statement
│   ├── BEYOND_UCT.md                   # 6+ bit optimality analysis
│   └── SELF_ORGANIZATION_THRESHOLD.md  # SOT formalization
├── discussion/
│   ├── INDEX.md                        # Discussion file index
│   ├── PRACTICAL_APPLICATIONS.md       # Real-world applications
│   ├── AI_EMERGENCE.md                 # Neural network implications
│   ├── FUTURE_WORK.md                  # Open problems
│   └── FAQ.md                          # Common questions
├── code/
│   ├── eca_analysis.py                 # Elementary CA experiments
│   ├── figure_generation.py            # Generate all figures
│   ├── control_analysis.py             # Control capability metrics
│   ├── rule110_analysis.py             # Rule 110 analysis
│   ├── rule122_analysis.py             # Rule 122 analysis
│   └── computational_metrics.py        # Shared metrics
├── data/
│   ├── CHECKPOINT.json                 # Research checkpoint
│   └── PROGRESS.md                     # Research progress log
├── LICENSE
├── five_bit_threshold.pdf              # PDF of the paper
└── README.md                           # This file
```

## Quick Start

### Requirements
- Python 3.10+
- NumPy, Matplotlib, SciPy

### Generate Figures
```bash
cd code
python figure_generation.py
```

### Build Paper (LaTeX)
```bash
cd paper
pdflatex five_bit_threshold.tex
bibtex five_bit_threshold
pdflatex five_bit_threshold.tex
pdflatex five_bit_threshold.tex
```

## Key Findings

### 1. The Five-Bit Threshold
Every universal computational system requires at least 5 bits of descriptive complexity under natural encodings. This is proven via capability decomposition and connected to classical results (Post, Turing, Böhm-Jacopini, Minsky).

### 2. Rule 110 is a 5-Bit Rule
Rule 110 (binary: 01101110) has exactly **5 bits set** in its rule table - achieving the UCT threshold directly under specification complexity.

### 3. Control as the Critical Capability
The transition from 4 bits to 5 bits corresponds to acquiring **Control** - the capacity for conditional, context-dependent state transitions. At 4 bits, systems can have Memory + State + partial Logic, but collisions are uniform rather than selective.

### 4. Two Distinct Peaks
- **Activity** peaks at 4 bits (50% density) - maximum combinatoric entropy
- **Computation** peaks at 5 bits (62.5% density) - structured information processing

These are empirically separable phenomena, confirming UCT is not merely the tail of an entropy curve.

### 5. Structural Conditions
Complexity ≥ 5 bits is necessary but not sufficient. Additional structural conditions are required:
- **1D CA:** Asymmetry > 0.3, collision diversity > 0.5
- **2D systems:** Collision geometry with ≥4 directions
- **Tag systems:** Production growth for some symbol

## Citation

```bibtex
@article{five_bit_threshold_2026,
  title={The Five-Bit Threshold for Universal Computation},
  author={[Author]},
  journal={[Journal]},
  year={2026},
  note={Preprint}
}
```

## References

1. Turing, A.M. (1936). "On Computable Numbers"
2. Post, E. (1941). "The Two-Valued Iterative Systems of Mathematical Logic"
3. Cocke, J. & Minsky, M. (1964). "Universality of Tag Systems with P=2"
4. Böhm, C. & Jacopini, G. (1966). "Flow Diagrams, Turing Machines and Languages"
5. Minsky, M. (1967). "Computation: Finite and Infinite Machines"
6. Cook, M. (2004). "Universality in Elementary Cellular Automata"

## License

MIT License - See [LICENSE](LICENSE) for details.

## Contributing

We welcome contributions, particularly:
- Proofs or refutations of the Control conjecture in alternative substrates
- Analysis of quantum computation thresholds
- Connections to thermodynamics and physical realizability

Please open an issue or submit a pull request.
