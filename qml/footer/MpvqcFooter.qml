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

import QtQuick

import "../settings"

Item {
    id: root

    required property var mpvqcApplication

    readonly property alias rowSelectionLabelText: _content.rowSelectionLabel // for tests
    readonly property alias percentLabelText: _content.percentLabel // for tests
    readonly property alias videoTimeLabelText: _content.videoTimeLabel // for tests

    height: 25
    visible: !root.mpvqcApplication.fullscreen

    QtObject {
        id: _impl

        readonly property var mpvqcSettings: root.mpvqcApplication.mpvqcSettings
        readonly property var mpvqcCommentTable: root.mpvqcApplication.mpvqcCommentTable
        readonly property var mpvqcLabelWidthCalculator: root.mpvqcApplication.mpvqcLabelWidthCalculator
        readonly property var mpvqcMpvPlayerPropertiesPyObject: root.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject
        readonly property var mpvqcUtilityPyObject: root.mpvqcApplication.mpvqcUtilityPyObject

        function formatTime(time: int): string {
            if (mpvqcMpvPlayerPropertiesPyObject.duration >= 60 * 60) {
                return mpvqcUtilityPyObject.formatTimeToStringLong(time);
            } else {
                return mpvqcUtilityPyObject.formatTimeToStringShort(time);
            }
        }

        function recalculateVideoTimeLabelWidth(): real {
            const items = [_content.determineTimeLabelText()];
            _content.videoTimeLabelWidth = mpvqcLabelWidthCalculator.calculateWidthFor(items, root); // qmllint disable
        }
    }

    MpvqcFooterContent {
        id: _content

        anchors.fill: parent

        isApplicationMazimized: root.mpvqcApplication.maximized

        selectedCommentIndex: _impl.mpvqcCommentTable.selectedCommentIndex
        totalCommentCount: _impl.mpvqcCommentTable.commentCount

        playerPercentPosition: _impl.mpvqcMpvPlayerPropertiesPyObject.percent_pos
        playerDuration: _impl.mpvqcMpvPlayerPropertiesPyObject.duration
        playerVideoLoaded: _impl.mpvqcMpvPlayerPropertiesPyObject.video_loaded
        playerTimePosition: _impl.mpvqcMpvPlayerPropertiesPyObject.time_pos
        playerTimeRemaining: _impl.mpvqcMpvPlayerPropertiesPyObject.time_remaining

        isStatusbarDisplayPercentage: _impl.mpvqcSettings.statusbarPercentage

        isTimeFormatCurrentTotalTime: _impl.mpvqcSettings.timeFormat === MpvqcSettings.TimeFormat.CURRENT_TOTAL_TIME
        isTimeFormatCurrentTime: _impl.mpvqcSettings.timeFormat === MpvqcSettings.TimeFormat.CURRENT_TIME
        isTimeFormatRemainingTime: _impl.mpvqcSettings.timeFormat === MpvqcSettings.TimeFormat.REMAINING_TIME
        isTimeFormatEmpty: _impl.mpvqcSettings.timeFormat === MpvqcSettings.TimeFormat.EMPTY

        formatTimeFunc: _impl.formatTime

        videoTimeLabelWidth: 0

        onCurrentTotalTimeSelected: {
            _impl.mpvqcSettings.timeFormat = MpvqcSettings.TimeFormat.CURRENT_TOTAL_TIME;
        }

        onCurrentTimeSelected: {
            _impl.mpvqcSettings.timeFormat = MpvqcSettings.TimeFormat.CURRENT_TIME;
        }

        onRemainingTimeSelected: {
            _impl.mpvqcSettings.timeFormat = MpvqcSettings.TimeFormat.REMAINING_TIME;
        }

        onEmptyTimeSelected: {
            _impl.mpvqcSettings.timeFormat = MpvqcSettings.TimeFormat.EMPTY;
        }

        onStatusBarPercentageToggled: {
            _impl.mpvqcSettings.statusbarPercentage = !_impl.mpvqcSettings.statusbarPercentage;
        }
    }

    Connections {
        target: _impl.mpvqcSettings

        function onTimeFormatChanged() {
            _impl.recalculateVideoTimeLabelWidth();
        }
    }

    Connections {
        target: _impl.mpvqcMpvPlayerPropertiesPyObject

        function onDurationChanged() {
            _impl.recalculateVideoTimeLabelWidth();
        }
    }
}
