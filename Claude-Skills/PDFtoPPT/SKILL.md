# PDF to PPT Skill

This skill converts Power BI PDF exports into Monthly Business Review (MBR) PowerPoint decks. It extracts large dashboard visuals (charts and tables) from specific "Slides" pages, saves the visuals as PNGs, and places them into an MBR template.

## Folder Structure

```
Claude-Skills/
  PDFtoPPT/
    uploads/        # input Power BI PDFs
    images/         # extracted chart/table images
    outputs/        # generated PPTX files
    templates/      # store the MBR template (mbr_template.pptx)
    pdf_to_ppt.py   # main CLI entrypoint
    pdf_extractor.py
    ppt_builder.py
    requirements.txt
    SKILL.md
```

## Installation

```bash
cd Claude-Skills/PDFtoPPT
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Usage

```bash
# Process a single PDF
python pdf_to_ppt.py --input-pdf uploads/Oct-25_MBR.pdf

# Process all PDFs in uploads
python pdf_to_ppt.py
```

Use `--images-dir`, `--outputs-dir`, and `--template` flags to override the defaults if needed.

## Assumptions & Limitations

- Optimized for Power BI PDF exports whose slide titles follow `(1) Summary` through `(5) Mkt. C`.
- Detects dashboard slides primarily via title text; falls back to pages 9–13 when text is missing.
- Extracts large embedded images only; smaller UI elements (icons, slicers) are filtered out heuristically.
- Focuses on visuals, not text boxes or annotations. Additional layout tweaks may be needed for atypical reports.
