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

import "../footer2"
import "../player"
import "../table"

FocusScope {
    id: root

    required property var mpvqcApplication

    readonly property var mpvqcSettings: mpvqcApplication.mpvqcSettings

    readonly property alias mpvqcCommentTable: _table.publicInterface
    readonly property alias playerContainer: _playerContainer
    readonly property alias tableContainer: _tableContainer
    readonly property alias playerArea: _player

    readonly property int tableContainerHeight: _tableContainer.height
    readonly property int tableContainerWidth: _tableContainer.width
    readonly property int draggerHeight: _splitView.height - _playerContainer.height - tableContainerHeight
    readonly property int draggerWidth: _splitView.width - _playerContainer.width - tableContainerWidth
    readonly property int orientation: _splitView.orientation

    state: mpvqcApplication.fullscreen ? "fullscreen" : "normal"
    states: [
        State {
            name: "fullscreen"
            ParentChange { target: _player; parent: root }
            PropertyChanges { _tableContainer { visible: false } }
        },
        State {
            name: "normal"
            ParentChange { target: _player; parent: _playerContainer }
            PropertyChanges { _tableContainer { visible: true } }
        }
    ]

    function applySaneDefaultSplitViewSize() {
        const prefHeight = _splitView.height * 0.4;
        const prefWidth = _splitView.width * 0.4;
        _tableContainer.setPreferredSizes(prefWidth, prefHeight);
    }

    function setPreferredTableSize(width: int, height: int): void {
        _tableContainer.setPreferredSizes(width, height);
    }

    SplitView {
        id: _splitView

        anchors.fill: root
        orientation: root.mpvqcSettings.layoutOrientation

        Item {
            id: _playerContainer

            SplitView.minimumHeight: 200
            SplitView.minimumWidth: 400

            SplitView.fillHeight: true
            SplitView.fillWidth: true

            MpvqcPlayer {
                id: _player

                mpvqcApplication: root.mpvqcApplication
                anchors.fill: parent // qmllint disable unqualified
            }
        }

        Column {
            id: _tableContainer

            SplitView.minimumHeight: 200
            SplitView.minimumWidth: 400

            function setPreferredSizes(width: int, height: int): void {
                SplitView.preferredWidth = width;
                SplitView.preferredHeight = height;
            }

            MpvqcTable {
                id: _table

                mpvqcApplication: root.mpvqcApplication
                focus: true
                width: _tableContainer.width
                height: _tableContainer.height - _footer.height
            }

            MpvqcFooter {
                id: _footer

                mpvqcApplication: root.mpvqcApplication
                width: _tableContainer.width
            }
        }
    }

    Connections {
        target: root.mpvqcSettings

        function onLayoutOrientationChanged() {
            _forceSplitViewLayoutRefresh();
            root.applySaneDefaultSplitViewSize();
        }

        function _forceSplitViewLayoutRefresh() {
            const bottomElement = _splitView.takeItem(1);
            _splitView.addItem(bottomElement);
        }
    }

    Connections {
        target: root.mpvqcCommentTable

        function onCommentCountChanged() {
            // we effectively force a redraw of the table here. if we don't do this and delete the last row
            // in the table, the table will not rerender completely and there might be color artifacts of the
            // alternating row colors
            _footer.height += 1;
            _footer.height -= 1;
        }
    }

    Component.onCompleted: {
        root.applySaneDefaultSplitViewSize();
    }
}
