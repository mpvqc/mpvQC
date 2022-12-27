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

import "MpvqcTimeFormatUtils.js" as TestObject


TestCase {
    name: "MpvqcTimeFormatUtils"

    function test_formatTimeToString_data() {
        return [
            { expected: '00:00:00', actual: TestObject.formatTimeToString(0), tag: '0 -> 00:00:00' },
            { expected: '00:01:08', actual: TestObject.formatTimeToString(68), tag: '68 -> 00:01:08' },
            { expected: '00:16:39', actual: TestObject.formatTimeToString(999), tag: '999 -> 00:16:39' },
            { expected: '02:46:40', actual: TestObject.formatTimeToString(10000), tag: '10000 -> 02:46:40' },
        ]
    }

    function test_formatTimeToString(data) {
        compare(data.actual, data.expected)
    }

    function test_formatTimeToStringShort_data() {
        return [
            { expected: '00:00', actual: TestObject.formatTimeToStringShort(0), tag: '0 -> 00:00' },
            { expected: '01:08', actual: TestObject.formatTimeToStringShort(68), tag: '68 -> 01:08' },
            { expected: '16:39', actual: TestObject.formatTimeToStringShort(999), tag: '999 -> 16:39' },
        ]
    }

    function test_formatTimeToStringShort(data) {
        compare(data.actual, data.expected)
    }

    function test_extractSecondsFrom_data() {
        return [
            { expected: 0, actual: TestObject.extractSecondsFrom('00:00:00'), tag: '00:00:00 -> 0' },
            { expected: 68, actual: TestObject.extractSecondsFrom('00:01:08'), tag: '00:01:08 -> 68' },
            { expected: 999, actual: TestObject.extractSecondsFrom('00:16:39'), tag: '00:16:39 -> 999' },
            { expected: 10000, actual: TestObject.extractSecondsFrom('02:46:40'), tag: '02:46:40 -> 10000' },
        ]
    }

    function test_extractSecondsFrom(data) {
        compare(data.actual, data.expected)
    }

}
