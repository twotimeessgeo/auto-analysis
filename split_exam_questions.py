#!/usr/bin/env python3
"""Split a two-column exam PDF into one image per question.

The script is intentionally OCR-free. It renders each page, detects the exam
body and two-column layout, then uses the left-edge question number markers as
question starts. It works well for the Korean mock-exam layout in this folder
and similar two-column papers.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import fitz
import numpy as np
from PIL import Image, ImageDraw


@dataclass
class QuestionCrop:
    question: int
    page: int
    column: str
    source_box: tuple[int, int, int, int]
    trimmed_box: tuple[int, int, int, int]
    output: str


@dataclass
class StartMarker:
    y: int
    raw_y0: int
    raw_y1: int


def px(value: float, unit: float, minimum: int = 1) -> int:
    return max(minimum, int(round(value * unit)))


def render_page(page: fitz.Page, dpi: int) -> tuple[Image.Image, float]:
    scale = dpi / 72.0
    pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
    image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    return image, scale / 1.5


def grayscale_array(image: Image.Image) -> np.ndarray:
    return np.asarray(image.convert("L"))


def grouped_true_runs(values: Iterable[bool], max_gap: int = 0) -> list[tuple[int, int]]:
    groups: list[tuple[int, int]] = []
    start: int | None = None
    last_true: int | None = None
    gap = 0

    for idx, value in enumerate(values):
        if value:
            if start is None:
                start = idx
            last_true = idx
            gap = 0
        elif start is not None:
            gap += 1
            if gap > max_gap:
                assert last_true is not None
                groups.append((start, last_true))
                start = None
                last_true = None
                gap = 0

    if start is not None and last_true is not None:
        groups.append((start, last_true))
    return groups


def find_exam_body(gray: np.ndarray, unit: float) -> tuple[int, int]:
    dark = gray < 80
    height, width = gray.shape
    x0 = int(width * 0.08)
    x1 = int(width * 0.92)
    row_counts = dark[:, x0:x1].sum(axis=1)
    likely_lines = row_counts > int((x1 - x0) * 0.62)
    upper_limit = int(height * 0.36)
    line_runs = [
        (start, end)
        for start, end in grouped_true_runs(likely_lines[:upper_limit], max_gap=px(1, unit))
    ]

    if line_runs:
        # The actual page/body divider is normally the darkest, longest
        # horizontal rule near the top. Some questions also contain wide boxes
        # in the same vertical band, so choosing the last rule can skip the
        # first question on a page.
        body_rule = max(
            line_runs,
            key=lambda run: (int(row_counts[run[0] : run[1] + 1].max()), run[1] - run[0]),
        )
        body_top = body_rule[1] + px(9, unit)
    else:
        body_top = int(height * 0.13)

    body_bottom = int(height * 0.91)
    footer_top = find_page_number_footer_top(gray, unit)
    if footer_top is not None:
        body_bottom = min(body_bottom, footer_top - px(10, unit))
    return body_top, body_bottom


def find_page_number_footer_top(gray: np.ndarray, unit: float) -> int | None:
    """Return the top y of the small page-number box, if detected."""

    dark = gray < 100
    height, width = gray.shape
    y_offset = int(height * 0.84)
    x0 = int(width * 0.42)
    x1 = int(width * 0.58)
    row_counts = dark[y_offset : int(height * 0.98), x0:x1].sum(axis=1)
    threshold = max(px(40, unit), int((x1 - x0) * 0.22))
    runs = [
        (y_offset + start, y_offset + end)
        for start, end in grouped_true_runs(row_counts > threshold, max_gap=px(1, unit))
    ]

    pairs: list[tuple[int, int]] = []
    min_gap = px(25, unit)
    max_gap = px(145, unit)
    for idx, first in enumerate(runs):
        for second in runs[idx + 1 :]:
            gap = second[0] - first[0]
            if min_gap <= gap <= max_gap and second[0] > int(height * 0.89):
                pairs.append((first[0], second[0]))

    if not pairs:
        return None
    return max(pairs, key=lambda pair: (pair[1], pair[0]))[0]


def find_separator(gray: np.ndarray, body_top: int, body_bottom: int) -> int:
    dark = gray < 95
    height, width = gray.shape
    del height
    search_start = int(width * 0.45)
    search_end = int(width * 0.55)
    counts = dark[body_top:body_bottom, search_start:search_end].sum(axis=0)
    sep = search_start + int(np.argmax(counts))
    if counts.max() < (body_bottom - body_top) * 0.25:
        sep = width // 2
    return sep


def first_last_ink_col(
    mask: np.ndarray, x0: int, x1: int, min_pixels: int, max_gap: int
) -> tuple[int, int]:
    counts = mask[:, x0:x1].sum(axis=0)
    runs = grouped_true_runs(counts > min_pixels, max_gap=max_gap)
    if not runs:
        return x0, x1

    # Ignore detached side labels/marginal furniture by keeping the dominant
    # horizontal content run in the column.
    best = max(
        runs,
        key=lambda run: (int(counts[run[0] : run[1] + 1].sum()), run[1] - run[0]),
    )
    return x0 + int(best[0]), x0 + int(best[1])


def find_columns(
    gray: np.ndarray, body_top: int, body_bottom: int, sep_x: int, unit: float
) -> dict[str, tuple[int, int]]:
    dark = gray < 180
    _, width = gray.shape
    body = dark[body_top:body_bottom]
    min_pixels = px(4, unit)
    pad = px(10, unit)
    gap = px(18, unit)

    left_min, left_max = first_last_ink_col(
        body, int(width * 0.05), sep_x - gap, min_pixels, px(3, unit)
    )
    right_min, right_max = first_last_ink_col(
        body, sep_x + gap, int(width * 0.96), min_pixels, px(3, unit)
    )

    return {
        "left": (max(0, left_min - pad), min(sep_x - gap, left_max + pad)),
        "right": (max(sep_x + gap, right_min - pad), min(width, right_max + pad)),
    }


def find_question_starts(
    gray: np.ndarray,
    x0: int,
    x1: int,
    body_top: int,
    body_bottom: int,
    unit: float,
) -> list[StartMarker]:
    del x1
    dark = gray < 150
    band_width = px(70, unit)
    band = dark[body_top:body_bottom, x0 : x0 + band_width]
    row_counts = band.sum(axis=1)
    active_rows = row_counts > px(4, unit)
    runs = grouped_true_runs(active_rows, max_gap=px(2, unit))

    starts: list[StartMarker] = []
    # Some pages render the next question marker just a hair shorter than the
    # usual 14pt-ish marker height, especially when it starts after a large
    # blank area at the bottom of a column. Keep this tolerant enough to catch
    # those starts without admitting the smaller answer-choice circles.
    min_height = px(13, unit)
    max_height = px(30, unit)
    max_left_offset = px(14, unit)

    for rel_y0, rel_y1 in runs:
        height = rel_y1 - rel_y0 + 1
        if height < min_height or height > max_height:
            continue

        segment = band[rel_y0 : rel_y1 + 1]
        coords = np.argwhere(segment)
        if coords.size == 0:
            continue

        min_x = int(coords[:, 1].min())
        if min_x > max_left_offset:
            continue

        raw_y0 = body_top + rel_y0
        raw_y1 = body_top + rel_y1
        y = max(body_top, raw_y0 - px(8, unit))
        if starts and y - starts[-1].y < px(35, unit):
            continue
        starts.append(StartMarker(y=y, raw_y0=raw_y0, raw_y1=raw_y1))

    return starts


def trim_to_ink(image: Image.Image, unit: float) -> tuple[Image.Image, tuple[int, int, int, int]]:
    gray = grayscale_array(image)
    ink = gray < 246
    coords = np.argwhere(ink)
    if coords.size == 0:
        return image, (0, 0, image.width, image.height)

    pad = px(16, unit)
    y0 = max(0, int(coords[:, 0].min()) - pad)
    y1 = min(image.height, int(coords[:, 0].max()) + pad + 1)
    x0 = max(0, int(coords[:, 1].min()) - pad)
    x1 = min(image.width, int(coords[:, 1].max()) + pad + 1)
    return image.crop((x0, y0, x1, y1)), (x0, y0, x1, y1)


def strip_trailing_note(
    gray: np.ndarray,
    x0: int,
    x1: int,
    top: int,
    bottom: int,
    unit: float,
) -> int:
    """Drop detached final-page notes separated from the last question."""

    dark = gray < 180
    region = dark[top:bottom, x0:x1]
    row_counts = region.sum(axis=1)
    active_rows = row_counts > px(4, unit)
    runs = [
        run
        for run in grouped_true_runs(active_rows, max_gap=px(2, unit))
        if run[1] - run[0] + 1 >= px(2, unit)
    ]
    if len(runs) < 2:
        return bottom

    min_gap = px(38, unit)
    min_relative_start = int((bottom - top) * 0.62)
    cut: int | None = None
    for idx in range(len(runs) - 1):
        gap = runs[idx + 1][0] - runs[idx][1] - 1
        if gap >= min_gap and runs[idx + 1][0] >= min_relative_start:
            cut = top + runs[idx][1] + px(8, unit)

    return cut if cut is not None else bottom


def draw_debug_page(
    page_image: Image.Image,
    body_top: int,
    body_bottom: int,
    sep_x: int,
    columns: dict[str, tuple[int, int]],
    starts_by_col: dict[str, list[StartMarker]],
    first_question: int,
    output_path: Path,
) -> None:
    debug = page_image.copy()
    draw = ImageDraw.Draw(debug)
    draw.line((0, body_top, page_image.width, body_top), fill=(255, 0, 0), width=3)
    draw.line((0, body_bottom, page_image.width, body_bottom), fill=(255, 0, 0), width=3)
    draw.line((sep_x, body_top, sep_x, body_bottom), fill=(0, 160, 255), width=3)

    q = first_question
    for col_name in ("left", "right"):
        x0, x1 = columns[col_name]
        draw.rectangle((x0, body_top, x1, body_bottom), outline=(0, 180, 0), width=3)
        for marker in starts_by_col[col_name]:
            draw.line((x0, marker.y, x1, marker.y), fill=(255, 128, 0), width=3)
            draw.text((x0 + 6, marker.y + 6), f"Q{q}", fill=(255, 0, 0))
            q += 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    debug.save(output_path)


def split_pdf(
    pdf_path: Path,
    output_dir: Path,
    expected_questions: int,
    dpi: int,
    make_debug: bool,
    strip_final_notes: bool,
) -> list[QuestionCrop]:
    output_dir.mkdir(parents=True, exist_ok=True)
    debug_dir = output_dir / "_debug"
    doc = fitz.open(pdf_path)
    manifest: list[QuestionCrop] = []
    question_number = 1

    for page_index, page in enumerate(doc, start=1):
        image, unit = render_page(page, dpi)
        gray = grayscale_array(image)
        body_top, body_bottom = find_exam_body(gray, unit)
        sep_x = find_separator(gray, body_top, body_bottom)
        columns = find_columns(gray, body_top, body_bottom, sep_x, unit)
        starts_by_col = {
            col_name: find_question_starts(gray, x0, x1, body_top, body_bottom, unit)
            for col_name, (x0, x1) in columns.items()
        }

        if make_debug:
            draw_debug_page(
                image,
                body_top,
                body_bottom,
                sep_x,
                columns,
                starts_by_col,
                question_number,
                debug_dir / f"page_{page_index:02d}_debug.png",
            )

        for col_name in ("left", "right"):
            if question_number > expected_questions:
                break
            starts = starts_by_col[col_name]
            x0, x1 = columns[col_name]
            for idx, marker in enumerate(starts):
                if question_number > expected_questions:
                    break

                top = marker.y
                if question_number == expected_questions:
                    bottom = body_bottom
                elif idx + 1 < len(starts):
                    bottom = max(top + px(40, unit), starts[idx + 1].y - px(10, unit))
                else:
                    bottom = body_bottom

                if strip_final_notes and question_number == expected_questions:
                    bottom = strip_trailing_note(gray, x0, x1, top, bottom, unit)

                source_box = (x0, top, x1, bottom)
                crop = image.crop(source_box)
                trimmed, trim_box = trim_to_ink(crop, unit)
                output_path = output_dir / f"q{question_number:02d}.png"
                trimmed.save(output_path)

                manifest.append(
                    QuestionCrop(
                        question=question_number,
                        page=page_index,
                        column=col_name,
                        source_box=source_box,
                        trimmed_box=trim_box,
                        output=str(output_path),
                    )
                )
                question_number += 1

    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps([asdict(item) for item in manifest], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    if len(manifest) != expected_questions:
        raise SystemExit(
            f"Detected {len(manifest)} questions, expected {expected_questions}. "
            f"Check debug images in {debug_dir if make_debug else output_dir}."
        )

    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Automatically crop a two-column exam PDF into question images."
    )
    parser.add_argument("pdf", type=Path, help="Input PDF path")
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=Path("question_crops"),
        help="Directory for q01.png, q02.png, ...",
    )
    parser.add_argument(
        "-n",
        "--expected-questions",
        type=int,
        default=20,
        help="Expected number of questions",
    )
    parser.add_argument("--dpi", type=int, default=240, help="Render DPI")
    parser.add_argument("--no-debug", action="store_true", help="Do not save debug overlays")
    parser.add_argument(
        "--keep-final-notes",
        action="store_true",
        help="Keep detached final-page notes after the last question",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    manifest = split_pdf(
        pdf_path=args.pdf,
        output_dir=args.output_dir,
        expected_questions=args.expected_questions,
        dpi=args.dpi,
        make_debug=not args.no_debug,
        strip_final_notes=not args.keep_final_notes,
    )
    print(f"Saved {len(manifest)} question images to {args.output_dir}")
    print(f"Manifest: {args.output_dir / 'manifest.json'}")


if __name__ == "__main__":
    main()
