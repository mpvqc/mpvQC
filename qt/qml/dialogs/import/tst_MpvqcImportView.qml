// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

TestCase {
    id: testCase

    readonly property int initialImportPolicy: 1 // Ask every time

    name: "MpvqcImportView"
    when: windowShown
    width: 400
    height: 400
    visible: true

    Component {
        id: objectUnderTest

        MpvqcImportView {
            mpvqcApplication: QtObject {
                property var mpvqcSettings: QtObject {
                    property int importWhenVideoLinkedInDocument: testCase.initialImportPolicy
                }
            }
        }
    }

    function test_accept() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        compare(control.mpvqcSettings.importWhenVideoLinkedInDocument, testCase.initialImportPolicy);
        compare(control.currentImportPolicy, testCase.initialImportPolicy);

        control.importPolicyComboBox.activated(0);
        compare(control.currentImportPolicy, 0);

        control.accept();
        compare(control.mpvqcSettings.importWhenVideoLinkedInDocument, 0);
    }

    function test_reject() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        compare(control.mpvqcSettings.importWhenVideoLinkedInDocument, testCase.initialImportPolicy);
        compare(control.currentImportPolicy, testCase.initialImportPolicy);

        control.importPolicyComboBox.activated(0);
        compare(control.currentImportPolicy, 0);

        compare(control.mpvqcSettings.importWhenVideoLinkedInDocument, testCase.initialImportPolicy);
    }
}
