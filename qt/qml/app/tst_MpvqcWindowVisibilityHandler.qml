// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtTest

TestCase {
    id: testCase

    readonly property int cNORMAL: 1
    readonly property int cMAXIMIZED: 2
    readonly property int cFULLSCREEN: 3

    width: 400
    height: 400
    visible: true
    when: windowShown
    name: "MpvqcWindowVisibilityHandler"

    Component {
        id: objectUnderTest

        MpvqcWindowVisibilityHandler {
            id: __objectUnderTest

            property int cVisibility: -1

            mpvqcApplication: QtObject {
                property bool fullscreen: false
                property bool maximized: false
                property bool wasMaximizedBefore: false
                function showNormal() {
                    __objectUnderTest.cVisibility = testCase.cNORMAL;
                }
                function showMaximized() {
                    __objectUnderTest.cVisibility = testCase.cMAXIMIZED;
                }
                function showFullScreen() {
                    __objectUnderTest.cVisibility = testCase.cFULLSCREEN;
                }
            }
        }
    }

    function test_maximize_data() {
        return [
            {
                tag: "not max",
                maximized: false,
                wasMaximizedBefore: false,
                expectedVisibility: testCase.cMAXIMIZED
            },
            {
                tag: "max",
                maximized: true,
                wasMaximizedBefore: false,
                expectedVisibility: testCase.cNORMAL
            },
        ];
    }

    function test_maximize(data) {
        const control = createTemporaryObject(objectUnderTest, testCase, {
            maximized: data.maximized
        });
        verify(control);

        control.toggleMaximized();
        compare(control.cVisibility, data.expectedVisibility);
    }

    function test_toggleFullScreen_data() {
        return [
            {
                tag: "no full, not max before -> full",
                fullscreen: false,
                wasMaximizedBefore: false,
                expectedVisibility: testCase.cFULLSCREEN
            },
            {
                tag: "no full, max before -> full",
                fullscreen: false,
                wasMaximizedBefore: true,
                expectedVisibility: testCase.cFULLSCREEN
            },
            {
                tag: "full, not max before -> normal",
                fullscreen: true,
                wasMaximizedBefore: false,
                expectedVisibility: testCase.cNORMAL
            },
            {
                tag: "full, max before -> max",
                fullscreen: true,
                wasMaximizedBefore: true,
                expectedVisibility: testCase.cMAXIMIZED
            },
        ];
    }

    function test_toggleFullScreen(data) {
        const control = createTemporaryObject(objectUnderTest, testCase, {
            fullscreen: data.fullscreen
        });
        verify(control);

        control.wasMaximizedBefore = data.wasMaximizedBefore;
        control.toggleFullScreen();
        compare(control.cVisibility, data.expectedVisibility);
    }
}
