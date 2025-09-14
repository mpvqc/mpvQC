// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

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
