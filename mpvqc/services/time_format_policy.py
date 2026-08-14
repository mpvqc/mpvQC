# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import QObject, Signal, Slot

from mpvqc.shared import MILLISECONDS_PER_SECOND, needs_long_format

from .comments import CommentsService
from .player import PlayerService


class TimeFormatPolicyService(QObject):
    _comments = inject.attr(CommentsService)
    _player = inject.attr(PlayerService)

    table_long_format_changed = Signal(bool)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._table_long_format = self._compute_table_long_format()
        self._player.duration_changed.connect(self._recompute)
        self._comments.comments_changed.connect(self._recompute)

    @property
    def table_long_format(self) -> bool:
        return self._table_long_format

    @Slot()
    def _recompute(self) -> None:
        value = self._compute_table_long_format()
        if value != self._table_long_format:
            self._table_long_format = value
            self.table_long_format_changed.emit(value)

    def _compute_table_long_format(self) -> bool:
        if needs_long_format(self._player.duration):
            return True
        count = self._comments.count
        if count == 0:
            return False
        # Comments are sorted by time, so the last one carries the maximum
        last_comment = self._comments.comment_at(count - 1)
        return needs_long_format(last_comment.time / MILLISECONDS_PER_SECOND)
