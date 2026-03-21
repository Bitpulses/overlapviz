import numpy as np
import os
import sys


# Add parent directory to path
# sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from overlapviz.core.calculator import OverlapCalculator
from overlapviz.venn import VennPlot
from overlapviz.core import PlotStyle
import pandas as pd



np.random.seed(42) 

base_elements = [f"element_{i:03d}" for i in range(1, 201)]

set_a = set(np.random.choice(base_elements, 100, replace=False).tolist())
set_b = set(np.random.choice(base_elements, 100, replace=False).tolist())
set_c = set(np.random.choice(base_elements, 100, replace=False).tolist())
set_d = set(np.random.choice(base_elements, 100, replace=False).tolist())
set_e = set(np.random.choice(base_elements, 100, replace=False).tolist())
set_f = set(np.random.choice(base_elements, 100, replace=False).tolist())
set_g = set(np.random.choice(base_elements, 100, replace=False).tolist())
set_h = set(np.random.choice(base_elements, 100, replace=False).tolist())


# Create data with custom set names
data = {
    'A': set_a,
    'B': set_b,
    'C': set_c,
    'D': set_d,
    'E': set_e,
    'F': set_f,
    'G': set_g
}

# df = pd.DataFrame({k: pd.Series(list(v)) for k, v in data.items()})
# df.to_csv("4_sets.csv", index=False)

calc = OverlapCalculator(data)

print("Test 1: Passing OverlapCalculator object directly to draw method")
venn = VennPlot(style=PlotStyle.paper())
print(venn.get_shapes(n_sets=7))
venn.draw(calc,title="7-set Venn Diagram", show_region_labels=True, label_formatter='count',figsize=(8,8))
venn.show()
