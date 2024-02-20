# mpvQC
#
# Copyright (C) 2022 mpvQC developers
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

import inject
from PySide6.QtCore import QLocale, QDateTime
from PySide6.QtCore import QStandardPaths
from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QApplication
from jinja2 import Environment, BaseLoader

from .player import PlayerService
from .settings import SettingsService


class DocumentRendererService:
    _player: PlayerService = inject.attr(PlayerService)
    _settings: SettingsService = inject.attr(SettingsService)

    class Filters:

        @staticmethod
        def as_time(seconds: int):
            hours, remainder = divmod(seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f'{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}'

        @staticmethod
        def as_comment_type(comment_type: str):
            return QApplication.translate("CommentTypes", comment_type)

    def __init__(self):
        self._env = Environment(loader=BaseLoader())
        self._env.filters['as_time'] = self.Filters.as_time
        self._env.filters['as_comment_type'] = self.Filters.as_comment_type

    @property
    def _arguments(self) -> dict:
        write_date = self._settings.writeHeaderDate
        write_generator = self._settings.writeHeaderGenerator
        write_video_path = self._settings.writeHeaderVideoPath
        write_nickname = self._settings.writeHeaderNickname

        date = QLocale(self._settings.language).toString(QDateTime.currentDateTime(), QLocale.FormatType.LongFormat)
        comments = QApplication.instance().find_object(QStandardItemModel, "mpvqcCommentModel").comments()

        return {
            'write_date': write_date,
            'write_generator': write_generator,
            'write_video_path': write_video_path,
            'write_nickname': write_nickname,

            'date': date,
            'generator': f"{QApplication.applicationName()} {QApplication.applicationVersion()}",
            'video_path': str(Path(self._player.path)) if self._player.path else "",
            'nickname': self._settings.nickname,

            'comments': comments,
        }

    def render(self, template: str):
        return self._env.from_string(template).render(**self._arguments)


class DocumentExporterService:
    _player: PlayerService = inject.attr(PlayerService)
    _renderer: DocumentRendererService = inject.attr(DocumentRendererService)
    _settings: SettingsService = inject.attr(SettingsService)

    def generate_file_path_proposal(self) -> Path:
        if video := Path(self._player.path) if self._player.path else None:
            video_directory = str(video.parent)
            video_name = video.stem
        else:
            video_directory = QStandardPaths.writableLocation(QStandardPaths.MoviesLocation)
            video_name = QApplication.translate("FileInteractionDialogs", "untitled")

        if nickname := self._settings.nickname:
            file_name = f"[QC]_{video_name}_{nickname}.txt"
        else:
            file_name = f"[QC]_{video_name}.txt"

        return Path(video_directory).joinpath(file_name).absolute()

    def write_template(self, template: Path, file: Path):
        print("Template", template)
        print("File", file)

        content = self._renderer.render(
            template=template.read_text(encoding='utf-8'),
        )

        print(content)
