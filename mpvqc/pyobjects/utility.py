# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from os import environ

import inject
from PySide6.QtCore import Property, QObject, QPoint, QUrl, Slot
from PySide6.QtGui import QCursor
from PySide6.QtQml import QmlElement

from mpvqc.services import (
    DocumentExportService,
    MimetypeProviderService,
    ReverseTranslatorService,
    TimeFormatterService,
    TypeMapperService,
)

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming, PyMethodMayBeStatic
@QmlElement
class MpvqcUtilityPyObject(QObject):
    _exporter: DocumentExportService = inject.attr(DocumentExportService)
    _mimetype_provider: MimetypeProviderService = inject.attr(MimetypeProviderService)
    _time_formatter: TimeFormatterService = inject.attr(TimeFormatterService)
    _translator: ReverseTranslatorService = inject.attr(ReverseTranslatorService)
    _type_mapper: TypeMapperService = inject.attr(TypeMapperService)

    @Property(QPoint, final=True)
    def cursorPosition(self) -> QPoint:
        return QCursor.pos()

    @Property(str, constant=True, final=True)
    def videoFileGlobPattern(self) -> str:
        return self._mimetype_provider.video_file_glob_pattern

    @Property(str, constant=True, final=True)
    def subtitleFileGlobPattern(self) -> str:
        return self._mimetype_provider.subtitle_file_glob_pattern

    @Property(list, constant=True, final=True)
    def subtitleFileExtensions(self) -> list:
        return self._mimetype_provider.subtitle_file_extensions

    @Slot(str, result=str)
    def getEnvironmentVariable(self, key: str) -> str | None:
        return environ.get(key) or None

    @Slot(float, result=str)
    def formatTimeToStringLong(self, seconds: float) -> str:
        return self._time_formatter.format_time_to_string(seconds, long_format=True)

    @Slot(float, result=str)
    def formatTimeToStringShort(self, seconds: float) -> str:
        return self._time_formatter.format_time_to_string(seconds, long_format=False)

    @Slot(QUrl, result=str)
    def urlToAbsolutePath(self, url: QUrl) -> str:
        return self._type_mapper.map_url_to_path_string(url)

    @Slot(str, result=str)
    def reverseLookupCommentType(self, non_english: str) -> str:
        return self._translator.lookup(non_english)

    @Slot(result=QUrl)
    def generate_file_path_proposal(self) -> QUrl:
        path = self._exporter.generate_file_path_proposal()
        return self._type_mapper.map_path_to_url(path)
