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

import player
import table


FocusScope {
    id: root

    required property var mpvqcApplication

    readonly property var mpvqcSettings: mpvqcApplication.mpvqcSettings

    readonly property alias mpvqcCommentTable: _commentTable.mpvqcCommentTable
    readonly property alias playerContainer: _playerContainer
    readonly property alias splitView: _splitView
    readonly property alias tableContainer: _tableContainer

    readonly property int tableContainerHeight: _tableContainer.height
    readonly property int draggerHeight: _splitView.height - _playerContainer.height - tableContainerHeight

    states: [
        State { name: "fullscreen"; ParentChange { target: _player; parent: root } },
        State { name: "normal"; ParentChange { target: _player; parent: _playerContainer } }
    ]

    function setPreferredTableSize(width: int, height: int): void {
        _tableContainer.setPreferredSizes(width, height)
    }

    Connections {
        target: mpvqcApplication

        function onFullscreenChanged() {
            state = mpvqcApplication.fullscreen ? "fullscreen" : "normal"
        }
    }

    SplitView {
        id: _splitView

        anchors.fill: root
        orientation: Qt.Vertical

        Item {
            id: _playerContainer

            SplitView.fillHeight: true

            MpvqcPlayer {
                id: _player

                mpvqcApplication: root.mpvqcApplication
                anchors.fill: parent
            }
        }

        Item {
            id: _tableContainer

            function setPreferredSizes(width: int, height: int): void {
                SplitView.preferredWidth = width
                SplitView.preferredHeight = height
            }

            MpvqcCommentTable {
                id: _commentTable

                mpvqcApplication: root.mpvqcApplication
                focus: true
                anchors.fill: parent
            }
        }

    }

    Component.onCompleted: {
        _splitView.restoreState(root.mpvqcSettings.dimensions)
    }

    Component.onDestruction: {
        root.mpvqcSettings.dimensions = _splitView.saveState()
    }

}