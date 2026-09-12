TOOLS
=====

acquire/   JHTDB acquisition clients and cutout request tools.
validate/  Raw/source and transformation validators.
derive/    Physical-field and multiscale derivations.
ladders/   Native-ladder builders plus STRUC-I / STRUC-PERC-I adapters.
controls/  Matched-control generators.
analyze/   Family, route, intermittency and control-comparison analysis.

All tools must be reproducible from configuration + recorded input checksums.
No tool should silently overwrite a raw source file.
