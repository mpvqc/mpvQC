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

import os
import sys


class PreStartUp:
    """Necessary steps for environment, Python and Qt"""

    @staticmethod
    def set_qt_application_name():
        from PySide6.QtCore import QCoreApplication
        QCoreApplication.setApplicationName('mpvQC')
        QCoreApplication.setOrganizationName('mpvQC')

    @staticmethod
    def set_qt_application_version():
        from PySide6.QtCore import QCoreApplication
        QCoreApplication.setApplicationVersion('>>>tag<<<')

    @staticmethod
    def set_qt_settings_format():
        from PySide6.QtCore import QSettings
        QSettings.setDefaultFormat(QSettings.IniFormat)

    @staticmethod
    def prepare_dependency_injection():
        from mpvqc.injections import configure_injections
        configure_injections()

    @staticmethod
    def set_render_backend():
        from PySide6.QtQuick import QSGRendererInterface
        from PySide6.QtQuick import QQuickWindow
        QQuickWindow.setGraphicsApi(QSGRendererInterface.GraphicsApi.OpenGL)

    @staticmethod
    def inject_environment_variables():
        # Qt expects 'qtquickcontrols2.conf' at root level, but the way we handle resources does not allow that.
        # So we need to override the path here
        os.environ['QT_QUICK_CONTROLS_CONF'] = ':/data/qtquickcontrols2.conf'

        # Requirement for mpv
        os.environ['LC_NUMERIC'] = 'C'


class StartUp:
    """Necessary steps for mpvQC"""

    @staticmethod
    def import_mpvqc_resources():
        try:
            import mpvqc.generated_resources
        except ImportError as e:
            print(f"Can not find module: mpvqc.generated_resources: {e}", file=sys.stderr)
            sys.exit(1)

    @staticmethod
    def import_mpvqc_bindings():
        try:
            import mpvqc.pyobjects
        except ImportError as e:
            print(f"Can not import python qml elements: {e}", file=sys.stderr)
            sys.exit(1)

    @staticmethod
    def start_application():
        from mpvqc.application import MpvqcApplication
        app = MpvqcApplication(sys.argv)

        app.set_window_icon()
        app.set_up_internationalization()
        app.create_directories()
        app.set_up_signals()
        app.set_up_imports()
        app.start_engine()
        app.verify()

        sys.exit(app.exec())


def perform_startup():
    we = PreStartUp()
    we.set_qt_application_name()
    we.set_qt_application_version()
    we.set_qt_settings_format()
    we.prepare_dependency_injection()
    we.set_render_backend()
    we.inject_environment_variables()

    we = StartUp()
    we.import_mpvqc_resources()
    we.import_mpvqc_bindings()
    we.start_application()
