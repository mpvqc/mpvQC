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


import QtQuick.Controls
import QtTest


MpvqcQuitHandler {
    id: objectUnderTest
    width: 400
    height: 400

    property bool closeFuncCalled: false

    canClose: false
    mpvqcApplication: ApplicationWindow {
        function close() {
            objectUnderTest.closeFuncCalled = true
        }
    }

    TestCase {
        name: "MpvqcQuitHandler"
        when: windowShown

        function cleanup() {
            objectUnderTest.canClose = false
            objectUnderTest.closeFuncCalled = false
            objectUnderTest.userConfirmedClose = false
        }

        function test_quit() {
            objectUnderTest.canClose = true
            objectUnderTest.requestClose()
            verify(objectUnderTest.userConfirmedClose)
            verify(objectUnderTest.closeFuncCalled)
        }

        function test_quit_closeRejected() {    // skip('- flaky in CI')
            objectUnderTest.requestClose()
            verify(!objectUnderTest.closeFuncCalled)
            verify(!objectUnderTest.userConfirmedClose)
            objectUnderTest.quitDialog.reject()
            verify(!objectUnderTest.userConfirmedClose)
            verify(!objectUnderTest.closeFuncCalled)
        }

        function test_quit_closeAccepted() {    // skip('- flaky in CI')
            objectUnderTest.requestClose()
            verify(!objectUnderTest.closeFuncCalled)
            verify(!objectUnderTest.userConfirmedClose)
            objectUnderTest.quitDialog.accept()
            verify(objectUnderTest.closeFuncCalled)
            verify(objectUnderTest.userConfirmedClose)
        }

    }

 }
