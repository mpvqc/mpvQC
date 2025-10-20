# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import inject
from jinja2 import BaseLoader, Environment, TemplateError, TemplateSyntaxError
from PySide6.QtCore import QCoreApplication, QDateTime, QLocale, QObject, QStandardPaths, Signal
from PySide6.QtGui import QStandardItemModel

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
        self._env = Environment(loader=BaseLoader(), keep_trailing_newline=True)  # noqa: S701
        self._filters = self.Filters()
        self._env.filters["as_time"] = self._filters.as_time
        self._env.filters["as_comment_type"] = self._filters.as_comment_type

    @property
    def _arguments(self) -> dict:
        write_date = self._settings.write_header_date
        write_generator = self._settings.write_header_generator
        write_video_path = self._settings.write_header_video_path
        write_nickname = self._settings.write_header_nickname
        write_subtitle_paths = self._settings.write_header_subtitles

        date = QLocale(self._settings.language).toString(QDateTime.currentDateTime(), QLocale.FormatType.LongFormat)
        comments = QCoreApplication.instance().find_object(QStandardItemModel, "mpvqcCommentModel").comments()
        generator = f"{QCoreApplication.applicationName()} {QCoreApplication.applicationVersion()}"
        nickname = self._settings.nickname
        subtitles = [str(sub) for sub in self._player.external_subtitles]

        if self._player.has_video:
            video_path = f"{Path(self._player.path)}"
            video_name = f"{Path(self._player.path).name}"
        else:
            video_path = ""
            video_name = ""

        return {
            "write_date": write_date,
            "write_generator": write_generator,
            "write_nickname": write_nickname,
            "write_video_path": write_video_path,
            "write_subtitle_paths": write_subtitle_paths,
            "date": date,
            "generator": generator,
            "nickname": nickname,
            "video_path": video_path,
            "video_name": video_name,
            "subtitles": subtitles,
            "comments": comments,
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
        #: Will be used in the file name proposal when saving a qc document when there's no video being loaded
        return QCoreApplication.translate("FileInteractionDialogs", "untitled")

    @property
    def _content(self) -> str:
        return self._renderer.render(self._resources.backup_template)

    def backup(self) -> None:
        now = QDateTime.currentDateTime()

        zip_name = f"{now.toString('yyyy-MM')}.zip"
        zip_path = self._paths.dir_backup / zip_name
        file_name = f"{now.toString('yyyy-MM-dd_HH-mm-ss')}_{self._video_name}.txt"

        with ZipFile(zip_path, mode="a" if zip_path.exists() else "w", compression=ZIP_DEFLATED) as file:
            file.writestr(file_name, self._content)


class DocumentExportService(QObject):
    _player: PlayerService = inject.attr(PlayerService)
    _renderer: DocumentRenderService = inject.attr(DocumentRenderService)
    _settings: SettingsService = inject.attr(SettingsService)
    _resources: ResourceService = inject.attr(ResourceService)

    export_error_occurred = Signal(str, int)

    def generate_file_path_proposal(self) -> Path:
        if video := Path(self._player.path) if self._player.path else None:
            video_directory = str(video.parent)
            video_name = video.stem
        else:
            video_directory = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.MoviesLocation)
            video_name = QCoreApplication.translate("FileInteractionDialogs", "untitled")

        if nickname := self._settings.nickname:
            file_name = f"[QC]_{video_name}_{nickname}.txt"
        else:
            file_name = f"[QC]_{video_name}.txt"

        return Path(video_directory).joinpath(file_name).absolute()

    def export(self, file: Path, template: Path) -> None:
        user_template = template.read_text(encoding="utf-8")

        try:
            content = self._renderer.render(user_template)
            file.write_text(content, encoding="utf-8", newline="\n")
        except TemplateSyntaxError as e:
            self.export_error_occurred.emit(e.message, e.lineno)
        except TemplateError as e:
            self.export_error_occurred.emit(e.message, -1)

    def save(self, file: Path) -> None:
        export_template = self._resources.default_export_template
        content = self._renderer.render(export_template)

        file.write_text(content, encoding="utf-8", newline="\n")
