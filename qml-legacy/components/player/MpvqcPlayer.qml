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
import QtQuick.Controls
import QtQuick.Layouts
import pyobjects


MpvPlayerPyObject {
    id: mpv

    Timer {
        id: hideMouseCursorTimer
        running: appWindow.displayVideoFullScreen && mouseArea.containsMouse
        repeat: true
        interval: 2000

        onTriggered: {
            mouseArea.hideCursor = true
        }
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        acceptedButtons: Qt.LeftButton | Qt.MiddleButton | Qt.RightButton
        cursorShape: hideCursor && appWindow.displayVideoFullScreen ? Qt.BlankCursor : Qt.ArrowCursor
        hoverEnabled: true

        property bool hideCursor: false

        onPositionChanged: (event) => {
            hideCursor = false
            mpv.move_mouse(event.x, event.y)
            hideMouseCursorTimer.restart()
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
                mpv.requestAddCommentMenu()
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
                utils.toggleFullScreen()
            }
        }
    }

    Connections {
        target: qcManager

        function onVideoImported(video) {
            mpv.open_video(video)
        }

        function onSubtitlesImported(subtitles) {
            mpv.open_subtitles(subtitles)
        }
    }

    Connections {
        target: globalEvents

        function onCustomPlayerCommandRequested(command) {
            executeCustomCommand(command)
        }

        function onNewCommentMenuRequested() {
            pauseVideo()
            showAddCommentMenu()
        }

        function onVideoPauseRequested() {
            pauseVideo()
        }

        function onVideoPositionRequested(seconds) {
            jumpToPostition(seconds)
        }

    }

    function requestAddCommentMenu() {
        globalEvents.requestNewCommentMenu()
    }

    function jumpToPostition(position) {
        mpv.jump_to(position)
    }

    function pauseVideo() {
        mpv.pause()
    }

    function executeCustomCommand(command) {
        mpv.execute(command)
    }

    function showAddCommentMenu() {
        const component = Qt.createComponent("MpvqcAddCommentMenu.qml")
        const menu = component.createObject(appWindow)
        menu.closed.connect(menu.destroy)
        menu.itemClicked.connect(mpv.requestNewComment)
        menu.popup()
    }

    function requestNewComment(commentType) {
        globalEvents.requestNewComment(commentType)
    }

}
