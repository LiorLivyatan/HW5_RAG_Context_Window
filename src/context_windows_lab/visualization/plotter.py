"""
Plotter - Building Block for Visualization Generation

This module provides the Plotter class for creating publication-quality
graphs and charts from experiment results.
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import matplotlib.pyplot as plt
    import numpy as np
    import seaborn as sns
except ImportError as e:
    raise ImportError(
        f"Required visualization library not installed: {e}. "
        "Install with: pip install matplotlib seaborn numpy"
    )

logger = logging.getLogger(__name__)


class Plotter:
    """
    Generate publication-quality visualizations from experiment results.

    This building block creates bar charts, line graphs, and other
    visualizations with proper styling and labels.

    Input Data:
        - data: Dictionary or array of data to plot
        - title: Plot title
        - labels: Axis labels and legend labels

    Output Data:
        - Path: Path to saved visualization file

    Setup Data:
        - style: Matplotlib/Seaborn style
        - dpi: Resolution (dots per inch)
        - color_palette: Color scheme
        - figsize: Figure dimensions
    """

    def __init__(
        self,
        style: str = "seaborn-v0_8-darkgrid",
        dpi: int = 300,
        color_palette: str = "deep",
        figsize: Tuple[int, int] = (10, 6),
    ):
        """
        Initialize Plotter with style settings.

        Args:
            style: Matplotlib style to use
            dpi: Dots per inch for saved figures
            dpi: Resolution for saved images
            color_palette: Seaborn color palette
            figsize: Default figure size (width, height)
        """
        self.dpi = dpi
        self.color_palette = color_palette
        self.figsize = figsize

        # Set style
        try:
            plt.style.use(style)
        except:
            logger.warning(f"Style '{style}' not available, using default")
            plt.style.use("default")

        sns.set_palette(color_palette)

    def plot_bar_chart(
        self,
        data: Dict[str, float],
        title: str,
        xlabel: str,
        ylabel: str,
        output_path: Path,
        show_values: bool = True,
    ) -> Path:
        """
        Create a bar chart.

        Args:
            data: Dictionary mapping categories to values
            title: Chart title
            xlabel: X-axis label
            ylabel: Y-axis label
            output_path: Path to save figure
            show_values: Whether to show values on top of bars

        Returns:
            Path to saved figure
        """
        fig, ax = plt.subplots(figsize=self.figsize)

        categories = list(data.keys())
        values = list(data.values())

        bars = ax.bar(categories, values)

        # Add value labels on top of bars
        if show_values:
            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2.0,
                    height,
                    f"{height:.2f}",
                    ha="center",
                    va="bottom",
                )

        ax.set_xlabel(xlabel, fontsize=12, fontweight="bold")
        ax.set_ylabel(ylabel, fontsize=12, fontweight="bold")
        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.grid(axis="y", alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_path, dpi=self.dpi, bbox_inches="tight")
        plt.close()

        logger.info(f"Bar chart saved to {output_path}")
        return output_path

    def plot_line_graph(
        self,
        x_data: List[float],
        y_data: List[float],
        title: str,
        xlabel: str,
        ylabel: str,
        output_path: Path,
        y_error: Optional[List[float]] = None,
        markers: bool = True,
    ) -> Path:
        """
        Create a line graph.

        Args:
            x_data: X-axis data points
            y_data: Y-axis data points
            title: Graph title
            xlabel: X-axis label
            ylabel: Y-axis label
            output_path: Path to save figure
            y_error: Optional error bars (standard deviation)
            markers: Whether to show markers at data points

        Returns:
            Path to saved figure
        """
        fig, ax = plt.subplots(figsize=self.figsize)

        marker_style = "o" if markers else ""

        if y_error:
            ax.errorbar(
                x_data,
                y_data,
                yerr=y_error,
                marker=marker_style,
                capsize=5,
                capthick=2,
                linewidth=2,
            )
        else:
            ax.plot(x_data, y_data, marker=marker_style, linewidth=2)

        ax.set_xlabel(xlabel, fontsize=12, fontweight="bold")
        ax.set_ylabel(ylabel, fontsize=12, fontweight="bold")
        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_path, dpi=self.dpi, bbox_inches="tight")
        plt.close()

        logger.info(f"Line graph saved to {output_path}")
        return output_path

    def plot_comparison_bars(
        self,
        data: Dict[str, Dict[str, float]],
        title: str,
        xlabel: str,
        ylabel: str,
        output_path: Path,
    ) -> Path:
        """
        Create grouped bar chart for comparing multiple series.

        Args:
            data: Nested dict {category: {series: value}}
            title: Chart title
            xlabel: X-axis label
            ylabel: Y-axis label
            output_path: Path to save figure

        Returns:
            Path to saved figure
        """
        fig, ax = plt.subplots(figsize=self.figsize)

        categories = list(data.keys())
        series_names = list(next(iter(data.values())).keys())
        n_series = len(series_names)

        x = np.arange(len(categories))
        width = 0.8 / n_series

        for i, series in enumerate(series_names):
            values = [data[cat][series] for cat in categories]
            offset = (i - n_series / 2) * width + width / 2
            ax.bar(x + offset, values, width, label=series)

        ax.set_xlabel(xlabel, fontsize=12, fontweight="bold")
        ax.set_ylabel(ylabel, fontsize=12, fontweight="bold")
        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        ax.legend()
        ax.grid(axis="y", alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_path, dpi=self.dpi, bbox_inches="tight")
        plt.close()

        logger.info(f"Comparison bar chart saved to {output_path}")
        return output_path

    def __repr__(self) -> str:
        """String representation of Plotter."""
        return f"Plotter(dpi={self.dpi}, palette='{self.color_palette}')"
