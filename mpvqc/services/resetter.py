# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject

from .comments import CommentsService
from .state import StateService


class ResetService:
    _app_state = inject.attr(StateService)
    _comments = inject.attr(CommentsService)

    def reset(self) -> None:
        self._comments.reset()
        self._app_state.reset()
