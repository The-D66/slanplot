import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sys
from slanplot import PiTree

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

if __name__ == "__main__":
    np.random.seed(42)
    Pi = np.array([3] + get_pi_digits(800))
    pos9 = np.where(Pi == 9)[0]
    pos9 = np.insert(pos9, 0, -1)
    
    fig, ax = plt.subplots(figsize=(9, 9))
    ax.set_facecolor('white')
    fig.patch.set_facecolor('white')
    ax.set_aspect('equal')
    ax.axis('off')
    
    for j in range(1, 4):  # just do a few to save time, MATLAB did 8x11=88
        for i in range(1, 5):
            n = i + (j - 1) * 11
            if n <= 85 and n < len(pos9) - 1:
                tPi = Pi[pos9[n]+1 : pos9[n+1]+1]
                if len(tPi) > 2:
                    pt = PiTree(tPi, [0 + i * 3, 0 - j * 4], True, ax=ax)
                    pt.draw()
                else:
                    pt = PiTree(np.concatenate(([Pi[pos9[n]]], tPi)), [0 + i * 3, 0 - j * 4], False, ax=ax)
                    pt.draw()
                    
    plt.savefig('output_pitree.png', dpi=300, bbox_inches='tight')
    print("Saved output_pitree.png")
