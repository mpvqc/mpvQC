# mpvQC
#
# Copyright (C) 2025 mpvQC developers
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

from collections.abc import Callable
from functools import cached_property
from pathlib import Path

import inject
from PySide6.QtCore import QCoreApplication, QObject, QRunnable, QThreadPool, QUrl, Signal, Slot
from PySide6.QtGui import QStandardItemModel
from PySide6.QtQml import QmlElement

from mpvqc.services import (
    DocumentExportService,
    DocumentImporterService,
    TypeMapperService,
)

from .comment_model import MpvqcCommentModelPyObject

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


class ImportJob(QRunnable):
    _importer: DocumentImporterService = inject.attr(DocumentImporterService)
    _type_mapper: TypeMapperService = inject.attr(TypeMapperService)

    def __init__(
        self,
        documents: list[QUrl],
        videos: list[QUrl],
        subtitles: list[QUrl],
        comment_model: MpvqcCommentModelPyObject,
        callback: Callable[[dict], None],
    ):
        super().__init__()
        self._documents = documents
        self._videos = videos
        self._subtitles = subtitles
        self._comment_model = comment_model
        self._callback = callback

    @Slot()
    def run(self):
        documents = self._type_mapper.map_urls_to_path(self._documents)
        videos = self._type_mapper.map_urls_to_path(self._videos)
        subtitles = self._type_mapper.map_urls_to_path(self._subtitles)

        result = self._importer.read(documents)
        self._comment_model.import_comments(result.comments)

        self._callback(
            {
                "documentsValid": [
                    {
                        "url": self._fully_encoded(document.path),
                        "videoUrl": self._fully_encoded(document.video_path) if document.video_exists else None,
                        "videoExists": document.video_exists,
                    }
                    for document in result.valid_documents
                ],
                "documentsInvalid": [str(p) for p in result.invalid_documents],
                "videos": [self._fully_encoded(p) for p in videos],
                "subtitles": [self._fully_encoded(p) for p in subtitles],
            }
        )

    def _fully_encoded(self, path: Path) -> str:
        url = self._type_mapper.map_path_to_url(path)
        return url.toString()


class ResetJob(QRunnable):
    def __init__(self, comment_model: MpvqcCommentModelPyObject, callback: Callable[[], None]):
        super().__init__()
        self._comment_model = comment_model
        self._callback = callback

    @Slot()
    def run(self):
        self._comment_model.clear_comments()
        self._callback()


class ExportJob(QRunnable):
    _exporter: DocumentExportService = inject.attr(DocumentExportService)
    _type_mapper: TypeMapperService = inject.attr(TypeMapperService)

    def __init__(self, url: QUrl, callback: Callable[[QUrl], None]):
        super().__init__()
        self._url = url
        self._callback = callback

    @Slot()
    def run(self):
        path = self._type_mapper.map_url_to_path(self._url)
        self._exporter.save(path)
        self._callback(self._url)


# noinspection PyPep8Naming
@QmlElement
class MpvqcManagerBackendPyObject(QObject):
    imported = Signal(dict)
    changed = Signal()
    reset = Signal()
    saved = Signal(QUrl)

    def __init__(self):
        super().__init__()
        QCoreApplication.instance().application_ready.connect(lambda: self._on_application_ready())

    def _on_application_ready(self):
        def on_comments_changed(*_):
            self.changed.emit()

        self._comment_model.commentsClearedUndone.connect(on_comments_changed)

        # Initial import is an "import" rather than a "change"
        self._comment_model.commentsImportedRedone.connect(on_comments_changed)
        self._comment_model.commentsImportedUndone.connect(on_comments_changed)

        self._comment_model.newCommentAddedInitially.connect(on_comments_changed)
        self._comment_model.newCommentAddedUndone.connect(on_comments_changed)
        self._comment_model.newCommentAddedRedone.connect(on_comments_changed)

        self._comment_model.commentRemoved.connect(on_comments_changed)
        self._comment_model.commentRemovedUndone.connect(on_comments_changed)

        self._comment_model.timeUpdatedInitially.connect(on_comments_changed)
        self._comment_model.timeUpdatedUndone.connect(on_comments_changed)
        self._comment_model.timeUpdatedRedone.connect(on_comments_changed)

        self._comment_model.commentTypeUpdated.connect(on_comments_changed)
        self._comment_model.commentTypeUpdatedUndone.connect(on_comments_changed)

        self._comment_model.commentUpdated.connect(on_comments_changed)
        self._comment_model.commentUpdatedUndone.connect(on_comments_changed)

    @cached_property
    def _comment_model(self) -> MpvqcCommentModelPyObject:
        return QCoreApplication.instance().find_object(QStandardItemModel, "mpvqcCommentModel")

    @Slot(list, list, list)
    def performImport(self, documents: list[QUrl], videos: list[QUrl], subtitles: list[QUrl]) -> None:
        job = ImportJob(
            documents=documents,
            videos=videos,
            subtitles=subtitles,
            comment_model=self._comment_model,
            callback=self.imported.emit,
        )
        QThreadPool.globalInstance().start(job)

    @Slot()
    def performReset(self) -> None:
        job = ResetJob(
            comment_model=self._comment_model,
            callback=self.reset.emit,
        )
        QThreadPool.globalInstance().start(job)

    @Slot(QUrl)
    def performSave(self, document: QUrl) -> None:
        job = ExportJob(
            url=document,
            callback=self.saved.emit,
        )
        QThreadPool.globalInstance().start(job)
