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


class StartUp:
    """"""

    @staticmethod
    def configure_qt_application_data():
        from PySide6.QtCore import QCoreApplication

        QCoreApplication.setApplicationName("mpvQC")
        QCoreApplication.setOrganizationName("mpvQC")
        QCoreApplication.setApplicationVersion(">>>tag<<<")

    @staticmethod
    def configure_qt_settings():
        from PySide6.QtCore import QSettings

        QSettings.setDefaultFormat(QSettings.IniFormat)

    @staticmethod
    def configure_qt_logging():
        from PySide6 import QtCore
        from .logging import qt_log_handler

        QtCore.qInstallMessageHandler(qt_log_handler())

    @staticmethod
    def configure_qt_render_backend():
        from PySide6.QtQuick import QSGRendererInterface
        from PySide6.QtQuick import QQuickWindow

        QQuickWindow.setGraphicsApi(QSGRendererInterface.GraphicsApi.OpenGL)

    @staticmethod
    def configure_dependency_injection():
        from mpvqc.injections import configure_injections

        configure_injections()

    @staticmethod
    def configure_environment_variables():
        import os

        # Qt expects 'qtquickcontrols2.conf' at root level, but the way we handle resources does not allow that.
        # So we need to override the path here
        os.environ["QT_QUICK_CONTROLS_CONF"] = ":/data/qtquickcontrols2.conf"

        # Requirement for mpv
        os.environ["LC_NUMERIC"] = "C"

    @staticmethod
    def import_mpvqc_resources():
        import mpvqc.generated_resources  # noqa: F401

    @staticmethod
    def import_mpvqc_bindings():
        import mpvqc.pyobjects  # noqa: F401

    @staticmethod
    def start_application():
        import sys
        from mpvqc.application import MpvqcApplication

        app = MpvqcApplication(sys.argv)

        app.set_window_icon()
        app.load_application_fonts()
        app.create_directories()
        app.set_up_signals()
        app.set_up_imports()
        app.install_window_event_filter()
        app.start_engine()
        app.add_window_effects()
        app.verify()
        app.notify_ready()

        sys.exit(app.exec())


def perform_startup():
    we = StartUp()

    we.configure_qt_application_data()
    we.configure_qt_settings()
    we.configure_qt_logging()
    we.configure_dependency_injection()
    we.configure_qt_render_backend()
    we.configure_environment_variables()

    we.import_mpvqc_resources()
    we.import_mpvqc_bindings()

    we.start_application()
