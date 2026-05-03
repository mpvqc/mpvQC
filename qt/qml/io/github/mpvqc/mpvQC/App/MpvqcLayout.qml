// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material

import io.github.mpvqc.mpvQC.Python
import io.github.mpvqc.mpvQC.Utility
import io.github.mpvqc.mpvQC.Views.Footer
import io.github.mpvqc.mpvQC.Views.Player
import io.github.mpvqc.mpvQC.Views.Table

Page {
    id: root

    required property int layoutOrientation
    required property int windowBorder
    required property int headerHeight

    readonly property int minContainerHeight: 200
    readonly property int minContainerWidth: 500
    readonly property real defaultSplitRatio: 0.4

    signal toggleFullScreenRequested
    signal addNewCommentMenuRequested
    signal appWindowSizeRequested(width: int, height: int)

    function focusCommentTable(): void {
        _mpvqcCommentTable.forceActiveFocus();
    }

    function addComment(commentType: string): void {
        _mpvqcCommentTable.addNewComment(commentType);
    }

    function recalculateSizes(): void {
        _videoResizer.recalculateSizes();
    }

    SplitView {
        id: _splitView
        objectName: "applicationSplitView"

        focus: true
        anchors.fill: root.contentItem
        orientation: root.layoutOrientation

        MpvqcPlayerView {
            id: _player

            SplitView.minimumHeight: root.minContainerHeight
            SplitView.minimumWidth: root.minContainerWidth
            SplitView.fillHeight: true
            SplitView.fillWidth: true

            onAddNewCommentMenuRequested: root.addNewCommentMenuRequested()
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

    MpvqcResizeViewModel {
        id: _videoResizer

        headerHeight: root.headerHeight
        borderSize: root.windowBorder
        handleWidth: _splitView.width - _player.width - _tableContainer.width
        handleHeight: _splitView.height - _player.height - _tableContainer.height
        tableWidth: _tableContainer.width
        tableHeight: _tableContainer.height

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
