# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, assert_never, override

from PySide6.QtCore import Property, QAbstractItemModel, QAbstractListModel, QByteArray, QObject, Qt, Signal, Slot
from PySide6.QtQml import QmlElement, QmlUncreatable

from mpvqc.services.importer import subtitles

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Any

    from PySide6.QtCore import QModelIndex, QPersistentModelIndex


QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@dataclass(slots=True)
class _SubtitleEntry:
    path: Path
    checked: bool


class MpvqcImportSubtitlesModel(QAbstractListModel):
    FilenameRole = Qt.ItemDataRole.UserRole + 1
    IsCheckedRole = Qt.ItemDataRole.UserRole + 2

    def __init__(self, subtitles: tuple[Path, ...]) -> None:
        super().__init__()
        self._items: list[_SubtitleEntry] = [_SubtitleEntry(path=subtitle, checked=True) for subtitle in subtitles]

    @override
    def rowCount(self, parent: QModelIndex | QPersistentModelIndex | None = None) -> int:
        return len(self._items)

    @override
    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid() or index.row() >= self.rowCount():
            return None

        item = self._items[index.row()]

        match role:
            case self.FilenameRole:
                return item.path.name
            case self.IsCheckedRole:
                return item.checked

        return None

    @override
    def roleNames(self) -> dict[int, QByteArray]:
        return {
            self.FilenameRole: QByteArray(b"filename"),
            self.IsCheckedRole: QByteArray(b"isChecked"),
        }

    def toggle(self, index: int) -> None:
        if not 0 <= index < len(self._items):
            return

        self._items[index].checked = not self._items[index].checked

        model_index = self.index(index, 0)
        self.dataChanged.emit(model_index, model_index, [self.IsCheckedRole])

    def set_all_checked(self, value: bool) -> None:
        if not self._items:
            return

        for item in self._items:
            item.checked = value

        first_index = self.index(0, 0)
        last_index = self.index(len(self._items) - 1, 0)
        self.dataChanged.emit(first_index, last_index, [self.IsCheckedRole])

    @property
    def checked_paths(self) -> tuple[Path, ...]:
        return tuple(item.path for item in self._items if item.checked)

    @property
    def checked_count(self) -> int:
        return sum(1 for item in self._items if item.checked)


@QmlElement
@QmlUncreatable("constructed by MpvqcImportWizardViewModel")
class MpvqcImportWizardSubtitlesStepViewModel(QObject):
    selectAllTriStateChanged = Signal(int)

    def __init__(self, parent: QObject, inputs: subtitles.Unresolved) -> None:
        super().__init__(parent)
        self._subtitles = MpvqcImportSubtitlesModel(inputs.candidates)
        self._subtitles.dataChanged.connect(self._emit_tri_state_changed)

    @Property(QAbstractItemModel, constant=True, final=True)
    def subtitles(self) -> MpvqcImportSubtitlesModel:
        return self._subtitles

    @Property(int, notify=selectAllTriStateChanged, final=True)
    def selectAllTriState(self) -> int:
        total = self._subtitles.rowCount()
        if total == 0:
            return Qt.CheckState.Checked.value

        checked = self._subtitles.checked_count
        if checked == 0:
            return Qt.CheckState.Unchecked.value
        if checked == total:
            return Qt.CheckState.Checked.value
        return Qt.CheckState.PartiallyChecked.value

    @Slot(int)
    def toggle(self, index: int) -> None:
        self._subtitles.toggle(index)

    @Slot()
    def toggleSelectAll(self) -> None:
        all_checked = self.selectAllTriState == Qt.CheckState.Checked.value
        self._subtitles.set_all_checked(not all_checked)

    @property
    def checked_paths(self) -> tuple[Path, ...]:
        return self._subtitles.checked_paths

    @Slot()
    def _emit_tri_state_changed(self) -> None:
        self.selectAllTriStateChanged.emit(self.selectAllTriState)


def build_subtitles_step(parent: QObject, concern: subtitles.Concern) -> MpvqcImportWizardSubtitlesStepViewModel | None:
    if isinstance(concern, subtitles.Unresolved):
        return MpvqcImportWizardSubtitlesStepViewModel(parent, concern)
    return None


def resolve_subtitles(
    subtitles_step: MpvqcImportWizardSubtitlesStepViewModel | None,
    concern: subtitles.Concern,
) -> subtitles.Resolved:
    match concern:
        case subtitles.Load() | subtitles.Skip():
            return concern
        case subtitles.Unresolved() if subtitles_step is not None:
            checked = subtitles_step.checked_paths
            return subtitles.Load(paths=checked) if checked else subtitles.Skip()
        case subtitles.Unresolved():
            msg = "subtitles.Unresolved reached commit without a subtitles step view-model"
            raise RuntimeError(msg)
        case _:
            assert_never(concern)
