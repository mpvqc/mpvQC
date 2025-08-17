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

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

import "../footer"
import "../header"
import "../player"
import "../table"

Page {
    id: root

    required property var mpvqcApplication

    readonly property var mpvqcManager: mpvqcApplication.mpvqcManager
    readonly property var mpvqcMpvPlayerPropertiesPyObject: mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject
    readonly property var mpvqcSettings: mpvqcApplication.mpvqcSettings
    readonly property var mpvqcUtilityPyObject: mpvqcApplication.mpvqcUtilityPyObject
    readonly property var supportedSubtitleFileExtensions: mpvqcUtilityPyObject.subtitleFileExtensions

    readonly property int minContainerHeight: 200
    readonly property int minContainerWidth: 500
    readonly property real defaultSplitRatio: 0.4

    readonly property alias mpvqcCommentTable: _table.publicInterface

    signal addNewCommentMenuRequested
    signal appWindowSizeRequested(width: int, height: int)
    signal customMpvCommandRequested(key: int, modifiers: int)
    signal disableFullScreenRequested
    signal toggleFullScreenRequested

    header: MpvqcHeader {
        mpvqcApplication: root.mpvqcApplication
        width: root.width

        onResizeVideoTriggered: _videoResizer.recalculateSizes()
    }

    function applySaneDefaultSplitViewSize(): void {
        const prefHeight = _splitView.height * defaultSplitRatio;
        const prefWidth = _splitView.width * defaultSplitRatio;
        _tableContainer.setPreferredSizes(prefWidth, prefHeight);
    }

    SplitView {
        id: _splitView

        readonly property int tableContainerHeight: _tableContainer.height
        readonly property int tableContainerWidth: _tableContainer.width
        readonly property int draggerHeight: _splitView.height - _playerLoader.height - tableContainerHeight
        readonly property int draggerWidth: _splitView.width - _playerLoader.width - tableContainerWidth

        focus: true
        anchors.fill: root.contentItem
        orientation: root.mpvqcSettings.layoutOrientation

        Component {
            id: _linuxPlayer

            MpvqcPlayerLinux {
                mpvqcApplication: root.mpvqcApplication
                anchors.fill: parent
            }
        }

        Component {
            id: _windowsPlayer

            MpvqcPlayerWindows {
                mpvqcApplication: root.mpvqcApplication
                anchors.fill: parent
            }
        }

        Loader {
            id: _playerLoader

            SplitView.minimumHeight: root.minContainerHeight
            SplitView.minimumWidth: root.minContainerWidth
            SplitView.fillHeight: true
            SplitView.fillWidth: true

            sourceComponent: Qt.platform.os === "windows" ? _windowsPlayer : _linuxPlayer
        }

        Column {
            id: _tableContainer

            visible: !root.mpvqcApplication.fullscreen

            SplitView.minimumHeight: root.minContainerHeight
            SplitView.minimumWidth: root.minContainerWidth

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

    Keys.onEscapePressed: {
        root.disableFullScreenRequested();
    }

    Keys.onPressed: event => {
        const key = event.key;
        const modifiers = event.modifiers;

        const noModifier = modifiers === Qt.NoModifier;
        const ctrlModifier = modifiers & Qt.ControlModifier;
        const plainPress = !event.isAutoRepeat && noModifier;

        if (key === Qt.Key_E && plainPress) {
            root.addNewCommentMenuRequested();
            return;
        }

        if (key === Qt.Key_F && plainPress) {
            root.toggleFullScreenRequested();
            return;
        }

        const preventReachingCustomUserCommands = //
        key === Qt.Key_Up  //
        || key === Qt.Key_Down //
        || (key === Qt.Key_Return && noModifier) //
        || (key === Qt.Key_Escape && noModifier) //
        || (key === Qt.Key_Delete && noModifier) //
        || (key === Qt.Key_Backspace && noModifier) //
        || (key === Qt.Key_F && ctrlModifier) //
        || (key === Qt.Key_C && ctrlModifier) //
        || (key === Qt.Key_Z && ctrlModifier);

        if (preventReachingCustomUserCommands) {
            return;
        }

        root.customMpvCommandRequested(key, modifiers);
    }

    MpvqcFileDropArea {
        anchors.fill: _splitView
        supportedSubtitleFileExtensions: root.supportedSubtitleFileExtensions

        onFilesDropped: (documents, videos, subtitles) => {
            root.mpvqcManager.open(documents, videos, subtitles);
        }
    }

    MpvqcResizeHandler {
        id: _videoResizer

        headerHeight: root.header.height
        appBorderSize: root.mpvqcApplication.windowBorder
        videoWidth: root.mpvqcMpvPlayerPropertiesPyObject.scaledWidth
        videoHeight: root.mpvqcMpvPlayerPropertiesPyObject.scaledHeight

        isAppFullScreen: root.mpvqcApplication.fullscreen
        isAppMaximized: root.mpvqcApplication.maximized
        videoPath: root.mpvqcMpvPlayerPropertiesPyObject.path

        splitViewOrientation: _splitView.orientation
        splitViewHandleWidth: _splitView.draggerWidth
        splitViewHandleHeight: _splitView.draggerHeight
        splitViewTableContainerWidth: _splitView.tableContainerWidth
        splitViewTableContainerHeight: _splitView.tableContainerHeight

        onAppWindowSizeRequested: (width, height) => {
            root.appWindowSizeRequested(width, height);
        }

        onSplitViewTableSizeRequested: (width, height) => {
            _tableContainer.setPreferredSizes(width, height);
        }
    }

    Connections {
        target: root.mpvqcCommentTable

        function onCommentCountChanged(): void {
            // we effectively force a redraw of the table here. if we don't do this and delete the last row
            // in the table, the table will not rerender completely and there might be color artifacts of the
            // alternating row colors
            _footer.height += 1;
            _footer.height -= 1;
        }
    }

    Component.onCompleted: root.applySaneDefaultSplitViewSize()
}
