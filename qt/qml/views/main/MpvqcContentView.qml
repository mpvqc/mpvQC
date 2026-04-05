// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

import pyobjects

import "../../utility"
import "../table"

Page {
    id: root

    required property MpvqcContentViewModel viewModel
    required property int windowBorder

    function focusCommentTable(): void {
        _mpvqcCommentTable.forceActiveFocus();
    }

    function resizeVideo(): void {
        _videoResizer.recalculateSizes();
    }

    Keys.onEscapePressed: root.viewModel.requestDisableFullScreen()

    Keys.onPressed: event => root.viewModel.onKeyPressed(event.key, event.modifiers, event.isAutoRepeat)

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

            SplitView.minimumHeight: root.viewModel.minContainerHeight
            SplitView.minimumWidth: root.viewModel.minContainerWidth
            SplitView.fillHeight: true
            SplitView.fillWidth: true

            onAddNewCommentMenuRequested: root.viewModel.openNewCommentMenuRequested()

            onToggleFullScreenRequested: root.viewModel.requestToggleFullScreen()
        }

        Column {
            id: _tableContainer

            visible: !MpvqcWindowUtility.isFullscreen

            SplitView.minimumHeight: root.viewModel.minContainerHeight
            SplitView.minimumWidth: root.viewModel.minContainerWidth

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

    MpvqcNewCommentMenuView {
        id: _commentMenu

        onCommentTypeChosen: commentType => {
            root.viewModel.requestDisableFullScreen();
            root.viewModel.addNewEmptyComment(commentType);
        }
    }

    // *** *** ***  *** ***  *** ***  *** ***  *** ***  *** ***  *** ***  *** ***
    // Workaround for QTBUG-145585: On Windows, Popup.Window menus do not respect
    // the modal property, allowing clicks to pass through to underlying items.
    // This item lives in the window overlay layer and intercepts every click
    // while the new-comment menu is open, closing it and swallowing the event
    // so nothing underneath reacts.
    //
    // The menuOpen flag is cleared via Qt.callLater instead of directly in
    // onClosed because the signal is delivered immediately.
    // Without the deferral the overlay would be gone before the click arrives.
    Item {
        id: _newCommentMenuOverlay

        property bool menuOpen: false

        parent: Overlay.overlay
        anchors.fill: parent
        visible: Qt.platform.os === "windows" && menuOpen

        Connections {
            target: _commentMenu
            function onAboutToShow(): void {
                _newCommentMenuOverlay.menuOpen = true;
            }
            function onClosed(): void {
                Qt.callLater(() => {
                    _newCommentMenuOverlay.menuOpen = false;
                });
            }
        }

        MouseArea {
            anchors.fill: parent
            onPressed: event => {
                event.accepted = true;
                _newCommentMenuOverlay.menuOpen = false;
                _commentMenu.close();
            }
        }
    }
    // *** *** ***  *** ***  *** ***  *** ***  *** ***  *** ***  *** ***  *** ***

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
        const sizes = root.viewModel.calculatePreferredSplitSizes(_splitView.width, _splitView.height);
        _tableContainer.setPreferredSizes(sizes.width, sizes.height);
    }
}
