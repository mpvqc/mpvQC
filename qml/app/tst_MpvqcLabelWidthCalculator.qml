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

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtTest

TestCase {
    id: testCase

    width: 400
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcLabelWidthCalculator"

    QtObject {
        id: testHelperMpvqcApplication

        property var mpvqcMpvPlayerPropertiesPyObject: QtObject {
            property var duration: 0
        }
        property var mpvqcSettings: QtObject {
            property var commentTypes: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
            property var language: "language"
        }
    }

    Label {
        id: testHelper
    }

    Component {
        id: commentTypeWidthCalculator

        MpvqcLabelWidthCalculator {
            property int calculateCounter: 0

            mpvqcApplication: testHelperMpvqcApplication

            function calculateWidthFor(texts, parent) {
                calculateCounter += 1;
                return 42;
            }
        }
    }

    Component {
        id: labelWidthCalculator

        MpvqcLabelWidthCalculator {
            mpvqcApplication: testHelperMpvqcApplication
        }
    }

    function test_commentTypesRecalculationTriggers() {
        const control = createTemporaryObject(commentTypeWidthCalculator, testCase);
        verify(control);

        const counter = control.calculateCounter;

        control.mpvqcApplication.mpvqcSettings.commentTypesChanged();
        compare(control.calculateCounter, counter + 1);

        control.mpvqcApplication.mpvqcSettings.languageChanged();
        compare(control.calculateCounter, counter + 2);
    }

    function test_calculateWidth() {
        const control = createTemporaryObject(labelWidthCalculator, testCase);
        verify(control);

        const smallWidth = control.calculateWidthFor(["a", "bb"], testHelper);
        const bigWidth = control.calculateWidthFor(["ccc", "dddd"], testHelper);
        verify(smallWidth < bigWidth);
    }
}
