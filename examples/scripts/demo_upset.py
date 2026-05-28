import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from upsetplot import UpSet
import matplotlib.colors as mcolors

np.random.seed(1)
set_names = ['RB1', 'PIK3R1', 'EGFR', 'TP53', 'PTEN']
set_mat = np.random.rand(200, 5) > 0.85

multi_idx = pd.MultiIndex.from_arrays(set_mat.T, names=set_names)
df = pd.DataFrame({'value': np.ones(200)}, index=multi_idx)

data_agg = df.groupby(level=set_names).count()['value']

fig = plt.figure(figsize=(10, 6))

bar_color_i = mcolors.to_hex((66/255, 182/255, 195/255))
line_color = mcolors.to_hex((61/255, 58/255, 61/255))
patch_color = mcolors.to_hex((248/255, 246/255, 249/255)) 
bkg_dot_color = mcolors.to_hex((233/255, 233/255, 233/255))

upset_data = UpSet(data_agg, 
                   facecolor=bar_color_i,
                   other_dots_color=bkg_dot_color,
                   shading_color=patch_color,
                   sort_by='cardinality')
res = upset_data.plot(fig=fig)

# 添加顶部标签
ax_intersections = res['intersections']
for c in ax_intersections.containers:
    ax_intersections.bar_label(c, label_type='edge', padding=2)

plt.savefig("output_upset.png", dpi=300, bbox_inches='tight')
print("Updated demo1_upset.png")
