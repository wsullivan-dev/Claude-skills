"""Utilities for extracting dashboard visuals from Power BI PDF exports."""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

import fitz  # PyMuPDF

LOGGER = logging.getLogger(__name__)

TARGET_SLIDE_LABELS = [
    "(1) Summary",
    "(2) Total Co",
    "(3) Mkt. A",
    "(4) Mkt. B",
    "(5) Mkt. C",
]

MIN_IMAGE_WIDTH = 200
MIN_IMAGE_HEIGHT = 150
MIN_AREA_RATIO = 0.05
DPI = 300


@dataclass
class SlideVisuals:
    """Container for extracted visuals for a single slide."""

    pdf_name: str
    page_number: int
    slide_label: str
    image_paths: List[Path] = field(default_factory=list)


def extract_slide_visuals(pdf_path: Path, images_dir: Path) -> Dict[str, SlideVisuals]:
    """Extracts large embedded visuals for qualifying slides.

    Args:
        pdf_path: Path to the Power BI PDF export.
        images_dir: Directory where extracted images should be written.

    Returns:
        Mapping of slide labels to ``SlideVisuals`` metadata.
    """

    images_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = pdf_path.resolve()
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    doc = fitz.open(pdf_path)
    try:
        detected_pages = _detect_slide_pages(doc)
        if not detected_pages:
            LOGGER.warning(
                "No slide titles detected in %s; falling back to page index heuristic",
                pdf_path.name,
            )
            detected_pages = _fallback_slide_pages(doc)
        elif len(detected_pages) < len(TARGET_SLIDE_LABELS):
            fallback = _fallback_slide_pages(doc)
            for label, page_index in fallback.items():
                detected_pages.setdefault(label, page_index)

        visuals: Dict[str, SlideVisuals] = {}
        for label, page_index in detected_pages.items():
            page = doc.load_page(page_index)
            image_paths = _extract_images_from_page(
                doc=doc,
                page=page,
                pdf_path=pdf_path,
                page_number=page_index + 1,
                images_dir=images_dir,
            )
            visuals[label] = SlideVisuals(
                pdf_name=pdf_path.stem,
                page_number=page_index + 1,
                slide_label=label,
                image_paths=image_paths,
            )
            LOGGER.info(
                "Extracted %d visuals for %s page %d (%s)",
                len(image_paths),
                pdf_path.name,
                page_index + 1,
                label,
            )
        return visuals
    finally:
        doc.close()


def _detect_slide_pages(doc: fitz.Document) -> Dict[str, int]:
    """Detect slide pages using the textual slide headers."""

    slide_pages: Dict[str, int] = {}
    for page_index in range(doc.page_count):
        page = doc.load_page(page_index)
        label = _extract_slide_label(page)
        if label and label not in slide_pages:
            slide_pages[label] = page_index
            LOGGER.debug("Detected slide %s on page %d", label, page_index + 1)
        if len(slide_pages) == len(TARGET_SLIDE_LABELS):
            break
    return slide_pages


def _fallback_slide_pages(doc: fitz.Document) -> Dict[str, int]:
    """Fallback mapping that uses the expected slide page range (pages 9-13)."""

    slide_pages: Dict[str, int] = {}
    for offset, label in enumerate(TARGET_SLIDE_LABELS):
        page_number = 9 + offset  # 1-based
        if page_number > doc.page_count:
            break
        slide_pages[label] = page_number - 1
    return slide_pages


def _extract_slide_label(page: fitz.Page) -> Optional[str]:
    text = page.get_text("text") or ""
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line.startswith("("):
            continue
        for target in TARGET_SLIDE_LABELS:
            # use regex to allow additional trailing text (e.g., punctuation)
            pattern = rf"^{re.escape(target)}(\b|$)"
            if re.match(pattern, line, re.IGNORECASE):
                return target
    return None


def _extract_images_from_page(
    doc: fitz.Document,
    page: fitz.Page,
    pdf_path: Path,
    page_number: int,
    images_dir: Path,
) -> List[Path]:
    """Extracts qualifying images from the provided page."""

    image_infos = page.get_images(full=True)
    if not image_infos:
        return _render_full_page_visual(
            reason="No embedded images found",
            page=page,
            pdf_path=pdf_path,
            page_number=page_number,
            images_dir=images_dir,
        )

    page_area = abs(page.rect.width * page.rect.height) or 1
    extracted: List[Path] = []
    visual_index = 1
    for info in image_infos:
        xref = info[0]
        bbox = page.get_image_bbox(xref)
        width = bbox.width
        height = bbox.height
        area_ratio = (width * height) / page_area
        if width < MIN_IMAGE_WIDTH or height < MIN_IMAGE_HEIGHT:
            LOGGER.debug(
                "Skipping small image on page %d (w=%s h=%s)",
                page_number,
                width,
                height,
            )
            continue
        if area_ratio < MIN_AREA_RATIO:
            LOGGER.debug(
                "Skipping low-area image on page %d (ratio=%.3f)",
                page_number,
                area_ratio,
            )
            continue

        image_data = doc.extract_image(xref)
        if not image_data:
            continue
        image_bytes = image_data.get("image")
        if not image_bytes:
            continue

        output_name = f"{pdf_path.stem}__p{page_number}__v{visual_index}.png"
        output_path = images_dir / output_name
        with open(output_path, "wb") as f:
            f.write(image_bytes)
        extracted.append(output_path)
        visual_index += 1

    if extracted:
        return extracted

    return _render_full_page_visual(
        reason="No qualifying visuals met size heuristics",
        page=page,
        pdf_path=pdf_path,
        page_number=page_number,
        images_dir=images_dir,
    )


def _render_full_page_visual(
    reason: str,
    page: fitz.Page,
    pdf_path: Path,
    page_number: int,
    images_dir: Path,
) -> List[Path]:
    """Render the entire page when we cannot extract embedded visuals."""

    LOGGER.warning(
        "%s on %s page %d; rendering full-page fallback",
        reason,
        pdf_path.name,
        page_number,
    )
    zoom = DPI / 72  # keep output resolution consistent with DPI
    matrix = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=matrix, alpha=False)
    if pix.width == 0 or pix.height == 0:
        return []
    output_name = f"{pdf_path.stem}__p{page_number}__full.png"
    output_path = images_dir / output_name
    pix.save(str(output_path))
    return [output_path]


__all__ = ["SlideVisuals", "extract_slide_visuals"]
