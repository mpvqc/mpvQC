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
import QtTest
import "MpvqcLabelWidthCalculator.js" as TestObject


Label {
    id: testHelper

    width: 400
    height: 400

    TestCase {
        name: "MpvqcLabelWidthCalculator"

        property var itemsShort: ['a', 'bb']
        property var itemsLong: ['ccc', 'dddd']

        function test_calculation() {
            const smallWidth = TestObject.calculateWidthFor(itemsShort, testHelper)
            const bigWidth = TestObject.calculateWidthFor(itemsLong, testHelper)
            verify(smallWidth < bigWidth)
        }
    }
}
