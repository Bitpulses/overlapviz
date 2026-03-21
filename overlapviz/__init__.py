"""
OverlapViz - A Python package for drawing Venn diagrams and UpSet plots.

This package provides functionality to visualize set overlaps using:
- Venn diagrams for 2-7 sets
- UpSet plots for 7+ sets

Main classes:
- VennPlot: Create Venn diagrams for 2-7 sets
- PlotStyle: Configure plot styles
- BasePlot: Base class for all plots
"""

from .venn import VennPlot
from .euler import EulerPlot
from .upset import UpsetPlot
from .core import PlotStyle, BasePlot

__version__ = '0.1.0'
__author__ = 'Dot4diw'
__all__ = ['VennPlot', 'EulerPlot','UpsetPlot','PlotStyle', 'BasePlot']
