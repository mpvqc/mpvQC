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

Item {
    id: testHelper

    width: 400
    height: 400

    MpvqcTextFieldRow {
        id: objectUnderTest

        property string newText: ''

        prefWidth: testHelper.width

        onTextChanged: (text) => {
            objectUnderTest.newText = text
        }

        TestCase {
            name: "MpvqcTextFieldRow"

            SignalSpy { id: textChangedSpy; target: objectUnderTest; signalName: 'textChanged' }

            function init() {
                objectUnderTest.newText = ''
                textChangedSpy.clear()
            }

            function test_text() {
                const firstText = 'abc'
                const secondText = 'def'

                objectUnderTest.input = firstText
                verify(objectUnderTest.newText, firstText)
                compare(textChangedSpy.count, 1)

                objectUnderTest.input = secondText
                verify(objectUnderTest.newText, secondText)
                compare(textChangedSpy.count, 2)
            }
        }
    }

}
