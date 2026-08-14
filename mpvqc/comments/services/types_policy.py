# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import QObject, Signal, Slot

from .service import CommentsService
from .settings import CommentsSettingsService


class CommentTypesPolicyService(QObject):
    _comments = inject.attr(CommentsService)
    _settings = inject.attr(CommentsSettingsService)

    displayable_comment_types_changed = Signal(frozenset)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._displayable_comment_types = self._compute_displayable_comment_types()
        self._comments.comments_changed.connect(self._recompute)
        self._settings.comment_types_changed.connect(self._recompute)

    @property
    def displayable_comment_types(self) -> frozenset[str]:
        return self._displayable_comment_types

    @Slot()
    def _recompute(self) -> None:
        value = self._compute_displayable_comment_types()
        if value != self._displayable_comment_types:
            self._displayable_comment_types = value
            self.displayable_comment_types_changed.emit(value)

    def _compute_displayable_comment_types(self) -> frozenset[str]:
        return frozenset(self._settings.comment_types) | self._comments.distinct_comment_types
