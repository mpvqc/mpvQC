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
