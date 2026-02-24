# overlapviz Usage Guide

This guide provides practical examples and usage patterns for the overlapviz package.

## Table of Contents
1. [Installation](#installation)
2. [Basic Usage](#basic-usage)
3. [Venn Diagrams](#venn-diagrams)
4. [Styling](#styling)
5. [Advanced Features](#advanced-features)

## Installation

The package can be installed in development mode:

```bash
pip install -e .
```

Or as a regular package:

```bash
pip install .
```

## Basic Usage

### Creating a Simple Venn Diagram

```python
from overlapviz import VennPlot
import pandas as pd

# Create sample data
data = pd.DataFrame({
    'set_names': ['A', 'B', 'C', 'A_B', 'A_C', 'B_C', 'A_B_C'],
    'size': [10, 15, 8, 5, 3, 4, 2]
})

# Create and draw Venn diagram
venn = VennPlot()
venn.plot(data, title="My Venn Diagram")
```

### Using Different Shapes

```python
from overlapviz import VennPlot

# Get available shapes for 4 sets
shapes = VennPlot.get_shapes(4)
print(f"Available shapes for 4 sets: {shapes}")

# Use a specific shape
venn = VennPlot()
venn.draw(data, shape_key='shape403', title="4-Set Venn with Specific Shape")
venn.show()
```

## Venn Diagrams

### Loading Data

Venn diagrams accept data in two formats:
1. Pandas DataFrame with 'set_names' and 'size' columns
2. CSV file path

```python
from overlapviz import VennPlot
import pandas as pd

# From DataFrame
df = pd.DataFrame({
    'set_names': ['A', 'B', 'C', 'A_B'],
    'size': [10, 15, 12, 5]
})
venn = VennPlot()
venn.draw(df)

# From CSV file
venn2 = VennPlot()
venn2.draw('path/to/data.csv')
```

### Customizing Labels

```python
from overlapviz import VennPlot

venn = VennPlot()

# Format labels as percentages
venn.draw(data, label_formatter='percentage')

# Format labels as both counts and percentages
venn.draw(data, label_formatter='all')

# Use a custom formatter function
def custom_formatter(value):
    return f"N={int(value)}"

venn.set_label_formatter(custom_formatter)
venn.draw(data)
```

### Setting Custom Colors

```python
from overlapviz import VennPlot

venn = VennPlot()

# Define custom colors for specific regions
colors = {
    'A': 'red',
    'B': 'blue',
    'C': 'green',
    'A_B': 'yellow',
    'A_C': 'orange',
    'B_C': 'purple',
    'A_B_C': 'pink'
}

venn.set_custom_colors(colors)
venn.draw(data)
venn.show()
```

## Styling

### Using Predefined Styles

```python
from overlapviz import VennPlot, PlotStyle

# Use predefined styles
venn = VennPlot(PlotStyle.bold())  # Bold style
venn = VennPlot(PlotStyle.soft())  # Soft style
venn = VennPlot(PlotStyle.dark())  # Dark theme
venn = VennPlot(PlotStyle.paper())  # Paper-friendly style
```

### Customizing Plot Style

```python
from overlapviz import VennPlot, PlotStyle

# Create custom style
style = PlotStyle()
style.colormap = 'Set1'
style.fill_alpha = 0.6
style.edge_width = 3.0
style.label_fontsize = 14

venn = VennPlot(style)
venn.draw(data)
venn.show()
```

### Available Predefined Styles

- `soft()` - Soft colors, thin borders
- `bold()` - Vivid colors, thick borders
- `paper()` - Professional colors, high resolution
- `white()` - White borders, white labels
- `clean()` - White borders, black labels
- `dark()` - Dark background, white borders
- `pastel()` - Soft white borders
- `vivid()` - High contrast
- `poster()` - Large font presentation
- `print()` - High DPI print quality
- `dashed()` - Dashed border
- `dotted()` - Dotted border
- `dashdot()` - Dash-dot border

## Advanced Features

### Getting Statistics

```python
from overlapviz import VennPlot

venn = VennPlot()
venn.draw(data)

# Get statistics about the diagram
stats = venn.get_statistics()
print(f"Number of regions: {stats['n_regions']}")
print(f"Number of sets: {stats['n_sets']}")
print(f"Total size: {stats['total_size']}")
print(f"Mean size: {stats['mean_size']}")
```

### Saving Figures

```python
from overlapviz import VennPlot

venn = VennPlot()
venn.draw(data)

# Save the figure
venn.save('my_venn.png', dpi=300)  # High-resolution PNG
venn.save('my_venn.pdf')  # PDF format
```

### Manual Figure Creation and Display

```python
from overlapviz import VennPlot

venn = VennPlot()

# Draw without showing
venn.draw(data, title="My Diagram")

# Manually show or save
venn.show()  # Display the figure
venn.save('output.png')  # Save to file
venn.close()  # Close the figure to free memory
```

## Working with OverlapCalculator

The package includes an OverlapCalculator for analyzing set overlaps:

```python
from overlapviz.core.calculator import OverlapCalculator

# Create sample data
sets_data = {
    'Set A': {'element1', 'element2', 'element3', 'element4'},
    'Set B': {'element2', 'element3', 'element5', 'element6'},
    'Set C': {'element3', 'element4', 'element6', 'element7'}
}

# Create calculator
calc = OverlapCalculator(sets_data)

# Get all combinations
combinations = calc.query_elements()
for combo in combinations:
    if combo['size'] > 0:  # Only show non-empty overlaps
        print(f"{combo['set_names']}: {combo['size']} elements")
        print(f"  Elements: {sorted(combo['elements'])}")
        print(f"  Exclusive elements: {sorted(combo['exclusive_elements'])}")
        print()

# Query specific combination
specific_combo = calc.query_elements(['Set A', 'Set B'])
print(f"A ∩ B: {specific_combo['elements']}")

# Compute all overlaps with size thresholds
df_overlaps = calc.compute(min_size=1)  # Only non-empty
print("\nAll non-empty overlaps:")
print(df_overlaps[['set_names', 'size', 'elements']])

# Get exclusive elements for each set
exclusive_df = calc.compute_exclusive()
print("\nExclusive elements for each set:")
print(exclusive_df[['set', 'exclusive_size', 'exclusive_elements']])

# Get pairwise overlap matrices
matrices = calc.get_pairwise_overlap()
print("\nPairwise overlap matrix:")
print(matrices['overlap_matrix'])
print("\nJaccard similarity matrix:")
print(matrices['jaccard_matrix'].round(3))

# Get data formatted for plotting
plot_data = calc.get_plot_data()
print("\nPlotting data:")
print(plot_data)
```