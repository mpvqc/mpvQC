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


Item {
    id: testHelper

    width: 400
    height: 400

    MpvqcSpinBoxRow {
        id: objectUnderTest

        prefWidth: testHelper.width
        valueFrom: 15
        value: 30
        valueTo: 45

        property int newValue: -1

        onValueModified: (value) => {
            objectUnderTest.newValue = value
        }

        TestCase {
            name: "MpvqcSpinBoxRow"
            when: windowShown

            SignalSpy { id: valueModifiedSpy; target: objectUnderTest; signalName: 'valueModified' }

            function init() {
                valueModifiedSpy.clear()
                objectUnderTest.newValue = -1
            }

            function test_spinBox_data() {
                return [
                    { tag: 'increase', value: 31, exec: () => { objectUnderTest.spinBox.increase() }, },
                ]
            }

            function test_spinBox(data) {
                data.exec()
                compare(objectUnderTest.newValue, data.value)
                compare(valueModifiedSpy.count, 1)
            }
        }
    }

}
