// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

import pyobjects

import "../../utility"
import "../footer"
import "../player"
import "../table"

Page {
    id: root

    required property MpvqcContentViewModel viewModel
    required property int windowBorder

    readonly property int minContainerHeight: 200
    readonly property int minContainerWidth: 500
    readonly property real defaultSplitRatio: 0.4

    signal toggleFullScreenRequested
    signal disableFullScreenRequested
    signal appWindowSizeRequested(width: int, height: int)

    function focusCommentTable(): void {
        _mpvqcCommentTable.forceActiveFocus();
    }

    function resizeVideo(): void {
        _videoResizer.recalculateSizes();
    }

    Keys.onEscapePressed: root.disableFullScreenRequested()

    Keys.onPressed: event => _keyHandler.handleKeyPress(event)

    MpvqcContentKeyHandler {
        id: _keyHandler

        onOpenCommentMenuRequested: _commentMenu.popup()
        onToggleFullScreenRequested: root.toggleFullScreenRequested()
        onForwardKeyToPlayerRequested: (key, modifiers) => root.viewModel.forwardKeyToPlayer(key, modifiers)
    }

    SplitView {
        id: _splitView
        objectName: "applicationSplitView"

        readonly property int tableContainerHeight: _tableContainer.height
        readonly property int tableContainerWidth: _tableContainer.width
        readonly property int draggerHeight: _splitView.height - _player.height - tableContainerHeight
        readonly property int draggerWidth: _splitView.width - _player.width - tableContainerWidth

        focus: true
        anchors.fill: root.contentItem
        orientation: root.viewModel.layoutOrientation

        MpvqcPlayerView {
            id: _player

            SplitView.minimumHeight: root.minContainerHeight
            SplitView.minimumWidth: root.minContainerWidth
            SplitView.fillHeight: true
            SplitView.fillWidth: true

            onAddNewCommentMenuRequested: _commentMenu.popup()

            onToggleFullScreenRequested: root.toggleFullScreenRequested()
        }

        Column {
            id: _tableContainer

            visible: !MpvqcWindowUtility.isFullscreen

            SplitView.minimumHeight: root.minContainerHeight
            SplitView.minimumWidth: root.minContainerWidth

            function setPreferredSizes(width, height) {
                SplitView.preferredWidth = width;
                SplitView.preferredHeight = height;
            }

            MpvqcTableView {
                id: _mpvqcCommentTable

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

                width: _tableContainer.width
                selectedCommentIndex: _mpvqcCommentTable.selectedCommentIndex
                totalCommentCount: _mpvqcCommentTable.commentCount
            }
        }
    }

    MpvqcFileDropArea {
        anchors.fill: _splitView
    }

    MpvqcNewCommentMenu {
        id: _commentMenu

        onCommentTypeChosen: commentType => {
            root.disableFullScreenRequested();
            _mpvqcCommentTable.addNewComment(commentType);
        }
    }

    MpvqcNewCommentMenuClickGuard {
        menu: _commentMenu
    }

    MpvqcResizeHandler {
        id: _videoResizer

        headerHeight: root.header.height
        borderSize: root.windowBorder
        handleWidth: _splitView.draggerWidth
        handleHeight: _splitView.draggerHeight
        tableWidth: _splitView.tableContainerWidth
        tableHeight: _splitView.tableContainerHeight

        onAppWindowSizeRequested: (width, height) => {
            root.appWindowSizeRequested(width, height);
        }

        onSplitViewTableSizeRequested: (width, height) => {
            _tableContainer.setPreferredSizes(width, height);
        }
    }

    Component.onCompleted: {
        const width = Math.round(_splitView.width * root.defaultSplitRatio);
        const height = Math.round(_splitView.height * root.defaultSplitRatio);
        _tableContainer.setPreferredSizes(width, height);
    }
}
