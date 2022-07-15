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
import Qt.labs.settings
import components.player
import components.table
import pyobjects


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

        Settings {
            id: settings
            fileName: MpvqcFilePathsPyObject.settings
            category: "SplitView"
        }

        Item {
            id: playerContainer
            SplitView.fillHeight: true

            MpvqcPlayer {
                id: player
            }
        }

        Item {

            Component.onCompleted: {
                splitView.restoreState(settings.value("dimensions"))
            }

            Component.onDestruction: {
                settings.setValue("dimensions", splitView.saveState())
            }

            MpvqcCommentTable {
                focus: true
                anchors.fill: parent
            }
        }

    }

    Component.onCompleted: {
        eventRegistry.subscribe(eventRegistry.EventAddNewRow, disableFullScreen)
    }

    function disableFullScreen() {
        utils.exitFullScreen()
    }

}
