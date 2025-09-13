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
import QtTest

import "../settings"

TestCase {
    id: testCase
    visible: false
    name: "MpvqcFooterController"

    Component {
        id: objectUnderTest

        MpvqcFooterController {
            isApplicationMazimized: false
            isApplicationFullscreen: false
            labelWidthTarget: Rectangle {
                width: 200
                height: 20
            }
            mpvqcSettings: QtObject {
                property int timeFormat: MpvqcSettings.TimeFormat.CURRENT_TIME
                property bool statusbarPercentage: true
            }
            mpvqcLabelWidthCalculator: QtObject {
                property var lastItems
                property var lastTarget
                function calculateWidthFor(items, target) {
                    lastItems = items;
                    lastTarget = target;
                    const t = (items && items.length) ? (items[0] || "") : "";
                    return String(t).length * 10;
                }
            }
            mpvqcMpvPlayerPropertiesPyObject: QtObject {
                property int duration: 3599
                property real percent_pos: 42.4
                property bool video_loaded: true
                property int time_pos: 75
                property int time_remaining: duration - time_pos
            }
            mpvqcUtilityPyObject: QtObject {
                function formatTimeToStringLong(t) {
                    return `L${t}`;
                }
                function formatTimeToStringShort(t) {
                    return `S${t}`;
                }
            }
        }
    }

    function test_formatTime_data() {
        return [
            {
                tag: "short-format-when-duration<1h",
                duration: 3599,
                input: 75,
                expected: "S75"
            },
            {
                tag: "long-format-when-duration>=1h",
                duration: 3600,
                input: 75,
                expected: "L75"
            },
        ];
    }

    function test_formatTime(data) {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        control.mpvqcMpvPlayerPropertiesPyObject.duration = data.duration;
        const out = control.formatTime(data.input);

        compare(out, data.expected);
    }

    function test_determineTimeLabelText_data() {
        return [
            {
                tag: "current/total",
                timeFormat: MpvqcSettings.TimeFormat.CURRENT_TOTAL_TIME,
                duration: 3600,
                time_pos: 10,
                time_remaining: 999,
                expected: "L10/L3600"
            },
            {
                tag: "current-only",
                timeFormat: MpvqcSettings.TimeFormat.CURRENT_TIME,
                duration: 3600,
                time_pos: 10,
                time_remaining: 999,
                expected: "L10"
            },
            {
                tag: "remaining",
                timeFormat: MpvqcSettings.TimeFormat.REMAINING_TIME,
                duration: 3600,
                time_pos: 10,
                time_remaining: 15,
                expected: "-L15"
            },
            {
                tag: "empty",
                timeFormat: MpvqcSettings.TimeFormat.EMPTY,
                duration: 3600,
                time_pos: 10,
                time_remaining: 15,
                expected: ""
            },
        ];
    }

    function test_determineTimeLabelText(data) {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        control.mpvqcMpvPlayerPropertiesPyObject.duration = data.duration;
        control.mpvqcMpvPlayerPropertiesPyObject.time_pos = data.time_pos;
        control.mpvqcMpvPlayerPropertiesPyObject.time_remaining = data.time_remaining;
        control.mpvqcSettings.timeFormat = data.timeFormat;

        const text = control.determineTimeLabelText();
        compare(text, data.expected);
    }

    function test_recalculateVideoTimeLabelWidth() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        control.mpvqcMpvPlayerPropertiesPyObject.duration = 3600; // long
        control.mpvqcMpvPlayerPropertiesPyObject.time_pos = 1;
        control.mpvqcSettings.timeFormat = MpvqcSettings.TimeFormat.CURRENT_TIME;

        const expectedText = "L1"; // from our fake formatter
        control.recalculateVideoTimeLabelWidth();

        compare(control.videoTimeLabelWidth, expectedText.length * 10);
        compare(control.mpvqcLabelWidthCalculator.lastItems.length, 1);
        compare(control.mpvqcLabelWidthCalculator.lastItems[0], expectedText);
        compare(control.mpvqcLabelWidthCalculator.lastTarget, control.labelWidthTarget);
    }

    function test_setTimeFormat_sets_property() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        control.setTimeFormat(MpvqcSettings.TimeFormat.REMAINING_TIME);
        compare(control.mpvqcSettings.timeFormat, MpvqcSettings.TimeFormat.REMAINING_TIME);
    }

    function test_toggleStatusBarPercentage_flips_value() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        const start = control.mpvqcSettings.statusbarPercentage;
        control.toggleStatusBarPercentage();
        compare(control.mpvqcSettings.statusbarPercentage, !start);
        control.toggleStatusBarPercentage();
        compare(control.mpvqcSettings.statusbarPercentage, start);
    }

    function test_reactive_onTimeFormatChanged_triggers_width_recalc() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        control.mpvqcMpvPlayerPropertiesPyObject.duration = 3600;
        control.mpvqcMpvPlayerPropertiesPyObject.time_pos = 10;
        control.mpvqcSettings.timeFormat = MpvqcSettings.TimeFormat.CURRENT_TIME;
        control.recalculateVideoTimeLabelWidth();
        compare(control.videoTimeLabelWidth, "L10".length * 10);

        control.mpvqcSettings.timeFormat = MpvqcSettings.TimeFormat.CURRENT_TOTAL_TIME;
        tryVerify(() => control.videoTimeLabelWidth === "L10/L3600".length * 10, 100);
    }

    function test_reactive_onDurationChanged_triggers_width_recalc() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        control.mpvqcSettings.timeFormat = MpvqcSettings.TimeFormat.CURRENT_TOTAL_TIME;
        control.mpvqcMpvPlayerPropertiesPyObject.time_pos = 10;
        control.mpvqcMpvPlayerPropertiesPyObject.duration = 3600;
        control.recalculateVideoTimeLabelWidth();
        compare(control.videoTimeLabelWidth, "L10/L3600".length * 10);

        control.mpvqcMpvPlayerPropertiesPyObject.duration = 7200; // emits durationChanged
        tryVerify(() => control.videoTimeLabelWidth === "L10/L7200".length * 10, 100);
    }
}
