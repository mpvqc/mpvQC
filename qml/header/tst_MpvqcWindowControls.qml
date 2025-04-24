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

    name: "MpvqcWindowControls"
    when: windowShown
    width: 400
    height: 400
    visible: true

    Component {
        id: objectUnderTest

        MpvqcWindowControls {
            id: __objectUnderTest

            property bool minimizeFuncCalled: false
            property bool maximizeFuncCalled: false
            property bool closeFuncCalled: false

            mpvqcApplication: QtObject {
                property bool maximized: false
                function showMinimized() {
                    __objectUnderTest.minimizeFuncCalled = true;
                }
                function toggleMaximized() {
                    __objectUnderTest.maximizeFuncCalled = true;
                }
                function close() {
                    __objectUnderTest.closeFuncCalled = true;
                }
            }
        }
    }

    function test_minimize() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        control.minimizeButton.clicked();
        verify(control.minimizeFuncCalled);
    }

    function test_maximize_data() {
        return [
            {
                maximizedInitial: false,
                iconSubstring: "open_in_full_black",
                tag: "maximize"
            },
            {
                maximizedInitial: true,
                iconSubstring: "close_fullscreen_black",
                tag: "minimize"
            },
        ];
    }

    function test_maximize(data) {
        const control = createTemporaryObject(objectUnderTest, testCase, {
            "mpvqcApplication.maximized": data.maximizedInitial
        });
        verify(control);
        verify(control.maximizeButton.icon.source.toString().includes(data.iconSubstring));

        control.maximizeButton.clicked();
        verify(control.maximizeFuncCalled);
    }

    function test_close() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        control.closeButton.clicked();
        verify(control.closeFuncCalled);
    }
}
