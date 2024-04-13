/*
mpvQC

Copyright (C) 2024 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

import QtQuick
import QtQuick.Controls.Material

import pyobjects


ApplicationWindow {
    id: root

    x: app.x
    y: app.y
    width: app.width
    height: app.height

    minimumWidth: app.minimumWidth
    minimumHeight: app.minimumHeight

    flags: Qt.FramelessWindowHint | Qt.Window
    visibility: Window.Windowed

    Material.theme: app.mpvqcSettings.theme
    Material.accent: app.mpvqcSettings.primary
    Material.primary: app.mpvqcSettings.primary

    WindowContainer {
        x: app.playerArea.applicationWideTopLeft.x
        y: app.playerArea.applicationWideTopLeft.y
        width: app.playerArea.width
        height: app.playerArea.height

        window: MpvWindowPyObject {
            flags: Qt.FramelessWindowHint | Qt.WindowDoesNotAcceptFocus | Qt.WindowTransparentForInput
            color: "black"
        }

        Main {
            id: app

            objectName: 'mpvqcControlsWindow'
            color: 'transparent'

            onClosing: event => {
                if (event.accepted) {
                    Qt.quit()
                }
            }

            onVisibilityChanged: {
                root.visibility = app.visibility
            }
        }
    }

}
