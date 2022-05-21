/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


import QtQuick
import QtQuick.Controls
import components
import handlers
import helpers
import manager
import pyobjects
import settings


ApplicationWindow {
    id: window
    visible: true
    width: 1290
    height: 970
    flags: Qt.FramelessWindowHint | Qt.Window
    Material.theme: appTheme
    Material.accent: displayableAccentColorFor(appThemeColorAccent)
    LayoutMirroring.enabled: Qt.application.layoutDirection === Qt.RightToLeft
    LayoutMirroring.childrenInherit: true

    property ApplicationWindow appWindow: window
    property MpvqcManager qcManager: MpvqcManager {}
    property var utils: MpvqcUtils
    property var eventRegistry: MpvqcEventRegistry
    property int appTheme: MpvqcSettings.theme
    property int appThemeColorAccent: MpvqcSettings.accent
    property int windowBorder: 5

    MpvqcWindowBorderMouseCurser {
        borderWidth: windowBorder
        anchors.fill: parent
    }

    MpvqcWindowResizeHandler {
        borderWidth: windowBorder
    }

    MpvqcMainPage {
        anchors.fill: parent
        anchors.margins: appWindow.visibility === Window.Windowed ? windowBorder : 0
    }

    Component.onCompleted: {
        TranslationPyObject.load_translation(MpvqcSettings.language)
    }

    function displayableAccentColorFor(color) {
        if (appTheme === Material.Light) {
            return color
        } else {
            return Qt.darker(Material.color(color), 1.10) // or Material.color(color, Material.Shade600)
        }
    }

}
