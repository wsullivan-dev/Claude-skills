# Data Story Skill

Transform raw data into compelling narrative reports with beautiful visualizations.

![Data Story Banner](https://img.shields.io/badge/Claude-Skill-blue?style=for-the-badge&logo=anthropic)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)

## 🎯 Overview

**Data Story** is a comprehensive Claude skill that transforms raw datasets (CSV, JSON, Excel) into professional narrative reports with actionable insights and publication-ready visualizations. It combines automated data analysis, professional charting, and storytelling frameworks to help you communicate data insights effectively.

## ✨ Features

### 📊 Automated Data Analysis
- **Summary Statistics**: Mean, median, std dev, quartiles for all numeric columns
- **Correlation Analysis**: Identify relationships between variables
- **Trend Detection**: Automatic time-series pattern recognition
- **Outlier Identification**: Flag anomalies and unusual data points
- **Missing Data Patterns**: Understand data quality issues

### 📈 Professional Visualizations
- **Time Series Charts**: Track changes over time
- **Correlation Heatmaps**: Visualize variable relationships
- **Distribution Histograms**: Understand data spread
- **Scatter Plots**: Explore correlations
- **Publication-ready styling** with matplotlib and seaborn

### 📝 Storytelling Frameworks
- **The Hero's Journey**: For transformation narratives
- **The Mystery**: For investigative reports
- **The Contrast**: For before/after comparisons
- **Building Blocks**: For complex multi-factor analysis

### 🎨 Beautiful Report Templates
- Professional HTML reports with branded styling
- Executive summary sections
- Interactive statistics cards
- Chart containers with captions
- Insight/warning/success boxes
- Print-friendly CSS
- Mobile responsive design

## 🚀 Quick Start

### Installation

1. Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/data-story-skill.git
cd data-story-skill
```

2. Install required Python packages:
```bash
pip install pandas matplotlib seaborn openpyxl
```

### Usage

#### 1. Analyze Your Data
```bash
python scripts/analyze_data.py your_data.csv
```

This generates:
- Summary statistics
- Correlations
- Trends
- Outliers
- Key insights (JSON output)

#### 2. Create Visualizations
```bash
python scripts/create_charts.py your_data.csv ./output_charts
```

This creates:
- Correlation heatmaps
- Time series charts
- Distribution plots
- Scatter plots

#### 3. Build Your Report

Use the HTML template in `assets/report_template.html` or create a custom report using the analysis results and generated charts.

## 📁 Repository Structure

```
data-story-skill/
├── SKILL.md                              # Main skill documentation
├── scripts/
│   ├── analyze_data.py                   # Data analysis script
│   └── create_charts.py                  # Visualization generator
├── references/
│   ├── storytelling_patterns.md          # Narrative frameworks
│   └── visualization_best_practices.md   # Chart design guidelines
└── assets/
    └── report_template.html              # Professional report template
```

## 📖 Documentation

### Analyzing Data

The `analyze_data.py` script supports:
- **CSV files**: Standard comma-separated values
- **JSON files**: Nested or flat JSON structures
- **Excel files**: .xlsx and .xls formats

Example output:
```json
{
  "dataset_info": {
    "rows": 12,
    "columns": 4,
    "column_names": ["date", "revenue", "customers", "satisfaction"]
  },
  "summary_stats": {
    "revenue": {
      "mean": 51083.33,
      "median": 50000.0,
      "std": 6374.07
    }
  },
  "correlations": {
    "revenue_vs_customers": {
      "correlation": 0.97,
      "strength": "strong"
    }
  }
}
```

### Creating Visualizations

The `create_charts.py` script automatically detects:
- Date columns for time series
- Numeric columns for distributions
- Relationships for scatter plots
- Correlations for heatmaps

All charts use professional styling with:
- 300 DPI resolution
- Consistent color schemes
- Clear labels and titles
- Grid overlays for readability

### Storytelling Patterns

Choose the right narrative structure:

| Pattern | Best For | Structure |
|---------|----------|-----------|
| **Hero's Journey** | Success stories, transformations | Challenge → Quest → Discovery → Transformation → New Normal |
| **Mystery** | Investigations, anomalies | Puzzle → Clues → Investigation → Revelation → Lesson |
| **Contrast** | Before/after, A/B tests | Past → Shift → Present → Drivers → Outlook |
| **Building Blocks** | Complex multi-factor analysis | Foundation → Layer 1 → Layer 2 → Layer 3 → Complete Picture |

## 🎨 Customization

### Branding Your Reports

The HTML template supports easy branding:
- Update color variables in the `<style>` section
- Add your logo in the header
- Customize fonts and typography
- Adjust layout and spacing

### Extending the Analysis

Add custom analysis functions to `analyze_data.py`:
```python
def custom_analysis(df):
    # Your custom logic here
    return results
```

### Creating New Chart Types

Extend `create_charts.py` with new visualization functions:
```python
def create_custom_chart(df, output_path):
    # Your custom chart logic
    plt.savefig(output_path, dpi=300)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built for Claude Skills framework by Anthropic
- Visualization powered by matplotlib and seaborn
- Data analysis with pandas
- Designed for Predictive Analytics Partners

## 📞 Support

For questions or issues:
- Open an issue in this repository
- Check the documentation in `references/`
- Review example reports in the demo

## 🔗 Links

- [Claude Skills Documentation](https://docs.claude.com)
- [Matplotlib Documentation](https://matplotlib.org/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [Seaborn Documentation](https://seaborn.pydata.org/)

---

**Made with ❤️ for data storytellers**
