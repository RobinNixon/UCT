"""
Experiment: Elementary Cellular Automata (1D)
=============================================

1D CA are the simplest possible automata:
- Binary cells on a line
- Next state depends on cell + two neighbors (3 bits -> 8 patterns)
- 2^8 = 256 possible rules

Rule 110 is proven Turing-complete. Let's explore the space.
"""

import numpy as np
from harness import *
from pathlib import Path

Path('output').mkdir(exist_ok=True)

# ============================================================
# ELEMENTARY CA IMPLEMENTATION
# ============================================================

def elementary_step(row, rule_num):
    """
    One step of elementary CA.
    rule_num: 0-255, encodes the 8 outputs for 8 possible inputs
    """
    w = len(row)
    new_row = np.zeros(w, dtype=int)

    for i in range(w):
        # Get neighborhood (with wrapping)
        left = row[(i-1) % w]
        center = row[i]
        right = row[(i+1) % w]

        # Pattern as 3-bit number: left*4 + center*2 + right
        pattern = left * 4 + center * 2 + right

        # Look up in rule table
        new_row[i] = (rule_num >> pattern) & 1

    return new_row

def run_elementary(rule_num, width=128, steps=128, init='single'):
    """Run elementary CA and return spacetime diagram."""
    if isinstance(init, str):
        if init == 'single':
            row = np.zeros(width, dtype=int)
            row[width // 2] = 1
        elif init == 'random':
            row = np.random.randint(0, 2, width)
    else:
        row = init.copy()
        width = len(row)

    history = [row.copy()]
    for _ in range(steps):
        row = elementary_step(row, rule_num)
        history.append(row.copy())

    return np.array(history)

def save_spacetime(diagram, filename, title=None):
    """Save spacetime diagram as image."""
    plt.figure(figsize=(8, 8))
    plt.imshow(diagram, cmap='binary', interpolation='nearest', aspect='auto')
    plt.xlabel('Space')
    plt.ylabel('Time')
    if title:
        plt.title(title)
    plt.savefig(filename, bbox_inches='tight', dpi=150)
    plt.close()

# ============================================================
# ANALYSIS FUNCTIONS
# ============================================================

def analyze_rule(rule_num, trials=5, width=64, steps=200):
    """Analyze a rule's behavior."""
    results = []

    for _ in range(trials):
        diagram = run_elementary(rule_num, width, steps, init='random')

        # Activity in final rows
        final_rows = diagram[-50:]
        activity = np.mean([np.mean(final_rows[i] != final_rows[i-1])
                          for i in range(1, len(final_rows))])

        # Density
        density = np.mean(diagram[-1])

        # Check for period
        period = None
        for p in range(1, 50):
            if np.array_equal(diagram[-1], diagram[-1-p]):
                period = p
                break

        results.append({
            'activity': activity,
            'density': density,
            'period': period
        })

    return {
        'mean_activity': np.mean([r['activity'] for r in results]),
        'mean_density': np.mean([r['density'] for r in results]),
        'periods': [r['period'] for r in results]
    }

def classify_rule(stats):
    """Classify rule behavior."""
    act = stats['mean_activity']
    dens = stats['mean_density']
    periods = stats['periods']

    # All periodic with same period
    if all(p is not None and p <= 2 for p in periods):
        if dens < 0.1 or dens > 0.9:
            return 'Class I (uniform)'
        else:
            return 'Class II (periodic)'

    # High activity, no period
    if act > 0.3:
        return 'Class III (chaotic)'

    # Some structure, moderate activity
    if act > 0.01 and act < 0.3:
        return 'Class IV (complex)'

    return 'Class II (periodic)'

# ============================================================
# EXPERIMENTS
# ============================================================

if __name__ == '__main__':
    print("="*60)
    print("Elementary Cellular Automata Exploration")
    print("="*60)

    # === FAMOUS RULES ===
    famous = {
        30: "Chaos from simple rules",
        90: "XOR/Sierpinski",
        110: "Turing complete!",
        184: "Traffic flow",
        150: "Linear feedback",
        22: "Complex patterns",
        54: "Interesting structure",
        60: "Pascal's triangle mod 2",
    }

    print("\n--- Famous Rules ---")
    for rule, desc in famous.items():
        diagram = run_elementary(rule, width=128, steps=128)
        save_spacetime(diagram, f'output/eca_rule{rule}.png', f'Rule {rule}: {desc}')

        stats = analyze_rule(rule)
        classification = classify_rule(stats)
        print(f"Rule {rule}: {desc}")
        print(f"  Activity: {stats['mean_activity']:.4f}, Density: {stats['mean_density']:.4f}")
        print(f"  Classification: {classification}")

    # === RULE 110 DEEP DIVE ===
    print("\n--- Rule 110 Deep Dive ---")

    # Standard initialization
    diagram = run_elementary(110, width=200, steps=200)
    save_spacetime(diagram, 'output/eca_rule110_large.png', 'Rule 110 - Single seed')

    # Random initialization
    diagram = run_elementary(110, width=200, steps=200, init='random')
    save_spacetime(diagram, 'output/eca_rule110_random.png', 'Rule 110 - Random init')

    # Look for gliders in Rule 110
    print("\nRule 110 is known to have gliders and can simulate computation.")
    print("The spacetime diagrams should show characteristic patterns.")

    # === SYSTEMATIC SEARCH FOR COMPLEX RULES ===
    print("\n--- Searching for Complex (Class IV) Rules ---")

    complex_rules = []

    for rule in range(256):
        stats = analyze_rule(rule, trials=3, width=48, steps=100)
        act = stats['mean_activity']
        dens = stats['mean_density']

        # Look for "edge of chaos" - moderate activity, non-trivial density
        if 0.02 < act < 0.25 and 0.1 < dens < 0.9:
            complex_rules.append((rule, act, dens))

    print(f"\nFound {len(complex_rules)} potentially complex rules:")
    for rule, act, dens in sorted(complex_rules, key=lambda x: -x[1])[:15]:
        print(f"  Rule {rule}: activity={act:.4f}, density={dens:.4f}")
        diagram = run_elementary(rule, width=128, steps=128)
        save_spacetime(diagram, f'output/eca_complex_{rule}.png', f'Rule {rule}')

    # === XOR RULE (90) ANALYSIS ===
    print("\n--- XOR Rule (90) Analysis ---")
    print("Rule 90 is linear (XOR of neighbors). Creates Sierpinski triangle.")

    diagram = run_elementary(90, width=128, steps=128)
    save_spacetime(diagram, 'output/eca_rule90_large.png', 'Rule 90 - Sierpinski')

    # Multiple seeds
    init = np.zeros(128, dtype=int)
    init[32] = 1
    init[96] = 1
    diagram = run_elementary(90, width=128, steps=128, init=init)
    save_spacetime(diagram, 'output/eca_rule90_double.png', 'Rule 90 - Double seed')

    print("Two seeds in XOR rule should show interference pattern.")

    # === MINIMAL COMPLEX RULES ===
    print("\n--- Looking for Minimal Complexity ---")
    print("Which rules have simplest structure while still being non-trivial?")

    # Count bits in rule number (simpler = fewer 1s)
    def bit_count(n):
        return bin(n).count('1')

    simple_complex = [(r, bit_count(r), act, dens)
                      for r, act, dens in complex_rules]
    simple_complex.sort(key=lambda x: (x[1], -x[2]))  # Sort by simplicity, then activity

    print("\nSimplest rules with complex behavior:")
    for rule, bits, act, dens in simple_complex[:10]:
        print(f"  Rule {rule} ({bits} bits): activity={act:.4f}")

    print("\n" + "="*60)
    print("Key findings will be in:")
    print("  - eca_rule110*.png: Turing-complete rule")
    print("  - eca_rule90*.png: XOR/Sierpinski patterns")
    print("  - eca_complex_*.png: Discovered complex rules")
    print("="*60)
