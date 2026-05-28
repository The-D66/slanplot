import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator

class SSankey:
    def __init__(self, source, target, value, ax=None, **kwargs):
        self.source = source
        self.target = target
        self.value = value
        
        self.ax = ax if ax is not None else plt.gca()
        # Accept both camelCase (for backward compat) and snake_case
        self.rendering_method = kwargs.get('rendering_method', kwargs.get('RenderingMethod', 'interp'))
        self.label_location = kwargs.get('label_location', kwargs.get('LabelLocation', 'left'))
        self.align = kwargs.get('align', kwargs.get('Align', 'center'))
        self.block_scale = kwargs.get('block_scale', kwargs.get('BlockScale', 0.05))
        self.sep = kwargs.get('sep', kwargs.get('Sep', 0.05))
        
        # ColorList
        self.color_list = np.array([
            [65, 140, 240], [252, 180, 65], [224, 64, 10], [5, 100, 146],
            [191, 191, 191], [26, 59, 105], [255, 227, 130], [18, 156, 221],
            [202, 107, 75], [0, 92, 219], [243, 210, 136], [80, 99, 129],
            [241, 185, 168], [224, 131, 10], [120, 147, 190],
            [127, 91, 93], [187, 128, 110], [197, 173, 143], [59, 71, 111],
            [104, 95, 126], [76, 103, 86], [112, 112, 124], [72, 39, 24],
            [197, 119, 106], [160, 126, 88], [238, 208, 146]
        ]) / 255.0
        
        # Unique node list
        self.node_list = []
        for n in self.source + self.target:
            if n not in self.node_list:
                self.node_list.append(n)
                
        self.bn = len(self.node_list)
        if self.bn > len(self.color_list):
            extra_colors = np.random.rand(self.bn - len(self.color_list), 3) * 0.7
            self.color_list = np.vstack([self.color_list, extra_colors])
            
        self.adj_mat = np.zeros((self.bn, self.bn))
        for s, t, v in zip(self.source, self.target, self.value):
            si = self.node_list.index(s)
            ti = self.node_list.index(t)
            self.adj_mat[si, ti] += v
            
        self.bool_mat = np.abs(self.adj_mat) > 0
        self.vn = np.sum(self.bool_mat)
        
        if isinstance(self.label_location, str):
            self.label_location = [self.label_location] * self.bn
            
        self.label_hdl = [None] * self.bn

    def set_label_location(self, layer, location):
        if not hasattr(self, 'layer'):
            self.get_layer()
        for i in range(self.bn):
            if self.layer[i] == layer:
                self.label_location[i] = location
                
                # Update drawn text if handle exists
                h = self.label_hdl[i]
                if h is not None:
                    x_center = (self.layer_pos[i, 0] + self.layer_pos[i, 1]) / 2
                    y_center = (self.layer_pos[i, 2] + self.layer_pos[i, 3]) / 2
                    if location == 'right':
                        h.set_position((self.layer_pos[i, 1] + 0.02, y_center))
                        h.set_horizontalalignment('left')
                        h.set_verticalalignment('center')
                    elif location == 'left':
                        h.set_position((self.layer_pos[i, 0] - 0.02, y_center))
                        h.set_horizontalalignment('right')
                        h.set_verticalalignment('center')
                    elif location == 'top':
                        h.set_position((x_center, self.layer_pos[i, 2] - 0.02))
                        h.set_horizontalalignment('center')
                        h.set_verticalalignment('bottom')
                    elif location == 'bottom':
                        h.set_position((x_center, self.layer_pos[i, 3] + 0.02))
                        h.set_horizontalalignment('center')
                        h.set_verticalalignment('top')
                    else:
                        h.set_position((x_center, y_center))
                        h.set_horizontalalignment('center')
                        h.set_verticalalignment('center')

    def get_layer(self):
        self.layer = np.zeros(self.bn, dtype=int)
        self.layer[np.sum(self.bool_mat, axis=0) == 0] = 1
        start_mat = np.diag(self.layer)
        
        bool_mat_f = self.bool_mat.astype(float)
        for i in range(1, self.bn):
            reachable = np.linalg.matrix_power(bool_mat_f, i) > 0
            t_layer = (np.sum(start_mat @ reachable, axis=0) > 0) * (i + 1)
            self.layer = np.maximum(self.layer, t_layer)
            
    def get_layer_pos(self):
        self.ln = np.max(self.layer)
        self.total_len = np.maximum(np.sum(self.adj_mat, axis=0), np.sum(self.adj_mat, axis=1))
        self.total_len[self.total_len == 0] = np.mean(self.total_len) / 2
        
        self.sep_len = np.max(self.total_len) * self.sep
        
        self.layer_pos = np.zeros((self.bn, 4))
        for i in range(1, self.ln + 1):
            t_block_ind = np.where(self.layer == i)[0]
            if len(t_block_ind) == 0:
                continue
            t_block_len = np.concatenate(([0], np.cumsum(self.total_len[t_block_ind])))
            sep_val = self.sep_len
            t_y1 = t_block_len[:-1] + np.arange(len(t_block_ind)) * sep_val
            t_y2 = t_block_len[1:] + np.arange(len(t_block_ind)) * sep_val
            
            self.layer_pos[t_block_ind, 2] = t_y1
            self.layer_pos[t_block_ind, 3] = t_y2
            
        self.layer_pos[:, 0] = self.layer
        self.layer_pos[:, 1] = self.layer + self.block_scale
        
        t_min_y = np.min(self.layer_pos[:, 2])
        t_max_y = np.max(self.layer_pos[:, 3])
        for i in range(1, self.ln + 1):
            t_block_ind = np.where(self.layer == i)[0]
            if len(t_block_ind) == 0:
                continue
            t_block_pos3 = self.layer_pos[t_block_ind, 2]
            t_block_pos4 = self.layer_pos[t_block_ind, 3]
            
            if self.align == 'up':
                pass
            elif self.align == 'down':
                shift = t_max_y - np.max(t_block_pos4)
                self.layer_pos[t_block_ind, 2] += shift
                self.layer_pos[t_block_ind, 3] += shift
            elif self.align == 'center':
                block_center = (np.min(t_block_pos3) + np.max(t_block_pos4)) / 2
                global_center = (t_min_y + t_max_y) / 2
                shift = global_center - block_center
                self.layer_pos[t_block_ind, 2] += shift
                self.layer_pos[t_block_ind, 3] += shift

    def draw(self):
        if not hasattr(self, 'layer'):
            self.get_layer()
        self.get_layer_pos()
        
        # Draw links
        M, N = np.nonzero(self.adj_mat)
        for t_source, t_target in zip(M, N):
            self.draw_link(t_source, t_target)
            
        # Draw blocks
        for i in range(self.bn):
            self.draw_node(i)
            
        self.ax.invert_yaxis()
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        for spine in self.ax.spines.values():
            spine.set_visible(False)
            
    def draw_link(self, t_source, t_target):
        t_s1 = np.sum(self.adj_mat[t_source, :t_target]) + self.layer_pos[t_source, 2]
        t_s2 = np.sum(self.adj_mat[t_source, :t_target+1]) + self.layer_pos[t_source, 2]
        t_t1 = np.sum(self.adj_mat[:t_source, t_target]) + self.layer_pos[t_target, 2]
        t_t2 = np.sum(self.adj_mat[:t_source+1, t_target]) + self.layer_pos[t_target, 2]
        
        t_x = np.array([self.layer_pos[t_source, 0], self.layer_pos[t_source, 1], 
                        self.layer_pos[t_target, 0], self.layer_pos[t_target, 1]])
                        
        qX = np.linspace(self.layer_pos[t_source, 1], self.layer_pos[t_target, 0], 200)
        
        # Ensure strict monotonicity by adding tiny epsilon if overlapping (shouldn't happen)
        if t_x[1] >= t_x[2]:
            t_x[2] = t_x[1] + 1e-5
            t_x[3] = max(t_x[3], t_x[2] + 1e-5)
            
        Y1 = [t_s1, t_s1, t_t1, t_t1]
        Y2 = [t_s2, t_s2, t_t2, t_t2]
        
        qY1 = PchipInterpolator(t_x, Y1)(qX)
        qY2 = PchipInterpolator(t_x, Y2)(qX)
        
        c_source = self.color_list[t_source]
        c_target = self.color_list[t_target]
        
        for i in range(len(qX) - 1):
            if self.rendering_method == 'interp':
                ratio = i / (len(qX) - 2)
                c = c_source * (1 - ratio) + c_target * ratio
            elif self.rendering_method == 'left':
                c = c_source
            elif self.rendering_method == 'right':
                c = c_target
            else:
                c = np.array([0.6, 0.6, 0.6])
                
            self.ax.fill_between(qX[i:i+2], qY1[i:i+2], qY2[i:i+2], color=c, alpha=0.3, edgecolor='none', antialiased=True)

    def draw_node(self, n):
        x_coords = [self.layer_pos[n, 0], self.layer_pos[n, 1], self.layer_pos[n, 1], self.layer_pos[n, 0]]
        y_coords = [self.layer_pos[n, 2], self.layer_pos[n, 2], self.layer_pos[n, 3], self.layer_pos[n, 3]]
        self.ax.fill(x_coords, y_coords, color=self.color_list[n], edgecolor='none', antialiased=True)
        
        loc = self.label_location[n]
        text_kwargs = {'fontname': 'Times New Roman', 'fontsize': 15}
        x_center = (self.layer_pos[n, 0] + self.layer_pos[n, 1]) / 2
        y_center = (self.layer_pos[n, 2] + self.layer_pos[n, 3]) / 2
        
        if loc == 'right':
            h = self.ax.text(self.layer_pos[n, 1] + 0.02, y_center, f' {self.node_list[n]} ', ha='left', va='center', **text_kwargs)
        elif loc == 'left':
            h = self.ax.text(self.layer_pos[n, 0] - 0.02, y_center, f' {self.node_list[n]} ', ha='right', va='center', **text_kwargs)
        elif loc == 'top':
            h = self.ax.text(x_center, self.layer_pos[n, 2] - 0.02, f' {self.node_list[n]} ', ha='center', va='bottom', **text_kwargs)
        elif loc == 'bottom':
            h = self.ax.text(x_center, self.layer_pos[n, 3] + 0.02, f' {self.node_list[n]} ', ha='center', va='top', **text_kwargs)
        else:
            h = self.ax.text(x_center, y_center, f' {self.node_list[n]} ', ha='center', va='center', **text_kwargs)
            
        self.label_hdl[n] = h
