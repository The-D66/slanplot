import matplotlib.pyplot as plt
import numpy as np

class HatchedBar:
    def __init__(self, data, ax=None, hatch_type=None, horizontal=False, **kwargs):
        """
        Creates a hatched bar chart.
        data: 1D or 2D array-like. If 2D, rows are groups, columns are categories.
        hatch_type: list of hatch patterns.
        horizontal: boolean, whether to draw horizontal bars.
        kwargs: other arguments to pass to ax.bar / ax.barh
        """
        self.ax = ax if ax is not None else plt.gca()
        self.data = np.atleast_2d(data)
        self.horizontal = horizontal
        self.kwargs = kwargs
        
        # Default hatches
        if hatch_type is None:
            hatch_type = ['/', '\\', '.', '-', 'x']
        
        # Map MATLAB hatch symbols to Matplotlib's
        hatch_map = {'_': '-', 'w': '', 'k': '', 'g': ''}
        self.hatch_type = [hatch_map.get(h, h) for h in hatch_type]
        
    def draw(self):
        num_groups, num_categories = self.data.shape
        
        if num_categories > len(self.hatch_type):
            self.hatch_type = (self.hatch_type * (num_categories // len(self.hatch_type) + 1))[:num_categories]
            
        bar_width = 0.8 / num_categories
        indices = np.arange(num_groups)
        
        bars = []
        for i in range(num_categories):
            pos = indices - 0.4 + (i + 0.5) * bar_width
            hatch = self.hatch_type[i]
            
            # Default style: white face, black edge, black hatch
            kwargs = self.kwargs.copy()
            if 'facecolor' not in kwargs and 'color' not in kwargs:
                kwargs['facecolor'] = 'white'
            if 'edgecolor' not in kwargs:
                kwargs['edgecolor'] = 'black'
            
            if self.horizontal:
                b = self.ax.barh(pos, self.data[:, i], height=bar_width, hatch=hatch*2, **kwargs) # hatch*2 for density
            else:
                b = self.ax.bar(pos, self.data[:, i], width=bar_width, hatch=hatch*2, **kwargs)
            bars.append(b)
            
        return bars

class HatchedPie:
    def __init__(self, data, ax=None, hatch_type=None, **kwargs):
        """
        Creates a hatched pie chart.
        data: 1D array-like.
        hatch_type: list of hatch patterns.
        """
        self.ax = ax if ax is not None else plt.gca()
        self.data = np.array(data).flatten()
        self.kwargs = kwargs
        
        if hatch_type is None:
            hatch_type = ['/', '\\', '.', '-', 'x']
            
        hatch_map = {'_': '-', 'w': '', 'k': '', 'g': ''}
        self.hatch_type = [hatch_map.get(h, h) for h in hatch_type]
        
    def draw(self):
        num_categories = len(self.data)
        if num_categories > len(self.hatch_type):
            self.hatch_type = (self.hatch_type * (num_categories // len(self.hatch_type) + 1))[:num_categories]
            
        kwargs = self.kwargs.copy()
        if 'colors' not in kwargs:
            kwargs['colors'] = ['white'] * num_categories
        if 'wedgeprops' not in kwargs:
            kwargs['wedgeprops'] = {'edgecolor': 'black', 'linewidth': 1}
            
        wedges, texts = self.ax.pie(self.data, **kwargs)
        
        for i, wedge in enumerate(wedges):
            wedge.set_hatch(self.hatch_type[i]*2)
            
        return wedges, texts
