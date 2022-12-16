/*
mpvQC

Copyright (C) 2022 mpvQC developers

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


MouseArea {
    id: root

    required property var mpvqcApplication
    property var mpv: mpvqcApplication.mpvqcMpvPlayerPyObject

    property bool showCursor: true

    property var cursorTimer: Timer {
        running: root.showCursor && mpvqcApplication.fullscreen && root.containsMouse
        repeat: true
        interval: 2000

        onTriggered: {
            root.showCursor = false
        }
    }

    signal rightMouseButtonPressed()

    acceptedButtons: Qt.LeftButton | Qt.MiddleButton | Qt.RightButton
    cursorShape: !root.showCursor && mpvqcApplication.fullscreen ? Qt.BlankCursor : Qt.ArrowCursor
    hoverEnabled: true

    onPositionChanged: (event) => {
        root.showCursor = true
        mpv.move_mouse(event.x, event.y)
    }

    onWheel: (event) => {
        const delta = event.angleDelta
        if (delta.y === 0 || delta.x !== 0) {
            return
        }
        if (delta.y > 0) {
            mpv.scroll_up()
        } else {
            mpv.scroll_down()
        }
    }

    onPressed: (event) => {
        const button = event.button
        if (button === Qt.LeftButton) {
            mpv.press_mouse_left()
        } else if (button === Qt.MiddleButton) {
            mpv.press_mouse_middle()
        } else if (button === Qt.RightButton) {
            root.rightMouseButtonPressed()
        }
    }

    onReleased: (event) => {
        const button = event.button
        if (button === Qt.LeftButton) {
            mpv.release_mouse_left()
        }
    }

    onDoubleClicked: (event) => {
        const button = event.button
        if (button === Qt.LeftButton) {
            root.mpvqcApplication.toggleFullScreen()
        }
    }

}
