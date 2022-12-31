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

    property int screenWidth: 2560
    property int screenHeight: 1440

    width: 400
    height: 400
    visible: true
    when: windowShown
    name: 'MpvqcResizeToOriginalResolutionHandler'

    Component { id: signalSpy; SignalSpy {} }

    Component {
        id: objectUnderTest

        MpvqcResizeToOriginalResolutionHandler {
            mpvqcApplication: QtObject {
                property bool fullscreen: false
                property bool maximized: false
                property int width: 1280
                property int height: 720
                property int windowBorder: 6
                property var mpvqcMpvPlayerPropertiesPyObject: QtObject {
                    property int width: 854
                    property int height: 480
                    property bool video_loaded: false
                }
            }
            header: QtObject {
                property int height: 40
            }
            footer: QtObject {
                property int height: 28
            }
            splitView: QtObject {
                property int height: 640
                property var playerContainer: QtObject {
                    property int height: 0
                    property int setWidth: 0
                    property int setHeight: 0
                    function setPreferredSizes(width, height) { setWidth = width; setHeight = height }
                }
                property var tableContainer: QtObject {
                    property int height: 0
                    property int setWidth: 0
                    property int setHeight: 0
                    function setPreferredSizes(width, height) { setWidth = width; setHeight = height }
                }
            }
        }
    }

    function test_canResize() {
        const control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        control.mpvqcApplication.fullscreen = false
        control.mpvqcApplication.maximized = false
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.video_loaded = false
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.width = 0
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.height = 0
        control.availableScreenWidth = 2560
        control.availableScreenHeight = 1440
        verify(!control.canResize())

        control.mpvqcApplication.fullscreen = false
        control.mpvqcApplication.maximized = false
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.video_loaded = true
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.width = 1280
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.height = 720
        control.availableScreenWidth = 2560
        control.availableScreenHeight = 1440
        verify(control.canResize())

        control.mpvqcApplication.fullscreen = true
        control.mpvqcApplication.maximized = false
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.video_loaded = true
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.width = 1280
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.height = 720
        control.availableScreenWidth = 2560
        control.availableScreenHeight = 1440
        verify(!control.canResize())

        control.mpvqcApplication.fullscreen = false
        control.mpvqcApplication.maximized = true
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.video_loaded = true
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.width = 1280
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.height = 720
        control.availableScreenWidth = 2560
        control.availableScreenHeight = 1440
        verify(!control.canResize())

        control.mpvqcApplication.fullscreen = false
        control.mpvqcApplication.maximized = false
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.video_loaded = true
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.width = 1280
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.height = 720
        control.availableScreenWidth = 1368
        control.availableScreenHeight = 768
        verify(control.canResize())

        control.mpvqcApplication.fullscreen = false
        control.mpvqcApplication.maximized = false
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.video_loaded = true
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.width = 1280
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.height = 720
        control.availableScreenWidth = 1280
        control.availableScreenHeight = 720
        verify(!control.canResize())
    }

    function test_resizeVideoInVerticalSplitView() {
        let control

        control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        control.availableScreenWidth = 2560 * 0.95
        control.availableScreenHeight = 1440 * 0.95
        control.mpvqcApplication.width = 1280
        control.mpvqcApplication.height = 720
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.width = 854
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.height = 480
        control.splitView.playerContainer.height = 434
        control.splitView.tableContainer.height = 200
        control.resizeVideoInVerticalSplitView()
        compare(control.mpvqcApplication.width, 866)
        compare(control.mpvqcApplication.height, 766)
        compare(control.splitView.playerContainer.setWidth, 854)
        compare(control.splitView.playerContainer.setHeight, 480)
        compare(control.splitView.tableContainer.setWidth, 854)
        compare(control.splitView.tableContainer.setHeight, 200)


        control = createTemporaryObject(objectUnderTest, testCase)
        verify(control)

        control.availableScreenWidth = 2560 * 0.95
        control.availableScreenHeight = 1440 * 0.95
        control.mpvqcApplication.width = 1280
        control.mpvqcApplication.height = 1200
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.width = 854
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.height = 480
        control.splitView.height = 1000
        control.splitView.playerContainer.height = 94
        control.splitView.tableContainer.height = 900
        control.resizeVideoInVerticalSplitView()
        compare(control.mpvqcApplication.width, 866)
        compare(control.mpvqcApplication.height, 1366)
        compare(control.splitView.playerContainer.setWidth, 854)
        compare(control.splitView.playerContainer.setHeight, 480)
        compare(control.splitView.tableContainer.setWidth, 854)
        compare(control.splitView.tableContainer.setHeight, 800)
    }

}
