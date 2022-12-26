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


TestCase {
    id: testCase

    width: 400
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcWidthCalculatorCommentTypes"

    Component {
        id: widthCalculator

        MpvqcWidthCalculatorCommentTypes {
            property int calculateCounter: 0

            mpvqcApplication: QtObject {
                property var mpvqcSettings: QtObject {
                    property var commentTypes: QtObject {
                        function items() { return ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'] }
                    }
                    property var language: 'language'
                }
                property var mpvqcWidthCalculatorLabel: QtObject {
                    function calculateWidthFor(items, parent) { calculateCounter += 1; return items.length }
                }
            }
        }
    }

    function test_recalculationTriggers() {
        const control = createTemporaryObject(widthCalculator, testCase)
        verify(control)

        compare(control.calculateCounter, 1)

        control.mpvqcApplication.mpvqcSettings.commentTypesChanged()
        compare(control.calculateCounter, 2)

        control.mpvqcApplication.mpvqcSettings.languageChanged()
        compare(control.calculateCounter, 3)
    }

}
