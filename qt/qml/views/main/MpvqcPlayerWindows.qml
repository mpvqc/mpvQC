// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

import pyobjects

WindowContainer {
    window: MpvWindowPyObject {
        flags: Qt.FramelessWindowHint | Qt.WindowDoesNotAcceptFocus | Qt.WindowTransparentForInput
        color: "black"
    }
}
