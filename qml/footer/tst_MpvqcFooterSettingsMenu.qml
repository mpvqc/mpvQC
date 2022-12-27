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


Item {
    id: testHelper

    width: 400
    height: 400

    MpvqcFooterSettingsMenu {
        id: objectUnderTest

        mpvqcApplication: QtObject {
            property var mpvqcSettings: QtObject {
                property int timeFormat: -1
                property bool statusbarPercentage: false
            }
        }
    }

    TestCase {
        name: "MpvqcFooterSettingsMenu"
        when: windowShown

        function init() {
            const settings = objectUnderTest.mpvqcApplication.mpvqcSettings
            settings.timeFormat = -1
            settings.statusbarPercentage = false
            objectUnderTest.open()
        }

        function test_selection_data() {
            return [
                {
                     tag: 'default',
                     mouseTarget: objectUnderTest.defaultFormat,
                     expected: MpvqcSettings.TimeFormat.CURRENT_TOTAL_TIME
                },
                {
                     tag: 'current',
                     mouseTarget: objectUnderTest.currentTimeFormat,
                     expected: MpvqcSettings.TimeFormat.CURRENT_TIME
                },
                {
                     tag: 'remaining',
                     mouseTarget: objectUnderTest.remainingTimeFormat,
                     expected: MpvqcSettings.TimeFormat.REMAINING_TIME
                },
                {
                     tag: 'hide',
                     mouseTarget: objectUnderTest.hideTimeFormat,
                     expected: MpvqcSettings.TimeFormat.EMPTY
                },
            ]
        }

        function test_selection(data) {
            mouseClick(data.mouseTarget)
            compare(objectUnderTest.mpvqcApplication.mpvqcSettings.timeFormat, data.expected)
        }

        function test_percentage() {
            objectUnderTest.percentage.trigger()
            compare(objectUnderTest.mpvqcApplication.mpvqcSettings.statusbarPercentage, true)
        }
    }

}
