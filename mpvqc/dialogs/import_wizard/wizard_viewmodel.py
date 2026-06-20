# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, assert_never

import inject
from PySide6.QtCore import Property, QCoreApplication, QObject, Signal, Slot
from PySide6.QtQml import QmlElement, QmlUncreatable

from mpvqc.enums import StepKind
from mpvqc.services import ImporterService
from mpvqc.services.importer import FinishedPlan

from .footer_policy import PrimaryAction, WizardFooterPolicy
from .steps import (
    MpvqcImportWizardErrorsStepViewModel,
    MpvqcImportWizardSessionStepViewModel,
    MpvqcImportWizardSubtitlesStepViewModel,
    MpvqcImportWizardVideoStepViewModel,
    build_errors_step,
    build_session_step,
    build_subtitles_step,
    build_video_step,
    resolve_session,
    resolve_subtitles,
    resolve_video,
)
from .wizard_helpers import compute_steps, has_valid_content

if TYPE_CHECKING:
    from mpvqc.services.importer import UnfinishedPlan


QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
@QmlUncreatable("constructed by MpvqcDialogLoaderViewModel with an UnfinishedPlan")
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
        self._footer = WizardFooterPolicy(unfinished_plan, self._steps)

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
        if self._steps == (StepKind.ERRORS,) and not has_valid_content(self._unfinished_plan):
            #: Title of the import wizard dialog when no valid content can be imported
            return QCoreApplication.translate("ImportWizardDialog", "Import Error")
        #: Title of the import wizard dialog
        return QCoreApplication.translate("ImportWizardDialog", "Confirm Import")

    @Property(str, notify=currentStepChanged, final=True)
    def primaryLabel(self) -> str:
        return self._footer.state_for(self._current_step_index).primary_label

    @Property(bool, notify=currentStepChanged, final=True)
    def showBack(self) -> bool:
        return self._footer.state_for(self._current_step_index).show_back

    @Property(bool, notify=currentStepChanged, final=True)
    def showCancel(self) -> bool:
        return self._footer.state_for(self._current_step_index).show_cancel

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
        action = self._footer.state_for(self._current_step_index).primary_action
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
        plan = FinishedPlan(
            comments=self._unfinished_plan.comments,
            session=resolve_session(self._session_step, self._unfinished_plan.session),
            video=resolve_video(self._video_step, self._unfinished_plan.video),
            subtitles=resolve_subtitles(self._subtitles_step, self._unfinished_plan.subtitles),
        )
        self._importer.execute(plan)
