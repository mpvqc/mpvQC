# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import QObject, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import (
    DocumentExportService,
    TimeFormatterService,
    TypeMapperService,
)

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming, PyMethodMayBeStatic
@QmlElement
class MpvqcUtilityPyObject(QObject):
    _exporter: DocumentExportService = inject.attr(DocumentExportService)
    _time_formatter: TimeFormatterService = inject.attr(TimeFormatterService)
    _type_mapper: TypeMapperService = inject.attr(TypeMapperService)

    @Slot(float, result=str)
    def formatTimeToStringLong(self, seconds: float) -> str:
        return self._time_formatter.format_time_to_string(seconds, long_format=True)

    @Slot(float, result=str)
    def formatTimeToStringShort(self, seconds: float) -> str:
        return self._time_formatter.format_time_to_string(seconds, long_format=False)
