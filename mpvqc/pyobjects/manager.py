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

from functools import cached_property
from pathlib import Path

import inject
from PySide6.QtCore import QObject, Slot, Signal, Property, QUrl, QCoreApplication
from PySide6.QtGui import QStandardItemModel
from PySide6.QtQml import QmlElement, QQmlComponent

from mpvqc.impl import InitialState, ApplicationState, ImportChange
from mpvqc.services import DocumentImporterService, VideoSelectorService, PlayerService, DocumentBackupService, \
    DocumentExportService, TypeMapperService
from .comment_model import MpvqcCommentModelPyObject

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcManagerPyObject(QObject):
    _backupper: DocumentBackupService = inject.attr(DocumentBackupService)
    _exporter: DocumentExportService = inject.attr(DocumentExportService)
    _importer: DocumentImporterService = inject.attr(DocumentImporterService)
    _player: PlayerService = inject.attr(PlayerService)
    _type_mapper: TypeMapperService = inject.attr(TypeMapperService)
    _video_selector: VideoSelectorService = inject.attr(VideoSelectorService)

    def __init__(self):
        super().__init__()
        QCoreApplication.instance().application_ready.connect(lambda: self._on_application_ready())
        self._state = InitialState.new()

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value: ApplicationState):
        self._state = value
        self.set_saved(value.saved)

    @cached_property
    def _comment_model(self) -> MpvqcCommentModelPyObject:
        return QCoreApplication.instance().find_object(QStandardItemModel, 'mpvqcCommentModel')

    def _on_application_ready(self):

        def bind_qml_property_with(name: str) -> QQmlComponent:
            qml_prop = self.property(name)
            assert qml_prop, f"Could not find qml property with name '{name}'"
            return qml_prop

        self.dialog_export_document_factory \
            = bind_qml_property_with(name='mpvqcDialogExportDocumentFactory')
        self.message_box_video_found_factory \
            = bind_qml_property_with(name='mpvqcMessageBoxVideoFoundFactory')
        self.message_box_new_document_factory \
            = bind_qml_property_with(name='mpvqcMessageBoxNewDocumentFactory')
        self.message_box_document_not_compatible_factory \
            = bind_qml_property_with(name='mpvqcMessageBoxDocumentNotCompatibleFactory')

        def on_comments_changed():
            self.state = self.state.handle_change()

        self._comment_model.commentsChanged.connect(on_comments_changed)

    # Qml Properties

    def get_saved(self):
        return self.state.saved

    def set_saved(self, value: bool):
        if value != self._saved:
            self._saved = value
            self.saved_changed.emit(value)

    _saved = True
    saved_changed = Signal(bool)
    saved = Property(bool, get_saved, set_saved, notify=saved_changed)

    # Qml Slots

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
            self.state = self.state.handle_reset()

        if self.saved:
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
    def open_impl(self, documents: list[QUrl], videos: list[QUrl], subtitles: list[QUrl]):
        documents = self._type_mapper.map_urls_to_path(documents)
        videos = self._type_mapper.map_urls_to_path(videos)
        subtitles = self._type_mapper.map_urls_to_path_strings(subtitles)

        document_import_result = self._importer.read(documents)

        def on_video_selected(video: Path or None):
            _load_new_comments()
            _load_new_video(video)
            _load_new_subtitles()
            _update_state(video)
            _display_erroneous_documents()

        def _load_new_comments():
            self._comment_model.import_comments(document_import_result.comments)

        def _load_new_video(video: Path or None):
            if video:
                self._player.open_video(f'{video}')

        def _load_new_subtitles():
            if subtitles:
                self._player.open_subtitles(subtitles)

        def _update_state(video: Path or None):
            if video or document_import_result.valid_documents:
                change = ImportChange(document_import_result.valid_documents, video)
                self.state = self.state.handle_import(change)

        def _display_erroneous_documents():
            paths = document_import_result.invalid_documents

            if not paths:
                return

            properties = {
                'count': len(paths),
                'text': '\n'.join([p.name for p in paths])
            }

            message_box = self.message_box_document_not_compatible_factory.createObject(None, properties)
            message_box.closed.connect(message_box.deleteLater)
            message_box.open()

        self._video_selector.select_video_from(
            existing_videos_dropped=videos,
            existing_videos_from_documents=document_import_result.existing_videos,
            video_found_dialog_factory=self.message_box_video_found_factory,
            on_video_selected=on_video_selected
        )

    @Slot()
    def save_impl(self):
        if document := self.state.document:
            self._save(document)
        else:
            self.save_as_impl()

    def _save(self, path: Path):
        self._exporter.save(path)
        self.state = self.state.handle_save(path)

    @Slot()
    def save_as_impl(self):
        path_proposal = self._exporter.generate_file_path_proposal()

        properties = {
            'selectedFile': self._type_mapper.map_path_to_url(path_proposal)
        }

        dialog = self.dialog_export_document_factory.createObject(None, properties)
        dialog.accepted.connect(dialog.deleteLater)
        dialog.rejected.connect(dialog.deleteLater)
        dialog.savePressed.connect(lambda url: self._save(self._type_mapper.map_url_to_path(url)))
        dialog.open()

    @Slot()
    def backup_impl(self):
        self._backupper.backup()
