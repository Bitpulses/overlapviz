# Installation Guide for overlapviz

## Prerequisites

- Python 3.8 or higher
- pip package manager

## Installation Methods

### 1. Development Installation (Recommended for development)

This installs the package in editable mode, so changes to the source code are immediately reflected:

```bash
# Navigate to the project root directory
cd d:\MyCode\Python\Overlapviz\overlapviz

# Install in development mode
pip install -e .

# Or install with development dependencies
pip install -e .[dev]
```

### 2. Regular Installation

```bash
pip install .
```

### 3. Build and Install from Source Distribution

```bash
# Build the package (using pyproject.toml)
python -m build

# Install from the built distribution
pip install dist/overlapviz-0.1.0.tar.gz
```

> **Note**: This project uses modern Python packaging with `pyproject.toml` only. No `setup.py` is required.

## Verification

After installation, you can verify it works correctly:

```bash
# Run the test script
python test_install.py
```

Or test manually in Python:

```python
import overlapviz
print(overlapviz.__version__)  # Should print 0.1.0

from overlapviz import VennPlot, PlotStyle
venn = VennPlot()
style = PlotStyle()
```

## Dependencies

The package automatically installs these runtime dependencies:
- matplotlib>=3.5.0
- numpy>=1.20.0
- pandas>=1.3.0

These are defined in the pyproject.toml file. For development, optional dependencies are available via:
- pip install -e .[dev]

which includes:
- pytest>=6.0
- pytest-cov>=2.0
- black>=21.0
- flake8>=3.9

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure you're in the correct directory and the package is properly installed
2. **Permission errors**: Try using `pip install --user` or run as administrator
3. **Dependency conflicts**: Create a virtual environment first

### Creating a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install the package
pip install -e .
```

## Development Workflow

1. Make changes to the source code
2. Run tests: `pytest`
3. Format code: `black .`
4. Check code quality: `flake8`
5. Test installation: `python test_install.py`

The editable installation (`-e .`) means you don't need to reinstall after making changes to the source code.