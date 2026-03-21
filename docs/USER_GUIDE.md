# OverlapViz User Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Core Modules](#core-modules)
   - [OverlapCalculator - Set Overlap Calculator](#overlapcalculator---set-overlap-calculator)
   - [VennPlot - Venn Diagram Plotting Class](#vennplot---venn-diagram-plotting-class)
   - [PlotStyle - Plot Style Configuration](#plotstyle---plot-style-configuration)
5. [Detailed Usage](#detailed-usage)
   - [Data Input Formats](#data-input-formats)
   - [Plot Style Customization](#plot-style-customization)
   - [Color Configuration](#color-configuration)
   - [Label Formatting](#label-formatting)
6. [API Reference](#api-reference)
7. [FAQ](#faq)

---

## Introduction

**OverlapViz** is a professional Python toolkit for set visualization, designed to transform complex data overlaps into intuitive Venn diagrams. It supports visualization of 2-7 sets with rich customization options.

### Key Features

- Support for 2-7 set Venn diagrams
- Automatic calculation of all set overlap combinations
- Rich predefined style themes
- Highly customizable colors, labels, and layouts
- Multiple data input format support
- High-resolution output suitable for publication

---

## Installation

### Requirements

- Python >= 3.12
- matplotlib >= 3.5.0
- numpy >= 1.20.0
- pandas >= 1.3.0

### Installation

```bash
git clone https://github.com/your-repo/overlapviz.git
cd overlapviz
pip install .
```

### Development Installation

```bash
git clone https://github.com/your-repo/overlapviz.git
cd overlapviz
pip install -e .
```

---

## Quick Start

### Minimal Example

```python
from overlapviz import VennPlot
from overlapviz.core import OverlapCalculator

# Prepare data
data = {
    'SetA': {'gene1', 'gene2', 'gene3', 'gene4'},
    'SetB': {'gene2', 'gene3', 'gene5', 'gene6'},
    'SetC': {'gene3', 'gene4', 'gene6', 'gene7'}
}

# Calculate overlaps
calc = OverlapCalculator(data)

# Draw Venn diagram
venn = VennPlot()
venn.draw(calc)
venn.show()
```

### Using Predefined Styles

```python
from overlapviz import VennPlot, PlotStyle

venn = VennPlot(style=PlotStyle.paper())
venn.draw(calc, title="Gene Set Overlap")
venn.save("output.png", dpi=300)
```

---

## Core Modules

### OverlapCalculator - Set Overlap Calculator

`OverlapCalculator` is the core tool for set overlap analysis, calculating all overlap combinations between multiple sets.

#### Constructor

```python
OverlapCalculator(data)
```

**Parameters:**

| Parameter | Type                                                    | Description                           |
| --------- | ------------------------------------------------------- | ------------------------------------- |
| `data`  | Union[Dict[str, Set], List[Set], List[Tuple[str, Set]]] | Input data, supports multiple formats |

#### Core Methods

##### `compute()` - Calculate All Overlap Combinations

```python
calc.compute(min_size=0, max_size=None)
```

Calculates all possible set combinations (2^n - 1 total), returning a DataFrame with detailed information for each combination.

**Parameters:**

| Parameter    | Type          | Default | Description                      |
| ------------ | ------------- | ------- | -------------------------------- |
| `min_size` | int           | 0       | Minimum intersection size filter |
| `max_size` | Optional[int] | None    | Maximum intersection size filter |

**Returned DataFrame Columns:**

| Column                 | Type  | Description                               |
| ---------------------- | ----- | ----------------------------------------- |
| `sets`               | tuple | Tuple of set names                        |
| `set_names`          | str   | String representation (e.g., "A & B & C") |
| `n_sets`             | int   | Number of participating sets              |
| `size`               | int   | Intersection size                         |
| `elements`           | list  | Sorted list of intersection elements      |
| `exclusive_size`     | int   | Number of exclusive elements              |
| `exclusive_elements` | list  | Sorted list of exclusive elements         |

**Example:**

```python
from overlapviz.core import OverlapCalculator

data = {
    'A': {1, 2, 3, 4, 5},
    'B': {2, 3, 4, 6, 7},
    'C': {3, 4, 5, 7, 8}
}

calc = OverlapCalculator(data)
df = calc.compute(min_size=1)  # Return only non-empty intersections
print(df[['set_names', 'size', 'n_sets']])
```

##### `compute_exclusive()` - Calculate Exclusive Elements

```python
calc.compute_exclusive()
```

Returns the exclusive elements for each set (elements belonging only to that set).

**Example:**

```python
exclusive_df = calc.compute_exclusive()
print(exclusive_df[['set', 'exclusive_size', 'exclusive_elements']])
```

##### `get_pairwise_overlap()` - Pairwise Overlap Matrices

```python
calc.get_pairwise_overlap()
```

Generates intersection matrices and Jaccard similarity matrices for all set pairs.

**Returned Dictionary:**

| Key                | Value Type   | Description                       |
| ------------------ | ------------ | --------------------------------- |
| `overlap_matrix` | pd.DataFrame | Pairwise intersection size matrix |
| `jaccard_matrix` | pd.DataFrame | Jaccard similarity matrix         |

**Example:**

```python
matrices = calc.get_pairwise_overlap()
print("Overlap Matrix:")
print(matrices['overlap_matrix'])
print("\nJaccard Similarity Matrix:")
print(matrices['jaccard_matrix'].round(3))
```

##### `get_summary()` - Statistical Summary

```python
calc.get_summary()
```

Returns a dictionary of comprehensive statistical information.

**Returned Dictionary Contents:**

| Key                       | Type  | Description                           |
| ------------------------- | ----- | ------------------------------------- |
| `n_sets`                | int   | Number of sets                        |
| `total_unique_elements` | int   | Total number of unique elements       |
| `all_common_size`       | int   | Number of elements common to all sets |
| `set_sizes`             | dict  | Size of each set                      |
| `mean_overlap`          | float | Average pairwise overlap rate         |
| `max_overlap`           | tuple | Set pair with maximum overlap         |

##### `get_plot_data()` - Get Plotting Data

```python
calc.get_plot_data()
```

Returns a DataFrame for Venn diagram plotting, containing exclusive element calculations.

##### `query_elements()` - Query Specific Combination

```python
calc.query_elements(query_sets=['A', 'B'])
```

Query overlap information for a specific set combination.

**Example:**

```python
result = calc.query_elements(['A', 'B'])
print(f"Elements in A ∩ B: {result['elements']}")
print(f"Size of A ∩ B: {result['size']}")
```

---

### VennPlot - Venn Diagram Plotting Class

`VennPlot` is used to create Venn diagrams for 2-7 sets.

#### Constructor

```python
VennPlot(style=None)
```

**Parameters:**

| Parameter | Type                | Default | Description                                       |
| --------- | ------------------- | ------- | ------------------------------------------------- |
| `style` | Optional[PlotStyle] | None    | Plot style configuration, defaults to PlotStyle() |

#### Core Methods

##### `draw()` - Draw Venn Diagram

```python
venn.draw(
    overlapdata,
    shape_key=None,
    title="Venn Diagram",
    show_region_labels=True,
    show_set_labels=True,
    label_formatter='count',
    show_regions_border=True,
    show_set_border=True,
    custom_set_labels=None,
    custom_colors=None,
    palette=None,
    figsize=None
)
```

**Parameter Details:**

| Parameter               | Type                                        | Default        | Description                                                            |
| ----------------------- | ------------------------------------------- | -------------- | ---------------------------------------------------------------------- |
| `overlapdata`         | Union[pd.DataFrame, str, OverlapCalculator] | Required       | Data source, supports DataFrame, CSV path, or OverlapCalculator object |
| `shape_key`           | Optional[str]                               | None           | Geometric shape key, e.g., 'shape403'; auto-selected if None           |
| `title`               | str                                         | "Venn Diagram" | Chart title                                                            |
| `show_region_labels`  | bool                                        | True           | Whether to show region labels (values)                                 |
| `show_set_labels`     | bool                                        | True           | Whether to show set name labels                                        |
| `label_formatter`     | str                                         | 'count'        | Label format: 'count'(values), 'percentage', 'all'(both)               |
| `show_regions_border` | bool                                        | True           | Whether to show region fills                                           |
| `show_set_border`     | bool                                        | True           | Whether to show set borders                                            |
| `custom_set_labels`   | Optional[List[str]]                         | None           | Custom set label list                                                  |
| `custom_colors`       | Optional[Dict[str, str]]                    | None           | Custom color dictionary                                                |
| `palette`             | Optional[str]                               | None           | matplotlib colormap name                                               |
| `figsize`             | Optional[Tuple[float, float]]               | None           | Figure size (width, height) in inches                                  |

##### `plot()` - Draw and Display

```python
venn.plot(overlapdata, **kwargs)
```

Convenience method that calls `draw()` and then automatically calls `show()`.

##### `get_shapes()` - Get Available Shapes

```python
VennPlot.get_shapes(n_sets)
```

Static method that returns the list of available shape keys for a specified number of sets.

**Example:**

```python
print(VennPlot.get_shapes(3))  # ['shape301']
print(VennPlot.get_shapes(4))  # ['shape403', 'shape404']
print(VennPlot.get_shapes(7))  # ['shape701']
```

##### `save()` - Save Figure

```python
venn.save(filepath, dpi=None)
```

Saves the figure to a file, supporting PNG, PDF, SVG, and other formats.

**Example:**

```python
venn.save("output.png", dpi=300)
venn.save("output.pdf")
venn.save("output.svg")
```

##### `get_statistics()` - Get Statistics

```python
venn.get_statistics()
```

Returns statistical information about the Venn diagram.

---

### PlotStyle - Plot Style Configuration

`PlotStyle` is a data class used to configure various plotting style parameters.

#### Constructor

```python
PlotStyle(
    figsize=(10, 10),
    dpi=100,
    facecolor='white',
    edgecolor='black',
    fill_alpha=0.4,
    colormap='viridis',
    edge_color='black',
    edge_width=2.0,
    edge_style='-',
    edge_alpha=1.0,
    label_fontsize=10,
    label_color='black',
    label_weight='bold',
    set_label_fontsize=12,
    set_label_color='darkred',
    title_fontsize=14,
    padding_ratio=0.1,
    show_axis=False,
    show_grid=False
)
```

#### Parameter Description

| Parameter              | Type                | Default   | Description                           |
| ---------------------- | ------------------- | --------- | ------------------------------------- |
| `figsize`            | Tuple[float, float] | (10, 10)  | Figure size (width, height) in inches |
| `dpi`                | int                 | 100       | Resolution (dots per inch)            |
| `facecolor`          | str                 | 'white'   | Figure background color               |
| `edgecolor`          | str                 | 'black'   | Figure edge color                     |
| `fill_alpha`         | float               | 0.4       | Region fill transparency (0-1)        |
| `colormap`           | str                 | 'viridis' | Default colormap                      |
| `edge_color`         | str                 | 'black'   | Set border color                      |
| `edge_width`         | float               | 2.0       | Border line width                     |
| `edge_style`         | str                 | '-'       | Border style: '-', '--', '-.', ':'    |
| `edge_alpha`         | float               | 1.0       | Border transparency (0-1)             |
| `label_fontsize`     | int                 | 10        | Region label font size                |
| `label_color`        | str                 | 'black'   | Region label color                    |
| `label_weight`       | str                 | 'bold'    | Region label font weight              |
| `set_label_fontsize` | int                 | 12        | Set label font size                   |
| `set_label_color`    | str                 | 'darkred' | Set label color                       |
| `title_fontsize`     | int                 | 14        | Title font size                       |
| `padding_ratio`      | float               | 0.1       | Padding ratio                         |
| `show_axis`          | bool                | False     | Whether to show axes                  |
| `show_grid`          | bool                | False     | Whether to show grid                  |

#### Predefined Styles

```python
from overlapviz import PlotStyle

# Paper style - professional colors, high resolution
style = PlotStyle.paper()

# Dark style - dark background, white borders
style = PlotStyle.dark()

# Poster style - large fonts for display
style = PlotStyle.poster()

# Soft style - light colors, thin borders
style = PlotStyle.soft()

# Bold style - vivid colors, thick borders
style = PlotStyle.bold()

# Clean style - white borders, black labels
style = PlotStyle.clean()

# Pastel style - soft color palette
style = PlotStyle.pastel()

# Vivid style - high contrast
style = PlotStyle.vivid()

# Print style - high DPI for print quality
style = PlotStyle.print()

# Dashed border
style = PlotStyle.dashed()

# Dotted border
style = PlotStyle.dotted()

# Dash-dot border
style = PlotStyle.dashdot()
```

---

## Detailed Usage

### Data Input Formats

OverlapViz supports multiple data input formats:

#### 1. Dictionary Format (Recommended)

```python
data = {
    'SetA': {'gene1', 'gene2', 'gene3'},
    'SetB': {'gene2', 'gene3', 'gene4'},
    'SetC': {'gene3', 'gene4', 'gene5'}
}
calc = OverlapCalculator(data)
```

#### 2. List of Sets

```python
data = [
    {'gene1', 'gene2', 'gene3'},
    {'gene2', 'gene3', 'gene4'},
    {'gene3', 'gene4', 'gene5'}
]
calc = OverlapCalculator(data)
```

#### 3. List of Tuples

```python
data = [
    ('SetA', {'gene1', 'gene2', 'gene3'}),
    ('SetB', {'gene2', 'gene3', 'gene4'}),
    ('SetC', {'gene3', 'gene4', 'gene5'})
]
calc = OverlapCalculator(data)
```

#### 4. DataFrame Format

```python
import pandas as pd

df = pd.DataFrame({
    'set_names': ['A', 'B', 'A_B', 'A_C', 'B_C', 'A_B_C'],
    'size': [10, 15, 5, 3, 4, 2]
})

venn = VennPlot()
venn.draw(df)
```

#### 5. CSV File

```python
venn = VennPlot()
venn.draw("data.csv")  # CSV file path
```

#### 6. Direct OverlapCalculator Object

```python
calc = OverlapCalculator(data)
venn = VennPlot()
venn.draw(calc)  # Automatically calls get_plot_data()
```

---

### Plot Style Customization

#### Custom Style

```python
from overlapviz import VennPlot, PlotStyle

# Create custom style
custom_style = PlotStyle(
    figsize=(12, 12),
    dpi=150,
    fill_alpha=0.5,
    edge_width=3.0,
    edge_style='--',
    label_fontsize=12,
    set_label_fontsize=14,
    set_label_color='navy'
)

venn = VennPlot(style=custom_style)
venn.draw(calc)
```

#### Modify Predefined Style

```python
# Modify based on predefined style
style = PlotStyle.paper()
style.figsize = (15, 15)
style.fill_alpha = 0.6

venn = VennPlot(style=style)
```

---

### Color Configuration

#### Using Colormaps

```python
venn = VennPlot()
venn.draw(calc, palette='Set2')
```

**Common Colormaps:**

- `viridis` - Default, perceptually uniform
- `Set1`, `Set2`, `Set3` - Discrete colors
- `tab10`, `tab20` - Tableau colors
- `Pastel1`, `Pastel2` - Soft colors
- `plasma`, `inferno` - Heat colors

#### Custom Colors

```python
custom_colors = {
    'A': '#FF6B6B',      # Set A
    'B': '#4ECDC4',      # Set B
    'C': '#45B7D1',      # Set C
    'A_B': '#FFBE0B',    # A ∩ B
    'A_C': '#FB5607',    # A ∩ C
    'B_C': '#8338EC',    # B ∩ C
    'A_B_C': '#3A86FF'   # A ∩ B ∩ C
}

venn.draw(calc, custom_colors=custom_colors)
```

---

### Label Formatting

#### Built-in Formatting Options

```python
# Show counts
venn.draw(calc, label_formatter='count')

# Show percentages
venn.draw(calc, label_formatter='percentage')

# Show both counts and percentages
venn.draw(calc, label_formatter='all')
```

#### Custom Formatting Function

```python
# Custom format
venn.set_label_formatter(lambda x: f"N={int(x)}")
venn.draw(calc)

# Conditional formatting
def format_label(x):
    if x > 100:
        return f"{int(x)} (large)"
    elif x > 10:
        return f"{int(x)} (medium)"
    else:
        return f"{int(x)} (small)"

venn.set_label_formatter(format_label)
venn.draw(calc)
```

---

## API Reference

### VennPlot

```python
class VennPlot(BasePlot):
    """
    Venn diagram plotting class
  
    Supports Venn diagrams for 2-7 sets.
    """
  
    def __init__(self, style: Optional[PlotStyle] = None)
  
    @staticmethod
    def get_shapes(n_sets: int) -> List[str]
  
    def draw(
        self,
        overlapdata: Union[pd.DataFrame, str, OverlapCalculator],
        shape_key: Optional[str] = None,
        title: str = "Venn Diagram",
        show_region_labels: bool = True,
        show_set_labels: bool = True,
        label_formatter: str = 'count',
        show_regions_border: bool = True,
        show_set_border: bool = True,
        custom_set_labels: Optional[List[str]] = None,
        custom_colors: Optional[Dict[str, str]] = None,
        palette: Optional[str] = None,
        figsize: Optional[Tuple[float, float]] = None
    ) -> None
  
    def plot(
        self,
        overlapdata: Union[pd.DataFrame, str],
        shape_key: Optional[str] = None,
        title: str = "Venn Diagram",
        label_formatter: str = 'count',
        custom_set_labels: Optional[List[str]] = None,
        custom_colors: Optional[Dict[str, str]] = None,
        palette: Optional[str] = None,
        figsize: Optional[Tuple[float, float]] = None,
        **kwargs
    ) -> None
  
    def save(self, filepath: str, dpi: Optional[int] = None) -> None
    def show(self) -> None
    def close(self) -> None
    def get_statistics(self) -> Dict
    def set_custom_colors(self, colors: Dict[str, str]) -> None
    def set_label_formatter(self, formatter: Callable) -> None
```

### OverlapCalculator

```python
class OverlapCalculator:
    """
    Set overlap calculator
  
    Calculates all overlap combinations between multiple sets.
    """
  
    def __init__(
        self,
        data: Union[Dict[str, Set], List[Set], List[Tuple[str, Set]]]
    )
  
    @property
    def sets_names(self) -> List[str]
  
    def compute(
        self,
        min_size: int = 0,
        max_size: Optional[int] = None
    ) -> pd.DataFrame
  
    def compute_exclusive(self) -> pd.DataFrame
    def get_pairwise_overlap(self) -> Dict[str, pd.DataFrame]
    def get_summary(self) -> Dict[str, Any]
    def get_dataframe(self) -> pd.DataFrame
    def get_plot_data(self) -> pd.DataFrame
    def query_elements(
        self,
        query_sets: Optional[List[str]] = None
    ) -> Union[Dict, List]
```

### PlotStyle

```python
@dataclass
class PlotStyle:
    """
    Plot style configuration class
    """
  
    figsize: Tuple[float, float] = (10, 10)
    dpi: int = 100
    facecolor: str = 'white'
    edgecolor: str = 'black'
    fill_alpha: float = 0.4
    colormap: str = 'viridis'
    edge_color: str = 'black'
    edge_width: float = 2.0
    edge_style: str = '-'
    edge_alpha: float = 1.0
    label_fontsize: int = 10
    label_color: str = 'black'
    label_weight: str = 'bold'
    set_label_fontsize: int = 12
    set_label_color: str = 'darkred'
    title_fontsize: int = 14
    padding_ratio: float = 0.1
    show_axis: bool = False
    show_grid: bool = False
  
    @classmethod
    def paper(cls) -> 'PlotStyle'
    @classmethod
    def dark(cls) -> 'PlotStyle'
    @classmethod
    def poster(cls) -> 'PlotStyle'
    @classmethod
    def soft(cls) -> 'PlotStyle'
    @classmethod
    def bold(cls) -> 'PlotStyle'
    @classmethod
    def clean(cls) -> 'PlotStyle'
    @classmethod
    def white(cls) -> 'PlotStyle'
    @classmethod
    def pastel(cls) -> 'PlotStyle'
    @classmethod
    def vivid(cls) -> 'PlotStyle'
    @classmethod
    def print(cls) -> 'PlotStyle'
    @classmethod
    def dashed(cls) -> 'PlotStyle'
    @classmethod
    def dotted(cls) -> 'PlotStyle'
    @classmethod
    def dashdot(cls) -> 'PlotStyle'
```

---

## FAQ

### Q: How many sets are supported?

A: VennPlot supports 2-7 sets. For more sets, consider using UpSet plots (coming soon).

### Q: How do I choose the right shape?

A: Use `VennPlot.get_shapes(n_sets)` to see available shapes. If `shape_key` is not specified, the first available shape is automatically selected.

### Q: How do I export high-resolution images?

A: Specify the `dpi` parameter when using the `save()` method:

```python
venn.save("output.png", dpi=300)
```

### Q: How do I hide certain labels?

A: Use the `show_region_labels` and `show_set_labels` parameters:

```python
venn.draw(calc, show_region_labels=False, show_set_labels=True)
```

### Q: How do I handle empty intersections?

A: `OverlapCalculator.compute(min_size=0)` includes all combinations, including empty intersections. Use `min_size=1` to return only non-empty intersections.

### Q: What output formats are supported?

A: All formats supported by matplotlib, including PNG, PDF, SVG, EPS, etc.

---

## Complete Example

```python
import numpy as np
from overlapviz import VennPlot, PlotStyle
from overlapviz.core import OverlapCalculator

# 1. Prepare data
np.random.seed(42)
base_elements = [f"gene_{i:03d}" for i in range(1, 201)]

data = {
    'SetA': set(np.random.choice(base_elements, 100, replace=False).tolist()),
    'SetB': set(np.random.choice(base_elements, 100, replace=False).tolist()),
    'SetC': set(np.random.choice(base_elements, 100, replace=False).tolist()),
    'SetD': set(np.random.choice(base_elements, 100, replace=False).tolist())
}

# 2. Calculate overlaps
calc = OverlapCalculator(data)

# 3. View statistics
summary = calc.get_summary()
print(f"Number of sets: {summary['n_sets']}")
print(f"Total unique elements: {summary['total_unique_elements']}")

# 4. View available shapes
print(f"Available shapes: {VennPlot.get_shapes(4)}")

# 5. Draw Venn diagram
venn = VennPlot(style=PlotStyle.paper())
venn.draw(
    calc,
    title="4-Set Gene Overlap Analysis",
    label_formatter='all',
    figsize=(12, 12),
    palette='Set2'
)

# 6. Save figure
venn.save("venn_output.png", dpi=300)

# 7. Display figure
venn.show()

# 8. Get chart statistics
stats = venn.get_statistics()
print(f"Number of regions: {stats['n_regions']}")
print(f"Total elements: {stats['total_size']}")
```

---

## Version History

### v0.1.0 (Current)

- Support for 2-7 set Venn diagrams
- OverlapCalculator for set overlap calculation
- Rich predefined styles
- Custom colors and labels
- Multiple data input format support

---

## License

MIT License

---

## Contact

For questions or suggestions, please submit an Issue or Pull Request.
