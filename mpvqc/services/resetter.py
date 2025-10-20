# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import QObject, Signal

from .state import StateService


class ResetService(QObject):
    _app_state: StateService = inject.attr(StateService)

    perform_reset = Signal()

    def reset(self) -> None:
        self.perform_reset.emit()
        self._app_state.reset()
