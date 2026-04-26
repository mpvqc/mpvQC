// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

import pyobjects

Item {
    id: root
    objectName: "tableView"

    property MpvqcCommentTableViewModel viewModel: MpvqcCommentTableViewModel {}
    property bool backupEnabled: true

    readonly property alias commentCount: _commentList.count
    readonly property alias selectedCommentIndex: _commentList.currentIndex
    readonly property alias commentList: _commentList

    function forceActiveFocus(): void {
        _commentList.forceActiveFocus();
    }

    function addNewComment(commentType: string): void {
        viewModel.addRow(commentType);
    }

    MpvqcCommentList {
        id: _commentList

        anchors.fill: parent
        visible: count > 0

        viewModel: root.viewModel

        modalActive: _overlays.anyModalActive
        searchQuery: _overlays.searchQuery
    }

    MpvqcCommentListOverlays {
        id: _overlays

        anchors.fill: _commentList

        viewModel: root.viewModel
        listView: _commentList

        onFocusWanted: _commentList.forceActiveFocus()
    }

    MpvqcPlaceholderView {
        anchors.fill: parent
        visible: _commentList.count === 0
    }

    Timer {
        readonly property MpvqcBackupTimerViewModel viewModel: MpvqcBackupTimerViewModel {}

        repeat: true
        interval: viewModel.backupInterval
        running: root.backupEnabled && viewModel.backupEnabled && _commentList.count > 0

        onTriggered: viewModel.backup()
    }
}
