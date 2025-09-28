// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

import pyobjects

import "../shared"

MpvqcObject {
    id: root

    required property var mpvqcSettings
    required property var mpvqcLabelWidthCalculator
    required property var mpvqcMpvPlayerPropertiesPyObject
    required property var mpvqcUtilityPyObject

    required property bool isApplicationMazimized
    required property bool isApplicationFullscreen

    readonly property real playerPercentPosition: mpvqcMpvPlayerPropertiesPyObject.percent_pos
    readonly property bool playerVideoLoaded: mpvqcMpvPlayerPropertiesPyObject.video_loaded

    readonly property bool isStatusbarDisplayPercentage: mpvqcSettings.statusbarPercentage
    readonly property bool isTimeFormatCurrentTotalTime: mpvqcSettings.timeFormat === MpvqcSettings.TimeFormat.CURRENT_TOTAL_TIME
    readonly property bool isTimeFormatCurrentTime: mpvqcSettings.timeFormat === MpvqcSettings.TimeFormat.CURRENT_TIME
    readonly property bool isTimeFormatRemainingTime: mpvqcSettings.timeFormat === MpvqcSettings.TimeFormat.REMAINING_TIME
    readonly property bool isTimeFormatEmpty: mpvqcSettings.timeFormat === MpvqcSettings.TimeFormat.EMPTY

    property int videoTimeLabelWidth: 0

    function formatTime(time: int): string {
        if (mpvqcMpvPlayerPropertiesPyObject.duration >= 60 * 60) {
            return mpvqcUtilityPyObject.formatTimeToStringLong(time);
        } else {
            return mpvqcUtilityPyObject.formatTimeToStringShort(time);
        }
    }

    function determineTimeLabelText(): string {
        if (isTimeFormatCurrentTotalTime) {
            const current = formatTime(mpvqcMpvPlayerPropertiesPyObject.time_pos);
            const total = formatTime(mpvqcMpvPlayerPropertiesPyObject.duration);
            return `${current}/${total}`;
        }
        if (isTimeFormatCurrentTime) {
            return formatTime(mpvqcMpvPlayerPropertiesPyObject.time_pos);
        }
        if (isTimeFormatRemainingTime) {
            const remaining = formatTime(mpvqcMpvPlayerPropertiesPyObject.time_remaining);
            return `-${remaining}`;
        }
        return "";
    }

    function recalculateVideoTimeLabelWidth(): void {
        const text = determineTimeLabelText();
        const items = [text];
        videoTimeLabelWidth = mpvqcLabelWidthCalculator.calculateWidthFor(items);
    }

    function setTimeFormat(newFormat: int): void {
        mpvqcSettings.timeFormat = newFormat;
    }

    function toggleStatusBarPercentage(): void {
        mpvqcSettings.statusbarPercentage = !mpvqcSettings.statusbarPercentage;
    }

    Connections {
        target: root.mpvqcSettings

        function onTimeFormatChanged(): void {
            root.recalculateVideoTimeLabelWidth();
        }
    }

    Connections {
        target: root.mpvqcMpvPlayerPropertiesPyObject

        function onDurationChanged(): void {
            root.recalculateVideoTimeLabelWidth();
        }
    }
}
