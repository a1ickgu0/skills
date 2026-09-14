# Implementation Notes

## 1. OCR backend selection

Reuse the source skill's sample-first approach and coordinate-aware OCR requirement. On macOS, Vision is the preferred local backend for Chinese scans when it returns stable line/word boxes and confidence. PaddleOCR is a good portable choice; Tesseract is a fallback for clean, high-contrast pages. Record engine version, language, recognition mode, render DPI, rotation handling, and preprocessing for every run.

Do not assume an OCR engine's coordinates use the same origin as PDF coordinates. OCR commonly uses a top-left normalized origin, while PDF drawing uses points with a bottom-left origin. Convert through the actual rendered image dimensions, PDF page box, and page rotation. Validate with at least three landmarks on a sample page.

## 2. Page rendering and classification

Use `pdfinfo` and `pdfimages -list` or equivalent libraries to inspect page boxes and embedded images. Render representative pages at roughly 180–300 DPI. Include cover, contents, body, chapter opening, multi-column, table, footnote, illustration, vertical-text, and poor-quality pages when present.

Classify each page as ordinary text, complex layout, image-heavy, blank/decorative, or uncertain. A page can remain image-backed and still gain a searchable OCR layer. Image retention is not a failure in `layout-preserving`; it is the mechanism that preserves visual fidelity.

## 3. Layout-preserving PDF construction

The safest default is:

1. copy or render the source page as an unchanged background;
2. place a transparent OCR text layer over it;
3. use a Unicode font with a valid ToUnicode map;
4. keep the text layer aligned to the source's line boxes and baselines;
5. avoid visible redraw unless the user explicitly requests a text-only page.

For a PDF library, prefer native text operators with per-word or per-character positioning. If a high-level library cannot emit reliable invisible Unicode text, use a PDF engine that embeds fonts and writes ToUnicode mappings, or retain the original page and produce a clearly labeled OCR companion instead of shipping a broken text layer.

The text layer must not hide the scan. Do not paint white rectangles over the background to make OCR text fit. If a region is uncertain, keep its original pixels and either omit the uncertain text or mark it as low-confidence in the processing report.

## 4. Coordinate normalization

For an image width `W_px`, image height `H_px`, and page dimensions `W_pt × H_pt`, first map a top-left image coordinate to unrotated PDF points:

```text
x_pt = x_px × W_pt / W_px
y_pt = H_pt − y_px × H_pt / H_px
```

Then apply the source page's rotation and CropBox/MediaBox relationship. Do not use the physical paper size inferred from the filename or a default letter/A4 size. Preserve MediaBox, CropBox, BleedBox, TrimBox, and ArtBox when the source defines them.

Calibrate scale and offset on a sample. Compare the top, middle, and bottom text lines; a single calibration point can hide non-uniform errors. Recheck landscape and rotated pages independently.

## 5. Reading order and regions

Group OCR words into lines using vertical overlap and baseline distance. Detect columns and sidebars from whitespace and aligned line clusters before sorting. Within a region, sort top-to-bottom and left-to-right; across regions, follow the visual reading order. Keep tables, captions, footnotes, marginal notes, and headers as separate regions.

Remove repeated headers, running titles, and isolated page numbers only from the text layer, and only when repetition and geometry make the classification reliable. Never remove them from the visual background in layout-preserving mode.

## 6. Font and glyph strategy

OCR text may not use the source font. In layout-preserving mode, the background supplies the visible glyphs, so the overlay font should prioritize accurate Unicode mapping and stable glyph widths over visual styling. Use a font known to contain the target scripts, embed it when licensing permits, and verify that copied Chinese characters are not empty, substituted, or mapped to private-use code points.

Use invisible text rendering only after testing selection in Preview, Acrobat, browser PDF viewers, and at least one Chinese-capable reader where available. Some viewers expose invisible text differently; record the tested viewers and limitations.

## 7. Difficult pages and fallback

Keep pages or regions image-only when OCR boxes overlap, reading order is ambiguous, text is severely skewed, formulas are not recognized, tables cannot be segmented, or confidence is below the configured threshold. A partial OCR layer is acceptable if its coverage and limitations are reported. Never use guessed text to fill a visually aligned layer.

For vertical Chinese, detect orientation and use an OCR model that reports vertical boxes; do not rotate text merely because the page is portrait. For double-page scans, detect the gutter and split the page only if doing so preserves the source page contract; otherwise keep the original page as one canvas.

## 8. Sample and regression checks

Before full conversion, create a sample from every page class. Render input and output at the same DPI and compare:

- page dimensions and crop;
- background pixel similarity;
- text-layer location at top/middle/bottom;
- column order and line breaks;
- selection/copy output;
- glyph coverage and replacement characters.

After batch conversion, inspect the first, last, cover, contents, chapter, table, image, and lowest-confidence pages. Keep a machine-readable processing manifest containing page number, OCR confidence, recognized character/word count, text-layer coverage, fallback status, and error message.

## 9. Validation commands

Use commands available on the host:

```bash
pdfinfo output.pdf
pdftotext -f 1 -l 3 output.pdf -
qpdf --check output.pdf                 # when qpdf is installed
pdftoppm -f 1 -l 3 -png -r 150 output.pdf out/page
```

Also validate that the input and output have equal page counts and equal page boxes in layout-preserving mode. Parse the PDF with a library when possible to inspect rotations and text operators. `pdftotext` being non-empty is necessary but not sufficient: visually inspect renders and test selecting/copying Chinese text.

## 10. Reporting

Report the selected mode, source/output metadata, OCR backend and settings, coordinate mapping, calibration pages, pages with retained image-only regions, low-confidence pages, text-layer coverage, validation commands and results, and residual OCR risks. Distinguish “visual fidelity” from “text accuracy”; preserving the background can make the first excellent even when the second still requires proofreading.
