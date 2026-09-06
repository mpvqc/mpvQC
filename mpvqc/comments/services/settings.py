# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, Self

from PySide6.QtCore import QT_TRANSLATE_NOOP, QObject, Signal

from mpvqc.services import MISSING, Setting

if TYPE_CHECKING:
    from collections.abc import Callable

    from PySide6.QtCore import QSettings


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
def _read_comment_types(stored: object, default: Callable[[], list[str]]) -> list[str]:
    if stored is MISSING:
        return default()
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
        self.qsettings = qsettings

    def _notify_comment_types(self, comment_types: list[str]) -> None:
        self.comment_types_changed.emit(comment_types)

    comment_types: Setting[Self, list[str]] = Setting[Self, list[str]](
        "Common/commentTypes",
        default=default_comment_types,
        decode=_read_comment_types,
        notify=_notify_comment_types,
    )
