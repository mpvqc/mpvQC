# mpvQC
#
# Copyright (C) 2025 mpvQC developers
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

from PySide6.QtCore import QObject, Slot
from PySide6.QtQml import QQmlEngine

from mpvqc import startup


# noinspection PyPep8Naming
class MpvqcTestSetup(QObject):
    @Slot(QQmlEngine)
    def qmlEngineAvailable(self, _: QQmlEngine):
        startup.configure_qt_application_data()
        startup.configure_qt_settings()
        startup.configure_dependency_injection()
        startup.configure_environment_variables()
        startup.import_mpvqc_bindings()
        import rc_project  # noqa: F401
