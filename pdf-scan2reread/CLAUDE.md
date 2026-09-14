# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository scope

This repository is a documentation-driven Claude skill for converting scanned or image-only PDFs into searchable, selectable, and copyable PDFs while preserving the source page appearance. There is no executable implementation, package manifest, build system, or automated test suite in this repository.

The primary behavior is defined in `SKILL.md`; `README.md` describes the user-facing purpose and invocation; `references/implementation-notes.md` contains backend, coordinate, font, fallback, validation, and reporting details.

## Common commands

There is no build, lint, test, or development server command. Validate generated PDFs with tools available on the host:

```bash
pdfinfo output.pdf
pdftotext -f 1 -l 3 output.pdf -
qpdf --check output.pdf                 # when qpdf is installed
pdftoppm -f 1 -l 3 -png -r 150 output.pdf out/page
```

For a layout-preserving conversion, also compare input and output page counts, page boxes, rotations, and same-DPI renders. `pdftotext` producing text is necessary but not sufficient: test selection/copy behavior and inspect representative rendered pages.

## Architecture and workflow

The skill is a procedural pipeline rather than an application:

1. **Inspect the source PDF** using `pdfinfo`, `pdftotext`, Poppler utilities, PyMuPDF, or pypdf. Record page count, page boxes, rotation, crop, metadata, encryption, image resolution, and existing text layers.
2. **Classify representative pages** including cover/title, contents, body, chapter opening, multi-column, table/footnote, image-heavy, vertical-text, and poor-quality pages when present. Identify reading direction, regions, repeated headers/footers, and page-number offsets.
3. **Process a sample first** spanning the page classes. Calibrate render DPI, rotation, crop, coordinate scaling, baseline placement, font size, and reading order before batch processing.
4. **Run coordinate-aware OCR** with an engine that supplies line/word boxes and confidence. Vision is preferred on macOS for suitable Chinese scans; PaddleOCR is the portable Chinese option; Tesseract is a fallback for clean pages. Preserve engine settings and raw OCR results.
5. **Normalize layout coordinates** from the OCR/render coordinate system into PDF coordinates, accounting for top-left versus bottom-left origins, page rotation, crop/media boxes, and render scale. Calibrate against at least three landmarks on a sample page.
6. **Construct the output PDF** by retaining the original page rendering as the visual background and adding a transparent, Unicode-capable OCR text layer aligned to recognized boxes. The `text-reflow` path is explicit only and may change typography, columns, pagination, and page geometry.
7. **Handle uncertain content conservatively.** Retain the original image for difficult or ambiguous regions and report image-only, provisional, or low-confidence areas rather than inventing aligned text.
8. **Validate and report** page geometry, background fidelity, text extraction, selection/copy behavior, glyph coverage, reading order, clipping/occlusion, and residual OCR risks. Include the OCR engine/settings, coordinate strategy, sample scope, fallback treatment, and validation results in the output report.

## Important invariants

- `layout-preserving` is the default and must remain page-for-page visually faithful; do not replace it with flowing OCR text.
- Keep source page boxes and rotations. Do not assume A4, letter, portrait orientation, or a default PDF coordinate system.
- For a rendered image mapped to a PDF page, first use `x_pt = x_px * W_pt / W_px` and `y_pt = H_pt - y_px * H_pt / H_px`, then apply rotation and CropBox/MediaBox relationships.
- Detect columns and separate regions before sorting OCR text; do not globally sort a multi-column page.
- Use an embedded Unicode font with a valid `ToUnicode` mapping so Chinese and other target scripts remain searchable and copyable.
- Never cover the scan with white rectangles or visibly redraw text in layout-preserving mode.
- Remove headers, footers, or page numbers only from the text layer and only when their repeated geometry makes the classification reliable; never remove them from the visual background.
- Low OCR confidence is a review signal, not permission to guess. Preserve difficult pages/regions as image-backed and list them in the report.
- Do not claim completion until the completion gate in `SKILL.md` is satisfied, including geometry, extraction, selection/copy, render, and available PDF integrity checks.

## Output naming and reporting

Use `<source>_可搜索版_版面保持.pdf` for the default mode and `<source>_文字重排版.pdf` for explicit reflow mode. Reports should distinguish visual fidelity from OCR accuracy and state known pages or regions requiring proofreading.
