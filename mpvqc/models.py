# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass


@dataclass
class Comment:
    time: int
    comment_type: str
    comment: str
