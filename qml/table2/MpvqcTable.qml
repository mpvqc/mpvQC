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

    readonly property var mpvqcDefaultTextValidatorPyObject: mpvqcApplication.mpvqcDefaultTextValidatorPyObject
    readonly property var mpvqcMpvPlayerPropertiesPyObject: mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject
    readonly property var mpvqcMpvPlayerPyObject: mpvqcApplication.mpvqcMpvPlayerPyObject
    readonly property var mpvqcUtilityPyObject: mpvqcApplication.mpvqcUtilityPyObject

    readonly property alias publicInterface: _publicInterface

    state: _publicInterface.commentCount > 0 ? "showTable" : "showPlaceholder"

    states: [
        State {
            name: "showTable"

            PropertyChanges {
                placeholder {
                    height: 0
                }
                commentTable {
                    height: root.height
                }
            }
        },
        State {
            name: "showPlaceholder"

            PropertyChanges {
                commentTable {
                    height: 0
                }
                placeholder {
                    height: root.height
                }
            }
        }
    ]

    QtObject {
        id: _impl

        function formatTime(time: int): string {
            if (root.mpvqcMpvPlayerPropertiesPyObject.duration >= 60 * 60) {
                return root.mpvqcUtilityPyObject.formatTimeToStringLong(time);
            } else {
                return root.mpvqcUtilityPyObject.formatTimeToStringShort(time);
            }
        }

        function sanitizeText(text: string): string {
            return root.mpvqcDefaultTextValidatorPyObject.replace_special_characters(text);
        }

        function jumpToTime(time: int): void {
            root.mpvqcMpvPlayerPyObject.jump_to(time);
        }

        function pauseVideo(): void {
            root.mpvqcMpvPlayerPyObject.pause();
        }
    }

    QtObject {
        id: _publicInterface

        readonly property int commentCount: commentTable.count
        readonly property int selectedCommentIndex: commentTable.currentIndex

        // readonly property bool currentlyEditing: false

        function forceActiveFocus(): void {
            commentTable.forceActiveFocus();
        }

        function addNewComment(commentType: string): void {
            commentTable.model.add_row(commentType);
        }
    }

    MpvqcCommentList {
        id: commentTable

        width: root.width
        visible: height > 0

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

        defaultTextValidator: root.mpvqcDefaultTextValidatorPyObject
        messageBoxParent: root.mpvqcApplication.contentItem
        commentTypes: root.mpvqcSettings.commentTypes

        videoDuration: root.mpvqcMpvPlayerPropertiesPyObject.duration
        isCurrentlyFullScreen: root.mpvqcApplication.fullscreen
    }

    MpvqcPlaceholder {
        id: placeholder

        height: root.height
        width: root.width
        visible: height > 0

        horizontalLayout: root.mpvqcSettings.layoutOrientation === Qt.Horizontal
    }
}
