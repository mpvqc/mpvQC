# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import QT_TRANSLATE_NOOP, QObject, Signal

if TYPE_CHECKING:
    from PySide6.QtCore import QSettings

_COMMENT_TYPES_KEY = "Common/commentTypes"


def default_comment_types() -> list[str]:
    return [
        str(QT_TRANSLATE_NOOP("CommentTypes", "Translation")),
        str(QT_TRANSLATE_NOOP("CommentTypes", "Spelling")),
        str(QT_TRANSLATE_NOOP("CommentTypes", "Punctuation")),
        str(QT_TRANSLATE_NOOP("CommentTypes", "Phrasing")),
        str(QT_TRANSLATE_NOOP("CommentTypes", "Timing")),
        str(QT_TRANSLATE_NOOP("CommentTypes", "Typeset")),
        str(QT_TRANSLATE_NOOP("CommentTypes", "Note")),
    ]


# Until something writes the key this run, an untyped read hands back the ini text, never the type that was stored
def _read_comment_types(stored: object) -> list[str]:
    if isinstance(stored, list):
        return [str(comment_type) for comment_type in stored]
    if isinstance(stored, str):
        return [stored]
    # a list the user emptied stores @Invalid(), which reads back as nothing
    return []


class CommentsSettingsService(QObject):
    comment_types_changed = Signal(list)

    def __init__(self, qsettings: QSettings, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._qsettings = qsettings

    @property
    def comment_types(self) -> list[str]:
        if not self._qsettings.contains(_COMMENT_TYPES_KEY):
            return default_comment_types()
        return _read_comment_types(self._qsettings.value(_COMMENT_TYPES_KEY))

    @comment_types.setter
    def comment_types(self, comment_types: list[str]) -> None:
        if self.comment_types == comment_types:
            return
        self._qsettings.setValue(_COMMENT_TYPES_KEY, comment_types)
        self.comment_types_changed.emit(comment_types)
