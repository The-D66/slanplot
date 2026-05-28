from .core.colors import SlandarerColormaps
from .distribution.marginal import MarginalPlot
from .distribution.joyplot import JoyPlot
from .relational.sankey import SSankey
from .relational.chord import ChordDiagram
from .relational.circ_tree import CircularTree
from .relational.stree import STree
from .relational.pitree import PiTree
from .distribution.hatched import HatchedBar, HatchedPie
from .distribution.calendar import CalendarHeatmap
import matplotlib.pyplot as plt

# 统一设置全局科研字体为 Times New Roman
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['mathtext.fontset'] = 'stix'  # 公式也使用类似 serif 的字体

from .distribution.venn import VennDiagram
from .distribution.sheatmap import SHeatmap
from .colors import scientific

__all__ = ['SlandarerColormaps', 'MarginalPlot', 'JoyPlot', 'SSankey', 'ChordDiagram', 'CircularTree', 'STree', 'PiTree', 'HatchedBar', 'HatchedPie', 'CalendarHeatmap', 'VennDiagram', 'SHeatmap', 'scientific']
