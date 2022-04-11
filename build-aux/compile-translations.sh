#!/usr/bin/env bash

TRANSLATIONS_IN="$1"
TRANSLATIONS_OUT="$2"
TOOL="$3"

for file_path in "$TRANSLATIONS_IN"/* ; do
    file_name=$(basename -- "$file_path")
    file_name="${file_name%.*}"
    "$TOOL" "$file_path" -qm "$TRANSLATIONS_OUT/$file_name.qm"
done
