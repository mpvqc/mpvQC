# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import TYPE_CHECKING

from PySide6.QtGui import QDesktopServices

if TYPE_CHECKING:
    from PySide6.QtCore import QUrl


class DesktopService:
    def open_url(self, url: QUrl) -> None:
        QDesktopServices.openUrl(url)
