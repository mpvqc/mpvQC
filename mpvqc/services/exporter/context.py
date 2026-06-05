# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mpvqc.services.build_info import BuildInfoService
    from mpvqc.services.comments import CommentsService
    from mpvqc.services.player import PlayerService
    from mpvqc.services.settings import SettingsService


@dataclass(frozen=True)
class RenderContext:
    settings: SettingsService
    player: PlayerService
    build_info: BuildInfoService
    comments: CommentsService
