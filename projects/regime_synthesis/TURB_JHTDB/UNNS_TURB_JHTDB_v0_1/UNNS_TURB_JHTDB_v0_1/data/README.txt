DATA STORAGE RULES
==================

source/   Official JHTDB documentation and compact source reference products.
raw/      Untouched acquired JHTDB cutouts and acquisition metadata.
derived/  Fields, scales and coherent-object products derived from raw data.
controls/ Matched artificial corpora generated from validated real data.

Raw data are immutable.
Derived and control products must always name or record their parent source.

PUBLIC SOURCE ARCHIVE
=====================

source/zenodo/  Zenodo DOI record, archive metadata, exact deposited companion files, and restore map for heavy JHTDB-derived sources.

The heavy payload itself remains under raw/ locally and is not duplicated in lightweight project packages.
