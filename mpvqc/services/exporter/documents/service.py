# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
from pathlib import Path

import inject
from PySide6.QtCore import QCoreApplication, QObject, QStandardPaths, Signal

from mpvqc.services.player import PlayerService
from mpvqc.services.resource import ResourceService
from mpvqc.services.settings import SettingsService

from .classic import DocumentRenderService
from .v1 import render as render_v1

logger = logging.getLogger(__name__)


class DocumentExportService(QObject):
    _player = inject.attr(PlayerService)
    _renderer = inject.attr(DocumentRenderService)
    _settings = inject.attr(SettingsService)
    _resources = inject.attr(ResourceService)

    export_error_occurred = Signal(str, int)

    def generate_file_path_proposal(self) -> Path:
        if raw_path := self._player.path:
            path = Path(raw_path)
            video_directory = str(path.parent)
            video_name = path.stem
        else:
            video_directory = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.MoviesLocation)
            video_name = QCoreApplication.translate("FileInteractionDialogs", "untitled")

        if nickname := self._settings.nickname:
            file_name = f"[QC]_{video_name}_{nickname}.txt"
        else:
            file_name = f"[QC]_{video_name}.txt"

        return Path(video_directory).joinpath(file_name).absolute()

    def export(self, file: Path, template: Path) -> None:
        from jinja2 import TemplateError, TemplateSyntaxError

        try:
            user_template = template.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            logger.exception("Failed to read export template %s", template)
            self.export_error_occurred.emit(self._template_read_error(), -1)
            return

        try:
            content = self._renderer.render(user_template)
            file.write_text(content, encoding="utf-8", newline="\n")
        except TemplateSyntaxError as e:
            self.export_error_occurred.emit(e.message, e.lineno)
        except TemplateError as e:
            self.export_error_occurred.emit(e.message, -1)
        except OSError:
            logger.exception("Failed to write export to %s", file)
            self.export_error_occurred.emit(self._document_save_error(), -1)

    def save(self, file: Path) -> None:
        self._write(file, render_v1())

    def save_classic(self, file: Path) -> None:
        export_template = self._resources.default_export_template
        content = self._renderer.render(export_template)
        self._write(file, content)

    def _write(self, file: Path, content: str) -> None:
        try:
            file.write_text(content, encoding="utf-8", newline="\n")
        except OSError:
            logger.exception("Failed to save document to %s", file)
            self.export_error_occurred.emit(self._document_save_error(), -1)

    @staticmethod
    def _template_read_error() -> str:
        #: Shown when a user-supplied export template cannot be read (file gone,
        #: permission denied, or not valid UTF-8). The technical detail is logged,
        #: not surfaced to the user.
        return QCoreApplication.translate("MessageBoxes", "The export template could not be read.")

    @staticmethod
    def _document_save_error() -> str:
        #: Shown when writing the QC document fails (permission denied, disk full,
        #: target directory missing). The technical detail is logged, not surfaced.
        return QCoreApplication.translate("MessageBoxes", "The document could not be saved.")
