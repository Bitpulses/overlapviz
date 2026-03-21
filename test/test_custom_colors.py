"""
Test custom_colors and palette parameters
"""
import numpy as np
import os
import sys

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

data = {
    'A': set_a,
    'B': set_b,
    'C': set_c,
    'D': set_d,
}

calc = OverlapCalculator(data)
plot_data = calc.get_plot_data()

# Test 1: Use custom_colors parameter
print("Test 1: Using custom_colors parameter")
venn1 = VennPlot(style=PlotStyle.paper())
venn1.draw(
    plot_data, 
    show_region_labels=True, 
    label_formatter='all',
    custom_colors={'A': '#FF6B6B', 'B': '#4ECDC4', 'C': '#45B7D1', 'D': '#96CEB4'},
    shape_key="shape403")
output_path1 = os.path.join(os.path.dirname(__file__), 'test_output', 'test_custom_colors.png')
os.makedirs(os.path.dirname(output_path1), exist_ok=True)
venn1.save(output_path1, dpi=150)
print(f"File saved to: {os.path.abspath(output_path1)}")

# Test 2: Use palette parameter
print("\nTest 2: Using palette parameter")
venn2 = VennPlot(style=PlotStyle.paper())
venn2.draw(
    plot_data, 
    show_region_labels=True, 
    label_formatter='all',
    palette='Set1',
    shape_key="shape403")
output_path2 = os.path.join(os.path.dirname(__file__), 'test_output', 'test_palette.png')
os.makedirs(os.path.dirname(output_path2), exist_ok=True)
venn2.save(output_path2, dpi=150)
print(f"File saved to: {os.path.abspath(output_path2)}")

# Test 3: Use palette with different colormap
print("\nTest 3: Using palette='Pastel1'")
venn3 = VennPlot(style=PlotStyle.paper())
venn3.draw(
    plot_data, 
    show_region_labels=True, 
    label_formatter='all',
    palette='Pastel1',
    shape_key="shape403")
output_path3 = os.path.join(os.path.dirname(__file__), 'test_output', 'test_palette_pastel.png')
os.makedirs(os.path.dirname(output_path3), exist_ok=True)
venn3.save(output_path3, dpi=150)
print(f"File saved to: {os.path.abspath(output_path3)}")

# Test 4: Use plot method with custom_colors
print("\nTest 4: Using plot method with custom_colors")
venn4 = VennPlot(style=PlotStyle.paper())
venn4.plot(
    plot_data, 
    show_region_labels=True, 
    label_formatter='all',
    custom_colors={'A': '#E74C3C', 'B': '#3498DB', 'C': '#2ECC71', 'D': '#F39C12'},
    shape_key="shape403")

print("\nAll tests completed successfully!")
