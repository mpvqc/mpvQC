# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from PySide6.QtCore import QMimeDatabase

from mpvqc.importing.domain import DOCUMENT_EXTENSIONS, SUBTITLE_EXTENSIONS

_VIDEO_FALLBACK_EXTENSIONS: frozenset[str] = frozenset({".avi", ".mkv", ".mp4"})


def video_file_glob_pattern() -> str:
    patterns = {f"*{ext}" for ext in _VIDEO_FALLBACK_EXTENSIONS}

    for mime_type in QMimeDatabase().allMimeTypes():
        if mime_type.name().startswith("video/"):
            patterns.update(mime_type.globPatterns())

    return _format_glob_pattern(patterns)


def subtitle_file_glob_pattern() -> str:
    return _format_glob_pattern({f"*{ext}" for ext in SUBTITLE_EXTENSIONS})


def document_file_glob_pattern() -> str:
    return _format_glob_pattern({f"*{ext}" for ext in DOCUMENT_EXTENSIONS})


def _format_glob_pattern(patterns: set[str]) -> str:
    return f" ({' '.join(sorted(patterns))})"
