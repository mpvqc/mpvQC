#  mpvQC
#
#  Copyright (C) 2022 mpvQC developers
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.


import inject
from PySide6.QtGui import QGuiApplication, QIcon

from mpvqc.services.resource import ResourceService


class WindowIconService:
    """Responsible for setting the icon in the window bar"""

    _resources = inject.attr(ResourceService)

    def restore(self, app: QGuiApplication):
        icon_path = self._resources.window_icon_path
        icon = QIcon(icon_path)
        app.setWindowIcon(icon)
