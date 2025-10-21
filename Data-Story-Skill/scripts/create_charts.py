#!/usr/bin/env python3
"""
Chart Generation Script for Data Story Skill

Creates beautiful, publication-ready charts from data.
Supports: line charts, bar charts, scatter plots, heatmaps, distributions
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import sys
from pathlib import Path

# Set style for professional-looking charts
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 11


def create_time_series(df, date_col, value_cols, output_path, title=None):
    """Create a time series line chart."""
    fig, ax = plt.subplots()
    
    for col in value_cols:
        ax.plot(df[date_col], df[col], marker='o', label=col, linewidth=2)
    
    ax.set_xlabel(date_col, fontsize=12, fontweight='bold')
    ax.set_ylabel('Value', fontsize=12, fontweight='bold')
    ax.set_title(title or 'Time Series Analysis', fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='best', frameon=True, shadow=True)
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()


def create_bar_chart(df, x_col, y_col, output_path, title=None, horizontal=False):
    """Create a bar chart."""
    fig, ax = plt.subplots()
    
    if horizontal:
        ax.barh(df[x_col], df[y_col], color=sns.color_palette("husl", 1)[0])
        ax.set_xlabel(y_col, fontsize=12, fontweight='bold')
        ax.set_ylabel(x_col, fontsize=12, fontweight='bold')
    else:
        ax.bar(df[x_col], df[y_col], color=sns.color_palette("husl", 1)[0])
        ax.set_xlabel(x_col, fontsize=12, fontweight='bold')
        ax.set_ylabel(y_col, fontsize=12, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
    
    ax.set_title(title or 'Bar Chart', fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='y' if not horizontal else 'x')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()


def create_scatter_plot(df, x_col, y_col, output_path, title=None, hue_col=None):
    """Create a scatter plot."""
    fig, ax = plt.subplots()
    
    if hue_col and hue_col in df.columns:
        categories = df[hue_col].unique()
        colors = sns.color_palette("husl", len(categories))
        for i, category in enumerate(categories):
            mask = df[hue_col] == category
            ax.scatter(df[mask][x_col], df[mask][y_col], 
                      label=category, alpha=0.6, s=100, color=colors[i])
        ax.legend(loc='best', frameon=True, shadow=True)
    else:
        ax.scatter(df[x_col], df[y_col], alpha=0.6, s=100, 
                  color=sns.color_palette("husl", 1)[0])
    
    ax.set_xlabel(x_col, fontsize=12, fontweight='bold')
    ax.set_ylabel(y_col, fontsize=12, fontweight='bold')
    ax.set_title(title or 'Scatter Plot', fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()


def create_distribution(df, col, output_path, title=None):
    """Create a distribution histogram with KDE."""
    fig, ax = plt.subplots()
    
    ax.hist(df[col], bins=30, alpha=0.7, color=sns.color_palette("husl", 1)[0], 
            edgecolor='black', density=True)
    
    # Add KDE curve
    df[col].plot.kde(ax=ax, linewidth=2, color='darkblue')
    
    ax.set_xlabel(col, fontsize=12, fontweight='bold')
    ax.set_ylabel('Density', fontsize=12, fontweight='bold')
    ax.set_title(title or f'Distribution of {col}', fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()


def create_correlation_heatmap(df, numeric_cols, output_path, title=None):
    """Create a correlation heatmap."""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    corr = df[numeric_cols].corr()
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax)
    
    ax.set_title(title or 'Correlation Matrix', fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()


def auto_visualize(filepath, output_dir=None):
    """
    Automatically create relevant visualizations for a dataset.
    
    Args:
        filepath: Path to data file
        output_dir: Directory to save charts (defaults to same directory as data)
    
    Returns:
        List of created chart paths
    """
    # Load data
    file_path = Path(filepath)
    if file_path.suffix == '.csv':
        df = pd.read_csv(filepath)
    elif file_path.suffix == '.json':
        df = pd.read_json(filepath)
    elif file_path.suffix in ['.xlsx', '.xls']:
        df = pd.read_excel(filepath)
    else:
        raise ValueError(f"Unsupported file format: {file_path.suffix}")
    
    if output_dir is None:
        output_dir = file_path.parent
    else:
        output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    created_charts = []
    
    # Identify column types
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    
    # Try to parse date columns
    if len(date_cols) == 0:
        for col in df.columns:
            if 'date' in col.lower() or 'time' in col.lower():
                try:
                    df[col] = pd.to_datetime(df[col])
                    date_cols = [col]
                    break
                except:
                    pass
    
    # Create correlation heatmap if multiple numeric columns
    if len(numeric_cols) > 1:
        output_path = output_dir / "correlation_heatmap.png"
        create_correlation_heatmap(df, numeric_cols[:10], output_path)
        created_charts.append(str(output_path))
    
    # Create time series if date column exists
    if len(date_cols) > 0 and len(numeric_cols) > 0:
        date_col = date_cols[0]
        df_sorted = df.sort_values(date_col)
        output_path = output_dir / "time_series.png"
        create_time_series(df_sorted, date_col, numeric_cols[:3], output_path)
        created_charts.append(str(output_path))
    
    # Create distributions for first few numeric columns
    for i, col in enumerate(numeric_cols[:3]):
        output_path = output_dir / f"distribution_{col.replace(' ', '_')}.png"
        create_distribution(df, col, output_path)
        created_charts.append(str(output_path))
    
    # Create scatter plot for first two numeric columns
    if len(numeric_cols) >= 2:
        output_path = output_dir / "scatter_plot.png"
        create_scatter_plot(df, numeric_cols[0], numeric_cols[1], output_path)
        created_charts.append(str(output_path))
    
    return created_charts


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create_charts.py <data_file> [output_directory]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    charts = auto_visualize(filepath, output_dir)
    print(json.dumps({"created_charts": charts}, indent=2))
