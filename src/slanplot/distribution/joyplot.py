import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.stats import gaussian_kde

class JoyPlot:
    def __init__(self, data_list, ax=None, **kwargs):
        self.ax = ax if ax is not None else plt.gca()
        self.data_list = [np.array(d).flatten() for d in data_list]
        self.ridge_num = len(self.data_list)
        
        # Color modes
        self.color_mode = kwargs.get('color_mode', kwargs.get('ColorMode', 'Order')).capitalize()
        
        # Default palettes
        self.default_c1 = np.array([
            [0.37, 0.27, 0.56], [0.11, 0.41, 0.58], [0.21, 0.65, 0.64], [0.05, 0.52, 0.32],
            [0.45, 0.68, 0.28], [0.92, 0.67, 0.03], [0.88, 0.48, 0.01], [0.80, 0.31, 0.24],
            [0.58, 0.20, 0.43], [0.43, 0.25, 0.43]
        ])
        self.default_c2 = np.array([
            [0.00, 0.00, 0.01], [0.01, 0.01, 0.07], [0.04, 0.03, 0.13], [0.07, 0.05, 0.20],
            [0.11, 0.06, 0.28], [0.16, 0.06, 0.36], [0.22, 0.06, 0.42], [0.27, 0.06, 0.46],
            [0.32, 0.07, 0.48], [0.37, 0.09, 0.50], [0.42, 0.11, 0.50], [0.47, 0.13, 0.50],
            [0.52, 0.15, 0.50], [0.58, 0.17, 0.50], [0.63, 0.18, 0.49], [0.68, 0.20, 0.48],
            [0.73, 0.22, 0.46], [0.79, 0.24, 0.44], [0.84, 0.26, 0.42], [0.88, 0.30, 0.39],
            [0.92, 0.34, 0.37], [0.95, 0.39, 0.36], [0.97, 0.45, 0.36], [0.98, 0.51, 0.37],
            [0.99, 0.57, 0.40], [0.99, 0.63, 0.43], [0.99, 0.69, 0.47], [0.99, 0.75, 0.52],
            [0.99, 0.81, 0.57], [0.99, 0.87, 0.63], [0.98, 0.93, 0.68], [0.98, 0.99, 0.74]
        ])
        self.default_c3 = np.array([
            [0.99, 0.60, 0.60], [0.86, 0.86, 0.86], [0.60, 0.60, 0.99]
        ])
        
        if self.color_mode == 'Order':
            self.color_list = self.default_c1
        elif self.color_mode in ['X', 'Globalx', 'Kdensity']:
            self.color_list = self.default_c2
        elif self.color_mode == 'Qt':
            self.color_list = self.default_c3
        else:
            self.color_list = self.default_c1
            
        c_list = kwargs.get('color_list', kwargs.get('ColorList', None))
        if c_list is not None:
            self.color_list = np.array(c_list)
            
        self.sep = kwargs.get('sep', kwargs.get('Sep', 1/16))
        self.scatter = str(kwargs.get('scatter', kwargs.get('Scatter', 'off'))).lower()
        self.med_line = str(kwargs.get('med_line', kwargs.get('MedLine', 'off'))).lower()
        self.qt_line = str(kwargs.get('qt_line', kwargs.get('QtLine', 'off'))).lower()
        self.quantiles = kwargs.get('quantiles', kwargs.get('Quantiles', [0.25, 0.75]))
        
        self.min_x = np.min(self.data_list[0])
        self.max_x = np.max(self.data_list[0])
        for d in self.data_list:
            self.min_x = min(self.min_x, np.min(d))
            self.max_x = max(self.max_x, np.max(d))
            
    def _create_gradient_img(self, x, f, y_base, extent, mode='X'):
        cmap = LinearSegmentedColormap.from_list("custom_cmap", self.color_list)
        if mode in ['X', 'Globalx']:
            gradient = np.linspace(0, 1, 512).reshape(1, -1)
        else:
            gradient = np.linspace(0, 1, 512).reshape(-1, 1)
            
        img = self.ax.imshow(gradient, aspect='auto', cmap=cmap, extent=extent, origin='lower')
        return img

    def draw(self):
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        self.ax.yaxis.grid(True, linestyle='-', color='gray', alpha=0.3)
        self.ax.set_yticks([i * self.sep for i in range(1, self.ridge_num + 1)])
        self.ax.set_yticklabels([f"Class-{i}" for i in range(1, self.ridge_num + 1)], fontsize=13)
        self.ax.tick_params(axis='x', direction='out', labelsize=13)
        self.ax.tick_params(axis='y', length=0)
        
        # Calculate KDE limits
        max_y = 0
        min_x = float('inf')
        max_x = -float('inf')
        
        kdes = []
        for i in range(self.ridge_num):
            d = self.data_list[i]
            kde = gaussian_kde(d)
            x_eval = np.linspace(d.min() - d.std(), d.max() + d.std(), 1000)
            f_eval = kde(x_eval)
            min_x = min(min_x, x_eval.min())
            max_x = max(max_x, x_eval.max())
            max_y = max(max_y, f_eval.max())
            kdes.append((x_eval, f_eval))
            
        self.min_x_kde = min_x
        self.max_x_kde = max_x
        self.max_y_kde = max_y
        
        self.ridge_patches = []
        self.legend_handles = []
        
        # Draw from back to front (top to bottom usually, but MATLAB draws obj.ridgeNum:-1:1)
        # Wait, if y_base is i*sep, drawing from top to bottom means i goes from N to 1.
        for i in range(self.ridge_num, 0, -1):
            idx = i - 1
            d = self.data_list[idx]
            x_eval, f_eval = kdes[idx]
            y_base = i * self.sep
            
            # Scatter
            if self.scatter == 'on':
                c_idx = idx % len(self.color_list)
                c = self.color_list[c_idx] if self.color_mode == 'Order' else [0, 0, 0]
                self.ax.vlines(d, y_base - self.sep/2.5, y_base - self.sep/10, color=c, alpha=0.5, linewidth=0.8, zorder=i)
                
            y_top = f_eval + y_base
            
            if self.color_mode == 'Order':
                c = self.color_list[idx % len(self.color_list)]
                poly = self.ax.fill_between(x_eval, y_base, y_top, facecolor=c, alpha=0.5, zorder=i+0.1)
                self.ax.plot(x_eval, y_top, color=c, linewidth=0.8, zorder=i+0.2)
                self.legend_handles.append(poly)
            
            elif self.color_mode in ['X', 'Globalx', 'Kdensity']:
                poly = self.ax.fill_between(x_eval, y_base, y_top, alpha=0.0, zorder=i+0.1)
                
                if self.color_mode == 'X':
                    extent = [x_eval.min(), x_eval.max(), y_base, y_base + f_eval.max()]
                elif self.color_mode == 'Globalx':
                    extent = [self.min_x, self.max_x, y_base, y_base + f_eval.max()]
                else: # Kdensity
                    extent = [x_eval.min(), x_eval.max(), y_base, y_base + self.max_y_kde]
                    
                img = self._create_gradient_img(x_eval, f_eval, y_base, extent, mode=self.color_mode)
                img.set_zorder(i + 0.1)
                img.set_alpha(0.9)
                
                from matplotlib.path import Path
                # Get polygon path
                verts = np.vstack([x_eval, y_top]).T
                verts = np.vstack([verts, np.array([[x_eval.max(), y_base], [x_eval.min(), y_base]])])
                path = Path(verts)
                from matplotlib.patches import PathPatch
                patch = PathPatch(path, facecolor='none', edgecolor='none')
                self.ax.add_patch(patch)
                img.set_clip_path(patch)
                
                self.ax.plot(x_eval, y_top, color='black', alpha=0.9, linewidth=0.8, zorder=i+0.2)
                self.legend_handles.append(patch)
                
            elif self.color_mode == 'Qt':
                q_vals = [np.quantile(d, q) for q in self.quantiles]
                q_bounds = [-np.inf] + q_vals + [np.inf]
                for j in range(len(q_bounds) - 1):
                    mask = (x_eval >= q_bounds[j]) & (x_eval <= q_bounds[j+1])
                    if not np.any(mask): continue
                    
                    x_sub = x_eval[mask]
                    y_sub = y_top[mask]
                    
                    # Ensure continuity
                    if j > 0:
                        x_sub = np.insert(x_sub, 0, q_bounds[j])
                        y_sub = np.insert(y_sub, 0, np.interp(q_bounds[j], x_eval, y_top))
                    if j < len(q_bounds) - 2:
                        x_sub = np.append(x_sub, q_bounds[j+1])
                        y_sub = np.append(y_sub, np.interp(q_bounds[j+1], x_eval, y_top))
                        
                    c = self.color_list[j % len(self.color_list)]
                    self.ax.fill_between(x_sub, y_base, y_sub, facecolor=c, alpha=0.9, zorder=i+0.1)
                    
                self.ax.plot(x_eval, y_top, color='black', alpha=0.9, linewidth=0.8, zorder=i+0.2)
                
            # Median line
            if self.med_line == 'on':
                med = np.median(d)
                med_y = np.interp(med, x_eval, y_top)
                self.ax.plot([med, med], [y_base, med_y], 'k--', linewidth=1, zorder=i+0.3)
                
            # Quantile lines
            if self.qt_line == 'on':
                q_vals = [np.quantile(d, q) for q in self.quantiles]
                for qv in q_vals:
                    qy = np.interp(qv, x_eval, y_top)
                    self.ax.plot([qv, qv], [y_base, qy], 'k-', color=[0,0,0,0.8], linewidth=1, zorder=i+0.3)
                    
        # Limits
        self.ax.set_ylim(self.sep / 2, (self.ridge_num + 1) * self.sep)
        self.ax.set_xlim(min_x, max_x)
        
    def get_legend_handles(self):
        if self.color_mode == 'Qt':
            import matplotlib.patches as mpatches
            return [mpatches.Patch(color=self.color_list[i % len(self.color_list)], alpha=0.9) for i in range(len(self.quantiles)+1)]
        else:
            return self.legend_handles[::-1]
