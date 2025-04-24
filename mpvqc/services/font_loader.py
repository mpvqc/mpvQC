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
