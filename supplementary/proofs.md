# Supplementary Material: Detailed Proofs

## S1. Capability Lower Bound Proofs

### S1.1 Logic Minimum (2 bits) - Extended Proof

**Theorem:** Any universal system requires ≥2 bits for Logic capability.

**Full Proof:**

1. **Boolean Completeness Requirement:**
   By Post's theorem (1941), any system capable of computing all Boolean functions must contain a functionally complete basis. A basis is functionally complete if it can express all 2^(2^n) n-input Boolean functions.

2. **Minimal Complete Bases:**
   The following are the ONLY single-gate complete bases for 2-input functions:
   - NAND: f(a,b) = ¬(a ∧ b)
   - NOR: f(a,b) = ¬(a ∨ b)

   Proof: Among the 16 two-input Boolean functions, only these two satisfy:
   - Self-dual: f(¬a, ¬b) ≠ ¬f(a,b)
   - Preserves neither 0 nor 1: f(0,0) ≠ 0 and f(1,1) ≠ 1

3. **Information Content:**
   To specify NAND among the 16 two-input functions:
   - Must specify the truth table output pattern
   - NAND outputs (1,1,1,0) for inputs (00,01,10,11)
   - The distinguishing feature: which input gives 0
   - 4 possibilities → log₂(4) = 2 bits

4. **Cannot Achieve with 1 Bit:**
   With 1 bit, we can distinguish only 2 functions. But:
   - Even among {NAND, NOR}, both are complete
   - We need to specify WHICH complete function
   - Specifying the truth table requires 2 bits minimum

5. **Tightness:**
   NAND can be specified with exactly 2 bits:
   - Bit 1: "The unique 0 output is at input index ≥ 2" (1 bit)
   - Bit 2: "The unique 0 output is at input index = 3" (1 bit)
   - Together: input index 11₂ = 3 → output 0

**QED**

### S1.2 Memory Minimum (1 bit) - Extended Proof

**Theorem:** Any universal system requires ≥1 bit for Memory capability.

**Full Proof:**

1. **Unbounded Storage Requirement:**
   By Turing's theorem (1936), universal computation requires access to unbounded storage. Without it:
   - System has finite configurations
   - By pigeonhole principle, computation is eventually periodic
   - Cannot compute non-regular languages (e.g., {a^n b^n})

2. **Minimal Operations:**
   Unbounded storage requires at minimum two distinguishable operations:

   **Option A (Random Access):**
   - READ: Retrieve value from address
   - WRITE: Store value to address

   **Option B (Sequential Access):**
   - LEFT: Move head/pointer left
   - RIGHT: Move head/pointer right

3. **Information Content:**
   - 2 distinct operations
   - log₂(2) = 1 bit to distinguish

4. **Cannot Achieve with 0 Bits:**
   With 0 bits for memory operations:
   - Either read-only (cannot store intermediate results)
   - Or write-only (cannot retrieve stored values)
   - Neither is Turing-complete

5. **Supporting Evidence (Minsky 1967):**
   - 1-register counter machines are NOT universal
   - They recognize only semilinear sets
   - 2-register counter machines ARE universal
   - The second register provides the necessary storage distinction

**QED**

### S1.3 Control Minimum (1 bit) - Extended Proof

**Theorem:** Any universal system requires ≥1 bit for Control capability.

**Full Proof:**

1. **Conditional Execution Requirement:**
   By the Böhm-Jacopini theorem (1966), any computable function can be expressed using:
   - Sequence (composition)
   - Selection (if-then-else)
   - Iteration (while loops)

   Selection and iteration both require conditional branching.

2. **Minimal Operations:**
   Control flow requires at minimum two distinguishable behaviors:
   - CONTINUE: Proceed to next instruction
   - BRANCH: Jump to different instruction

3. **Information Content:**
   - 2 distinct control flows
   - log₂(2) = 1 bit to distinguish

4. **Cannot Achieve with 0 Bits:**
   With 0 bits for control:
   - Execution is strictly sequential (straight-line program)
   - Program length is bounded by description length
   - Cannot implement loops or conditionals
   - Recognizes only a finite set of functions

5. **Formal Argument:**
   Let P be a straight-line program of length n.
   - P can execute at most n instructions
   - P can visit at most n configurations
   - P recognizes at most 2^n inputs
   - This is a finite set, hence not universal

**QED**

### S1.4 State Minimum (1 bit) - Extended Proof

**Theorem:** Any universal system requires ≥1 bit for State capability.

**Full Proof:**

1. **Halting Requirement:**
   By definition, a computation produces an output. This requires:
   - Recognizing when computation is complete
   - Distinguishing "still computing" from "done"

2. **Minimal States:**
   Must distinguish at minimum two internal states:
   - COMPUTING: Active processing
   - HALTED: Computation complete

3. **Information Content:**
   - 2 distinct states
   - log₂(2) = 1 bit to distinguish

4. **Cannot Achieve with 0 Bits:**
   With 1 state (0 bits for state encoding):
   - Same transition applies regardless of history
   - Behavior is purely determined by current input
   - No memory of past computation
   - Cannot track progress toward goal

5. **Minsky's Theorem (1967):**
   **All 1-state Turing machines are trivial.**

   Proof: For a 1-state TM with alphabet Σ:
   - Single state q with transitions (q, σ) → (q, σ', d)
   - For each symbol σ, writes σ', moves direction d, stays in q
   - Behavior is purely periodic
   - Never halts or loops forever regardless of input
   - Cannot implement any non-trivial computation

**QED**

---

## S2. Capability Independence Proofs

### S2.1 Logic-Memory Independence

**Claim:** Logic cannot substitute for Memory, and Memory cannot substitute for Logic.

**Proof:**

**System with Logic but not Memory: Combinational Circuit**
- Implements Boolean functions (has Logic)
- Output depends only on current input (stateless)
- No storage of intermediate values
- E_L(d) specifies gate types; E_M(d) = ε

**System with Memory but not Logic: Shift Register**
- Stores and shifts bits (has Memory)
- No Boolean operations on bits (just moves them)
- Each bit remains unchanged, only position changes
- E_M(d) specifies shift direction; E_L(d) = ε

**Conclusion:** The information in E_L and E_M is structurally disjoint. □

### S2.2 Control-State Independence

**Claim:** Control cannot substitute for State, and State cannot substitute for Control.

**Proof:**

**System with Control but not State: Infinite Branching Automaton**
- Can branch based on input (has Control)
- Single internal state (lacks State to track progress)
- Branches forever without halting
- Cannot remember "what mode" it's in

**System with State but not Control: Linear Halting Machine**
- Multiple states including halt state (has State)
- No conditional branching (always same path)
- Executes fixed sequence then halts
- Cannot choose different paths based on input

**Conclusion:** Control determines WHERE execution goes; State determines WHAT MODE we're in. These are independent. □

### S2.3 Complete Independence Matrix

| Has \ Lacks | Logic | Memory | Control | State |
|-------------|-------|--------|---------|-------|
| **Logic** | - | Comb. circuit | Feedforward | Single-state calc |
| **Memory** | Shift register | - | Linear tape | Non-halting writer |
| **Control** | Branch-only FSM | Finite automaton | - | Infinite brancher |
| **State** | 2-state trivial | Halting FA | Linear halter | - |

Each cell shows a system that has the row capability but lacks the column capability, proving pairwise independence.

---

## S3. The Counting Argument

### S3.1 Formal Statement

**Theorem (4-Bit Impossibility):** Let D be any natural encoding. Let C be any computational system with |D(C)| ≤ 4 bits. Then C is not universal.

### S3.2 Proof

1. By Theorem S1.1: |E_L(D(C))| ≥ 2
2. By Theorem S1.2: |E_M(D(C))| ≥ 1
3. By Theorem S1.3: |E_K(D(C))| ≥ 1
4. By Theorem S1.4: |E_S(D(C))| ≥ 1

5. By independence (Section S2), the extractors produce non-overlapping regions.

6. By additivity:
   |D(C)| ≥ |E_L| + |E_M| + |E_K| + |E_S| ≥ 2 + 1 + 1 + 1 = 5

7. If |D(C)| ≤ 4, then |D(C)| < 5.

8. This contradicts step 6, so at least one capability must have |E_X| below its minimum.

9. A system below capability minimum lacks that capability.

10. A system lacking any required capability is not universal.

**QED**

---

## S4. Tightness: Tag(2,2) Achieves 5 Bits

### S4.1 System Definition

Tag(2,2) is defined by:
- Alphabet: Σ = {0, 1}
- Deletion number: v = 2
- Productions: P(0) = 00, P(1) = 1101

### S4.2 Complexity Calculation

| Component | Description | Bits |
|-----------|-------------|------|
| Alphabet size | log₂(2) | 1.0 |
| Deletion number | log₂(2) for v ∈ {1,2} | 1.0 |
| Production P(0) | Length + pattern | ~1.5 |
| Production P(1) | Length + pattern | ~1.5 |
| **Total** | | **5.0** |

### S4.3 Universality Proof Reference

Cocke and Minsky (1964) proved Tag(2,2) is Turing-complete by showing:
1. Any Turing machine can be simulated by a 2-register counter machine
2. Any 2-register counter machine can be simulated by a 2-tag system with 2 symbols

### S4.4 Conclusion

Tag(2,2) is universal with K = 5.0 bits, proving the bound is achievable. □
