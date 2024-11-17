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

import inject
from PySide6.QtCore import QObject, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import ThemeService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming
@QmlElement
class MpvqcThemesPyObject(QObject):
    _themes: ThemeService = inject.attr(ThemeService)

    @Slot(result=list)
    def getThemeSummaries(self) -> list[dict]:
        return self._themes.get_theme_summaries()

    @Slot(str, result=dict)
    def getThemeSummary(self, theme_identifier: str) -> dict:
        return self._themes.get_theme_summary(theme_identifier)

    @Slot(str, result=list)
    def getThemeColorOptions(self, theme_identifier: str) -> list[dict]:
        return self._themes.get_theme_colors(theme_identifier)

    @Slot(int, str, result=dict)
    def getThemeColorOption(self, color_option: int, theme_identifier: str):
        return self._themes.get_theme_color(color_option, theme_identifier)
