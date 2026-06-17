#!/usr/bin/env bash
# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: MIT
#
# Regenerate the mangled Qt symbol names the Linux drop-shadow hack pins in
# mpvqc/services/platform/linux/window_geometry.py

set -euo pipefail

if [[ "$(uname -s)" != "Linux" ]]; then
    echo "skipped: pinned symbols are Linux-only"
    exit 0
fi

for tool in nm c++filt; do
    command -v "$tool" >/dev/null || {
        echo "error: $tool not found (install binutils)" >&2
        exit 1
    }
done

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
target="$repo_root/mpvqc/services/platform/linux/window_geometry.py"
lib_dir="$(uv run python -c 'import PySide6, pathlib; print(pathlib.Path(PySide6.__file__).parent / "Qt" / "lib")')"

declare -A library=(
    [_HANDLE_SYMBOL]="Qt6Gui"
    [_SET_CUSTOM_MARGINS_SYMBOL]="Qt6WaylandClient"
)
declare -A signature=(
    [_HANDLE_SYMBOL]="QWindow::handle() const"
    [_SET_CUSTOM_MARGINS_SYMBOL]="QtWaylandClient::QWaylandWindow::setCustomMargins(QMargins const&)"
)

# Find the mangled symbol in a bundled library whose demangling exactly matches
# the wanted C++ signature (versioned "@@..." suffix stripped).
mangled_for() {
    local lib="$1" want="$2" so symbols
    so="$(find "$lib_dir" -maxdepth 1 -name "lib$lib.so*" 2>/dev/null | sort | head -n1)" || true
    [[ -n "$so" ]] || return 1
    symbols="$(nm -D --defined-only "$so" | awk '{print $NF}' | sed 's/@@.*//' | sort -u)"
    paste <(printf '%s\n' "$symbols") <(printf '%s\n' "$symbols" | c++filt) |
        awk -F'\t' -v want="$want" '$2 == want { print $1; exit }'
}

for constant in "${!library[@]}"; do
    symbol="$(mangled_for "${library[$constant]}" "${signature[$constant]}")" || true
    if [[ -z "$symbol" ]]; then
        echo "error: no symbol in lib${library[$constant]} demangles to '${signature[$constant]}'" >&2
        echo "       the private Qt API may have changed; window_geometry.py needs a manual look." >&2
        exit 1
    fi
    sed -i "s|^$constant = \".*\"|$constant = \"$symbol\"|" "$target"
done
