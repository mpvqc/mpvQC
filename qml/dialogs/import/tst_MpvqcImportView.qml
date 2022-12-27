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


MpvqcImportView {
    id: objectUnderTest

    mpvqcApplication: QtObject {
        property var mpvqcSettings: QtObject {
            property var importWhenVideoLinkedInDocument: 2
        }
    }

    width: 400
    height: 400

    TestCase {
        name: "MpvqcImportView"
        when: windowShown

        function init() {
            objectUnderTest.mpvqcApplication.mpvqcSettings.importWhenVideoLinkedInDocument = 2
        }

        function test_preselected() {
            verify(!objectUnderTest.selectionAlways.checked)
            verify(!objectUnderTest.selectionAsk.checked)
            verify(objectUnderTest.selectionNever.checked)
        }

        function test_selection() {
            mouseClick(objectUnderTest.selectionAlways)
            verify(objectUnderTest.selectionAlways.checked)

            mouseClick(objectUnderTest.selectionAsk)
            verify(objectUnderTest.selectionAsk.checked)

            mouseClick(objectUnderTest.selectionNever)
            verify(objectUnderTest.selectionNever.checked)
        }

    }

}
