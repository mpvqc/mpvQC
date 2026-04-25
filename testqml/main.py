# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os

os.environ["QT_QUICK_CONTROLS_STYLE"] = "Material"
os.environ["QT_QUICK_CONTROLS_MATERIAL_VARIANT"] = "Dense"

import sys

from PySide6.QtCore import QObject, Slot
from PySide6.QtQml import QQmlEngine
from PySide6.QtQuickTest import QUICK_TEST_MAIN_WITH_SETUP

import testqml.bridge  # noqa: F401, registers MpvqcTestBridge
from mpvqc import startup
from testqml.injections import configure_injections


# noinspection PyPep8Naming
class MpvqcTestSetup(QObject):
    @Slot(QQmlEngine)
    def qmlEngineAvailable(self, engine: QQmlEngine) -> None:
        import testqml.rc_project  # noqa: F401

        startup.configure_qt_application_data()
        startup.configure_qt_settings()
        configure_injections()
        startup.configure_environment_variables()
        startup.import_mpvqc_bindings()

        engine.rootContext().setContextProperty("mpvqcTestMode", True)


def main() -> int:
    sys.argv += ["-platform", "offscreen"]  # Disabled: run with a visible window so events are observable
    sys.argv += ["-silent"]
    sys.argv += ["-input", "qt/qml/tst_MpvqcApplicationContent.qml"]
    # sys.argv += ["-eventdelay", "50"]  # Slow events down so the test is watchable

    return QUICK_TEST_MAIN_WITH_SETUP("qmltestrunner", MpvqcTestSetup, argv=sys.argv)


if __name__ == "__main__":
    sys.exit(main())
