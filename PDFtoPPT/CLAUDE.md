# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

PDF to PPT Skill — converts Power BI PDF exports into Monthly Business Review (MBR) PowerPoint decks. Extracts dashboard visuals (charts, tables) from specific slides, saves as PNGs, and places them into an MBR template.

## Commands

```bash
# Setup
cd Claude-skills/PDFtoPPT
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Process a single PDF
python pdf_to_ppt.py --input-pdf uploads/<file>.pdf

# Process all PDFs in uploads/
python pdf_to_ppt.py
```

## Key Files

- `SKILL.md` — Skill overview and usage
- `pdf_to_ppt.py` — Main CLI entrypoint
- `pdf_extractor.py` — PDF visual extraction logic
- `ppt_builder.py` — PowerPoint deck assembly
- `uploads/` — Input PDFs
- `images/` — Extracted chart/table images
- `outputs/` — Generated PPTX files
- `templates/` — MBR template (mbr_template.pptx)

## Critical Rules

- Optimized for Power BI PDF exports with slides titled `(1) Summary` through `(5) Mkt. C`
- Falls back to pages 9–13 when title text detection fails
- Extracts large embedded images only; small UI elements are filtered out
- Template must exist at `templates/mbr_template.pptx`
