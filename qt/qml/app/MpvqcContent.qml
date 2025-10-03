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
    required property MpvqcAppHeaderViewController headerController
    required property MpvqcContentController contentController

    readonly property var mpvqcMpvPlayerPropertiesPyObject: mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject
    readonly property var mpvqcUtilityPyObject: mpvqcApplication.mpvqcUtilityPyObject

    function focusCommentTable(): void {
        _mpvqcCommentTable.forceActiveFocus();
    }

    Keys.onEscapePressed: root.contentController.requestDisableFullScreen()

    Keys.onPressed: event => root.contentController.onKeyPressed(event.key, event.modifiers, event.isAutoRepeat)

    SplitView {
        id: _splitView

        readonly property int tableContainerHeight: _tableContainer.height
        readonly property int tableContainerWidth: _tableContainer.width
        readonly property int draggerHeight: _splitView.height - _player.height - tableContainerHeight
        readonly property int draggerWidth: _splitView.width - _player.width - tableContainerWidth

        focus: true
        anchors.fill: root.contentItem
        orientation: root.contentController.layoutOrientation

        MpvqcPlayerView {
            id: _player

            SplitView.minimumHeight: root.contentController.minContainerHeight
            SplitView.minimumWidth: root.contentController.minContainerWidth
            SplitView.fillHeight: true
            SplitView.fillWidth: true

            onAddNewCommentMenuRequested: root.contentController.openNewCommentMenuRequested()

            onToggleFullScreenRequested: root.contentController.requestToggleFullScreen()
        }

        Column {
            id: _tableContainer

            visible: !root.mpvqcApplication.fullscreen

            SplitView.minimumHeight: root.contentController.minContainerHeight
            SplitView.minimumWidth: root.contentController.minContainerWidth

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

                controller: MpvqcFooterViewController {
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

        commentTypes: root.contentController.commentTypes

        function _adjustPosition(): void {
            const isMirrored = root.mpvqcApplication.LayoutMirroring.enabled;
            const global = root.mpvqcUtilityPyObject.cursorPosition;
            const local = _commentMenu.parent.mapFromGlobal(global);
            _commentMenu.x = isMirrored ? local.x - width : local.x;
            _commentMenu.y = local.y;
        }

        onAboutToShow: {
            _adjustPosition();
            root.contentController.pausePlayer();
        }

        onCommentTypeChosen: commentType => {
            root.contentController.requestDisableFullScreen();
            root.contentController.addNewEmptyComment(commentType);
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
            root.contentController.requestResizeAppWindow(width, height);
        }

        onSplitViewTableSizeRequested: (width, height) => {
            _tableContainer.setPreferredSizes(width, height);
        }
    }

    Connections {
        target: root.headerController

        function onResetAppStateRequested(): void {
            root.contentController.resetAppState();
        }

        function onSaveQcDocumentsRequested(): void {
            root.contentController.save();
        }

        function onSaveQcDocumentsAsRequested(): void {
            root.contentController.saveAs();
        }

        function onResizeVideoRequested(): void {
            _videoResizer.recalculateSizes();
        }
    }

    Connections {
        target: root.contentController

        function onOpenNewCommentMenuRequested(): void {
            _commentMenu.popup();
        }

        function onAddNewCommentRequested(commentType: string): void {
            _mpvqcCommentTable.addNewComment(commentType);
        }

        function onSplitViewTableSizeRequested(width: int, height: int): void {
            _tableContainer.setPreferredSizes(width, height);
        }
    }

    Component.onCompleted: {
        const preferred = root.contentController.preferredSplitSizes(_splitView.width, _splitView.height);
        _tableContainer.setPreferredSizes(preferred.width, preferred.height);
    }
}
