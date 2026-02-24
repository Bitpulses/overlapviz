"""
Plotting configuration module
Centralized management of all plotting-related configuration parameters
"""

from dataclasses import dataclass
from typing import Optional, Tuple, Dict


@dataclass
class PlotStyle:
    """Plot style configuration"""
    # Figure settings
    figsize: Tuple[float, float] = (10, 10)
    dpi: int = 100
    facecolor: str = 'white'
    edgecolor: str = 'black'
    
    # Area style
    fill_alpha: float = 0.4
    colormap: str = 'viridis'
    
    # Border style
    edge_color: str = 'black'
    edge_width: float = 2.0
    edge_style: str = '-'  # Line style: '-' solid, '--' dashed, '-.' dash-dot, ':' dotted, (0,(5,5)) custom
    edge_alpha: float = 1.0
    
    # Label style
    label_fontsize: int = 10
    label_color: str = 'black'
    label_weight: str = 'bold'
    label_alpha: float = 1.0
    label_ha: str = 'center'
    label_va: str = 'center'
    
    # Set label style
    set_label_fontsize: int = 12
    set_label_color: str = 'darkred'
    set_label_weight: str = 'bold'
    set_label_alpha: float = 1.0
    set_label_ha: str = 'center'
    set_label_va: str = 'center'
    
    # Title style
    title_fontsize: int = 14
    title_weight: str = 'bold'
    title_color: str = 'black'
    title_pad: float = 20.0
    title_loc: str = 'center'
    
    # Axes
    padding_ratio: float = 0.1
    show_axis: bool = False
    axis_color: str = 'black'
    
    # Background and grid
    show_grid: bool = False
    grid_color: str = 'gray'
    grid_alpha: float = 0.3
    grid_linestyle: str = '--'
    
    @classmethod
    def soft(cls) -> 'PlotStyle':
        """Soft - Soft colors, thin borders"""
        return cls(
            colormap='Pastel1',
            fill_alpha=0.3,
            edge_color='gray',
            edge_width=1.5,
            edge_alpha=0.8,
            label_fontsize=9,
            label_color='dimgray',
            set_label_color='gray'
        )
    
    @classmethod
    def bold(cls) -> 'PlotStyle':
        """Bold - Vivid colors, thick borders"""
        return cls(
            colormap='Set1',
            fill_alpha=0.6,
            edge_color='black',
            edge_width=3,
            label_fontsize=12,
            label_weight='bold',
            set_label_fontsize=14,
            set_label_weight='bold'
        )
    
    @classmethod
    def paper(cls) -> 'PlotStyle':
        """Paper - Professional colors, high resolution"""
        return cls(
            dpi=100,
            colormap='tab10',
            fill_alpha=0.4,
            edge_color='black',
            edge_width=1.5,
            label_fontsize=10,
            set_label_fontsize=11,
            title_fontsize=12
        )
    
    @classmethod
    def white(cls) -> 'PlotStyle':
        """White border - White borders, white labels"""
        return cls(
            colormap='Set2',
            fill_alpha=0.7,
            edge_color='white',
            edge_width=2.5,
            edge_alpha=1.0,
            label_color='white',
            label_weight='bold',
            set_label_color='black',
            set_label_weight='bold',
            title_color='black'
        )
    
    @classmethod
    def clean(cls) -> 'PlotStyle':
        """Clean - White borders, black labels"""
        return cls(
            colormap='Set3',
            fill_alpha=0.5,
            edge_color='white',
            edge_width=3.0,
            label_fontsize=11,
            label_color='black',
            set_label_fontsize=13,
            set_label_color='darkblue'
        )
    
    @classmethod
    def dark(cls) -> 'PlotStyle':
        """Dark - Dark background, white borders"""
        return cls(
            facecolor='#2e2e2e',
            colormap='Set2',
            fill_alpha=0.6,
            edge_color='white',
            edge_width=2.0,
            label_color='white',
            set_label_color='white',
            title_color='white',
            axis_color='white'
        )
    
    @classmethod
    def pastel(cls) -> 'PlotStyle':
        """Pastel - Soft white borders"""
        return cls(
            colormap='Pastel2',
            fill_alpha=0.6,
            edge_color='white',
            edge_width=2.5,
            label_fontsize=10,
            label_color='dimgray',
            set_label_fontsize=12,
            set_label_color='gray'
        )
    
    @classmethod
    def vivid(cls) -> 'PlotStyle':
        """Vivid - High contrast"""
        return cls(
            colormap='bright',
            fill_alpha=0.7,
            edge_color='black',
            edge_width=2.5,
            label_fontsize=11,
            label_weight='bold',
            set_label_fontsize=13,
            set_label_weight='bold'
        )
    
    @classmethod
    def poster(cls) -> 'PlotStyle':
        """Poster - Large font presentation"""
        return cls(
            colormap='Set1',
            fill_alpha=0.6,
            edge_color='black',
            edge_width=3.5,
            label_fontsize=14,
            label_weight='bold',
            set_label_fontsize=16,
            set_label_weight='bold',
            title_fontsize=20,
            title_weight='bold'
        )
    
    @classmethod
    def print(cls) -> 'PlotStyle':
        """Print - High DPI print quality"""
        return cls(
            dpi=100,
            colormap='tab10',
            fill_alpha=0.4,
            edge_color='black',
            edge_width=1.0,
            label_fontsize=9,
            set_label_fontsize=10,
            title_fontsize=11
        )
    
    @classmethod
    def dashed(cls) -> 'PlotStyle':
        """Dashed - Dashed border"""
        return cls(
            colormap='Set2',
            fill_alpha=0.5,
            edge_color='black',
            edge_width=2.0,
            edge_style='--',
            label_fontsize=10,
            set_label_fontsize=12
        )
    
    @classmethod
    def dotted(cls) -> 'PlotStyle':
        """Dotted - Dotted border"""
        return cls(
            colormap='Pastel1',
            fill_alpha=0.4,
            edge_color='dimgray',
            edge_width=2.5,
            edge_style=':',
            label_fontsize=10,
            set_label_fontsize=12
        )
    
    @classmethod
    def dashdot(cls) -> 'PlotStyle':
        """Dash-dot - Dash-dot border"""
        return cls(
            colormap='Set3',
            fill_alpha=0.5,
            edge_color='navy',
            edge_width=2.0,
            edge_style='-.',
            label_fontsize=10,
            set_label_fontsize=12
        )