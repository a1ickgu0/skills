---
name: pdf-scan2reread
description: Convert scanned or image-only PDFs into searchable/selectable PDFs while preserving the original page geometry, typography, columns, images, headers, footers, and pagination as closely as possible. Use when the user needs a layout-faithful text PDF rather than an image-only PDF, EPUB, or plain OCR text.
---

# PDF Scan To Re-readable PDF

## Purpose

Turn a scanned PDF into a PDF whose text can be searched, selected, copied, and indexed without sacrificing the visual arrangement of the source. Unless the user explicitly specifies another destination, place the generated document and its processing report in the same directory as the input PDF. The default deliverable is a page-for-page facsimile: keep the rendered scan as the visual background and add a coordinate-aligned OCR text layer. Do not describe a flowing re-typeset PDF as layout-preserving.

## Modes

### `layout-preserving` (default)

Preserve the source page size, rotation, crop, margins, columns, line breaks, page breaks, illustrations, tables, headers, footers, and page numbers. Render each source page as the background and add an invisible, selectable OCR text layer at the recognized coordinates. This is the reliable mode for books and documents where visual fidelity matters.

If the source contains an existing usable text layer, retain it when it is aligned and readable; otherwise replace or supplement it after checking for duplicate or conflicting layers.

### `text-reflow` (explicit only)

Create a text-first PDF using OCR text and reconstructed paragraphs. Use only when the user explicitly accepts changes to the original layout. State clearly that typography, columns, pagination, tables, and page geometry may differ. Never select this mode merely because it is easier to generate.

## Workflow

1. **Inspect the source.** Record filename, page count, page sizes, rotation, crop boxes, metadata, bookmarks, encryption, image resolution, and whether a text layer is present. Use `pdfinfo`, `pdftotext`, Poppler, PyMuPDF, or pypdf as available. Treat a page as a scan when extracted text is empty or obviously incomplete.
2. **Classify representative pages.** Render at least the cover/title page, contents page, ordinary body page, chapter opening, multi-column page, table/footnote page, image-heavy page, vertical-text page when present, and a low-quality or skewed page. Identify reading direction, body bounds, repeated headers/footers, printed page-number offset, and pages that must remain image-backed.
3. **Build a sample first.** Process a small sample spanning the classes above. Compare source and output renders at the same page dimensions. Correct DPI, rotation, crop, coordinate scaling, baseline placement, font size, and column ordering before processing the whole document.
4. **Run OCR with coordinates.** Prefer an engine that returns line and word/character boxes and confidence. On macOS prefer Vision with accurate recognition and `zh-Hans`/`zh-Hant`/`en-US` as appropriate. Use PaddleOCR for portable Chinese OCR; use Tesseract as a fallback for clean pages. Preserve the raw OCR result and engine settings for reproducibility.
5. **Recover page layout.** Normalize OCR coordinates to the PDF coordinate system (including the bottom-left PDF origin, page rotation, crop box, and render scale). Sort by reading order within detected regions, not globally when the page has columns. Group words into lines using vertical overlap and baseline proximity. Estimate font size from line height, preserve spaces/punctuation, and retain line breaks where they are visible in the source.
6. **Create the PDF.** In `layout-preserving`, place the source raster or original page rendering unchanged, then add an invisible text layer whose glyph positions follow the OCR boxes. Use an embedded Unicode-capable font or a verified fallback with a correct ToUnicode mapping. Keep text transparent or otherwise non-obscuring; never paint a white rectangle over source content unless the user explicitly requests a clean re-typeset page. In `text-reflow`, reconstruct blocks and paragraphs separately and label the output as reflowed.
7. **Handle difficult content conservatively.** Keep the original image for covers, illustrations, diagrams, formulas, tables, unusual fonts, vertical writing, overlapping text, severe skew, low-confidence OCR, and uncertain reading order. Add OCR for search where it is safe, but do not invent a visually aligned text layer for content that cannot be reliably localized. Report pages and regions that remain image-only or provisional.
8. **Clean only with evidence.** Remove repeated running headers, marginal titles, and isolated page numbers from the text layer only when they are confidently identified; do not remove them from the visual background. Do not silently correct names, numbers, quotations, or terminology. Use a supplied reliable text source for proofreading only after checking edition and page alignment.
9. **Validate before delivery.** Confirm output opens, page count matches, every page retains source dimensions and rotation, the first page remains the first page, text extraction returns expected language, selected text is in sensible reading order, and the background render is visually unchanged. Run `qpdf --check` when available, `pdfinfo`, `pdftotext`, and same-DPI page renders. Check representative pages for text-layer drift, duplicate text, missing glyphs, clipping, hidden text that cannot be selected, and accidental occlusion.

## Coordinate and layout rules

- Keep all page boxes in the source coordinate space; explicitly document any MediaBox/CropBox conversion.
- Apply rotation before comparing coordinates; do not assume portrait orientation.
- For a rendered image of width `W_px` and height `H_px` mapped to a PDF page of width `W_pt` and height `H_pt`, map `x_pt = x_px * W_pt / W_px` and `y_pt = H_pt - y_px * H_pt / H_px` before accounting for page rotation.
- Calibrate against at least three known points on the sample page. A global offset or scale correction must be recorded rather than hidden in code.
- Detect columns and sidebars from whitespace and aligned line clusters. Read each region top-to-bottom, then follow the source's column order.
- Treat tables, footnotes, marginalia, and captions as separate regions; do not merge them into body paragraphs.
- Use confidence and geometric overlap to identify questionable text. Low confidence is a review signal, not permission to guess.

## Output contract

For every generated PDF, report:

- input and output filenames;
- selected mode and why;
- source/output page count, page boxes, rotation, and render DPI;
- OCR engine, language models, version/settings, and coordinate strategy;
- pages or regions retained as image-only or marked low-confidence;
- whether headers, footers, and page numbers were only excluded from the text layer;
- search/copy validation result and representative visual comparison result;
- known OCR risks and the exact sample or pages needing proofreading.

Use a descriptive filename such as `<source>_可搜索版_版面保持.pdf` for the default mode, or `<source>_文字重排版.pdf` for explicit reflow mode.

## Common failures to avoid

- Replacing each page with a continuous OCR paragraph and calling it layout preservation.
- Rendering OCR text visibly with a guessed font that changes the page appearance.
- Using a non-Unicode font or omitting ToUnicode, making Chinese text unsearchable or copied as garbage.
- Ignoring PDF rotation, CropBox, DPI, or coordinate-origin differences.
- Reading a two-column page as one interleaved stream.
- Removing headers or page numbers from the visual page when only the text layer should be cleaned.
- Trusting low-confidence OCR for names, numbers, formulas, or tables without marking it for review.
- Claiming the output is text-only when images or difficult regions were intentionally retained.

## Completion gate

Do not claim completion unless the output passes all applicable checks:

- `layout-preserving` or explicit `text-reflow` mode is stated;
- page count, page boxes, rotation, and ordering match the source in layout-preserving mode;
- `qpdf --check` passes when available and `pdfinfo` can read the output;
- `pdftotext` extracts non-empty expected-language text from representative pages;
- text selection/copy works and preserves Chinese characters and punctuation;
- same-DPI renders show no unintended background changes, text drift, clipping, or occlusion;
- complex and low-confidence pages are listed with their fallback treatment;
- OCR settings, sample scope, validation results, and residual risks are reported.
