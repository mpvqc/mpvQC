# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from PySide6.QtCore import QObject, Slot
from PySide6.QtQml import QQmlEngine

from mpvqc import startup


# noinspection PyPep8Naming
class MpvqcTestSetup(QObject):
    @Slot(QQmlEngine)
    def qmlEngineAvailable(self, _: QQmlEngine):
        import rc_project  # noqa: F401

        startup.configure_qt_application_data()
        startup.configure_qt_settings()
        startup.configure_dependency_injection()
        startup.configure_environment_variables()
        startup.import_mpvqc_bindings()
