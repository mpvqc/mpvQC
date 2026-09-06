# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject

from mpvqc.session import SessionService

from .service import CommentsService


class ResetService:
    _comments = inject.attr(CommentsService)
    _session = inject.attr(SessionService)

    def reset(self) -> None:
        self._comments.reset()
        self._session.record_reset()
