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

    width: 400
    height: 400
    visible: true
    when: windowShown
    name: 'MpvqcMenuVideo'

    Component { id: signalSpy; SignalSpy {} }

    Component {
        id: dialogMock

        QtObject {
            property bool openCalled: false
            signal closed()
            function open() { openCalled = true }
        }
    }

    Component {
        id: objectUnderTest

        MpvqcMenuVideo {
            mpvqcApplication: QtObject {
                property var mpvqcManager: QtObject {}
                property var mpvqcSettings: QtObject {
                    property string lastDirectoryVideo: 'initial directory'
                    property string lastDirectorySubtitles: 'initial directory'
                }
                property var supportedSubtitleFileExtensions: [ 'ass' ]
            }
        }
    }

    function test_importVideo() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        const mock = createTemporaryObject(dialogMock, testCase)
        verify(mock)

        control.openVideoAction.dialog = mock
        control.openVideoAction.trigger()
        verify(mock.openCalled)
    }

    function test_importSubtitles() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        const mock = createTemporaryObject(dialogMock, testCase)
        verify(mock)

        control.openSubtitlesAction.dialog = mock
        control.openSubtitlesAction.trigger()
        verify(mock.openCalled)
    }

    function test_resizeVideoToOriginalResolution() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        const spy = signalSpy.createObject(null, {target: control, signalName: 'resizeVideoTriggered'})
        verify(spy)

        control.resizeToOriginalResolutionAction.trigger()
        compare(spy.count, 1)
    }

}
