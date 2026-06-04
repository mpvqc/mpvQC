# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from PySide6.QtCore import QDir
from PySide6.QtGui import QFont, QFontDatabase


class FontLoaderService:
    @staticmethod
    def load_application_fonts() -> None:
        for entry_info in QDir(":/data/fonts").entryInfoList():
            resource_path = entry_info.filePath()
            if QFontDatabase.addApplicationFont(resource_path) == -1:
                msg = f"Cannot load font from {resource_path}"
                raise ValueError(msg)

    @staticmethod
    def application_font() -> QFont:
        font = QFont()
        font.setFamilies(["Noto Sans", "Noto Sans Hebrew"])
        font.setPointSize(10)
        return font

    @staticmethod
    def monospace_font() -> QFont:
        font = QFont()
        font.setFamilies(["Noto Sans Mono", "Noto Sans", "Noto Sans Hebrew"])
        font.setPointSize(11)
        return font
