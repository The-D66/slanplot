# slanplot

![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-green.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

`slanplot` is a high-level, elegant Python visualization library that reproduces the incredibly aesthetic MATLAB scientific visualization suite authored by *slandarer*. By bridging the gap between MATLAB and Python, `slanplot` makes stunning and publication-ready statistical and relational diagrams accessible to the Python data science ecosystem.

## ✨ Features

- **Rich Aesthetics**: Ships with 53 highly-curated scientific colormaps directly adapted from MATLAB's premium `slanColor` palette. Automatically registers them into Matplotlib's global colormaps registry.
- **Relational Diagrams**:
  - `ChordDiagram` (和弦图)
  - `SSankey` (带智能排板的多级桑基图)
  - `STree`, `PiTree`, `CircularTree` (层级树、环形树)
- **Distribution Diagrams**:
  - `JoyPlot` (峰峦图 / Ridgeline Plot)
  - `MarginalPlot` (带地毯式误差带和误差棒的联合边缘分布)
  - `HatchedBar`, `HatchedPie` (支持密集交叉纹理的经典带阴影条形图与饼图)
  - `VennDiagram` (平滑贝塞尔三相维恩图)
  - `CalendarHeatmap` (GitHub 风格日历热力图)
  - `SHeatmap` (支持六边形、扇形、自定义填充的特种相关性热力矩阵)
- **Scientific Ready**: Includes built-in support for rendering `***` significance stars, overlaying nested distribution patches, and `fill_between` dynamic standard deviation bounds.

## 📦 Installation

Install `slanplot` easily via pip:

```bash
pip install slanplot
```

## 🚀 Quick Start

```python
import numpy as np
import matplotlib.pyplot as plt
from slanplot import SHeatmap

# 1. Generate correlation data
data = np.random.randn(10, 10)
pvals = np.random.rand(10, 10)

# 2. Draw a gorgeous special heatmap
fig, ax = plt.subplots(figsize=(8, 8))
hm = SHeatmap(data, format_type='pie', ax=ax, pval=pvals, cmap='slan_batlow')
hm.draw()

plt.show()
```

## 📖 Documentation & Examples

Please check the interactive Jupyter Notebooks in the `examples/notebooks/` directory for an exhaustive visual walkthrough of every chart type:
1. `01_Relational_Plots.ipynb`: Focuses on network and relation distributions (Sankey, Chord).
2. `02_Distribution_Plots.ipynb`: Focuses on complex statistical comparisons (Joyplot, Marginal, Venn).
3. `03_Scientific_Visualization.ipynb`: Step-by-step reproduction of top-tier biological scientific plots.

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## 📜 License
This project is licensed under the MIT License.
