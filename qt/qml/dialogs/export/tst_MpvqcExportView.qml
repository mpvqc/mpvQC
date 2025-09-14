// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtTest

TestCase {
    id: testCase

    name: "MpvqcExportView"
    when: windowShown
    width: 400
    height: 400
    visible: true

    Component {
        id: objectUnderTest

        MpvqcExportView {
            mpvqcApplication: QtObject {
                property var mpvqcSettings: QtObject {
                    property string nickname: "nickname"
                    property bool writeHeaderDate: false
                    property bool writeHeaderGenerator: false
                    property bool writeHeaderNickname: false
                    property bool writeHeaderVideoPath: false
                }
            }
        }
    }

    function test_accept() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        changeValues(control);
        control.accept();

        compare(control.mpvqcApplication.mpvqcSettings.nickname, "nickname-edited");
        compare(control.mpvqcApplication.mpvqcSettings.writeHeaderDate, true);
        compare(control.mpvqcApplication.mpvqcSettings.writeHeaderGenerator, true);
        compare(control.mpvqcApplication.mpvqcSettings.writeHeaderNickname, true);
        compare(control.mpvqcApplication.mpvqcSettings.writeHeaderVideoPath, true);
    }

    function changeValues(control) {
        compare(control.currentNickname, "nickname");
        compare(control.currentWriteHeaderDate, false);
        compare(control.currentWriteHeaderGenerator, false);
        compare(control.currentWriteHeaderNickname, false);
        compare(control.currentWriteHeaderVideoPath, false);

        control.nicknameInput.input = "nickname-edited";
        control.dateToggle.toggle.toggle();
        control.generatorToggle.toggle.toggle();
        control.nicknameToggle.toggle.toggle();
        control.pathToggle.toggle.toggle();

        compare(control.currentNickname, "nickname-edited");
        compare(control.currentWriteHeaderDate, true);
        compare(control.currentWriteHeaderGenerator, true);
        compare(control.currentWriteHeaderNickname, true);
        compare(control.currentWriteHeaderVideoPath, true);
    }

    function test_reject() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        changeValues(control);
        compare(control.mpvqcApplication.mpvqcSettings.nickname, "nickname");
        compare(control.mpvqcApplication.mpvqcSettings.writeHeaderDate, false);
        compare(control.mpvqcApplication.mpvqcSettings.writeHeaderGenerator, false);
        compare(control.mpvqcApplication.mpvqcSettings.writeHeaderNickname, false);
        compare(control.mpvqcApplication.mpvqcSettings.writeHeaderVideoPath, false);
    }
}
