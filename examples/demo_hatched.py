import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from slanplot.distribution.hatched import HatchedBar, HatchedPie

def main():
    # Demo 1: Bar
    y = np.array([
        [2, 2, 3, 2, 5],
        [2, 5, 6, 2, 5],
        [9, 8, 9, 2, 5]
    ])
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor('white')
    
    hb = HatchedBar(y, ax=axes[0], hatch_type=['/', '\\', '.', '_', 'x'])
    hb.draw()
    axes[0].set_xticks(np.arange(3))
    axes[0].set_xticklabels(['1', '2', '3'])
    axes[0].set_title('Hatched Bar Chart')
    
    # Demo 2: Pie
    x = [1, 3, 0.5, 2.5, 2]
    hp = HatchedPie(x, ax=axes[1], hatch_type=['/', '.', '|', '+', 'x'])
    hp.draw()
    axes[1].set_title('Hatched Pie Chart')
    
    plt.savefig('/Users/the-d/.gemini/antigravity/brain/d52f437c-6ca0-4617-8907-efca4c6f0b8c/demo1_hatched.png', dpi=300, bbox_inches='tight')
    print("Saved demo1_hatched.png")

if __name__ == "__main__":
    main()
