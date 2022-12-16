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


MpvqcFooter {
    id: objectUnderTest

    width: 400
    height: 400

    mpvqcApplication: QtObject {
        property bool maximized: false
        property var mpvqcSettings: QtObject {
            property int timeFormat: -1
            property bool statusbarPercentage: false
        }
        property var mpvqcMpvPlayerPropertiesPyObject: QtObject {
            property bool video_loaded: false
            property real percent_pos: 10.0
            property real duration: 10.0
            property real time_pos: 10.0
            property real time_remaining: 10.0
        }
        property var mpvqcLabelWidthCalculator: QtObject {
            function calculateWidthFor(items, parent) {}
        }
        property var mpvqcTimeFormatUtils: QtObject {
            function formatTimeToString(seconds) {}
            function formatTimeToStringShort(seconds) {}
        }
    }

    TestCase {
        name: "MpvqcFooter"
        when: windowShown

        function init() {
            _menuMock.openCalled = false
        }

        QtObject {
            id: _menuMock
            property bool openCalled: false
            function open() { openCalled = true }
        }

        function test_open_menu() {
            objectUnderTest.formattingOptionsButton.menu = _menuMock
            mouseClick(objectUnderTest.formattingOptionsButton)
            verify(_menuMock.openCalled)
        }

    }

}
