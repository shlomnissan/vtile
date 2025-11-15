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
    parser.add_argument("-o", "--output-dir", type = Path, required = True, help = s)

    s = "Downsampling filter used when generating lower LODs (default: box)."
    parser.add_argument("--filter", choices = FILTERS.keys(), default = "box", help = s)

    s = "Optional filename prefix."
    parser.add_argument("--prefix", type = str, default = "", help = s)

    return parser.parse_args()

def main():
    args = parse_args()

    input_path = args.input
    tile_size = args.tile_size
    output_dir = args.output_dir
    filter  = args.filter
    prefix = args.prefix

if __name__ == "__main__":
    main()