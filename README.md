# vtile

A tiny command-line tool that takes a large image and breaks it into uniformly sized tiles. I built it while experimenting with virtual textures and needed a quick way to generate tile sets from 8K and 16K assets.

`vtile` doesn’t try to do anything clever. It just loads an image, checks that it divides cleanly into the tile size you asked for, and writes out the tiles with a simple naming scheme. That’s it.

### Features
- Split any image into fixed-size tiles
- Ensures the dimensions are divisible by the tile size
- Preserves the input format
- Optional prefix for tile naming
- Optional post-processing filter

### Usage

```bash
vtile \
  --input example.png \
  --tile-size 256 \
  --output tiles
```

This will produce tiles named like `1_0_0.png`. LOD and coordinates are encoded as `lod_x_y` to keep filenames short and easy to scan.

### Example

The repository includes a sample 8192×8192 image (example.png) you can test with. It was created by Maurus Löffel. Higher resolutions and source files are [available here](https://drive.google.com/drive/folders/1K_G_hbFyohR8-xCCAlYx8xhsd_a7Ir7G).

Try: `vtile -i example.png -t 1024`

You should see a `tiles` directory that includes 4 LODs and 85 tiles all of which are 1024x1024.

### Why this exists

Virtual textures and tile streaming rely on breaking images into pages. I needed a simple repeatable way to generate the tiles for experiments and tests. `vtile` is the small boring part of the pipeline, the part that should just work so you can focus on the rest.

## License

```                                                                                                                              
Copyright (c) 2025-present Shlomi Nissan
https://shlom.dev

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
