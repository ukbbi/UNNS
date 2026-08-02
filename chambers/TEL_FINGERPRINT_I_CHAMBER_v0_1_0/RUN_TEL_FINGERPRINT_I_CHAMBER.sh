#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")"
PAGE="TEL_FINGERPRINT_I_CHAMBER_v0_1_0.html"
if command -v xdg-open >/dev/null 2>&1; then xdg-open "$PAGE" >/dev/null 2>&1 &
elif command -v open >/dev/null 2>&1; then open "$PAGE"
else printf 'Open %s in a modern browser.\n' "$(pwd)/$PAGE"
fi
