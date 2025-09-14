# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Callable
from pathlib import Path

import inject
from PySide6.QtQml import QQmlComponent

from .settings import SettingsService


class VideoSelectorService:
    _settings: SettingsService = inject.attr(SettingsService)

    def select_video_from(
        self,
        existing_videos_dropped: list[Path],
        existing_videos_from_documents: list[Path],
        video_found_dialog_factory: QQmlComponent,
        on_video_selected: Callable[[Path | None], None],
    ):
        def pick(video: Path | None):
            on_video_selected(video)

        if existing_videos_dropped:
            return pick(existing_videos_dropped[0])
        if self._user_never_wants_to_import_linked_video:
            return pick(None)
        if not existing_videos_from_documents:
            return pick(None)
        if self._user_always_wants_to_import_linked_video:
            return pick(existing_videos_from_documents[0])

        return self.ask_user(
            video_found_dialog_factory,
            on_do_open=lambda: pick(existing_videos_from_documents[0]),
            on_do_not_open=lambda: pick(None),
        )

    @property
    def _user_never_wants_to_import_linked_video(self) -> bool:
        return (
            self._settings.import_video_when_video_linked_in_document
            == SettingsService.ImportWhenVideoLinkedInDocument.NEVER
        )

    @property
    def _user_always_wants_to_import_linked_video(self) -> bool:
        return (
            self._settings.import_video_when_video_linked_in_document
            == SettingsService.ImportWhenVideoLinkedInDocument.ALWAYS
        )

    @staticmethod
    def ask_user(video_found_dialog_factory: QQmlComponent, on_do_open: Callable, on_do_not_open: Callable):
        message_box = video_found_dialog_factory.createObject()
        message_box.closed.connect(message_box.deleteLater)
        message_box.accepted.connect(on_do_open)
        message_box.rejected.connect(on_do_not_open)
        message_box.open()
