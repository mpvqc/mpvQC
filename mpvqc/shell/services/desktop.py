# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices


class DesktopService:
    def open_url(self, url: QUrl) -> None:
        QDesktopServices.openUrl(url)
