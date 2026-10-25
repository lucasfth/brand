#!/usr/bin/env bash
# Copy a pinned release of the hbit brand assets into a consumer repository.
# Usage: sync.sh <ref> <dest-dir> <dist-path>...
#   sync.sh v1 public favicon/favicon.ico favicon/apple-touch-icon.png
# Files land flat in <dest-dir>. The ref must be a tag so every site is reproducible.
set -euo pipefail
[ $# -ge 3 ] || { sed -n '2,5p' "$0" >&2; exit 2; }
ref=$1 dest=$2; shift 2
mkdir -p "$dest"
for path in "$@"; do
  curl -fsSL "https://raw.githubusercontent.com/lucasfth/brand/$ref/dist/$path" -o "$dest/$(basename "$path")"
  echo "$ref dist/$path -> $dest/$(basename "$path")"
done
