# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Comment:
    time: int | float
    comment_type: str
    comment: str


@dataclass
class VideoSource:
    path: Path
    from_document: bool
    from_subtitle: bool
