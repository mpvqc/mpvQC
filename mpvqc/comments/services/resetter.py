# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject

from mpvqc.services import StateService

from .service import CommentsService


class ResetService:
    _comments = inject.attr(CommentsService)
    _app_state = inject.attr(StateService)

    def reset(self) -> None:
        self._comments.reset()
        self._app_state.record_reset()
