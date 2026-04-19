# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later


from typing import Never


def perform_startup() -> Never:
    configure_qt_application_data()
    configure_qt_style()
    configure_qt_settings()
    configure_logging()
    configure_dependency_injection()
    configure_environment_variables()

    import_mpvqc_bindings()

    start_application()


def configure_qt_application_data() -> None:
    from PySide6.QtCore import QCoreApplication

    from mpvqc.build import get_build_info

    app = get_build_info().application
    QCoreApplication.setApplicationName(app.name)
    QCoreApplication.setOrganizationName(app.organization)
    QCoreApplication.setOrganizationDomain(app.domain)
    QCoreApplication.setApplicationVersion(app.version)


def configure_qt_style() -> None:
    from PySide6.QtQuickControls2 import QQuickStyle

    QQuickStyle.setStyle("MpvqcStyle")
    QQuickStyle.setFallbackStyle("Material")


def configure_qt_settings() -> None:
    from PySide6.QtCore import QSettings

    QSettings.setDefaultFormat(QSettings.Format.IniFormat)


def configure_logging() -> None:
    from PySide6 import QtCore

    from mpvqc.logging_utils import qt_log_handler, setup_mpvqc_logging

    setup_mpvqc_logging()
    QtCore.qInstallMessageHandler(qt_log_handler())


def configure_dependency_injection() -> None:
    from mpvqc.injections import configure_injections

    configure_injections()


def configure_environment_variables() -> None:
    import os

    os.environ["QT_QUICK_CONTROLS_MATERIAL_VARIANT"] = "Dense"

    # Requirement for mpv
    os.environ["LC_NUMERIC"] = "C"


def import_mpvqc_bindings() -> None:
    import mpvqc.enums  # noqa: F401
    import mpvqc.models  # noqa: F401
    import mpvqc.utility  # noqa: F401
    import mpvqc.viewmodels  # noqa: F401
    import mpvqc.views  # noqa: F401


def start_application() -> Never:
    import sys

    from mpvqc.application import MpvqcApplication

    app = MpvqcApplication(sys.argv)
    app.configure()
    app.start()

    sys.exit(app.exec())
