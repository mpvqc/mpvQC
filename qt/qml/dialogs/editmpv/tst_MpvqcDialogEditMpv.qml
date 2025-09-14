// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtTest

import "../../app"

TestCase {
    id: testCase

    width: 400
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcDialogEditMpv"

    Component {
        id: signalSpy

        SignalSpy {}
    }

    Component {
        id: objectUnderTest

        MpvqcDialogEditMpv {

            mpvqcApplication: QtObject {
                property var mpvqcPlayerFilesPyObject: QtObject {
                    property string default_mpv_conf_content: "default"
                    property url mpv_conf_url: Qt.resolvedUrl("")
                }
                property var mpvqcTheme: MpvqcTheme {
                    themeColorOption: 4
                    themeIdentifier: "Material You"
                }
            }
        }
    }

    function test_edit_accept() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        const acceptedSpy = createTemporaryObject(signalSpy, testCase, {
            target: control.editView,
            signalName: "accepted"
        });
        verify(acceptedSpy);

        const resetSpy = createTemporaryObject(signalSpy, testCase, {
            target: control.editView,
            signalName: "reset"
        });
        verify(resetSpy);

        control.editView.textArea.text = "changed by user";
        control.accepted();

        compare(acceptedSpy.count, 1);
        compare(resetSpy.count, 0);
    }

    function test_edit_reset() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        const acceptedSpy = createTemporaryObject(signalSpy, testCase, {
            target: control.editView,
            signalName: "accepted"
        });
        verify(acceptedSpy);

        const resetSpy = createTemporaryObject(signalSpy, testCase, {
            target: control.editView,
            signalName: "reset"
        });
        verify(resetSpy);

        control.editView.textArea.text = "changed by user";
        control.reset();

        compare(acceptedSpy.count, 0);
        compare(resetSpy.count, 1);
    }
}
