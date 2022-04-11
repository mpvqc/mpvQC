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
import pyobjects
import "event-registry.js" as EventRegistry
import "window-operations.js" as WindowOperations


ApplicationWindow {
    id: window

    property ApplicationWindow appWindow: window
    property var windowOperations: WindowOperations
    property var eventRegistry: EventRegistry
    property var appTheme: SettingsPyObject.theme
    property var appThemeColorAccent: SettingsPyObject.theme_accent
    property int windowBorder: 5

    visible: true
    width: 1290
    height: 970
    flags: Qt.FramelessWindowHint

    Material.theme: appTheme
    Material.accent: appThemeColorAccent

    LayoutMirroring.enabled: TranslationPyObject.rtl_enabled
    LayoutMirroring.childrenInherit: true

    WindowBorderMouseCurser {

        borderWidth: windowBorder
        anchors.fill: parent

    }

    WindowResizeHandler {

        borderWidth: windowBorder

    }

    PageMain {

        anchors.fill: parent
        anchors.margins: appWindow.visibility === Window.Windowed ? windowBorder : 0

    }

}
