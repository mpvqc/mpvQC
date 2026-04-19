// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

import pyobjects

import "../../utility"
import "../player"
import "../table"

Page {
    id: root

    required property MpvqcContentViewModel viewModel
    required property int windowBorder

    readonly property int minContainerHeight: 200
    readonly property int minContainerWidth: 500
    readonly property real defaultSplitRatio: 0.4

    function focusCommentTable(): void {
        _mpvqcCommentTable.forceActiveFocus();
    }

    function resizeVideo(): void {
        _videoResizer.recalculateSizes();
    }

    Keys.onEscapePressed: root.viewModel.requestDisableFullScreen()

    Keys.onPressed: event => _keyHandler.handleKeyPress(event)

    MpvqcContentKeyHandler {
        id: _keyHandler

        onOpenCommentMenuRequested: root.viewModel.requestOpenNewCommentMenu()
        onToggleFullScreenRequested: root.viewModel.requestToggleFullScreen()
        onForwardKeyToPlayerRequested: (key, modifiers) => root.viewModel.forwardKeyToPlayer(key, modifiers)
    }

    SplitView {
        id: _splitView

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

            onAddNewCommentMenuRequested: root.viewModel.openNewCommentMenuRequested()

            onToggleFullScreenRequested: root.viewModel.requestToggleFullScreen()
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

                viewModel: MpvqcFooterViewModel {
                    selectedCommentIndex: _mpvqcCommentTable.selectedCommentIndex
                    totalCommentCount: _mpvqcCommentTable.commentCount
                }

                width: _tableContainer.width
            }
        }
    }

    MpvqcFileDropAreaView {
        anchors.fill: _splitView
    }

    MpvqcNewCommentMenu {
        id: _commentMenu

        onCommentTypeChosen: commentType => {
            root.viewModel.requestDisableFullScreen();
            root.viewModel.addNewEmptyComment(commentType);
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
            root.viewModel.requestResizeAppWindow(width, height);
        }

        onSplitViewTableSizeRequested: (width, height) => {
            _tableContainer.setPreferredSizes(width, height);
        }
    }

    Connections {
        target: root.viewModel

        function onOpenNewCommentMenuRequested(): void {
            _commentMenu.popup();
        }

        function onAddNewCommentRequested(commentType: string): void {
            _mpvqcCommentTable.addNewComment(commentType);
        }
    }

    Component.onCompleted: {
        const width = Math.round(_splitView.width * root.defaultSplitRatio);
        const height = Math.round(_splitView.height * root.defaultSplitRatio);
        _tableContainer.setPreferredSizes(width, height);
    }
}
