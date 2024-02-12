/*
mpvQC

Copyright (C) 2022 mpvQC developers

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
import QtQuick.Controls

import settings


Label {
    id: root

    required property var mpvqcApplication

    readonly property int secondsPerHour: 60 * 60

    readonly property var mpvqcSettings: mpvqcApplication.mpvqcSettings
    readonly property var mpvqcMpvPlayerPropertiesPyObject: mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject
    readonly property var mpvqcTimeFormatUtils: mpvqcApplication.mpvqcTimeFormatUtils
    readonly property var mpvqcLabelWidthCalculator: mpvqcApplication.mpvqcLabelWidthCalculator

    readonly property int duration: mpvqcMpvPlayerPropertiesPyObject.duration
    readonly property int timePos: mpvqcMpvPlayerPropertiesPyObject.time_pos
    readonly property real timeRemaining: mpvqcMpvPlayerPropertiesPyObject.time_remaining

    property int timeFormat: mpvqcSettings.timeFormat


    visible: mpvqcMpvPlayerPropertiesPyObject.video_loaded && timeFormat !== MpvqcSettings.TimeFormat.EMPTY

    text: accordingToSetting()

    function accordingToSetting(): string {
        switch (timeFormat) {
            case MpvqcSettings.TimeFormat.CURRENT_TIME: return currentTime()
            case MpvqcSettings.TimeFormat.REMAINING_TIME: return remainingTime()
            case MpvqcSettings.TimeFormat.CURRENT_TOTAL_TIME: return currentTotalTime()
            default: return ''
        }
    }

    function currentTime(): string {
        return duration >= secondsPerHour
            ? mpvqcTimeFormatUtils.formatTimeToString(timePos)
            : mpvqcTimeFormatUtils.formatTimeToStringShort(timePos)
    }

    function remainingTime(): string {
        const remaining = duration >= secondsPerHour
            ? mpvqcTimeFormatUtils.formatTimeToString(timeRemaining)
            : mpvqcTimeFormatUtils.formatTimeToStringShort(timeRemaining)
        return `-${remaining}`
    }

    function currentTotalTime(): string {
        let current; let total
        if (duration >= secondsPerHour) {
            current = mpvqcTimeFormatUtils.formatTimeToString(timePos)
            total = mpvqcTimeFormatUtils.formatTimeToString(duration)
        } else {
            current = mpvqcTimeFormatUtils.formatTimeToStringShort(timePos)
            total = mpvqcTimeFormatUtils.formatTimeToStringShort(duration)
        }
        return `${current}/${total}`
    }

    function _recalculateWidth(): real {
        const items = [root.text]
        width = root.mpvqcLabelWidthCalculator.calculateWidthFor(items, root)
    }

    Connections {
        target: root.mpvqcSettings

        function onTimeFormatChanged() {
            root._recalculateWidth()
        }
    }

    Connections {
        target: root.mpvqcMpvPlayerPropertiesPyObject

        function onDurationChanged() {
            root._recalculateWidth()
        }
    }

}
