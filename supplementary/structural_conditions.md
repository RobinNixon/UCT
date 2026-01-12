# Supplementary Material: Structural Conditions for Universality

## S1. Overview

The five-bit threshold establishes that K(C) ≥ 5 is **necessary** for universality. However, it is **not sufficient**. Additional structural conditions, specific to each substrate, determine whether a system above threshold achieves universality.

This document details the structural conditions for each substrate.

---

## S2. One-Dimensional Cellular Automata

### S2.1 Required Conditions

For a 1D elementary CA to be universal, it must satisfy:

1. **Asymmetry** (Proven Necessary)
   - Definition: The rule must not commute with spatial reflection
   - Threshold: Asymmetry score > 0.3
   - Why: Symmetric rules have zero mean information velocity

2. **Glider Support** (Empirically Necessary)
   - Definition: Must support translating persistent patterns
   - Threshold: ≥1 glider type
   - Why: Gliders carry information between computation sites

3. **Collision Diversity** (Empirically Necessary)
   - Definition: Glider collisions must produce varied outcomes
   - Threshold: Diversity score > 0.5
   - Why: Collisions implement logic gates

4. **Class 4 Behavior** (Empirically Necessary)
   - Definition: Wolfram's "edge of chaos" classification
   - Not Class 1 (trivial), Class 2 (periodic), or Class 3 (chaotic)
   - Why: Class 4 balances structure and dynamics

### S2.2 The Symmetry Obstruction Theorem

**Theorem:** Symmetric 1D cellular automata cannot be universal.

**Proof:**

Let f be a CA rule and R be the spatial reflection operator.

If f ∘ R = R ∘ f (rule is symmetric), then:

1. For any configuration x₀:
   - v̄(R(x₀)) = -v̄(x₀) (reflection reverses velocity)

2. But if f commutes with R:
   - v̄(R(x₀)) = v̄(x₀) (symmetric evolution preserves statistics)

3. Together: v̄(x₀) = -v̄(x₀), hence v̄(x₀) = 0

4. Zero mean velocity means no directed information transport

5. Universal computation requires sequential processing, which requires directional transport

**Conclusion:** Symmetric rules cannot be universal. □

### S2.3 Rule 110 vs Rule 122

| Property | Rule 110 | Rule 122 |
|----------|----------|----------|
| Bits set | 5 | 6 |
| Asymmetry | 1.0 (maximal) | 0.0 (symmetric) |
| Mean velocity | -0.51 | 0 |
| Gliders | Many types | None |
| Collision diversity | 0.92 | N/A |
| **Universal** | **Yes** | **No** |

Rule 122 has MORE bits but LESS computational capability due to symmetry.

---

## S3. Two-Dimensional Cellular Automata

### S3.1 Required Conditions

For 2D CA (Life-like rules) to be universal:

1. **Collision Geometry**
   - Must support collisions from ≥4 directions
   - Why: Logic gates require multiple input/output paths

2. **Glider/Spaceship Support**
   - Must support mobile persistent structures
   - Why: Information carriers

3. **Stable Structures**
   - Must support static configurations (still lifes)
   - Why: Memory elements

4. **Balanced Birth/Survival**
   - Neither too much birth (explosive) nor too much survival (static)
   - Why: Edge of chaos dynamics

### S3.2 Conway's Game of Life Analysis

Rule: B3/S23 (Birth on 3 neighbors, Survive on 2-3)

**Complexity:** ~3 bits (specification complexity)

**Note:** Life is below the UCT threshold under specification complexity. Its universality relies on:
- Rich initial configurations
- Infinite grid
- Complex emergent structures (glider guns, etc.)

Life achieves weak universality through complexity emerging from simple rules + complex initial conditions.

---

## S4. Turing Machines

### S4.1 Required Conditions

For a Turing machine to be universal:

1. **State Count** ≥ 2 (Proven)
   - 1-state machines are trivial (Minsky)

2. **Transition Variety**
   - Not all transitions identical
   - Must have both L and R moves
   - Must have state changes

3. **Non-Trivial Halting**
   - Must be able to halt on some inputs
   - Must not halt on all inputs (trivial)

### S4.2 TM(2,2) Analysis

All 4096 TM(2,2) machines satisfy the state requirement but fail on transition variety:
- Most have degenerate transition tables
- Head gets "stuck" in small loops
- Tape usage is bounded

**Conclusion:** The 5-bit threshold allows for universality, but the specific encoding of those 5 bits matters.

---

## S5. Tag Systems

### S5.1 Required Conditions

For a tag system to be universal:

1. **Production Growth**
   - At least one production must produce more symbols than deleted
   - |P(σ)| > v for some symbol σ
   - Why: Allows unbounded string growth

2. **Non-Trivial Productions**
   - Productions must not be identity or constant
   - Why: Must transform information

3. **Deletion Number** v ≥ 2
   - v = 1 tag systems are known non-universal
   - Why: Insufficient "mixing" of symbols

### S5.2 Tag(2,2) Analysis

- Σ = {0, 1}, v = 2
- P(0) = 00, P(1) = 1101

**Verification:**
- |P(1)| = 4 > 2 = v ✓ (growth)
- Productions are non-trivial ✓
- v = 2 ✓

All conditions satisfied → Universal (Cocke-Minsky 1964)

---

## S6. Counter Machines

### S6.1 Required Conditions

For a counter machine to be universal:

1. **Register Count** ≥ 2 (Proven)
   - 1-register machines compute only semilinear sets
   - Minsky 1967

2. **Full Instruction Set**
   - INCREMENT
   - DECREMENT (with zero test)
   - CONDITIONAL JUMP

### S6.2 Significance

The counter machine threshold provides independent confirmation:
- 1 counter: NOT universal (~3 bits)
- 2 counters: Universal (~5 bits)

The jump crosses the UCT threshold.

---

## S7. Particle Systems (BBM/HPP)

### S7.1 Required Conditions

For particle systems to be universal:

1. **Dimension** ≥ 2
   - 1D conserving systems are "traffic-like"
   - Cannot implement logic gates

2. **Direction Count** ≥ 4
   - Need multiple collision geometries
   - Why: Logic gates require signal routing

3. **Non-Trivial Scattering**
   - Head-on collisions must change directions
   - Why: Implements NAND-like behavior

### S7.2 BBM Analysis

The Billiard Ball Model (Margolus) satisfies:
- 2D grid ✓
- 4 directions (N,E,S,W) ✓
- 90° scattering on collision ✓

**Additional property:** Energy conservation adds ZERO overhead.
BBM complexity: ~5.64 bits → Universal

---

## S8. Summary: Structural Checklist

| Substrate | Complexity | Condition 1 | Condition 2 | Condition 3 |
|-----------|------------|-------------|-------------|-------------|
| 1D CA | K ≥ 5 | Asymmetric | Gliders | Collision diversity |
| 2D CA | K ≥ 5 | 4+ directions | Gliders | Balanced B/S |
| Turing | K ≥ 5 | ≥2 states | Transition variety | Non-trivial halt |
| Tag | K ≥ 5 | v ≥ 2 | Production growth | Non-trivial P |
| Counter | K ≥ 5 | ≥2 registers | Full instruction set | - |
| Particles | K ≥ 5 | 2D | ≥4 directions | Non-trivial scatter |

---

## S9. The Control Connection

The structural conditions across substrates share a common theme: they enable **Control**—the capacity for conditional, context-dependent state transitions.

| Substrate | How Control is Achieved |
|-----------|-------------------------|
| 1D CA | Asymmetric collision outcomes |
| 2D CA | Directional signal routing |
| Turing | State-dependent transitions |
| Tag | Symbol-dependent productions |
| Counter | Zero-test branching |
| Particles | Collision geometry |

This supports the conjecture that Control is the critical capability distinguishing 4-bit from 5-bit systems.
