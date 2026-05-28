import matplotlib.pyplot as plt
import numpy as np
from venn import venn

class VennDiagram:
    def __init__(self, data, labels=None, ax=None, **kwargs):
        """
        Creates a Venn Diagram.
        data: A boolean matrix (samples x sets).
        labels: List of names for the sets.
        """
        self.ax = ax
        self.data = np.atleast_2d(data)
        self.kwargs = kwargs
        
        num_sets = self.data.shape[1]
        
        if labels is None:
            self.labels = [chr(65 + i) for i in range(num_sets)]
        else:
            self.labels = labels
            
    def draw(self):
        num_sets = self.data.shape[1]
        if num_sets > 6:
            print("Warning: Venn diagram supports a maximum of 6 sets. Truncating to 6 sets.")
            self.data = self.data[:, :6]
            self.labels = self.labels[:6]
            num_sets = 6
            
        dataset_dict = {}
        for i in range(num_sets):
            # Find indices where the item belongs to set i
            indices = np.where(self.data[:, i])[0]
            dataset_dict[self.labels[i]] = set(indices)
            
        kwargs = self.kwargs.copy()
        if self.ax is not None:
            kwargs['ax'] = self.ax
            
        # Optional styling defaults
        if 'cmap' not in kwargs:
            kwargs['cmap'] = 'viridis'
            
        ax = venn(dataset_dict, **kwargs)
        return ax
