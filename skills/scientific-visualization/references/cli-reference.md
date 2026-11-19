# Pinned snapshot and bundled CLIs

## Pinned snapshot

The examples and native smoke tests use these direct package pins, reviewed 2026-10-01:

```bash
uv run --isolated --no-project --python 3.13 \
  --with "matplotlib==3.11.2" \
  --with "seaborn==0.13.2" \
  --with "plotly==7.1.0" \
  --with "kaleido==1.4.0" \
  --with "pillow==12.3.0" \
  --with "pypdf==6.19.0" \
  python your_figure.py
```

This is a dated direct-dependency snapshot, not a transitive lock. Create a lock in the consuming figure project for exact replay; the repository lock does not cover these isolated scientific dependencies.

## Bundled CLIs

Bundled CLIs make no network calls and apply input byte/pixel limits; these are not general parser-memory or CPU limits. They reject final-path symlinks and refuse overwrite unless `--force` is explicit. Matplotlib file timestamps and backend versions can vary, so identical inputs do not guarantee byte-identical output.

### Inspect raster/vector metadata

```bash
uv run --isolated --no-project --python 3.13 \
  --with "pillow==12.3.0" \
  python scripts/image_metadata.py figure.tiff \
  --format tiff --mode RGB --min-dpi 300 --target-width-mm 85 \
  --alpha-policy forbid
```

Supports raster images (Pillow), SVG, PDF (pypdf), and EPS/PS. Reports dimensions, DPI/effective DPI, mode, alpha, ICC presence, compression, and first-page PDF fonts. PDF dimensions include UserUnit and rotation, with CropBox separate from MediaBox. It does not fully decode every raster frame, inspect all PDF pages/fonts, or measure embedded-raster DPI.

### Audit palette contrast and grayscale

```bash
uv run --isolated --no-project --python 3.13 \
  python scripts/palette_audit.py \
  --palette okabe_ito_on_white \
  --background FFFFFF \
  --role graphical
```

Reports exact WCAG sRGB contrast plus pairwise CIE L* grayscale screening. The grayscale threshold is a heuristic, not a standard.

### Plan/screen publisher export

```bash
uv run --isolated --no-project --python 3.13 \
  python scripts/export_plan.py \
  --publisher nature \
  --figure-type combination \
  --width single \
  --phase final
```

Add `--input figure.pdf` to screen machine-readable properties. Profiles record source dates individually. Most were checked 2026-10-01; Science retains its 2026-07-23 snapshot because live access failed, and ACS is explicitly legacy guidance. Phase mismatches and advisory rules require review; a zero failure count is not acceptance.

### Preview styles

```bash
uv run --isolated --no-project --python 3.13 \
  --with "matplotlib==3.11.2" \
  python scripts/style_preview.py \
  --output outputs/style-preview \
  --style default \
  --palette okabe_ito_on_white \
  --formats png,svg
```

### Inspect/write styles and smoke-test export

```bash
uv run --isolated --no-project --python 3.13 \
  python scripts/style_presets.py --list
uv run --isolated --no-project --python 3.13 \
  python scripts/style_presets.py --show nature
uv run --isolated --no-project --python 3.13 \
  --with "matplotlib==3.11.2" \
  python scripts/figure_export.py --demo outputs/export-smoke --manifest
```
