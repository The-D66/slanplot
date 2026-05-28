import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.cluster.hierarchy import linkage
from slanplot import STree

if __name__ == "__main__":
    np.random.seed(10)
    data = np.random.rand(75, 3)
    Z = linkage(data, 'average')
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    st = STree(Z, ax=ax, max_clust=5, layout='rectangular',
               clust_gap='on', branch_color='on', branch_highlight='on',
               class_highlight='on', class_label='on')
    st.draw()
    
    plt.savefig('output_stree.png', dpi=300, bbox_inches='tight')
    print("Saved output_stree.png")
