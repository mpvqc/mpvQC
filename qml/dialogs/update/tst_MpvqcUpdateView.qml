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

import settings


TestCase {
    id: testCase

    visible: true
    when: windowShown
    name: 'MpvqcUpdateView'

    Component {
        id: objectUnderTest

        MpvqcUpdateView {}
    }

    function _mockVersion(version: string) {
        Qt.application.version = version
    }

    function _mockResponse(control, status: int, body: string) {
        control.request = createTemporaryQmlObject(`
        import QtQuick

        QtObject {
            property int status: ${status}
            property string responseText: '${body}'
        }`, control)
    }

    function test_loading() {
        const control = createTemporaryObject(objectUnderTest, testCase, {'trigger.running': false})
        verify(control)

        compare(control.title, "Checking for Updates...")
        compare(control.text, "Loading...")
    }

    function test_response200Up2Date() {
        const control = createTemporaryObject(objectUnderTest, testCase, {'trigger.running': false})
        verify(control)

        _mockVersion("0.8.0")
        _mockResponse(control, 200, '{"latest": "0.8.0"}')
        control.onRequestDone()

        compare(control.title, "👌")
        compare(control.text, "You are already using the most recent version of mpvQC!")
    }

    function test_response200OutdatedVersion() {
        const control = createTemporaryObject(objectUnderTest, testCase, {'trigger.running': false})
        verify(control)

        _mockVersion("0.8.0")
        _mockResponse(control, 200, '{"latest": "0.8.1"}')
        control.onRequestDone()

        compare(control.title, "New Version Available")
        verify(control.text.startsWith("<html>"))
    }

    function test_response400() {
        const control = createTemporaryObject(objectUnderTest, testCase, {'trigger.running': false})
        verify(control)

        _mockResponse(control, 400, '')
        control.onRequestDone()

        compare(control.title, "Server Error")
        compare(control.text, "The server returned error code 400.")
    }

    function test_error() {
        const control = createTemporaryObject(objectUnderTest, testCase, {
            'trigger.running': false,
            'mpvqcUpdateUrl': 'httpshttps://'
        })
        verify(control)

        control.checkForUpdate()

        wait(25)

        compare(control.title, "Server Not Reachable")
        compare(control.text, "A connection to the server could not be established.")
    }

}
