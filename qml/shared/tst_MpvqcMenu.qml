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

    MpvqcMenu {
        id: objectUnderTest1

        Action { text: qsTranslate("MainWindow", "Short text") }
    }

    MpvqcMenu {
        id: objectUnderTest2

        Action { text: qsTranslate("MainWindow", "Short text") }
        MenuSeparator { }
    }

    MpvqcMenu {
        id: objectUnderTest3

        Action { text: qsTranslate("MainWindow", "Very very long text so that we can compare") }
    }

    TestCase {
        name: "MpvqcMenu"

        function test_width_data() {
            return [
                { tag: 'same', equals: 'equals', obj1: objectUnderTest1, obj2: objectUnderTest2 },
                { tag: 'different', obj1: objectUnderTest1, obj2: objectUnderTest3 },
            ]
        }

        function test_width(data) {
            if (data.equals) {
                verify(data.obj1.width === data.obj2.width)
            } else {
                verify(data.obj1.width < data.obj2.width)
            }
        }
    }

}
