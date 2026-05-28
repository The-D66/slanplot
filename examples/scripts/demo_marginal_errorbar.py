import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from slanplot.distribution.marginal import MarginalPlot

def main():
    np.random.seed(42)
    # 模拟数据
    # Python 3.7+ np.random.multivariate_normal is the correct one:
    Data1 = np.random.multivariate_normal([2, 3], [[1, 0], [0, 2]], 300)
    Data2 = np.random.multivariate_normal([6, 7], [[1, 0], [0, 2]], 300)
    Data3 = np.random.multivariate_normal([14, 9], [[1, 0], [0, 1]], 300)
    Data1 = np.random.multivariate_normal([2, 3], [[1, 0], [0, 2]], 300)
    Data2 = np.random.multivariate_normal([6, 7], [[1, 0], [0, 2]], 300)
    Data3 = np.random.multivariate_normal([14, 9], [[1, 0], [0, 1]], 300)
    
    DataSet = [Data1, Data2, Data3]
    labels = ['Class-1', 'Class-2', 'Class-3']
    colors = ['#8EBAD1', '#405B67', '#F15A62']
    
    # 绘制左半部分的图: errorbar, rug, hist
    MP = MarginalPlot(DataSet, main_type='errorbar', top_type='rug', right_type='hist', 
                      labels=labels, colors=colors, figsize=(7, 7))
    MP.draw()
    
    # 调整坐标轴的风格
    MP.ax_main.set_xlabel('Main XXXXX', fontsize=12)
    MP.ax_main.set_ylabel('Main YYYYY', fontsize=12)
    MP.ax_top.set_ylabel('X-axis data statistics', fontsize=12)
    MP.ax_right.set_xlabel('Y-axis data statistics', fontsize=12)
    
    plt.savefig("output_marginal_errorbar.png", dpi=300, bbox_inches='tight')
    print("Saved demo_marginal_errorbar.png")

if __name__ == "__main__":
    main()
