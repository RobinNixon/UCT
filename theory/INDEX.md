# Theory Documents Index

This directory contains the formal theoretical development of the Universal Computation Threshold (UCT).

## Core Documents

### 1. UCT_COMPLETE_PROOF.md
The complete formal proof of the 5-bit threshold, including:
- Theorem statement
- Capability decomposition lemmas
- Tightness proof
- Structural conditions

### 2. CAPABILITY_CALCULUS.md
Formal framework defining:
- Capability extractors (E_L, E_M, E_K, E_S)
- Accounting conventions
- Natural encoding class
- Independence theorem

### 3. FOUR_BIT_IMPOSSIBILITY.md
Formal impossibility proof establishing:
- Each capability minimum (Logic ≥ 2, Memory ≥ 1, Control ≥ 1, State ≥ 1)
- Connections to Post, Turing, Böhm-Jacopini, Minsky
- Information-theoretic foundation
- The counting argument

### 4. UCT_FORMALIZATION.md
Early formalization work including:
- Initial definitions
- First proof attempts
- Identification of proof gaps

## Extended Analysis

### 5. SELF_ORGANIZATION_THRESHOLD.md
Analysis of the Self-Organization Threshold (SOT):
- SOT ≈ 3 bits vs UCT = 5 bits
- The 2-bit gap between structure and control
- Experimental evidence from Life-like rules

### 6. BEYOND_UCT.md
What happens above the threshold:
- Diminishing returns above 5 bits
- The inverted-U complexity curve
- Why UCT is optimal, not just minimal

## Document Hierarchy

```
UCT Theory
├── Core Theorem
│   ├── UCT_COMPLETE_PROOF.md (main result)
│   ├── CAPABILITY_CALCULUS.md (formal framework)
│   └── FOUR_BIT_IMPOSSIBILITY.md (lower bound)
├── Extended Analysis
│   ├── SELF_ORGANIZATION_THRESHOLD.md
│   └── BEYOND_UCT.md
└── Historical
    └── UCT_FORMALIZATION.md (early work)
```

## Key Theorems

| Theorem | File | Statement |
|---------|------|-----------|
| UCT Main | UCT_COMPLETE_PROOF | K(C) ≥ 5 bits for universal C |
| 4-Bit Impossibility | FOUR_BIT_IMPOSSIBILITY | No 4-bit system is universal |
| Capability Independence | CAPABILITY_CALCULUS | L, M, K, S are independent |
| Symmetry Obstruction | FOUR_BIT_IMPOSSIBILITY | Symmetric 1D CA cannot be universal |

## Reading Order

For newcomers:
1. Start with UCT_COMPLETE_PROOF.md for the main result
2. Read FOUR_BIT_IMPOSSIBILITY.md for detailed proofs
3. Read CAPABILITY_CALCULUS.md for the formal framework

For experts:
1. Jump directly to CAPABILITY_CALCULUS.md for the formal definitions
2. Check FOUR_BIT_IMPOSSIBILITY.md for connections to classical results
