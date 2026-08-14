# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

import inject

from .state import StateService

if TYPE_CHECKING:
    # A runtime import would close a cycle: the comments slice imports this package back.
    from mpvqc.comments.services import CommentsService


class ResetService:
    _app_state = inject.attr(StateService)

    def __init__(self, comments: CommentsService) -> None:
        self._comments = comments

    def reset(self) -> None:
        self._comments.reset()
        self._app_state.record_reset()
