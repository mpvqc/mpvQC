# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from PySide6.QtGui import QFont


def application_font() -> QFont:
    font = QFont()
    font.setFamilies(["Noto Sans", "Noto Sans Hebrew"])
    font.setPointSize(10)
    return font


def monospace_font() -> QFont:
    font = QFont()
    font.setFamilies(["Noto Sans Mono", "Noto Sans", "Noto Sans Hebrew"])
    font.setPointSize(11)
    return font
