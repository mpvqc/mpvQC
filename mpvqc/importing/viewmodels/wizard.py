# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, assert_never

import inject
from PySide6.QtCore import Property, QCoreApplication, QObject, Signal, Slot
from PySide6.QtQml import QmlElement, QmlUncreatable

from mpvqc.importing.domain import (
    PrimaryAction,
    PrimaryLabel,
    compute_footer_state,
    compute_steps,
    finish_plan,
    is_close_only,
)
from mpvqc.importing.services import ImporterService

from .steps import (
    MpvqcImportWizardErrorsStepViewModel,
    MpvqcImportWizardSessionStepViewModel,
    MpvqcImportWizardSubtitlesStepViewModel,
    MpvqcImportWizardVideoStepViewModel,
    build_errors_step,
    build_session_step,
    build_subtitles_step,
    build_video_step,
)

if TYPE_CHECKING:
    from mpvqc.importing.domain import FooterState, UnfinishedPlan


QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
@QmlUncreatable("constructed by MpvqcImportWizardRequestRelayViewModel with an UnfinishedPlan")
class MpvqcImportWizardViewModel(QObject):
    _importer = inject.attr(ImporterService)

    currentStepChanged = Signal()
    acceptRequested = Signal()
    rejectRequested = Signal()

    def __init__(self, parent: QObject | None, unfinished_plan: UnfinishedPlan) -> None:
        super().__init__(parent)
        self._unfinished_plan = unfinished_plan
        self._current_step_index = 0

        self._steps = compute_steps(unfinished_plan)
        self._close_only = is_close_only(unfinished_plan, self._steps)

        self._errors_step = build_errors_step(self, unfinished_plan.errors)
        self._session_step = build_session_step(self, unfinished_plan.session)
        self._video_step = build_video_step(self, unfinished_plan.video)
        self._subtitles_step = build_subtitles_step(self, unfinished_plan.subtitles)

    @Property(int, notify=currentStepChanged, final=True)
    def currentStepIndex(self) -> int:
        return self._current_step_index

    @currentStepIndex.setter
    def currentStepIndex(self, value: int) -> None:
        if 0 <= value < len(self._steps) and value != self._current_step_index:
            self._current_step_index = value
            self.currentStepChanged.emit()

    @Property(int, notify=currentStepChanged, final=True)
    def currentStepKind(self) -> int:
        return int(self._steps[self._current_step_index])

    @Property(list, constant=True, final=True)
    def stepKinds(self) -> list[int]:
        return [int(s) for s in self._steps]

    @Property(str, constant=True, final=True)
    def title(self) -> str:
        if self._close_only:
            #: Title of the import wizard dialog when no valid content can be imported
            return QCoreApplication.translate("ImportWizardDialog", "Import Error")
        #: Title of the import wizard dialog
        return QCoreApplication.translate("ImportWizardDialog", "Confirm Import")

    @Property(str, notify=currentStepChanged, final=True)
    def primaryLabel(self) -> str:
        return self._primary_label_text(self._footer_state().primary_label)

    @Property(bool, notify=currentStepChanged, final=True)
    def showBack(self) -> bool:
        return self._footer_state().show_back

    @Property(bool, notify=currentStepChanged, final=True)
    def showCancel(self) -> bool:
        return self._footer_state().show_cancel

    @Property(MpvqcImportWizardErrorsStepViewModel, constant=True, final=True)
    def errorsStepViewModel(self) -> MpvqcImportWizardErrorsStepViewModel | None:
        return self._errors_step

    @Property(MpvqcImportWizardSessionStepViewModel, constant=True, final=True)
    def sessionStepViewModel(self) -> MpvqcImportWizardSessionStepViewModel | None:
        return self._session_step

    @Property(MpvqcImportWizardVideoStepViewModel, constant=True, final=True)
    def videoStepViewModel(self) -> MpvqcImportWizardVideoStepViewModel | None:
        return self._video_step

    @Property(MpvqcImportWizardSubtitlesStepViewModel, constant=True, final=True)
    def subtitlesStepViewModel(self) -> MpvqcImportWizardSubtitlesStepViewModel | None:
        return self._subtitles_step

    @Slot()
    def next(self) -> None:
        if self._current_step_index < len(self._steps) - 1:
            self._current_step_index += 1
            self.currentStepChanged.emit()

    @Slot()
    def back(self) -> None:
        if self._current_step_index > 0:
            self._current_step_index -= 1
            self.currentStepChanged.emit()

    @Slot()
    def primaryClicked(self) -> None:
        action = self._footer_state().primary_action
        match action:
            case PrimaryAction.ADVANCE:
                self.next()
            case PrimaryAction.ACCEPT:
                self._commit()
                self.acceptRequested.emit()
            case PrimaryAction.REJECT:
                self.rejectRequested.emit()
            case _:
                assert_never(action)

    @Slot()
    def cancelClicked(self) -> None:
        self.rejectRequested.emit()

    def _commit(self) -> None:
        plan = finish_plan(
            self._unfinished_plan,
            session=self._session_step.resolved if self._session_step is not None else None,
            video=self._video_step.resolved if self._video_step is not None else None,
            subtitles=self._subtitles_step.resolved if self._subtitles_step is not None else None,
        )
        self._importer.execute(plan)

    def _footer_state(self) -> FooterState:
        return compute_footer_state(self._unfinished_plan, self._steps, self._current_step_index)

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
