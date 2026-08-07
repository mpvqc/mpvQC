# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, assert_never

from PySide6.QtCore import Property, QCoreApplication, QObject, Signal, Slot
from PySide6.QtQml import QmlElement, QmlUncreatable

from mpvqc.importing.domain import NotAsked
from mpvqc.importing.enums import MpvqcImportWizardNavigationDirection

from .wizard_state import (
    ErrorsStep,
    PrimaryAction,
    PrimaryLabel,
    SessionStep,
    SubtitlesStep,
    VideoStep,
    make_wizard_state,
)
from .wizard_steps import (
    MpvqcImportWizardErrorsStepViewModel,
    MpvqcImportWizardSessionStepViewModel,
    MpvqcImportWizardSubtitlesStepViewModel,
    MpvqcImportWizardVideoStepViewModel,
)

if TYPE_CHECKING:
    from mpvqc.importing.domain import PendingImport

    from .wizard_state import WizardState
    from .wizard_steps import WizardStepViewModel


QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
@QmlUncreatable("constructed by MpvqcImportWizardRequestRelayViewModel with a PendingImport")
class MpvqcImportWizardViewModel(QObject):
    currentStepChanged = Signal()
    navigated = Signal(int)
    acceptRequested = Signal()
    rejectRequested = Signal()

    def __init__(self, parent: QObject | None, pending: PendingImport) -> None:
        super().__init__(parent)
        self._pending = pending
        self._state = make_wizard_state(pending.plan)

        self._session_step: MpvqcImportWizardSessionStepViewModel | None = None
        self._video_step: MpvqcImportWizardVideoStepViewModel | None = None
        self._subtitles_step: MpvqcImportWizardSubtitlesStepViewModel | None = None

        step_view_models: list[WizardStepViewModel] = []
        for step in self._state.steps:
            match step:
                case ErrorsStep():
                    step_view_models.append(MpvqcImportWizardErrorsStepViewModel(self, step.errors))
                case SessionStep():
                    self._session_step = MpvqcImportWizardSessionStepViewModel(self, step.session)
                    step_view_models.append(self._session_step)
                case VideoStep():
                    self._video_step = MpvqcImportWizardVideoStepViewModel(self, step.video)
                    step_view_models.append(self._video_step)
                case SubtitlesStep():
                    self._subtitles_step = MpvqcImportWizardSubtitlesStepViewModel(self, step.subtitles)
                    step_view_models.append(self._subtitles_step)
                case _:
                    assert_never(step)

        self._steps: tuple[WizardStepViewModel, ...] = tuple(step_view_models)

    @Property(int, notify=currentStepChanged, final=True)
    def currentStepIndex(self) -> int:
        return self._state.current_index

    @currentStepIndex.setter
    def currentStepIndex(self, value: int) -> None:
        self._move_to(self._state.jump_to(value))

    @Property(list, constant=True, final=True)
    def steps(self) -> list[WizardStepViewModel]:
        return list(self._steps)

    @Property(str, constant=True, final=True)
    def title(self) -> str:
        if self._state.close_only:
            #: Title of the import wizard dialog when no valid content can be imported
            return QCoreApplication.translate("ImportWizardDialog", "Import Error")
        #: Title of the import wizard dialog
        return QCoreApplication.translate("ImportWizardDialog", "Confirm Import")

    @Property(str, notify=currentStepChanged, final=True)
    def primaryLabel(self) -> str:
        return self._primary_label_text(self._state.footer.primary_label)

    @Property(bool, notify=currentStepChanged, final=True)
    def showBack(self) -> bool:
        return self._state.footer.show_back

    @Property(bool, notify=currentStepChanged, final=True)
    def showCancel(self) -> bool:
        return self._state.footer.show_cancel

    @Property(bool, constant=True, final=True)
    def showStepIndicator(self) -> bool:
        return self._state.multi_step

    @Slot()
    def next(self) -> None:
        self._move_to(self._state.advance())

    @Slot()
    def back(self) -> None:
        self._move_to(self._state.back())

    @Slot()
    def primaryClicked(self) -> None:
        action = self._state.footer.primary_action
        match action:
            case PrimaryAction.ADVANCE:
                self.next()
            case PrimaryAction.ACCEPT:
                self.acceptRequested.emit()
            case PrimaryAction.REJECT:
                self.rejectRequested.emit()
            case _:
                assert_never(action)

    @Slot()
    def cancelClicked(self) -> None:
        self.rejectRequested.emit()

    @Slot()
    def finish(self) -> None:
        self._pending.finish(
            session=self._session_step.resolved if self._session_step is not None else NotAsked(),
            video=self._video_step.resolved if self._video_step is not None else NotAsked(),
            subtitles=self._subtitles_step.resolved if self._subtitles_step is not None else NotAsked(),
        )

    @Slot()
    def dismiss(self) -> None:
        self._pending.dismiss()

    def _move_to(self, state: WizardState) -> None:
        if state.current_index == self._state.current_index:
            return
        direction = (
            MpvqcImportWizardNavigationDirection.NavigationDirection.FORWARD
            if state.current_index > self._state.current_index
            else MpvqcImportWizardNavigationDirection.NavigationDirection.BACK
        )
        self._state = state
        self.currentStepChanged.emit()
        self.navigated.emit(direction.value)

    @staticmethod
    def _primary_label_text(label: PrimaryLabel) -> str:
        match label:
            case PrimaryLabel.CLOSE:
                #: Primary button when the wizard only lists unreadable documents
                return QCoreApplication.translate("ImportWizardDialog", "Close")
            case PrimaryLabel.CONFIRM:
                #: Primary button on the last step when nothing valid has been resolved yet
                return QCoreApplication.translate("ImportWizardDialog", "Confirm")
            case PrimaryLabel.CONFIRM_IMPORT:
                #: Primary button finalizing the import on the last wizard step
                return QCoreApplication.translate("ImportWizardDialog", "Confirm import")
            case PrimaryLabel.NEXT:
                #: Primary button advancing to the next wizard step
                return QCoreApplication.translate("ImportWizardDialog", "Next")
            case _:
                assert_never(label)
