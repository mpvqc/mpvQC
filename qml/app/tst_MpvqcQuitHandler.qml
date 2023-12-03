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
import QtQuick.Controls
import QtTest


TestCase {
    id: testCase

    width: 400
    height: 400
    visible: true
    when: windowShown
    name: 'MpvqcQuitHandler'

    Component { id: signalSpy; SignalSpy {} }

    Component {
        id: objectUnderTest

        MpvqcQuitHandler {
            property bool closeFuncCalled: false

            canClose: false
            mpvqcApplication: ApplicationWindow {
                function close() { closeFuncCalled = true }
            }
        }
    }

    function test_quit() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        control.canClose = true
        control.requestClose()
        verify(control.userConfirmedClose)
        verify(control.closeFuncCalled)
    }

    function test_quitRejected() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        control.requestClose()
        verify(!control.closeFuncCalled)
        verify(!control.userConfirmedClose)

        control.quitDialog.reject()
        verify(!control.closeFuncCalled)
        verify(!control.userConfirmedClose)
    }

    function test_quitAccepted() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        control.requestClose()
        verify(!control.closeFuncCalled)
        verify(!control.userConfirmedClose)

        control.quitDialog.accept()
        verify(control.closeFuncCalled)
        verify(control.userConfirmedClose)
    }

}
