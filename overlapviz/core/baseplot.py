"""
Base class: Provides common plotting functionality, inherited by subclasses to implement specific plotting logic
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Tuple

import matplotlib.pyplot as plt
import pandas as pd
from .plotstyle import PlotStyle


class BasePlot(ABC):
    """
    Base plotting class
    
    Provides common functionality for figure creation, axis settings, saving, etc.
    """
    
    def __init__(self, style: Optional[PlotStyle] = None):
        """
        Initialize
        
        Args:
            style: Plotting style configuration, defaults to PlotStyle()
        """
        self.style = style or PlotStyle()
        self.fig: Optional[plt.Figure] = None
        self.ax: Optional[plt.Axes] = None
    
    def create_figure(self):
        """Create figure and axes"""
        self.fig, self.ax = plt.subplots(
            figsize=self.style.figsize,
            dpi=self.style.dpi,
            facecolor=self.style.facecolor,
            edgecolor=self.style.edgecolor
        )
    
    def calculate_limits(self, df: pd.DataFrame) -> Tuple[float, float, float, float]:
        """
        Calculate axis limits
        
        Args:
            df: DataFrame containing X, Y columns
            
        Returns:
            (x_min, x_max, y_min, y_max)
        """
        x_min, x_max = df['X'].min(), df['X'].max()
        y_min, y_max = df['Y'].min(), df['Y'].max()
        
        # Add padding
        x_margin = (x_max - x_min) * self.style.padding_ratio
        y_margin = (y_max - y_min) * self.style.padding_ratio
        
        return (
            x_min - x_margin,
            x_max + x_margin,
            y_min - y_margin,
            y_max + y_margin
        )
    
    def setup_axes(self, x_lim: Tuple[float, float], y_lim: Tuple[float, float]):
        """
        Set up axes
        
        Args:
            x_lim: X-axis range (min, max)
            y_lim: Y-axis range (min, max)
        """
        self.ax.set_xlim(x_lim)
        self.ax.set_ylim(y_lim)
        self.ax.set_aspect('equal')
        
        if self.style.show_axis:
            self.ax.spines['top'].set_color(self.style.axis_color)
            self.ax.spines['bottom'].set_color(self.style.axis_color)
            self.ax.spines['left'].set_color(self.style.axis_color)
            self.ax.spines['right'].set_color(self.style.axis_color)
        else:
            self.ax.axis('off')
        
        if self.style.show_grid:
            self.ax.grid(
                True,
                color=self.style.grid_color,
                alpha=self.style.grid_alpha,
                linestyle=self.style.grid_linestyle
            )
    
    def set_title(self, title: str):
        """Set title"""
        self.ax.set_title(
            title,
            fontsize=self.style.title_fontsize,
            fontweight=self.style.title_weight,
            color=self.style.title_color,
            pad=self.style.title_pad,
            loc=self.style.title_loc
        )
    
    @abstractmethod
    def draw(self, **kwargs):
        """Draw plot (to be implemented by subclasses)"""
        pass
    
    def show(self):
        """Display the figure"""
        plt.show()
    
    def save(self, filepath: str, dpi: Optional[int] = None):
        """
        Save the figure
        
        Args:
            filepath: Save path
            dpi: Resolution, defaults to dpi in style
        """
        dpi = dpi or self.style.dpi
        self.fig.savefig(filepath, dpi=dpi, bbox_inches='tight')
    
    def close(self):
        """Close the figure"""
        if self.fig:
            plt.close(self.fig)
            self.fig = None
            self.ax = None
