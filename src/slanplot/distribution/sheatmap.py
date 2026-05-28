import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import numpy as np
from matplotlib.patches import Polygon, Circle, Wedge, RegularPolygon

class SHeatmap:
    def __init__(self, data, format_type='sq', ax=None, pval=None, cmap=None, **kwargs):
        self.data = np.array(data, dtype=float)
        self.format_type = format_type
        self.ax = ax if ax is not None else plt.gca()
        self.pval = np.array(pval, dtype=float) if pval is not None else None
        self.kwargs = kwargs
        self.max_v = np.nanmax(np.abs(self.data))
        if self.max_v == 0:
            self.max_v = 1
            
        self.has_negative = np.any(self.data < 0)
        
        if cmap is None:
            if self.has_negative:
                self.cmap = plt.get_cmap('RdBu_r')
            else:
                self.cmap = plt.get_cmap('YlGnBu')
        else:
            self.cmap = plt.get_cmap(cmap) if isinstance(cmap, str) else cmap
            
        self.norm = mcolors.Normalize(vmin=-self.max_v if self.has_negative else 0, vmax=self.max_v)
        
        # Grid settings
        self.rows, self.cols = self.data.shape
        self.patches = []
        self.texts = []
        
        self.mask_type = kwargs.get('mask_type', 'full') # 'full', 'triu', 'tril', 'triu0', 'tril0'
        
    def _is_visible(self, r, c):
        if self.mask_type == 'triu' and c < r: return False
        if self.mask_type == 'tril' and c > r: return False
        if self.mask_type == 'triu0' and c <= r: return False
        if self.mask_type == 'tril0' and c >= r: return False
        return True

    def draw(self):
        self.ax.set_aspect('equal')
        self.ax.invert_yaxis()
        
        self.ax.set_xlim(-0.5, self.cols - 0.5)
        self.ax.set_ylim(self.rows - 0.5, -0.5)
        self.ax.set_xticks(np.arange(self.cols))
        self.ax.set_yticks(np.arange(self.rows))
        
        # 移除外边框，保持和原图无框风格一致
        for spine in self.ax.spines.values():
            spine.set_visible(False)
        self.ax.tick_params(top=False, bottom=False, left=False, right=False)
        
        # Draw background grid
        for r in range(self.rows + 1):
            self.ax.axhline(r - 0.5, color='lightgray', linewidth=0.5)
        for c in range(self.cols + 1):
            self.ax.axvline(c - 0.5, color='lightgray', linewidth=0.5)
            
        for r in range(self.rows):
            for c in range(self.cols):
                if not self._is_visible(r, c):
                    continue
                    
                val = self.data[r, c]
                if np.isnan(val):
                    self.ax.text(c, r, '×', ha='center', va='center', fontsize=14, color='gray')
                    continue
                    
                ratio = abs(val) / self.max_v
                color = self.cmap(self.norm(val))
                
                ft = self.format_type
                p = None
                
                if ft == 'sq':
                    p = plt.Rectangle((c - 0.48, r - 0.48), 0.96, 0.96, facecolor=color)
                elif ft == 'asq':
                    size = 0.96 * ratio
                    p = plt.Rectangle((c - size/2, r - size/2), size, size, facecolor=color)
                elif ft == 'circ':
                    p = Circle((c, r), 0.46, facecolor=color)
                elif ft == 'acirc':
                    p = Circle((c, r), 0.46 * ratio, facecolor=color)
                elif ft == 'pie':
                    bg = Circle((c, r), 0.46, facecolor='white', edgecolor='gray')
                    self.ax.add_patch(bg)
                    theta2 = 90 - (ratio * 360)
                    p = Wedge((c, r), 0.46, theta2, 90, facecolor=color, edgecolor='gray')
                elif ft == 'donut':
                    bg = Wedge((c, r), 0.46, 0, 360, width=0.23, facecolor='white', edgecolor='gray')
                    self.ax.add_patch(bg)
                    theta2 = 90 - (ratio * 360)
                    p = Wedge((c, r), 0.46, theta2, 90, width=0.23, facecolor=color, edgecolor='gray')
                elif ft == 'hex':
                    p = RegularPolygon((c, r), numVertices=6, radius=0.48*ratio, orientation=np.pi/6, facecolor=color)
                elif ft in ['tril', 'trill']:
                    p = Polygon([[c-0.5, r-0.5], [c+0.5, r+0.5], [c-0.5, r+0.5]], facecolor=color)
                elif ft in ['triur', 'triu']:
                    p = Polygon([[c-0.5, r-0.5], [c+0.5, r-0.5], [c+0.5, r+0.5]], facecolor=color)
                elif ft == 'triul':
                    p = Polygon([[c-0.5, r+0.5], [c-0.5, r-0.5], [c+0.5, r-0.5]], facecolor=color)
                elif ft == 'trilr':
                    p = Polygon([[c-0.5, r+0.5], [c+0.5, r-0.5], [c+0.5, r+0.5]], facecolor=color)
                else:
                    # fallback to sq
                    p = plt.Rectangle((c - 0.48, r - 0.48), 0.96, 0.96, facecolor=color)
                    
                if p is not None:
                    self.ax.add_patch(p)
                    self.patches.append(p)
                    
                # Add stars
                if self.pval is not None and not np.isnan(self.pval[r, c]):
                    pv = self.pval[r, c]
                    stars = ''
                    if pv < 0.001: stars = '***'
                    elif pv < 0.01: stars = '**'
                    elif pv < 0.05: stars = '*'
                    
                    if stars:
                        self.ax.text(c, r, stars, ha='center', va='center', fontsize=12, color='black' if val > 0 else 'white')
                        
        sm = cm.ScalarMappable(cmap=self.cmap, norm=self.norm)
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=self.ax, fraction=0.046, pad=0.04)
        cbar.outline.set_visible(False)
        
        return self
