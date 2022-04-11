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
import QtQuick.Layouts
import pyobjects


MpvPlayerPyObject {

    id: mpv
    anchors.fill: parent

    MouseArea {
        id: mouseArea

        anchors.fill: parent
        acceptedButtons: Qt.LeftButton | Qt.MiddleButton | Qt.RightButton
        hoverEnabled: true

        onPositionChanged: event => {
            mpv.move_mouse(event.x, event.y)
        }

        onWheel: event => {
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

        onPressed: event => {
            const button = event.button
            if (button === Qt.LeftButton) {
                mpv.press_mouse_left()
            } else if (button === Qt.MiddleButton) {
                mpv.press_mouse_middle()
            } else if (button === Qt.RightButton) {
                mpv.onRightMouseButtonClicked()
            }
        }

        onReleased: event => {
            const button = event.button
            if (button === Qt.LeftButton) {
                mpv.release_mouse_left()
            }
        }

        onDoubleClicked: event => {
            const button = event.button
            if (button === Qt.LeftButton) {
                console.log("todo: full screen on double clicked left button")
            }  else if (button === Qt.MiddleButton) {
                mpv.press_mouse_middle()
            }
        }

    }

    function onRightMouseButtonClicked() {
        eventRegistry.produce(eventRegistry.EventRequestNewComment)
    }

    Component.onCompleted: {
        eventRegistry.register(eventRegistry.EventRequestNewComment, () => mpv.pause())
        eventRegistry.register(eventRegistry.EventJumpToVideoPosition, (seconds) => mpv.jump_to(seconds))
    }
}
