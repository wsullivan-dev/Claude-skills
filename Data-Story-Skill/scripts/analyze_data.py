#!/usr/bin/env python3
"""
Data Analysis Script for Data Story Skill

Analyzes datasets and extracts key insights including:
- Summary statistics
- Trends and patterns
- Correlations
- Anomalies
- Key findings
"""

import pandas as pd
import numpy as np
import json
import sys
from pathlib import Path


def analyze_dataset(filepath):
    """
    Analyze a dataset and return structured insights.
    
    Args:
        filepath: Path to CSV, JSON, or Excel file
        
    Returns:
        Dictionary containing analysis results
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
    
    results = {
        "dataset_info": {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "missing_values": df.isnull().sum().to_dict()
        },
        "summary_stats": {},
        "insights": [],
        "correlations": {},
        "trends": []
    }
    
    # Summary statistics for numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        results["summary_stats"][col] = {
            "mean": float(df[col].mean()),
            "median": float(df[col].median()),
            "std": float(df[col].std()),
            "min": float(df[col].min()),
            "max": float(df[col].max()),
            "q1": float(df[col].quantile(0.25)),
            "q3": float(df[col].quantile(0.75))
        }
    
    # Find correlations between numeric columns
    if len(numeric_cols) > 1:
        corr_matrix = df[numeric_cols].corr()
        for i, col1 in enumerate(numeric_cols):
            for col2 in numeric_cols[i+1:]:
                corr = corr_matrix.loc[col1, col2]
                if abs(corr) > 0.5:  # Only significant correlations
                    results["correlations"][f"{col1}_vs_{col2}"] = {
                        "correlation": float(corr),
                        "strength": "strong" if abs(corr) > 0.7 else "moderate"
                    }
    
    # Identify trends in time-series data
    date_cols = df.select_dtypes(include=['datetime64']).columns
    if len(date_cols) == 0:
        # Try to parse date columns
        for col in df.columns:
            if 'date' in col.lower() or 'time' in col.lower():
                try:
                    df[col] = pd.to_datetime(df[col])
                    date_cols = [col]
                    break
                except:
                    pass
    
    if len(date_cols) > 0 and len(numeric_cols) > 0:
        date_col = date_cols[0]
        df_sorted = df.sort_values(date_col)
        for num_col in numeric_cols[:3]:  # Analyze first 3 numeric columns
            values = df_sorted[num_col].values
            if len(values) > 2:
                # Simple trend detection
                first_half_avg = np.mean(values[:len(values)//2])
                second_half_avg = np.mean(values[len(values)//2:])
                pct_change = ((second_half_avg - first_half_avg) / first_half_avg) * 100
                
                if abs(pct_change) > 10:
                    trend = "increasing" if pct_change > 0 else "decreasing"
                    results["trends"].append({
                        "column": num_col,
                        "trend": trend,
                        "percent_change": float(pct_change)
                    })
    
    # Generate key insights
    for col in numeric_cols:
        std = df[col].std()
        mean = df[col].mean()
        if std > 0:
            # Find outliers (>2 std from mean)
            outliers = df[abs(df[col] - mean) > 2 * std]
            if len(outliers) > 0:
                results["insights"].append({
                    "type": "outliers",
                    "column": col,
                    "count": len(outliers),
                    "message": f"Found {len(outliers)} potential outliers in {col}"
                })
    
    # Check for missing data patterns
    missing_counts = df.isnull().sum()
    high_missing = missing_counts[missing_counts > len(df) * 0.1]
    if len(high_missing) > 0:
        for col in high_missing.index:
            pct = (high_missing[col] / len(df)) * 100
            results["insights"].append({
                "type": "missing_data",
                "column": col,
                "percent": float(pct),
                "message": f"{col} has {pct:.1f}% missing values"
            })
    
    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_data.py <data_file>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    results = analyze_dataset(filepath)
    print(json.dumps(results, indent=2))
