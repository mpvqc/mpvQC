/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


import QtQuick
import QtQuick.Controls
import handlers
import helpers
import settings


Label {
    id: label
    visible: MpvqcPlayerProperties.path

    readonly property int secondsPerHour: 60 * 60
    readonly property int duration: MpvqcPlayerProperties.duration
    readonly property int timePos: MpvqcPlayerProperties.time_pos
    readonly property real timeRemaining: MpvqcPlayerProperties.time_remaining
    readonly property int timeFormat: MpvqcSettings.timeFormat

    property int preferredLabelWidth: 0

    onVisibleChanged: {
        if (visible) {
            updateText()
        }
    }

    onDurationChanged: {
        updateText()
        recalculcatePreferredWidth()
    }

    onTimePosChanged: {
        updateText()
    }

    onTimeFormatChanged: {
        updateText()
        recalculcatePreferredWidth()
    }

    function updateText() {
        text = formatText()
    }

    function formatText() {
        switch (timeFormat) {
            case MpvqcTimeFormat.currentTime: return formatCurrentTime()
            case MpvqcTimeFormat.remainingTime: return formatRemainingTime()
            case MpvqcTimeFormat.currentTotalTime: return formatCurrentTotalTime()
            default: return ''
        }
    }

    function formatCurrentTime() {
        return duration >= secondsPerHour
            ? MpvqcTimeFormatUtils.formatTimeToString(timePos)
            : MpvqcTimeFormatUtils.formatTimeToStringShort(timePos)
    }

    function formatRemainingTime() {
        const remaining = duration >= secondsPerHour
            ? MpvqcTimeFormatUtils.formatTimeToString(timeRemaining)
            : MpvqcTimeFormatUtils.formatTimeToStringShort(timeRemaining)
        return `-${remaining}`
    }

    function formatCurrentTotalTime() {
        let current; let total
        if (duration >= secondsPerHour) {
            current = MpvqcTimeFormatUtils.formatTimeToString(timePos)
            total = MpvqcTimeFormatUtils.formatTimeToString(duration)
        } else {
            current = MpvqcTimeFormatUtils.formatTimeToStringShort(timePos)
            total = MpvqcTimeFormatUtils.formatTimeToStringShort(duration)
        }
        return `${current}/${total}`
    }

    function recalculcatePreferredWidth() {
        const items = [label.text]
        const width = MpvqcLabelWidthCalculator.calculateWidthFor(items, label)
        preferredLabelWidth = width
    }

}
