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

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

import inject
from PySide6.QtCore import QLocale, QDateTime, QCoreApplication, QStandardPaths
from PySide6.QtGui import QStandardItemModel
from jinja2 import Environment, BaseLoader, TemplateSyntaxError, TemplateError

from .application_paths import ApplicationPathsService
from .formatter_time import TimeFormatterService
from .player import PlayerService
from .resource import ResourceService
from .settings import SettingsService


class DocumentRenderService:
    _player: PlayerService = inject.attr(PlayerService)
    _settings: SettingsService = inject.attr(SettingsService)

    class Filters:
        _time_formatter: TimeFormatterService = inject.attr(TimeFormatterService)

        def as_time(self, seconds: int):
            return self._time_formatter.format_time_to_string(seconds, long_format=True)

        @staticmethod
        def as_comment_type(comment_type: str):
            return QCoreApplication.translate("CommentTypes", comment_type)

    def __init__(self):
        self._env = Environment(loader=BaseLoader(), keep_trailing_newline=True)
        self._filters = self.Filters()
        self._env.filters['as_time'] = self._filters.as_time
        self._env.filters['as_comment_type'] = self._filters.as_comment_type

    @property
    def _arguments(self) -> dict:
        write_date = self._settings.writeHeaderDate
        write_generator = self._settings.writeHeaderGenerator
        write_video_path = self._settings.writeHeaderVideoPath
        write_nickname = self._settings.writeHeaderNickname

        date = QLocale(self._settings.language).toString(QDateTime.currentDateTime(), QLocale.FormatType.LongFormat)
        comments = QCoreApplication.instance().find_object(QStandardItemModel, "mpvqcCommentModel").comments()
        generator = f"{QCoreApplication.applicationName()} {QCoreApplication.applicationVersion()}"
        nickname = self._settings.nickname

        if self._player.has_video:
            video_path = f'{Path(self._player.path)}'
            video_name = f'{Path(self._player.path).name}'
        else:
            video_path = ''
            video_name = ''

        return {
            'write_date': write_date,
            'write_generator': write_generator,
            'write_video_path': write_video_path,
            'write_nickname': write_nickname,

            'date': date,
            'generator': generator,
            'video_path': video_path,
            'video_name': video_name,
            'nickname': nickname,

            'comments': comments,
        }

    def render(self, template: str):
        return self._env.from_string(template).render(**self._arguments)


class DocumentBackupService:
    _paths: ApplicationPathsService = inject.attr(ApplicationPathsService)
    _player: PlayerService = inject.attr(PlayerService)
    _renderer: DocumentRenderService = inject.attr(DocumentRenderService)
    _resources: ResourceService = inject.attr(ResourceService)

    @property
    def _video_name(self) -> str:
        if self._player.has_video:
            return Path(self._player.path).name
        else:
            return QCoreApplication.translate("FileInteractionDialogs", "untitled")

    @property
    def _content(self) -> str:
        return self._renderer.render(self._resources.backup_template)

    def backup(self) -> None:
        now = datetime.now()

        zip_name = f'{now:%Y-%m}.zip'
        zip_path = self._paths.dir_backup / zip_name
        zip_mode = 'a' if zip_path.exists() else 'w'

        file_name = f'{now:%Y-%m-%d_%H-%M-%S}_{self._video_name}.txt'

        # noinspection PyTypeChecker
        with ZipFile(zip_path, mode=zip_mode, compression=ZIP_DEFLATED) as file:
            file.writestr(file_name, self._content)


class DocumentExportService:
    _player: PlayerService = inject.attr(PlayerService)
    _renderer: DocumentRenderService = inject.attr(DocumentRenderService)
    _settings: SettingsService = inject.attr(SettingsService)
    _resources: ResourceService = inject.attr(ResourceService)

    @dataclass
    class ExportError:
        message: str
        line_nr: int or None

    def generate_file_path_proposal(self) -> Path:
        if video := Path(self._player.path) if self._player.path else None:
            video_directory = str(video.parent)
            video_name = video.stem
        else:
            video_directory = QStandardPaths.writableLocation(QStandardPaths.MoviesLocation)
            video_name = QCoreApplication.translate("FileInteractionDialogs", "untitled")

        if nickname := self._settings.nickname:
            file_name = f"[QC]_{video_name}_{nickname}.txt"
        else:
            file_name = f"[QC]_{video_name}.txt"

        return Path(video_directory).joinpath(file_name).absolute()

    def export(self, file: Path, template: Path) -> ExportError or None:
        user_template = template.read_text(encoding='utf-8')

        try:
            content = self._renderer.render(user_template)
        except TemplateSyntaxError as e:
            return self.ExportError(e.message, line_nr=e.lineno)
        except TemplateError as e:
            return self.ExportError(e.message, line_nr=None)

        file.write_text(content, encoding='utf-8', newline='\n')

    def save(self, file: Path) -> None:
        export_template = self._resources.default_export_template
        content = self._renderer.render(export_template)

        file.write_text(content, encoding='utf-8', newline='\n')
