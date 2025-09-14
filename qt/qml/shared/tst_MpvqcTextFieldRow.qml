// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtTest

Item {
    id: testHelper

    width: 400
    height: 400

    MpvqcTextFieldRow {
        id: objectUnderTest

        property string newText: ''

        prefWidth: testHelper.width

        onTextChanged: text => {
            objectUnderTest.newText = text;
        }

        TestCase {
            name: "MpvqcTextFieldRow"

            SignalSpy {
                id: textChangedSpy
                target: objectUnderTest
                signalName: "textChanged"
            }

            function init() {
                objectUnderTest.newText = '';
                textChangedSpy.clear();
            }

            function test_text() {
                const firstText = "abc";
                const secondText = "def";

                objectUnderTest.input = firstText;
                verify(objectUnderTest.newText, firstText);
                compare(textChangedSpy.count, 1);

                objectUnderTest.input = secondText;
                verify(objectUnderTest.newText, secondText);
                compare(textChangedSpy.count, 2);
            }
        }
    }
}
