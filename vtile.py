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
    s = "Generate tiled mip levels for a square image."
    parser = argparse.ArgumentParser(description = s)

    s = "Path to the input image."
    parser.add_argument("-i", "--input", type = Path, required = True, help = s)

    s = "Tile size in pixels (square tiles)."
    parser.add_argument("-t", "--tile-size", type = int, required = True, help = s)

    s = "Directory to write the tiles into."
    parser.add_argument("-o", "--output-dir", type = Path, default = "tiles", help = s)

    s = "Downsampling filter used when generating lower LODs (default: box)."
    parser.add_argument("--filter", choices = FILTERS.keys(), default = "box", help = s)

    s = "Optional filename prefix."
    parser.add_argument("--prefix", type = str, default = "", help = s)

    return parser.parse_args()

def validate_image_and_tile_size(image: Image.Image, tile_size: int):
    width, height = image.size

    if width != height:
        raise ValueError("Image must be square")

    if tile_size <= 0:
        raise ValueError("Tile size must be a positive integer")

    if width % tile_size != 0:
        raise ValueError(
            f"Image size {width} is not divisible by tile size {tile_size}."
        )

    # require ratio to be a power of two so that halving reaches a 1x1 tile
    ratio = width // tile_size
    if ratio & (ratio - 1) != 0:
        raise ValueError(
            f"(image_size / tile_size) = {ratio}, which is not a power of two."
        )

    return width

def generate_tiles_for_level(
    image: Image.Image,
    lod: int,
    tile_size: int,
    output_dir: Path,
    prefix: str,
    ext: str,
):
    width, height = image.size
    tiles_x = width // tile_size
    tiles_y = height // tile_size

    for y in range(tiles_y):
        for x in range(tiles_x):
            left = x * tile_size
            top = y * tile_size
            right = left + tile_size
            bottom = top + tile_size
            tile = image.crop((left, top, right, bottom))
            filename = f"{prefix}{lod}_{x}_{y}{ext}"
            output_path = output_dir / filename
            tile.save(output_path)

def build_mip_pyramid(
    base_image: Image.Image,
    base_size: int,
    tile_size: int,
    output_dir: Path,
    prefix: str,
    ext: str,
    filter_name: str,
):
    resample = FILTERS[filter_name]
    current_image = base_image.copy()
    current_size = base_size
    lod = 0

    while True:
        print(f"Generating tiles for LOD {lod} ({current_size}x{current_size})")

        generate_tiles_for_level(
            image = current_image,
            lod = lod,
            tile_size = tile_size,
            output_dir = output_dir,
            prefix = prefix,
            ext = ext,
        )

        # reached the level where there is exactly 1x1 tile of tile_size
        if current_size == tile_size: break

        next_size = current_size // 2
        if next_size < tile_size:
            raise RuntimeError(
                f"Next mip size {next_size} is smaller than tile size {tile_size}. "
                f"This should not happen if validation passed."
            )

        current_image = current_image.resize(
            (next_size, next_size),
            resample = resample,
        )

        current_size = next_size
        lod += 1

def main():
    args = parse_args()

    input_path = args.input
    tile_size = args.tile_size
    output_dir = args.output_dir
    filter_name  = args.filter
    prefix = args.prefix

    if not input_path.is_file():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    ext = input_path.suffix
    if not ext:
        raise ValueError("Input file must have an extension")

    output_dir.mkdir(parents = True, exist_ok = True)
    image = Image.open(input_path)
    base_size = validate_image_and_tile_size(image, tile_size)

    print(
        f"Input: {input_path} ({base_size}x{base_size}), "
        f"tile size: {tile_size}, "
        f"filter: {filter_name}"
    )

    print(f"Writing tiles to: {output_dir.resolve()}")

    build_mip_pyramid(
        base_image = image,
        base_size = base_size,
        tile_size = tile_size,
        output_dir = output_dir,
        prefix = prefix,
        ext = ext,
        filter_name = filter_name,
    )

    print("Done.")

if __name__ == "__main__":
    main()