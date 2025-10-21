---
name: data-story
description: Transform raw data (CSV, JSON, Excel) into compelling narrative reports with visualizations. Use when users want to create data reports, analyze datasets, generate insights from data, create data visualizations, or turn numbers into stories. Creates professional reports with charts, insights, and actionable recommendations.
---

# Data Story

Transform raw data into compelling narratives with beautiful visualizations and actionable insights.

## When to Use This Skill

Use this skill when users request:
- "Analyze this data and create a report"
- "Turn this CSV into a story"
- "Create visualizations from this dataset"
- "Generate insights from my data"
- "Make a professional data report"
- "Help me understand what this data means"
- Any request involving data analysis combined with reporting or storytelling

## Workflow

### Step 1: Analyze the Data

Run the analysis script to extract insights:

```bash
python /mnt/skills/user/data-story/scripts/analyze_data.py <path_to_data_file>
```

This generates:
- Summary statistics for all numeric columns
- Correlation analysis between variables
- Trend detection in time-series data
- Outlier identification
- Missing data patterns
- Key insights and findings

The script supports CSV, JSON, and Excel files.

### Step 2: Create Visualizations

Generate charts automatically:

```bash
python /mnt/skills/user/data-story/scripts/create_charts.py <path_to_data_file> <output_directory>
```

This creates:
- Correlation heatmaps (if multiple numeric columns)
- Time series line charts (if date column exists)
- Distribution histograms (for numeric columns)
- Scatter plots (for variable relationships)

All charts are publication-ready with professional styling.

**Chart customization**: The scripts use matplotlib and seaborn. For custom visualizations, modify the scripts or create charts directly using the chart creation functions.

### Step 3: Craft the Narrative

Read the storytelling patterns reference to structure the report:

```bash
cat /mnt/skills/user/data-story/references/storytelling_patterns.md
```

Key patterns to consider:
- **Hero's Journey**: For success/transformation stories
- **Mystery**: For investigative analysis
- **Contrast**: For before/after comparisons
- **Building Blocks**: For complex multi-factor analysis

Choose the pattern that best fits the data story.

### Step 4: Apply Visualization Best Practices

Consult the visualization reference for chart selection and design:

```bash
cat /mnt/skills/user/data-story/references/visualization_best_practices.md
```

Ensure charts:
- Have clear titles and labels
- Use appropriate chart types
- Follow color accessibility guidelines
- Include meaningful annotations
- Pass the "squint test"

### Step 5: Create the Report

**Option A: HTML Report** (Recommended for detailed reports)

Use the report template:

```bash
cp /mnt/skills/user/data-story/assets/report_template.html /home/claude/report.html
```

Then replace placeholders:
- `{{REPORT_TITLE}}`: Main report title
- `{{REPORT_SUBTITLE}}`: Subtitle or tagline
- `{{REPORT_DATE}}`: Date of report
- `{{EXECUTIVE_SUMMARY}}`: One-paragraph summary
- `{{KEY_FINDINGS_LIST}}`: Bullet points as `<li>` tags
- `{{CONTENT_SECTIONS}}`: Main analysis sections
- `{{RECOMMENDATIONS_LIST}}`: Action items as `<li>` tags

The template includes:
- Executive summary section
- Multiple content sections
- Chart containers with captions
- Insight/warning/success boxes
- Statistics grid
- Recommendations section
- Professional styling with gradient headers
- Print-friendly CSS
- Mobile-responsive design

**Option B: Markdown Report**

Create a markdown artifact for simpler reports:
- Start with executive summary
- Add sections with insights
- Embed charts as images
- End with recommendations

**Option C: Interactive React Dashboard**

For interactive data exploration, create a React artifact with:
- Chart.js or Recharts for interactive visualizations
- Filters and controls
- Data tables
- Download capabilities

## Best Practices

### Data Analysis
- Always run the analysis script first to understand the data
- Look for patterns in correlations, trends, and distributions
- Identify the most surprising or actionable insights
- Consider what the audience needs to know

### Narrative Structure
- Lead with the most important insight
- Use the appropriate storytelling pattern
- Build momentum from small to big revelations
- Connect insights to actions

### Visualization
- One clear message per chart
- Add annotations for key points
- Use captions that explain "what" and "so what"
- Place charts where they support the narrative

### Writing
- Use active voice
- Quantify impact in concrete terms
- Avoid data dumping
- Match tone to audience

## Examples

### Example 1: Sales Analysis

**User**: "Analyze this sales data and tell me what's happening"

**Workflow**:
1. Run `analyze_data.py` → Find sales declined 23% in Q3
2. Run `create_charts.py` → Generate time series and correlation charts
3. Read `storytelling_patterns.md` → Use "Mystery Pattern"
4. Structure report:
   - The Puzzle: Unexpected Q3 decline
   - The Clues: Correlation with pricing change
   - The Investigation: Customer segment analysis
   - The Revelation: Price sensitivity in core segment
   - The Lesson: Pricing strategy recommendations
5. Create HTML report using template

### Example 2: Quick Insight Report

**User**: "What's interesting in this dataset?"

**Workflow**:
1. Run `analyze_data.py` → Get key statistics
2. Create 2-3 most relevant charts
3. Write concise markdown report with:
   - Top 3 insights
   - Supporting visualizations
   - One-paragraph implications

### Example 3: Executive Brief

**User**: "Create an executive summary of this data"

**Workflow**:
1. Run analysis to find top insights
2. Use "Contrast Pattern" if showing change over time
3. Create single stat-grid visualization
4. Write tight 1-page HTML report with:
   - Bold key metrics
   - 3-bullet key findings
   - 3-item action list

## Tips for Success

1. **Know your audience**: Executives want decisions, analysts want methodology, stakeholders want implications
2. **Start simple**: Begin with overview, drill into details only as needed
3. **Make it scannable**: Use headers, bullet points, and bold for key facts
4. **Quantify impact**: Turn percentages into dollar amounts or customer counts
5. **Be honest**: Acknowledge limitations and uncertainty
6. **Focus on action**: Every insight should lead somewhere

## Common Pitfalls to Avoid

- Don't show every statistic—curate insights
- Don't bury the lede—start with findings
- Don't use jargon without definition
- Don't present correlation as causation
- Don't create charts without clear purpose
- Don't skip the "so what" and "now what"

## Skill Resources Summary

**Scripts**:
- `analyze_data.py`: Extract insights from data files
- `create_charts.py`: Generate professional visualizations

**References**:
- `storytelling_patterns.md`: Narrative structure templates
- `visualization_best_practices.md`: Chart design guidelines

**Assets**:
- `report_template.html`: Professional HTML report template
