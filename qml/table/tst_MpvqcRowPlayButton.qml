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
    name: "MpvqcRowPlayButton"

    Component {
        id: signalSpy
        SignalSpy {}
    }

    Component {
        id: objectUnderTest

        MpvqcRowPlayButton {
            tableInEditMode: false
        }
    }

    function test_click() {
        const control = createTemporaryObject(objectUnderTest, testCase);
        verify(control);

        const buttonPressedSpy = createTemporaryObject(signalSpy, testCase, {
            target: control,
            signalName: "buttonPressed"
        });
        verify(buttonPressedSpy);

        const playPressedSpy = createTemporaryObject(signalSpy, testCase, {
            target: control,
            signalName: "playPressed"
        });
        verify(playPressedSpy);

        control.tableInEditMode = false;
        mouseClick(control);
        compare(buttonPressedSpy.count, 1);
        compare(playPressedSpy.count, 1);

        buttonPressedSpy.clear();
        playPressedSpy.clear();

        control.tableInEditMode = true;
        mouseClick(control);
        compare(buttonPressedSpy.count, 1);
        compare(playPressedSpy.count, 0);
    }
}
