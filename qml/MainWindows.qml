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

    x: appWindow.x
    y: appWindow.y
    width: appWindow.width
    height: appWindow.height

    minimumWidth: appWindow.minimumWidth
    minimumHeight: appWindow.minimumHeight

    flags: Qt.FramelessWindowHint | Qt.Window
    visibility: Window.Windowed

    Material.theme: appWindow.mpvqcSettings.theme
    Material.background: appWindow.Material.background
    Material.foreground: appWindow.Material.foreground
    Material.accent: appWindow.mpvqcSettings.primary

    onActiveFocusItemChanged: {
        if (activeFocusItem != null) {
            // Due to us being required to stack 3 windows, this outer window can obtain focus. This is the case when
            // the video player window was clicked using the mouse. As soon as this happens, we refocus the appWindow
            appWindow.requestActivate()
            appWindow.focusCommentTable()
        }
    }

    WindowContainer {
        x: appWindow.playerArea.globalCoordinate.x
        y: appWindow.playerArea.globalCoordinate.y
        width: appWindow.playerArea.width
        height: appWindow.playerArea.height

        window: MpvWindowPyObject {
            flags: Qt.FramelessWindowHint | Qt.WindowDoesNotAcceptFocus | Qt.WindowTransparentForInput
            color: "black"
        }

        Main {
            id: appWindow

            objectName: 'mpvqcControlsWindow'
            color: 'transparent'

            onClosing: event => {
                if (event.accepted) {
                    Qt.quit()
                }
            }

            function forceRerender() {
                appWindow.height += 1; appWindow.width += 1
                appWindow.height -= 1; appWindow.width -= 1
                appWindow.x += 1; appWindow.y += 1
                appWindow.x -= 1; appWindow.y -= 1
            }

            onVisibilityChanged: {
                root.visibility = appWindow.visibility

                if (appWindow.visibility !== Window.FullScreen) {
                    appWindow.forceRerender()
                }
            }
        }
    }

}
