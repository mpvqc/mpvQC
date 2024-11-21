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
