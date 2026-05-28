import numpy as np
import matplotlib.pyplot as plt

class PiTree:
    def __init__(self, digits, pos, d_flag, ax=None):
        self.ax = ax if ax is not None else plt.gca()
        self.digits = np.array(digits)
        self.pos = np.array(pos)
        self.d_flag = d_flag
        
        self.lw = 2.0
        self.theta = np.pi / 2 + (np.random.rand() - 0.5) * np.pi / 12
        
        self.cm = np.array([
            [237, 32, 121], [237, 62, 54], [247, 99, 33], [255, 183, 59], [245, 236, 43],
            [141, 196, 63], [57, 178, 74], [0, 171, 238], [40, 56, 145], [146, 39, 139]
        ]) / 255.0
        
    def _kplot(self, x_coords, y_coords, lw):
        lw_vals = np.linspace(lw, lw * 0.6, 10)
        x_vals = np.linspace(x_coords[0], x_coords[1], 11)
        y_vals = np.linspace(y_coords[0], y_coords[1], 11)
        
        for i in range(10):
            self.ax.plot([x_vals[i], x_vals[i+1]], [y_vals[i], y_vals[i+1]], 
                         linewidth=lw_vals[i], color=[0.1, 0.1, 0.1])
                         
    def draw(self):
        if np.all(self.digits[:-2] == 0):
            end_set = [[self.pos[0], self.pos[1], self.pos[0], self.pos[1], self.theta]]
        else:
            self._kplot([self.pos[0], self.pos[0] + np.cos(self.theta)],
                        [self.pos[1], self.pos[1] + np.sin(self.theta)], self.lw / 0.6)
            end_set = [[self.pos[0], self.pos[1], self.pos[0] + np.cos(self.theta), self.pos[1] + np.sin(self.theta), self.theta]]
            
            layer = [0]
            for i in range(len(self.digits)):
                layer.extend([i] * int(self.digits[i]))
            layer = np.array(layer)
            
            if self.d_flag:
                for i in range(len(self.digits) - 2):
                    cur_end = end_set.pop(0)
                    x_i = self.digits[i]
                    
                    if x_i == 0:
                        new_set = [cur_end]
                    elif x_i == 1:
                        t_theta = cur_end[4]
                        t_theta_vals = np.linspace(t_theta + np.pi/8, t_theta - np.pi/8, 2) + (np.random.rand(2) - 0.5) * np.pi / 8
                        
                        scale1 = 0.7 ** layer[i+1] if i+1 < len(layer) else 0.7**i # Approximate indexing
                        
                        n1 = [cur_end[2], cur_end[3], cur_end[2] + np.cos(t_theta_vals[0]) * scale1, cur_end[3] + np.sin(t_theta_vals[0]) * scale1, t_theta_vals[0]]
                        n2 = [cur_end[2], cur_end[3], cur_end[2] + np.cos(t_theta_vals[1]) * scale1 * 0.1, cur_end[3] + np.sin(t_theta_vals[1]) * scale1 * 0.1, t_theta_vals[1]]
                        new_set = [n1, n2]
                    else:
                        t_theta = cur_end[4]
                        t_theta_vals = np.linspace(t_theta + np.pi/5, t_theta - np.pi/5, int(x_i)) + (np.random.rand(int(x_i)) - 0.5) * np.pi / 8
                        
                        scale = 0.7 ** layer[i+1] if i+1 < len(layer) else 0.7**i
                        
                        new_set = []
                        for j in range(int(x_i)):
                            new_set.append([cur_end[2], cur_end[3], cur_end[2] + np.cos(t_theta_vals[j]) * scale, cur_end[3] + np.sin(t_theta_vals[j]) * scale, t_theta_vals[j]])
                            
                    for ns in new_set:
                        scale = 0.6 ** layer[i+1] if i+1 < len(layer) else 0.6**i
                        self._kplot([ns[0], ns[2]], [ns[1], ns[3]], self.lw * scale)
                        
                    end_set.extend(new_set)
                    
        # Leaves and flowers
        fl_set = np.array([[e[2], e[3]] for e in end_set])
        if len(fl_set) == 0:
            fl_set = np.array([self.pos])
            
        sort_idx = np.argsort(fl_set[:, 0])
        fl_set = fl_set[sort_idx]
        
        temp_ind = np.argsort(np.random.rand(len(fl_set)))
        temp_ind = np.sort(temp_ind[:max(1, len(self.digits) - 2)])
        flower_ind = temp_ind[np.random.randint(0, len(temp_ind))]
        leaf_ind = [ti for ti in temp_ind if ti != flower_ind]
        
        for i, li in enumerate(leaf_ind):
            c_idx = self.digits[i % len(self.digits)]
            self.ax.scatter(fl_set[li, 0], fl_set[li, 1], s=70, c=[self.cm[c_idx]], edgecolors='none', zorder=10)
            
        # Flowers
        flower_color = self.cm[self.digits[-3]] if self.d_flag else self.cm[self.digits[-1]]
        center_color = self.cm[self.digits[-1]]
        for i in range(1, 6):
            self.ax.scatter(fl_set[flower_ind, 0] + np.cos(np.pi*2*i/5)*0.18,
                            fl_set[flower_ind, 1] + np.sin(np.pi*2*i/5)*0.18,
                            s=60, c=[flower_color], edgecolors='white', zorder=10)
                            
        self.ax.scatter(fl_set[flower_ind, 0], fl_set[flower_ind, 1], s=60, c=[center_color], edgecolors='white', zorder=11)
