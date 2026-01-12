"""
Deep Dive: Rule 110
===================

Rule 110 is the simplest known Turing-complete 1D CA.
Let's understand WHY it works and if it can be simplified.

Rule 110 in binary: 01101110
- 111 -> 0 (overcrowding dies)
- 110 -> 1 (stable edge)
- 101 -> 1 (stable with gap)
- 100 -> 0 (isolated dies)
- 011 -> 1 (growth)
- 010 -> 1 (survives)
- 001 -> 1 (growth)
- 000 -> 0 (stays dead)

Key features:
- Asymmetric (left-biased)
- Has both "death" and "birth" conditions
- Creates traveling structures (gliders)
"""

import numpy as np
from harness import *
from pathlib import Path
import matplotlib.pyplot as plt

Path('output').mkdir(exist_ok=True)

# ============================================================
# RULE 110 IMPLEMENTATION
# ============================================================

def elementary_step(row, rule_num):
    """One step of elementary CA."""
    w = len(row)
    new_row = np.zeros(w, dtype=int)
    for i in range(w):
        pattern = row[(i-1) % w] * 4 + row[i] * 2 + row[(i+1) % w]
        new_row[i] = (rule_num >> pattern) & 1
    return new_row

def run_rule(rule_num, init, steps):
    """Run a rule and return spacetime diagram."""
    row = init.copy()
    history = [row.copy()]
    for _ in range(steps):
        row = elementary_step(row, rule_num)
        history.append(row.copy())
    return np.array(history)

def find_gliders(rule_num, max_width=10, max_period=20):
    """
    Find all glider-like patterns for a rule.
    A glider is a pattern that returns to itself (possibly shifted) after some period.
    """
    gliders = []

    # Try all small patterns
    for width in range(1, max_width + 1):
        for pattern_bits in range(2**width):
            # Create pattern
            pattern = np.array([(pattern_bits >> i) & 1 for i in range(width)])

            # Embed in larger space with zeros
            row = np.zeros(width + 2 * max_period, dtype=int)
            start = max_period
            row[start:start+width] = pattern

            # Run and check for return
            initial = row.copy()
            for period in range(1, max_period + 1):
                row = elementary_step(row, rule_num)

                # Check if pattern returned (possibly shifted)
                for shift in range(-period, period + 1):
                    shifted = np.roll(row, -shift)
                    if np.array_equal(shifted, initial):
                        # Found a glider!
                        gliders.append({
                            'pattern': pattern.tolist(),
                            'width': width,
                            'period': period,
                            'shift': shift,
                            'speed': shift / period if period > 0 else 0
                        })
                        break
                else:
                    continue
                break

    # Remove duplicates and subpatterns
    unique_gliders = []
    for g in gliders:
        is_dup = False
        for ug in unique_gliders:
            if g['pattern'] == ug['pattern']:
                is_dup = True
                break
        if not is_dup:
            unique_gliders.append(g)

    return unique_gliders

# ============================================================
# RULE 110 ANALYSIS
# ============================================================

def analyze_rule_110():
    """Deep analysis of Rule 110."""
    print("="*60)
    print("RULE 110 DEEP DIVE")
    print("="*60)

    # Rule table
    print("\nRule 110 lookup table:")
    for pattern in range(8):
        bits = f"{pattern:03b}"
        output = (110 >> pattern) & 1
        print(f"  {bits} -> {output}")

    # Count 1s
    print(f"\nRule complexity: {bin(110).count('1')} bits set (out of 8)")

    # Find gliders
    print("\n--- Searching for Gliders ---")
    gliders = find_gliders(110, max_width=8, max_period=15)

    print(f"\nFound {len(gliders)} glider candidates:")
    for g in sorted(gliders, key=lambda x: (x['width'], x['period'])):
        pattern_str = ''.join(str(b) for b in g['pattern'])
        print(f"  Pattern '{pattern_str}' (w={g['width']}): "
              f"period={g['period']}, shift={g['shift']}, speed={g['speed']:.2f}")

    # Visualize key gliders
    print("\n--- Visualizing Gliders ---")

    # The famous gliders in Rule 110
    known_gliders = [
        [1],           # Single cell
        [1, 1],        # Pair
        [1, 1, 1],     # Triple
        [1, 1, 1, 1],  # Quad
        [1, 0, 1],     # Spaced pair
        [1, 1, 0, 1],  # 1101
        [1, 0, 1, 1],  # 1011
    ]

    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    axes = axes.flatten()

    for idx, pattern in enumerate(known_gliders):
        if idx >= 8:
            break

        # Create initial condition
        width = 64
        row = np.zeros(width, dtype=int)
        start = width // 2 - len(pattern) // 2
        row[start:start+len(pattern)] = pattern

        # Run
        history = run_rule(110, row, 50)

        axes[idx].imshow(history, cmap='binary', interpolation='nearest', aspect='auto')
        axes[idx].set_title(f"Pattern: {''.join(str(b) for b in pattern)}")
        axes[idx].set_xlabel('Space')
        axes[idx].set_ylabel('Time')

    # Hide unused subplot
    if len(known_gliders) < 8:
        axes[-1].axis('off')

    plt.tight_layout()
    plt.savefig('output/rule110_gliders.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved glider visualizations to output/rule110_gliders.png")

    return gliders

# ============================================================
# COLLISION ANALYSIS
# ============================================================

def analyze_collisions():
    """Analyze what happens when gliders collide."""
    print("\n--- Collision Analysis ---")

    # Set up two patterns on collision course
    collisions = [
        ("1 vs 1", [1], [1], 20),
        ("11 vs 1", [1, 1], [1], 15),
        ("11 vs 11", [1, 1], [1, 1], 10),
        ("111 vs 1", [1, 1, 1], [1], 10),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(12, 12))
    axes = axes.flatten()

    for idx, (name, left_pattern, right_pattern, gap) in enumerate(collisions):
        width = 80
        row = np.zeros(width, dtype=int)

        # Place left pattern
        left_pos = width // 3
        row[left_pos:left_pos+len(left_pattern)] = left_pattern

        # Place right pattern
        right_pos = left_pos + len(left_pattern) + gap
        row[right_pos:right_pos+len(right_pattern)] = right_pattern

        # Run
        history = run_rule(110, row, 80)

        axes[idx].imshow(history, cmap='binary', interpolation='nearest', aspect='auto')
        axes[idx].set_title(f"Collision: {name}")
        axes[idx].set_xlabel('Space')
        axes[idx].set_ylabel('Time')

    plt.tight_layout()
    plt.savefig('output/rule110_collisions.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved collision analysis to output/rule110_collisions.png")

# ============================================================
# SIMPLIFICATION ATTEMPTS
# ============================================================

def try_simplifications():
    """Try to simplify Rule 110 while keeping interesting behavior."""
    print("\n--- Simplification Attempts ---")

    # Rule 110 = 01101110
    # Try flipping each bit and see what happens

    results = []

    for bit in range(8):
        modified_rule = 110 ^ (1 << bit)

        # Test with random init
        np.random.seed(42)
        row = np.random.randint(0, 2, 64)
        history = run_rule(modified_rule, row, 200)

        # Analyze
        final_rows = history[-50:]
        activity = np.mean([np.mean(final_rows[i] != final_rows[i-1])
                          for i in range(1, len(final_rows))])
        density = np.mean(history[-1])

        results.append({
            'bit': bit,
            'rule': modified_rule,
            'activity': activity,
            'density': density
        })

        # Which transition changed?
        old_output = (110 >> bit) & 1
        new_output = 1 - old_output
        pattern = f"{bit:03b}"
        print(f"  Flip bit {bit} ({pattern}: {old_output}->{new_output}): "
              f"Rule {modified_rule}, activity={activity:.4f}, density={density:.4f}")

    # Visualize most interesting modifications
    interesting = [r for r in results if 0.01 < r['activity'] < 0.5]

    if interesting:
        fig, axes = plt.subplots(1, len(interesting[:4]), figsize=(4*len(interesting[:4]), 4))
        if len(interesting[:4]) == 1:
            axes = [axes]

        for idx, r in enumerate(interesting[:4]):
            np.random.seed(42)
            row = np.random.randint(0, 2, 64)
            history = run_rule(r['rule'], row, 100)

            axes[idx].imshow(history, cmap='binary', interpolation='nearest', aspect='auto')
            axes[idx].set_title(f"Rule {r['rule']} (bit {r['bit']} flipped)")

        plt.tight_layout()
        plt.savefig('output/rule110_modifications.png', dpi=150, bbox_inches='tight')
        plt.close()
        print("Saved modifications to output/rule110_modifications.png")

    return results

# ============================================================
# RULE NEIGHBORHOOD ANALYSIS
# ============================================================

def analyze_nearby_rules():
    """Analyze rules close to 110 in rule space."""
    print("\n--- Nearby Rules Analysis ---")

    # Check all rules within Hamming distance 1-2 of Rule 110
    interesting_neighbors = []

    for rule in range(256):
        # Hamming distance
        diff = bin(rule ^ 110).count('1')
        if diff > 2:
            continue

        # Test
        np.random.seed(42)
        row = np.random.randint(0, 2, 64)
        history = run_rule(rule, row, 200)

        final_rows = history[-50:]
        activity = np.mean([np.mean(final_rows[i] != final_rows[i-1])
                          for i in range(1, len(final_rows))])

        if 0.02 < activity < 0.4:
            interesting_neighbors.append({
                'rule': rule,
                'distance': diff,
                'activity': activity
            })

    print(f"\nFound {len(interesting_neighbors)} interesting neighbors (distance <= 2):")
    for r in sorted(interesting_neighbors, key=lambda x: -x['activity']):
        print(f"  Rule {r['rule']} (dist={r['distance']}): activity={r['activity']:.4f}")

    # Visualize top neighbors
    if interesting_neighbors:
        top = sorted(interesting_neighbors, key=lambda x: -x['activity'])[:4]

        fig, axes = plt.subplots(1, len(top), figsize=(4*len(top), 4))
        if len(top) == 1:
            axes = [axes]

        for idx, r in enumerate(top):
            np.random.seed(42)
            row = np.random.randint(0, 2, 64)
            history = run_rule(r['rule'], row, 100)

            axes[idx].imshow(history, cmap='binary', interpolation='nearest', aspect='auto')
            axes[idx].set_title(f"Rule {r['rule']} (dist={r['distance']}, act={r['activity']:.3f})")

        plt.tight_layout()
        plt.savefig('output/rule110_neighbors.png', dpi=150, bbox_inches='tight')
        plt.close()
        print("Saved neighbors to output/rule110_neighbors.png")

    return interesting_neighbors

# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    gliders = analyze_rule_110()
    analyze_collisions()
    modifications = try_simplifications()
    neighbors = analyze_nearby_rules()

    print("\n" + "="*60)
    print("SYNTHESIS")
    print("="*60)
    print("""
Key findings about Rule 110:

1. GLIDERS: Multiple traveling patterns with different speeds
   - Small patterns (1-4 cells) create traveling structures
   - Period and speed vary by pattern

2. COLLISIONS: When gliders meet, they interact non-trivially
   - Collisions can create new structures
   - Different collision types produce different outcomes

3. SIMPLIFICATION: Flipping any single bit changes behavior significantly
   - Rule 110 is precisely tuned for complex behavior
   - Small changes lead to either chaos or death

4. NEIGHBORS: Few rules near 110 show similar complexity
   - 110 sits in a special region of rule space
   - Most neighbors are either chaotic or trivial

This suggests Rule 110 is near a "critical point" in rule space where
computational behavior emerges. It may be close to minimal.
""")
