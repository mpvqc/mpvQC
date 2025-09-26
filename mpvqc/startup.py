# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later


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
    import mpvqc.controllers  # noqa: F401
    import mpvqc.helpers  # noqa: F401
    import mpvqc.models  # noqa: F401
    import mpvqc.pyobjects  # noqa: F401


def start_application():
    import sys

    from mpvqc.application import MpvqcApplication

    app = MpvqcApplication(sys.argv)

    app.set_window_icon()
    app.load_application_fonts()
    app.create_directories()
    app.set_up_signals()
    app.load_language()
    app.start_engine()
    app.notify_ready()
    app.configure_frameless_window()

    sys.exit(app.exec())
