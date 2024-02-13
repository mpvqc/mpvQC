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

import settings


MpvqcVideoTimeLabel {
    id: objectUnderTest

    width: 400
    height: 400

    mpvqcApplication: QtObject {
        property var mpvqcSettings: QtObject {
            property bool timeFormat: MpvqcSettings.TimeFormat.EMPTY
        }
        property var mpvqcMpvPlayerPropertiesPyObject: QtObject {
            property bool video_loaded: false
            property real duration: 10.0
            property real time_pos: 10.0
            property real time_remaining: 10.0
        }
        property var mpvqcLabelWidthCalculator: QtObject {
            function calculateWidthFor(items, parent) { return 42 }
        }
        property var mpvqcTimeFormatUtils: QtObject {
            function formatTimeToStringLong(seconds) { return 'formatted' }
            function formatTimeToStringShort(seconds) { return 'formatted' }
        }
    }

    TestCase {
        name: "MpvqcVideoTimeLabel"
        when: windowShown

        function init() {
            objectUnderTest.mpvqcApplication.mpvqcSettings.timeFormat = MpvqcSettings.TimeFormat.EMPTY
            objectUnderTest.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.duration = 0
        }

        function test_reformat_on_data() {
            return [
                {
                    tag: 'timeFormatChanged',
                    change: () => { objectUnderTest.mpvqcSettings.timeFormat = MpvqcSettings.TimeFormat.CURRENT_TIME },
                },
                {
                    tag: 'durationChanged',
                    change: () => { objectUnderTest.mpvqcMpvPlayerPropertiesPyObject.duration = 60 * 60 + 1 },
                },
            ]
        }

        function test_reformat_on(data) {
            objectUnderTest.width = 400
            compare(objectUnderTest.width, 400)

            objectUnderTest.text = 'abc'
            compare(objectUnderTest.width, 400)

            data.change()
            compare(objectUnderTest.width, 42)
        }

        function test_format_data() {
            return [
                { tag: 'default', expected: 'formatted/formatted', format: MpvqcSettings.TimeFormat.CURRENT_TOTAL_TIME },
                { tag: 'current', expected: 'formatted', format: MpvqcSettings.TimeFormat.CURRENT_TIME },
                { tag: 'remaining', expected: '-formatted', format: MpvqcSettings.TimeFormat.REMAINING_TIME },
                { tag: 'empty', expected: '', format: MpvqcSettings.TimeFormat.EMPTY },
            ]
        }

        function test_format(data) {
            objectUnderTest.width = 400
            objectUnderTest.text = ''

            objectUnderTest.timeFormat = data.format
            compare(objectUnderTest.accordingToSetting(), data.expected)
        }

    }

}
