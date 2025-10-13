// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick

import pyobjects

import "../../utility"

Item {
    id: root

    readonly property var mpvqcMpvPlayerPropertiesPyObject: MpvqcMpvPlayerPropertiesPyObject {}
    readonly property var mpvqcMpvPlayerPyObject: MpvqcMpvPlayerPyObject {}
    readonly property var mpvqcUtilityPyObject: MpvqcUtilityPyObject {}

    readonly property var mpvqcLabelWidthCalculator: MpvqcLabelWidthCalculator
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

        /*
         * Replace some characters:
         *  - soft hyphen (\xad); When copying from Duden they include these :|
         *  - carriage return
         *  - newline
         */
        readonly property var reForbidden: new RegExp('[\u00AD\r\n]', 'gi')

        function formatTime(time: int): string {
            if (root.mpvqcMpvPlayerPropertiesPyObject.duration >= 60 * 60) {
                return root.mpvqcUtilityPyObject.formatTimeToStringLong(time);
            } else {
                return root.mpvqcUtilityPyObject.formatTimeToStringShort(time);
            }
        }

        function sanitizeText(text: string): string {
            if (text.search(reForbidden) === -1) {
                return text;
            } else {
                return text.replace(reForbidden, "");
            }
        }

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

        timeLabelWidth: root.mpvqcLabelWidthCalculator.timeLabelWidth
        commentTypeLabelWidth: root.mpvqcLabelWidthCalculator.commentTypesLabelWidth

        backgroundColor: root.mpvqcTheme.background
        rowHighlightColor: root.mpvqcTheme.rowHighlight
        rowHighlightTextColor: root.mpvqcTheme.rowHighlightText
        rowBaseColor: root.mpvqcTheme.rowBase
        rowBaseTextColor: root.mpvqcTheme.rowBaseText
        rowAlternateBaseColor: root.mpvqcTheme.rowBaseAlternate
        rowAlternateBaseTextColor: root.mpvqcTheme.rowBaseAlternateText

        timeFormatFunc: _impl.formatTime
        sanitizeTextFunc: _impl.sanitizeText
        jumpToTimeFunc: _impl.jumpToTime
        pauseVideoFunc: _impl.pauseVideo

        commentTypes: root.mpvqcSettings.commentTypes

        videoDuration: root.mpvqcMpvPlayerPropertiesPyObject.duration
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
