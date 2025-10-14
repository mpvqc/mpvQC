// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

import pyobjects

import "../../utility"

Item {
    id: root

    readonly property var mpvqcMpvPlayerPyObject: MpvqcMpvPlayerPyObject {}
    readonly property var mpvqcSettings: MpvqcSettings
    readonly property var mpvqcTheme: MpvqcTheme

    readonly property alias commentCount: _commentTable.count
    readonly property alias selectedCommentIndex: _commentTable.currentIndex

    function forceActiveFocus(): void {
        _commentTable.forceActiveFocus();
    }

    function addNewComment(commentType: string): void {
        _commentTable.model.add_row(commentType);
    }

    QtObject {
        id: _impl

        function jumpToTime(time: int): void {
            root.mpvqcMpvPlayerPyObject.jump_to(time);
        }

        function pauseVideo(): void {
            root.mpvqcMpvPlayerPyObject.pause();
        }
    }

    MpvqcCommentList {
        id: _commentTable

        width: root.width
        height: root.height
        visible: count > 0

        backgroundColor: root.mpvqcTheme.background
        rowHighlightColor: root.mpvqcTheme.rowHighlight
        rowHighlightTextColor: root.mpvqcTheme.rowHighlightText
        rowBaseColor: root.mpvqcTheme.rowBase
        rowBaseTextColor: root.mpvqcTheme.rowBaseText
        rowAlternateBaseColor: root.mpvqcTheme.rowBaseAlternate
        rowAlternateBaseTextColor: root.mpvqcTheme.rowBaseAlternateText

        jumpToTimeFunc: _impl.jumpToTime
        pauseVideoFunc: _impl.pauseVideo

        commentTypes: root.mpvqcSettings.commentTypes

        videoDuration: MpvqcTableUtility.duration
        isCurrentlyFullScreen: MpvqcWindowProperties.isFullscreen
    }

    MpvqcPlaceholderView {
        width: root.width
        height: root.height
        visible: root.commentCount === 0
    }

    Timer {
        readonly property MpvqcBackupTimerViewModel viewModel: MpvqcBackupTimerViewModel {}

        repeat: true
        interval: viewModel.backupInterval
        running: viewModel.backupEnabled && _commentTable.count > 0

        onTriggered: viewModel.backup()
    }
}
