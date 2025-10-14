// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

import pyobjects

import "../../utility"

Item {
    id: root

    readonly property alias commentCount: _commentTable.count
    readonly property alias selectedCommentIndex: _commentTable.currentIndex

    function forceActiveFocus(): void {
        _commentTable.forceActiveFocus();
    }

    function addNewComment(commentType: string): void {
        _commentTable.model.add_row(commentType);
    }

    MpvqcCommentList {
        id: _commentTable

        viewModel: MpvqcCommentTableViewModel {
            model: MpvqcCommentModel {}
        }

        width: root.width
        height: root.height
        visible: count > 0
    }

    MpvqcPlaceholderView {
        width: root.width
        height: root.height
        visible: _commentTable.count === 0
    }

    Timer {
        readonly property MpvqcBackupTimerViewModel viewModel: MpvqcBackupTimerViewModel {}

        repeat: true
        interval: viewModel.backupInterval
        running: viewModel.backupEnabled && _commentTable.count > 0

        onTriggered: viewModel.backup()
    }
}
