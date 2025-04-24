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

    MpvqcSwitchRow {
        id: objectUnderTest

        property bool newChecked: false

        prefWidth: testHelper.width

        onCheckedChanged: {
            objectUnderTest.newChecked = checked;
        }

        TestCase {
            name: "MpvqcSwitchRow"
            when: windowShown

            SignalSpy {
                id: toggledSpy
                target: objectUnderTest
                signalName: "toggled"
            }

            function init() {
                objectUnderTest.newChecked = false;
                toggledSpy.clear();
            }

            function test_toggle() {
                verify(!objectUnderTest.checked);

                mouseClick(objectUnderTest.toggle);
                compare(toggledSpy.count, 1);
                verify(objectUnderTest.checked);

                mouseClick(objectUnderTest.toggle);
                compare(toggledSpy.count, 2);
                verify(!objectUnderTest.checked);
            }
        }
    }
}
