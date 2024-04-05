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


import unittest

from PySide6.QtCore import QFile
from PySide6.QtGui import QFontDatabase

from mpvqc.application import MpvqcApplication
from mpvqc.services import FontLoaderService


class FontLoaderTest(unittest.TestCase):
    """"""

    def setUp(self):
        self.tearDown()
        self._app = MpvqcApplication([])

    def tearDown(self):
        if hasattr(self, "_app") and self._app:
            self._app.shutdown()

    def test_fonts_present_in_resources(self):
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
            self.assertTrue(file.exists(), f"Expected to find {variant} in resources but couldn't")

    def test_fonts_loaded(self):
        # It's not possible to clear Qt's entire font database. Additionally, font backends on different OS's behave
        # differently. Therefore, we just test for the common font families.
        font_families = [
            "Noto Sans",
            "Noto Sans Hebrew",
            "Noto Sans Mono",
        ]

        FontLoaderService().load_application_fonts()

        loaded_font_families = QFontDatabase.families()

        for font_family in font_families:
            self.assertIn(
                font_family,
                loaded_font_families,
                msg=f"Cannot find font family '{font_family}' in loaded font families {loaded_font_families}",
            )
