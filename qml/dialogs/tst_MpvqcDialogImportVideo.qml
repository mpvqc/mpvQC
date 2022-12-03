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


Item {
    id: testHelper
    width: 400
    height: 400

    property bool openVideoCalled: false

    MpvqcDialogImportVideo {
        id: objectUnderTest

        mpvqcApplication: QtObject {
            property var mpvqcManager: QtObject {
                function openVideo(video) { testHelper.openVideoCalled = true }
            }
            property var mpvqcSettings: QtObject {
                property string lastDirectoryVideo: 'initial directory'
            }
        }
    }

    TestCase {
        name: "MpvqcDialogImportVideo"
        when: windowShown

        function test_import() { skip('- flaky since Qt 6.4.1')
            imitateHuman()

            verify(testHelper.openVideoCalled)
            verify(!objectUnderTest.mpvqcSettings.lastDirectoryVideo.toString().includes('initial directory'))
        }

        function imitateHuman() {
            objectUnderTest.currentFolder = 'some directory'
            objectUnderTest.accept()
        }
    }

}
