# overlapviz Detailed API Documentation

## overlapviz.venn.VennPlot

### Class Definition
```python
class VennPlot(BasePlot):
```

### Constructor
```python
def __init__(self, style: Optional[PlotStyle] = None):
```
**Description**: Initializes a VennPlot instance.
**Parameters**:
- `style`: Plotting style, defaults to PlotStyle()
**Returns**: VennPlot instance

### Public Methods

#### `get_shapes`
```python
@staticmethod
def get_shapes(n_sets: int) -> List[str]:
```
**Description**: Get all available shape IDs for the specified number of sets.
**Parameters**:
- `n_sets`: Number of sets (2-5)
**Returns**: List of available shape IDs
**Example**:
```python
>>> VennPlot.get_shapes(4)
['shape403', 'shape404']
```

#### `set_custom_colors`
```python
def set_custom_colors(self, colors: Dict[str, str]):
```
**Description**: Sets custom colors for regions.
**Parameters**:
- `colors`: {region_id: color} mapping

#### `set_label_formatter`
```python
def set_label_formatter(self, formatter: Callable):
```
**Description**: Sets a formatting function for labels.
**Parameters**:
- `formatter`: Formatting function func(value) -> str

#### `draw`
```python
def draw(self,
         overlapdata: Union[pd.DataFrame, str],
         shape_key: Optional[str] = None,
         title: str = "Venn Diagram",
         show_region_labels: bool = True,
         show_set_labels: bool = True,
         label_formatter: str = 'count'):
```
**Description**: Draws a Venn diagram.
**Parameters**:
- `overlapdata`: Data source, can be:
  - pd.DataFrame: Overlap data DataFrame (e.g., output from calc.get_plot_data())
  - str: CSV file path
- `shape_key`: Geometric data key name, defaults to None (automatically calculates number of sets from data and selects first available shape)
  - Options: 'shape201'(2 sets), 'shape301'(3 sets), 'shape403'(4 sets), 'shape501'(5 sets), etc.
- `title`: Title
- `show_region_labels`: Whether to show region labels
- `show_set_labels`: Whether to show set labels
- `label_formatter`: Label format, options 'count'(value), 'percentage', 'all'(both)

#### `plot`
```python
def plot(self, overlapdata: Union[pd.DataFrame, str],
         shape_key: Optional[str] = None,
         title: str = "Venn Diagram",
         label_formatter: str = 'count',
         **kwargs):
```
**Description**: Draws and displays the Venn diagram (convenience method that calls draw() and then show()).
**Parameters**:
- `overlapdata`: Data source (DataFrame or CSV path)
- `shape_key`: Geometric data key name, defaults to None (auto-select)
- `title`: Title
- `label_formatter`: Label format, options 'count', 'percentage', 'all'
- `**kwargs`: Additional parameters passed to draw

#### `get_statistics`
```python
def get_statistics(self) -> Dict:
```
**Description**: Gets statistics about the Venn diagram.
**Returns**: Dictionary containing region count, set count, and size statistics

### Private Methods

#### `_load_geometric_data`
```python
def _load_geometric_data(self, shape_key: str = 'shape403'):
```
**Description**: Loads geometric data (fixed to use geometric_data_v3.pkl in the current directory).
**Parameters**:
- `shape_key`: Data key name, defaults to 'shape403' (4 sets)
  - Options: 'shape201'(2 sets), 'shape301'(3 sets), 'shape403'(4 sets), 'shape501'(5 sets)

#### `_load_overlap_data`
```python
def _load_overlap_data(self, overlapdata: Union[pd.DataFrame, str]):
```
**Description**: Loads overlap data.
**Parameters**:
- `overlapdata`: Data source, can be:
  - pd.DataFrame: Overlap data DataFrame (e.g., output from calc.get_plot_data())
  - str: CSV file path

#### `_get_n_sets_from_data`
```python
def _get_n_sets_from_data(self, overlapdata: Union[pd.DataFrame, str]) -> int:
```
**Description**: Calculates the number of sets from overlapdata.
**Parameters**:
- `overlapdata`: Data source
**Returns**: Number of sets
**Raises**:
- `ValueError`: When unable to calculate number of sets from data

#### `_get_colors`
```python
def _get_colors(self):
```
**Description**: Generates color mapping for regions.
**Returns**: Dict mapping region IDs to colors

#### `_draw_regions`
```python
def _draw_regions(self):
```
**Description**: Draws filled regions with colors. Each region is filled with its corresponding color based on the colormap or custom color settings.

#### `_draw_borders`
```python
def _draw_borders(self):
```
**Description**: Draws border lines around each region. Borders are drawn with consistent styling defined in plot style.

#### `_draw_region_labels`
```python
def _draw_region_labels(self):
```
**Description**: Draws labels for each region showing the size/count. Labels are positioned at the center coordinates of each region and formatted according to the specified formatter.

#### `_draw_set_labels`
```python
def _draw_set_labels(self):
```
**Description**: Draws labels for each set (A, B, C, etc.). Set labels are positioned at specified coordinates to identify each individual set in the Venn diagram.

---

## overlapviz.core.plotstyle.PlotStyle

### Class Definition
```python
@dataclass
class PlotStyle:
```

### Attributes

#### Figure Settings
- `figsize: Tuple[float, float] = (10, 10)` - Figure size in inches
- `dpi: int = 100` - Dots per inch resolution
- `facecolor: str = 'white'` - Figure background color
- `edgecolor: str = 'black'` - Figure edge color

#### Area Style
- `fill_alpha: float = 0.4` - Transparency of filled areas (0-1)
- `colormap: str = 'viridis'` - Colormap for regions

#### Border Style
- `edge_color: str = 'black'` - Color of borders
- `edge_width: float = 2.0` - Width of borders in points
- `edge_style: str = '-'` - Line style: '-' solid, '--' dashed, '-.' dash-dot, ':' dotted
- `edge_alpha: float = 1.0` - Transparency of borders (0-1)

#### Label Style
- `label_fontsize: int = 10` - Font size for region labels
- `label_color: str = 'black'` - Color of region labels
- `label_weight: str = 'bold'` - Font weight of region labels ('normal', 'bold', etc.)
- `label_alpha: float = 1.0` - Transparency of region labels (0-1)
- `label_ha: str = 'center'` - Horizontal alignment ('left', 'center', 'right')
- `label_va: str = 'center'` - Vertical alignment ('top', 'center', 'bottom')

#### Set Label Style
- `set_label_fontsize: int = 12` - Font size for set labels
- `set_label_color: str = 'darkred'` - Color of set labels
- `set_label_weight: str = 'bold'` - Font weight of set labels
- `set_label_alpha: float = 1.0` - Transparency of set labels (0-1)
- `set_label_ha: str = 'center'` - Horizontal alignment of set labels
- `set_label_va: str = 'center'` - Vertical alignment of set labels

#### Title Style
- `title_fontsize: int = 14` - Font size for title
- `title_weight: str = 'bold'` - Font weight of title
- `title_color: str = 'black'` - Color of title
- `title_pad: float = 20.0` - Padding around title
- `title_loc: str = 'center'` - Location of title ('center', 'left', 'right')

#### Axes Settings
- `padding_ratio: float = 0.1` - Ratio of padding around plot
- `show_axis: bool = False` - Whether to show axes
- `axis_color: str = 'black'` - Color of axes if shown

#### Grid Settings
- `show_grid: bool = False` - Whether to show grid
- `grid_color: str = 'gray'` - Color of grid lines
- `grid_alpha: float = 0.3` - Transparency of grid lines (0-1)
- `grid_linestyle: str = '--'` - Style of grid lines

### Class Methods (Predefined Styles)

#### `soft()`
```python
@classmethod
def soft(cls) -> 'PlotStyle':
```
**Description**: Creates a style with soft colors and thin borders.

#### `bold()`
```python
@classmethod
def bold(cls) -> 'PlotStyle':
```
**Description**: Creates a style with vivid colors and thick borders.

#### `paper()`
```python
@classmethod
def paper(cls) -> 'PlotStyle':
```
**Description**: Creates a professional style suitable for papers.

#### `white()`
```python
@classmethod
def white(cls) -> 'PlotStyle':
```
**Description**: Creates a style with white borders and labels.

#### `clean()`
```python
@classmethod
def clean(cls) -> 'PlotStyle':
```
**Description**: Creates a clean style with white borders and black labels.

#### `dark()`
```python
@classmethod
def dark(cls) -> 'PlotStyle':
```
**Description**: Creates a dark theme style.

#### `pastel()`
```python
@classmethod
def pastel(cls) -> 'PlotStyle':
```
**Description**: Creates a style with soft white borders.

#### `vivid()`
```python
@classmethod
def vivid(cls) -> 'PlotStyle':
```
**Description**: Creates a high-contrast style.

#### `poster()`
```python
@classmethod
def poster(cls) -> 'PlotStyle':
```
**Description**: Creates a large-font presentation style.

#### `print()`
```python
@classmethod
def print(cls) -> 'PlotStyle':
```
**Description**: Creates a high-DPI print-quality style.

#### `dashed()`
```python
@classmethod
def dashed(cls) -> 'PlotStyle':
```
**Description**: Creates a style with dashed borders.

#### `dotted()`
```python
@classmethod
def dotted(cls) -> 'PlotStyle':
```
**Description**: Creates a style with dotted borders.

#### `dashdot()`
```python
@classmethod
def dashdot(cls) -> 'PlotStyle':
```
**Description**: Creates a style with dash-dot borders.

---

## overlapviz.core.baseplot.BasePlot

### Class Definition
```python
class BasePlot(ABC):
```

### Constructor
```python
def __init__(self, style: Optional[PlotStyle] = None):
```
**Description**: Initializes a BasePlot instance.
**Parameters**:
- `style`: Plotting style configuration, defaults to PlotStyle()

### Public Methods

#### `create_figure`
```python
def create_figure(self):
```
**Description**: Creates figure and axes with the configured style.

#### `calculate_limits`
```python
def calculate_limits(self, df: pd.DataFrame) -> Tuple[float, float, float, float]:
```
**Description**: Calculates axis limits with padding.
**Parameters**:
- `df`: DataFrame containing X, Y columns
**Returns**: (x_min, x_max, y_min, y_max)

#### `setup_axes`
```python
def setup_axes(self, x_lim: Tuple[float, float], y_lim: Tuple[float, float]):
```
**Description**: Sets up axes with limits, aspect ratio, grid, and visibility.
**Parameters**:
- `x_lim`: X-axis range (min, max)
- `y_lim`: Y-axis range (min, max)

#### `set_title`
```python
def set_title(self, title: str):
```
**Description**: Sets plot title with configured style.
**Parameters**:
- `title`: Title text

#### `show`
```python
def show(self):
```
**Description**: Displays the figure.

#### `save`
```python
def save(self, filepath: str, dpi: Optional[int] = None):
```
**Description**: Saves the figure to file.
**Parameters**:
- `filepath`: Save path
- `dpi`: Resolution, defaults to dpi in style

#### `close`
```python
def close(self):
```
**Description**: Closes the figure and frees resources.

#### `draw` (abstract)
```python
@abstractmethod
def draw(self, **kwargs):
```
**Description**: Abstract method to be implemented by subclasses.

---

## overlapviz.core.calculator.OverlapCalculator

### Class Definition
```python
class OverlapCalculator:
```

### Constructor
```python
def __init__(self, data: Union[Dict[str, Set], List[Set], List[Tuple[str, Set]]]):
```
**Description**: Initialize the OverlapCalculator with input data.
**Parameters**:
- `data`: Input set data in one of the supported formats:
  - Dictionary mapping set names to sets (recommended for clarity)
  - List of sets (auto-named as Set1, Set2, Set3, etc.)
  - List of tuples: (set_name, set_elements) for explicit naming

### Methods

#### `compute`
```python
def compute(self, min_size: int = 0, max_size: Optional[int] = None) -> pd.DataFrame:
```
**Description**: Compute all overlaps between sets and return as DataFrame.
**Parameters**:
- `min_size`: Minimum overlap size threshold. Only returns combinations with intersection size >= min_size. Set to 0 to include empty intersections.
- `max_size`: Maximum overlap size threshold. Only returns combinations with intersection size <= max_size
**Returns**: pd.DataFrame with columns: sets, set_names, n_sets, size, elements, exclusive_size, exclusive_elements

#### `compute_exclusive`
```python
def compute_exclusive(self) -> pd.DataFrame:
```
**Description**: Compute exclusive elements for each individual set.
**Returns**: pd.DataFrame with columns: set, total_size, exclusive_size, exclusive_elements, overlap_size

#### `get_pairwise_overlap`
```python
def get_pairwise_overlap(self) -> Dict[str, pd.DataFrame]:
```
**Description**: Generate pairwise overlap and Jaccard similarity matrices.
**Returns**: Dictionary containing two DataFrames: 'overlap_matrix' and 'jaccard_matrix'

#### `query_elements`
```python
def query_elements(self, query_sets: Optional[List[str]] = None) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
```
**Description**: Query overlap information for specific set combinations.
**Parameters**:
- `query_sets`: List of set names to query. If None (default), returns ALL possible overlap combinations (2^n - 1 total).
**Returns**: 
  - If query_sets provided: Single dictionary with overlap info
  - If query_sets is None: List of dictionaries for all combinations

#### `get_summary`
```python
def get_summary(self) -> Dict[str, Any]:
```
**Description**: Get summary statistics about the overlaps.
**Returns**: Dictionary containing summary statistics

#### `get_plot_data`
```python
def get_plot_data(self) -> pd.DataFrame:
```
**Description**: Get data formatted for plotting with Venn diagrams.
**Returns**: pd.DataFrame formatted for use with VennPlot
