// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma Singleton

import QtQuick

import pyobjects

QtObject {

    readonly property MpvqcWindowPropertiesBackend windowPropertiesBackend: MpvqcWindowPropertiesBackend {}

    readonly property int appWidth: windowPropertiesBackend.appWidth
    readonly property int appHeight: windowPropertiesBackend.appHeight
    readonly property bool isFullscreen: windowPropertiesBackend.isFullscreen
    readonly property bool isMaximized: windowPropertiesBackend.isMaximized
}
