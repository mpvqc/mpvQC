// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

import pyobjects

import "../views"
import "../table"

Page {
    id: root

    required property var mpvqcApplication
    required property MpvqcAppHeaderViewModel headerViewModel
    required property MpvqcContentViewModel contentViewModel

    readonly property var mpvqcMpvPlayerPropertiesPyObject: mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject

    function focusCommentTable(): void {
        _mpvqcCommentTable.forceActiveFocus();
    }

    Keys.onEscapePressed: root.contentViewModel.requestDisableFullScreen()

    Keys.onPressed: event => root.contentViewModel.onKeyPressed(event.key, event.modifiers, event.isAutoRepeat)

    SplitView {
        id: _splitView

        readonly property int tableContainerHeight: _tableContainer.height
        readonly property int tableContainerWidth: _tableContainer.width
        readonly property int draggerHeight: _splitView.height - _player.height - tableContainerHeight
        readonly property int draggerWidth: _splitView.width - _player.width - tableContainerWidth

        focus: true
        anchors.fill: root.contentItem
        orientation: root.contentViewModel.layoutOrientation

        MpvqcPlayerView {
            id: _player

            SplitView.minimumHeight: root.contentViewModel.minContainerHeight
            SplitView.minimumWidth: root.contentViewModel.minContainerWidth
            SplitView.fillHeight: true
            SplitView.fillWidth: true

            onAddNewCommentMenuRequested: root.contentViewModel.openNewCommentMenuRequested()

            onToggleFullScreenRequested: root.contentViewModel.requestToggleFullScreen()
        }

        Column {
            id: _tableContainer

            visible: !root.mpvqcApplication.fullscreen

            SplitView.minimumHeight: root.contentViewModel.minContainerHeight
            SplitView.minimumWidth: root.contentViewModel.minContainerWidth

            function setPreferredSizes(width, height) {
                SplitView.preferredWidth = width;
                SplitView.preferredHeight = height;
            }

            MpvqcTable {
                id: _mpvqcCommentTable

                mpvqcApplication: root.mpvqcApplication
                focus: true
                width: _tableContainer.width
                height: _tableContainer.height - _footer.height

                onCommentCountChanged: {
                    // force a redraw to avoid leftover alternating row color artifacts
                    _footer.height += 1;
                    _footer.height -= 1;
                }
            }

            MpvqcFooterView {
                id: _footer

                viewModel: MpvqcFooterViewModel {
                    selectedCommentIndex: _mpvqcCommentTable.selectedCommentIndex
                    totalCommentCount: _mpvqcCommentTable.commentCount
                }

                width: _tableContainer.width
            }
        }
    }

    MpvqcFileDropArea {
        anchors.fill: _splitView
    }

    MpvqcNewCommentMenu {
        id: _commentMenu

        onCommentTypeChosen: commentType => {
            root.contentViewModel.requestDisableFullScreen();
            root.contentViewModel.addNewEmptyComment(commentType);
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
            root.contentViewModel.requestResizeAppWindow(width, height);
        }

        onSplitViewTableSizeRequested: (width, height) => {
            _tableContainer.setPreferredSizes(width, height);
        }
    }

    Connections {
        target: root.headerViewModel

        function onResizeVideoRequested(): void {
            _videoResizer.recalculateSizes();
        }
    }

    Connections {
        target: root.contentViewModel

        function onOpenNewCommentMenuRequested(): void {
            _commentMenu.popup();
        }

        function onAddNewCommentRequested(commentType: string): void {
            _mpvqcCommentTable.addNewComment(commentType);
        }
    }

    Component.onCompleted: {
        const sizes = root.contentViewModel.calculatePreferredSplitSizes(_splitView.width, _splitView.height);
        _tableContainer.setPreferredSizes(sizes.width, sizes.height);
    }
}
