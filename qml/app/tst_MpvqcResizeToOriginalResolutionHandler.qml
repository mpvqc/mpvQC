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

    property int screenWidth: 2560
    property int screenHeight: 1440

    width: 400
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcResizeToOriginalResolutionHandler"

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
                    property int scaledWidth: 854
                    property int scaledHeight: 480
                    property bool video_loaded: false
                }
            }
            header: QtObject {
                property int height: 40
            }
            splitView: QtObject {
                property int height: 640
                property int tableContainerHeight: 0
                property int tableContainerWidth: 0
                property int draggerHeight: 0
                property int draggerWidth: 0
                property int setWidth: 0
                property int setHeight: 0
                function setPreferredTableSize(width, height) {
                    setWidth = width;
                    setHeight = height;
                }
            }
        }
    }

    function test_canResize() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        control.mpvqcApplication.fullscreen = false;
        control.mpvqcApplication.maximized = false;
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.video_loaded = false;
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.scaledWidth = 0;
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.scaledHeight = 0;
        control.availableScreenWidth = 2560;
        control.availableScreenHeight = 1440;
        verify(!control.canResize());

        control.mpvqcApplication.fullscreen = false;
        control.mpvqcApplication.maximized = false;
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.video_loaded = true;
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.scaledWidth = 1280;
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.scaledHeight = 720;
        control.availableScreenWidth = 2560;
        control.availableScreenHeight = 1440;
        verify(control.canResize());

        control.mpvqcApplication.fullscreen = true;
        control.mpvqcApplication.maximized = false;
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.video_loaded = true;
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.scaledWidth = 1280;
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.scaledHeight = 720;
        control.availableScreenWidth = 2560;
        control.availableScreenHeight = 1440;
        verify(!control.canResize());

        control.mpvqcApplication.fullscreen = false;
        control.mpvqcApplication.maximized = true;
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.video_loaded = true;
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.scaledWidth = 1280;
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.scaledHeight = 720;
        control.availableScreenWidth = 2560;
        control.availableScreenHeight = 1440;
        verify(!control.canResize());

        control.mpvqcApplication.fullscreen = false;
        control.mpvqcApplication.maximized = false;
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.video_loaded = true;
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.scaledWidth = 1280;
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.scaledHeight = 720;
        control.availableScreenWidth = 1368;
        control.availableScreenHeight = 768;
        verify(control.canResize());

        control.mpvqcApplication.fullscreen = false;
        control.mpvqcApplication.maximized = false;
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.video_loaded = true;
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.scaledWidth = 1280;
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.scaledHeight = 720;
        control.availableScreenWidth = 1280;
        control.availableScreenHeight = 720;
        verify(!control.canResize());
    }

    function test_resizeVideoInVerticalSplitView() {
        let control;

        control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        control.availableScreenWidth = 2560 * 0.95;
        control.availableScreenHeight = 1440 * 0.95;
        control.mpvqcApplication.width = 1280;
        control.mpvqcApplication.height = 720;
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.scaledWidth = 854;
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.scaledHeight = 480;
        control.splitView.draggerHeight = 6;
        control.splitView.tableContainerHeight = 200;
        control.resizeVideoInVerticalSplitView();
        compare(control.mpvqcApplication.width, 866);
        compare(control.mpvqcApplication.height, 738);
        compare(control.splitView.setWidth, 854);
        compare(control.splitView.setHeight, 200);

        control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        control.availableScreenWidth = 2560 * 0.95;
        control.availableScreenHeight = 1440 * 0.95;
        control.mpvqcApplication.width = 1280;
        control.mpvqcApplication.height = 1200;
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.scaledWidth = 854;
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.scaledHeight = 480;
        control.splitView.draggerHeight = 6;
        control.splitView.tableContainerHeight = 900;
        control.resizeVideoInVerticalSplitView();
        compare(control.mpvqcApplication.width, 866);
        compare(control.mpvqcApplication.height, 1368);
        compare(control.splitView.setWidth, 854);
        compare(control.splitView.setHeight, 830);
    }

    function test_resizeVideoInHorizontalSplitView() {
        let control;

        control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        control.availableScreenWidth = 2560 * 0.95;
        control.availableScreenHeight = 1440 * 0.95;
        control.mpvqcApplication.width = 1280;
        control.mpvqcApplication.height = 720;
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.scaledWidth = 854;
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.scaledHeight = 480;
        control.splitView.draggerWidth = 6;
        control.splitView.tableContainerWidth = 200;
        control.resizeVideoInHorizontalSplitView();
        compare(control.mpvqcApplication.width, 1072);
        compare(control.mpvqcApplication.height, 532);
        compare(control.splitView.setWidth, 200);
        compare(control.splitView.setHeight, 480);

        control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        control.availableScreenWidth = 2560 * 0.95;
        control.availableScreenHeight = 1440 * 0.95;
        control.mpvqcApplication.width = 1280;
        control.mpvqcApplication.height = 1200;
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.scaledWidth = 854;
        control.mpvqcApplication.mpvqcMpvPlayerPropertiesPyObject.scaledHeight = 480;
        control.splitView.draggerWidth = 6;
        control.splitView.tableContainerWidth = 900;
        control.resizeVideoInHorizontalSplitView();
        compare(control.mpvqcApplication.width, 1772);
        compare(control.mpvqcApplication.height, 532);
        compare(control.splitView.setWidth, 900);
        compare(control.splitView.setHeight, 480);
    }
}
