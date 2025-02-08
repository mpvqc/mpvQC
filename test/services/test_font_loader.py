# mpvQC
#
# Copyright (C) 2024 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
