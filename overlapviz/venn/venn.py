"""
Venn diagram plotting class
version v 0.01

"""

import pickle
from pathlib import Path
from typing import Dict, Optional, Callable, Union, List, Tuple

import pandas as pd

import matplotlib.cm as cm
from matplotlib.patches import Polygon
from matplotlib.colors import to_rgba

from ..core.baseplot import BasePlot
from ..core.plotstyle import PlotStyle
from ..core.calculator import OverlapCalculator



class VennPlot(BasePlot):
    """
        venn = VennPlot()
        venn.draw(data, title="My Venn")
        venn.show()
    """

    def __init__(self, style: Optional[PlotStyle] = None):
        """
        Args:
            style: Plotting style, defaults to PlotStyle()
        """
        super().__init__(style)

        # Data attributes
        self.df_edges: Optional[pd.DataFrame] = None
        self.df_set_labels: Optional[pd.DataFrame] = None
        self.df_region_labels: Optional[pd.DataFrame] = None

        # Custom options
        self.custom_colors: Optional[Dict[str, str]] = None
        self.label_formatter: Optional[Callable] = None
        self.custom_set_labels: Optional[List[str]] = None

    def _load_geometric_data(self, shape_key: str = 'shape403'):
        """
        Load geometric data (fixed to use geometric_data_v3.pkl in the current directory)

        Args:
            shape_key: Data key name, defaults to 'shape403' (4 sets)
                      Options: 'shape201'(2 sets), 'shape301'(3 sets), 'shape403'(4 sets), 'shape501'(5 sets)
        """
        # Get current file directory and load geometric_data_v3.pkl
        current_dir = Path(__file__).parent
        filepath = current_dir / 'geometric_data_v3.pkl'

        with open(filepath, 'rb') as f:
            data = pickle.load(f)

        shape_data = data[shape_key]
        self.df_edges = shape_data['set_edge']
        self.df_set_labels = shape_data['set_label']
        self.df_region_labels = shape_data['region_label']

    def _load_overlap_data(self, overlapdata: Union[pd.DataFrame, str, OverlapCalculator]):
        """
        Load overlap data

        Args:
            overlapdata: Data source, can be:
                     - pd.DataFrame: Overlap data DataFrame (e.g., output from calc.get_plot_data())
                     - str: CSV file path
                     - OverlapCalculator: OverlapCalculator object
        """
        if isinstance(overlapdata, pd.DataFrame):
            # Directly pass DataFrame
            overlap_data = overlapdata.copy()
        elif isinstance(overlapdata, str):
            # Read from CSV file
            overlap_data = pd.read_csv(overlapdata)
        elif hasattr(overlapdata, 'compute') and hasattr(overlapdata, 'sets_names'):
            # Handle OverlapCalculator object
            # Use get_plot_data() to get exclusive elements for correct Venn diagram plotting
            overlap_data = overlapdata.get_plot_data()
            # Update df_set_labels with custom set names if available
            if hasattr(overlapdata, 'sets_names') and len(overlapdata.sets_names) > 0:
                # Create a mapping from original set labels to custom set names
                # Assuming the order of sets in overlapdata.sets_names matches the order in df_set_labels
                if self.df_set_labels is not None and len(self.df_set_labels) == len(overlapdata.sets_names):
                    # Create a copy to avoid modifying the original
                    self.df_set_labels = self.df_set_labels.copy()
                    
                    # Update the 'id' column with custom set names
                    self.df_set_labels['id'] = overlapdata.sets_names
        else:
            raise TypeError("overlapdata must be pd.DataFrame, str (CSV path), or OverlapCalculator object")

        # Replace ' & ' in set_names with '_' to match id in geometric data
        overlap_data['set_names'] = overlap_data['set_names'].str.replace(' & ', '_')

        # Get set name mapping from geometric data
        geo_ids = self.df_region_labels['id'].unique()
        overlap_ids = overlap_data['set_names'].unique()

        # Check if mapping is needed (if set names are different)
        if not any(oid in geo_ids for oid in overlap_ids):
            # Need to establish mapping: get single set names from geometric data
            geo_single_sets = set()
            for gid in geo_ids:
                if '_' not in str(gid):
                    geo_single_sets.add(str(gid))

            # Get single set names from overlap_data
            overlap_single_sets = set()
            for oid in overlap_ids:
                parts = str(oid).split('_')
                overlap_single_sets.update(parts)
            overlap_single_sets = sorted(list(overlap_single_sets))
            geo_single_sets = sorted(list(geo_single_sets))

            # Build mapping dictionary
            if len(overlap_single_sets) == len(geo_single_sets):
                mapping = dict(zip(overlap_single_sets, geo_single_sets))

                # Apply mapping to set_names
                def map_name(name):
                    parts = str(name).split('_')
                    mapped_parts = [mapping.get(p, p) for p in parts]
                    return '_'.join(mapped_parts)

                overlap_data['set_names'] = overlap_data['set_names'].apply(map_name)
        
        
        self.df_region_labels = pd.merge(
            self.df_region_labels,
            overlap_data,
            left_on='id',
            right_on='set_names',
            how='left'
        )

    @staticmethod
    def get_shapes(n_sets: int) -> List[str]:
        """
        Get all available shape IDs for the specified number of sets

        Args:
            n_sets: Number of sets (2-5)

        Returns:
            List of available shape IDs

        Example:
            >>> VennPlot.get_shapes(4)
            ['shape403', 'shape404']
        """
        # Get current file directory
        current_dir = Path(__file__).parent
        filepath = current_dir / 'geometric_data_v3.pkl'

        if not filepath.exists():
            return []

        with open(filepath, 'rb') as f:
            data = pickle.load(f)

        # Filter shapes for the specified number of sets
        shapes = []
        for shape_key, shape_data in data.items():
            if isinstance(shape_data, dict) and 'nsets' in shape_data:
                if int(shape_data['nsets']) == n_sets:
                    shapes.append(shape_key)

        return sorted(shapes)  # Return sorted list of available shape IDs

    def set_custom_colors(self, colors: Dict[str, str]):
        """
        Args:
            colors: {region_id: color} mapping
        """
        self.custom_colors = colors

    def set_label_formatter(self, formatter: Callable):
        """
        Args:
            formatter: Formatting function func(value) -> str
        """
        self.label_formatter = formatter

    def _get_colors(self):
        """Generate color mapping for regions
        
        Returns:
            Dict mapping region IDs to colors
        """
        unique_ids = self.df_edges['id'].unique()
        cmap = cm.get_cmap(self.style.colormap)
        n = len(unique_ids)

        colors = {}
        for i, region_id in enumerate(unique_ids):
            if self.custom_colors and region_id in self.custom_colors:
                # Use custom color if specified
                colors[region_id] = self.custom_colors[region_id]
            else:
                # Generate color from colormap
                colors[region_id] = cmap(i / max(n - 1, 1))

        return colors

    def _draw_regions(self):
        """Draw filled regions with colors
        
        Each region is filled with its corresponding color based on the colormap
        or custom color settings
        """
        colors = self._get_colors()

        for region_id, group in self.df_edges.groupby('id'):
            vertices = group[['X', 'Y']].values
            color = colors[region_id]

            # Create filled polygon for each region
            poly = Polygon(
                vertices,
                closed=True,
                facecolor=to_rgba(color, self.style.fill_alpha),  # Apply transparency
                edgecolor='none',
                zorder=1
            )
            self.ax.add_patch(poly)

    def _draw_borders(self):
        """Draw border lines around each region
        
        Borders are drawn with consistent styling defined in plot style
        """
        for region_id, group in self.df_edges.groupby('id'):
            self.ax.plot(
                group['X'],
                group['Y'],
                color=self.style.edge_color,
                linewidth=self.style.edge_width,
                linestyle=self.style.edge_style,
                alpha=self.style.edge_alpha,
                zorder=2  # Draw on top of filled regions
            )

    def _draw_region_labels(self):
        """Draw labels for each region showing the size/count
        
        Labels are positioned at the center coordinates of each region
        and formatted according to the specified formatter
        """
        if 'size' not in self.df_region_labels.columns:
            return

        for _, row in self.df_region_labels.iterrows():
            if pd.notna(row['size']):
                # Format text based on label formatter
                if self.label_formatter:
                    text = self.label_formatter(row['size'])
                else:
                    text = str(int(row['size']))

                # Add text label at region center
                self.ax.text(
                    row['X'],
                    row['Y'],
                    text,
                    fontsize=self.style.label_fontsize,
                    color=self.style.label_color,
                    fontweight=self.style.label_weight,
                    alpha=self.style.label_alpha,
                    ha=self.style.label_ha,
                    va=self.style.label_va
                )

    def _draw_set_labels(self):
        """Draw labels for each set (A, B, C, etc.)
        
        Set labels are positioned at specified coordinates to identify
        each individual set in the Venn diagram
        """
        for i, (_, row) in enumerate(self.df_set_labels.iterrows()):
            # Use custom label if provided and index is within bounds
            if self.custom_set_labels and i < len(self.custom_set_labels):
                label = self.custom_set_labels[i]
            else:
                label = str(row['id'])
                
            self.ax.text(
                row['X'],
                row['Y'],
                label,
                fontsize=self.style.set_label_fontsize,
                color=self.style.set_label_color,
                fontweight=self.style.set_label_weight,
                alpha=self.style.set_label_alpha,
                ha=self.style.set_label_ha,
                va=self.style.set_label_va
            )

    def _get_n_sets_from_data(self, overlapdata: Union[pd.DataFrame, str, 'OverlapCalculator']) -> int:
        """
        Calculate the number of sets from overlapdata

        Args:
            overlapdata: Data source

        Returns:
            Number of sets

        Raises:
            ValueError: When unable to calculate number of sets from data
        """
        if isinstance(overlapdata, pd.DataFrame):
            overlap_data = overlapdata.copy()
        elif isinstance(overlapdata, str):
            overlap_data = pd.read_csv(overlapdata)
        elif hasattr(overlapdata, 'sets_names'):
            return len(overlapdata.sets_names)
        else:
            raise ValueError("Unrecognized data type, unable to calculate number of sets")

        if 'set_names' in overlap_data.columns:
            all_sets = set()
            for name in overlap_data['set_names']:
                if pd.notna(name):
                    name_str = str(name).replace(' & ', '_')
                    parts = name_str.split('_')
                    all_sets.update(parts)
            if all_sets:
                return len(all_sets)

        raise ValueError("Unable to calculate number of sets from data, please check data format or specify shape_key manually")

    def draw(self,
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
             figsize: Optional[Tuple[float, float]] = None):
        """
        Draw Venn diagram

        Args:
            overlapdata: Data source, can be:
                     - pd.DataFrame: Overlap data DataFrame (e.g., output from calc.get_plot_data())
                     - str: CSV file path
            shape_key: Geometric data key name, defaults to None (automatically calculates number of sets from data and selects first available shape)
                      Options: 'shape201'(2 sets), 'shape301'(3 sets), 'shape403'(4 sets), 'shape501'(5 sets), etc.
            title: Title
            show_region_labels: Whether to show region labels
            show_set_labels: Whether to show set labels
            label_formatter: Label format, options 'count'(value), 'percentage', 'all'(both)
            custom_set_labels: Custom set labels list, defaults to None (use default labels)
            custom_colors: Custom colors dict, e.g., {'A': '#FF0000', 'B': '#00FF00'}
            palette: Color palette name, auto-generates colors for sets. 
                    Options: 'viridis', 'Set1', 'Set2', 'Set3', 'tab10', 'Pastel1', 'Pastel2', etc.
            figsize: Figure size (width, height) in inches. If None, uses style.figsize
        """

        
        # If shape_key is not specified, automatically calculate number of sets and select first available shape
        if shape_key is None:
            n_sets = self._get_n_sets_from_data(overlapdata)
            available_shapes = self.get_shapes(n_sets)
            if not available_shapes:
                raise ValueError(f"No available shapes: Could not find available shape for {n_sets} sets")
            shape_key = available_shapes[0]
        
        # Load geometric data and overlap data
        self._load_geometric_data(shape_key)
        self._load_overlap_data(overlapdata)

        # Set custom set labels if provided
        self.custom_set_labels = custom_set_labels
        
        # Handle custom colors and palette
        if custom_colors is not None:
            self.custom_colors = custom_colors
        elif palette is not None:
            # Generate colors from palette for each set
            unique_ids = self.df_edges['id'].unique()
            n = len(unique_ids)
            cmap = cm.get_cmap(palette)
            self.custom_colors = {}
            for i, region_id in enumerate(unique_ids):
                self.custom_colors[region_id] = cmap(i / max(n - 1, 1))
        
        # Calculate total for percentage calculations
        total_size = self.df_region_labels['size'].sum() if 'size' in self.df_region_labels.columns else 0
        
        # Set label formatting function (only if not set via set_label_formatter)
        if self.label_formatter is None:
            if label_formatter == 'count':
                # Show count values only
                self.label_formatter = lambda x: str(int(x))
            elif label_formatter == 'percentage':
                # Show percentages only
                self.label_formatter = lambda x: f"{x/total_size*100:.1f}%" if total_size > 0 else "0%"
            elif label_formatter == 'all':
                # Show both count and percentage
                self.label_formatter = lambda x: f"{int(x)}\n({x/total_size*100:.1f}%)" if total_size > 0 else f"{int(x)}\n(0%)"

        # Create figure and setup axes
        self.create_figure(figsize)

        # Draw diagram layers in order: regions first, then borders
        if show_regions_border:
            self._draw_regions()

        if show_set_border:
            self._draw_borders()

        # Add labels if requested
        if show_region_labels:
            self._draw_region_labels()

        if show_set_labels:
            self._draw_set_labels()

        # Configure axes limits and appearance
        x_min, x_max, y_min, y_max = self.calculate_limits(self.df_edges)
        self.setup_axes((x_min, x_max), (y_min, y_max))

        # Add title if specified
        if title:
            self.set_title(title)

    def plot(self, overlapdata: Union[pd.DataFrame, str],
             shape_key: Optional[str] = None,
             title: str = "Venn Diagram",
             label_formatter: str = 'count',
             custom_set_labels: Optional[List[str]] = None,
             custom_colors: Optional[Dict[str, str]] = None,
             palette: Optional[str] = None,
             figsize: Optional[Tuple[float, float]] = None,
             **kwargs):
        """
        Draw and display the Venn diagram
        
        This is a convenience method that calls draw() and then show()

        Args:
            overlapdata: Data source (DataFrame or CSV path)
            shape_key: Geometric data key name, defaults to None (auto-select)
            title: Title
            label_formatter: Label format, options 'count', 'percentage', 'all'
            custom_set_labels: Custom set labels list, defaults to None (use default labels)
            custom_colors: Custom colors dict, e.g., {'A': '#FF0000', 'B': '#00FF00'}
            palette: Color palette name, auto-generates colors for sets
            figsize: Figure size (width, height) in inches. If None, uses style.figsize
            **kwargs: Additional parameters passed to draw
        """
        self.draw(overlapdata=overlapdata, shape_key=shape_key, title=title,
                  label_formatter=label_formatter, custom_set_labels=custom_set_labels,
                  custom_colors=custom_colors, palette=palette, figsize=figsize, **kwargs)
        self.show()

    def get_statistics(self) -> Dict:
        """Get statistics about the Venn diagram
        
        Returns:
            Dictionary containing region count, set count, and size statistics
        """
        stats = {
            'n_regions': len(self.df_edges['id'].unique()),  # Number of distinct regions
            'n_sets': len(self.df_set_labels)  # Number of sets
        }

        # Add size statistics if available
        if 'size' in self.df_region_labels.columns:
            sizes = self.df_region_labels['size'].dropna()
            stats.update({
                'total_size': sizes.sum(),
                'mean_size': sizes.mean(),
                'max_size': sizes.max(),
                'min_size': sizes.min()
            })

        return stats
