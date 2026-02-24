# overlapviz API Reference

Welcome to the API reference documentation for overlapviz, a Python toolkit for professional set visualization. This package transforms complex data overlaps into intuitive Venn and UpSet plots.

## Package Structure

```
overlapviz/
├── __init__.py          # Main package exports
├── core/                # Core functionality
│   ├── __init__.py      # Core module exports
│   ├── baseplot.py      # Base plotting class
│   ├── plotstyle.py     # Plot styling configuration
│   └── calculator.py    # Overlap calculation utilities
├── venn/                # Venn diagram functionality
│   ├── __init__.py      # Venn module exports
│   └── venn.py          # Venn diagram plotting class
├── euler/               # Euler diagram functionality
├── upset/               # UpSet plot functionality
└── utils/               # Utility functions
```

## Main Package Interface

### [overlapviz](file:///d:/MyCode/Python/Overlapviz/overlapviz/overlapviz/__init__.py)

Main package module that exports the core functionality.

#### Exports
- [VennPlot](file:///d:/MyCode/Python/Overlapviz/overlapviz/overlapviz/venn/venn.py#L20-L427) - Create Venn diagrams for 2-7 sets
- [PlotStyle](file:///d:/MyCode/Python/Overlapviz/overlapviz/overlapviz/core/plotstyle.py#L10-L245) - Configure plot styles
- [BasePlot](file:///d:/MyCode/Python/Overlapviz/overlapviz/overlapviz/core/baseplot.py#L15-L130) - Base class for all plots

## Core Components

### [overlapviz.core](file:///d:/MyCode/Python/Overlapviz/overlapviz/overlapviz/core/__init__.py)

Core functionality for plotting and overlap calculations.

#### [PlotStyle](file:///d:/MyCode/Python/Overlapviz/overlapviz/overlapviz/core/plotstyle.py#L10-L245)

Class that manages all plotting configuration parameters.

##### Constructor
```python
PlotStyle(
    figsize: Tuple[float, float] = (10, 10),
    dpi: int = 100,
    facecolor: str = 'white',
    edgecolor: str = 'black',
    fill_alpha: float = 0.4,
    colormap: str = 'viridis',
    edge_color: str = 'black',
    edge_width: float = 2.0,
    edge_style: str = '-',  # Line style: '-' solid, '--' dashed, '-.' dash-dot, ':' dotted
    edge_alpha: float = 1.0,
    label_fontsize: int = 10,
    label_color: str = 'black',
    label_weight: str = 'bold',
    label_alpha: float = 1.0,
    label_ha: str = 'center',
    label_va: str = 'center',
    set_label_fontsize: int = 12,
    set_label_color: str = 'darkred',
    set_label_weight: str = 'bold',
    set_label_alpha: float = 1.0,
    set_label_ha: str = 'center',
    set_label_va: str = 'center',
    title_fontsize: int = 14,
    title_weight: str = 'bold',
    title_color: str = 'black',
    title_pad: float = 20.0,
    title_loc: str = 'center',
    padding_ratio: float = 0.1,
    show_axis: bool = False,
    axis_color: str = 'black',
    show_grid: bool = False,
    grid_color: str = 'gray',
    grid_alpha: float = 0.3,
    grid_linestyle: str = '--'
)
```

##### Class Methods (Predefined Styles)
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

#### [BasePlot](file:///d:/MyCode/Python/Overlapviz/overlapviz/overlapviz/core/baseplot.py#L15-L130)

Abstract base class that provides common functionality for figure creation, axis settings, and saving.

##### Constructor
```python
BasePlot(style: Optional[PlotStyle] = None)
```

##### Methods
- `create_figure()` - Create figure and axes
- `calculate_limits(df: pd.DataFrame)` - Calculate axis limits with padding
- `setup_axes(x_lim: Tuple[float, float], y_lim: Tuple[float, float])` - Set up axes with limits, aspect ratio, grid, and visibility
- `set_title(title: str)` - Set plot title with configured style
- `show()` - Display the figure
- `save(filepath: str, dpi: Optional[int] = None)` - Save the figure to file
- `close()` - Close the figure and free resources
- `draw(**kwargs)` - Abstract method to be implemented by subclasses

#### [OverlapCalculator](file:///d:/MyCode/Python/Overlapviz/overlapviz/overlapviz/core/calculator.py)

Class for analyzing overlaps between multiple sets. Provides comprehensive functionality for computing all possible set combinations, calculating intersection sizes, identifying exclusive elements, and generating pairwise overlap matrices.

##### Constructor
```python
OverlapCalculator(data: Union[Dict[str, Set], List[Set], List[Tuple[str, Set]]])
```

##### Methods
- `compute(min_size: int = 0, max_size: Optional[int] = None) -> pd.DataFrame` - Compute all overlaps between sets
- `compute_exclusive() -> pd.DataFrame` - Compute exclusive elements for each individual set
- `get_pairwise_overlap() -> Dict[str, pd.DataFrame]` - Generate pairwise overlap and Jaccard similarity matrices
- `query_elements(query_sets: Optional[List[str]] = None) -> Union[Dict[str, Any], List[Dict[str, Any]]]` - Query overlap information for specific set combinations
- `get_summary() -> Dict[str, Any]` - Get summary statistics
- `get_plot_data() -> pd.DataFrame` - Get data formatted for plotting

## Venn Diagram Module

### [overlapviz.venn](file:///d:/MyCode/Python/Overlapviz/overlapviz/overlapviz/venn/__init__.py)

Venn diagram plotting functionality.

#### [VennPlot](file:///d:/MyCode/Python/Overlapviz/overlapviz/overlapviz/venn/venn.py#L20-L427)

Class for creating Venn diagrams for 2-7 sets.

##### Constructor
```python
VennPlot(style: Optional[PlotStyle] = None)
```

##### Attributes
- `df_edges` - DataFrame containing edge coordinates for regions
- `df_set_labels` - DataFrame containing set label positions
- `df_region_labels` - DataFrame containing region label positions
- `custom_colors` - Dictionary mapping region IDs to custom colors
- `label_formatter` - Callable to format label text

##### Methods
- `_load_geometric_data(shape_key: str = 'shape403')` - Load geometric data for the specified shape
- `_load_overlap_data(overlapdata: Union[pd.DataFrame, str])` - Load overlap data from DataFrame or CSV
- `get_shapes(n_sets: int) -> List[str]` - Get all available shape IDs for the specified number of sets
- `set_custom_colors(colors: Dict[str, str])` - Set custom colors for regions
- `set_label_formatter(formatter: Callable)` - Set a formatter function for labels
- `draw(overlapdata: Union[pd.DataFrame, str], shape_key: Optional[str] = None, title: str = "Venn Diagram", show_region_labels: bool = True, show_set_labels: bool = True, label_formatter: str = 'count')` - Draw the Venn diagram
- `plot(overlapdata: Union[pd.DataFrame, str], shape_key: Optional[str] = None, title: str = "Venn Diagram", label_formatter: str = 'count', **kwargs)` - Convenience method to draw and display the Venn diagram
- `get_statistics() -> Dict` - Get statistics about the Venn diagram

## Euler Diagram Module

### [overlapviz.euler](file:///d:/MyCode/Python/Overlapviz/overlapviz/overlapviz/euler/__init__.py)

Placeholder module for Euler diagram functionality (to be implemented).

## UpSet Plot Module

### [overlapviz.upset](file:///d:/MyCode/Python/Overlapviz/overlapviz/overlapviz/upset/__init__.py)

Placeholder module for UpSet plot functionality (to be implemented).

## Utilities

### [overlapviz.utils](file:///d:/MyCode/Python/Overlapviz/overlapviz/overlapviz/utils/__init__.py)

Placeholder module for utility functions (to be implemented).