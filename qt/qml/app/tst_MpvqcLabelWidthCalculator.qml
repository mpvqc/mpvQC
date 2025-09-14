// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material
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
            property real duration: 0
        }
        property var mpvqcSettings: QtObject {
            property var commentTypes: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
            property string language: "language"
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
