import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class ChordDiagram:
    def __init__(self, data_mat, row_name=None, col_name=None, ax=None, **kwargs):
        self.ax = ax if ax is not None else plt.gca()
        
        # Convert to numpy array if it's dataframe
        if isinstance(data_mat, pd.DataFrame):
            self.data_mat = data_mat.values
            if row_name is None:
                row_name = data_mat.index.astype(str).tolist()
            if col_name is None:
                col_name = data_mat.columns.astype(str).tolist()
        else:
            self.data_mat = np.array(data_mat)
            
        self.num_f, self.num_t = self.data_mat.shape
        
        self.row_name = row_name if row_name is not None else [f"R{i+1}" for i in range(self.num_f)]
        self.col_name = col_name if col_name is not None else [f"C{j+1}" for j in range(self.num_t)]
        
        self.sep = kwargs.get('sep', kwargs.get('Sep', 1/40.0))
        self.l_radius = kwargs.get('l_radius', kwargs.get('LRadius', 1.28))
        self.l_rotate = kwargs.get('l_rotate', kwargs.get('LRotate', 'off'))
        self.s_sq_ratio = kwargs.get('s_sq_ratio', kwargs.get('SSqRatio', 1.0))
        self.o_sq_ratio = kwargs.get('o_sq_ratio', kwargs.get('OSqRatio', 1.0))
        self.rotation = kwargs.get('rotation', kwargs.get('Rotation', 0.0))
        
        self.name_f_hdl = [None] * self.num_f
        self.name_t_hdl = [None] * self.num_t
        self.square_f_hdl = [None] * self.num_f
        self.square_t_hdl = [None] * self.num_t
        self.chord_mat_hdl = {}
        
        self.theta_tick_f_hdl = []
        self.theta_tick_t_hdl = []
        self.r_tick_f_hdl = []
        self.r_tick_t_hdl = []
        self.theta_tick_label_f_hdl = []
        self.theta_tick_label_t_hdl = []
        self.tick_mode = kwargs.get('tick_mode', kwargs.get('TickMode', 'value'))

    def _bezier_curve(self, pnt1, pnt3, N=200):
        # pnt2 is [0, 0] in slandarer's implementation
        t = np.linspace(0, 1, N).reshape(-1, 1)
        # B(t) = (1-t)^2 P1 + 2(1-t)t P2 + t^2 P3
        # Since P2 is [0, 0], B(t) = (1-t)^2 P1 + t^2 P3
        line = ((1 - t) ** 2) * pnt1 + (t ** 2) * pnt3
        return line

    def draw(self):
        self.ax.set_xlim([-1.38, 1.38])
        self.ax.set_ylim([-1.38, 1.38])
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        for spine in self.ax.spines.values():
            spine.set_visible(False)
        self.ax.set_aspect('equal')
        
        total_sum = np.sum(self.data_mat)
        
        # Calculate ratios
        ratio_f = np.sum(self.data_mat, axis=1) / total_sum
        ratio_f_cum = np.concatenate(([0], np.cumsum(ratio_f)))
        
        ratio_t = np.sum(self.data_mat, axis=0) / total_sum
        ratio_t_cum = np.concatenate(([0], np.cumsum(ratio_t)))
        
        sep1 = 1/20.0
        sep2 = self.sep
        
        sep_len = np.pi * (1 - 2*sep1) * sep2
        base_len_f = (np.pi * (1 - sep1) - (self.num_f - 1) * sep_len)
        base_len_t = (np.pi * (1 - sep1) - (self.num_t - 1) * sep_len)
        
        t_color = np.array([[61, 96, 137], [76, 103, 86]]) / 255.0
        
        mean_theta_f = np.zeros(self.num_f)
        rotation_f = np.zeros(self.num_f)
        theta_set_f = [[] for _ in range(self.num_f)]
        
        # Draw bottom blocks (F)
        for i in range(self.num_f):
            theta1 = 2*np.pi - np.pi*sep1/2 - ratio_f_cum[i]*base_len_f - i*sep_len + self.rotation
            theta2 = 2*np.pi - np.pi*sep1/2 - ratio_f_cum[i+1]*base_len_f - i*sep_len + self.rotation
            theta = np.linspace(theta1, theta2, 100)
            X = np.cos(theta)
            Y = np.sin(theta)
            
            r_inner = 1.15 - 0.1 * self.o_sq_ratio
            r_outer = 1.15
            
            px = np.concatenate([r_inner * X, r_outer * X[::-1]])
            py = np.concatenate([r_inner * Y, r_outer * Y[::-1]])
            
            self.square_f_hdl[i] = self.ax.fill(px, py, color=t_color[0], edgecolor='none', zorder=2)
            
            # R-Ticks
            l_rtick, = self.ax.plot(np.cos(theta)*1.17, np.sin(theta)*1.17, color='black', linewidth=0.8, visible=False)
            self.r_tick_f_hdl.append(l_rtick)
            
            theta3 = (theta1 + theta2) / 2.0 % (2*np.pi)
            mean_theta_f[i] = theta3
            rot = theta3 / np.pi * 180.0 % 360
            
            # Label
            if 0 < rot < 180:
                rot_ang = -(0.5*np.pi - theta3) / np.pi * 180.0
                self.name_f_hdl[i] = self.ax.text(np.cos(theta3)*self.l_radius, np.sin(theta3)*self.l_radius, 
                                                  self.row_name[i], fontsize=12, 
                                                  ha='center', va='center', rotation=rot_ang)
                rotation_f[i] = rot_ang
            else:
                rot_ang = -(1.5*np.pi - theta3) / np.pi * 180.0
                self.name_f_hdl[i] = self.ax.text(np.cos(theta3)*self.l_radius, np.sin(theta3)*self.l_radius, 
                                                  self.row_name[i], fontsize=12, 
                                                  ha='center', va='center', rotation=rot_ang)
                rotation_f[i] = rot_ang

        mean_theta_t = np.zeros(self.num_t)
        rotation_t = np.zeros(self.num_t)
        theta_set_t = [[] for _ in range(self.num_t)]
        
        # Draw top blocks (T)
        for j in range(self.num_t):
            theta1 = np.pi - np.pi*sep1/2 - ratio_t_cum[j]*base_len_t - j*sep_len + self.rotation
            theta2 = np.pi - np.pi*sep1/2 - ratio_t_cum[j+1]*base_len_t - j*sep_len + self.rotation
            theta = np.linspace(theta1, theta2, 100)
            X = np.cos(theta)
            Y = np.sin(theta)
            
            r_inner = 1.15 - 0.1 * self.o_sq_ratio
            r_outer = 1.15
            
            px = np.concatenate([r_inner * X, r_outer * X[::-1]])
            py = np.concatenate([r_inner * Y, r_outer * Y[::-1]])
            
            self.square_t_hdl[j] = self.ax.fill(px, py, color=t_color[1], edgecolor='none', zorder=2)
            
            # R-Ticks
            l_rtick, = self.ax.plot(np.cos(theta)*1.17, np.sin(theta)*1.17, color='black', linewidth=0.8, visible=False)
            self.r_tick_t_hdl.append(l_rtick)
            
            theta3 = (theta1 + theta2) / 2.0 % (2*np.pi)
            mean_theta_t[j] = theta3
            rot = theta3 / np.pi * 180.0
            
            # Label
            if 0 < rot < 180:
                rot_ang = -(0.5*np.pi - theta3) / np.pi * 180.0
                self.name_t_hdl[j] = self.ax.text(np.cos(theta3)*self.l_radius, np.sin(theta3)*self.l_radius, 
                                                  self.col_name[j], fontsize=12, 
                                                  ha='center', va='center', rotation=rot_ang)
                rotation_t[j] = rot_ang
            else:
                rot_ang = -(1.5*np.pi - theta3) / np.pi * 180.0
                self.name_t_hdl[j] = self.ax.text(np.cos(theta3)*self.l_radius, np.sin(theta3)*self.l_radius, 
                                                  self.col_name[j], fontsize=12, 
                                                  ha='center', va='center', rotation=rot_ang)
                rotation_t[j] = rot_ang

        # Data map coloring (Using Summer colormap for now to match MATLAB)
        d_mat_uni = self.data_mat - np.min(self.data_mat)
        if np.max(d_mat_uni) > 0:
            d_mat_uni = d_mat_uni / np.max(d_mat_uni)
            
        cmap = plt.get_cmap('summer_r')
        
        # Draw chords
        for i in range(self.num_f):
            for j in range(self.num_t - 1, -1, -1):
                if self.data_mat[i, j] == 0:
                    continue
                    
                theta1 = 2*np.pi - np.pi*sep1/2 - ratio_f_cum[i]*base_len_f - i*sep_len + self.rotation
                theta2 = 2*np.pi - np.pi*sep1/2 - ratio_f_cum[i+1]*base_len_f - i*sep_len + self.rotation
                theta3 = np.pi - np.pi*sep1/2 - ratio_t_cum[j]*base_len_t - j*sep_len + self.rotation
                theta4 = np.pi - np.pi*sep1/2 - ratio_t_cum[j+1]*base_len_t - j*sep_len + self.rotation
                
                t_row_v = self.data_mat[i, ::-1]
                t_row_v = np.concatenate(([0], t_row_v / np.sum(t_row_v)))
                
                t_col_v = self.data_mat[:, j]
                t_col_v = np.concatenate(([0], t_col_v / np.sum(t_col_v)))
                
                theta5 = (theta2 - theta1) * np.sum(t_row_v[:(self.num_t + 1 - j)]) + theta1
                theta6 = (theta2 - theta1) * np.sum(t_row_v[:(self.num_t + 2 - j)]) + theta1
                theta7 = (theta3 - theta4) * np.sum(t_col_v[:i+1]) + theta4
                theta8 = (theta3 - theta4) * np.sum(t_col_v[:i+2]) + theta4
                
                t_pnt1 = np.array([np.cos(theta5), np.sin(theta5)])
                t_pnt2 = np.array([np.cos(theta6), np.sin(theta6)])
                t_pnt3 = np.array([np.cos(theta7), np.sin(theta7)])
                t_pnt4 = np.array([np.cos(theta8), np.sin(theta8)])
                
                # Add ticks base collection
                if self.tick_mode != 'linear':
                    if len(theta_set_f[i]) == 0:
                        theta_set_f[i].append(theta5)
                    theta_set_f[i].append(theta6)
                    
                    if len(theta_set_t[j]) == 0:
                        theta_set_t[j].append(theta7)
                    theta_set_t[j].append(theta8)
                
                t_line1 = self._bezier_curve(t_pnt1, t_pnt3, 200)
                t_line2 = self._bezier_curve(t_pnt2, t_pnt4, 200)
                
                t_line3 = np.column_stack([np.cos(np.linspace(theta6, theta5, 100)), 
                                           np.sin(np.linspace(theta6, theta5, 100))])
                t_line4 = np.column_stack([np.cos(np.linspace(theta7, theta8, 100)), 
                                           np.sin(np.linspace(theta7, theta8, 100))])
                
                px = np.concatenate([t_line1[:, 0], t_line4[:, 0], t_line2[::-1, 0], t_line3[:, 0]])
                py = np.concatenate([t_line1[:, 1], t_line4[:, 1], t_line2[::-1, 1], t_line3[:, 1]])
                
                c = cmap(d_mat_uni[i, j])
                
                poly = self.ax.fill(px, py, color=c, alpha=0.3, edgecolor='none', zorder=1)
                self.chord_mat_hdl[(i, j)] = poly
                
        # Draw Theta Ticks for F and T if 'value' mode
        if self.tick_mode == 'value':
            for i in range(self.num_f):
                if i < len(theta_set_f):
                    tsf = np.unique(theta_set_f[i])
                    for t in tsf:
                        l, = self.ax.plot([np.cos(t)*1.17, np.cos(t)*1.19], [np.sin(t)*1.17, np.sin(t)*1.19], color='k', lw=0.8, visible=False)
                        self.theta_tick_f_hdl.append(l)
            for j in range(self.num_t):
                if j < len(theta_set_t):
                    tst = np.unique(theta_set_t[j])
                    for t in tst:
                        l, = self.ax.plot([np.cos(t)*1.17, np.cos(t)*1.19], [np.sin(t)*1.17, np.sin(t)*1.19], color='k', lw=0.8, visible=False)
                        self.theta_tick_t_hdl.append(l)

    def tick_state(self, state):
        visible = True if state.lower() == 'on' else False
        for hdl in self.r_tick_f_hdl + self.r_tick_t_hdl + self.theta_tick_f_hdl + self.theta_tick_t_hdl:
            hdl.set_visible(visible)

    def set_font(self, **kwargs):
        for hdl in self.name_f_hdl + self.name_t_hdl:
            if hdl is not None:
                plt.setp(hdl, **kwargs)
