# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

import inject
from PySide6.QtCore import QCoreApplication, QDateTime

from mpvqc.services.build_info import BuildInfoService
from mpvqc.services.comments import CommentsService
from mpvqc.services.formatter_time import TimeFormatterService
from mpvqc.services.player import PlayerService
from mpvqc.services.settings import SettingsService


class DocumentRenderService:
    _player = inject.attr(PlayerService)
    _settings = inject.attr(SettingsService)
    _build_info = inject.attr(BuildInfoService)
    _comments_service = inject.attr(CommentsService)

    class Filters:
        _time_formatter = inject.attr(TimeFormatterService)

        def as_time(self, seconds: int) -> str:
            return self._time_formatter.format_time_to_string(seconds, long_format=True)

        @staticmethod
        def as_comment_type(comment_type: str) -> str:
            return QCoreApplication.translate("CommentTypes", comment_type)

    def __init__(self) -> None:
        from jinja2 import BaseLoader, Environment

        self._env = Environment(loader=BaseLoader(), keep_trailing_newline=True)  # noqa: S701
        self._filters = self.Filters()
        self._env.filters["as_time"] = self._filters.as_time
        self._env.filters["as_comment_type"] = self._filters.as_comment_type

    @property
    def _arguments(self) -> dict:
        if raw_path := self._player.path:
            path = Path(raw_path)
            video_path = str(path)  # use platform-specific path separators
            video_name = path.name
        else:
            video_path = ""
            video_name = ""

        return {
            "write_date": self._settings.write_header_date,
            "write_generator": self._settings.write_header_generator,
            "write_nickname": self._settings.write_header_nickname,
            "write_video_path": self._settings.write_header_video_path,
            "write_subtitle_paths": self._settings.write_header_subtitles,
            "date": QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm"),
            "generator": f"{self._build_info.name} {self._build_info.version}",
            "nickname": self._settings.nickname,
            "video_path": video_path,
            "video_name": video_name,
            "subtitles": self._player.external_subtitles,
            "comments": [
                {**c, "time": c["time"] // TimeFormatterService.MILLISECONDS_PER_SECOND}
                for c in self._comments_service.comments()
            ],
        }

    def render(self, template: str) -> str:
        return self._env.from_string(template).render(**self._arguments)
