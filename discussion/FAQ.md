# Frequently Asked Questions

## Basic Questions

### Q: What is the five-bit threshold?

**A:** The five-bit threshold (UCT) states that any universal computational system requires at least 5 bits of descriptive complexity under natural encodings. This is proven via capability decomposition: Logic (2) + Memory (1) + Control (1) + State (1) = 5 bits.

### Q: What is a "natural encoding"?

**A:** A natural encoding is a description scheme where:
1. Description components correspond to system components
2. Specifying among n choices costs log₂(n) bits
3. Composite descriptions concatenate with logarithmic overhead
4. Capability extractors are well-defined and non-overlapping

Examples: TM transition tables, CA rule numbers, tag system productions.

### Q: Why 5 bits specifically?

**A:** The decomposition is:
- **Logic (2 bits):** Need Boolean completeness (NAND/NOR)
- **Memory (1 bit):** Need read/write distinction
- **Control (1 bit):** Need branch/continue distinction
- **State (1 bit):** Need computing/halted distinction

These are independent capabilities that cannot be shared.

---

## Technical Questions

### Q: Why does Rule 110 have both "5 bits" and "6.58 bits"?

**A:** We use two complexity measures:
- **K_spec (5 bits):** Number of 1s in the rule table (popcount)
- **K_full (6.58 bits):** Includes neighborhood specification (log₂(3) ≈ 1.58)

The UCT uses specification complexity for cross-substrate comparability.

### Q: Is 5 bits sufficient for universality?

**A:** No. 5 bits is necessary but not sufficient. Systems must also satisfy structural conditions:
- 1D CA: Asymmetry, collision diversity
- 2D: Collision geometry
- Tag systems: Production growth

Rule 122 has 6 bits but is not universal due to symmetry.

### Q: What about Rule 122? It has 6 bits but isn't universal.

**A:** Rule 122 fails the structural condition of asymmetry. Symmetric rules cannot support directed information flow, which is required for universal computation. This demonstrates that complexity alone is not sufficient.

---

## Scope Questions

### Q: Does this apply to quantum computers?

**A:** We conjecture Quantum UCT = Classical UCT = 5 bits. Quantum provides speedup, not simplification. The Holevo bound limits information extraction. This remains an open question.

### Q: Does this apply to neural networks?

**A:** Not directly. Neural networks are continuous systems with different encoding considerations. However, the capability decomposition may provide insight into minimum architectural requirements for universal computation.

### Q: What about analog computers?

**A:** The UCT applies to discrete computational systems. Analog systems require a separate analysis with appropriate definitions of "natural encoding."

---

## Objections

### Q: Can't you encode a UTM in 1 bit by pre-agreement?

**A:** Yes, but this violates the "natural encoding" requirement. Such an encoding doesn't satisfy structural correspondence—it's a cryptographic/adversarial encoding, not a natural one.

### Q: What if Logic and Memory share bits (e.g., NAND flip-flop)?

**A:** A NAND flip-flop requires:
- 2 bits for gate type (Logic)
- ≥2 bits for connection topology (Memory)

The topology is additional information, properly accounted as Memory. Sharing actually increases total bits, not decreases.

### Q: Isn't "natural encoding" circular?

**A:** The definition is explicit and testable. The conjecture (5.3) asserts that natural encodings capture all reasonable encodings. If someone exhibits a counterexample, it would challenge this conjecture—but the counterexample must be structurally reasonable, not adversarial.

---

## Implications

### Q: What does this mean for the origin of life?

**A:** Any physical/chemical system achieving universal computation must encode ≥5 bits of programmatic structure. This may explain why life required a minimum complexity threshold before hereditary computation could emerge.

### Q: Is 5 bits optimal or just minimal?

**A:** Both. Our analysis shows:
- 5 bits is the minimum for universality
- Computational richness peaks at 5 bits
- Above 5 bits, collision diversity and structure decline

The 5-bit point is the peak of an inverted-U curve.

### Q: What about self-organization?

**A:** Self-organization emerges at the SOT (~3 bits), below UCT. The 2-bit gap represents the acquisition of Control. Systems can self-organize without computing universally.

---

## Getting Started

### Q: How do I test if my system is universal?

**A:** Use the Universality Checklist (Appendix D):
1. Logic Test: Can implement NAND/NOR?
2. Memory Test: Unbounded storage?
3. Control Test: Conditional branching?
4. State Test: ≥2 configurations?
5. Complexity Test: K_spec ≥ 5 bits?

Plus substrate-specific structural conditions.

### Q: Where can I find the code?

**A:** See the `code/` directory:
- `figure_generation.py` - Generate all paper figures
- `eca_analysis.py` - Elementary CA analysis
- `rule110_analysis.py` - Rule 110 deep dive
- `control_analysis.py` - Control capability metrics
