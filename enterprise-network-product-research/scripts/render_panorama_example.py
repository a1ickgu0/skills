"""Render the bundled Aruba layout example; requires ImageMagick for PNG output."""
import argparse
import html
import json
from pathlib import Path
import subprocess


def render(data):
    def text(x, y, value, size=15, color="#26324b", weight=400):
        return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}">{html.escape(value)}</text>'

    height = 160 + len(data["lanes"]) * 218
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1320" height="{height}" viewBox="0 0 1320 {height}" role="img" aria-labelledby="title desc" font-family="Hiragino Sans GB, PingFang SC, Noto Sans CJK SC, sans-serif">',
           '<title id="title">Aruba CX 产品全景图：八型号布局示例</title>',
           '<desc id="desc">基于Aruba研究输入的独立示例。按接口形态分层，突出气流、电源和TAA名称标注，不代表完整目录或官方认证结论。</desc>',
           f'<rect width="1320" height="{height}" fill="#f4f6f9"/>',
           text(28, 42, "Aruba CX 产品全景图", 28, weight=700),
           text(28, 72, "8款研究输入示例 · 按接口能力分层，非部署层级或性能排名 · 非全量官方核验", 16),
           text(28, 98, "读图：卡片头为SKU/子平台；正文为共同能力；末两行为采购差异与限制。", 14, "#59677b")]
    for i, lane in enumerate(data["lanes"]):
        y = 120 + i * 218
        out += [f'<rect x="28" y="{y}" width="1264" height="202" rx="6" fill="#ffffff"/>',
                f'<rect x="28" y="{y}" width="1264" height="34" rx="5" fill="#263d59"/>',
                text(42, y + 24, lane["label"], 18, "#ffffff", 700)]
        for j, item in enumerate(lane["items"]):
            x = 40 + j * 420
            out += [f'<rect x="{x}" y="{y+46}" width="404" height="144" rx="4" fill="#edf2f7"/>',
                    text(x + 12, y + 72, item["sku"], 21, weight=700),
                    text(x + 238, y + 71, item["platform"], 14)]
            for k, line in enumerate(item["lines"]):
                out.append(text(x + 12, y + 99 + k * 25, line, 14 if k > 1 else 15, weight=700 if k == 2 else 400))
    out += [text(28, height - 20, "输入日期2026-10-27 · TAA未标明≠不符合；电源制式未标明不默认AC · 字段依据见panorama-example.json", 13, "#59677b"), '</svg>']
    return "\n".join(out) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path(__file__).resolve().parents[1] / "references/panorama-example.json")
    parser.add_argument("--font", required=True, type=Path, help="Local licensed Chinese sans-serif font file")
    args = parser.parse_args()
    if not args.font.is_file():
        parser.error("font file does not exist")
    data = json.loads(args.data.read_text(encoding="utf-8"))
    svg = args.data.parent / "panorama_masked.svg"
    svg.write_text(render(data), encoding="utf-8")
    subprocess.run(["magick", "-font", str(args.font), "-background", "white", str(svg), str(svg.with_suffix(".png"))], check=True)


if __name__ == "__main__":
    main()
