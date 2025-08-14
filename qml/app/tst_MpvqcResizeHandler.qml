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

    readonly property string noVideoLoaded: ""
    readonly property string videoLoaded: "/path/given"

    property int screenWidth: 2560
    property int screenHeight: 1440

    width: 400
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcResizeHandler"

    Component {
        id: signalSpy

        SignalSpy {}
    }

    Component {
        id: objectUnderTest

        MpvqcResizeHandler {
            headerHeight: 40
            appBorderSize: 6
            splitViewHandleWidth: 6
            splitViewHandleHeight: 6
            splitViewTableContainerWidth: 640
            splitViewTableContainerHeight: 640
        }
    }

    function test_canResize_data() {
        return [
            {
                input: {
                    "videoWidth": 0,
                    "videoHeight": 0,
                    "isAppFullScreen": false,
                    "isAppMaximized": false,
                    "videoPath": testCase.noVideoLoaded,
                    "splitViewOrientation": Qt.Vertical,
                    "availableScreenWidth": 2560,
                    "availableScreenHeight": 1440
                },
                expected: false
            },
            {
                input: {
                    "videoWidth": 1280,
                    "videoHeight": 720,
                    "isAppFullScreen": false,
                    "isAppMaximized": false,
                    "videoPath": testCase.videoLoaded,
                    "splitViewOrientation": Qt.Vertical,
                    "availableScreenWidth": 2560,
                    "availableScreenHeight": 1440
                },
                expected: true
            },
            {
                input: {
                    "videoWidth": 1280,
                    "videoHeight": 720,
                    "isAppFullScreen": true,
                    "isAppMaximized": false,
                    "videoPath": testCase.videoLoaded,
                    "splitViewOrientation": Qt.Vertical,
                    "availableScreenWidth": 2560,
                    "availableScreenHeight": 1440
                },
                expected: false
            },
            {
                input: {
                    "videoWidth": 1280,
                    "videoHeight": 720,
                    "isAppFullScreen": false,
                    "isAppMaximized": true,
                    "videoPath": testCase.videoLoaded,
                    "splitViewOrientation": Qt.Vertical,
                    "availableScreenWidth": 2560,
                    "availableScreenHeight": 1440
                },
                expected: false
            },
            {
                input: {
                    "videoWidth": 1280,
                    "videoHeight": 720,
                    "isAppFullScreen": false,
                    "isAppMaximized": false,
                    "videoPath": testCase.videoLoaded,
                    "splitViewOrientation": Qt.Vertical,
                    "availableScreenWidth": 1368,
                    "availableScreenHeight": 768
                },
                expected: true
            },
            {
                input: {
                    "videoWidth": 1280,
                    "videoHeight": 720,
                    "isAppFullScreen": false,
                    "isAppMaximized": false,
                    "videoPath": testCase.videoLoaded,
                    "splitViewOrientation": Qt.Vertical,
                    "availableScreenWidth": 1280,
                    "availableScreenHeight": 720
                },
                expected: false
            },
        ];
    }

    function test_canResize(data) {
        const control = createTemporaryObject(objectUnderTest, testCase, data.input);
        verify(control);

        compare(control.canResize(), data.expected);
    }

    function test_resize_data() {
        return [
            {
                input: {
                    "videoWidth": 854,
                    "videoHeight": 480,
                    "isAppFullScreen": false,
                    "isAppMaximized": false,
                    "videoPath": testCase.videoLoaded,
                    "splitViewOrientation": Qt.Vertical,
                    "availableScreenWidth": 2560 * 0.95,
                    "availableScreenHeight": 1440 * 0.95,
                    "splitViewTableContainerHeight": 200
                },
                expected: {
                    "requestAppWindowWidth": 866,
                    "requestAppWindowHeight": 738,
                    "requestedTableWidth": 854,
                    "requestedTableHeight": 200
                }
            },
            {
                input: {
                    "videoWidth": 854,
                    "videoHeight": 480,
                    "isAppFullScreen": false,
                    "isAppMaximized": false,
                    "videoPath": testCase.videoLoaded,
                    "splitViewOrientation": Qt.Vertical,
                    "availableScreenWidth": 2560 * 0.95,
                    "availableScreenHeight": 1440 * 0.95,
                    "splitViewTableContainerHeight": 900
                },
                expected: {
                    "requestAppWindowWidth": 866,
                    "requestAppWindowHeight": 1368,
                    "requestedTableWidth": 854,
                    "requestedTableHeight": 830
                }
            },
            {
                input: {
                    "videoWidth": 854,
                    "videoHeight": 480,
                    "isAppFullScreen": false,
                    "isAppMaximized": false,
                    "videoPath": testCase.videoLoaded,
                    "splitViewOrientation": Qt.Horizontal,
                    "availableScreenWidth": 2560 * 0.95,
                    "availableScreenHeight": 1440 * 0.95,
                    "splitViewTableContainerWidth": 200
                },
                expected: {
                    "requestAppWindowWidth": 1072,
                    "requestAppWindowHeight": 532,
                    "requestedTableWidth": 200,
                    "requestedTableHeight": 480
                }
            },
            {
                input: {
                    "videoWidth": 854,
                    "videoHeight": 480,
                    "isAppFullScreen": false,
                    "isAppMaximized": false,
                    "videoPath": testCase.videoLoaded,
                    "splitViewOrientation": Qt.Horizontal,
                    "availableScreenWidth": 2560 * 0.95,
                    "availableScreenHeight": 1440 * 0.95,
                    "splitViewTableContainerWidth": 900
                },
                expected: {
                    "requestAppWindowWidth": 1772,
                    "requestAppWindowHeight": 532,
                    "requestedTableWidth": 900,
                    "requestedTableHeight": 480
                }
            },
        ];
    }

    function test_resize(data) {
        const control = createTemporaryObject(objectUnderTest, testCase, data.input);
        verify(control);

        const appWindowSpy = createTemporaryObject(signalSpy, testCase, {
            target: control,
            signalName: "appWindowSizeRequested"
        });
        verify(appWindowSpy);

        const tableSpy = createTemporaryObject(signalSpy, testCase, {
            target: control,
            signalName: "splitViewTableSizeRequested"
        });
        verify(tableSpy);

        if (control.splitViewOrientation === Qt.Vertical) {
            control.recalculateSizesForVerticalAppLayout();
        } else if (control.splitViewOrientation === Qt.Horizontal) {
            control.recalculateSizesForHorizontalAppLayout();
        }

        compare(appWindowSpy.count, 1);
        compare(tableSpy.count, 1);

        const [requestAppWindowWidth, requestAppWindowHeight] = appWindowSpy.signalArguments[0];
        compare(requestAppWindowWidth, data.expected.requestAppWindowWidth);
        compare(requestAppWindowHeight, data.expected.requestAppWindowHeight);

        const [requestTableWidth, requestTableHeight] = appWindowSpy.signalArguments[0];
        compare(requestTableWidth, data.expected.requestAppWindowWidth);
        compare(requestTableHeight, data.expected.requestAppWindowHeight);
    }
}
