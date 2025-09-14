# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from PySide6.QtCore import QFile
from PySide6.QtGui import QFontDatabase

from mpvqc.services import FontLoaderService


def test_fonts_present_in_resources(qt_app):
    variants = [
        "NotoSans-Regular.ttf",
        "NotoSans-Italic.ttf",
        "NotoSans-Bold.ttf",
        "NotoSans-SemiBold.ttf",
        "NotoSansHebrew-Bold.ttf",
        "NotoSansHebrew-Regular.ttf",
        "NotoSansHebrew-SemiBold.ttf",
        "NotoSansMono-Regular.ttf",
    ]
    for variant in variants:
        file = QFile(f":/data/fonts/{variant}")
        assert file.exists(), f"Expected to find {variant} in resources but couldn't"


def test_fonts_loaded(qt_app):
    # It's not possible to clear Qt's entire font database. Additionally, font backends on different OS's behave
    # differently. Therefore, we just test for the common font families.
    verifiable_font_families = [
        "Noto Sans",
        "Noto Sans Hebrew",
        "Noto Sans Mono",
    ]

    FontLoaderService().load_application_fonts()
    loaded_font_families = QFontDatabase.families()

    for font_family in verifiable_font_families:
        assert font_family in loaded_font_families, (
            f"Cannot find font family '{font_family}' in loaded font families {loaded_font_families}"
        )
