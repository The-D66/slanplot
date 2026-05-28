import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from slanplot.distribution.venn import VennDiagram

def main():
    np.random.seed(1)
    
    # Generate random Boolean matrix: 500 samples, 6 sets (venn lib supports up to 6)
    bool_set = np.random.randint(0, 2, size=(500, 6))
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    fig.patch.set_facecolor('white')
    
    # 3 sets
    vd3 = VennDiagram(bool_set[:, :3], labels=['A', 'B', 'C'], ax=axes[0])
    vd3.draw()
    axes[0].set_title("3 Sets")
    
    # 5 sets
    vd5 = VennDiagram(bool_set[:, :5], labels=['A', 'B', 'C', 'D', 'E'], ax=axes[1])
    vd5.draw()
    axes[1].set_title("5 Sets")
    
    plt.savefig('/Users/the-d/.gemini/antigravity/brain/d52f437c-6ca0-4617-8907-efca4c6f0b8c/demo_venn.png', dpi=300, bbox_inches='tight')
    print("Saved demo_venn.png")

if __name__ == "__main__":
    main()
