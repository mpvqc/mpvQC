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

TestCase {
    id: testCase

    name: "MpvqcBackupView"
    when: windowShown
    width: 400
    height: 400
    visible: true

    Component {
        id: objectUnderTest

        MpvqcBackupView {
            mpvqcApplication: QtObject {
                property var mpvqcSettings: QtObject {
                    property bool backupEnabled: true
                    property int backupInterval: 90
                }
                property var mpvqcApplicationPathsPyObject: QtObject {
                    property url dir_backup: "file:///hello.txt"
                }
                property var mpvqcUtilityPyObject: QtObject {
                    function urlToAbsolutePath(url) {
                        return `${url}-as-abs-path`;
                    }
                }
            }
        }
    }

    function test_value_change() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        verifyTemporaryValues(control);

        control.accept();

        compare(control.mpvqcApplication.mpvqcSettings.backupEnabled, false);
        compare(control.mpvqcApplication.mpvqcSettings.backupInterval, 91);
    }

    function verifyTemporaryValues(control) {
        compare(control.mpvqcApplication.mpvqcSettings.backupEnabled, true);
        compare(control.mpvqcApplication.mpvqcSettings.backupInterval, 90);

        control.backupEnabledSwitch.checked = false;
        compare(control.currentBackupEnabled, false);

        control.backupIntervalSpinBox.increase();
        compare(control.currentBackupInterval, 91);
    }

    function test_reset() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        verifyTemporaryValues(control);

        compare(control.mpvqcApplication.mpvqcSettings.backupEnabled, true);
        compare(control.mpvqcApplication.mpvqcSettings.backupInterval, 90);
    }
}
