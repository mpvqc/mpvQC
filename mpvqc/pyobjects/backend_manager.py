# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
from functools import cached_property
from pathlib import Path

import inject
from PySide6.QtCore import QCoreApplication, QObject, QUrl, Signal, Slot
from PySide6.QtGui import QStandardItemModel
from PySide6.QtQml import QmlElement, QQmlComponent

from mpvqc.pyobjects.comment_model import MpvqcCommentModelPyObject
from mpvqc.services import (
    DocumentExportService,
    DocumentImporterService,
    PlayerService,
    TypeMapperService,
    VideoSelectorService,
)

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcManagerBackendPyObject(QObject):
    _exporter: DocumentExportService = inject.attr(DocumentExportService)
    _importer: DocumentImporterService = inject.attr(DocumentImporterService)
    _player: PlayerService = inject.attr(PlayerService)
    _type_mapper: TypeMapperService = inject.attr(TypeMapperService)
    _video_selector: VideoSelectorService = inject.attr(VideoSelectorService)

    imported = Signal(str)  # json payload
    changed = Signal()
    reset = Signal()
    saved = Signal(str)

    def __init__(self):
        super().__init__()
        QCoreApplication.instance().application_ready.connect(lambda: self._on_application_ready())

    @cached_property
    def _comment_model(self) -> MpvqcCommentModelPyObject:
        return QCoreApplication.instance().find_object(QStandardItemModel, "mpvqcCommentModel")

    @property
    def document(self) -> str | None:
        return self.property("_document")

    @property
    def is_saved(self) -> bool:
        return bool(self.property("saved"))

    def _on_application_ready(self):
        def bind_qml_property_with(name: str) -> QQmlComponent:
            qml_prop = self.property(name)
            if not qml_prop:
                msg = f"Could not find qml property with name '{name}'"
                raise ValueError(msg)
            return qml_prop

        # fmt: off
        self.dialog_export_document_factory \
            = bind_qml_property_with(name="mpvqcDialogExportDocumentFactory")
        self.message_box_video_found_factory \
            = bind_qml_property_with(name="mpvqcMessageBoxVideoFoundFactory")
        self.message_box_new_document_factory \
            = bind_qml_property_with(name="mpvqcMessageBoxNewDocumentFactory")
        self.message_box_document_not_compatible_factory \
            = bind_qml_property_with(name="mpvqcMessageBoxDocumentNotCompatibleFactory")

        # fmt: on

        def on_comments_changed(*_):
            self.changed.emit()

        def on_comments_cleared(*_):
            self.reset.emit()

        self._comment_model.commentsCleared.connect(on_comments_cleared)
        self._comment_model.commentsClearedUndone.connect(on_comments_changed)

        # Signal 'commentsImportedInitially' is an "import" rather than a "change"
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

    @Slot()
    def reset_impl(self):
        """ """

        def _ask_to_confirm_reset():
            message_box = self.message_box_new_document_factory.createObject()
            message_box.closed.connect(message_box.deleteLater)
            message_box.accepted.connect(_reset)
            message_box.open()

        def _reset():
            self._comment_model.clear_comments()

        if self.is_saved:
            _reset()
        else:
            _ask_to_confirm_reset()

    @Slot(list)
    def open_documents_impl(self, documents: list[QUrl]):
        self.open_impl(documents=documents, videos=[], subtitles=[])

    @Slot(QUrl)
    def open_video_impl(self, video: QUrl):
        self.open_impl(documents=[], videos=[video], subtitles=[])

    @Slot(list)
    def open_subtitles_impl(self, subtitles: list[QUrl]):
        self.open_impl(documents=[], videos=[], subtitles=subtitles)

    @Slot(list, list, list)
    def open_impl(self, documents: list[QUrl], videos: list[QUrl], subtitles: list[QUrl]):  # noqa: C901
        documents = self._type_mapper.map_urls_to_path(documents)
        videos = self._type_mapper.map_urls_to_path(videos)
        subtitles = self._type_mapper.map_urls_to_path_strings(subtitles)

        document_import_result = self._importer.read(documents)

        def on_video_selected(video: Path | None):
            _load_new_comments()
            _load_new_video(video)
            _load_new_subtitles()
            _update_state(video)
            _display_erroneous_documents()

        def _load_new_comments():
            self._comment_model.import_comments(document_import_result.comments)

        def _load_new_video(video: Path | None):
            if video:
                self._player.open_video(f"{video}")

        def _load_new_subtitles():
            if subtitles:
                self._player.open_subtitles(subtitles)

        def _update_state(video: Path | None):
            if video or document_import_result.valid_documents:
                payload = {
                    "documents": self._type_mapper.map_paths_to_str(document_import_result.valid_documents),
                    "video": self._type_mapper.map_path_to_str(video) if video else None,
                }
                self.imported.emit(json.dumps(payload))

        def _display_erroneous_documents():
            paths = document_import_result.invalid_documents

            if not paths:
                return

            properties = {"paths": [p.name for p in paths]}

            message_box = self.message_box_document_not_compatible_factory.createObject(None, properties)
            message_box.closed.connect(message_box.deleteLater)
            message_box.open()

        self._video_selector.select_video_from(
            existing_videos_dropped=videos,
            existing_videos_from_documents=document_import_result.existing_videos,
            video_found_dialog_factory=self.message_box_video_found_factory,
            on_video_selected=on_video_selected,
        )

    @Slot()
    def save_impl(self):
        if document := self.document:
            self._save(document)
        else:
            self.save_as_impl()

    def _save(self, path: str):
        self._exporter.save(Path(path))
        self.saved.emit(path)

    @Slot()
    def save_as_impl(self):
        path_proposal = self._exporter.generate_file_path_proposal()

        properties = {"selectedFile": self._type_mapper.map_path_to_url(path_proposal)}

        dialog = self.dialog_export_document_factory.createObject(None, properties)
        dialog.accepted.connect(dialog.deleteLater)
        dialog.rejected.connect(dialog.deleteLater)
        dialog.savePressed.connect(lambda url: self._save(self._type_mapper.map_url_to_path_string(url)))
        dialog.open()
