# Future Work

## Open Problems

### 1. The Control Conjecture

**Statement:** The five-bit threshold reflects the minimum complexity to encode Control—conditional, context-dependent state transitions.

**What's Needed:**
- Formal proof that Control ≥ 1 bit is necessary in arbitrary substrates
- Or a counterexample: a 4-bit universal system under natural encoding

### 2. Quantum UCT

**Question:** Does quantum computation change the threshold?

**Hypothesis:** Quantum UCT = Classical UCT = 5 bits

**Approach:**
- Formalize quantum capability extractors
- Prove or refute quantum advantage for threshold reduction
- Investigate Holevo bound implications

### 3. Continuous Systems

**Question:** What is the UCT for continuous dynamical systems?

**Approach:**
- Define "natural encoding" for ODEs/PDEs
- Identify capability analogues (Logic → nonlinearity, etc.)
- Compute thresholds for known universal continuous systems

---

## Extensions

### 4. Hierarchical UCT

**Question:** What are the thresholds for higher-level computational capabilities?

**Possibilities:**
- Self-modification: UCT + X bits
- Learning: UCT + Y bits
- Agency: UCT + Z bits

### 5. Physical Realizability

**Current Result:** Energy conservation adds 0 overhead (BBM at 5.64 bits)

**Extensions:**
- Noise tolerance overhead?
- Error correction overhead?
- Quantum decoherence overhead?

### 6. Biological Systems

**Question:** What is the minimal biochemical universal computer?

**Current Estimate:** DNA strand displacement at ~7 bits

**Open:**
- Tighter bounds for biochemical substrates
- Connection to origin of life

---

## Verification Projects

### 7. Exhaustive Enumeration

**Completed:** TM(2,2) - all 4096 machines

**Future:**
- TM(2,3) - 13,824 machines (partial)
- All 5-bit ECAs exhaustively analyzed
- Larger tag systems

### 8. Automated Universality Checking

**Goal:** Tool that takes a system description and:
1. Computes K_spec
2. Checks structural conditions
3. Reports universality status/likelihood

### 9. Formal Verification

**Goal:** Coq/Lean formalization of:
- Capability calculus
- Independence theorem
- UCT theorem

---

## Community Challenges

### 10. Find a 4-Bit Universal System

**Prize:** Disproof of UCT under natural encodings

**Requirements:**
- Natural encoding (Definition 2.3)
- Specification complexity ≤ 4 bits
- Proven universality

### 11. Prove Control Necessity

**Prize:** Formal proof of Control conjecture

**Requirements:**
- Arbitrary substrate
- Rigorous Control definition
- Proof that Control ≥ 1 bit for universality

---

## Connections to Explore

### 12. Kolmogorov Complexity

- Relationship between UCT and invariance theorem
- UCT as lower bound on program complexity

### 13. Thermodynamics

- Landauer's principle and UCT
- Minimum energy cost of universal computation

### 14. Category Theory

- Categorical formulation of capability calculus
- Functorial view of universality

### 15. Busy Beaver

- BB(5) = 47,176,870 and the UCT connection
- What happens at BB(4)?
