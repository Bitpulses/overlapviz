# overlapviz Documentation

Welcome to the documentation for overlapviz, a Python toolkit for professional set visualization. This package transforms complex data overlaps into intuitive Venn and UpSet plots.

## Overview

overlapviz is designed to make set visualization easy and customizable. It provides:

- **Venn diagrams** for 2-7 sets with customizable styling
- **UpSet plots** for visualizing set relationships with 7+ sets (coming soon)
- **Euler diagrams** for proportional set visualization (coming soon)
- **Flexible styling** options with predefined themes
- **Easy data integration** with pandas DataFrames and CSV files


## Quick Start

```python
from overlapviz import VennPlot, PlotStyle
import pandas as pd

# Create sample data
data = pd.DataFrame({
    'set_names': ['A', 'B', 'C', 'A_B', 'A_C', 'B_C', 'A_B_C'],
    'size': [10, 15, 8, 5, 3, 4, 2]
})

# Create and draw a Venn diagram
venn = VennPlot(PlotStyle.paper())  # Professional styling
venn.plot(data, title="My Venn Diagram")
```

## Documentation Sections

- [API Reference](API_REFERENCE.md) - Complete API documentation
- [Usage Guide](USAGE_GUIDE.md) - Practical examples and usage patterns
- [Examples](./test/test_venn.py) - Working examples of the package

## Features

### Venn Diagrams
- Support for 2-7 sets
- Automatic shape selection based on number of sets
- Customizable colors, labels, and styling
- Percentage and count labeling options
- Export to various formats (PNG, PDF, etc.)

### Styling Options
- Multiple predefined styles (bold, soft, dark, etc.)
- Customizable color schemes
- Configurable fonts, borders, and transparency
- Professional printing options

### Data Integration
- Accepts pandas DataFrames
- Supports CSV file input
- Automatic data mapping and alignment
- Flexible label formatting

## Contributing

For developers interested in contributing to overlapviz, please check out the source code structure and API documentation.

## License

This project is licensed under the GPL-3.0 license.
