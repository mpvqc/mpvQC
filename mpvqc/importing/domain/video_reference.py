# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from pathlib import Path

SUBTITLE_WITH_VIDEO_REFERENCE_EXTENSIONS: frozenset[str] = frozenset({".ass", ".ssa"})


def parse_video_references(content: str) -> tuple[Path, ...]:
    references = []

    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line.startswith("Video File:"):
            continue

        video_path = line.split(":", 1)[1].strip()
        if video_path:
            references.append(Path(video_path))

    return tuple(references)
