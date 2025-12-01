#!/usr/bin/env python3
from __future__ import annotations

from typing import Dict
from pathlib import Path
from PIL import Image

import argparse

FILTERS: Dict[str, int] = {
    "nearest": Image.NEAREST,
    "box": Image.BOX,
    "bilinear": Image.BILINEAR,
}

def parse_args():
    s = "Generate tiled mip levels for images."
    parser = argparse.ArgumentParser(description = s)

    s = "Path to the input image."
    parser.add_argument("-i", "--input", type = Path, required = True, help = s)

    s = "Tile width in pixels."
    parser.add_argument("--tile-w", type = int, required = True, help = s)

    s = "Tile height in pixels."
    parser.add_argument("--tile-h", type = int, required = True, help = s)

    s = "Directory to write the tiles into."
    parser.add_argument("-o", "--output-dir", type = Path, default = "tiles", help = s)

    s = "Downsampling filter used when generating lower LODs (default: box)."
    parser.add_argument("--filter", choices = FILTERS.keys(), default = "box", help = s)

    s = "Optional filename prefix."
    parser.add_argument("--prefix", type = str, default = "", help = s)

    return parser.parse_args()

def validate_image_and_tile_size(image: Image.Image, tile_w: int, tile_h):
    width, height = image.size

    if tile_w <= 0:
        raise ValueError("Tile width must be a positive integer")

    if width % tile_w != 0:
        raise ValueError("Input width must be divisible by tile width")

    if tile_h <= 0:
        raise ValueError("Tile height must be a positive integer")

    if height % tile_h != 0:
        raise ValueError("Input height must be divisible by tile height")

def generate_tiles_for_level(
    image: Image.Image,
    lod: int,
    tile_w: int,
    tile_h: int,
    output_dir: Path,
    prefix: str,
    ext: str,
):
    width, height = image.size
    tiles_x = width // tile_w
    tiles_y = height // tile_h

    for y in range(tiles_y):
        for x in range(tiles_x):
            left = x * tile_w
            top = y * tile_h
            right = left + tile_w
            bottom = top + tile_h
            tile = image.crop((left, top, right, bottom))
            filename = f"{prefix}{lod}_{x}_{y}{ext}"
            output_path = output_dir / filename
            tile.save(output_path)

def build_mip_pyramid(
    image: Image.Image,
    tile_w: int,
    tile_h: int,
    output_dir: Path,
    prefix: str,
    ext: str,
    filter_name: str,
):
    resample = FILTERS[filter_name]
    current_image = image.copy()
    current_width, current_height = current_image.size
    lod = 0

    while True:
        print(f"Generating tiles for LOD {lod} ({current_width}x{current_height})")

        generate_tiles_for_level(
            image = current_image,
            lod = lod,
            tile_w = tile_w,
            tile_h = tile_h,
            output_dir = output_dir,
            prefix = prefix,
            ext = ext,
        )

        # reached the level where one axis equals tile size
        if current_width == tile_w or current_height == tile_h: break

        next_width = current_width // 2
        next_height = current_height // 2

        if next_width < tile_w or next_height < tile_h:
            break

        current_image = current_image.resize(
            (next_width, next_height),
            resample = resample,
        )

        current_width = next_width
        current_height = next_height
        lod += 1

def main():
    args = parse_args()

    input_path = args.input
    tile_w = args.tile_w
    tile_h = args.tile_h
    output_dir = args.output_dir
    filter_name  = args.filter
    prefix = args.prefix

    if not input_path.is_file():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    ext = input_path.suffix
    if not ext:
        raise ValueError("Input file must have an extension")

    image = Image.open(input_path)
    validate_image_and_tile_size(image, tile_w, tile_h)

    output_dir.mkdir(parents = True, exist_ok = True)

    width, height = image.size
    print(
        f"Input: {input_path} {width}x{height}\n"
        f"Tile size: {tile_w}x{tile_h}\n"
        f"Filter: {filter_name}\n"
        f"Output directory: {output_dir.resolve()}\n"
    )

    build_mip_pyramid(
        image = image,
        tile_w = tile_w,
        tile_h = tile_h,
        output_dir = output_dir,
        prefix = prefix,
        ext = ext,
        filter_name = filter_name,
    )

    print("\nDone.")

if __name__ == "__main__":
    main()