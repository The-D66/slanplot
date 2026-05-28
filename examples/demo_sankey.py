import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from slanplot import SSankey

links = [
    ['a1','A',1.2], ['a2','A',1], ['a1','B',.6], ['a3','A',1], ['a3','C',0.5],
    ['b1','B',.4], ['b2','B',1], ['b3','B',1], ['c1','C',1],
    ['c2','C',1],  ['c3','C',1], ['A','AA',2], ['A','BB',1.2],
    ['B','BB',1.5], ['B','AA',1.5], ['C','BB',2.3], ['C','AA',1.2]
]

source = [l[0] for l in links]
target = [l[1] for l in links]
value = [l[2] for l in links]

fig, ax = plt.subplots(figsize=(10, 8))
SK = SSankey(source, target, value, ax=ax, rendering_method='interp', align='center', label_location='top', sep=0.2)
SK.draw()

SK.set_label_location(1, 'left')

plt.title("SSankey plot via slanplot")
plt.savefig('output_sankey.png', dpi=300, bbox_inches='tight')
print("Saved output_sankey.png using slanplot module!")
