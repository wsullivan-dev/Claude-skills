# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

Data Story Skill — a Claude Code custom skill that transforms raw data (CSV, JSON, Excel) into narrative reports with visualizations. Users trigger it by asking to analyze data, create reports, or generate insights.

## Commands

```bash
# Analyze data
python scripts/analyze_data.py <path_to_data_file>
```

## Key Files

- `SKILL.md` — Skill definition (triggers, workflow, output format)
- `GITHUB_SETUP.md` — Setup instructions for GitHub integration
- `scripts/` — Analysis scripts
- `references/` — Reference materials
- `examples/` — Example outputs
- `assets/` — Supporting assets

## Critical Rules

- Follow the workflow defined in `SKILL.md` exactly
- Output must include both visualizations and narrative text
- Support CSV, JSON, and Excel input formats
