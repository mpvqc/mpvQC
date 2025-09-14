// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick
import QtQuick.Controls.Material
import QtTest

TestCase {
    id: testCase

    width: 400
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcQuitHandler"

    Component {
        id: objectUnderTest

        MpvqcQuitHandler {
            id: __objectUnderTest

            property bool closeFuncCalled: false

            canClose: false
            mpvqcApplication: ApplicationWindow {
                function close() {
                    __objectUnderTest.closeFuncCalled = true;
                }
            }
        }
    }

    function test_quit() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        control.canClose = true;
        control.requestClose();
        verify(control.userConfirmedClose);
        verify(control.closeFuncCalled);
    }

    function test_quitRejected() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        control.requestClose();
        verify(!control.closeFuncCalled);
        verify(!control.userConfirmedClose);

        control.quitDialog.reject();
        verify(!control.closeFuncCalled);
        verify(!control.userConfirmedClose);
    }

    function test_quitAccepted() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        control.requestClose();
        verify(!control.closeFuncCalled);
        verify(!control.userConfirmedClose);

        control.quitDialog.accept();
        verify(control.closeFuncCalled);
        verify(control.userConfirmedClose);
    }
}
