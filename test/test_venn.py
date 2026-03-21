import numpy as np
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from overlapviz.core.calculator import OverlapCalculator
from overlapviz.venn import VennPlot
from overlapviz.core import PlotStyle


np.random.seed(42) 

base_elements = [f"gene_{i:03d}" for i in range(1, 201)]

set_a = set(np.random.choice(base_elements, 100, replace=False).tolist())
set_b = set(np.random.choice(base_elements, 100, replace=False).tolist())
set_c = set(np.random.choice(base_elements, 100, replace=False).tolist())
set_d = set(np.random.choice(base_elements, 100, replace=False).tolist())
# set_e = set(np.random.choice(base_elements, 100, replace=False).tolist())
# set_f = set(np.random.choice(base_elements, 100, replace=False).tolist())
# set_g = set(np.random.choice(base_elements, 100, replace=False).tolist())

data = {
    'A': set_a,
    'B': set_b,
    'C': set_c,
    'D': set_d,
    # 'E': set_e,
    # 'F': set_f,
    # 'G': set_g,
}

calc = OverlapCalculator(data)
plot_data = calc.get_plot_data()

venn = VennPlot(style=PlotStyle.paper())

print(venn.get_shapes(n_sets=4))
#venn.set_label_formatter(lambda x: f"{x}\n({x/(plot_data['size'].sum())*100:.1f}%)")  # Uncomment to show percentage

venn.draw(
    plot_data, 
    show_region_labels=False, 
    show_set_labels=False,
    label_formatter='all',
    show_regions_border=True,
    figsize=(6, 6),
    show_set_border=False,
    #custom_colors={'Set1': '#FF6B6B', 'Set2': '#4ECDC4', 'Set3': '#45B7D1', 'Set4': '#96CEB4'},
    palette='plasma',
    #custom_set_labels=['A','B','C','D'],
    #shape_key="shape404"
    )  # Pass DataFrame directly

output_path = os.path.join(os.path.dirname(__file__), 'test_output', '4set_test_venn_output3.png')
os.makedirs(os.path.dirname(output_path), exist_ok=True)
venn.save(output_path, dpi=150)
print(f"File saved to: {os.path.abspath(output_path)}")

venn.show()
