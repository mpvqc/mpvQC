# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import inject


def bindings(binder: inject.Binder) -> None:
    import inject
    from PySide6.QtCore import QSettings

    from mpvqc.comments.models import CommentStore
    from mpvqc.comments.services import (
        CommentsService,
        CommentsSettingsService,
        CommentTypesPolicyService,
        ResetService,
        TimeFormatPolicyService,
    )

    def comments_service() -> CommentsService:
        return CommentsService(inject.instance(CommentStore))

    def comments_settings_service() -> CommentsSettingsService:
        return CommentsSettingsService(inject.instance(QSettings))

    binder.bind_to_constructor(CommentStore, CommentStore)
    binder.bind_to_constructor(CommentsService, comments_service)
    binder.bind_to_constructor(CommentsSettingsService, comments_settings_service)
    binder.bind_to_constructor(CommentTypesPolicyService, CommentTypesPolicyService)
    binder.bind_to_constructor(ResetService, ResetService)
    binder.bind_to_constructor(TimeFormatPolicyService, TimeFormatPolicyService)


def register_qml_types() -> None:
    import mpvqc.comments.viewmodels  # ruff: ignore[unused-import]
