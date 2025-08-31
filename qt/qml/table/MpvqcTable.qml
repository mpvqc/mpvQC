/*
mpvQC

Copyright (C) 2024 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

pragma ComponentBehavior: Bound

import QtQuick

import pyobjects

Item {
    id: root

    required property var mpvqcApplication

    readonly property var mpvqcLabelWidthCalculator: mpvqcApplication.mpvqcLabelWidthCalculator
    readonly property var mpvqcSettings: mpvqcApplication.mpvqcSettings
    readonly property var mpvqcTheme: mpvqcApplication.mpvqcTheme

    readonly property var mpvqcMpvPlayerPropertiesPyObject: mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject
    readonly property var mpvqcMpvPlayerPyObject: mpvqcApplication.mpvqcMpvPlayerPyObject
    readonly property var mpvqcUtilityPyObject: mpvqcApplication.mpvqcUtilityPyObject

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
        visible: root.commentCount > 0

        model: MpvqcCommentModelPyObject {}

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

        messageBoxParent: root.mpvqcApplication.contentItem
        commentTypes: root.mpvqcSettings.commentTypes

        videoDuration: root.mpvqcMpvPlayerPropertiesPyObject.duration
        isCurrentlyFullScreen: root.mpvqcApplication.fullscreen
    }

    MpvqcPlaceholder {
        id: placeholder

        width: root.width
        height: root.height
        visible: root.commentCount === 0

        horizontalLayout: root.mpvqcSettings.layoutOrientation === Qt.Horizontal
    }
}
