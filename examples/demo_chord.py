import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from slanplot import ChordDiagram

if __name__ == "__main__":
    data_mat = np.array([
        [2, 0, 1, 2, 5, 1, 2],
        [3, 5, 1, 4, 2, 0, 1],
        [4, 0, 5, 5, 2, 4, 3]
    ])
    col_name = ['B1','G2','G3','G4','G5','G6','G7']
    row_name = ['S1','S2','S3']
    
    fig, ax = plt.subplots(figsize=(10, 10))
    cc = ChordDiagram(data_mat, row_name=row_name, col_name=col_name, ax=ax)
    cc.draw()
    cc.set_font(fontsize=17, fontname='Cambria')
    cc.tick_state('on')
    
    plt.savefig('output_chord.png', dpi=300, bbox_inches='tight')
    print("Saved output_chord.png using slanplot module!")
