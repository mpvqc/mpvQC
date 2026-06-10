# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from typing import TYPE_CHECKING, assert_never, override

from PySide6.QtCore import (
    Property,
    QAbstractListModel,
    QByteArray,
    QCoreApplication,
    QSortFilterProxyModel,
    Qt,
    Signal,
)
from PySide6.QtQml import QmlElement

if TYPE_CHECKING:
    from typing import Any

    from PySide6.QtCore import QModelIndex, QObject, QPersistentModelIndex

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@dataclass(frozen=True)
class TextKey:
    text: str


@dataclass(frozen=True)
class IconKey:
    name: str


type Key = TextKey | IconKey


@dataclass(frozen=True)
class Shortcut:
    category: str
    label: str
    alternatives: tuple[tuple[Key, ...], ...]
    note: str = ""

    @classmethod
    def of(cls, category: str, label: str, *alternatives: list[Key | str], note: str = "") -> Shortcut:
        return cls(
            category=category,
            label=label,
            alternatives=tuple(
                tuple(TextKey(key) if isinstance(key, str) else key for key in alternative)
                for alternative in alternatives
            ),
            note=note,
        )

    @cached_property
    def sequences(self) -> list[list[dict[str, str]]]:
        return [[self.role_data(key) for key in alternative] for alternative in self.alternatives]

    @staticmethod
    def role_data(key: Key) -> dict[str, str]:
        match key:
            case TextKey(text):
                return {"text": text}
            case IconKey(name):
                return {"icon": name}
            case _:
                assert_never(key)

    @cached_property
    def search_text(self) -> str:
        chords = [self.chord_text(alternative) for alternative in self.alternatives]
        searchable_chords = [chord for chord in chords if chord]
        return "\n".join([self.label, self.category, *searchable_chords]).lower()

    @staticmethod
    def chord_text(alternative: tuple[Key, ...]) -> str:
        return "+".join(key.text for key in alternative if isinstance(key, TextKey))


RETURN = IconKey("return")
BACKSPACE = IconKey("backspace")
ARROW_UP = IconKey("arrowUp")
ARROW_DOWN = IconKey("arrowDown")
ARROW_LEFT = IconKey("arrowLeft")
ARROW_RIGHT = IconKey("arrowRight")
SPACE = IconKey("space")


def build_shortcuts() -> tuple[Shortcut, ...]:
    # lupdate only extracts strings from calls literally named "translate"
    translate = QCoreApplication.translate

    ctrl = translate("KeyboardKeys", "Ctrl")
    shift = translate("KeyboardKeys", "Shift")
    alt = translate("KeyboardKeys", "Alt")
    delete = translate("KeyboardKeys", "Delete")

    mpvqc = "mpvQC"
    comments = translate("ShortcutsDialog", "Comments")
    video = translate("ShortcutsDialog", "Video")

    subtitle_seek_note = translate(
        "ShortcutsDialog",
        "With embedded subtitle tracks, seeking is limited to lines mpv has already buffered. External subtitle files work across the whole video.",
    )

    return (
        Shortcut.of(mpvqc, translate("ShortcutsDialog", "New QC Document"), [ctrl, "N"]),
        Shortcut.of(mpvqc, translate("ShortcutsDialog", "Open QC Document(s)"), [ctrl, "O"]),
        Shortcut.of(mpvqc, translate("ShortcutsDialog", "Save QC Document"), [ctrl, "S"]),
        Shortcut.of(mpvqc, translate("ShortcutsDialog", "Save as new QC Document"), [ctrl, shift, "S"]),
        Shortcut.of(mpvqc, translate("ShortcutsDialog", "Open Video"), [ctrl, alt, "O"]),
        Shortcut.of(mpvqc, translate("ShortcutsDialog", "Resize Video to Original Resolution"), [ctrl, "R"]),
        Shortcut.of(mpvqc, translate("ShortcutsDialog", "Add Comment"), ["E"]),
        Shortcut.of(mpvqc, translate("ShortcutsDialog", "Keyboard Shortcuts"), ["?"]),
        Shortcut.of(mpvqc, translate("ShortcutsDialog", "Open Search"), [ctrl, "F"]),
        Shortcut.of(mpvqc, translate("ShortcutsDialog", "Undo Previous Action"), [ctrl, "Z"]),
        Shortcut.of(mpvqc, translate("ShortcutsDialog", "Redo Previous Action"), [ctrl, shift, "Z"]),
        Shortcut.of(mpvqc, translate("ShortcutsDialog", "Quit"), [ctrl, "Q"]),
        Shortcut.of(comments, translate("ShortcutsDialog", "Edit Comment"), [RETURN]),
        Shortcut.of(comments, translate("ShortcutsDialog", "Copy Comment to Clipboard"), [ctrl, "C"]),
        Shortcut.of(comments, translate("ShortcutsDialog", "Delete Comment"), [BACKSPACE], [delete]),
        Shortcut.of(comments, translate("ShortcutsDialog", "Previous Comment"), [ARROW_UP]),
        Shortcut.of(comments, translate("ShortcutsDialog", "Next Comment"), [ARROW_DOWN]),
        Shortcut.of(video, translate("ShortcutsDialog", "Toggle Fullscreen"), ["F"]),
        Shortcut.of(video, translate("ShortcutsDialog", "Toggle Play/Pause"), [SPACE], ["P"]),
        Shortcut.of(video, translate("ShortcutsDialog", "Seek Backward by 2 Seconds"), [ARROW_LEFT]),
        Shortcut.of(video, translate("ShortcutsDialog", "Seek Forward by 2 Seconds"), [ARROW_RIGHT]),
        Shortcut.of(video, translate("ShortcutsDialog", "Seek Backward by 5 Seconds to Keyframe"), [shift, ARROW_LEFT]),
        Shortcut.of(video, translate("ShortcutsDialog", "Seek Forward by 5 Seconds to Keyframe"), [shift, ARROW_RIGHT]),
        Shortcut.of(
            video,
            translate("ShortcutsDialog", "Seek to Previous Subtitle"),
            [ctrl, ARROW_LEFT],
            note=subtitle_seek_note,
        ),
        Shortcut.of(
            video,
            translate("ShortcutsDialog", "Seek to Next Subtitle"),
            [ctrl, ARROW_RIGHT],
            note=subtitle_seek_note,
        ),
        Shortcut.of(video, translate("ShortcutsDialog", "Decrease Volume"), ["9"]),
        Shortcut.of(video, translate("ShortcutsDialog", "Increase Volume"), ["0"]),
        Shortcut.of(video, translate("ShortcutsDialog", "Toggle Mute"), ["M"]),
        Shortcut.of(video, translate("ShortcutsDialog", "Frame Step Backward"), [","]),
        Shortcut.of(video, translate("ShortcutsDialog", "Frame Step Forward"), ["."]),
        Shortcut.of(video, translate("ShortcutsDialog", "Set/Clear A-B Loop"), ["L"]),
        Shortcut.of(video, translate("ShortcutsDialog", "Cycle Through Subtitle Tracks"), ["J"]),
        Shortcut.of(video, translate("ShortcutsDialog", "Cycle Through Subtitle Tracks Backwards"), [shift, "J"]),
        Shortcut.of(video, translate("ShortcutsDialog", "Cycle Through Audio Tracks"), ["#"]),
        Shortcut.of(video, translate("ShortcutsDialog", "Video Screenshot (Unscaled)"), ["S"]),
        Shortcut.of(video, translate("ShortcutsDialog", "Video Screenshot (Scaled)"), [shift, "S"]),
        Shortcut.of(video, translate("ShortcutsDialog", "Cycle Through Subtitle Render Modes"), ["B"]),
        Shortcut.of(video, translate("ShortcutsDialog", "Toggle Video Statistics"), ["I"]),
    )


class MpvqcShortcutsModelBackend(QAbstractListModel):
    LabelRole = Qt.ItemDataRole.UserRole + 1
    CategoryRole = Qt.ItemDataRole.UserRole + 2
    SequencesRole = Qt.ItemDataRole.UserRole + 3
    SearchTextRole = Qt.ItemDataRole.UserRole + 4
    NoteRole = Qt.ItemDataRole.UserRole + 5

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._shortcuts = build_shortcuts()

    @override
    def rowCount(self, parent: QModelIndex | QPersistentModelIndex | None = None) -> int:
        if parent is not None and parent.isValid():
            return 0
        return len(self._shortcuts)

    @override
    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid() or index.row() >= self.rowCount():
            return None

        shortcut = self._shortcuts[index.row()]

        match role:
            case self.LabelRole:
                return shortcut.label
            case self.CategoryRole:
                return shortcut.category
            case self.SequencesRole:
                return shortcut.sequences
            case self.SearchTextRole:
                return shortcut.search_text
            case self.NoteRole:
                return shortcut.note

        return None

    @override
    def roleNames(self) -> dict[int, QByteArray]:
        return {
            self.LabelRole: QByteArray(b"label"),
            self.CategoryRole: QByteArray(b"category"),
            self.SequencesRole: QByteArray(b"sequences"),
            self.NoteRole: QByteArray(b"note"),
        }


@QmlElement
class MpvqcShortcutsModel(QSortFilterProxyModel):
    queryChanged = Signal(str)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._query = ""
        self._needle = ""
        self.setSourceModel(MpvqcShortcutsModelBackend(self))

    @Property(str, notify=queryChanged)
    def query(self) -> str:
        return self._query

    @query.setter
    def query(self, value: str) -> None:
        if value != self._query:
            self.beginFilterChange()
            self._query = value
            self._needle = value.strip().lower()
            self.endFilterChange(QSortFilterProxyModel.Direction.Rows)
            self.queryChanged.emit(value)

    @override
    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex | QPersistentModelIndex) -> bool:
        if not self._needle:
            return True
        index = self.sourceModel().index(source_row, 0, source_parent)
        return self._needle in index.data(MpvqcShortcutsModelBackend.SearchTextRole)
