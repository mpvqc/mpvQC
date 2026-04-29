# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
import os
import pathlib
import sys

from PySide6.QtCore import QCoreApplication, QObject, Qt, Slot
from PySide6.QtQml import QQmlEngine
from PySide6.QtQuickTest import QUICK_TEST_MAIN_WITH_SETUP

import testqml.bridge  # noqa: F401, registers MpvqcTestBridge
from mpvqc import startup
from testqml.injections import TEMP_ROOT, configure_injections


# noinspection PyPep8Naming
class MpvqcTestSetup(QObject):
    @Slot(QQmlEngine)
    def qmlEngineAvailable(self, engine: QQmlEngine) -> None:
        import testqml.rc_project  # noqa: F401

        startup.configure_qt_application_data()
        startup.configure_qt_settings()
        # startup.configure_logging()
        configure_injections()
        startup.configure_environment_variables()
        startup.import_mpvqc_bindings()

        engine.rootContext().setContextProperty("mpvqcTestMode", True)


def parse_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="testqml")
    parser.add_argument(
        "--target",
        help="Run a single file by name (matches anywhere under qt/qml/).",
    )
    return parser.parse_args()


def resolve_input(args: argparse.Namespace) -> str:
    if args.target:
        return resolve_target_file(args.target)
    return "qt/qml"


def resolve_target_file(file_part: str) -> str:
    if file_part.endswith(".qml") and pathlib.Path(file_part).is_file():
        return file_part
    basename = file_part if file_part.endswith(".qml") else f"{file_part}.qml"
    matches = sorted(str(p) for p in pathlib.Path("qt/qml").rglob(basename))
    if not matches:
        msg = f"No test file found matching '{file_part}'"
        raise SystemExit(msg)
    if len(matches) > 1:
        joined = ", ".join(matches)
        msg = f"Ambiguous target '{file_part}', matches: {joined}"
        raise SystemExit(msg)
    return matches[0]


def main() -> int:
    os.environ["QT_QUICK_CONTROLS_STYLE"] = "Material"
    os.environ["QT_QUICK_CONTROLS_MATERIAL_VARIANT"] = "Dense"
    os.environ["MPVQC_DEBUG"] = "1"

    args = parse_cli()
    input_path = resolve_input(args)

    print(f"Storing temporary test data in {TEMP_ROOT}", flush=True)

    # Always work with Qt internal file dialogs in tests (less variation -> hopefully more stable tests)
    QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs)

    qt_argv = [sys.argv[0]]

    # qt_argv += ["-silent"]
    # qt_argv += ["-eventdelay", "50"]

    qt_argv += ["-platform", "offscreen"]
    qt_argv += ["-input", input_path]

    return QUICK_TEST_MAIN_WITH_SETUP("qmltestrunner", MpvqcTestSetup, argv=qt_argv)


if __name__ == "__main__":
    sys.exit(main())
