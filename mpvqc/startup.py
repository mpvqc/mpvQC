# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later


from typing import Never


def perform_startup(process_started_at: float) -> Never:
    configure_qt_application_data()
    configure_qt_style()
    configure_qt_settings()
    configure_logging()
    configure_dependency_injection()
    configure_environment_variables()
    pin_windows_ui_library()

    register_qml_types()

    start_application(process_started_at)


def configure_qt_application_data() -> None:
    from PySide6.QtGui import QGuiApplication

    from mpvqc.build import get_build_info

    build = get_build_info()
    QGuiApplication.setApplicationName(build.name)
    QGuiApplication.setDesktopFileName(build.app_id)
    QGuiApplication.setOrganizationName(build.organization)
    QGuiApplication.setOrganizationDomain(build.domain)
    QGuiApplication.setApplicationVersion(build.version)


def configure_qt_style() -> None:
    from PySide6.QtQuickControls2 import QQuickStyle

    QQuickStyle.setStyle("MpvqcStyle")
    QQuickStyle.setFallbackStyle("Material")


def configure_qt_settings() -> None:
    from PySide6.QtCore import QSettings

    QSettings.setDefaultFormat(QSettings.Format.IniFormat)


def configure_logging() -> None:
    from mpvqc.logging_utils import setup_mpvqc_logging

    setup_mpvqc_logging()


def configure_dependency_injection() -> None:
    from mpvqc.injections import configure_injections

    configure_injections()


def configure_environment_variables() -> None:
    import os

    os.environ["QT_QUICK_CONTROLS_MATERIAL_VARIANT"] = "Dense"

    # Requirement for mpv
    os.environ["LC_NUMERIC"] = "C"


def pin_windows_ui_library() -> None:
    import sys

    if sys.platform != "win32":
        return

    import ctypes

    # mpv's and Qt's shutdown do not go well together: Windows may unload this
    # library while Qt still holds pointers into it, crashing on exit. An extra
    # reference keeps it loaded until the process ends.
    # pyrefly: ignore [missing-attribute]
    ctypes.WinDLL("Windows.UI.dll")


def register_qml_types() -> None:
    import mpvqc.dialogs  # ruff: ignore[unused-import]
    import mpvqc.enums  # ruff: ignore[unused-import]
    import mpvqc.models  # ruff: ignore[unused-import]
    import mpvqc.viewmodels  # ruff: ignore[unused-import]
    from mpvqc import appearance, comments, exporting, importing, player, window

    appearance.register_qml_types()
    comments.register_qml_types()
    exporting.register_qml_types()
    importing.register_qml_types()
    player.register_qml_types()
    window.register_qml_types()


def start_application(process_started_at: float) -> Never:
    import sys

    from PySide6.QtCore import QThreadPool

    from mpvqc.application import MpvqcApplication

    app = MpvqcApplication(sys.argv)
    app.configure()

    app.about_to_show.connect(remove_nuitka_splash_screen)
    app.first_frame_rendered.connect(lambda: log_startup_time(process_started_at))

    app.start()

    exit_code = app.exec()
    # A pool worker still calling into Python during interpreter teardown segfaults
    QThreadPool.globalInstance().waitForDone()
    sys.exit(exit_code)


def log_startup_time(process_started_at: float) -> None:
    import logging
    import time

    elapsed_ms = (time.perf_counter() - process_started_at) * 1000
    logging.getLogger(__name__).info("Startup took %.0f ms", elapsed_ms)


def remove_nuitka_splash_screen() -> None:
    import os
    import tempfile
    from pathlib import Path

    parent_pid = os.environ.get("NUITKA_ONEFILE_PARENT")
    if parent_pid is None:
        return

    splash_filename = Path(tempfile.gettempdir()) / f"onefile_{parent_pid}_splash_feedback.tmp"

    if splash_filename.exists():
        splash_filename.unlink()
