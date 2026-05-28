import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from slanplot import CircularTree

if __name__ == "__main__":
    np.random.seed(1)
    
    list_a = [f"Class-{np.random.randint(65, 70)}" for _ in range(500)]
    list_b = [f"Type-{np.random.randint(97, 100)}" for _ in range(500)]
    list_c = [f"Object-{i+1:03d}" for i in range(500)]
    
    data_list = np.column_stack([list_a, list_b, list_c])
    value = np.ones(500)
    
    fig, ax = plt.subplots(figsize=(12, 12))
    ct = CircularTree(data_list, value=value, ax=ax, disp_end_labels='on')
    ct.draw()
    
    plt.savefig('output_circ_tree.png', dpi=300, bbox_inches='tight')
    print("Saved output_circ_tree.png")
