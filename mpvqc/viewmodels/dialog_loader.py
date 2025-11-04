# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
from pathlib import Path

import inject
from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.datamodels import VideoSource
from mpvqc.services import ImporterService, TypeMapperService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming
@QmlElement
class MpvqcDialogLoaderViewModel(QObject):
    _importer: ImporterService = inject.attr(ImporterService)
    _type_mapper: TypeMapperService = inject.attr(TypeMapperService)

    # param 1: JSON string of videos with path, filename, fromDocument, fromSubtitle
    # param 2: JSON string of subtitles with path, filename
    importConfirmationDialogRequested = Signal(str, str)

    def __init__(self):
        super().__init__()
        self._importer.ask_user_what_to_import.connect(self._ask_user_what_to_import)

    @Slot("QVariantList", "QVariantList")
    def _ask_user_what_to_import(
        self,
        videos_found: tuple[VideoSource, ...],
        subtitles_found: tuple[Path, ...],
    ) -> None:
        videos = [
            {
                "path": self._type_mapper.map_path_to_str(video.path),
                "filename": video.path.name,
                "fromDocument": video.from_document,
                "fromSubtitle": video.from_subtitle,
            }
            for video in videos_found
        ]

        subtitles = [
            {
                "path": self._type_mapper.map_path_to_str(subtitle),
                "filename": subtitle.name,
                "checked": True,
            }
            for subtitle in subtitles_found
        ]

        self.importConfirmationDialogRequested.emit(json.dumps(videos), json.dumps(subtitles))

    @Slot(str, list)
    def confirmImport(self, video_path: str, subtitle_paths: list[str]):
        video = Path(video_path) if video_path else None
        subtitles = tuple(Path(p) for p in subtitle_paths)
        self._importer.finalize_import(video, subtitles)
