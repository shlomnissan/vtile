# vtile

A tiny command line tool that splits large images into tiled mip pyramids.

Built while experimenting with [virtual textures](https://github.com/shlomnissan/virtual-textures) and needing a fast, repeatable way to generate tiles from high-resolution images. `vtile` has a single job: take a large image and turn it into a predictable set of tiles across multiple LODs.

### Why this exists

Virtual textures and tile streaming start by breaking large images into pages. `vtile` handles this boring step. It lets you focus on page tables, residency, feedback passes, and everything else that actually matters.

### Features
- Split any image into tiles
- Validate image dimensions against tile size
- Preserve the input image format
- Generate mip levels
- Optional downsampling filter
- Optional per tile padding for correct texture filtering
- Optional filename prefix

### CLI options

| Option | Description | Default |
|------|-------------|---------|
| `-i`, `--input` | Path to the input image | — |
| `--tile-w` | Tile width in pixels | — |
| `--tile-h` | Tile height in pixels | — |
| `-o`, `--output-dir` | Directory to write tiles into | `tiles` |
| `--filter` | Downsampling filter for lower LODs (`nearest`, `box`, `bilinear`) | `box` |
| `-p`, `--padding` | Padding in pixels added on all sides of each tile | `0` |
| `--prefix` | Optional filename prefix | `""` |

### Project overview

The repository includes a sample 8192×8192 image (`example.png`) for testing created by Maurus Löffel. Higher resolutions and source files are [available here](https://drive.google.com/drive/folders/1K_G_hbFyohR8-xCCAlYx8xhsd_a7Ir7G).

#### Basic usage
```bash
python vtile.py -i example.png --tile-w 1024 --tile-h 1024
```

This generates a tiles directory containing multiple tiles per LODs. Tiles are named using the format `lod_x_y`. Short and easy to scan.

#### Padding and filtering

By default tiles are generated without padding. This works for nearest neighbor sampling.

Linear and trilinear filtering are different. They sample across tile boundaries. Without padding this produces visible seams in virtual textures and tile streaming systems.

`vtile` supports per tile padding to fix this:
```bash
python vtile.py -i example.png --tile-w 1024 --tile-h 1024 --padding 2
```

When padding is enabled:
- Extra pixels are added on all sides of each tile
- Padding pixels duplicate edge pixels using `CLAMP_TO_EDGE`
- The core tile remains `tile_w × tile_h`
- The output tile size becomes `(tile_w + 2p) × (tile_h + 2p)`
- The result is tiles that can be sampled safely with bilinear and trilinear filtering.
- Padding is applied per LOD and does not affect tile layout or naming.

### Dependencies
`vtile` is a single-file Python script. It depends on [Pillow](https://pillow.readthedocs.io/en/stable/) for image loading and saving.

If Pillow is not installed, install it with:
```bash
pip install pillow
```

## License

```
Copyright (c) 2025-present Shlomi Nissan
https://shlom.dev | https://vglx.org

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
