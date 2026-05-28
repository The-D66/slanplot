import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Ellipse
import matplotlib.transforms as transforms
from ..core.colors import SlandarerColormaps

class MarginalPlot:
    def __init__(self, data_list, main_type='scatter', top_type='hist', right_type='hist', 
                 colors=None, labels=None, figsize=(8, 8)):
        self.data_list = data_list
        self.num_groups = len(data_list)
        self.main_type = main_type
        self.top_type = top_type
        self.right_type = right_type
        
        if colors is None:
            # Default to tab10 if no colors provided
            self.colors = plt.get_cmap('tab10').colors[:self.num_groups]
        else:
            self.colors = colors
            
        if labels is None:
            self.labels = [f'Group {i+1}' for i in range(self.num_groups)]
        else:
            self.labels = labels

        self.fig = plt.figure(figsize=figsize)
        gs = self.fig.add_gridspec(3, 3, width_ratios=[4, 1, 0.1], height_ratios=[0.1, 1, 4], 
                                   wspace=0.05, hspace=0.05)
        
        self.ax_main = self.fig.add_subplot(gs[2, 0])
        self.ax_top = self.fig.add_subplot(gs[1, 0], sharex=self.ax_main)
        self.ax_right = self.fig.add_subplot(gs[2, 1], sharey=self.ax_main)
        
        # 不隐藏边框，让它们可以显示坐标轴
        # 默认只显示左边和下边，或者根据需要开启
        self.ax_main.spines['top'].set_visible(False)
        self.ax_main.spines['right'].set_visible(False)
        self.ax_top.spines['top'].set_visible(False)
        self.ax_top.spines['right'].set_visible(False)
        self.ax_right.spines['top'].set_visible(False)
        self.ax_right.spines['right'].set_visible(False)
        
        # 让 top 图显示 Y 轴，right 图显示 X 轴
        self.ax_top.set_xticks([])
        self.ax_right.set_yticks([])
        self.ax_top.tick_params(axis='y', left=True, labelleft=True)
        self.ax_right.tick_params(axis='x', bottom=True, labelbottom=True)

    def _confidence_ellipse(self, x, y, ax, n_std=3.0, facecolor='none', **kwargs):
        if x.size != y.size:
            raise ValueError("x and y must be the same size")
        cov = np.cov(x, y)
        pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
        ell_radius_x = np.sqrt(1 + pearson)
        ell_radius_y = np.sqrt(1 - pearson)
        ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                          facecolor=facecolor, **kwargs)
        scale_x = np.sqrt(cov[0, 0]) * n_std
        mean_x = np.mean(x)
        scale_y = np.sqrt(cov[1, 1]) * n_std
        mean_y = np.mean(y)
        transf = transforms.Affine2D().rotate_deg(45).scale(scale_x, scale_y).translate(mean_x, mean_y)
        ellipse.set_transform(transf + ax.transData)
        return ax.add_patch(ellipse)

    def draw(self):
        for i, data in enumerate(self.data_list):
            x, y = data[:, 0], data[:, 1]
            color = self.colors[i]
            label = self.labels[i]

            # --- Main Plot ---
            if self.main_type in ['scatter', 'ellipse', 'errorbar']:
                # 只有 scatter 和 ellipse 原本绘制大散点，errorbar 将单独绘制误差棒散点
                if self.main_type != 'errorbar':
                    self.ax_main.scatter(x, y, color=color, label=label, alpha=0.7, edgecolors='w', s=50)
            
            if self.main_type == 'ellipse':
                self._confidence_ellipse(x, y, self.ax_main, n_std=2.5, edgecolor=color, linewidth=2, alpha=0.5)
                # optionally fill with low alpha
                self._confidence_ellipse(x, y, self.ax_main, n_std=2.5, facecolor=color, alpha=0.1)
                
            if self.main_type == 'errorbar':
                # 散点误差棒 (原图中有空心大圆圈带十字误差棒)
                mean_x, mean_y = np.mean(x), np.mean(y)
                std_x, std_y = np.std(x), np.std(y)
                self.ax_main.errorbar(mean_x, mean_y, xerr=std_x, yerr=std_y, fmt='o',
                                      color=color, ecolor=color, capsize=4, elinewidth=1.5, 
                                      markeredgewidth=1.5, markerfacecolor='none', markersize=10, label=label)
                
            # --- Top Plot ---
            if self.top_type == 'hist':
                sns.histplot(x=x, ax=self.ax_top, color=color, element='step', fill=True, alpha=0.3)
            elif self.top_type == 'kd-hist':
                sns.histplot(x=x, ax=self.ax_top, color=color, kde=True, stat="density", fill=True, alpha=0.3, line_kws={'linewidth': 2})
            elif self.top_type == 'kd-area':
                sns.kdeplot(x=x, ax=self.ax_top, color=color, fill=True, alpha=0.5)
            elif self.top_type == 'rug':
                # 绘制类似条形码的地毯图，使用垂直线条，自适应高度
                h = 1.0 / self.num_groups
                y_min = i * h + h * 0.1
                y_max = (i + 1) * h - h * 0.1
                self.ax_top.vlines(x, ymin=y_min, ymax=y_max, color=color, alpha=0.4, linewidth=1)

            # --- Right Plot ---
            # Right Plot (如果是 hist，跳过这里在循环外绘制)
            if self.right_type == 'kd-hist':
                sns.histplot(y=y, ax=self.ax_right, color=color, kde=True, stat="density", fill=True, alpha=0.3, line_kws={'linewidth': 2})
            elif self.right_type == 'half-violin':
                sns.kdeplot(y=y, ax=self.ax_right, color=color, fill=True, alpha=0.5)
            elif self.right_type == 'rug':
                h = 1.0 / self.num_groups
                x_min = i * h + h * 0.1
                x_max = (i + 1) * h - h * 0.1
                self.ax_right.hlines(y, xmin=x_min, xmax=x_max, color=color, alpha=0.4, linewidth=1)
                
        # 右侧统一绘制直方图，避免遮挡
        if self.right_type == 'hist':
            y_list = [d[:, 1] for d in self.data_list]
            all_y = np.concatenate(y_list)
            bins = np.histogram_bin_edges(all_y, bins=15)
            for i, y in enumerate(y_list):
                self.ax_right.hist(y, bins=bins, orientation='horizontal', color=self.colors[i], alpha=0.5, edgecolor='none')

        self.ax_main.legend(frameon=False)
        self.ax_main.grid(True, linestyle='--', alpha=0.6)
        
        # Adjust tick labels
        plt.setp(self.ax_top.get_xticklabels(), visible=False)
        plt.setp(self.ax_right.get_yticklabels(), visible=False)
