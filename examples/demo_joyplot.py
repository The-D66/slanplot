import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from slanplot import JoyPlot

if __name__ == "__main__":
    np.random.seed(31)
    def rx():
        return np.concatenate([
            np.random.normal(np.random.rand()*20, np.random.rand()*5 + 1, 50),
            np.random.normal(np.random.rand()*20, np.random.rand()*5 + 1, 50)
        ])
        
    data = [rx() for _ in range(9)]
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 6))
    
    jp1 = JoyPlot(data, color_mode='order', ax=axes[0])
    jp1.draw()
    axes[0].set_title('ColorMode: Order')
    
    jp2 = JoyPlot(data, color_mode='X', scatter='on', med_line='on', ax=axes[1])
    jp2.draw()
    axes[1].set_title('ColorMode: X')
    
    jp3 = JoyPlot(data, color_mode='Qt', qt_line='on', quantiles=[0.25, 0.75], ax=axes[2])
    jp3.draw()
    axes[2].set_title('ColorMode: Qt')
    
    plt.savefig('output_joyplot.png', dpi=300, bbox_inches='tight')
    print("Saved output_joyplot.png")
