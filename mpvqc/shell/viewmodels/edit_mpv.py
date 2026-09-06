# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, QUrl, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import ApplicationPathsService, DesktopService, read_mpv_conf
from mpvqc.shared import map_path_to_url

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcEditMpvDialogViewModel(QObject):
    _desktop = inject.attr(DesktopService)
    _paths = inject.attr(ApplicationPathsService)

    @Property(QUrl, constant=True, final=True)
    def mpvFileUrl(self) -> QUrl:
        return map_path_to_url(self._paths.file_mpv_conf)

    @Property(str, constant=True, final=True)
    def defaultMpvConfiguration(self) -> str:
        return read_mpv_conf()

    @Slot(QUrl)
    def openLink(self, link: QUrl) -> None:
        self._desktop.open_url(link)
