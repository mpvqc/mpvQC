# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, auto
from typing import TYPE_CHECKING

from PySide6.QtCore import QCoreApplication

from mpvqc.enums import StepKind

from .wizard_helpers import has_valid_content

if TYPE_CHECKING:
    from mpvqc.services.importer import UnfinishedPlan


class PrimaryAction(IntEnum):
    ADVANCE = auto()
    ACCEPT = auto()
    REJECT = auto()


@dataclass(frozen=True, slots=True)
class FooterState:
    primary_label: str
    primary_action: PrimaryAction
    show_cancel: bool
    show_back: bool


class WizardDialogPolicy:
    def __init__(self, plan: UnfinishedPlan, steps: tuple[StepKind, ...]) -> None:
        self._steps = steps
        self._has_valid_content = has_valid_content(plan)
        self._close_only = steps == (StepKind.ERRORS,) and not self._has_valid_content

    @property
    def title(self) -> str:
        if self._close_only:
            #: Title of the import wizard dialog when no valid content can be imported
            return QCoreApplication.translate("ImportWizardDialog", "Import Error")
        #: Title of the import wizard dialog
        return QCoreApplication.translate("ImportWizardDialog", "Confirm Import")

    def state_for(self, current_index: int) -> FooterState:
        is_last = current_index == len(self._steps) - 1

        if self._close_only:
            #: Primary button when the wizard only lists unreadable documents
            label = QCoreApplication.translate("ImportWizardDialog", "Close")
            action = PrimaryAction.REJECT
        elif is_last and not self._has_valid_content:
            #: Primary button on the last step when nothing valid has been resolved yet
            label = QCoreApplication.translate("ImportWizardDialog", "Confirm")
            action = PrimaryAction.ACCEPT
        elif is_last:
            #: Primary button finalizing the import on the last wizard step
            label = QCoreApplication.translate("ImportWizardDialog", "Confirm import")
            action = PrimaryAction.ACCEPT
        else:
            #: Primary button advancing to the next wizard step
            label = QCoreApplication.translate("ImportWizardDialog", "Next")
            action = PrimaryAction.ADVANCE

        return FooterState(
            primary_label=label,
            primary_action=action,
            show_cancel=self._has_valid_content or len(self._steps) > 1,
            show_back=current_index > 0,
        )
