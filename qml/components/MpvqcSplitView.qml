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
import settings


FocusScope {
    id: focusScope

    Connections {
        target: appWindow

        function onDisplayVideoFullScreenChanged() {
            state = appWindow.displayVideoFullScreen ? "fullscreen" : "normal"
        }
    }

    states: [
        State { name: "fullscreen"; ParentChange { target: player; parent: focusScope } },
        State { name: "normal"; ParentChange { target: player; parent: playerContainer } }
    ]

    SplitView {
        id: splitView
        anchors.fill: parent
        orientation: Qt.Vertical

        Item {
            id: playerContainer
            SplitView.fillHeight: true

            MpvqcPlayer {
                id: player
                anchors.fill: parent
            }
        }

        Item {

            Component.onCompleted: {
                splitView.restoreState(MpvqcSettings.dimensions)
            }

            Component.onDestruction: {
                MpvqcSettings.dimensions = splitView.saveState()
            }

            MpvqcCommentTable {
                focus: true
                anchors.fill: parent
            }
        }

    }

    Connections {
        target: globalEvents

        function onNewCommentRequested() {
            disableFullScreen()
        }
    }

    function disableFullScreen() {
        utils.exitFullScreen()
    }

}
