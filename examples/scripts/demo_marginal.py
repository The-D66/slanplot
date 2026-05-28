import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from slanplot import MarginalPlot

if __name__ == "__main__":
    np.random.seed(42)
    Data1 = np.random.multivariate_normal([2, 3], [[1, 0], [0, 2]], 300)
    Data2 = np.random.multivariate_normal([6, 7], [[1, 0], [0, 2]], 300)
    Data3 = np.random.multivariate_normal([14, 9], [[1, 0], [0, 1]], 300)
    
    DataSet = [Data1, Data2, Data3]
    
    custom_colors = np.array([
        [122, 117, 119],
        [255, 163, 25],
        [135, 146, 73]
    ]) / 255.0
    
    labels = ['AAAAA', 'BBBBB', 'CCCCC']
    
    mp = MarginalPlot(DataSet, main_type='ellipse', top_type='kd-hist', right_type='half-violin', 
                      colors=custom_colors, labels=labels)
    mp.draw()
    
    mp.ax_main.set_xlabel('Thank U very much for your five-star review !!!', fontsize=12)
    mp.ax_main.set_ylabel('Rate me please.', fontsize=12)
    mp.ax_top.set_title('Marginal plot (Original design by slandarer)', fontsize=14)
    mp.ax_right.set_xlabel('Original design by slandarer', fontsize=12)
    
    plt.savefig('output_marginal.png', dpi=300, bbox_inches='tight')
    print("Saved output_marginal.png using slanplot module!")
