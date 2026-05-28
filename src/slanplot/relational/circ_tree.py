import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class CircularTree:
    def __init__(self, data_list, ax=None, **kwargs):
        self.ax = ax if ax is not None else plt.gca()
        
        # Parse data_list
        if isinstance(data_list, pd.DataFrame):
            self.data_list = data_list.values.astype(str)
        else:
            self.data_list = np.array(data_list).astype(str)
            
        self.curvature = kwargs.get('curvature', kwargs.get('Curvature', 1.0))
        self.disp_end_nodes = kwargs.get('disp_end_nodes', kwargs.get('DispEndNodes', 'off'))
        self.disp_end_labels = kwargs.get('disp_end_labels', kwargs.get('DispEndLabels', 'off'))
        self.node_size_lim = kwargs.get('node_size_lim', kwargs.get('NodeSizeLim', [0.01, 0.4]))
        self.edge_width_lim = kwargs.get('edge_width_lim', kwargs.get('EdgeWidthLim', [0.01, 0.4]))
        self.node_alpha = kwargs.get('node_alpha', kwargs.get('NodeAlpha', 1.0))
        self.edge_alpha = kwargs.get('edge_alpha', kwargs.get('EdgeAlpha', 0.3))
        
        self.value = kwargs.get('value', kwargs.get('Value', None))
        
        # Clean empty strings propagating to the right
        self.sz = self.data_list.shape
        for i in range(self.sz[0]):
            for j in range(self.sz[1]):
                if self.data_list[i, j] == '' or self.data_list[i, j] == 'nan':
                    self.data_list[i, j:] = ''
                    break
                    
        if self.sz[1] == 2:
            self.edge_width_lim = [0.02, 0.06]
            self.node_size_lim = [0.07, 0.15]
            
        if self.value is None:
            self.value = np.ones(self.sz[0])
        else:
            self.value = np.abs(np.array(self.value))
            
        empty_mask = (self.data_list[:, -1] == '')
        self.value[empty_mask] = 0
        
        non_zero_vals = self.value[self.value != 0]
        self.min_value = np.min(non_zero_vals) if len(non_zero_vals) > 0 else 0
        
        # Default colormap
        self.cdata = np.array([
            [110,110,110], [127, 91, 93], [187,128,110], [197,173,143],  [59, 71,111], [104, 95,126],  
            [76,103, 86], [112,112,124],  [72, 39, 24], [197,119,106], [160,126, 88], [238,208,146]
        ]) / 255.0
        
        # Step 1 & 2: Hierarchical encoding
        self.base_id_list = np.zeros(self.sz, dtype=int)
        self.base_layer_nodes = []
        
        for i in range(self.sz[1]):
            unique_nodes, indices = np.unique(self.data_list[:, i], return_inverse=True)
            self.base_layer_nodes.append(unique_nodes)
            self.base_id_list[:, i] = indices
            
        self.id_list = np.zeros(self.sz, dtype=int)
        self.layer_nodes = []
        self.layer_sizes = []
        
        for i in range(self.sz[1]):
            # Get unique rows up to column i
            unique_rows, indices = np.unique(self.base_id_list[:, :i+1], axis=0, return_inverse=True)
            # The node names for this layer
            nodes_for_layer = self.base_layer_nodes[i][unique_rows[:, i]]
            self.layer_nodes.append(nodes_for_layer)
            self.layer_sizes.append(len(unique_rows))
            self.id_list[:, i] = indices
            
        # Sort by hierarchical path
        # In python, argsort on records or lexicographical sort
        sort_order = np.lexsort([self.id_list[:, i] for i in range(self.sz[1]-1, -1, -1)])
        self.id_list = self.id_list[sort_order]
        self.value = self.value[sort_order]
        
        self.max_value = self.min_value
        for i in range(self.layer_sizes[0]):
            self.max_value = max(self.max_value, np.sum(self.value[self.id_list[:, 0] == i]))
            
        # Append random colors if needed
        if self.layer_sizes[0] + 1 > len(self.cdata):
            extra_colors = np.random.rand(self.layer_sizes[0] + 1, 3) * 0.6 + 0.3
            self.cdata = np.vstack([self.cdata, extra_colors])

    def _circ_mean_theta(self, theta):
        x = np.mean(np.cos(theta))
        y = np.mean(np.sin(theta))
        return np.mod(np.arctan2(y, x), 2*np.pi)
        
    def _thicken_polyline(self, XY, w):
        X = XY[:, 0]
        Y = XY[:, 1]
        n = len(X)
        dx = np.zeros(n)
        dy = np.zeros(n)
        
        if n > 2:
            dx[1:-1] = X[2:] - X[:-2]
            dy[1:-1] = Y[2:] - Y[:-2]
        if n > 1:
            dx[0] = X[1] - X[0]
            dy[0] = Y[1] - Y[0]
            dx[-1] = X[-1] - X[-2]
            dy[-1] = Y[-1] - Y[-2]
            
        length = np.sqrt(dx**2 + dy**2)
        length[length == 0] = np.finfo(float).eps
        dx = dx / length
        dy = dy / length
        
        nx = -dy
        ny = dx
        
        XL = X + nx * w / 2
        YL = Y + ny * w / 2
        XR = X - nx * w / 2
        YR = Y - ny * w / 2
        
        return np.column_stack([XL, YL]), np.column_stack([XR, YR])
        
    def _bezier_curve(self, pnts, N=50):
        t = np.linspace(0, 1, N).reshape(-1, 1)
        p = len(pnts) - 1
        
        from math import factorial
        pnts_out = np.zeros((N, 2))
        for i in range(p + 1):
            binom = factorial(p) / (factorial(i) * factorial(p - i))
            term = binom * (t ** i) * ((1 - t) ** (p - i))
            pnts_out += term * pnts[i]
        return pnts_out

    def draw(self):
        self.curvature = np.clip(self.curvature, 0, 1)
        
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        for spine in self.ax.spines.values():
            spine.set_visible(False)
        self.ax.set_aspect('equal')
        
        pad = 0.5 if str(self.disp_end_labels).lower() == 'on' else 0.1
        limit = self.sz[1] + pad
        self.ax.set_xlim([-limit, limit])
        self.ax.set_ylim([-limit, limit])
        
        theta_set_raw = np.linspace(0, 2*np.pi, self.sz[0] + 1)[:-1]
        self.theta_set = theta_set_raw
        
        # Center Root node
        self.ax.scatter([0], [0], s=0, color='none') # Just to keep bounds
        
        max_node_sz = max(np.abs(self.node_size_lim))
        
        # 1. Root edges
        for i in range(self.layer_sizes[0]):
            if self.layer_nodes[0][i] != '':
                mask = self.id_list[:, 0] == i
                t_theta = self._circ_mean_theta(self.theta_set[mask])
                t_val = np.sum(self.value[mask])
                
                denom = self.max_value - self.min_value
                if denom == 0: denom = 1
                t_width = (t_val - self.min_value) / denom * abs(self.edge_width_lim[1] - self.edge_width_lim[0]) + min(np.abs(self.edge_width_lim))
                
                pts = np.array([
                    [np.cos(t_theta), np.sin(t_theta)],
                    [0.3 * self.curvature, -0.5 * self.curvature],
                    [0.0, 0.0]
                ])
                L, R = self._thicken_polyline(pts, t_width)
                LL = self._bezier_curve(L, 50)
                RR = self._bezier_curve(R, 50)
                
                px = np.concatenate([LL[:, 0], RR[::-1, 0]])
                py = np.concatenate([LL[:, 1], RR[::-1, 1]])
                
                self.ax.fill(px, py, color=self.cdata[i+1], alpha=self.edge_alpha, edgecolor='none', zorder=1)
                
        # 2. Intermediate edges
        if self.sz[1] > 1:
            for k in range(1, self.sz[1]):
                for i in range(self.layer_sizes[k]):
                    if self.layer_nodes[k][i] != '':
                        mask_k = self.id_list[:, k] == i
                        if not np.any(mask_k):
                            continue
                            
                        # Find parent id (tId) and root id (CId)
                        idx = np.where(mask_k)[0][0]
                        tId = self.id_list[idx, k-1]
                        CId = self.id_list[idx, 0]
                        
                        mask_parent = self.id_list[:, k-1] == tId
                        tThetaA = self._circ_mean_theta(self.theta_set[mask_parent])
                        tThetaB = self._circ_mean_theta(self.theta_set[mask_k])
                        
                        XYA = np.array([np.cos(tThetaA), np.sin(tThetaA)]) * k
                        XYB = np.array([np.cos(tThetaB), np.sin(tThetaB)]) * (k + 1)
                        XYM = (XYA + XYB) / 2.0
                        
                        XYAm = np.array([np.cos(tThetaA), np.sin(tThetaA)]) * (k + 0.3) * self.curvature + (1 - self.curvature) * XYM
                        XYBm = np.array([np.cos(tThetaB), np.sin(tThetaB)]) * (k + 0.7) * self.curvature + (1 - self.curvature) * XYM
                        
                        t_val = np.sum(self.value[mask_k])
                        denom = self.max_value - self.min_value
                        if denom == 0: denom = 1
                        t_width = (t_val - self.min_value) / denom * abs(self.edge_width_lim[1] - self.edge_width_lim[0]) + min(np.abs(self.edge_width_lim))
                        
                        pts = np.array([XYB, XYBm, XYAm, XYA])
                        L, R = self._thicken_polyline(pts, t_width)
                        LL = self._bezier_curve(L, 50)
                        RR = self._bezier_curve(R, 50)
                        
                        px = np.concatenate([LL[:, 0], RR[::-1, 0]])
                        py = np.concatenate([LL[:, 1], RR[::-1, 1]])
                        
                        self.ax.fill(px, py, color=self.cdata[CId+1], alpha=self.edge_alpha, edgecolor='none', zorder=1)
                        
        # 3. Root Node
        circle = plt.Circle((0, 0), max_node_sz / 2, color=self.cdata[0], alpha=self.node_alpha, zorder=2)
        self.ax.add_patch(circle)
        
        # 4. Layer Nodes and Labels
        for k in range(self.sz[1]):
            if k < self.sz[1] - 1 or str(self.disp_end_nodes).lower() == 'on' or str(self.disp_end_labels).lower() == 'on':
                for i in range(self.layer_sizes[k]):
                    if self.layer_nodes[k][i] != '':
                        mask = self.id_list[:, k] == i
                        if not np.any(mask):
                            continue
                            
                        t_val = np.sum(self.value[mask])
                        idx = np.where(mask)[0][0]
                        CId = self.id_list[idx, 0]
                        tThetaB = self._circ_mean_theta(self.theta_set[mask])
                        
                        denom = self.max_value - self.min_value
                        if denom == 0: denom = 1
                        t_width = (t_val - self.min_value) / denom * abs(self.node_size_lim[1] - self.node_size_lim[0]) + min(np.abs(self.node_size_lim))
                        
                        cx = np.cos(tThetaB) * (k + 1)
                        cy = np.sin(tThetaB) * (k + 1)
                        
                        if k < self.sz[1] - 1 or str(self.disp_end_nodes).lower() == 'on':
                            circle = plt.Circle((cx, cy), t_width / 2, color=self.cdata[CId+1], alpha=self.node_alpha, zorder=2)
                            self.ax.add_patch(circle)
                            
                        if k < self.sz[1] - 1 or str(self.disp_end_labels).lower() == 'on':
                            lbl_x = np.cos(tThetaB) * (k + 1 + t_width/2 + 0.1)
                            lbl_y = np.sin(tThetaB) * (k + 1 + t_width/2 + 0.1)
                            
                            rot = tThetaB / np.pi * 180.0
                            if 90 < rot < 270:
                                self.ax.text(lbl_x, lbl_y, self.layer_nodes[k][i], 
                                             fontsize=10, fontname='Times New Roman',
                                             rotation=rot + 180, ha='right', va='center', color=self.cdata[CId+1])
                            else:
                                self.ax.text(lbl_x, lbl_y, self.layer_nodes[k][i], 
                                             fontsize=10, fontname='Times New Roman',
                                             rotation=rot, ha='left', va='center', color=self.cdata[CId+1])
