# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from mpvqc.importing.domain import DOCUMENT_EXTENSIONS, SUBTITLE_EXTENSIONS
from mpvqc.importing.services import document_file_glob_pattern, subtitle_file_glob_pattern, video_file_glob_pattern


def test_document_file_glob_pattern_wraps_sorted_extensions() -> None:
    expected = f" ({' '.join(sorted(f'*{ext}' for ext in DOCUMENT_EXTENSIONS))})"

    assert document_file_glob_pattern() == expected


def test_subtitle_file_glob_pattern_wraps_sorted_extensions() -> None:
    expected = f" ({' '.join(sorted(f'*{ext}' for ext in SUBTITLE_EXTENSIONS))})"

    assert subtitle_file_glob_pattern() == expected


def test_video_file_glob_pattern_includes_fixed_fallback_patterns() -> None:
    pattern = video_file_glob_pattern()

    assert "*.avi" in pattern
    assert "*.mkv" in pattern
    assert "*.mp4" in pattern
