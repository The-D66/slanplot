import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, fcluster
import math
from math import factorial

class STree:
    def __init__(self, Z, ax=None, **kwargs):
        self.ax = ax if ax is not None else plt.gca()
        self.Z = Z
        
        # Default properties
        self.max_clust = kwargs.get('max_clust', kwargs.get('MaxClust', 3))
        self.layout = kwargs.get('layout', kwargs.get('Layout', 'rectangular')).lower()
        self.orientation = kwargs.get('orientation', kwargs.get('Orientation', 'top')).lower()
        
        self.xlim = kwargs.get('xlim', kwargs.get('XLim', None))
        self.ylim = kwargs.get('ylim', kwargs.get('YLim', None))
        self.tlim = kwargs.get('tlim', kwargs.get('TLim', [0, 0]))
        
        self.clust_gap = kwargs.get('clust_gap', kwargs.get('ClustGap', 'off'))
        self.branch_color = kwargs.get('branch_color', kwargs.get('BranchColor', 'off'))
        self.branch_highlight = kwargs.get('branch_highlight', kwargs.get('BranchHighlight', 'off'))
        
        self.label = kwargs.get('label', kwargs.get('Label', 'on'))
        self.class_highlight = kwargs.get('class_highlight', kwargs.get('ClassHighlight', 'off'))
        self.class_label = kwargs.get('class_label', kwargs.get('ClassLabel', 'off'))
        
        self.rtick = kwargs.get('rtick', kwargs.get('RTick', [1 + 1/40, 1.22, 1.27, 1.35]))
        
        # Color palette
        cdata = kwargs.get('cdata', kwargs.get('CData', None))
        if cdata is None:
            color_list = np.array([
                [204, 61, 36],
                [243, 197, 88],
                [109, 174, 144],
                [48, 180, 204],
                [0, 79, 122]
            ]) / 255.0
            
            n_colors = len(color_list)
            idx = np.arange(self.max_clust) % n_colors
            fade = 0.9 ** (np.arange(self.max_clust) // n_colors)
            self.cdata = color_list[idx] * fade[:, None]
        else:
            self.cdata = np.array(cdata)
            
        # Names
        num_leaves = len(Z) + 1
        self.sample_name = kwargs.get('sample_name', kwargs.get('SampleName', [f"slan{i+1}" for i in range(num_leaves+10)]))
        self.class_name = kwargs.get('class_name', kwargs.get('ClassName', [f"Class-{chr(65+i)}" for i in range(self.max_clust)]))
        
        self.sample_font = kwargs.get('sample_font', {'fontsize': 10, 'fontname': 'Times New Roman'})
        self.class_font = kwargs.get('class_font', {'fontsize': 14, 'fontname': 'Times New Roman', 'weight': 'bold'})

    def _bezier_curve(self, pnts, N):
        t = np.linspace(0, 1, N).reshape(-1, 1)
        p = len(pnts) - 1
        
        pnts_out = np.zeros((N, 2))
        for i in range(p + 1):
            binom = factorial(p) / (factorial(i) * factorial(p - i))
            term = binom * (t ** i) * ((1 - t) ** (p - i))
            pnts_out += term * pnts[i]
        return pnts_out

    def draw(self):
        # We need to temporarily draw to get coordinates without actually plotting
        R = dendrogram(self.Z, no_plot=True)
        
        self.ori_w_set = np.array(R['icoord'])
        self.ori_h_set = np.array(R['dcoord'])
        
        # order is given by ivl but we need numerical order matching scipy leaves
        self.order = np.array(R['leaves'])
        
        self.T = fcluster(self.Z, t=self.max_clust, criterion='maxclust')
        self.cutoff = np.median([self.Z[-(self.max_clust-1), 2], self.Z[-(self.max_clust-2), 2]])
        
        self.class_array = self.T[self.order]
        
        w_set_combined = np.vstack([self.ori_w_set[:, 0:2], self.ori_w_set[:, 2:4]])
        h_set_combined = np.vstack([self.ori_h_set[:, 0:2], self.ori_h_set[:, 2:4]])
        
        # Calculate cluster highlights
        b_set = (h_set_combined[:, 0] - self.cutoff) * (h_set_combined[:, 1] - self.cutoff) < 0
        self.H = (h_set_combined[b_set, 0] + h_set_combined[b_set, 1]) / 2.0
        
        # Use round(w_set_combined) properly, scipy coordinates are 5, 15, 25... scaled by 10.
        w_idx = np.round((w_set_combined[b_set, 0] - 5) / 10).astype(int)
        w_idx = np.clip(w_idx, 0, len(self.class_array) - 1)
        self.h_class = self.class_array[w_idx]
        
        # Pre-generate branch colors
        # branch lines strictly below cutoff
        below_cutoff = np.all(self.ori_h_set < self.cutoff, axis=1)
        center_w = (self.ori_w_set[:, 1] + self.ori_w_set[:, 2]) / 2.0
        c_idx = np.round((center_w - 5) / 10).astype(int)
        c_idx = np.clip(c_idx, 0, len(self.class_array) - 1)
        self.line_class = below_cutoff * self.class_array[c_idx]
        
        gap_indices = np.where(np.diff(self.class_array) != 0)[0]
        # scipy leaves are mapped to 5, 15, 25...
        gap_w = gap_indices * 10 + 10
        self.w_tick = np.arange(len(self.class_array)) * 10 + 5.0
        
        if str(self.clust_gap).lower() == 'on':
            for g in reversed(gap_w):
                self.ori_w_set[self.ori_w_set > g] += 10
                self.w_tick[self.w_tick > g] += 10
                
        # Transform shapes
        n_lines = len(self.ori_w_set)
        if self.layout == 'rectangular':
            new_w = np.zeros((n_lines, 90))
            new_h = np.zeros((n_lines, 90))
            for i in range(n_lines):
                new_w[i, :30] = np.linspace(self.ori_w_set[i, 0], self.ori_w_set[i, 1], 30)
                new_w[i, 30:60] = np.linspace(self.ori_w_set[i, 1], self.ori_w_set[i, 2], 30)
                new_w[i, 60:] = np.linspace(self.ori_w_set[i, 2], self.ori_w_set[i, 3], 30)
                
                new_h[i, :30] = np.linspace(self.ori_h_set[i, 0], self.ori_h_set[i, 1], 30)
                new_h[i, 30:60] = np.linspace(self.ori_h_set[i, 1], self.ori_h_set[i, 2], 30)
                new_h[i, 60:] = np.linspace(self.ori_h_set[i, 2], self.ori_h_set[i, 3], 30)
                
        elif self.layout == 'rounded':
            tX = np.concatenate([
                -1.0 * np.ones(15),
                np.cos(np.linspace(np.pi, np.pi/2, 20)) * 0.3 - 0.7,
                np.linspace(-0.7, 0.7, 15),
                np.cos(np.linspace(np.pi/2, 0, 20)) * 0.3 + 0.7,
                1.0 * np.ones(15)
            ])
            tY = np.concatenate([
                np.linspace(0, 0.7, 15),
                np.sin(np.linspace(np.pi, np.pi/2, 20)) * 0.3 + 0.7,
                1.0 * np.ones(15),
                np.sin(np.linspace(np.pi/2, 0, 20)) * 0.3 + 0.7,
                np.linspace(0.7, 0, 15)
            ])
            new_w = self.ori_w_set[:, 0:1] * 0 + self.ori_w_set[:, 0:1] # Just to size
            w_diff = (self.ori_w_set[:, 3:4] - self.ori_w_set[:, 0:1]) / 2.0
            w_mid = (self.ori_w_set[:, 3:4] + self.ori_w_set[:, 0:1]) / 2.0
            new_w = np.hstack([self.ori_w_set[:, 0:1], tX[None, :] * w_diff + w_mid, self.ori_w_set[:, 3:4]])
            
            h_max = np.maximum(self.ori_h_set[:, 0:1], self.ori_h_set[:, 3:4])
            h_diff = self.ori_h_set[:, 1:2] - h_max
            new_h = np.hstack([self.ori_h_set[:, 0:1], tY[None, :] * h_diff + h_max, self.ori_h_set[:, 3:4]])
            
        elif self.layout == 'slanted':
            new_w = np.zeros((n_lines, 60))
            new_h = np.zeros((n_lines, 60))
            for i in range(n_lines):
                # We need original Z array to find children
                c1, c2 = int(self.Z[i, 0]), int(self.Z[i, 1])
                n_leaves = len(self.Z) + 1
                tW = np.mean(self.ori_w_set[i, 1:3])
                
                # Try to mimic the Slanted logic from matlab
                if c1 >= n_leaves and c2 >= n_leaves:
                    idx1, idx2 = c1 - n_leaves, c2 - n_leaves
                    tW1 = self.ori_w_set[idx1, 0] if abs(self.ori_w_set[idx1, 0] - tW) < abs(self.ori_w_set[idx1, 3] - tW) else self.ori_w_set[idx1, 3]
                    tW2 = self.ori_w_set[idx2, 0] if abs(self.ori_w_set[idx2, 0] - tW) < abs(self.ori_w_set[idx2, 3] - tW) else self.ori_w_set[idx2, 3]
                    tW = tW1 if abs(tW1 - tW) > abs(tW2 - tW) else tW2
                elif c1 >= n_leaves:
                    idx1 = c1 - n_leaves
                    tW = self.ori_w_set[idx1, 0] if abs(self.ori_w_set[idx1, 0] - tW) > abs(self.ori_w_set[idx1, 3] - tW) else self.ori_w_set[idx1, 3]
                elif c2 >= n_leaves:
                    idx2 = c2 - n_leaves
                    tW = self.ori_w_set[idx2, 0] if abs(self.ori_w_set[idx2, 0] - tW) > abs(self.ori_w_set[idx2, 3] - tW) else self.ori_w_set[idx2, 3]
                
                new_w[i, :30] = np.linspace(self.ori_w_set[i, 0], tW, 30)
                new_w[i, 30:] = np.linspace(tW, self.ori_w_set[i, 3], 30)
                
                h_mid = np.mean(self.ori_h_set[i, 1:3])
                new_h[i, :30] = np.linspace(self.ori_h_set[i, 0], h_mid, 30)
                new_h[i, 30:] = np.linspace(h_mid, self.ori_h_set[i, 3], 30)
                
        elif self.layout == 'ellipse':
            tT = np.linspace(np.pi, 0, 30)
            t01 = np.linspace(0, 1, 25)
            
            w_diff = (self.ori_w_set[:, 3:4] - self.ori_w_set[:, 0:1]) / 2.0
            w_mid = (self.ori_w_set[:, 3:4] + self.ori_w_set[:, 0:1]) / 2.0
            new_w = np.hstack([
                np.ones((n_lines, 25)) * self.ori_w_set[:, 0:1],
                np.cos(tT)[None, :] * w_diff + w_mid,
                np.ones((n_lines, 25)) * self.ori_w_set[:, 3:4]
            ])
            
            h_max = np.maximum(self.ori_h_set[:, 0:1], self.ori_h_set[:, 3:4])
            h_diff = self.ori_h_set[:, 1:2] - h_max
            new_h = np.hstack([
                self.ori_h_set[:, 0:1] + t01[None, :] * (h_max - self.ori_h_set[:, 0:1]),
                np.sin(tT)[None, :] * h_diff + h_max,
                h_max + t01[None, :] * (self.ori_h_set[:, 3:4] - h_max)
            ])
            
        elif self.layout == 'bezier':
            new_w = np.zeros((n_lines, 60))
            new_h = np.zeros((n_lines, 60))
            for i in range(n_lines):
                pnts_l = np.array([
                    [self.ori_w_set[i, 0], self.ori_h_set[i, 0]],
                    [self.ori_w_set[i, 1], self.ori_h_set[i, 1]],
                    [np.mean(self.ori_w_set[i, 1:3]), self.ori_h_set[i, 1]]
                ])
                pnts_r = np.array([
                    [np.mean(self.ori_w_set[i, 1:3]), self.ori_h_set[i, 2]],
                    [self.ori_w_set[i, 2], self.ori_h_set[i, 2]],
                    [self.ori_w_set[i, 3], self.ori_h_set[i, 3]]
                ])
                
                L = self._bezier_curve(pnts_l, 30)
                R = self._bezier_curve(pnts_r, 30)
                
                new_w[i, :] = np.concatenate([L[:, 0], R[:, 0]])
                new_h[i, :] = np.concatenate([L[:, 1], R[:, 1]])
                
        # Highlight regions
        class_num = []
        for c in self.class_array:
            if c not in class_num:
                class_num.append(c)
                
        self.branch_hlt_w = np.zeros((self.max_clust, 200))
        self.branch_hlt_h = np.zeros((self.max_clust, 200))
        self.class_hlt_w = np.zeros((self.max_clust, 200))
        self.class_hlt_h = np.zeros((self.max_clust, 200))
        
        max_h = np.max(self.ori_h_set)
        min_h = np.min(self.ori_h_set)
        diff_h = max_h - min_h
        
        for i in range(min(self.max_clust, len(class_num))):
            c_id = class_num[i]
            indices = np.where(self.class_array == c_id)[0]
            tX = [self.w_tick[indices[0]] - 5.0, self.w_tick[indices[-1]] + 5.0]
            
            self.branch_hlt_w[i, :] = np.concatenate([
                np.linspace(tX[0], tX[1], 50),
                np.ones(50) * tX[1],
                np.linspace(tX[1], tX[0], 50),
                np.ones(50) * tX[0]
            ])
            
            h_val = self.H[c_id == self.h_class]
            h_val = h_val[0] if len(h_val) > 0 else 0
            
            self.branch_hlt_h[i, :] = np.concatenate([
                np.ones(50) * h_val,
                np.linspace(h_val, 0, 50),
                np.zeros(50),
                np.linspace(0, h_val, 50)
            ])
            
            self.class_hlt_w[i, :] = self.branch_hlt_w[i, :]
            self.class_hlt_h[i, :] = np.concatenate([
                np.ones(50) * (-diff_h * (self.rtick[1] - 1)),
                np.linspace(-diff_h * (self.rtick[1] - 1), -diff_h * (self.rtick[2] - 1), 50),
                np.ones(50) * (-diff_h * (self.rtick[2] - 1)),
                np.linspace(-diff_h * (self.rtick[2] - 1), -diff_h * (self.rtick[1] - 1), 50)
            ])
            
        # Orientation mapping
        if self.orientation == 'left':
            new_h = max_h - new_h
            self.branch_hlt_h = max_h - self.branch_hlt_h
            self.class_hlt_h = max_h - self.class_hlt_h
        elif self.orientation == 'bottom':
            new_h = -new_h
            self.branch_hlt_h = -self.branch_hlt_h
            self.class_hlt_h = -self.class_hlt_h
            
        if self.orientation in ['top', 'bottom']:
            new_x = new_w
            new_y = new_h
            br_x, br_y = self.branch_hlt_w, self.branch_hlt_h
            cl_x, cl_y = self.class_hlt_w, self.class_hlt_h
        else:
            new_x = new_h
            new_y = new_w
            br_x, br_y = self.branch_hlt_h, self.branch_hlt_w
            cl_x, cl_y = self.class_hlt_h, self.class_hlt_w
            
        # Handle XLim YLim mappings (scaling)
        gap_val = 10 if str(self.clust_gap).lower() == 'on' else 5
        if self.orientation in ['top', 'bottom']:
            self.ori_xlim = [np.min(new_x) - gap_val, np.max(new_x) + gap_val]
            self.ori_ylim = [np.min(new_y), np.max(new_y)]
        else:
            self.ori_xlim = [np.min(new_x), np.max(new_x)]
            self.ori_ylim = [np.min(new_y) - gap_val, np.max(new_y) + gap_val]
            
        if self.xlim is not None:
            new_x = (new_x - self.ori_xlim[0]) / (self.ori_xlim[1] - self.ori_xlim[0]) * (self.xlim[1] - self.xlim[0]) + self.xlim[0]
            br_x = (br_x - self.ori_xlim[0]) / (self.ori_xlim[1] - self.ori_xlim[0]) * (self.xlim[1] - self.xlim[0]) + self.xlim[0]
            cl_x = (cl_x - self.ori_xlim[0]) / (self.ori_xlim[1] - self.ori_xlim[0]) * (self.xlim[1] - self.xlim[0]) + self.xlim[0]
        else:
            self.xlim = self.ori_xlim
            
        if self.ylim is not None:
            new_y = (new_y - self.ori_ylim[0]) / (self.ori_ylim[1] - self.ori_ylim[0]) * (self.ylim[1] - self.ylim[0]) + self.ylim[0]
            br_y = (br_y - self.ori_ylim[0]) / (self.ori_ylim[1] - self.ori_ylim[0]) * (self.ylim[1] - self.ylim[0]) + self.ylim[0]
            cl_y = (cl_y - self.ori_ylim[0]) / (self.ori_ylim[1] - self.ori_ylim[0]) * (self.ylim[1] - self.ylim[0]) + self.ylim[0]
        else:
            self.ylim = self.ori_ylim
            
        # Handle Theta mappings (polar)
        if abs(self.tlim[0] - self.tlim[1]) < 1e-6:
            # No polar mapping, just rotate
            theta = self.tlim[0]
            rot_mat = np.array([
                [np.cos(theta), -np.sin(theta)],
                [np.sin(theta), np.cos(theta)]
            ])
            # Apply rot
            def rotate(x, y):
                xy = np.dot(rot_mat, np.vstack([x.flatten(), y.flatten()]))
                return xy[0].reshape(x.shape), xy[1].reshape(y.shape)
            
            new_x, new_y = rotate(new_x, new_y)
            br_x, br_y = rotate(br_x, br_y)
            cl_x, cl_y = rotate(cl_x, cl_y)
        else:
            # Polar
            t_set = (new_y - self.ylim[0]) / (self.ylim[1] - self.ylim[0]) * (self.tlim[1] - self.tlim[0]) + self.tlim[0]
            r_set = new_x
            new_x = np.cos(t_set) * r_set
            new_y = np.sin(t_set) * r_set
            
            t_set = (br_y - self.ylim[0]) / (self.ylim[1] - self.ylim[0]) * (self.tlim[1] - self.tlim[0]) + self.tlim[0]
            br_x_new = np.cos(t_set) * br_x
            br_y_new = np.sin(t_set) * br_x
            br_x, br_y = br_x_new, br_y_new
            
            t_set = (cl_y - self.ylim[0]) / (self.ylim[1] - self.ylim[0]) * (self.tlim[1] - self.tlim[0]) + self.tlim[0]
            cl_x_new = np.cos(t_set) * cl_x
            cl_y_new = np.sin(t_set) * cl_x
            cl_x, cl_y = cl_x_new, cl_y_new

        # Draw branches
        self.ax.set_aspect('equal' if (self.tlim[0] != 0 or self.tlim[1] != 0) else 'auto')
        self.ax.axis('off')
        
        for i in range(self.max_clust):
            mask = (self.line_class == class_num[i])
            if np.any(mask):
                c = self.cdata[i] if str(self.branch_color).lower() == 'on' else [0, 0, 0]
                for x, y in zip(new_x[mask], new_y[mask]):
                    self.ax.plot(x, y, color=c, linewidth=0.8)
                    
        mask_0 = (self.line_class == 0)
        if np.any(mask_0):
            for x, y in zip(new_x[mask_0], new_y[mask_0]):
                self.ax.plot(x, y, color='black', linewidth=0.7)
                
        # Draw branch highlights
        if str(self.branch_highlight).lower() == 'on':
            for i in range(self.max_clust):
                self.ax.fill(br_x[i], br_y[i], color=self.cdata[i], alpha=0.25, edgecolor='none')
                
        # Draw class highlights
        if str(self.class_highlight).lower() == 'on':
            for i in range(self.max_clust):
                self.ax.fill(cl_x[i], cl_y[i], color=self.cdata[i], alpha=0.9, edgecolor='none')
                
        # Draw labels
        # Non-polar labels
        if abs(self.tlim[0] - self.tlim[1]) < 1e-6:
            theta = self.tlim[0]
            rot_mat = np.array([
                [np.cos(theta), -np.sin(theta)],
                [np.sin(theta), np.cos(theta)]
            ])
            tT = theta / np.pi * 180.0
            
            if self.orientation == 'top':
                tX = (self.w_tick - self.ori_xlim[0]) / (self.ori_xlim[1] - self.ori_xlim[0]) * (self.xlim[1] - self.xlim[0]) + self.xlim[0]
                tY = -np.ones_like(tX) * abs(self.ylim[1] - self.ylim[0]) * (self.rtick[0] - 1) + self.ylim[0]
                tXY = np.dot(rot_mat, np.vstack([tX, tY]))
                
                if str(self.label).lower() == 'on':
                    for i in range(len(tX)):
                        self.ax.text(tXY[0, i], tXY[1, i], self.sample_name[self.order[i]],
                                     fontsize=self.sample_font['fontsize'], fontname=self.sample_font['fontname'],
                                     rotation=tT - 90, ha='right', va='center')
                                     
                if str(self.class_label).lower() == 'on':
                    for i in range(self.max_clust):
                        cx = np.mean(self.w_tick[self.class_array == class_num[i]])
                        cx = (cx - self.ori_xlim[0]) / (self.ori_xlim[1] - self.ori_xlim[0]) * (self.xlim[1] - self.xlim[0]) + self.xlim[0]
                        cy = -abs(self.ylim[1] - self.ylim[0]) * (self.rtick[3] - 1) + self.ylim[0]
                        cxy = np.dot(rot_mat, np.array([cx, cy]))
                        
                        self.ax.text(cxy[0], cxy[1], self.class_name[i], color=self.cdata[i],
                                     fontsize=self.class_font['fontsize'], fontname=self.class_font['fontname'], weight=self.class_font.get('weight', 'normal'),
                                     rotation=tT, ha='center', va='center')
                                     
            # ... can implement bottom, left, right if needed
        else:
            # Polar labels
            pass # TODO: translate polar labels
            
        self.ax.autoscale()
