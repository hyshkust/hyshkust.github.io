#!/usr/bin/env python3
"""Regenerate legacy publication and OCRTOC thumbnails without changing originals.

Requires Pillow. Run from any working directory, for example:
    python3 /path/to/repository/scripts/optimize_thumbnails.py
    python3 scripts/optimize_thumbnails.py --manifest /tmp/thumbnails.json

Images retain their full content and aspect ratio, are never enlarged, and are
saved as WebP at quality 88 / method 6 with a maximum width of 480 pixels.
The two existing EgoAlign and PASPA thumbnails are intentionally excluded.
"""

import argparse
import json
from pathlib import Path

from PIL import Image, ImageOps


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
MAX_WIDTH = 480
QUALITY = 88

# Explicit original sources keep reruns independent of the paths in index.html.
SOURCES = (
    "images/fa-lam.png",
    "images/PanoLAM.png",
    "images/Forge4D.png",
    "images/meshlam.png",
    "images/ldcm.png",
    "images/visa3d.png",
    "images/CoProSketch.png",
    "images/LAM.png",
    "images/LaMP.png",
    "images/MulsMo.png",
    "images/GIC.png",
    "images/MoGenTS.png",
    "images/freditor.png",
    "images/sketch2nerf.png",
    "images/OV9D.png",
    "images/selfcatposesize.png",
    "images/fs6d.png",
    "images/ffb6d.png",
    "images/ishape.png",
    "images/pvn3d.png",
    "images/OCRTOC.png",
)


def optimize_thumbnails():
    output_directory = REPOSITORY_ROOT / "images" / "thumbnails"
    output_directory.mkdir(parents=True, exist_ok=True)
    records = []

    for source in SOURCES:
        source_path = REPOSITORY_ROOT / source
        output_path = output_directory / (source_path.stem.lower() + ".webp")
        with Image.open(source_path) as original:
            thumbnail = ImageOps.exif_transpose(original)
            mode = "RGBA" if "A" in thumbnail.getbands() or "transparency" in thumbnail.info else "RGB"
            thumbnail = thumbnail.convert(mode)
            if thumbnail.width > MAX_WIDTH:
                target_height = max(1, round(thumbnail.height * MAX_WIDTH / thumbnail.width))
                thumbnail = thumbnail.resize((MAX_WIDTH, target_height), Image.Resampling.LANCZOS)
            thumbnail.save(output_path, format="WEBP", quality=QUALITY, method=6)
            records.append({
                "source": source,
                "path": output_path.relative_to(REPOSITORY_ROOT).as_posix(),
                "width": thumbnail.width,
                "height": thumbnail.height,
                "bytes": output_path.stat().st_size,
                "original_bytes": source_path.stat().st_size,
            })

    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, help="Optional JSON output with source, path, dimensions, and byte sizes")
    args = parser.parse_args()
    records = optimize_thumbnails()

    if args.manifest:
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")

    for record in records:
        print(f"{record['source']} -> {record['path']} "
              f"({record['width']}x{record['height']}, "
              f"{record['original_bytes']:,} -> {record['bytes']:,} bytes)")
    original_bytes = sum(record["original_bytes"] for record in records)
    thumbnail_bytes = sum(record["bytes"] for record in records)
    saving = 100 * (1 - thumbnail_bytes / original_bytes)
    print(f"Total: {len(records)} images; {original_bytes:,} -> {thumbnail_bytes:,} bytes ({saving:.1f}% smaller)")


if __name__ == "__main__":
    main()
