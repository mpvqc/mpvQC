// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

import pyobjects

Item {
    id: root

    readonly property alias commentCount: _commentList.count
    readonly property alias selectedCommentIndex: _commentList.currentIndex

    function forceActiveFocus(): void {
        _commentList.forceActiveFocus();
    }

    function addNewComment(commentType: string): void {
        _commentList.viewModel.addRow(commentType);
    }

    MpvqcCommentList {
        id: _commentList

        width: root.width
        height: root.height
        visible: count > 0

        viewModel: MpvqcCommentTableViewModel {
            model: MpvqcCommentModel {}
        }
    }

    MpvqcPlaceholderView {
        width: root.width
        height: root.height
        visible: _commentList.count === 0
    }

    Timer {
        readonly property MpvqcBackupTimerViewModel viewModel: MpvqcBackupTimerViewModel {}

        repeat: true
        interval: viewModel.backupInterval
        running: viewModel.backupEnabled && _commentList.count > 0

        onTriggered: viewModel.backup()
    }
}
