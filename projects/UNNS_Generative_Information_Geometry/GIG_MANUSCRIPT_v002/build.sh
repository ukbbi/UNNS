#!/bin/sh
# Compiles the monograph from src/*.tex. Any LaTeX error stops the build with a non-zero exit status.
# (tools/compose.py is an authoring tool that regenerates src/ from tpl/ and tools/v001_src/; it is not part of the build.)
set -e
cd "$(dirname "$0")"
for pass in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error main.tex > build.log
done
if grep -q "undefined" build.log; then echo "BUILD_FAILED: undefined references" >&2; exit 1; fi
echo BUILD_OK
