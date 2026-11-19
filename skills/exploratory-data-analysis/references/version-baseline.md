# Version baseline

## Version baseline (verified 2026-09-30)

The bundled core CSV/TSV/strict-JSON tools use only the Python standard
library. Optional inspectors were verified against these stable PyPI releases:

| Package | Version | Published | Used for |
|---|---:|---:|---|
| NumPy | `2.5.3` | 2026-09-06 | NPY/NPZ |
| h5py | `3.16.0` | 2026-03-06 | HDF5 metadata |
| Biopython | `1.88` | 2026-08-06 | FASTA/FASTQ streaming |
| Pillow | `12.3.0` | 2026-07-01 | PNG/JPEG metadata |
| tifffile | `2026.9.20` | 2026-09-21 | TIFF/OME-TIFF metadata |
| pandas | `3.0.6` | 2026-09-17 | Documented alternate tabular I/O |
| Polars | `1.44.2` | 2026-09-09 | Documented alternate tabular I/O |

NumPy 2.5.3 and tifffile
2026.9.20 require Python 3.12+. These pins are a dated direct-dependency
snapshot, not a transitive lockfile.

The isolated suite exercises these releases with Python 3.13 on synthetic local
fixtures; the pandas/Polars examples are executed separately. No scientific
service endpoints, authentication, or network I/O are used by bundled CLIs.
Install only capabilities needed for the task in a dedicated environment:

```bash
uv pip install \
  "numpy==2.5.3" \
  "h5py==3.16.0" \
  "biopython==1.88" \
  "pillow==12.3.0" \
  "tifffile==2026.9.20"
```

Optional alternate table engines:

```bash
uv pip install "pandas==3.0.6" "polars==1.44.2"
```
