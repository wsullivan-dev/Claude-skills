# Visualization Best Practices

Guidelines for creating clear, impactful data visualizations.

## Chart Selection Matrix

| Data Type | Goal | Best Chart |
|-----------|------|------------|
| Time series | Show change over time | Line chart |
| Categorical comparison | Compare values across categories | Bar chart |
| Part-to-whole | Show composition | Pie chart, stacked bar |
| Relationship | Show correlation | Scatter plot |
| Distribution | Show data spread | Histogram, box plot |
| Hierarchical | Show nested relationships | Treemap, sunburst |
| Geographic | Show spatial patterns | Choropleth map |

## Color Principles

### Color Palette Guidelines

**Sequential palettes**: Use for continuous data (light → dark)
- One hue progressing in intensity
- Example: Revenue growth over time

**Diverging palettes**: Use for data with meaningful midpoint
- Two hues meeting at neutral center
- Example: Sentiment analysis (negative ← neutral → positive)

**Categorical palettes**: Use for distinct categories
- Distinct, easily distinguishable hues
- Limit to 6-8 categories maximum

### Accessibility
- Never use color as the only way to convey information
- Ensure sufficient contrast (4.5:1 minimum)
- Avoid red-green combinations (colorblind friendly)
- Test with grayscale conversion

## Typography

### Font Guidelines
- **Title**: 14-16pt, bold
- **Axis labels**: 11-12pt, bold
- **Data labels**: 9-11pt, regular
- **Annotations**: 9-10pt, italic for emphasis

### Avoid
- All caps (harder to read)
- Vertical text (except Y-axis labels)
- Too many font styles in one chart

## Chart-Specific Guidelines

### Line Charts
✅ Do:
- Use for temporal data or ordered sequences
- Limit to 5-7 lines maximum
- Use direct labeling instead of legends when possible
- Highlight the most important line

❌ Don't:
- Use for unordered categorical data
- Cross too many lines (creates spaghetti)
- Use 3D effects

### Bar Charts
✅ Do:
- Start Y-axis at zero
- Order bars meaningfully (by value, alphabetically, or chronologically)
- Use horizontal bars for long labels
- Add data labels when precise values matter

❌ Don't:
- Use 3D effects or decorative patterns
- Truncate the axis to exaggerate differences
- Overcrowd with too many bars

### Scatter Plots
✅ Do:
- Use for showing relationships between variables
- Include trend line when correlation exists
- Add annotations for outliers
- Use transparency with many points

❌ Don't:
- Overload with too many points (>1000 without aggregation)
- Use without clear X-Y relationship
- Skip axis labels

### Pie Charts
✅ Do:
- Use only for part-to-whole relationships
- Limit to 5-7 slices maximum
- Start at 12 o'clock position
- Order slices by size

❌ Don't:
- Use when precise comparison needed (use bar chart instead)
- Create 3D pies or "exploded" slices
- Use for data that doesn't sum to 100%

## Annotation Best Practices

### Effective Annotations
- Point to specific data points or features
- Use arrows or lines to connect text to data
- Keep text concise and actionable
- Place annotations where they don't obscure data

### When to Annotate
- Outliers or anomalies
- Inflection points or trend changes
- Goal lines or benchmarks
- Key events that explain patterns

## Decluttering Techniques

### Remove
- Unnecessary grid lines
- Redundant labels
- Decorative elements
- Chart borders
- Background fills

### Simplify
- Reduce decimal places
- Round large numbers (5M instead of 5,000,000)
- Use thousand separators (5,000 not 5000)
- Minimize tick marks

### Emphasize
- Use bold for key data
- Use color strategically (1-2 colors for emphasis)
- Increase size of important elements
- Use whitespace to create focus

## Common Mistakes

1. **Dual Y-axes**: Confusing and can mislead
2. **3D charts**: Distort perception and add no value
3. **Too many decimals**: 47.3% not 47.28573%
4. **Truncated axes**: Can exaggerate differences
5. **Inconsistent scales**: Comparing charts with different scales
6. **Chart junk**: Unnecessary decoration that distracts
7. **Missing context**: No benchmarks, goals, or comparisons
8. **Poor aspect ratio**: Distorts perception of change

## Interactivity Considerations

For interactive charts (HTML/React artifacts):
- Add hover tooltips for detailed values
- Enable zoom for dense data
- Allow filtering by category
- Include download/export options
- Provide toggles for showing/hiding data series

## The Squint Test

A good visualization should pass the "squint test":
- Squint at your chart
- The main message should still be clear
- If not, simplify or refine

## Before Publishing Checklist

- [ ] Clear, descriptive title
- [ ] Labeled axes with units
- [ ] Legend or direct labels (if multiple series)
- [ ] Source citation
- [ ] Annotations for key insights
- [ ] Accessible colors
- [ ] Readable at target size
- [ ] No unnecessary elements
- [ ] One clear message
