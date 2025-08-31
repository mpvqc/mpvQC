# mpvQC
#
# Copyright (C) 2022 mpvQC developers
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


def perform_startup():
    configure_qt_application_data()
    configure_qt_settings()
    configure_qt_logging()
    configure_dependency_injection()
    configure_environment_variables()

    import_mpvqc_bindings()

    start_application()


def configure_qt_application_data():
    from PySide6.QtCore import QCoreApplication
    from PySide6.QtQuickControls2 import QQuickStyle

    QCoreApplication.setApplicationName("mpvQC")
    QCoreApplication.setOrganizationName("mpvQC")
    QCoreApplication.setApplicationVersion(">>>tag<<<")

    QQuickStyle.setStyle("Material")


def configure_qt_settings():
    from PySide6.QtCore import QSettings

    QSettings.setDefaultFormat(QSettings.Format.IniFormat)


def configure_qt_logging():
    from PySide6 import QtCore

    from .logging import qt_log_handler

    QtCore.qInstallMessageHandler(qt_log_handler())


def configure_dependency_injection():
    from mpvqc.injections import configure_injections

    configure_injections()


def configure_environment_variables():
    import os

    os.environ["QT_QUICK_CONTROLS_MATERIAL_VARIANT"] = "Dense"

    # Requirement for mpv
    os.environ["LC_NUMERIC"] = "C"


def import_mpvqc_bindings():
    import mpvqc.pyobjects  # noqa: F401


def start_application():
    import sys

    from mpvqc.application import MpvqcApplication

    app = MpvqcApplication(sys.argv)

    app.set_window_icon()
    app.load_application_fonts()
    app.create_directories()
    app.set_up_signals()
    app.start_engine()
    app.notify_ready()
    app.configure_frameless_window()

    sys.exit(app.exec())
