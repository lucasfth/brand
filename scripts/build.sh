#!/usr/bin/env bash
# Rebuild dist/ from scripts/build.py, then decode-check every QR PNG.
set -euo pipefail
cd "$(dirname "$0")/.."
rm -rf dist
nix shell --impure \
  --expr 'with import <nixpkgs> {}; [ (python3.withPackages (p: [ p.fonttools ])) librsvg qrencode imagemagick zbar ]' \
  -c bash -c '
    python3 scripts/build.py
    for f in dist/qr/png/*.png; do
      got=$(zbarimg -q --raw "$f")
      [ "$got" = "${QR_URL:-HTTPS://HBIT.SH}" ] || { echo "QR decode failed: $f -> $got" >&2; exit 1; }
    done
    echo "built $(find dist -type f | wc -l | tr -d " ") files; QR decode ok"'
