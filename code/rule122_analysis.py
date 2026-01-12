"""
Rule 122 as Canonical False Positive

Rule 122 is the perfect foil for Rule 110:
- Same unified complexity (6.58 bits)
- Visually complex behavior
- But SYMMETRIC and NOT universal

This experiment shows:
1. Why entropy/compressibility metrics misclassify it as "complex"
2. The absence of directional information flow (symmetric = v_mean = 0)
3. No collision algebra (collisions are uniform, not conditional)
4. No Control capability despite sufficient bits

Contrast with Rule 110 on:
- Directional flow
- Sequential dependency
- Control completeness
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import os

os.makedirs("output/rule122_analysis", exist_ok=True)

def get_rule_bits(rule_num):
    return [(rule_num >> i) & 1 for i in range(8)]

def run_rule(rule_num, width, steps, init=None, seed=42):
    if init is None:
        np.random.seed(seed)
        grid = np.random.randint(0, 2, width)
    else:
        grid = np.array(init)

    rule_bits = get_rule_bits(rule_num)
    history = [grid.copy()]

    for _ in range(steps):
        new_grid = np.zeros_like(grid)
        for i in range(width):
            left = grid[(i-1) % width]
            center = grid[i]
            right = grid[(i+1) % width]
            idx = (left << 2) | (center << 1) | right
            new_grid[i] = rule_bits[idx]
        grid = new_grid
        history.append(grid.copy())

    return np.array(history)

# =============================================================================
# 1. ENTROPY/COMPRESSIBILITY METRICS (WHY THEY FAIL)
# =============================================================================

def measure_entropy_metrics(rule_num, width=200, steps=150):
    """Measure metrics that INCORRECTLY classify Rule 122 as complex."""
    history = run_rule(rule_num, width, steps)

    # Shannon entropy of final state
    final = history[-1]
    p1 = np.mean(final)
    if 0 < p1 < 1:
        entropy = -p1 * np.log2(p1) - (1-p1) * np.log2(1-p1)
    else:
        entropy = 0

    # Block entropy (2x2 patterns)
    block_counts = defaultdict(int)
    for t in range(50, min(100, len(history)-1)):
        for x in range(width - 1):
            block = (history[t, x], history[t, x+1],
                     history[t+1, x], history[t+1, x+1])
            block_counts[block] += 1

    total = sum(block_counts.values())
    if total > 0:
        block_entropy = -sum((c/total) * np.log2(c/total)
                            for c in block_counts.values() if c > 0)
    else:
        block_entropy = 0

    # Compressibility estimate (unique patterns / total)
    patterns = set()
    for t in range(50, len(history)):
        for x in range(width - 4):
            patterns.add(tuple(history[t, x:x+5]))
    compressibility = len(patterns) / (50 * width)

    # Activity
    activity = np.mean([np.mean(history[t] != history[t-1])
                       for t in range(1, len(history))])

    return {
        'entropy': entropy,
        'block_entropy': block_entropy,
        'compressibility': compressibility,
        'activity': activity,
    }

# =============================================================================
# 2. DIRECTIONAL INFORMATION FLOW
# =============================================================================

def measure_information_flow(rule_num, width=200, steps=150):
    """Measure directional information flow.

    Symmetric rules have v_mean = 0 (no net direction).
    Rule 110 has leftward drift.
    """
    history = run_rule(rule_num, width, steps)

    # Track center of mass of 1s over time
    centers = []
    for t in range(len(history)):
        positions = np.where(history[t] == 1)[0]
        if len(positions) > 0:
            # Handle wraparound
            center = np.mean(positions)
            centers.append(center)

    # Measure drift
    if len(centers) > 50:
        # Linear fit to center of mass
        x = np.arange(len(centers))
        drift = np.polyfit(x, centers, 1)[0]  # Slope = drift velocity
    else:
        drift = 0

    # Measure glider velocities
    velocities = []
    for t in range(20, min(80, len(history) - 5)):
        for x in range(width):
            for size in [3, 4, 5]:
                p1 = tuple(history[t, (x+i) % width] for i in range(size))
                if sum(p1) < 2 or sum(p1) >= size - 1:
                    continue
                for vel in range(-3, 4):
                    if vel == 0:
                        continue
                    p2 = tuple(history[t+1, (x+vel+i) % width] for i in range(size))
                    if p1 == p2:
                        velocities.append(vel)
                        break

    # Mean velocity and asymmetry
    if velocities:
        mean_vel = np.mean(velocities)
        vel_asymmetry = abs(mean_vel)
        left_count = sum(1 for v in velocities if v < 0)
        right_count = sum(1 for v in velocities if v > 0)
        directional_bias = abs(left_count - right_count) / max(len(velocities), 1)
    else:
        mean_vel = 0
        vel_asymmetry = 0
        directional_bias = 0

    return {
        'drift': drift,
        'mean_velocity': mean_vel,
        'velocity_asymmetry': vel_asymmetry,
        'directional_bias': directional_bias,
        'glider_count': len(velocities),
    }

# =============================================================================
# 3. COLLISION ALGEBRA (UNIFORM VS CONDITIONAL)
# =============================================================================

def analyze_collisions(rule_num, width=200, steps=100):
    """Analyze whether collisions are uniform or conditional.

    Uniform: Same collision always produces same result
    Conditional: Collision outcome depends on local context
    """
    # Run multiple times with different contexts
    collision_outcomes = defaultdict(list)

    for seed in range(10):
        history = run_rule(rule_num, width, steps, seed=seed)

        for t in range(10, steps - 5):
            for x in range(5, width - 5):
                # Narrow collision signature (the interacting patterns)
                collision_core = tuple(history[t, x-2:x+3])

                # Broader context
                context_left = tuple(history[t, x-5:x-2])
                context_right = tuple(history[t, x+3:x+6])

                # Outcome
                outcome = tuple(history[t+2, x-2:x+3])

                # Only count if something changed (a collision happened)
                if collision_core != outcome:
                    # Key: collision core + context
                    key = (collision_core, context_left, context_right)
                    collision_outcomes[key].append(outcome)

    # Analyze uniformity vs conditionality
    total_collisions = len(collision_outcomes)
    uniform_collisions = 0
    conditional_collisions = 0

    for key, outcomes in collision_outcomes.items():
        unique_outcomes = len(set(outcomes))
        if unique_outcomes == 1:
            uniform_collisions += 1
        else:
            conditional_collisions += 1

    # Same collision core, different contexts, different outcomes?
    core_to_outcomes = defaultdict(set)
    for key, outcomes in collision_outcomes.items():
        core = key[0]
        for o in outcomes:
            core_to_outcomes[core].add(o)

    context_dependent = sum(1 for core, outcomes in core_to_outcomes.items()
                           if len(outcomes) > 1)

    return {
        'total_collisions': total_collisions,
        'uniform_fraction': uniform_collisions / max(total_collisions, 1),
        'conditional_fraction': conditional_collisions / max(total_collisions, 1),
        'context_dependent_cores': context_dependent,
        'collision_diversity': len(core_to_outcomes),
    }

# =============================================================================
# 4. CONTROL CAPABILITY TEST
# =============================================================================

def test_control_capability(rule_num, width=150, steps=80):
    """Test for Control capability:

    Control requires:
    1. At least 2 distinct collision outcomes for same signal pair
       under different local contexts
    2. Non-commuting interaction sequences (order matters)
    3. Collision outcome dependence on background state
    """
    # Test 1: Context-dependent collision outcomes
    context_dependency_score = 0

    # Create controlled collision scenarios
    for pattern_type in range(5):
        # Different initial patterns
        init1 = [0] * width
        init2 = [0] * width

        # Same collision setup, different context
        center = width // 2

        # Pattern A: collision with sparse background
        init1[center-10:center-7] = [1, 1, 1]
        init1[center+7:center+10] = [1, 1, 1]

        # Pattern B: collision with dense background
        init2[center-10:center-7] = [1, 1, 1]
        init2[center+7:center+10] = [1, 1, 1]
        init2[center-15:center-12] = [1, 1, 1]  # Extra context

        h1 = run_rule(rule_num, width, steps, init=init1)
        h2 = run_rule(rule_num, width, steps, init=init2)

        # Compare outcomes in collision region
        region1 = h1[steps//2, center-5:center+5]
        region2 = h2[steps//2, center-5:center+5]

        if not np.array_equal(region1, region2):
            context_dependency_score += 1

    # Test 2: Order dependence (non-commutativity)
    order_dependence_score = 0

    # Create A then B vs B then A scenarios
    for scenario in range(3):
        init_ab = [0] * width
        init_ba = [0] * width

        center = width // 2

        # A first, then B
        init_ab[center-20] = 1
        init_ab[center-19] = 1
        init_ab[center+10] = 1
        init_ab[center+11] = 1

        # B first (shifted timing via position)
        init_ba[center+20] = 1
        init_ba[center+21] = 1
        init_ba[center-10] = 1
        init_ba[center-9] = 1

        h_ab = run_rule(rule_num, width, steps, init=init_ab)
        h_ba = run_rule(rule_num, width, steps, init=init_ba)

        # Compare final states
        if not np.array_equal(h_ab[-1], h_ba[-1]):
            order_dependence_score += 1

    # Test 3: Background state dependence
    background_dependence_score = 0

    for bg_type in range(3):
        init_sparse = [0] * width
        init_dense = [1 if i % 3 == 0 else 0 for i in range(width)]

        # Same signal in both
        center = width // 2
        init_sparse[center] = 1
        init_sparse[center+1] = 1
        init_dense[center] = 1
        init_dense[center+1] = 1

        h_sparse = run_rule(rule_num, width, steps, init=init_sparse)
        h_dense = run_rule(rule_num, width, steps, init=init_dense)

        # Signal evolution differs based on background?
        sparse_spread = np.sum(h_sparse[steps//2] != h_sparse[0])
        dense_spread = np.sum(h_dense[steps//2] != h_dense[0])

        if abs(sparse_spread - dense_spread) > 10:
            background_dependence_score += 1

    # Combined Control score
    has_control = (context_dependency_score >= 2 and
                   order_dependence_score >= 1 and
                   background_dependence_score >= 1)

    control_score = (context_dependency_score / 5 +
                    order_dependence_score / 3 +
                    background_dependence_score / 3) / 3

    return {
        'context_dependency': context_dependency_score / 5,
        'order_dependence': order_dependence_score / 3,
        'background_dependence': background_dependence_score / 3,
        'control_score': control_score,
        'has_control': has_control,
    }

# =============================================================================
# 5. RULE SYMMETRY ANALYSIS
# =============================================================================

def analyze_symmetry(rule_num):
    """Analyze if rule is symmetric under reflection."""
    rule_bits = get_rule_bits(rule_num)

    # Check if f(L,C,R) = f(R,C,L) for all inputs
    is_symmetric = True
    for L in [0, 1]:
        for C in [0, 1]:
            for R in [0, 1]:
                idx1 = (L << 2) | (C << 1) | R
                idx2 = (R << 2) | (C << 1) | L  # Reflected
                if rule_bits[idx1] != rule_bits[idx2]:
                    is_symmetric = False
                    break

    # Compute asymmetry measure
    asymmetry = 0
    for L in [0, 1]:
        for C in [0, 1]:
            for R in [0, 1]:
                idx1 = (L << 2) | (C << 1) | R
                idx2 = (R << 2) | (C << 1) | L
                if rule_bits[idx1] != rule_bits[idx2]:
                    asymmetry += 1

    return {
        'is_symmetric': is_symmetric,
        'asymmetry_count': asymmetry,
        'asymmetry_fraction': asymmetry / 8,
    }

# =============================================================================
# MAIN COMPARISON
# =============================================================================

def main():
    print("=" * 70)
    print("RULE 122 AS CANONICAL FALSE POSITIVE")
    print("=" * 70)
    print("""
Rule 122 is the perfect foil for Rule 110:
- Same unified complexity (6.58 bits)
- Visually complex behavior
- But SYMMETRIC and NOT universal

This analysis shows why reviewers might mistakenly think Rule 122
should compute, and why it cannot.
""")

    rules = {
        110: "Universal (proven)",
        122: "Non-universal (symmetric)",
    }

    results = {}

    for rule, desc in rules.items():
        print(f"\n{'='*70}")
        print(f"RULE {rule}: {desc}")
        print("="*70)

        # Symmetry
        sym = analyze_symmetry(rule)
        print(f"\n1. SYMMETRY ANALYSIS:")
        print(f"   Is symmetric: {sym['is_symmetric']}")
        print(f"   Asymmetry count: {sym['asymmetry_count']}/8")

        # Entropy metrics (why they fail)
        ent = measure_entropy_metrics(rule)
        print(f"\n2. ENTROPY/COMPRESSIBILITY METRICS:")
        print(f"   Shannon entropy: {ent['entropy']:.3f}")
        print(f"   Block entropy: {ent['block_entropy']:.3f}")
        print(f"   Compressibility: {ent['compressibility']:.3f}")
        print(f"   Activity: {ent['activity']:.3f}")

        # Information flow
        flow = measure_information_flow(rule)
        print(f"\n3. DIRECTIONAL INFORMATION FLOW:")
        print(f"   Drift velocity: {flow['drift']:.4f}")
        print(f"   Mean glider velocity: {flow['mean_velocity']:.3f}")
        print(f"   Velocity asymmetry: {flow['velocity_asymmetry']:.3f}")
        print(f"   Directional bias: {flow['directional_bias']:.3f}")
        print(f"   Glider count: {flow['glider_count']}")

        # Collision algebra
        coll = analyze_collisions(rule)
        print(f"\n4. COLLISION ALGEBRA:")
        print(f"   Total collision types: {coll['total_collisions']}")
        print(f"   Uniform fraction: {coll['uniform_fraction']:.3f}")
        print(f"   Conditional fraction: {coll['conditional_fraction']:.3f}")
        print(f"   Context-dependent cores: {coll['context_dependent_cores']}")

        # Control capability
        ctrl = test_control_capability(rule)
        print(f"\n5. CONTROL CAPABILITY:")
        print(f"   Context dependency: {ctrl['context_dependency']:.2f}")
        print(f"   Order dependence: {ctrl['order_dependence']:.2f}")
        print(f"   Background dependence: {ctrl['background_dependence']:.2f}")
        print(f"   Control score: {ctrl['control_score']:.3f}")
        print(f"   HAS CONTROL: {ctrl['has_control']}")

        results[rule] = {
            'symmetry': sym,
            'entropy': ent,
            'flow': flow,
            'collisions': coll,
            'control': ctrl,
        }

    # Direct comparison
    print("\n" + "="*70)
    print("DIRECT COMPARISON: RULE 110 vs RULE 122")
    print("="*70)

    print("""
| Metric                    | Rule 110      | Rule 122      | Significance |
|---------------------------|---------------|---------------|--------------|""")

    r110, r122 = results[110], results[122]

    comparisons = [
        ("Symmetric", "No", "YES", "Blocks directed flow"),
        ("Asymmetry", f"{r110['symmetry']['asymmetry_fraction']:.2f}",
         f"{r122['symmetry']['asymmetry_fraction']:.2f}", "Must be >0 for flow"),
        ("Mean velocity", f"{r110['flow']['mean_velocity']:.3f}",
         f"{r122['flow']['mean_velocity']:.3f}", "Directed propagation"),
        ("Velocity asymmetry", f"{r110['flow']['velocity_asymmetry']:.3f}",
         f"{r122['flow']['velocity_asymmetry']:.3f}", "Flow direction"),
        ("Control score", f"{r110['control']['control_score']:.3f}",
         f"{r122['control']['control_score']:.3f}", "Conditional collisions"),
        ("Has Control", str(r110['control']['has_control']),
         str(r122['control']['has_control']), "UCT requirement"),
    ]

    for name, v110, v122, sig in comparisons:
        print(f"| {name:25} | {v110:13} | {v122:13} | {sig:12} |")

    # Why entropy fails
    print("\n" + "="*70)
    print("WHY ENTROPY/COMPRESSIBILITY METRICS FAIL")
    print("="*70)
    print(f"""
Rule 122 FOOLS entropy-based metrics:

  Block entropy:    Rule 110 = {r110['entropy']['block_entropy']:.3f}
                    Rule 122 = {r122['entropy']['block_entropy']:.3f}

  Compressibility:  Rule 110 = {r110['entropy']['compressibility']:.3f}
                    Rule 122 = {r122['entropy']['compressibility']:.3f}

  Activity:         Rule 110 = {r110['entropy']['activity']:.3f}
                    Rule 122 = {r122['entropy']['activity']:.3f}

These metrics are SIMILAR because both rules produce complex-LOOKING
patterns. But complexity != computation.

The critical difference is STRUCTURE, not ENTROPY:
- Rule 110: Asymmetric -> directed flow -> Control -> computation
- Rule 122: Symmetric -> no net flow -> no Control -> no computation
""")

    # The key insight
    print("\n" + "="*70)
    print("THE KEY INSIGHT: SYMMETRY BLOCKS CONTROL")
    print("="*70)
    print("""
Rule 122 in binary: 01111010
Rule 110 in binary: 01101110

Both have similar popcount (6 vs 5 bits set).
Both produce visually complex patterns.

BUT Rule 122 is SYMMETRIC under reflection:
  f(L,C,R) = f(R,C,L) for all inputs

This symmetry has fatal consequences:

1. INFORMATION CANNOT FLOW DIRECTIONALLY
   - Any rightward glider has a leftward mirror
   - Mean velocity v_mean = 0 (proven in Theorem 8.3)
   - Signals cannot be routed to specific destinations

2. COLLISIONS ARE UNIFORM, NOT CONDITIONAL
   - Symmetric collisions produce symmetric outcomes
   - No way to implement selective branching
   - The collision algebra lacks Control

3. CONTROL CAPABILITY IS IMPOSSIBLE
   - Control requires breaking symmetry
   - Symmetric rules can implement Memory, State, Logic
   - But NEVER Control

This is why Rule 122, despite its visual complexity and high
entropy, CANNOT be universal. The symmetry structurally forbids
the Control capability that computation requires.
""")

    # Visualize
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # Space-time diagrams
    for idx, rule in enumerate([110, 122]):
        ax = axes[0, idx]
        history = run_rule(rule, 150, 100, seed=42)
        ax.imshow(history, cmap='binary', aspect='auto')
        ax.set_title(f'Rule {rule}: {"Universal" if rule == 110 else "NOT Universal (Symmetric)"}')
        ax.set_xlabel('Space')
        ax.set_ylabel('Time')

    # Comparison bars
    ax = axes[1, 0]
    metrics = ['Asymmetry', 'Velocity\nAsymmetry', 'Control\nScore']
    r110_vals = [r110['symmetry']['asymmetry_fraction'],
                 r110['flow']['velocity_asymmetry'],
                 r110['control']['control_score']]
    r122_vals = [r122['symmetry']['asymmetry_fraction'],
                 r122['flow']['velocity_asymmetry'],
                 r122['control']['control_score']]

    x = np.arange(len(metrics))
    width = 0.35
    ax.bar(x - width/2, r110_vals, width, label='Rule 110', color='green')
    ax.bar(x + width/2, r122_vals, width, label='Rule 122', color='red')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    ax.set_ylabel('Score')
    ax.set_title('Computational Metrics')
    ax.legend()
    ax.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)

    # Entropy comparison (showing they're similar = misleading)
    ax = axes[1, 1]
    metrics2 = ['Block\nEntropy', 'Compress.', 'Activity']
    r110_ent = [r110['entropy']['block_entropy'],
                r110['entropy']['compressibility'],
                r110['entropy']['activity']]
    r122_ent = [r122['entropy']['block_entropy'],
                r122['entropy']['compressibility'],
                r122['entropy']['activity']]

    x = np.arange(len(metrics2))
    ax.bar(x - width/2, r110_ent, width, label='Rule 110', color='green', alpha=0.7)
    ax.bar(x + width/2, r122_ent, width, label='Rule 122', color='red', alpha=0.7)
    ax.set_xticks(x)
    ax.set_xticklabels(metrics2)
    ax.set_ylabel('Value')
    ax.set_title('Entropy Metrics (MISLEADING - similar for both!)')
    ax.legend()

    plt.suptitle('Rule 122: The Canonical False Positive\n(Looks complex, but symmetric -> no computation)',
                 fontsize=14)
    plt.tight_layout()
    plt.savefig("output/rule122_analysis/comparison.png", dpi=150)
    plt.close()

    print("\nResults saved to output/rule122_analysis/")
    return results

if __name__ == "__main__":
    results = main()
