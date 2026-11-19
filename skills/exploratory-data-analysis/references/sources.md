# Source basis

## Source basis

Current parser APIs and format guidance were checked 2026-09-30. Detailed links are in
the six references. Key sources include:

- Python [`csv`](https://docs.python.org/3/library/csv.html) and
  [`json`](https://docs.python.org/3/library/json.html);
- NumPy [`load`](https://numpy.org/doc/stable/reference/generated/numpy.load.html)
  and [security](https://numpy.org/doc/stable/reference/security.html);
- [pandas I/O](https://pandas.pydata.org/docs/user_guide/io.html),
  [Polars `read_csv`](https://docs.pola.rs/api/python/stable/reference/api/polars.read_csv.html),
  and [h5py links](https://docs.h5py.org/en/stable/high/group.html);
- [Biopython SeqIO](https://biopython.org/docs/latest/Tutorial/chapter_seqio.html),
  [Pillow decompression-bomb guidance](https://pillow.readthedocs.io/en/stable/reference/Image.html),
  and the [OME-TIFF specification](https://ome-model.readthedocs.io/en/stable/ome-tiff/specification.html);
- NIST [EDA handbook](https://www.itl.nist.gov/div898/handbook/eda/eda.htm),
  FDA/ICH [E9(R1)](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e9r1-statistical-principles-clinical-trials-addendum-estimands-and-sensitivity-analysis-clinical),
  EPA [detection-limit guidance](https://www.epa.gov/system/files/documents/2025-09/wqxdetectionlimitsbestpracticesguide_final.pdf),
  and scikit-learn [data-leakage guidance](https://scikit-learn.org/stable/common_pitfalls.html);
- Benjamini–Hochberg [FDR](https://academic.oup.com/jrsssb/article/57/1/289/7035855),
  National Academies [reproducibility](https://doi.org/10.17226/25303), and
  Wilkinson et al. [FAIR principles](https://doi.org/10.1038/sdata.2016.18).
