# mpvQC
#
# Copyright (C) 2024 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pathlib import Path
from typing import Callable

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
            on_video_selected: Callable[[Path or None], None]
    ):
        def pick(video: Path or None):
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
        return (self._settings.import_video_when_video_linked_in_document
                == SettingsService.ImportWhenVideoLinkedInDocument.NEVER)

    @property
    def _user_always_wants_to_import_linked_video(self) -> bool:
        return (self._settings.import_video_when_video_linked_in_document
                == SettingsService.ImportWhenVideoLinkedInDocument.ALWAYS)

    @staticmethod
    def ask_user(video_found_dialog_factory: QQmlComponent, on_do_open: Callable, on_do_not_open: Callable):
        message_box = video_found_dialog_factory.createObject()
        message_box.closed.connect(message_box.deleteLater)
        message_box.accepted.connect(on_do_open)
        message_box.rejected.connect(on_do_not_open)
        message_box.open()
