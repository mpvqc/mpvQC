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
import pyobjects
import shared


MpvqcMpvFrameBufferObjectPyObject {
    id: root

    required property var mpvqcApplication

    property MpvqcNewCommentMenu newCommentMenu: MpvqcNewCommentMenu {
        mpvqcApplication: root.mpvqcApplication
    }

    MpvqcPlayerMouseArea {
        mpvqcApplication: root.mpvqcApplication
        anchors.fill: root

        onRightMouseButtonPressed: {
            newCommentMenu.popupMenu()
        }
    }

//    Connections {
//        target: qcManager
//
//        function onVideoImported(video) {
//            root.open_video(video)
//        }
//
//        function onSubtitlesImported(subtitles) {
//            root.open_subtitles(subtitles)
//        }
//    }
//
//    Connections {
//        target: globalEvents
//
//        function onCustomPlayerCommandRequested(command) {
//            executeCustomCommand(command)
//        }
//
//        function onNewCommentMenuRequested() {
//            pauseVideo()
//            showAddCommentMenu()
//        }
//
//        function onVideoPauseRequested() {
//            pauseVideo()
//        }
//
//        function onVideoPositionRequested(seconds) {
//            jumpToPostition(seconds)
//        }
//
//    }
//
//    function requestAddCommentMenu() {
//        globalEvents.requestNewCommentMenu()
//    }
//
//    function jumpToPostition(position) {
//        root.jump_to(position)
//    }
//
//    function pauseVideo() {
//        root.pause()
//    }
//
//    function executeCustomCommand(command) {
//        root.execute(command)
//    }
//
//    function showAddCommentMenu() {
//        const component = Qt.createComponent("MpvqcNewCommentMenu.qml")
//        const menu = component.createObject(appWindow)
//        menu.closed.connect(menu.destroy)
//        menu.itemClicked.connect(root.requestNewComment)
//        menu.popup()
//    }
//
//    function requestNewComment(commentType) {
//        globalEvents.requestNewComment(commentType)
//    }

}
