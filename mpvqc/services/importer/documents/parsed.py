# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from mpvqc.datamodels import Comment


@dataclass(frozen=True)
class ParsedDocument:
    video: Path | None
    subtitles: tuple[Path, ...]
    comments: tuple[Comment, ...]
