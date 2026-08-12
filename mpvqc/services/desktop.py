# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices

from mpvqc.shared import map_path_to_url

from .application_paths import ApplicationPathsService


class DesktopService:
    _paths = inject.attr(ApplicationPathsService)

    def open_app_data_folder(self) -> None:
        path = self._paths.dir_config
        url = map_path_to_url(path)
        QDesktopServices.openUrl(url)

    def open_backup_folder(self) -> None:
        path = self._paths.dir_backup
        url = map_path_to_url(path)
        QDesktopServices.openUrl(url)

    def open_url(self, url: QUrl) -> None:
        QDesktopServices.openUrl(url)
