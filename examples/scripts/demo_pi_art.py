import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import math

def get_pi_digits(n):
    # compute pi digits using integer arithmetic
    q, r, t, k, n_val, l = 1, 0, 1, 1, 3, 3
    digits = []
    while len(digits) < n:
        if 4 * q + r - t < n_val * t:
            digits.append(n_val)
            nr = 10 * (r - n_val * t)
            n_val = ((10 * (3 * q + r)) // t) - 10 * n_val
            q *= 10
            r = nr
        else:
            nr = (2 * q + r) * l
            nn = (q * (7 * k + 2) + r * l) // (t * l)
            q *= k
            t *= l
            l += 2
            k += 1
            n_val = nn
            r = nr
    return digits

def draw_pi_tree(ax, digits, max_depth=6):
    # A simple fractal tree driven by pi digits
    # Each node branches into several nodes based on the digit
    
    # We use digits to control angle and length
    digit_idx = 0
    
    def branch(x, y, angle, length, depth, width):
        nonlocal digit_idx
        if depth == 0 or digit_idx >= len(digits):
            return
            
        x_new = x + length * math.cos(angle)
        y_new = y + length * math.sin(angle)
        
        # Color based on depth
        c = plt.cm.viridis(depth / max_depth)
        
        ax.plot([x, x_new], [y, y_new], color=c, lw=width, alpha=0.8)
        
        d = digits[digit_idx]
        digit_idx += 1
        
        # Branching factor based on digit
        # 0-3: 1 branch, 4-6: 2 branches, 7-9: 3 branches
        branches = 1 if d < 4 else (2 if d < 7 else 3)
        
        if branches == 1:
            angles = [angle + (digits[digit_idx % len(digits)] - 4.5) * 0.1]
        elif branches == 2:
            angles = [angle - 0.3, angle + 0.3]
        else:
            angles = [angle - 0.4, angle, angle + 0.4]
            
        for a in angles:
            branch(x_new, y_new, a, length * 0.8, depth - 1, width * 0.7)
            
    branch(0, 0, math.pi / 2, 10, max_depth, 5)

if __name__ == "__main__":
    digits = get_pi_digits(1000)
    fig, ax = plt.subplots(figsize=(10, 10))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    draw_pi_tree(ax, digits, max_depth=10)
    ax.axis('off')
    ax.set_aspect('equal')
    plt.savefig('output_pi_tree.png', dpi=300, bbox_inches='tight', facecolor='black')
    print("Saved output_pi_tree.png")
