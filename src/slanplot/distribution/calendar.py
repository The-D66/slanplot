import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import numpy as np
import pandas as pd
import datetime

class CalendarHeatmap:
    def __init__(self, year, dates, values, ax=None, month_lim=(1, 12), cmap=None, **kwargs):
        self.ax = ax if ax is not None else plt.gca()
        self.year = year
        self.dates = pd.to_datetime(dates)
        self.values = np.array(values)
        self.month_lim = month_lim
        self.kwargs = kwargs
        
        # Default colormap (green shades like GitHub)
        if cmap is None:
            colors = [
                [1.0000, 1.0000, 0.8980], [0.9833, 0.9937, 0.8060], [0.9608, 0.9851, 0.7197], 
                [0.8980, 0.9600, 0.6737], [0.8280, 0.9312, 0.6282], [0.7359, 0.8915, 0.5843],
                [0.6369, 0.8486, 0.5404], [0.5260, 0.8005, 0.4965], [0.4131, 0.7482, 0.4452], 
                [0.2980, 0.6918, 0.3867], [0.2157, 0.6196, 0.3307], [0.1529, 0.5380, 0.2763],
                [0.0824, 0.4737, 0.2439], [0.0092, 0.4152, 0.2188], [0.0000, 0.3438, 0.1901],
                [0.0000, 0.2706, 0.1608]
            ]
            self.cmap = mcolors.LinearSegmentedColormap.from_list('cal', colors)
        else:
            self.cmap = cmap
            
    def draw(self):
        # Filter dates for the year and month limits
        start_date = pd.Timestamp(year=self.year, month=self.month_lim[0], day=1)
        if self.month_lim[1] == 12:
            end_date = pd.Timestamp(year=self.year + 1, month=1, day=1)
        else:
            end_date = pd.Timestamp(year=self.year, month=self.month_lim[1] + 1, day=1)
            
        mask = (self.dates >= start_date) & (self.dates < end_date)
        dates_filtered = self.dates[mask]
        values_filtered = self.values[mask]
        
        # Create full date range
        full_dates = pd.date_range(start=start_date, end=end_date - pd.Timedelta(days=1), freq='D')
        
        # Create a mapping from date to (x, y) grid coordinates
        # y: day of week (0=Mon, ..., 6=Sun) -> mapped to 1-7 for MATLAB compatibility
        day_numbers = full_dates.dayofweek + 1
        
        # x: week column
        x_list = []
        col = 1
        for i in range(len(full_dates)):
            if full_dates[i].dayofweek == 0 and i > 0:
                col += 1
            x_list.append(col)
            
        x_list = np.array(x_list)
        y_list = day_numbers
        
        self.ax.set_aspect('equal')
        self.ax.invert_yaxis()
        self.ax.set_yticks(np.arange(1, 8))
        self.ax.set_yticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
        self.ax.yaxis.tick_right()
        
        # Draw background gray squares
        for x, y in zip(x_list, y_list):
            rect = plt.Rectangle((x - 0.5, y - 0.5), 1, 1, facecolor=[0.8, 0.8, 0.8], edgecolor='white', linewidth=1)
            self.ax.add_patch(rect)
            
        # Draw value squares
        norm = mcolors.Normalize(vmin=values_filtered.min(), vmax=values_filtered.max())
        for d, v in zip(dates_filtered, values_filtered):
            idx = np.where(full_dates == d)[0]
            if len(idx) > 0:
                i = idx[0]
                rect = plt.Rectangle((x_list[i] - 0.5, y_list[i] - 0.5), 1, 1, facecolor=self.cmap(norm(v)), edgecolor='white', linewidth=1)
                self.ax.add_patch(rect)
                
        # Draw borders
        months = full_dates.month
        mon_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        x_ticks = []
        x_labels = []
        
        for m in range(self.month_lim[0], self.month_lim[1] + 1):
            mask_m = (months == m)
            if not np.any(mask_m):
                continue
            x_m = x_list[mask_m]
            y_m = y_list[mask_m]
            
            x_u = x_m[y_m == 1]
            if len(x_u) > 0:
                self.ax.plot([np.min(x_u) - 0.5, np.max(x_u) + 0.5], [0.5, 0.5], color='black', linewidth=1)
                
            x_d = x_m[y_m == 7]
            if len(x_d) > 0:
                x_ticks.append(np.mean(x_d))
                x_labels.append(mon_names[m - 1])
                self.ax.plot([np.min(x_d) - 0.5, np.max(x_d) + 0.5], [7.5, 7.5], color='black', linewidth=1)
                
            if len(x_u) > 0:
                max_xu = np.max(x_u)
                y_l = y_m[x_m == max_xu]
                self.ax.plot([max_xu + 0.5, max_xu + 0.5], [np.min(y_l) - 0.5, np.max(y_l) + 0.5], color='black', linewidth=1)
                self.ax.plot([max_xu - 0.5, max_xu - 0.5], [min(np.max(y_l) + 1, 8) - 0.5, 7.5], color='black', linewidth=1)
                self.ax.plot([max_xu + 0.5, max_xu - 0.5], [np.max(y_l) + 0.5, np.max(y_l) + 0.5], color='black', linewidth=1)
                
            if m == self.month_lim[0]:
                min_xd = np.min(x_d) if len(x_d) > 0 else np.min(x_m)
                y_r = y_m[x_m == min_xd]
                if len(y_r) > 0:
                    self.ax.plot([min_xd - 0.5, min_xd - 0.5], [np.min(y_r) - 0.5, np.max(y_r) + 0.5], color='black', linewidth=1)
                    self.ax.plot([min_xd + 0.5, min_xd + 0.5], [max(np.min(y_r) - 1, 0) + 0.5, 0.5], color='black', linewidth=1)
                    self.ax.plot([min_xd - 0.5, min_xd + 0.5], [np.min(y_r) - 0.5, np.min(y_r) - 0.5], color='black', linewidth=1)
                    
        self.ax.set_xlim(0.5, np.max(x_list) + 0.5)
        self.ax.set_ylim(7.5, 0.5)
        
        self.ax.set_xticks(x_ticks)
        self.ax.set_xticklabels(x_labels)
        self.ax.tick_params(axis='x', length=0)
        self.ax.tick_params(axis='y', length=0)
        
        # Colorbar
        sm = cm.ScalarMappable(cmap=self.cmap, norm=norm)
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=self.ax, orientation='vertical', fraction=0.046, pad=0.04)
        cbar.outline.set_linewidth(1)
        
        # Year title
        self.ax.text(-0.5, 4, str(self.year), rotation=90, ha='center', va='center', 
                     fontsize=27, fontweight='bold', color=[0.6, 0.6, 0.6])
        
        # Hide spines
        for spine in self.ax.spines.values():
            spine.set_visible(False)
