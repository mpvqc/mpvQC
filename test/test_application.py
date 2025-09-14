# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest
from PySide6.QtCore import QObject, QUrl

QML = """
    import QtQuick
    import QtQuick.Controls

    ApplicationWindow {
        visible: false; width: 50; height: 50

        Button { objectName: "button-click-me"; text: "Click Me" }
    }
"""


def test_find_object(qt_app):
    qt_app._engine.loadData(QML.encode(), QUrl())
    obj = qt_app.find_object(QObject, "button-click-me")
    assert obj

    with pytest.raises(ValueError):  # noqa: PT011
        qt_app.find_object(QObject, "other-button-that-does-not-exist")
