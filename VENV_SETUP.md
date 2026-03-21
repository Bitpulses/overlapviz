# Virtual Environment Setup with uv

This document explains how to set up and use a virtual environment for the overlapviz package with Python 3.13.2.

## Creating the Virtual Environment

```bash
# Create a virtual environment with Python 3.12 or 13/14
uv venv --python 3.13.2 .venv
```

## Installing overlapviz in the Virtual Environment

```bash
# Install the package in editable mode with all dependencies
uv pip install -e . --python .venv\Scripts\python.exe --refresh
```

## Activating the Virtual Environment

On Windows:
```bash
.venv\Scripts\activate
```

On macOS/Linux:
```bash
source .venv/bin/activate
```

## Using the Package

Once activated, you can use the package:

```python
import overlapviz
from overlapviz import VennPlot, PlotStyle

print(f"overlapviz version: {overlapviz.__version__}")
print(f"Python version: {__import__('sys').version}")

# Create instances
venn = VennPlot()
style = PlotStyle()
```

## Deactivating the Virtual Environment

```bash
deactivate
```

## Alternative: Direct Command Execution

You can run commands in the virtual environment without activating it:

```bash
# Run Python scripts directly in the virtual environment
uv run --python .venv\Scripts\python.exe python your_script.py

# Run tests directly in the virtual environment
uv run --python .venv\Scripts\python.exe python test_install.py
```

## Adding Development Dependencies

If you need development tools:

```bash
# Install with development dependencies
uv pip install -e .[dev] --python .venv\Scripts\python.exe --refresh
```

## Notes

- The virtual environment is named `.venv` (hidden directory convention) with Python 3.13.2
- The environment contains Python 3.13.2 specifically as required by the package
- All dependencies are automatically resolved and installed by uv
- The `-e` flag installs the package in editable mode, so changes to the source code are immediately available
