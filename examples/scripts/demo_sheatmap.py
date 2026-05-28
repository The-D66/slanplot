import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from slanplot.distribution.sheatmap import SHeatmap

def main():
    np.random.seed(1)
    
    # Generate data
    data = np.random.rand(10, 10) - 0.5
    data[2, 3] = np.nan
    data[4, 8] = np.nan
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 12))
    fig.patch.set_facecolor('white')
    
    # 1. Square
    SHeatmap(data, format_type='sq', ax=axes[0,0]).draw()
    axes[0,0].set_title("Square (sq)")
    
    # 2. Auto-size circle
    SHeatmap(data, format_type='acirc', ax=axes[0,1]).draw()
    axes[0,1].set_title("Auto-size Circle (acirc)")
    
    # 3. Pie
    SHeatmap(data, format_type='pie', ax=axes[1,0]).draw()
    axes[1,0].set_title("Pie Chart (pie)")
    
    # 4. Triangles
    data_corr = np.corrcoef(np.random.randn(20, 10), rowvar=False)
    pval = np.random.rand(10, 10) * 0.1
    SHeatmap(data_corr, format_type='tril', pval=pval, ax=axes[1,1]).draw()
    axes[1,1].set_title("Lower Triangle (tril) with P-values")
    
    plt.tight_layout()
    plt.savefig('/Users/the-d/.gemini/antigravity/brain/d52f437c-6ca0-4617-8907-efca4c6f0b8c/demo_sheatmap.png', dpi=300, bbox_inches='tight')
    print("Saved demo_sheatmap.png")

if __name__ == "__main__":
    main()
