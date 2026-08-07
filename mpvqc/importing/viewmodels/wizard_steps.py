# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import assert_never

from PySide6.QtCore import Property, QAbstractItemModel, QCoreApplication, QObject, Qt, Signal, Slot
from PySide6.QtQml import QmlElement, QmlUncreatable

from mpvqc.importing.domain import (
    ErrorsPresent,
    SessionMerge,
    SessionReplace,
    SessionResolved,
    SessionUnresolved,
    SubtitlesLoad,
    SubtitlesResolved,
    SubtitlesSkip,
    SubtitlesUnresolved,
    VideoLoad,
    VideoResolved,
    VideoSkip,
    VideoUnresolved,
)
from mpvqc.importing.enums import MpvqcImportWizardSessionMode, MpvqcImportWizardStepKind
from mpvqc.importing.models import ErrorsModel, SubtitlesModel, VideosModel

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
@QmlUncreatable("constructed by MpvqcImportWizardViewModel")
class MpvqcImportWizardErrorsStepViewModel(QObject):
    def __init__(self, parent: QObject, inputs: ErrorsPresent) -> None:
        super().__init__(parent)
        self._documents = ErrorsModel(inputs.rejected_documents)

    @Property(int, constant=True, final=True)
    def kind(self) -> int:
        return MpvqcImportWizardStepKind.StepKind.ERRORS

    @Property(str, constant=True, final=True)
    def indicatorLabel(self) -> str:
        #: Step indicator label for the errors step
        return QCoreApplication.translate("ImportWizardDialog", "Errors")

    @Property(QAbstractItemModel, constant=True, final=True)
    def documents(self) -> ErrorsModel:
        return self._documents


@QmlElement
@QmlUncreatable("constructed by MpvqcImportWizardViewModel")
class MpvqcImportWizardSessionStepViewModel(QObject):
    modeChanged = Signal(int)

    def __init__(self, parent: QObject, inputs: SessionUnresolved) -> None:
        super().__init__(parent)
        self._incoming_comment_count = inputs.incoming_comment_count
        self._resolved: SessionResolved = SessionMerge()

    @Property(int, constant=True, final=True)
    def kind(self) -> int:
        return MpvqcImportWizardStepKind.StepKind.SESSION

    @Property(str, constant=True, final=True)
    def indicatorLabel(self) -> str:
        #: Step indicator label for the session step
        return QCoreApplication.translate("ImportWizardDialog", "Session")

    @property
    def resolved(self) -> SessionResolved:
        return self._resolved

    @resolved.setter
    def resolved(self, value: SessionResolved) -> None:
        if self._resolved == value:
            return
        self._resolved = value
        self.modeChanged.emit(_to_mode(value).value)

    @Property(int, constant=True, final=True)
    def incomingCommentCount(self) -> int:
        return self._incoming_comment_count

    @Property(int, notify=modeChanged, final=True)
    def mode(self) -> int:
        return _to_mode(self._resolved).value

    @mode.setter
    def mode(self, value: int) -> None:
        try:
            self.resolved = _to_resolved(MpvqcImportWizardSessionMode.SessionMode(value))
        except ValueError:
            return


def _to_mode(resolved: SessionResolved) -> MpvqcImportWizardSessionMode.SessionMode:
    match resolved:
        case SessionMerge():
            return MpvqcImportWizardSessionMode.SessionMode.MERGE
        case SessionReplace():
            return MpvqcImportWizardSessionMode.SessionMode.REPLACE
        case _:
            assert_never(resolved)


def _to_resolved(mode: MpvqcImportWizardSessionMode.SessionMode) -> SessionResolved:
    match mode:
        case MpvqcImportWizardSessionMode.SessionMode.MERGE:
            return SessionMerge()
        case MpvqcImportWizardSessionMode.SessionMode.REPLACE:
            return SessionReplace()
        case _:
            assert_never(mode)


@QmlElement
@QmlUncreatable("constructed by MpvqcImportWizardViewModel")
class MpvqcImportWizardVideoStepViewModel(QObject):
    selectedIndexChanged = Signal(int)

    def __init__(self, parent: QObject, inputs: VideoUnresolved) -> None:
        super().__init__(parent)
        self._candidates = VideosModel(inputs.candidates)
        self._selected_index = 0

    @Property(int, constant=True, final=True)
    def kind(self) -> int:
        return MpvqcImportWizardStepKind.StepKind.VIDEO

    @Property(str, constant=True, final=True)
    def indicatorLabel(self) -> str:
        #: Step indicator label for the video step
        return QCoreApplication.translate("ImportWizardDialog", "Video")

    @Property(QAbstractItemModel, constant=True, final=True)
    def candidates(self) -> VideosModel:
        return self._candidates

    @Property(int, notify=selectedIndexChanged, final=True)
    def selectedIndex(self) -> int:
        return self._selected_index

    @selectedIndex.setter
    def selectedIndex(self, value: int) -> None:
        if self._selected_index == value:
            return
        self._selected_index = value
        self.selectedIndexChanged.emit(value)

    @property
    def resolved(self) -> VideoResolved:
        if path := self._candidates.path_at(self._selected_index):
            return VideoLoad(path=path)
        return VideoSkip()


@QmlElement
@QmlUncreatable("constructed by MpvqcImportWizardViewModel")
class MpvqcImportWizardSubtitlesStepViewModel(QObject):
    selectAllTriStateChanged = Signal(int)

    def __init__(self, parent: QObject, inputs: SubtitlesUnresolved) -> None:
        super().__init__(parent)
        self._subtitles = SubtitlesModel(inputs.candidates)
        self._subtitles.dataChanged.connect(self._emit_tri_state_changed)

    @Property(int, constant=True, final=True)
    def kind(self) -> int:
        return MpvqcImportWizardStepKind.StepKind.SUBTITLES

    @Property(str, constant=True, final=True)
    def indicatorLabel(self) -> str:
        #: Step indicator label for the subtitles step
        return QCoreApplication.translate("ImportWizardDialog", "Subtitles")

    @Property(QAbstractItemModel, constant=True, final=True)
    def subtitles(self) -> SubtitlesModel:
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
    def resolved(self) -> SubtitlesResolved:
        checked = self._subtitles.checked_paths
        return SubtitlesLoad(paths=checked) if checked else SubtitlesSkip()

    @Slot()
    def _emit_tri_state_changed(self) -> None:
        self.selectAllTriStateChanged.emit(self.selectAllTriState)


type WizardStepViewModel = (
    MpvqcImportWizardErrorsStepViewModel
    | MpvqcImportWizardSessionStepViewModel
    | MpvqcImportWizardVideoStepViewModel
    | MpvqcImportWizardSubtitlesStepViewModel
)
