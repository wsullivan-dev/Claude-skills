"""Command-line interface for converting Power BI PDFs into MBR PPTX files."""
from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import Iterable, List

from pdf_extractor import extract_slide_visuals
from ppt_builder import build_mbr_ppt

DEFAULT_UPLOADS = Path("Claude-Skills/PDFtoPPT/uploads")
DEFAULT_IMAGES = Path("Claude-Skills/PDFtoPPT/images")
DEFAULT_OUTPUTS = Path("Claude-Skills/PDFtoPPT/outputs")
DEFAULT_TEMPLATE = Path("Claude-Skills/PDFtoPPT/templates/mbr_template.pptx")


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
LOGGER = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert Power BI PDFs to PPTX")
    parser.add_argument(
        "--input-pdf",
        type=Path,
        help="Path to a single PDF to process. If omitted, all PDFs in uploads are processed.",
    )
    parser.add_argument(
        "--uploads-dir",
        type=Path,
        default=DEFAULT_UPLOADS,
        help="Directory containing PDF uploads.",
    )
    parser.add_argument(
        "--images-dir",
        type=Path,
        default=DEFAULT_IMAGES,
        help="Directory to store extracted chart images.",
    )
    parser.add_argument(
        "--outputs-dir",
        type=Path,
        default=DEFAULT_OUTPUTS,
        help="Directory for generated PPTX files.",
    )
    parser.add_argument(
        "--template",
        type=Path,
        default=DEFAULT_TEMPLATE,
        help="Path to the Monthly Business Review PPTX template.",
    )
    return parser.parse_args()


def iter_pdfs(args: argparse.Namespace) -> Iterable[Path]:
    if args.input_pdf:
        yield args.input_pdf
        return
    uploads_dir = args.uploads_dir
    if not uploads_dir.exists():
        raise FileNotFoundError(f"Uploads directory not found: {uploads_dir}")
    for pdf_path in sorted(uploads_dir.glob("*.pdf")):
        yield pdf_path


def process_pdf(pdf_path: Path, images_dir: Path, outputs_dir: Path, template: Path) -> None:
    LOGGER.info("Processing %s", pdf_path)
    slide_visuals = extract_slide_visuals(pdf_path, images_dir)
    if not slide_visuals:
        LOGGER.warning("No qualifying slides found in %s", pdf_path)
    output_name = f"{pdf_path.stem}_MBR.pptx"
    output_path = outputs_dir / output_name
    build_mbr_ppt(slide_visuals, template, output_path)
    LOGGER.info("Finished %s", pdf_path)


def main() -> None:
    args = parse_args()
    args.images_dir.mkdir(parents=True, exist_ok=True)
    args.outputs_dir.mkdir(parents=True, exist_ok=True)

    pdfs = list(iter_pdfs(args))
    if not pdfs:
        LOGGER.warning("No PDFs found to process")
        return

    for pdf_path in pdfs:
        process_pdf(pdf_path, args.images_dir, args.outputs_dir, args.template)


if __name__ == "__main__":
    main()
