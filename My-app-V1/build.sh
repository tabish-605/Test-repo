#!/usr/bin/env bash
set -e
ZIP=observa-lite.zip
rm -f $ZIP
DIR=$(basename $(pwd))
if [ "$DIR" != "observa-lite" ]; then echo "Run from repo root"; exit 1; fi
zip -r9 ../$ZIP . -x "*/node_modules/*" "*/__pycache__/*"
echo "Created $ZIP"
