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

    property var mpvqcApplication: ApplicationWindow {}

    MpvqcDialog {
        id: objectUnderTest1
        mpvqcApplication: testHelper.mpvqcApplication

        Rectangle { property string title: 'title-1' }
    }

    MpvqcDialog {
        id: objectUnderTest2
        mpvqcApplication: testHelper.mpvqcApplication

        Rectangle { property string title: 'title-1' }
        Rectangle { property string title: 'title-2' }
    }

    MpvqcDialog {
        id: objectUnderTest3
        mpvqcApplication: testHelper.mpvqcApplication

        Rectangle { property string title: 'title-1' }
        Rectangle { property string title: 'title-2' }
        Rectangle { property string title: 'title-3' }
    }

    TestCase {
        name: "MpvqcDialog"

        function test_children_data() {
            return [
                { tag: '1x', expected: 1, testobject: objectUnderTest1 },
                { tag: '2x', expected: 2, testobject: objectUnderTest2 },
                { tag: '3x', expected: 3, testobject: objectUnderTest3 },
            ]
        }

        function test_children(data) {
            compare(data.testobject.bar.count, data.expected)
            compare(data.testobject.stack.count, data.expected)
        }
    }

}
