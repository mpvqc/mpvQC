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


from PySide6.QtGui import QFont, QFontDatabase


class FontLoaderService:
    _used_variants = [
        'NotoSans-Regular.ttf',
        'NotoSans-Italic.ttf',
        'NotoSans-Bold.ttf',
        'NotoSans-SemiBold.ttf',
        'NotoSansHebrew-Bold.ttf',
        'NotoSansHebrew-Regular.ttf',
        'NotoSansHebrew-SemiBold.ttf',
        'NotoSansMono-Regular.ttf'
    ]

    def load_application_fonts(self):
        for variant in self._used_variants:
            QFontDatabase.addApplicationFont(f":/data/fonts/{variant}")

        QFont.insertSubstitution('NotoSans', 'NotoSansHebrew')
