# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from PySide6.QtCore import QDir
from PySide6.QtGui import QFont, QFontDatabase


class FontLoaderService:
    """"""

    @staticmethod
    def load_application_fonts():
        for entry_info in QDir(":/data/fonts").entryInfoList():
            resource_path = entry_info.filePath()
            if not QFontDatabase.addApplicationFont(resource_path) >= 0:
                msg = f"Cannot load font from {resource_path}"
                raise ValueError(msg)

        QFont.insertSubstitution("Noto Sans", "Noto Sans Hebrew")
